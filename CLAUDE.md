This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the EducateAI Blog project built with Mintlify, migrating from blog.educate-ai.com. The site uses MDX (Markdown with JSX) files to create engaging educational content focused on AI-driven learning strategies and educational technology.

## Project Goals

- Migrate and enhance the EducateAI blog from the current platform to Mintlify
- Create comprehensive educational content about AI, learning strategies, and educational technology
- Focus on user-friendly design with engaging blog features
- Use accent color #2563eb (blue theme) to match current brand
- Organize content in logical categories: AI, Guides, Science, Tips and Tricks
- Build a modern, performant blog platform with enhanced features

## Current Focus

**Blog Migration and Enhancement**:
- Migrate ~12 existing posts from blog.educate-ai.com
- Maintain bilingual support (EN/DE)
- Implement newsletter signup functionality
- Create custom blog components for enhanced user experience
- SEO-optimized content with proper meta tags
- Reading progress indicators and estimated reading times

## Important Notes

- This blog focuses on educational technology and AI-driven learning strategies
- Content should be accessible to educators, students, and educational technology enthusiasts
- Maintain professional but approachable tone
- Posts typically 1-2 per month, focusing on quality over quantity

## Essential Commands

### Development
- `mint dev` - Start the local development server (default port 3000)
- `mint dev --port 3333` - Start dev server on custom port
- `mint update` - Update Mintlify CLI to latest version

### Content Management
- All blog posts stored in `/blog/` directory
- Categories: `/blog/ai/`, `/blog/guides/`, `/blog/science/`, `/blog/tips-and-tricks/`
- Archives in `/blog/archive/` for older content

## Content Structure

### Main Blog Categories
```
/blog/                    # Main blog hub
  /index.mdx             # Blog homepage
  /recent.mdx            # Recent posts listing
  /ai/                   # AI and machine learning content
    /index.mdx           # AI category page
    /[posts].mdx         # Individual AI posts
  /guides/               # How-to guides and tutorials
    /index.mdx           # Guides category page
    /[posts].mdx         # Individual guide posts
  /science/              # Educational science content
    /index.mdx           # Science category page
    /[posts].mdx         # Individual science posts
  /tips-and-tricks/      # Quick tips and strategies
    /index.mdx           # Tips category page
    /[posts].mdx         # Individual tip posts
  /archive/              # Older posts organized by date

/components/             # Custom blog components
  /BlogPost.tsx          # Blog post layout
  /CategoryGrid.tsx      # Category navigation
  /NewsletterSignup.tsx  # Newsletter subscription
  /AuthorBio.tsx         # Author information
  /RelatedPosts.tsx      # Content recommendations
  /ReadingProgress.tsx   # Reading progress indicator
  /SocialShare.tsx       # Social media sharing

/data/                   # Blog metadata
  /authors.json          # Author information database
  /categories.json       # Category metadata
  /tags.json             # Tag system for content
```

## Writing Style Guidelines

### Content Principles
- **Educational**: Focus on practical learning strategies and educational technology
- **Evidence-based**: Support claims with research and real-world examples
- **Accessible**: Write for educators and learners of all technical levels
- **Actionable**: Provide concrete steps and implementation strategies
- **International**: Consider both English and German-speaking audiences

### Blog Post Structure
Every blog post should include:
- Engaging introduction with clear value proposition
- Well-structured content with headers and subheadings
- Practical examples and real-world applications
- Actionable takeaways or next steps
- Author bio and related content suggestions

### Post Frontmatter Format
```yaml
---
title: "How AI is Revolutionizing Personalized Learning"
description: "Discover how artificial intelligence creates tailored educational experiences for every learner"
author: "Dr. Sarah Mueller"
date: "2024-03-15"
category: "AI"
tags: ["personalized-learning", "adaptive-systems", "educational-technology"]
readTime: "8 min read"
image: "/images/blog/ai-personalized-learning.jpg"
seo:
  title: "AI Personalized Learning Revolution - EducateAI"
  description: "Explore how AI transforms education through personalized learning paths and adaptive systems"
  keywords: "AI education, personalized learning, adaptive learning systems"
language: "en"
translatedVersions:
  de: "/de/blog/ai/ki-revolutioniert-personalisiertes-lernen"
canonical: "https://blog.educate-ai.com/ai/ai-revolutionizing-personalized-learning"
---
```

## Key Development Notes

### Custom Blog Components
- `<BlogHeader>` - Post title, author, date, reading time
- `<ReadingProgress>` - Progress indicator for long posts
- `<TableOfContents>` - Auto-generated TOC for articles
- `<AuthorBio>` - Author information and credentials
- `<RelatedPosts>` - Category-based content recommendations
- `<NewsletterSignup>` - Email subscription form
- `<SocialShare>` - Social media sharing buttons
- `<CategoryCard>` - Visual category navigation

### Bilingual Support
- English content in main directories
- German translations in `/de/` subdirectories
- Language switcher in navigation
- Proper hreflang tags for SEO
- Translated metadata and navigation elements

### SEO and Analytics
- Google Analytics 4 integration
- Schema.org markup for blog posts
- Open Graph optimization for social sharing
- XML sitemap generation
- Proper canonical URLs for bilingual content

### Performance Optimization
- Image optimization with Next.js Image component
- Lazy loading for non-critical content
- Code splitting for better load times
- CDN integration for static assets

## Configuration
- **Main config**: `docs.json` (to be renamed to `mint.json`)
- **Primary color**: #2563eb (blue theme matching EducateAI brand)
- **Theme**: Clean, modern blog design focused on readability and engagement

## Deployment
- Automatic deployment via GitHub Actions
- Custom domain: blog.educate-ai.com
- Environment variables for newsletter integration
- Mintlify hosting with CDN

## Migration Checklist
- [ ] Update docs.json to mint.json with blog configuration
- [ ] Create blog directory structure
- [ ] Import existing posts from Ghost export
- [ ] Convert posts to MDX format
- [ ] Implement custom blog components
- [ ] Set up bilingual navigation
- [ ] Configure newsletter integration
- [ ] Test all functionality before go-live

## Content Guidelines
- Focus on educational technology trends and AI applications
- Include practical implementation strategies
- Provide downloadable resources when relevant
- Maintain consistent publishing schedule
- Engage with education community through comments and social media