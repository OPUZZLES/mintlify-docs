#!/usr/bin/env python3
"""
Convert all Ghost blog posts to MDX format.
"""

from ghost_to_mdx_converter import GhostToMDXConverter
import json


def main():
    """Convert all posts and create summary files."""
    ghost_json_path = "/Users/pierreillsley/Documents/GitHub/mintlify-docs/educateai-blog.ghost.2025-07-02-12-29-23.json"
    
    converter = GhostToMDXConverter(ghost_json_path)
    
    # Convert all posts
    print("Converting all posts...")
    converted_posts = converter.convert_all_posts()
    
    # Print summary
    converter.print_summary(converted_posts)
    
    # Create featured images summary
    print("\nCreating featured images summary...")
    if converter.featured_images:
        with open("featured_images_to_migrate.json", "w", encoding="utf-8") as f:
            json.dump(converter.featured_images, f, indent=2)
        print("Featured images list saved to: featured_images_to_migrate.json")
    
    # Create posts summary
    posts_summary = []
    for post in converted_posts:
        posts_summary.append({
            'title': post['title'],
            'slug': post['slug'],
            'category': post['category'],
            'tags': post['tags'],
            'filepath': post['filepath']
        })
    
    with open("converted_posts_summary.json", "w", encoding="utf-8") as f:
        json.dump(posts_summary, f, indent=2)
    print("Posts summary saved to: converted_posts_summary.json")
    
    print(f"\n✅ Successfully converted {len(converted_posts)} posts!")
    print("\nNext steps:")
    print("1. Review the generated MDX files")
    print("2. Download and organize featured images using featured_images_to_migrate.json")
    print("3. Update any internal links or references")
    print("4. Test the MDX files in your blog system")


if __name__ == "__main__":
    main()