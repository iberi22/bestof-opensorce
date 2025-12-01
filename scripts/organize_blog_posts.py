#!/usr/bin/env python3
"""
Organize Blog Posts into Categories and Page Bundles
Converts .md files to page bundles (folders with index.md) for proper image support.
"""

import os
import sys
import shutil
import json
import re
from pathlib import Path

# Add src to path to import MarkdownWriter logic
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from blog_generator.markdown_writer import MarkdownWriter

def parse_frontmatter(content):
    """Simple manual frontmatter parser."""
    if not content.startswith("---"):
        return {}

    try:
        _, fm, _ = content.split("---", 2)
        metadata = {}
        for line in fm.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                # Handle basic types
                if value.startswith("[") and value.endswith("]"):
                    try:
                        value = json.loads(value)
                    except:
                        pass
                elif value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                metadata[key] = value
        return metadata
    except Exception:
        return {}


def get_slug_from_filename(filename: str) -> str:
    """Extract a clean slug from filename."""
    # Remove date prefix and .md extension
    name = filename.replace('.md', '')
    # Remove date patterns like 20251129- or 2025-11-29-
    name = re.sub(r'^\d{8}-', '', name)
    name = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', name)
    return name


def get_repo_slug_from_content(content: str) -> str:
    """Extract owner-repo slug from frontmatter content."""
    # Look for repo: owner/name or full_name in repo_data
    match = re.search(r'^repo:\s*([^\n]+)', content, re.MULTILINE)
    if match:
        repo_value = match.group(1).strip().strip('"\'')
        # Convert owner/repo to owner-repo format
        return repo_value.lower().replace('/', '-').replace(' ', '-')
    
    match = re.search(r'full_name:\s*["\']?([^"\'\n]+)', content)
    if match:
        repo_value = match.group(1).strip()
        return repo_value.lower().replace('/', '-').replace(' ', '-')
    
    return None


def convert_to_page_bundle(md_file: Path, target_category_dir: Path, content: str = None) -> Path:
    """
    Convert a .md file to a page bundle (folder with index.md).
    Returns the path to the new index.md file.
    """
    # Try to get slug from content (repo field) first for consistency
    if content:
        slug = get_repo_slug_from_content(content)
    
    # Fallback to filename
    if not slug:
        slug = get_slug_from_filename(md_file.name)

    # Create bundle directory
    bundle_dir = target_category_dir / slug
    bundle_dir.mkdir(parents=True, exist_ok=True)

    # Move/copy content to index.md
    index_path = bundle_dir / "index.md"

    if content is None:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Remove original file
    md_file.unlink()

    return index_path

def organize_posts():
    blog_dir = Path(__file__).parent.parent / 'website' / 'src' / 'content' / 'blog'
    writer = MarkdownWriter()

    print(f"📂 Organizing posts in {blog_dir}...")

    # Get all .md files in the root of blog_dir and category subdirs
    md_files = list(blog_dir.glob("*.md"))

    # Also check category directories for .md files that aren't in bundles
    for category_dir in blog_dir.iterdir():
        if category_dir.is_dir():
            md_files.extend(category_dir.glob("*.md"))

    if not md_files:
        print("ℹ️ No files to organize.")
        return

    converted_count = 0

    for file_path in md_files:
        # Skip if already in a bundle (parent is not a category dir)
        if file_path.name == "index.md":
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            metadata = parse_frontmatter(content)
            tags = metadata.get('tags', [])
            if isinstance(tags, str):
                tags = []

            language = metadata.get('language', 'Unknown')

            # Determine category
            categories = writer._determine_categories(tags, language)
            primary_category = categories[0].lower().replace(" ", "-") if categories else "general"

            # Target category directory
            target_dir = blog_dir / primary_category
            target_dir.mkdir(parents=True, exist_ok=True)

            # Convert to page bundle (pass content to extract slug from repo field)
            new_path = convert_to_page_bundle(file_path, target_dir, content)
            converted_count += 1

            # Get final slug for logging
            slug = get_repo_slug_from_content(content) or get_slug_from_filename(file_path.name)
            print(f"  ✅ Converted {file_path.name} -> {primary_category}/{slug}/index.md")

        except Exception as e:
            print(f"  ❌ Failed to process {file_path.name}: {e}")

    print(f"\n✨ Organization complete! Converted {converted_count} posts to page bundles.")


if __name__ == "__main__":
    organize_posts()
