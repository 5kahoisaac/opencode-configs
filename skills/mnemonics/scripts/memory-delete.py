#!/usr/bin/env python3
"""
Memory Deletion Script
Deletes memories from the OpenCode memory system with safety checks.
"""

import argparse
import os
import glob
import re
from pathlib import Path


def find_memories(title=None, memory_type=None, topic=None):
    """Find matching memories based on search criteria."""
    memories = []

    base_memory_dir = Path.home() / ".config" / "opencode" / ".opencode" / "memory"

    for memory_dir in base_memory_dir.glob("*"):
        if memory_dir.is_dir() and memory_dir.name not in [".", ".."]:
            if memory_type and memory_dir.name != memory_type:
                continue

            for md_file in memory_dir.glob("**/*.md"):
                if title:
                    if not _title_matches(md_file, title):
                        continue

                if topic:
                    if not _topic_matches(md_file, topic):
                        continue

                memories.append(md_file)

    return memories


def _title_matches(memory_file, search_title):
    """Check if memory file title matches search title."""
    file_name = memory_file.stem.replace("-", " ").replace("_", " ")
    search_lower = search_title.lower()

    if search_lower in file_name.lower():
        return True

    # Also check file content for title
    try:
        with open(memory_file, "r", encoding="utf-8") as f:
            content = f.read()
            return search_lower in content.lower()
    except (IOError, UnicodeDecodeError):
        return False


def _topic_matches(memory_file, search_topic):
    """Check if memory file content matches search topic."""
    try:
        with open(memory_file, "r", encoding="utf-8") as f:
            content = f.read()
            return search_topic.lower() in content.lower()
    except (IOError, UnicodeDecodeError):
        return False


def find_linked_references(memory_file):
    """Find all memories that reference the given memory file."""
    base_dir = Path.home() / ".config" / "opencode" / ".opencode" / "memory"
    references = []
    memory_filename = memory_file.name

    for memory_dir in base_dir.glob("*"):
        if memory_dir.is_dir() and memory_dir.name not in [".", ".."]:
            for md_file in memory_dir.glob("**/*.md"):
                if md_file == memory_file:
                    continue

                try:
                    with open(md_file, "r", encoding="utf-8") as f:
                        content = f.read()
                        if memory_filename in content:
                            references.append(md_file)
                except (IOError, UnicodeDecodeError):
                    continue

                try:
                    with open(md_file, "r", encoding="utf-8") as f:
                        content = f.read()
                        if memory_filename in content:
                            references.append(md_file)
                except (IOError, UnicodeDecodeError):
                    continue

    return references


def remove_memory_reference(memory_file, reference_file):
    """Remove reference to memory_file from reference_file."""
    try:
        with open(reference_file, "r", encoding="utf-8") as f:
            content = f.read()

        updated_content = re.sub(
            r"\[\[.*?" + re.escape(memory_file.name) + r".*?\]\]", "", content
        )

        updated_content = re.sub(r"\n\s*\n", "\n", updated_content)
        updated_content = updated_content.strip()

        with open(reference_file, "w", encoding="utf-8") as f:
            f.write(updated_content)

    except (IOError, UnicodeDecodeError) as e:
        print(f"Warning: Could not update references in {reference_file}: {e}")


def load_forget_template():
    """Load the forget template for response formatting."""
    template_path = (
        Path(__file__).parent.parent.parent / "templates" / "forget-template.md"
    )

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    except (IOError, UnicodeDecodeError):
        return """# Memory Forgotten

**Title**: {title}
**Type**: {memory_type}
**Status**: {status}
**Path**: {path}

{details}

---

*Memory system - {timestamp}*
"""


def format_forget_response(memory_file, status, details=""):
    """Format response using forget template."""
    template = load_forget_template()

    # Extract memory type from directory structure
    memory_type = memory_file.parent.name

    return template.format(
        title=memory_file.stem.replace("-", " ").replace("_", " "),
        memory_type=memory_type,
        status=status,
        path=str(memory_file),
        details=details,
        timestamp="Current",
    )


