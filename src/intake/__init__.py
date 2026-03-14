#!/usr/bin/env python3
"""
Source Intake
=============
Ingests raw source materials (chat transcripts, research notes, documents)
into the knowledge engine.

Features:
- Parse chat transcript formats (ChatGPT, Claude, etc.)
- Normalize text encoding
- Extract prompt/response pairs
- Assign provenance metadata
- Queue for refinery processing
"""

import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class PromptResponsePair:
    """Represents a prompt/response pair from a transcript."""

    id: str
    prompt: str
    response: str
    source: str
    timestamp: Optional[str] = None
    metadata: dict = field(default_factory=dict)


@dataclass
class IntakeRecord:
    """Represents an ingested source."""

    id: str
    source_type: str
    content: str
    pairs: list = field(default_factory=list)
    provenance: dict = field(default_factory=dict)
    ingested_at: str = field(default_factory=lambda: datetime.now().isoformat())
    hash: str = ""


class SourceIntake:
    """Ingests raw source materials into the knowledge engine."""

    CHATGPT_PATTERN = re.compile(
        r"(?:Prompt:?\s*)?(.+?)(?=\n\s*(?:Response|Answer|Output):|\Z)",
        re.DOTALL | re.IGNORECASE,
    )
    RESPONSE_PATTERN = re.compile(
        r"(?:Response:?\s*)?(.+?)(?=\n\s*(?:Prompt|Response|Answer|$))",
        re.DOTALL | re.IGNORECASE,
    )
    CLAUDE_PATTERN = re.compile(
        r"(?:\[(?:Human|User)\]\s*)(.+?)(?=\n\s*\[(?:Assistant|AI)\]:|\Z)", re.DOTALL
    )
    CLAUDE_RESPONSE_PATTERN = re.compile(
        r"(?:\[Assistant\]:\s*)(.+?)(?=\n\s*\[(?:Human|User)\]:|\Z)", re.DOTALL
    )

    def __init__(self, output_dir: str = "./data/intake"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.encoding = "utf-8"
        self.queue = []

    def _normalize_encoding(self, content: str) -> str:
        """Normalize text encoding."""
        if isinstance(content, bytes):
            content = content.decode(self.encoding, errors="replace")
        content = content.replace("\r\n", "\n").replace("\r", "\n")
        return content

    def _compute_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content."""
        return hashlib.sha256(content.encode(self.encoding)).hexdigest()

    def _extract_chatgpt_pairs(self, content: str) -> list[PromptResponsePair]:
        """Extract prompt/response pairs from ChatGPT format."""
        pairs = []
        prompt_blocks = self.CHATGPT_PATTERN.findall(content)
        response_blocks = self.RESPONSE_PATTERN.findall(content)

        for i, (prompt, response) in enumerate(zip(prompt_blocks, response_blocks)):
            prompt = prompt.strip()
            response = response.strip()
            if prompt and response:
                pair_id = f"chatgpt_{self._compute_hash(prompt + response)[:12]}"
                pairs.append(
                    PromptResponsePair(
                        id=pair_id,
                        prompt=prompt,
                        response=response,
                        source="chatgpt",
                        metadata={"format": "chatgpt", "index": i},
                    )
                )

        return pairs

    def _extract_claude_pairs(self, content: str) -> list[PromptResponsePair]:
        """Extract prompt/response pairs from Claude format."""
        pairs = []
        prompts = self.CLAUDE_PATTERN.findall(content)
        responses = self.CLAUDE_RESPONSE_PATTERN.findall(content)

        for i, (prompt, response) in enumerate(zip(prompts, responses)):
            prompt = prompt.strip()
            response = response.strip()
            if prompt and response:
                pair_id = f"claude_{self._compute_hash(prompt + response)[:12]}"
                pairs.append(
                    PromptResponsePair(
                        id=pair_id,
                        prompt=prompt,
                        response=response,
                        source="claude",
                        metadata={"format": "claude", "index": i},
                    )
                )

        return pairs

    def _detect_format(self, content: str) -> str:
        """Detect the transcript format."""
        if "[Claude]" in content or "[Assistant]:" in content:
            return "claude"
        elif "Response:" in content or "Answer:" in content:
            return "chatgpt"
        elif "Human:" in content or "User:" in content:
            return "claude"
        return "unknown"

    def ingest_file(self, filepath: str) -> IntakeRecord:
        """
        Ingest a file into the knowledge engine.

        Args:
            filepath: Path to the file to ingest

        Returns:
            IntakeRecord with ingested content and extracted pairs
        """
        path = Path(filepath)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        content = path.read_text(encoding=self.encoding)
        return self.ingest_content(content, source_type="file", source_path=str(path))

    def ingest_content(
        self, content: str, source_type: str = "text", source_path: str = ""
    ) -> IntakeRecord:
        """
        Ingest content into the knowledge engine.

        Args:
            content: The content to ingest
            source_type: Type of source (file, url, text, transcript)
            source_path: Optional path or URL of the source

        Returns:
            IntakeRecord with ingested content and extracted pairs
        """
        content = self._normalize_encoding(content)
        content_hash = self._compute_hash(content)

        format_type = self._detect_format(content)

        pairs = []
        if format_type == "chatgpt":
            pairs = self._extract_chatgpt_pairs(content)
        elif format_type == "claude":
            pairs = self._extract_claude_pairs(content)

        record = IntakeRecord(
            id=content_hash[:16],
            source_type=source_type,
            content=content,
            pairs=pairs,
            provenance={
                "source_path": source_path,
                "format": format_type,
                "content_hash": content_hash,
                "pair_count": len(pairs),
            },
            hash=content_hash,
        )

        self.queue.append(record)
        return record

    def ingest_directory(
        self, dirpath: str, pattern: str = "*.txt"
    ) -> list[IntakeRecord]:
        """
        Ingest all files matching pattern in a directory.

        Args:
            dirpath: Path to directory
            pattern: Glob pattern for files to ingest

        Returns:
            List of IntakeRecords
        """
        path = Path(dirpath)
        records = []

        for filepath in path.glob(pattern):
            try:
                record = self.ingest_file(str(filepath))
                records.append(record)
            except Exception as e:
                print(f"Error ingesting {filepath}: {e}")

        return records

    def save_record(self, record: IntakeRecord) -> str:
        """Save intake record to JSON file."""
        output_path = self.output_dir / f"{record.id}.json"

        data = {
            "id": record.id,
            "source_type": record.source_type,
            "content": record.content,
            "pairs": [
                {
                    "id": p.id,
                    "prompt": p.prompt,
                    "response": p.response,
                    "source": p.source,
                    "timestamp": p.timestamp,
                    "metadata": p.metadata,
                }
                for p in record.pairs
            ],
            "provenance": record.provenance,
            "ingested_at": record.ingested_at,
            "hash": record.hash,
        }

        output_path.write_text(json.dumps(data, indent=2), encoding=self.encoding)
        return str(output_path)

    def process_queue(self) -> list[str]:
        """Process all queued records and save them."""
        output_paths = []
        for record in self.queue:
            path = self.save_record(record)
            output_paths.append(path)
        self.queue.clear()
        return output_paths

    def get_queued_count(self) -> int:
        """Get the number of records in the queue."""
        return len(self.queue)
