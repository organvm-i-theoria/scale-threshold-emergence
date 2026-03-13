#!/usr/bin/env python3
"""
Academic Paper Client - Unified Interface
=========================================
Supports: Semantic Scholar, arXiv, PubMed/Europe PMC

Usage:
    from academic_client import AcademicClient

    client = AcademicClient()

    # Search all sources
    results = client.search("origin of life energy", sources=["semantic_scholar", "arxiv"])

    # Get paper by ID
    paper = client.get_paper("DOI:10.1126/science.169.3946.635")

    # Get full text URL
    fulltext = client.get_fulltext("PMID:12345678")
"""

import os
import time
import json
import requests
from dataclasses import dataclass, field, asdict
from typing import Optional
from urllib.parse import quote_plus, urljoin
import xml.etree.ElementTree as ET


@dataclass
class Paper:
    """Unified paper representation."""

    id: str
    title: str
    authors: list
    year: Optional[int] = None
    abstract: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    arxiv_id: Optional[str] = None
    pdf_url: Optional[str] = None
    source_url: Optional[str] = None
    venue: Optional[str] = None
    citation_count: int = 0
    source: str = ""

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}


class SemanticScholarClient:
    """Semantic Scholar API client."""

    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    def __init__(self, api_key: Optional[str] = None):  # allow-secret
        self.api_key = api_key or os.environ.get(  # allow-secret
            "SEMANTIC_SCHOLAR_API_KEY"  # allow-secret
        )  # allow-secret
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"x-api-key": self.api_key})  # allow-secret
        self.rate_limit = 1.0  # seconds between requests

    def search(self, query: str, limit: int = 10) -> list[Paper]:
        """Search for papers."""
        time.sleep(self.rate_limit)

        url = f"{self.BASE_URL}/paper/search"
        params = {
            "query": query,
            "limit": limit,
            "fields": "title,authors,year,abstract,doi,externalIds,venue,citationCount,openAccessPdf,url",
        }

        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        papers = []
        for item in data.get("data", []):
            pdf_url = None
            if item.get("openAccessPdf"):
                pdf_url = item["openAccessPdf"].get("url")

            external = item.get("externalIds", {})

            papers.append(
                Paper(
                    id=item.get("paperId", ""),
                    title=item.get("title", ""),
                    authors=[a.get("name", "") for a in item.get("authors", [])],
                    year=item.get("year"),
                    abstract=item.get("abstract"),
                    doi=external.get("DOI"),
                    arxiv_id=external.get("ArXiv"),
                    pdf_url=pdf_url,
                    source_url=item.get("url"),
                    venue=item.get("venue"),
                    citation_count=item.get("citationCount", 0),
                    source="semantic_scholar",
                )
            )

        return papers

    def get_paper(self, paper_id: str) -> Optional[Paper]:
        """Get paper by ID or DOI."""
        time.sleep(self.rate_limit)

        # Check if DOI
        if paper_id.startswith("DOI:") or "10." in paper_id:
            doi = paper_id.replace("DOI:", "").strip()
            paper_id = f"DOI:{doi}"

        url = f"{self.BASE_URL}/paper/{quote_plus(paper_id)}"
        params = {
            "fields": "title,authors,year,abstract,doi,externalIds,venue,citationCount,openAccessPdf,url"
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            item = response.json()

            pdf_url = None
            if item.get("openAccessPdf"):
                pdf_url = item["openAccessPdf"].get("url")

            external = item.get("externalIds", {})

            return Paper(
                id=item.get("paperId", ""),
                title=item.get("title", ""),
                authors=[a.get("name", "") for a in item.get("authors", [])],
                year=item.get("year"),
                abstract=item.get("abstract"),
                doi=external.get("DOI"),
                pmid=external.get("PubMed"),
                arxiv_id=external.get("ArXiv"),
                pdf_url=pdf_url,
                source_url=item.get("url"),
                venue=item.get("venue"),
                citation_count=item.get("citationCount", 0),
                source="semantic_scholar",
            )
        except Exception as e:
            print(f"Error fetching paper: {e}")
            return None


class ArxivClient:
    """arXiv API client."""

    BASE_URL = "http://export.arxiv.org/api/query"

    def __init__(self):
        self.rate_limit = 3.0  # arXiv rate limit

    def search(self, query: str, max_results: int = 10) -> list[Paper]:
        """Search arXiv."""
        time.sleep(self.rate_limit)

        params = {
            "search_query": f"all:{query}",
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending",
        }

        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        papers = []
        for entry in root.findall("atom:entry", ns):
            arxiv_id = entry.find("atom:id", ns).text.split("/")[-1]
            title = entry.find("atom:title", ns).text.replace("\n", " ").strip()
            abstract = entry.find("atom:summary", ns).text.replace("\n", " ").strip()

            authors = [
                a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)
            ]

            published = entry.find("atom:published", ns).text[:4]

            pdf_link = None
            for link in entry.findall("atom:link", ns):
                if link.get("title") == "pdf":
                    pdf_link = link.get("href")
                    break

            papers.append(
                Paper(
                    id=arxiv_id,
                    title=title,
                    authors=authors,
                    year=int(published) if published else None,
                    abstract=abstract,
                    arxiv_id=arxiv_id,
                    pdf_url=pdf_link,
                    source_url=f"https://arxiv.org/abs/{arxiv_id}",
                    source="arxiv",
                )
            )

        return papers

    def get_paper(self, arxiv_id: str) -> Optional[Paper]:
        """Get paper by arXiv ID."""
        # Clean ID
        arxiv_id = arxiv_id.replace("arxiv:", "").strip()

        results = self.search(f"id:{arxiv_id}", max_results=1)
        return results[0] if results else None


