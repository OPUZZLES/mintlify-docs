#!/usr/bin/env python3
"""
Add featured images to all blog posts
This script adds the featured image at the top of each blog post
"""

import os
import re
from pathlib import Path

def process_blog_post(file_path):
    """Process a single blog post to add featured image"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
        if not frontmatter_match:
            print(f"⚠️  No frontmatter found in {file_path}")
            return False
        
        frontmatter = frontmatter_match.group(1)
        body = frontmatter_match.group(2)
        
        # Extract featured_image from frontmatter
        featured_image_match = re.search(r'featured_image:\s*["\']?([^"\'\n]+)["\']?', frontmatter)
        if not featured_image_match:
            print(f"⚠️  No featured_image found in {file_path}")
            return False
        
        featured_image = featured_image_match.group(1)
        
        # Extract title for alt text
        title_match = re.search(r'title:\s*["\']([^"\']+)["\']', frontmatter)
        title = title_match.group(1) if title_match else "Blog Post"
        
        # Check if image is already added
        if '<img' in body[:500]:  # Check first 500 chars
            print(f"✓ Image already exists in {file_path}")
            return True
        
        # Create image HTML
        image_html = f'''<img
  src="{featured_image}"
  alt="{title}"
  style={{{{ width: '100%', height: '400px', objectFit: 'cover', borderRadius: '8px', marginBottom: '2rem' }}}}
/>

'''
        
        # Add image at the beginning of body
        new_content = f"---\n{frontmatter}\n---\n\n{image_html}{body}"
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ Added featured image to {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def add_featured_images():
    """Add featured images to all blog posts"""
    
    blog_dir = Path("blog")
    processed = 0
    updated = 0
    
    # Find all MDX files in blog subdirectories
    for mdx_file in blog_dir.rglob("*.mdx"):
        # Skip category index files
        if mdx_file.name in ['ai.mdx', 'guides.mdx', 'science.mdx', 'tips-and-tricks.mdx', 'recent.mdx']:
            continue
        
        processed += 1
        if process_blog_post(mdx_file):
            updated += 1
    
    print(f"\n🎉 Featured image addition complete!")
    print(f"   Processed: {processed} files")
    print(f"   Updated: {updated} files")

if __name__ == "__main__":
    add_featured_images()