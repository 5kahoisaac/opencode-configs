#!/usr/bin/env python3
"""
Memory Remember Script - Creates new memories or updates existing ones
Usage: python3 memory-remember.py --type <type> --title <title> --content <content> [--related <path>] [--confirm]
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


class MemoryRemember:
    def __init__(self):
        self.memory_root = Path.home() / ".config" / "opencode" / ".opencode" / "memory"
        self.template_path = Path(
            "skills/mnemonics/templates/memory/memory-template.md"
        )
        self.memory_types = {
            "learning": {"path": "learning", "section": "Examples"},
            "decision": {"path": "decision/architectural", "section": "Context"},
            "idea": {"path": "ideas", "section": "Details"},
            "todo": {"path": "todos", "section": "Tasks"},
            "reference": {"path": "reference", "section": "Documentation"},
            "default": {"path": "general", "section": "Content"},
        }

    def kebab_case(self, text: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

    def generate_iso_timestamp(self) -> str:
        return datetime.now().isoformat()

    def load_template(self) -> str:
        try:
            with open(self.template_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return """# {Memory Title}

- created at: {timestamp}
- last modified at: {timestamp}

## Overview

{Overview content goes here}

## Examples

{Examples content goes here}

## Related

{Related links and references go here}

## Content

{Memory content goes here}"""

    def parse_arguments(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description="Create or update a memory entry",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        parser.add_argument(
            "--type",
            type=str,
            required=True,
            help="Memory type (learning, decision, idea, todo, reference)",
        )
        parser.add_argument(
            "--title", type=str, required=True, help="Title of the memory"
        )
        parser.add_argument(
            "--content", type=str, required=True, help="Content of the memory"
        )
        parser.add_argument("--related", type=str, help="Path to related memory file")
        parser.add_argument(
            "--confirm", action="store_true", help="Skip confirmation prompts"
        )

        return parser.parse_args()

    def detect_intent_with_llm(self, content: str) -> str:
        content_lower = content.lower()
        if any(
            word in content_lower
            for word in ["learn", "study", "tutorial", "guide", "how to"]
        ):
            return "learning"
        elif any(
            word in content_lower
            for word in ["decision", "choose", "option", "architecture", "design"]
        ):
            return "decision"
        elif any(
            word in content_lower
            for word in ["idea", "thought", "concept", "brainstorm"]
        ):
            return "idea"
        elif any(
            word in content_lower
            for word in ["todo", "task", "fix", "implement", "build"]
        ):
            return "todo"
        elif any(
            word in content_lower
            for word in ["reference", "doc", "documentation", "manual", "guide"]
        ):
            return "reference"

        return "default"

    def find_similar_memories(
        self, content: str, title: str, memory_type: str
    ) -> List[Dict[str, Any]]:
        similar_memories = []
        target_dir = (
            self.memory_root
            / self.memory_types.get(memory_type, self.memory_types["default"])["path"]
        )

        if not target_dir.exists():
            return []

        content_keywords = set(re.findall(r"\b\w{3,}\b", content.lower()))
        title_keywords = set(re.findall(r"\b\w{3,}\b", title.lower()))

        for memory_file in target_dir.glob("*.md"):
            try:
                with open(memory_file, "r", encoding="utf-8") as f:
                    memory_content = f.read().lower()

                memory_title_match = re.search(r"# (.+)", memory_content)
                memory_title = (
                    memory_title_match.group(1)
                    if memory_title_match
                    else memory_file.stem
                )

                memory_keywords = set(re.findall(r"\b\w{3,}\b", memory_content))
                memory_title_keywords = set(
                    re.findall(r"\b\w{3,}\b", memory_title.lower())
                )

                content_overlap = len(content_keywords & memory_keywords) / len(
                    content_keywords | memory_keywords
                )
                title_overlap = len(title_keywords & memory_title_keywords) / len(
                    title_keywords | memory_title_keywords
                )

                similarity = (content_overlap * 0.7) + (title_overlap * 0.3)

                if similarity > 0.3:
                    similar_memories.append(
                        {
                            "file": memory_file,
                            "title": memory_title,
                            "similarity": similarity,
                            "path": str(memory_file.relative_to(self.memory_root)),
                        }
                    )

            except (FileNotFoundError, UnicodeDecodeError):
                continue

        return sorted(similar_memories, key=lambda x: x["similarity"], reverse=True)

    def get_memory_config(self, memory_type: str) -> Dict[str, str]:
        return self.memory_types.get(memory_type, self.memory_types["default"])

    def check_circular_dependency(self, current_path: str, related_path: str) -> bool:
        try:
            with open(related_path, "r", encoding="utf-8") as f:
                related_content = f.read()

            current_filename = Path(current_path).name
            return current_filename in related_content
        except FileNotFoundError:
            return False

    def create_memory_directory(self, memory_type: str) -> Path:
        config = self.get_memory_config(memory_type)
        target_dir = self.memory_root / config["path"]

        if not target_dir.exists():
            print(f"Directory missing, creating: {target_dir}")
            target_dir.mkdir(parents=True, exist_ok=True)

        return target_dir

    def render_memory_content(
        self, args: argparse.Namespace, template: str, is_update: bool = False
    ) -> str:
        timestamp = self.generate_iso_timestamp()

        content = template.replace("{Memory Title}", args.title)
        content = content.replace("{timestamp}", timestamp)

        config = self.get_memory_config(args.type)
        content_section = config["section"]

        content = content.replace(
            f"## {content_section}", f"## {content_section}\n\n{args.content}"
        )
        content = content.replace("{Overview content goes here}", f"{args.content}")
        content = content.replace("{Examples content goes here}", f"{args.content}")
        content = content.replace("{Memory content goes here}", f"{args.content}")
        content = content.replace("{Content goes here}", f"{args.content}")

        if args.related:
            try:
                related_path = Path(args.related)
                if not related_path.is_absolute():
                    related_path = Path.cwd() / related_path

                if self.check_circular_dependency(related_path.name, str(related_path)):
                    print(
                        "⚠️  Warning: Circular dependency detected in related memories"
                    )
                    related_section = (
                        f"## Related\n\n⚠️  Circular dependency with {related_path.name}"
                    )
                else:
                    related_section = (
                        f"## Related\n\n- [{related_path.stem}]({args.related})"
                    )

                content = content.replace(
                    "{Related links and references go here}", related_section
                )
            except Exception as e:
                print(f"⚠️  Warning: Could not process related memory: {e}")
                content = content.replace("{Related links and references go here}", "")
        else:
            content = content.replace("{Related links and references go here}", "")

        return content

    def confirm_action(self, action: str, details: str) -> bool:
        if hasattr(self, "_confirm_all") and self._confirm_all:
            return True

        try:
            response = input(f"✓ {action}: {details}\nProceed? (Y/n): ").strip().lower()
            return response in ["", "y", "yes"]
        except (EOFError, KeyboardInterrupt):
            return False

    def save_memory(
        self,
        args: argparse.Namespace,
        content: str,
        target_path: Path,
        is_update: bool = False,
    ) -> bool:
        try:
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)

            if is_update:
                print(f"✓ Updated: {args.title}")
            else:
                print(f"✓ Added: {args.title}")

            return True
        except Exception as e:
            print(f"❌ Error saving memory: {e}")
            return False

    def run(self):
        args = self.parse_arguments()

        self._confirm_all = args.confirm

        if args.type not in self.memory_types and args.type != "default":
            print(f"❌ Unknown memory type: {args.type}")
            print(f"Available types: {', '.join(self.memory_types.keys())}")
            sys.exit(1)

        target_dir = self.create_memory_directory(args.type)

        filename = f"{self.kebab_case(args.title)}.md"
        target_path = target_dir / filename

        is_update = target_path.exists()

        if is_update:
            print(f"📝 Memory already exists: {args.title}")
            if not self.confirm_action("Update existing memory", str(target_path)):
                print("❌ Update cancelled")
                return

        similar_memories = self.find_similar_memories(
            args.content, args.title, args.type
        )

        if similar_memories:
            print(f"🔍 Similar memory found:")
            for memory in similar_memories[:3]:
                print(f"  - {memory['title']} (similarity: {memory['similarity']:.2f})")

            if not self.confirm_action(
                "Update similar memory",
                f"{similar_memories[0]['title']} ({similar_memories[0]['similarity']:.2f})",
            ):
                print("❌ Update cancelled")
                return

        template = self.load_template()
        content = self.render_memory_content(args, template, is_update)

        if self.save_memory(args, content, target_path, is_update):
            print("✅ Complete")
        else:
            print("❌ Failed to save memory")
            sys.exit(1)


if __name__ == "__main__":
    script = MemoryRemember()
    script.run()
