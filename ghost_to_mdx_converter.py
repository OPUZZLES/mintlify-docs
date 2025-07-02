#!/usr/bin/env python3
"""
Ghost Blog to MDX Converter

This script converts Ghost blog export JSON to MDX files with proper frontmatter.
It handles lexical JSON content conversion to markdown and categorizes posts.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class GhostToMDXConverter:
    def __init__(self, ghost_json_path: str, base_output_dir: str = "blog"):
        self.ghost_json_path = ghost_json_path
        self.base_output_dir = base_output_dir
        
        # Category mapping for tags
        self.category_mapping = {
            "ai": ["ai", "artificial-intelligence", "machine-learning", "deep-learning", "neural-networks"],
            "guides": ["guide", "tutorial", "how-to", "step-by-step", "walkthrough", "tips"],
            "science": ["science", "research", "study", "academic", "scientific", "theory"],
            "tips-and-tricks": ["tips", "tricks", "hacks", "productivity", "efficiency", "shortcuts"]
        }
        
        # Featured images found
        self.featured_images = []
        
    def load_ghost_data(self) -> Dict[str, Any]:
        """Load and parse Ghost JSON export."""
        with open(self.ghost_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    
    def get_published_posts(self, ghost_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract published posts from Ghost data."""
        posts = ghost_data.get('db', [{}])[0].get('data', {}).get('posts', [])
        published_posts = [post for post in posts if post.get('status') == 'published']
        print(f"Found {len(published_posts)} published posts")
        return published_posts
    
    def get_tags_for_post(self, post: Dict[str, Any], ghost_data: Dict[str, Any]) -> List[str]:
        """Extract tags for a post."""
        # Get tags from posts_tags relationship
        post_id = post.get('id')
        posts_tags = ghost_data.get('db', [{}])[0].get('data', {}).get('posts_tags', [])
        tags_data = ghost_data.get('db', [{}])[0].get('data', {}).get('tags', [])
        
        # Find tag IDs for this post
        tag_ids = [pt['tag_id'] for pt in posts_tags if pt['post_id'] == post_id]
        
        # Get tag names
        tag_names = []
        for tag in tags_data:
            if tag['id'] in tag_ids:
                tag_names.append(tag['name'])
        
        return tag_names
    
    def categorize_post(self, tags: List[str]) -> str:
        """Determine category based on tags."""
        tags_lower = [tag.lower() for tag in tags]
        
        for category, keywords in self.category_mapping.items():
            if any(keyword in tags_lower for keyword in keywords):
                return category
        
        # Default category
        return "ai"
    
    def convert_lexical_to_markdown(self, lexical_json: str) -> str:
        """Convert Ghost's lexical JSON format to markdown."""
        try:
            lexical_data = json.loads(lexical_json)
            return self._process_lexical_node(lexical_data.get('root', {}))
        except json.JSONDecodeError:
            return ""
    
    def _process_lexical_node(self, node: Dict[str, Any]) -> str:
        """Process a lexical node recursively."""
        if not isinstance(node, dict):
            return ""
        
        node_type = node.get('type', '')
        children = node.get('children', [])
        
        if node_type == 'paragraph':
            content = self._process_children(children)
            return f"{content}\n\n" if content.strip() else ""
        
        elif node_type == 'extended-heading':
            tag = node.get('tag', 'h2')
            level = int(tag[1]) if tag.startswith('h') else 2
            content = self._process_children(children)
            return f"{'#' * level} {content}\n\n"
        
        elif node_type == 'list':
            list_type = node.get('listType', 'bullet')
            items = []
            for child in children:
                if child.get('type') == 'listitem':
                    item_content = self._process_children(child.get('children', []))
                    if list_type == 'bullet':
                        items.append(f"- {item_content}")
                    else:  # numbered
                        value = child.get('value', 1)
                        items.append(f"{value}. {item_content}")
            return '\n'.join(items) + '\n\n'
        
        elif node_type == 'horizontalrule':
            return "---\n\n"
        
        elif node_type == 'extended-text':
            text = node.get('text', '')
            format_flags = node.get('format', 0)
            
            # Apply formatting based on format flags
            if format_flags & 1:  # bold
                text = f"**{text}**"
            if format_flags & 2:  # italic
                text = f"*{text}*"
            if format_flags & 4:  # underline
                text = f"_{text}_"
            if format_flags & 8:  # strikethrough
                text = f"~~{text}~~"
            if format_flags & 16:  # code
                text = f"`{text}`"
            
            return text
        
        else:
            # For unknown types, process children
            return self._process_children(children)
    
    def _process_children(self, children: List[Dict[str, Any]]) -> str:
        """Process children nodes."""
        return ''.join(self._process_lexical_node(child) for child in children)
    
    def create_frontmatter(self, post: Dict[str, Any], tags: List[str], category: str) -> str:
        """Create MDX frontmatter."""
        title = post.get('title', '').replace('"', '\\"')
        slug = post.get('slug', '')
        
        # Convert published_at to date
        published_at = post.get('published_at', '')
        if published_at:
            try:
                date_obj = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                date_str = date_obj.strftime('%Y-%m-%d')
            except:
                date_str = datetime.now().strftime('%Y-%m-%d')
        else:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        # Get excerpt or create description
        excerpt = post.get('excerpt', '')
        if not excerpt:
            # Try to get first paragraph from content
            lexical = post.get('lexical', '')
            if lexical:
                try:
                    lexical_data = json.loads(lexical)
                    root = lexical_data.get('root', {})
                    children = root.get('children', [])
                    for child in children:
                        if child.get('type') == 'paragraph' and child.get('children'):
                            text_nodes = child.get('children', [])
                            for text_node in text_nodes:
                                if text_node.get('type') == 'extended-text':
                                    excerpt = text_node.get('text', '')[:200] + "..."
                                    break
                            if excerpt:
                                break
                except:
                    pass
        
        if not excerpt:
            excerpt = f"Learn about {title.lower()}"
        
        # Handle featured image
        featured_image = post.get('feature_image', '')
        if featured_image:
            # Extract filename and clean it for blog path
            image_filename = os.path.basename(featured_image)
            # If URL has query parameters, create a cleaner filename
            if '?' in image_filename:
                # Extract the base photo name from Unsplash URLs
                if 'photo-' in image_filename:
                    clean_name = image_filename.split('?')[0] + '.jpg'
                else:
                    clean_name = f"{slug}-featured.jpg"
            else:
                clean_name = image_filename
            
            blog_image_path = f"/images/blog/{clean_name}"
            self.featured_images.append({
                'original_url': featured_image,
                'blog_path': blog_image_path,
                'post_slug': slug,
                'filename': clean_name
            })
        else:
            blog_image_path = "/images/blog/default-featured-image.jpg"
        
        # Clean excerpt for frontmatter
        clean_excerpt = excerpt.replace('"', '\\"')
        
        frontmatter = f"""---
title: "{title}"
description: "{clean_excerpt}"
author: "Pierre Illsley"
date: "{date_str}"
category: "{category}"
tags: {json.dumps(tags)}
slug: "{slug}"
featured_image: "{blog_image_path}"
---

"""
        return frontmatter
    
    def create_output_directories(self):
        """Create output directories."""
        categories = ["ai", "guides", "science", "tips-and-tricks"]
        for category in categories:
            dir_path = os.path.join(self.base_output_dir, category)
            os.makedirs(dir_path, exist_ok=True)
    
    def convert_post(self, post: Dict[str, Any], ghost_data: Dict[str, Any]) -> Dict[str, str]:
        """Convert a single post to MDX."""
        # Get tags
        tags = self.get_tags_for_post(post, ghost_data)
        
        # Determine category
        category = self.categorize_post(tags)
        
        # Convert content
        lexical_json = post.get('lexical', '')
        markdown_content = self.convert_lexical_to_markdown(lexical_json)
        
        # Create frontmatter
        frontmatter = self.create_frontmatter(post, tags, category)
        
        # Combine frontmatter and content
        mdx_content = frontmatter + markdown_content
        
        # Create filename
        slug = post.get('slug', '').strip()
        if not slug:
            slug = re.sub(r'[^a-zA-Z0-9\s]', '', post.get('title', 'untitled')).replace(' ', '-').lower()
        
        filename = f"{slug}.mdx"
        filepath = os.path.join(self.base_output_dir, category, filename)
        
        return {
            'content': mdx_content,
            'filepath': filepath,
            'category': category,
            'title': post.get('title', ''),
            'slug': slug,
            'tags': tags
        }
    
    def convert_all_posts(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """Convert all published posts."""
        print("Loading Ghost data...")
        ghost_data = self.load_ghost_data()
        
        print("Getting published posts...")
        published_posts = self.get_published_posts(ghost_data)
        
        if limit:
            published_posts = published_posts[:limit]
            print(f"Processing first {limit} posts...")
        
        print("Creating output directories...")
        self.create_output_directories()
        
        converted_posts = []
        for i, post in enumerate(published_posts, 1):
            print(f"Converting post {i}/{len(published_posts)}: {post.get('title', 'Untitled')}")
            converted_post = self.convert_post(post, ghost_data)
            converted_posts.append(converted_post)
            
            # Write the file
            with open(converted_post['filepath'], 'w', encoding='utf-8') as f:
                f.write(converted_post['content'])
            
            print(f"  → Saved to: {converted_post['filepath']}")
        
        return converted_posts
    
    def print_summary(self, converted_posts: List[Dict[str, str]]):
        """Print conversion summary."""
        print("\n" + "="*50)
        print("CONVERSION SUMMARY")
        print("="*50)
        
        # Count by category
        category_counts = {}
        for post in converted_posts:
            category = post['category']
            category_counts[category] = category_counts.get(category, 0) + 1
        
        print(f"Total posts converted: {len(converted_posts)}")
        print("\nPosts by category:")
        for category, count in category_counts.items():
            print(f"  {category}: {count} posts")
        
        print(f"\nFeatured images found: {len(self.featured_images)}")
        if self.featured_images:
            print("\nFeatured images to migrate:")
            for img in self.featured_images[:5]:  # Show first 5
                print(f"  {img['original_url']} → {img['blog_path']}")
            if len(self.featured_images) > 5:
                print(f"  ... and {len(self.featured_images) - 5} more")
        
        print("\nFirst few converted posts:")
        for post in converted_posts[:3]:
            print(f"  {post['title']} ({post['category']}) → {post['filepath']}")


def main():
    """Main function."""
    ghost_json_path = "/Users/pierreillsley/Documents/GitHub/mintlify-docs/educateai-blog.ghost.2025-07-02-12-29-23.json"
    
    converter = GhostToMDXConverter(ghost_json_path)
    
    # Convert first 5 posts as examples
    converted_posts = converter.convert_all_posts(limit=5)
    
    # Print summary
    converter.print_summary(converted_posts)
    
    print("\n" + "="*50)
    print("SAMPLE OUTPUT")
    print("="*50)
    
    # Show first converted post content
    if converted_posts:
        first_post = converted_posts[0]
        print(f"First post: {first_post['title']}")
        print(f"File: {first_post['filepath']}")
        print("\nContent preview:")
        print("-" * 30)
        print(first_post['content'][:1000] + "..." if len(first_post['content']) > 1000 else first_post['content'])


if __name__ == "__main__":
    main()