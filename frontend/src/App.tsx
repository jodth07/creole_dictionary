// src/App.tsx
import React, { useEffect, useRef, useState } from 'react';
import axios from 'axios';

interface WordDefinition {
  word: string;
  definition: string;
  source: string;
  image_url?: string;
}

interface ChatResponse {
  reply: string;
  definitions: WordDefinition[];
}

interface Message {
  sender: 'user' | 'bot';
  text: string;
  definitions?: WordDefinition[];
}

function App() {
  const [message, setMessage] = useState('');
  const [conversation, setConversation] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [showImages, setShowImages] = useState(true);
  const chatEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [conversation, loading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;

    const userMessage: Message = { sender: 'user', text: message };
    setConversation((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const res = await axios.post<ChatResponse>('/api/chat', { message });
      const botMessage: Message = {
        sender: 'bot',
        text: res.data.reply,
        definitions: res.data.definitions
      };
      setConversation((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error(error);
      setConversation((prev) => [
        ...prev,
        { sender: 'bot', text: '⚠️ Erè pandan analiz mesaj la.' },
      ]);
    } finally {
      setLoading(false);
      setMessage('');
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-2xl mx-auto bg-white rounded-2xl shadow p-6">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-2xl font-bold">💬 Diksyonè Kreyòl Chatbot</h1>
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={showImages}
              onChange={() => setShowImages(!showImages)}
            />
            Montre imaj
          </label>
        </div>

        <div className="space-y-3 mb-6 max-h-[60vh] overflow-y-auto">
          {conversation.map((msg, idx) => (
            <div key={idx} className="w-fit max-w-[90%]">
              <div
                className={`p-3 rounded-xl ${
                  msg.sender === 'user'
                    ? 'ml-auto bg-blue-500 text-white'
                    : 'mr-auto bg-gray-200'
                }`}
              >
                {msg.text}
              </div>

              {msg.definitions?.map((def, defIdx) => (
                <div
                  key={defIdx}
                  className="mt-2 ml-4 bg-white border border-gray-300 rounded-lg p-3"
                >
                  <p className="font-bold">{def.word}</p>
                  <p className="text-sm">{def.definition}</p>
                  <p className="text-xs text-gray-500">Sous: {def.source}</p>
                  {showImages && def.image_url && (
                    <img
                      src={def.image_url}
                      alt={`Imaj pou ${def.word}`}
                      className="mt-2 max-w-xs rounded-md border"
                    />
                  )}
                </div>
              ))}
            </div>
          ))}

          {loading && (
            <div className="flex items-center gap-2 text-sm text-gray-500">
              <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-blue-500"></div>
              Nap chèche definisyon yo...
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Antre fraz ou la..."
            className="flex-1 p-3 border border-gray-300 rounded-xl"
          />
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded-xl hover:bg-blue-600"
          >
            Voye
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
