#!/usr/bin/env python3
"""
Fix strikethrough links in blog posts
Replace ~~text~~ with actual links where appropriate
"""

import os
import re
from pathlib import Path

def fix_links_in_file(file_path):
    """Fix strikethrough links in a single blog post"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Common patterns to fix
        replacements = [
            # Remove strikethrough from references/citations
            (r'~~([^~]+\s*–\s*Wikipedia)~~', r'\1'),
            (r'~~([^~]+\s*\|\s*Vaia)~~', r'\1'),
            (r'~~([^~]+\s*\|\s*[^~]+)~~', r'\1'),
            (r'~~(Active Recall: Techniques & Benefits \| Vaia)~~', r'\1'),
            (r'~~(spaced repetition – Wikipedia)~~', r'\1'),
            (r'~~(Spaced Repetition – Wikipedia)~~', r'\1'),
            (r'~~(Forgetting Curve – Wikipedia)~~', r'\1'),
            (r'~~(What is the evidence around spaced repetition \| SC Training)~~', r'\1'),
            (r'~~([^~]*Understanding AI in Education \| Restackio[^~]*)~~', r'\1'),
            (r'~~([^~]*New AI Tools[^~]*)~~', r'\1'),
            (r'~~([^~]*EdSurge News[^~]*)~~', r'\1'),
            (r'~~(EducateAI)~~', r'EducateAI'),
            
            # Remove strikethrough from study tool names but keep the text
            (r'~~([A-Za-z0-9\s\-]+\s*–\s*[A-Za-z0-9\s\-]+)~~', r'\1'),
        ]
        
        # Apply replacements
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # If content changed, write it back
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed links in {file_path}")
            return True
        else:
            print(f"- No changes needed in {file_path}")
            return False
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def fix_all_blog_links():
    """Fix strikethrough links in all blog posts"""
    
    blog_dir = Path("blog")
    processed = 0
    updated = 0
    
    # Find all MDX files in blog subdirectories
    for mdx_file in blog_dir.rglob("*.mdx"):
        # Skip category index files
        if mdx_file.name in ['ai.mdx', 'guides.mdx', 'science.mdx', 'tips-and-tricks.mdx', 'recent.mdx']:
            continue
        
        processed += 1
        if fix_links_in_file(mdx_file):
            updated += 1
    
    print(f"\n🎉 Link fixing complete!")
    print(f"   Processed: {processed} files")
    print(f"   Updated: {updated} files")

if __name__ == "__main__":
    fix_all_blog_links()