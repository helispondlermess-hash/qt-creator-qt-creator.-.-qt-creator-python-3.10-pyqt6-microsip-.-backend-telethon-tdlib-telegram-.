"use client";
import { useState, useEffect } from "react";

interface Contact {
  id: number;
  name: string;
  phone: string;
  username: string | null;
}

interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
}

export default function Home() {
  const [apiId, setApiId] = useState("");
  const [apiHash, setApiHash] = useState("");
  const [phone, setPhone] = useState("");
  const [isConnected, setIsConnected] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [callStatus, setCallStatus] = useState("");

  const checkStatus = async () => {
    try {
      const res = await fetch("/api/status");
      const data = await res.json();
      setIsConnected(data.connected);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    checkStatus();
  }, []);

  const handleLogin = async () => {
    if (!apiId || !apiHash) {
      setError("API ID и API Hash обязательны");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_id: apiId, api_hash: apiHash, phone }),
      });
      const data = await res.json();
      if (data.error) {
        setError(data.error);
      } else {
        setUser(data.user);
        setIsConnected(true);
        loadContacts();
      }
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const loadContacts = async () => {
    try {
      const res = await fetch("/api/contacts");
      const data = await res.json();
      if (data.contacts) {
        setContacts(data.contacts);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleCall = async (userId: number) => {
    setCallStatus("Инициируем звонок...");
    try {
      const res = await fetch("/api/call", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId }),
      });
      const data = await res.json();
      if (data.success) {
        setCallStatus("Звонок инициирован!");
      } else {
        setCallStatus(data.error || "Ошибка");
      }
    } catch (e: any) {
      setCallStatus(e.message);
    }
  };

  const handleLogout = async () => {
    await fetch("/api/logout", { method: "POST" });
    setIsConnected(false);
    setUser(null);
    setContacts([]);
  };

  return (
    <div className="min-h-screen bg-neutral-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8 text-center">
          Telegram Caller
        </h1>

        {!isConnected ? (
          <div className="max-w-md mx-auto bg-neutral-800 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Вход в Telegram</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-neutral-400 mb-1">API ID</label>
                <input
                  type="text"
                  value={apiId}
                  onChange={(e) => setApiId(e.target.value)}
                  className="w-full bg-neutral-700 border border-neutral-600 rounded px-3 py-2 focus:outline-none focus:border-blue-500"
                  placeholder="Введите API ID"
                />
              </div>
              <div>
                <label className="block text-sm text-neutral-400 mb-1">API Hash</label>
                <input
                  type="text"
                  value={apiHash}
                  onChange={(e) => setApiHash(e.target.value)}
                  className="w-full bg-neutral-700 border border-neutral-600 rounded px-3 py-2 focus:outline-none focus:border-blue-500"
                  placeholder="Введите API Hash"
                />
              </div>
              <div>
                <label className="block text-sm text-neutral-400 mb-1">Телефон (опционально)</label>
                <input
                  type="text"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  className="w-full bg-neutral-700 border border-neutral-600 rounded px-3 py-2 focus:outline-none focus:border-blue-500"
                  placeholder="+7XXXXXXXXXX"
                />
              </div>
              {error && <p className="text-red-400 text-sm">{error}</p>}
              <button
                onClick={handleLogin}
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-neutral-600 rounded py-2 font-semibold transition-colors"
              >
                {loading ? "Подключение..." : "Подключиться"}
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="bg-neutral-800 rounded-lg p-4 flex justify-between items-center">
              <div>
                <p className="text-neutral-400">Подключен как:</p>
                <p className="font-semibold">{user?.first_name} {user?.last_name}</p>
                <p className="text-sm text-neutral-400">@{user?.username}</p>
              </div>
              <button
                onClick={handleLogout}
                className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded font-semibold"
              >
                Выйти
              </button>
            </div>

            {callStatus && (
              <div className="bg-blue-900/50 border border-blue-500 rounded-lg p-4 text-center">
                {callStatus}
              </div>
            )}

            <div className="bg-neutral-800 rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Контакты</h2>
              {contacts.length === 0 ? (
                <p className="text-neutral-400">Загрузка контактов...</p>
              ) : (
                <div className="space-y-2">
                  {contacts.map((contact) => (
                    <div
                      key={contact.id}
                      className="flex justify-between items-center bg-neutral-700 rounded p-3"
                    >
                      <div>
                        <p className="font-medium">{contact.name}</p>
                        <p className="text-sm text-neutral-400">{contact.phone}</p>
                      </div>
                      <button
                        onClick={() => handleCall(contact.id)}
                        className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded font-semibold"
                      >
                        Позвонить
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}