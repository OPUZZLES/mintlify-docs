import React from 'react';

interface Post {
  title: string;
  slug: string;
  description: string;
  category: string;
  readTime: string;
  featuredImage?: string;
}

interface RelatedPostsProps {
  currentCategory: string;
  currentSlug: string;
  posts?: Post[];
  maxPosts?: number;
}

// Sample related posts - in a real implementation, this would come from your content management system
const samplePosts: Post[] = [
  {
    title: "Why AI Flashcards Are the Future of Study Habits",
    slug: "why-ai-flashcards-are-the-future-of-study-habits",
    description: "Discover how AI-powered flashcards adapt to your learning style and improve retention rates significantly.",
    category: "ai",
    readTime: "7 min read",
    featuredImage: "/images/blog/photo-1597570889212-97f48e632dad.jpg"
  },
  {
    title: "How to Study Effectively: Master Spacing and Active Recall",
    slug: "how-to-study-effectively-master-spacing-and-active-recall-for-academic-success",
    description: "Learn evidence-based techniques for optimal learning retention and academic success.",
    category: "guides",
    readTime: "12 min read",
    featuredImage: "/images/blog/photo-1522202176988-66273c2fd55f.jpg"
  },
  {
    title: "The Science of Learning",
    slug: "the-science-of-learning-understanding-how-your-brain-absorbs-and-retains-information",
    description: "Understand how your brain processes and retains information for better study strategies.",
    category: "science",
    readTime: "10 min read",
    featuredImage: "/images/blog/photo-1559757148-5c350d0d3c56.jpg"
  }
];

export default function RelatedPosts({
  currentCategory,
  currentSlug,
  posts = samplePosts,
  maxPosts = 3,
}: RelatedPostsProps) {
  // Filter and sort related posts
  const relatedPosts = posts
    .filter(post => post.slug !== currentSlug) // Exclude current post
    .sort((a, b) => {
      // Prioritize posts from the same category
      if (a.category === currentCategory && b.category !== currentCategory) return -1;
      if (b.category === currentCategory && a.category !== currentCategory) return 1;
      return 0;
    })
    .slice(0, maxPosts);

  if (relatedPosts.length === 0) {
    return null;
  }

  const getCategoryColor = (category: string) => {
    switch (category.toLowerCase()) {
      case 'ai':
      case 'ki':
        return 'bg-blue-100 text-blue-800';
      case 'guides':
      case 'leitfäden':
        return 'bg-green-100 text-green-800';
      case 'science':
      case 'wissenschaft':
        return 'bg-purple-100 text-purple-800';
      case 'tips-and-tricks':
      case 'tipps-und-tricks':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <section className="my-12 py-8 border-t border-gray-200">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Related Articles</h2>
      
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {relatedPosts.map((post, index) => (
          <article
            key={post.slug}
            className="bg-white rounded-lg border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow duration-200"
          >
            {post.featuredImage && (
              <div className="aspect-video overflow-hidden">
                <img
                  src={post.featuredImage}
                  alt={post.title}
                  className="w-full h-full object-cover hover:scale-105 transition-transform duration-200"
                />
              </div>
            )}
            
            <div className="p-6">
              <div className="flex items-center gap-2 mb-3">
                <span
                  className={`px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(
                    post.category
                  )}`}
                >
                  {post.category.charAt(0).toUpperCase() + post.category.slice(1)}
                </span>
                <span className="text-gray-500 text-xs">{post.readTime}</span>
              </div>
              
              <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                <a
                  href={`/blog/${post.category}/${post.slug}`}
                  className="hover:text-blue-600 transition-colors"
                >
                  {post.title}
                </a>
              </h3>
              
              <p className="text-gray-600 text-sm line-clamp-3 mb-4">
                {post.description}
              </p>
              
              <a
                href={`/blog/${post.category}/${post.slug}`}
                className="text-blue-600 hover:text-blue-800 text-sm font-medium inline-flex items-center gap-1"
              >
                Read more
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </a>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}