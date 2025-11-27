import os
import shutil
import re
from pathlib import Path

def migrate_blog_structure():
    base_dir = Path("website/src/content/blog")
    images_dir = Path("website/public/images/blog")

    # Regex to parse filename: YYYY-MM-DD-slug.md
    filename_pattern = re.compile(r"(\d{4}-\d{2}-\d{2})-(.+)\.md")

    for md_file in base_dir.rglob("*.md"):
        if md_file.name == "index.md":
            continue

        match = filename_pattern.match(md_file.name)
        if not match:
            print(f"Skipping {md_file.name} (no date pattern)")
            continue

        date_str, slug = match.groups()
        category_dir = md_file.parent

        # Create new directory structure
        new_dir = category_dir / slug
        new_dir.mkdir(parents=True, exist_ok=True)

        new_md_path = new_dir / "index.md"

        # Read content to get repo name for image finding
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract repo from frontmatter
        repo_match = re.search(r"^repo:\s*(.+)$", content, re.MULTILINE)
        repo_name = repo_match.group(1).strip() if repo_match else None

        # Find image
        image_name = None
        if repo_name:
            # Image naming convention: owner-repo-header.png
            sanitized_repo = repo_name.replace("/", "-")
            possible_image = images_dir / f"{sanitized_repo}-header.png"

            if possible_image.exists():
                image_name = "header.png"
                shutil.move(str(possible_image), str(new_dir / image_name))
                print(f"Moved image for {repo_name}")
            else:
                print(f"Image not found for {repo_name} at {possible_image}")

        # Update frontmatter
        if image_name:
            # Check if images section exists
            if "images:" not in content:
                # Insert after repo: or title:
                insertion_point = content.find("---", 3)
                if insertion_point != -1:
                    # simplistic insertion, better to use regex or yaml parser but this is quick
                    # We'll insert before the closing ---
                    extra_fm = f"images:\n  screenshot: ./{image_name}\n"
                    content = content[:insertion_point] + extra_fm + content[insertion_point:]

        # Write new file
        with open(new_md_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Remove old file
        md_file.unlink()
        print(f"Migrated {md_file.name} to {new_md_path}")

if __name__ == "__main__":
    migrate_blog_structure()
