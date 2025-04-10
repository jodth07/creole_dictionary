// src/App.tsx
import React, { useState } from 'react';
import axios from 'axios';

interface WordDefinition {
  word: string;
  definition: string;
  source: string;
}

interface ChatResponse {
  reply: string;
  definitions: WordDefinition[];
}

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState<ChatResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post<ChatResponse>('/api/chat', { message });
      setResponse(res.data);
    } catch (error) {
      console.error(error);
      setResponse({ reply: 'Erè pandan analiz mesaj la.', definitions: [] });
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-2xl mx-auto bg-white rounded-2xl shadow p-6">
        <h1 className="text-2xl font-bold mb-4">Diksyonè Kreyòl Chatbot</h1>
        <form onSubmit={handleSubmit} className="mb-4">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Antre yon fraz an kreyòl"
            className="w-full p-3 border border-gray-300 rounded-xl"
          />
          <button
            type="submit"
            className="mt-2 bg-blue-500 text-white px-4 py-2 rounded-xl hover:bg-blue-600"
          >
            Voye
          </button>
        </form>

        {loading && <p>Nap chèche definisyon yo...</p>}

        {response && (
          <div className="bg-gray-50 p-4 rounded-xl">
            <p className="mb-4 whitespace-pre-line">{response.reply}</p>
            {response.definitions.length > 0 && (
              <ul className="list-disc pl-6">
                {response.definitions.map((def, idx) => (
                  <li key={idx}>
                    <strong>{def.word}</strong>: {def.definition} <em>({def.source})</em>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
