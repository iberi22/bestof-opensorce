import os
import shutil
import re
from pathlib import Path

def sync_images():
    blog_dir = Path("website/src/content/blog")
    public_images_dir = Path("website/public/images/blog")
    public_images_dir.mkdir(parents=True, exist_ok=True)

    # Base URL for the website (adjust if needed, e.g. /bestof-opensorce/)
    base_url = "/bestof-opensorce/images/blog"

    for md_file in blog_dir.rglob("index.md"):
        # Slug is the parent directory name
        slug = md_file.parent.name
        category = md_file.parent.parent.name

        # Look for header.png in the same directory
        src_image = md_file.parent / "header.png"

        if src_image.exists():
            # Destination name: category-slug-header.png or just slug-header.png
            # Let's use slug-header.png to be unique enough (assuming slugs are unique)
            dest_filename = f"{slug}-header.png"
            dest_path = public_images_dir / dest_filename

            # Copy file
            shutil.copy2(src_image, dest_path)
            print(f"Synced {src_image} -> {dest_path}")

            # Update Frontmatter to point to public URL
            public_path = f"{base_url}/{dest_filename}"

            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Regex to replace the image path
            # It matches: screenshot: "..." or screenshot: ...
            # We want to replace whatever is there with the public path

            # Pattern: screenshot: <whitespace> <quote?> <path> <quote?>
            pattern = re.compile(r'(screenshot:\s*)(["\']?)(.+?)(["\']?)(\s*\n)')

            if pattern.search(content):
                new_content = pattern.sub(f'\\1"{public_path}"\\5', content)

                if new_content != content:
                    with open(md_file, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Updated frontmatter in {md_file}")
            else:
                print(f"Warning: 'screenshot' field not found in {md_file}")

if __name__ == "__main__":
    sync_images()