def delete_memory_with_safeguards(memory_file):
    """Delete memory with user confirmation and reference cleanup."""
    print("\n" + "=" * 50)
    print("MEMORY FOUND:")
    print("=" * 50)

    try:
        with open(memory_file, "r", encoding="utf-8") as f:
            content = f.read()
            print(f"Title: {memory_file.stem.replace('-', ' ').replace('_', ' ')}")
            print(f"Type: {memory_file.parent.name}")
            print(f"Path: {memory_file}")
            print("\nContent:")
            print("-" * 20)
            print(content)
            print("-" * 20)
    except (IOError, UnicodeDecodeError) as e:
        print(f"Error reading memory file: {e}")
        return False

    references = find_linked_references(memory_file)
    if references:
        print(
            f"\n📝 This memory is referenced in {len(references)} other memory file(s):"
        )
        for ref in references:
            print(f"   - {ref}")

    print("\n" + "=" * 50)
    print("DELETION WARNING:")
    print("This action cannot be undone!")
    print("=" * 50)

    while True:
        confirm = input("Confirm deletion? [Y/N]: ").strip().upper()
        if confirm == "Y":
            break
        elif confirm == "N":
            print("Deletion cancelled.")
            return False
        else:
            print("Please enter 'Y' to confirm or 'N' to cancel.")

    for ref_file in references:
        remove_memory_reference(memory_file, ref_file)
        print(f"🔄 Removed reference from: {ref_file}")

    try:
        os.remove(memory_file)
        print(f"✓ Removed: {memory_file}")

        try:
            parent_dir = memory_file.parent
            if not any(parent_dir.iterdir()):
                parent_dir.rmdir()
                print(f"✓ Removed empty directory: {parent_dir}")
        except OSError:
            pass

        return True

    except OSError as e:
        print(f"❌ Error deleting memory: {e}")
        return False

    # Find linked references
    references = find_linked_references(memory_file)
    if references:
        print(
            f"\n📝 This memory is referenced in {len(references)} other memory file(s):"
        )
        for ref in references:
            print(f"   - {ref}")

    print("\n" + "=" * 50)
    print("DELETION WARNING:")
    print("This action cannot be undone!")
    print("=" * 50)

    # Get user confirmation
    while True:
        confirm = input("Confirm deletion? [Y/N]: ").strip().upper()
        if confirm == "Y":
            break
        elif confirm == "N":
            print("Deletion cancelled.")
            return False
        else:
            print("Please enter 'Y' to confirm or 'N' to cancel.")

    # Remove references from other memories
    for ref_file in references:
        remove_memory_reference(memory_file, ref_file)
        print(f"🔄 Removed reference from: {ref_file}")

    # Delete the memory file
    try:
        os.remove(memory_file)
        print(f"✓ Removed: {memory_file}")

        # Clean up empty directories
        try:
            parent_dir = memory_file.parent
            if not any(parent_dir.iterdir()):  # Check if directory is empty
                parent_dir.rmdir()
                print(f"✓ Removed empty directory: {parent_dir}")
        except OSError:
            pass  # Directory not empty or other error

        return True

    except OSError as e:
        print(f"❌ Error deleting memory: {e}")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Delete OpenCode memories")
    parser.add_argument("--title", required=True, help="Title of memory to delete")
    parser.add_argument("--type", help="Memory type filter (e.g., learning, problems)")
    parser.add_argument("--topic", help="Search within memory content")

    args = parser.parse_args()

    memories = find_memories(args.title, args.type, args.topic)

    if not memories:
        print("No memories found matching your criteria.")
        response = format_forget_response(
            Path("not_found"),
            "Not Found",
            f"No memories found with title '{args.title}'",
        )
        print(response)
        print("✅ Complete")
        return

    if len(memories) > 1:
        print(f"\nFound {len(memories)} matching memories:")
        for i, mem in enumerate(memories, 1):
            print(f"{i}. {mem}")

        choice = input("Which memory would you like to delete? (number): ").strip()
        try:
            choice_num = int(choice) - 1
            if 0 <= choice_num < len(memories):
                memory_file = memories[choice_num]
            else:
                print("Invalid choice. Aborting.")
                return
        except ValueError:
            print("Invalid input. Aborting.")
            return
    else:
        memory_file = memories[0]

    success = delete_memory_with_safeguards(memory_file)

    if success:
        response = format_forget_response(memory_file, "Deleted")
        print("\n" + "=" * 50)
        print("DELETION SUMMARY:")
        print("=" * 50)
        print(response)
    else:
        response = format_forget_response(memory_file, "Deletion Failed")
        print("\n" + "=" * 50)
        print("DELETION FAILED:")
        print("=" * 50)
        print(response)

    print("✅ Complete")


if __name__ == "__main__":
    main()
