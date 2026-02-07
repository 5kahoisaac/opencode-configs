#!/usr/bin/env python3
"""
Memory Recall Script
Read-only memory retrieval with agent-based comparison
"""

import argparse
import glob
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional


def find_memory_files(memory_dir: str, memory_type: Optional[str] = None) -> List[Path]:
    """Find all memory files based on type filter."""
    memory_path = Path(memory_dir)

    if not memory_path.exists():
        return []

    if memory_type:
        type_dir = memory_path / memory_type
        if not type_dir.exists():
            return []

        # Find all markdown files in the type directory
        pattern = str(type_dir / "**/*.md")
        return [Path(f) for f in glob.glob(pattern, recursive=True)]
    else:
        # Find all markdown files in all subdirectories
        pattern = str(memory_path / "**/*.md")
        return [Path(f) for f in glob.glob(pattern, recursive=True)]


def read_memory_content(file_path: Path) -> str:
    """Read memory file content without modifications."""
    try:
        return file_path.read_text(encoding="utf-8").strip()
    except (UnicodeDecodeError, IOError) as e:
        return f"[Error reading file: {e}]"


def is_topic_match(content: str, topic: str) -> bool:
    """Check if content contains the topic."""
    return topic.lower() in content.lower()


def is_query_match(content: str, query: str) -> bool:
    """Check if content matches the full-text query."""
    return query.lower() in content.lower()


def find_matching_memories(
    memory_dir: str,
    memory_type: Optional[str] = None,
    topic: Optional[str] = None,
    query: Optional[str] = None,
) -> List[Dict]:
    """Find memories that match the criteria."""
    matching_memories = []

    # Find all relevant memory files
    memory_files = find_memory_files(memory_dir, memory_type)

    for file_path in memory_files:
        # Only search within content if filters are provided
        if topic or query:
            content = read_memory_content(file_path)

            # Check topic match
            topic_match = True
            if topic:
                topic_match = is_topic_match(content, topic)

            # Check query match
            query_match = True
            if query:
                query_match = is_query_match(content, query)

            if topic_match and query_match:
                matching_memories.append(
                    {
                        "path": str(file_path.relative_to(Path(memory_dir))),
                        "content": content,
                    }
                )
        else:
            # No filters, include all memories
            matching_memories.append(
                {
                    "path": str(file_path.relative_to(Path(memory_dir))),
                    "content": read_memory_content(file_path),
                }
            )

    return matching_memories


def format_recall_response(
    memories: List[Dict], search_type: Optional[str] = None
) -> str:
    """Format the recall response according to recall-template.md format."""
    response = []

    response.append("📋 Memories Recall")
    response.append("=" * 50)

    if not memories:
        response.append("No memories found")
    else:
        for i, memory in enumerate(memories, 1):
            response.append(f"\n📝 Memory {i}:")
            response.append(f"   📍 Path: ./opencode/memory/{memory['path']}")
            response.append(f"   📄 Content:")

            # Format content with proper indentation
            lines = memory["content"].split("\n")
            for line in lines:
                response.append(f"      {line}")

            # Add separator if not the last memory
            if i < len(memories):
                response.append("")

    response.append("\n" + "=" * 50)
    response.append("✅ Complete")

    return "\n".join(response)


def main():
    """Main function to handle arguments and execute memory recall."""
    parser = argparse.ArgumentParser(
        description="Recall memories from memory storage (read-only)"
    )

    parser.add_argument(
        "--type",
        type=str,
        help="Memory type to filter by (learning, architectural, decisions, problems, issues)",
    )

    parser.add_argument(
        "--topic", type=str, help="Topic to search for within memory content"
    )

    parser.add_argument(
        "--query", type=str, help="Full-text search query within memory content"
    )

    # Default memory directory path
    memory_dir = os.path.expanduser("~/.config/opencode/.opencode/memory")

    args = parser.parse_args()

    # Validate type argument if provided
    if args.type and args.type not in [
        "learning",
        "architectural",
        "decisions",
        "problems",
        "issues",
    ]:
        print(
            f"Error: Invalid memory type '{args.type}'. Valid types are: learning, architectural, decisions, problems, issues",
            file=sys.stderr,
        )
        sys.exit(1)

    # Find matching memories
    matching_memories = find_matching_memories(
        memory_dir=memory_dir, memory_type=args.type, topic=args.topic, query=args.query
    )

    # Format and display response
    formatted_response = format_recall_response(
        matching_memories, search_type=args.type
    )

    print(formatted_response)


if __name__ == "__main__":
    main()
