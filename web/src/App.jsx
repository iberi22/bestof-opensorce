import React, { useState, useEffect } from 'react';

function App() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    // Placeholder for fetching blog posts
    setPosts([
      {
        id: 1,
        title: "Example Repo - Solving Developer Pain Points",
        date: "2025-11-23",
        repo: "example/awesome-project",
        status: "Published"
      }
    ]);
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-8">
      <header className="mb-12 text-center">
        <h1 className="text-4xl font-bold text-blue-500 mb-4">Open Source Video Generator</h1>
        <p className="text-xl text-gray-400">Automated Video Production Dashboard</p>
      </header>

      <main className="max-w-4xl mx-auto">
        <div className="grid gap-6">
          {posts.map(post => (
            <div key={post.id} className="bg-gray-800 rounded-xl p-6 border border-gray-700 hover:border-blue-500 transition-colors">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h2 className="text-2xl font-semibold mb-2">{post.title}</h2>
                  <p className="text-gray-400 text-sm">Repo: {post.repo}</p>
                </div>
                <span className="px-3 py-1 bg-green-900 text-green-300 rounded-full text-sm font-medium">
                  {post.status}
                </span>
              </div>
              <div className="flex gap-4 mt-6">
                <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-colors">
                  View Post
                </button>
                <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg font-medium transition-colors">
                  Watch Video
                </button>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;
