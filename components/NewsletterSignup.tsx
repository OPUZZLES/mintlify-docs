import React, { useState } from 'react';

interface NewsletterSignupProps {
  title?: string;
  description?: string;
  placeholder?: string;
  buttonText?: string;
  variant?: 'default' | 'compact' | 'inline';
}

export default function NewsletterSignup({
  title = "Stay Updated with AI Learning Insights",
  description = "Get weekly tips on AI-powered learning, study techniques, and educational technology trends directly in your inbox.",
  placeholder = "Enter your email address",
  buttonText = "Subscribe",
  variant = 'default',
}: NewsletterSignupProps) {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;

    setStatus('loading');
    
    try {
      // TODO: Replace with actual newsletter service endpoint
      const response = await fetch('/api/newsletter/subscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (response.ok) {
        setStatus('success');
        setEmail('');
      } else {
        setStatus('error');
      }
    } catch (error) {
      setStatus('error');
    }
  };

  if (variant === 'compact') {
    return (
      <div className="bg-blue-50 rounded-lg p-6 border border-blue-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder={placeholder}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <button
            type="submit"
            disabled={status === 'loading'}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            {status === 'loading' ? 'Subscribing...' : buttonText}
          </button>
        </form>
        {status === 'success' && (
          <p className="text-green-600 text-sm mt-2">✓ Successfully subscribed!</p>
        )}
        {status === 'error' && (
          <p className="text-red-600 text-sm mt-2">✗ Something went wrong. Please try again.</p>
        )}
      </div>
    );
  }

  if (variant === 'inline') {
    return (
      <div className="my-8 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border-l-4 border-blue-500">
        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3">
          <div className="flex-1">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder={placeholder}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <button
            type="submit"
            disabled={status === 'loading'}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            {status === 'loading' ? 'Subscribing...' : buttonText}
          </button>
        </form>
        {status === 'success' && (
          <p className="text-green-600 text-sm mt-2">✓ Successfully subscribed!</p>
        )}
        {status === 'error' && (
          <p className="text-red-600 text-sm mt-2">✗ Something went wrong. Please try again.</p>
        )}
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-xl p-8 text-white my-12">
      <div className="max-w-2xl mx-auto text-center">
        <h2 className="text-2xl font-bold mb-4">{title}</h2>
        <p className="text-blue-100 mb-6">{description}</p>
        
        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder={placeholder}
            className="flex-1 px-4 py-3 rounded-lg border-0 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-blue-600"
            required
          />
          <button
            type="submit"
            disabled={status === 'loading'}
            className="px-6 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-gray-100 disabled:opacity-50 transition-colors"
          >
            {status === 'loading' ? 'Subscribing...' : buttonText}
          </button>
        </form>

        {status === 'success' && (
          <p className="text-green-200 mt-4">✓ Thank you for subscribing! Check your email to confirm.</p>
        )}
        {status === 'error' && (
          <p className="text-red-200 mt-4">✗ Something went wrong. Please try again later.</p>
        )}

        <p className="text-blue-200 text-sm mt-4">
          No spam, unsubscribe at any time. We respect your privacy.
        </p>
      </div>
    </div>
  );
}