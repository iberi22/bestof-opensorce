#!/usr/bin/env python3
"""
Clean Duplicate Blog Posts

This script identifies and removes duplicate blog posts based on the
repository they reference. Keeps the version with owner-repo format
as the canonical one.
"""

import os
import sys
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple


def find_duplicates(blog_dir: Path) -> Dict[str, List[dict]]:
    """
    Find blogs with duplicate repo values.
    
    Returns:
        Dictionary mapping repo names to list of blog paths.
    """
    repos = {}
    
    for md_file in blog_dir.rglob('index.md'):
        content = md_file.read_text(encoding='utf-8', errors='ignore')
        
        # Search for repo field (format: owner/repo)
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
                'file': str(md_file),
                'category': str(md_file.parent.parent.name)
            })
    
    return repos


def determine_canonical(entries: List[dict]) -> Tuple[dict, List[dict]]:
    """
    Determine which entry is canonical (keeper) and which are duplicates.
    
    We prefer:
    1. Folders with owner-repo format (more specific)
    2. Longer folder names (more info)
    
    Returns:
        Tuple of (canonical entry, list of duplicates to remove)
    """
    if len(entries) == 1:
        return entries[0], []
    
    # Sort by folder name length (longer = more specific = keep)
    sorted_entries = sorted(entries, key=lambda x: len(x['folder']), reverse=True)
    
    canonical = sorted_entries[0]
    duplicates = sorted_entries[1:]
    
    return canonical, duplicates


def clean_duplicates(blog_dir: Path, dry_run: bool = True) -> Tuple[int, int]:
    """
    Clean duplicate blog posts.
    
    Args:
        blog_dir: Path to blog content directory
        dry_run: If True, only print what would be deleted
        
    Returns:
        Tuple of (duplicates found, duplicates removed)
    """
    repos = find_duplicates(blog_dir)
    
    duplicates_found = 0
    duplicates_removed = 0
    
    for repo_key, entries in sorted(repos.items()):
        if len(entries) > 1:
            duplicates_found += len(entries) - 1
            canonical, duplicates = determine_canonical(entries)
            
            print(f"\n🔍 {repo_key}")
            print(f"   ✅ Keep: {canonical['folder']} ({canonical['category']})")
            
            for dup in duplicates:
                print(f"   🗑️  Remove: {dup['folder']} ({dup['category']})")
                
                if not dry_run:
                    try:
                        shutil.rmtree(dup['path'])
                        duplicates_removed += 1
                        print(f"      ✓ Deleted")
                    except Exception as e:
                        print(f"      ✗ Error: {e}")
    
    return duplicates_found, duplicates_removed


def main():
    blog_dir = Path(__file__).parent.parent / 'website' / 'src' / 'content' / 'blog'
    
    print("=" * 60)
    print("🧹 Blog Post Duplicate Cleaner")
    print("=" * 60)
    
    # Check for --execute flag
    dry_run = '--execute' not in sys.argv
    
    if dry_run:
        print("\n⚠️  DRY RUN MODE - No files will be deleted")
        print("   Use --execute flag to actually delete duplicates\n")
    else:
        print("\n🔥 EXECUTE MODE - Duplicates will be deleted!\n")
    
    found, removed = clean_duplicates(blog_dir, dry_run=dry_run)
    
    print("\n" + "=" * 60)
    print(f"📊 SUMMARY")
    print(f"   Duplicates found: {found}")
    if dry_run:
        print(f"   Would remove: {found}")
        print(f"\n💡 Run with --execute to delete duplicates")
    else:
        print(f"   Duplicates removed: {removed}")
    print("=" * 60)


if __name__ == '__main__':
    main()
