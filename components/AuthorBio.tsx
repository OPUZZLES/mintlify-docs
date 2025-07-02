import React from 'react';

interface AuthorBioProps {
  name: string;
  bio?: string;
  email?: string;
  website?: string;
  avatar?: string;
  compact?: boolean;
}

export default function AuthorBio({
  name,
  bio = "Pierre Illsley is the founder of EducateAI, pioneering AI-powered educational technology to help students learn more effectively through personalized learning experiences.",
  email = "illsley.pierre@gmx.de",
  website = "https://educate-ai.com",
  avatar,
  compact = false,
}: AuthorBioProps) {
  if (compact) {
    return (
      <div className="flex items-center gap-3 py-4">
        <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold text-lg">
          {name.split(' ').map(n => n[0]).join('')}
        </div>
        <div>
          <p className="font-semibold text-gray-900">{name}</p>
          <p className="text-sm text-gray-600">Founder, EducateAI</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gray-50 rounded-xl p-6 my-8 border border-gray-200">
      <div className="flex items-start gap-4">
        <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold text-xl flex-shrink-0">
          {avatar ? (
            <img src={avatar} alt={name} className="w-full h-full rounded-full object-cover" />
          ) : (
            name.split(' ').map(n => n[0]).join('')
          )}
        </div>
        
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-1">{name}</h3>
          <p className="text-blue-600 font-medium mb-3">Founder & CEO, EducateAI</p>
          <p className="text-gray-600 mb-4 leading-relaxed">{bio}</p>
          
          <div className="flex flex-wrap gap-4">
            {email && (
              <a
                href={`mailto:${email}`}
                className="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1"
              >
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                </svg>
                Contact
              </a>
            )}
            
            {website && (
              <a
                href={website}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1"
              >
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4.083 9h1.946c.089-1.546.383-2.97.837-4.118A6.004 6.004 0 004.083 9zM10 2a8 8 0 100 16 8 8 0 000-16zm0 2c-.076 0-.232.032-.465.262-.238.234-.497.623-.737 1.182-.389.907-.673 2.142-.766 3.556h3.936c-.093-1.414-.377-2.649-.766-3.556-.24-.559-.499-.948-.737-1.182C10.232 4.032 10.076 4 10 4zm3.971 5c-.089-1.546-.383-2.97-.837-4.118A6.004 6.004 0 0115.917 9h-1.946zm-2.003 2H8.032c.093 1.414.377 2.649.766 3.556.24.559.499.948.737 1.182.233.23.389.262.465.262.076 0 .232-.032.465-.262.238-.234.497-.623.737-1.182.389-.907.673-2.142.766-3.556zm1.166 4.118c.454-1.148.748-2.572.837-4.118h1.946a6.004 6.004 0 01-2.783 4.118zm-6.268 0C6.412 13.97 6.118 12.546 6.03 11H4.083a6.004 6.004 0 002.783 4.118z" clipRule="evenodd" />
                </svg>
                Website
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}