class PubmedClient:
    """PubMed/Europe PMC API client."""

    EPMC_BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest"
    PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def __init__(self):
        self.rate_limit = 1.0

    def search(self, query: str, limit: int = 10) -> list[Paper]:
        """Search PubMed/Europe PMC."""
        time.sleep(self.rate_limit)

        url = f"{self.EPMC_BASE}/search"
        params = {
            "query": query,
            "resulttype": "core",
            "format": "json",
            "pageSize": limit,
            "formatFields": "title,authorString,year,doi,pubType",
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        papers = []
        for hit in data.get("resultList", {}).get("result", []):
            papers.append(
                Paper(
                    id=hit.get("pubmedId", ""),
                    title=hit.get("title", ""),
                    authors=hit.get("authorString", "").split(", "),
                    year=int(hit.get("year")) if hit.get("year") else None,
                    doi=hit.get("doi"),
                    pmid=hit.get("pubmedId"),
                    source_url=f"https://pubmed.ncbi.nlm.nih.gov/{hit.get('pubmedId')}/",
                    source="pubmed",
                )
            )

        return papers

    def get_paper(self, identifier: str) -> Optional[Paper]:
        """Get paper by PMID or DOI."""
        time.sleep(self.rate_limit)

        # Determine if PMID or DOI
        if identifier.startswith("PMID:"):
            pmid = identifier.replace("PMID:", "").strip()
            url = f"{self.PUBMED_BASE}/esummary.fcgi"
            params = {"db": "pubmed", "id": pmid, "retmode": "json"}

            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                doc = data.get("result", {}).get(pmid, {})

                return Paper(
                    id=pmid,
                    title=doc.get("title", ""),
                    authors=[a.get("name", "") for a in doc.get("authors", [])],
                    year=int(doc.get("pubdate", "")[:4])
                    if doc.get("pubdate")
                    else None,
                    pmid=pmid,
                    source_url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                    source="pubmed",
                )
            except Exception as e:
                print(f"Error fetching paper: {e}")
                return None
        else:
            # Try as DOI
            doi = identifier.replace("DOI:", "").strip()
            return (
                self.search(f"DOI:{doi}", limit=1)[0]
                if self.search(f"DOI:{doi}", limit=1)
                else None
            )

    def get_fulltext_url(self, pmid: str) -> Optional[str]:
        """Get full text URL for a PMID."""
        time.sleep(self.rate_limit)

        url = f"{self.EPMC_BASE}/rest/{pmid}/fullTextXML"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Try to find PMC ID
                root = ET.fromstring(response.content)
                pmc = root.find(".//articleId[@idType='pmc']")
                if pmc is not None:
                    return f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc.text}/"
        except:
            pass

        return None


