// src/App.tsx
import React, { useEffect, useRef, useState } from 'react';
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

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

function App() {
  const [message, setMessage] = useState('');
  const [conversation, setConversation] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
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
      const botMessage: Message = { sender: 'bot', text: res.data.reply };
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
        <h1 className="text-2xl font-bold mb-4">💬 Diksyonè Kreyòl Chatbot</h1>

        <div className="space-y-3 mb-6 max-h-[60vh] overflow-y-auto">
          {conversation.map((msg, idx) => (
            <div
              key={idx}
              className={`p-3 rounded-xl w-fit max-w-[90%] ${
                msg.sender === 'user'
                  ? 'ml-auto bg-blue-500 text-white'
                  : 'mr-auto bg-gray-200'
              }`}
            >
              {msg.text}
            </div>
          ))}
          {loading && <div className="text-sm text-gray-500">⏳ Nap chèche definisyon yo...</div>}
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
