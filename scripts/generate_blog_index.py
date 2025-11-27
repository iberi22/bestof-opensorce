import os
import json
import re
from pathlib import Path
from datetime import datetime

def parse_frontmatter(content):
    if not content.startswith("---"):
        return {}

    try:
        _, fm, _ = content.split("---", 2)
        data = {}
        for line in fm.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                # Handle lists roughly
                if value.startswith("[") and value.endswith("]"):
                    value = [x.strip().strip('"\'') for x in value[1:-1].split(",")]
                data[key] = value
        return data
    except Exception:
        return {}

def generate_blog_index():
    blog_dir = Path("website/src/content/blog")
    output_file = Path("website/public/blog_index.json")

    posts = []

    for md_file in blog_dir.rglob("index.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        data = parse_frontmatter(content)

        # Get slug from directory name
        slug = md_file.parent.name
        category = md_file.parent.parent.name

        post_data = {
            "slug": slug,
            "category": category,
            "title": data.get("title", ""),
            "repo": data.get("repo", ""),
            "date": data.get("date", ""),
            "description": data.get("description", ""),
            "path": str(md_file.relative_to(Path("website"))).replace("\\", "/"),
            "last_updated": datetime.now().isoformat()
        }

        posts.append(post_data)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"posts": posts, "generated_at": datetime.now().isoformat()}, f, indent=2)

    print(f"Generated blog index with {len(posts)} posts at {output_file}")

if __name__ == "__main__":
    generate_blog_index()