class AcademicClient:
    """Unified academic paper client."""

    def __init__(self, api_key: Optional[str] = None):  # allow-secret
        self.semantic_scholar = SemanticScholarClient(api_key)  # allow-secret
        self.arxiv = ArxivClient()
        self.pubmed = PubmedClient()

    def search(
        self, query: str, sources: Optional[list[str]] = None, limit: int = 10
    ) -> dict[str, list[Paper]]:
        """Search across multiple sources."""
        if sources is None:
            sources = ["semantic_scholar", "arxiv", "pubmed"]

        results = {}

        if "semantic_scholar" in sources:
            try:
                results["semantic_scholar"] = self.semantic_scholar.search(query, limit)
            except Exception as e:
                print(f"Semantic Scholar error: {e}")
                results["semantic_scholar"] = []

        if "arxiv" in sources:
            try:
                results["arxiv"] = self.arxiv.search(query, limit)
            except Exception as e:
                print(f"arXiv error: {e}")
                results["arxiv"] = []

        if "pubmed" in sources:
            try:
                results["pubmed"] = self.pubmed.search(query, limit)
            except Exception as e:
                print(f"PubMed error: {e}")
                results["pubmed"] = []

        return results

    def get_paper(
        self, identifier: str, source: Optional[str] = None
    ) -> Optional[Paper]:
        """Get paper by identifier (DOI, PMID, arXiv ID)."""
        # Auto-detect source
        if source is None:
            if (
                identifier.startswith("arxiv:")
                or identifier.startswith("arXiv:")
                or identifier.replace(".", "").isdigit()
            ):
                if "-" in identifier and not identifier.startswith("10."):
                    source = "arxiv"
                else:
                    source = "semantic_scholar"
            elif identifier.startswith("PMID:"):
                source = "pubmed"
            elif "10." in identifier:
                source = "semantic_scholar"
            else:
                source = "semantic_scholar"  # default

        if source == "arxiv":
            return self.arxiv.get_paper(identifier)
        elif source == "pubmed":
            return self.pubmed.get_paper(identifier)
        else:
            return self.semantic_scholar.get_paper(identifier)

    def get_fulltext_url(self, identifier: str) -> Optional[str]:
        """Get full text URL for a paper."""
        paper = self.get_paper(identifier)

        if paper and paper.pdf_url:
            return paper.pdf_url

        # Try PubMed for full text
        if paper and paper.pmid:
            return self.pubmed.get_fulltext_url(paper.pmid)

        return paper.source_url if paper else None

    def download_pdf(self, identifier: str, output_dir: str) -> Optional[str]:
        """Download PDF to output directory."""
        paper = self.get_paper(identifier)

        if not paper or not paper.pdf_url:
            print(f"No PDF available for {identifier}")
            return None

        # Download
        response = requests.get(paper.pdf_url)
        response.raise_for_status()

        # Determine filename
        safe_id = paper.id.replace("/", "_")
        filename = f"{safe_id}.pdf"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "wb") as f:
            f.write(response.content)

        return filepath


if __name__ == "__main__":
    import sys

    client = AcademicClient()

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"Searching for: {query}")
        results = client.search(query)

        for source, papers in results.items():
            print(f"\n=== {source.upper()} ===")
            for i, paper in enumerate(papers[:5], 1):
                print(f"{i}. {paper.title}")
                print(f"   Authors: {', '.join(paper.authors[:3])}")
                print(f"   Year: {paper.year}")
                print(f"   PDF: {paper.pdf_url or 'N/A'}")
