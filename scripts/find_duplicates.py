"""
Script to find duplicate blog posts by repo field or html_url.
"""

import os
from pathlib import Path
import re

def find_duplicates():
    """Find blogs with duplicate repo values."""
    blog_dir = Path('website/src/content/blog')
    repos = {}
    
    for md_file in blog_dir.rglob('index.md'):
        content = md_file.read_text(encoding='utf-8', errors='ignore')
        
        # Search for repo field (format: owner/repo) or full_name in repo_data
        repo_key = None
        
        # Method 1: Look for "repo: owner/name" 
        match = re.search(r'^repo:\s*([^\n]+)', content, re.MULTILINE)
        if match:
            repo_key = match.group(1).strip().strip('"\'')
        
        # Method 2: Look for full_name in repo_data
        if not repo_key:
            match = re.search(r'full_name:\s*["\']?([^"\'\n]+)', content)
            if match:
                repo_key = match.group(1).strip()
        
        if repo_key:
            if repo_key not in repos:
                repos[repo_key] = []
            repos[repo_key].append({
                'folder': str(md_file.parent.name),
                'path': str(md_file.parent),
                'category': str(md_file.parent.parent.name)
            })
    
    print('=== REPOS DUPLICADOS ===')
    duplicates = 0
    duplicate_paths = []
    
    for repo, entries in sorted(repos.items()):
        if len(entries) > 1:
            duplicates += 1
            print(f'\n🔴 {repo}')
            for entry in entries:
                print(f'   -> {entry["folder"]} ({entry["path"]})')
                duplicate_paths.append(entry)
    
    print(f'\n=== RESUMEN ===')
    print(f'Total blogs: {sum(len(f) for f in repos.values())}')
    print(f'Repos únicos: {len(repos)}')
    print(f'Repos duplicados: {duplicates}')
    
    return repos, duplicates

if __name__ == '__main__':
    find_duplicates()
