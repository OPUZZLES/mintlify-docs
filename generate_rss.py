#!/usr/bin/env python3
"""
RSS Feed Generator for EducateAI Blog
Generates RSS feeds for all posts and category-specific feeds
"""

import json
import os
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
from xml.dom import minidom

def load_posts_summary():
    """Load the converted posts summary"""
    with open('converted_posts_summary.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def create_rss_item(channel, post):
    """Create an RSS item element for a blog post"""
    item = SubElement(channel, 'item')
    
    # Title
    title = SubElement(item, 'title')
    title.text = post['title']
    
    # Link
    link = SubElement(item, 'link')
    link.text = f"https://blog.educate-ai.com/blog/{post['category']}/{post['slug']}"
    
    # Description
    description = SubElement(item, 'description')
    description.text = post.get('description', post.get('title', 'EducateAI Blog Post'))
    
    # Publication date
    pub_date = SubElement(item, 'pubDate')
    if 'date' in post and post['date']:
        try:
            # Convert ISO date to RFC 2822 format
            date_obj = datetime.fromisoformat(post['date'].replace('Z', '+00:00'))
            pub_date.text = date_obj.strftime('%a, %d %b %Y %H:%M:%S %z')
        except:
            pub_date.text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
    else:
        pub_date.text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
    
    # GUID
    guid = SubElement(item, 'guid')
    guid.text = f"https://blog.educate-ai.com/blog/{post['category']}/{post['slug']}"
    guid.set('isPermaLink', 'true')
    
    # Author
    author = SubElement(item, 'author')
    author_name = post.get('author', 'Pierre Illsley')
    author.text = f"illsley.pierre@gmx.de ({author_name})"
    
    # Category
    category = SubElement(item, 'category')
    category.text = post['category'].capitalize()
    
    # Featured image (enclosure)
    if post.get('featured_image'):
        enclosure = SubElement(item, 'enclosure')
        enclosure.set('url', f"https://blog.educate-ai.com{post['featured_image']}")
        enclosure.set('type', 'image/jpeg')
        enclosure.set('length', '0')  # We don't have the actual file size

def create_rss_feed(posts, title, description, category=None):
    """Create an RSS feed XML structure"""
    rss = Element('rss')
    rss.set('version', '2.0')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
    
    channel = SubElement(rss, 'channel')
    
    # Channel info
    channel_title = SubElement(channel, 'title')
    channel_title.text = title
    
    channel_link = SubElement(channel, 'link')
    if category:
        channel_link.text = f"https://blog.educate-ai.com/blog/{category}"
    else:
        channel_link.text = "https://blog.educate-ai.com"
    
    channel_description = SubElement(channel, 'description')
    channel_description.text = description
    
    language = SubElement(channel, 'language')
    language.text = 'en-us'
    
    copyright_elem = SubElement(channel, 'copyright')
    copyright_elem.text = '© 2024 EducateAI. All rights reserved.'
    
    managing_editor = SubElement(channel, 'managingEditor')
    managing_editor.text = 'illsley.pierre@gmx.de (Pierre Illsley)'
    
    web_master = SubElement(channel, 'webMaster')
    web_master.text = 'illsley.pierre@gmx.de (Pierre Illsley)'
    
    last_build_date = SubElement(channel, 'lastBuildDate')
    last_build_date.text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
    
    # Self-referencing atom:link
    atom_link = SubElement(channel, 'atom:link')
    if category:
        atom_link.set('href', f"https://blog.educate-ai.com/rss/{category}.xml")
    else:
        atom_link.set('href', "https://blog.educate-ai.com/rss/feed.xml")
    atom_link.set('rel', 'self')
    atom_link.set('type', 'application/rss+xml')
    
    # Add items (sort by date, newest first)
    sorted_posts = sorted(posts, key=lambda x: x.get('date', '2024-01-01'), reverse=True)
    
    for post in sorted_posts:
        create_rss_item(channel, post)
    
    return rss

def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element"""
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def generate_rss_feeds():
    """Generate RSS feeds for the blog"""
    
    # Create RSS directory
    os.makedirs('rss', exist_ok=True)
    
    # Load posts
    posts = load_posts_summary()
    
    print(f"Generating RSS feeds for {len(posts)} posts...")
    
    # Generate main RSS feed (all posts)
    main_feed = create_rss_feed(
        posts,
        "EducateAI Blog - AI-Powered Learning Insights",
        "Discover the future of education with AI-powered learning strategies, study techniques, and educational technology insights"
    )
    
    # Save main feed
    with open('rss/feed.xml', 'w', encoding='utf-8') as f:
        f.write(prettify_xml(main_feed))
    print("✓ Generated main RSS feed: rss/feed.xml")
    
    # Generate category-specific feeds
    categories = {}
    for post in posts:
        category = post['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(post)
    
    category_titles = {
        'ai': 'EducateAI Blog - AI in Education',
        'guides': 'EducateAI Blog - Study Guides',
        'science': 'EducateAI Blog - Learning Science',
        'tips-and-tricks': 'EducateAI Blog - Study Tips & Tricks'
    }
    
    category_descriptions = {
        'ai': 'Explore artificial intelligence applications in education and personalized learning',
        'guides': 'Comprehensive guides for effective studying and academic success',
        'science': 'Research-backed insights into cognitive science and learning psychology',
        'tips-and-tricks': 'Quick tips and strategies to boost your learning efficiency'
    }
    
    for category, category_posts in categories.items():
        if len(category_posts) > 0:
            category_feed = create_rss_feed(
                category_posts,
                category_titles.get(category, f"EducateAI Blog - {category.capitalize()}"),
                category_descriptions.get(category, f"Posts in the {category} category"),
                category
            )
            
            # Save category feed
            filename = f'rss/{category}.xml'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(prettify_xml(category_feed))
            print(f"✓ Generated {category} RSS feed: {filename} ({len(category_posts)} posts)")
    
    # Generate RSS index page
    rss_index = f"""---
title: "RSS Feeds - EducateAI Blog"
description: "Subscribe to EducateAI blog RSS feeds to stay updated with the latest AI-powered learning insights"
---

# RSS Feeds

Subscribe to our RSS feeds to stay updated with the latest content from EducateAI Blog.

## Available Feeds

<CardGroup cols={2}>
  <Card title="All Posts" href="/rss/feed.xml" icon="rss">
    Complete feed with all blog posts ({len(posts)} articles)
  </Card>
  
  <Card title="AI in Education" href="/rss/ai.xml" icon="robot">
    AI and machine learning in education ({len(categories.get('ai', []))} articles)
  </Card>
  
  <Card title="Study Guides" href="/rss/guides.xml" icon="book-open">
    Comprehensive study guides and tutorials ({len(categories.get('guides', []))} articles)
  </Card>
  
  <Card title="Learning Science" href="/rss/science.xml" icon="flask">
    Research-backed learning insights ({len(categories.get('science', []))} articles)
  </Card>
</CardGroup>

## How to Subscribe

1. **Copy the RSS feed URL** of your choice from above
2. **Open your RSS reader** (Feedly, Inoreader, Apple News, etc.)
3. **Add the feed** using the copied URL
4. **Enjoy automatic updates** when we publish new content!

## RSS Reader Recommendations

- **[Feedly](https://feedly.com)** - Web-based, great for beginners
- **[Inoreader](https://www.inoreader.com)** - Advanced features and filtering
- **[NetNewsWire](https://netnewswire.com)** - Native Mac/iOS app
- **[Reeder](https://reederapp.com)** - Beautiful iOS/Mac reader

<Info>
  RSS feeds are updated automatically when we publish new articles. No signup required!
</Info>

## Feed Statistics

- **Total articles**: {len(posts)}
- **Categories**: {len(categories)}
- **Languages**: English (with German content coming soon)
- **Update frequency**: 1-2 articles per week
- **Content format**: Full text with images

---

*Stay ahead with the latest in AI-powered education and evidence-based learning strategies.*
"""
    
    with open('rss.mdx', 'w', encoding='utf-8') as f:
        f.write(rss_index)
    print("✓ Generated RSS index page: rss.mdx")
    
    print(f"\n🎉 RSS feed generation complete!")
    print(f"   Main feed: rss/feed.xml")
    print(f"   Category feeds: {len(categories)} feeds")
    print(f"   Total posts: {len(posts)}")

if __name__ == "__main__":
    generate_rss_feeds()