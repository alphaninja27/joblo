import { useState } from 'react';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const searchJobs = async () => {
    setLoading(true);
    try {
      // Pick from env or fallback to window origin
      const apiUrl = import.meta.env.VITE_API_URL || window.location.origin;
      const cleanUrl = apiUrl.replace(/\/$/, '');
      console.log("👉 Using API URL:", cleanUrl);

      const res = await fetch(`${cleanUrl}/api/match`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });

      if (!res.ok) throw new Error(`❌ Failed to fetch: ${res.status}`);
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error("❌ Error searching jobs:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-4">BuddyBot Search</h1>

      <div className="flex space-x-2">
        <input
          type="text"
          className="flex-1 p-3 border border-gray-300 rounded-lg"
          placeholder="e.g. remote python jobs"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          onClick={searchJobs}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </div>

      <div className="mt-6 space-y-4">
        {results.length === 0 && !loading && (
          <p className="text-gray-500">No results yet.</p>
        )}
        {results.map((job, i) => (
          <div key={i} className="p-4 rounded-lg shadow border bg-white">
            <h2 className="text-xl font-semibold">{job.title} at {job.company}</h2>
            <p className="text-gray-600">{job.location}</p>
            <p className="text-sm mt-2 text-gray-800">{job.description}</p>
            <a href={job.url} className="text-blue-600 mt-2 inline-block" target="_blank" rel="noopener noreferrer">
              View Job
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
