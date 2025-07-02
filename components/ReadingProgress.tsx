import React, { useEffect, useState } from 'react';

interface ReadingProgressProps {
  target?: string; // CSS selector for the content area
  className?: string;
}

export default function ReadingProgress({
  target = 'article',
  className = '',
}: ReadingProgressProps) {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const updateProgress = () => {
      const article = document.querySelector(target);
      if (!article) return;

      const scrollTop = window.scrollY;
      const articleTop = article.offsetTop;
      const articleHeight = article.offsetHeight;
      const windowHeight = window.innerHeight;

      const startReading = articleTop - windowHeight * 0.3;
      const finishReading = articleTop + articleHeight - windowHeight * 0.7;

      if (scrollTop < startReading) {
        setProgress(0);
      } else if (scrollTop > finishReading) {
        setProgress(100);
      } else {
        const progressPercentage = 
          ((scrollTop - startReading) / (finishReading - startReading)) * 100;
        setProgress(Math.min(Math.max(progressPercentage, 0), 100));
      }
    };

    window.addEventListener('scroll', updateProgress);
    window.addEventListener('resize', updateProgress);
    updateProgress();

    return () => {
      window.removeEventListener('scroll', updateProgress);
      window.removeEventListener('resize', updateProgress);
    };
  }, [target]);

  return (
    <>
      {/* Fixed progress bar at top */}
      <div 
        className={`fixed top-0 left-0 right-0 h-1 bg-blue-600 z-50 transition-all duration-150 ease-out ${className}`}
        style={{ 
          width: `${progress}%`,
          opacity: progress > 0 ? 1 : 0 
        }}
      />
      
      {/* Circular progress indicator (optional) */}
      <div className="fixed bottom-8 right-8 z-40">
        {progress > 0 && progress < 100 && (
          <div className="relative">
            <svg className="w-12 h-12 transform -rotate-90" viewBox="0 0 40 40">
              <circle
                cx="20"
                cy="20"
                r="16"
                fill="none"
                stroke="#e5e7eb"
                strokeWidth="3"
              />
              <circle
                cx="20"
                cy="20"
                r="16"
                fill="none"
                stroke="#2563eb"
                strokeWidth="3"
                strokeDasharray={`${2 * Math.PI * 16}`}
                strokeDashoffset={`${2 * Math.PI * 16 * (1 - progress / 100)}`}
                strokeLinecap="round"
                className="transition-all duration-150 ease-out"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-xs font-medium text-gray-700">
                {Math.round(progress)}%
              </span>
            </div>
          </div>
        )}
      </div>
    </>
  );
}