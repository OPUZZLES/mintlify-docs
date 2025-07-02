import React from 'react';

interface BlogPostProps {
  title: string;
  description: string;
  author: string;
  date: string;
  readTime: string;
  category: string;
  featuredImage?: string;
  children: React.ReactNode;
}

export default function BlogPost({
  title,
  description,
  author,
  date,
  readTime,
  category,
  featuredImage,
  children,
}: BlogPostProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const getCategoryColor = (cat: string) => {
    switch (cat.toLowerCase()) {
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
    <article className="max-w-4xl mx-auto">
      {/* Featured Image */}
      {featuredImage && (
        <div className="mb-8 rounded-lg overflow-hidden">
          <img
            src={featuredImage}
            alt={title}
            className="w-full h-64 object-cover"
          />
        </div>
      )}

      {/* Header */}
      <header className="mb-8">
        <div className="flex items-center gap-4 mb-4">
          <span
            className={`px-3 py-1 rounded-full text-sm font-medium ${getCategoryColor(
              category
            )}`}
          >
            {category.charAt(0).toUpperCase() + category.slice(1)}
          </span>
          <span className="text-gray-500 text-sm">{readTime}</span>
        </div>

        <h1 className="text-4xl font-bold text-gray-900 mb-4">{title}</h1>
        
        <p className="text-xl text-gray-600 mb-6">{description}</p>

        <div className="flex items-center gap-4 pb-6 border-b border-gray-200">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold">
              {author.charAt(0)}
            </div>
            <div>
              <p className="font-medium text-gray-900">{author}</p>
              <p className="text-sm text-gray-500">{formatDate(date)}</p>
            </div>
          </div>
        </div>
      </header>

      {/* Content */}
      <div className="prose prose-lg max-w-none">
        {children}
      </div>

      {/* Footer */}
      <footer className="mt-12 pt-8 border-t border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-gray-500">Written by</span>
            <span className="font-medium text-gray-900">{author}</span>
          </div>
          <div className="flex gap-2">
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              Share
            </button>
          </div>
        </div>
      </footer>
    </article>
  );
}