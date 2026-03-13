#!/usr/bin/env python3
"""
Academic Paper MCP Server
=========================
Exposes academic paper search and retrieval as MCP tools.

Usage:
    # Run directly
    python -m academic_mcp.server

    # Or install and run
    pip install -e .
    academic-mcp
"""

import os
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server.fastmcp import FastMCP
from academic import AcademicClient, Paper

# Initialize FastMCP
mcp = FastMCP("academic")

# Initialize client
_client = None


def get_client() -> AcademicClient:
    global _client
    if _client is None:
        api_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")  # allow-secret
        _client = AcademicClient(api_key)
    return _client


@mcp.tool()
def academic_search(
    query: str, sources: str = "semantic_scholar,arxiv,pubmed", limit: int = 10
) -> str:
    """
    Search for academic papers across multiple sources.

    Args:
        query: Search query string
        sources: Comma-separated sources to search (semantic_scholar, arxiv, pubmed)
        limit: Maximum results per source

    Returns:
        JSON string of search results
    """
    source_list = [s.strip() for s in sources.split(",")]
    client = get_client()
    results = client.search(query, sources=source_list, limit=limit)

    output = []
    for source, papers in results.items():
        output.append(f"=== {source.upper()} ({len(papers)} results) ===")
        for i, paper in enumerate(papers, 1):
            output.append(f"{i}. {paper.title}")
            output.append(
                f"   Authors: {', '.join(paper.authors[:3])}"
                + ("..." if len(paper.authors) > 3 else "")
            )
            output.append(f"   Year: {paper.year or 'N/A'}")
            output.append(f"   DOI: {paper.doi or 'N/A'}")
            output.append(f"   PDF: {paper.pdf_url or 'N/A'}")
            output.append("")

    return "\n".join(output)


@mcp.tool()
def academic_get_paper(identifier: str) -> str:
    """
    Get paper metadata by identifier.

    Args:
        identifier: Paper ID (DOI, PMID, arXiv ID, or Semantic Scholar ID)

    Returns:
        JSON string of paper metadata
    """
    client = get_client()
    paper = client.get_paper(identifier)

    if paper is None:
        return f"Paper not found: {identifier}"

    lines = [
        f"Title: {paper.title}",
        f"Authors: {', '.join(paper.authors)}",
        f"Year: {paper.year or 'N/A'}",
        f"DOI: {paper.doi or 'N/A'}",
        f"PMID: {paper.pmid or 'N/A'}",
        f"arXiv: {paper.arxiv_id or 'N/A'}",
        f"Venue: {paper.venue or 'N/A'}",
        f"Citations: {paper.citation_count}",
        f"PDF URL: {paper.pdf_url or 'N/A'}",
        f"Source: {paper.source}",
        f"Abstract: {paper.abstract[:500] + '...' if paper.abstract and len(paper.abstract) > 500 else paper.abstract or 'N/A'}",
    ]

    return "\n".join(lines)


@mcp.tool()
def academic_get_fulltext(identifier: str) -> str:
    """
    Get full text URL for a paper.

    Args:
        identifier: Paper ID (DOI, PMID, arXiv ID)

    Returns:
        URL to full text or PDF
    """
    client = get_client()
    url = client.get_fulltext_url(identifier)

    if url:
        return url
    else:
        return f"No full text available for {identifier}"


@mcp.tool()
def academic_download_pdf(identifier: str, output_dir: str = "./downloads") -> str:
    """
    Download PDF for a paper.

    Args:
        identifier: Paper ID (DOI, PMID, arXiv ID)
        output_dir: Directory to save PDF

    Returns:
        Path to downloaded file or error message
    """
    client = get_client()

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    filepath = client.download_pdf(identifier, output_dir)

    if filepath:
        return f"Downloaded: {filepath}"
    else:
        return f"Failed to download PDF for {identifier}"


@mcp.tool()
def academic_find_reading(topic: str, research_lane: str = "") -> str:
    """
    Find relevant academic papers for a research lane.

    Args:
        topic: Research topic or keywords
        research_lane: Optional research lane (e.g., R2-01)

    Returns:
        Formatted list of relevant papers
    """
    client = get_client()

    # Expand query with lane context
    if research_lane:
        query = f"{topic} {research_lane}"
    else:
        query = topic

    results = client.search(query, limit=15)

    output = [f"Search: {query}", ""]

    all_papers = []
    for source, papers in results.items():
        all_papers.extend(papers)

    # Sort by citation count
    all_papers.sort(key=lambda p: p.citation_count, reverse=True)

    for i, paper in enumerate(all_papers[:10], 1):
        output.append(f"{i}. {paper.title}")
        output.append(f"   {', '.join(paper.authors[:2])} ({paper.year or 'N/A'})")
        output.append(f"   Citations: {paper.citation_count}")
        output.append(f"   Source: {paper.source}")
        output.append(f"   PDF: {paper.pdf_url or 'N/A'}")
        output.append("")

    return "\n".join(output)


if __name__ == "__main__":
    # Run the server
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        # Development mode with stdio
        mcp.run()
    else:
        # Standard mode
        mcp.run(transport="stdio")
