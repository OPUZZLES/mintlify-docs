#!/usr/bin/env python3
"""
Sitemap Generator for EducateAI Blog
Generates XML sitemap for SEO optimization
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

def create_sitemap():
    """Generate XML sitemap for the blog"""
    
    # Create sitemap root
    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:image', 'http://www.google.com/schemas/sitemap-image/1.1')
    
    # Load posts
    posts = load_posts_summary()
    
    # Homepage
    url = SubElement(urlset, 'url')
    loc = SubElement(url, 'loc')
    loc.text = 'https://blog.educate-ai.com'
    lastmod = SubElement(url, 'lastmod')
    lastmod.text = datetime.now().strftime('%Y-%m-%d')
    changefreq = SubElement(url, 'changefreq')
    changefreq.text = 'daily'
    priority = SubElement(url, 'priority')
    priority.text = '1.0'
    
    # German homepage
    url = SubElement(urlset, 'url')
    loc = SubElement(url, 'loc')
    loc.text = 'https://blog.educate-ai.com/de'
    lastmod = SubElement(url, 'lastmod')
    lastmod.text = datetime.now().strftime('%Y-%m-%d')
    changefreq = SubElement(url, 'changefreq')
    changefreq.text = 'weekly'
    priority = SubElement(url, 'priority')
    priority.text = '0.8'
    
    # Category pages
    categories = ['ai', 'guides', 'science', 'tips-and-tricks']
    for category in categories:
        # English category page
        url = SubElement(urlset, 'url')
        loc = SubElement(url, 'loc')
        loc.text = f'https://blog.educate-ai.com/blog/{category}'
        lastmod = SubElement(url, 'lastmod')
        lastmod.text = datetime.now().strftime('%Y-%m-%d')
        changefreq = SubElement(url, 'changefreq')
        changefreq.text = 'weekly'
        priority = SubElement(url, 'priority')
        priority.text = '0.8'
    
    # Recent posts page
    url = SubElement(urlset, 'url')
    loc = SubElement(url, 'loc')
    loc.text = 'https://blog.educate-ai.com/blog/recent'
    lastmod = SubElement(url, 'lastmod')
    lastmod.text = datetime.now().strftime('%Y-%m-%d')
    changefreq = SubElement(url, 'changefreq')
    changefreq.text = 'daily'
    priority = SubElement(url, 'priority')
    priority.text = '0.9'
    
    # RSS page
    url = SubElement(urlset, 'url')
    loc = SubElement(url, 'loc')
    loc.text = 'https://blog.educate-ai.com/rss'
    lastmod = SubElement(url, 'lastmod')
    lastmod.text = datetime.now().strftime('%Y-%m-%d')
    changefreq = SubElement(url, 'changefreq')
    changefreq.text = 'weekly'
    priority = SubElement(url, 'priority')
    priority.text = '0.6'
    
    # Blog posts
    for post in posts:
        url = SubElement(urlset, 'url')
        loc = SubElement(url, 'loc')
        loc.text = f"https://blog.educate-ai.com/blog/{post['category']}/{post['slug']}"
        
        # Try to extract date from post, fallback to current date
        if 'date' in post and post['date']:
            try:
                date_obj = datetime.fromisoformat(post['date'].replace('Z', '+00:00'))
                lastmod_date = date_obj.strftime('%Y-%m-%d')
            except:
                lastmod_date = '2024-08-10'  # Fallback date
        else:
            lastmod_date = '2024-08-10'  # Fallback date
            
        lastmod = SubElement(url, 'lastmod')
        lastmod.text = lastmod_date
        
        changefreq = SubElement(url, 'changefreq')
        changefreq.text = 'monthly'
        
        priority = SubElement(url, 'priority')
        priority.text = '0.7'
        
        # Add image if available
        if 'featured_image' in post and post['featured_image']:
            image = SubElement(url, 'image:image')
            image_loc = SubElement(image, 'image:loc')
            image_loc.text = f"https://blog.educate-ai.com{post['featured_image']}"
            image_title = SubElement(image, 'image:title')
            image_title.text = post['title']
    
    return urlset

def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element"""
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def generate_sitemap():
    """Generate sitemap.xml file"""
    
    posts = load_posts_summary()
    print(f"Generating sitemap for {len(posts)} posts...")
    
    sitemap = create_sitemap()
    
    # Save sitemap
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(prettify_xml(sitemap))
    
    print("✓ Generated sitemap.xml")
    
    # Calculate total URLs
    total_urls = (
        1 +  # Homepage
        1 +  # German homepage
        4 +  # Category pages
        1 +  # Recent posts
        1 +  # RSS page
        len(posts)  # Blog posts
    )
    
    print(f"   Total URLs: {total_urls}")
    print(f"   Blog posts: {len(posts)}")
    print(f"   Static pages: {total_urls - len(posts)}")

if __name__ == "__main__":
    generate_sitemap()