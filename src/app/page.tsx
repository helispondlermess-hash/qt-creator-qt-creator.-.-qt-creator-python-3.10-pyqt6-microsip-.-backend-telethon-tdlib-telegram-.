"use client";
import { useState } from "react";

interface Contact {
  id: number;
  name: string;
  phone: string;
  username: string | null;
}

interface User {
  id: number;
  username: string | null;
  first_name: string;
  last_name: string | null;
}

export default function Home() {
  const [step, setStep] = useState<"phone" | "code" | "dashboard">("phone");
  const [phone, setPhone] = useState("");
  const [code, setCode] = useState("");
  const [apiId, setApiId] = useState("");
  const [apiHash, setApiHash] = useState("");
  const [phoneCodeHash, setPhoneCodeHash] = useState("");
  const [session, setSession] = useState("");
  const [user, setUser] = useState<User | null>(null);
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSendCode = async () => {
    if (!phone || !apiId || !apiHash) {
      setError("Заполните все поля");
      return;
    }
    setLoading(true);
    setError("");
    
    try {
      let phoneNum = phone.trim();
      if (!phoneNum.startsWith("+")) {
        phoneNum = "+" + phoneNum;
      }
      
      const res = await fetch("/api/auth/send-code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          phone: phoneNum,
          api_id: apiId,
          api_hash: apiHash
        }),
      });
      const data = await res.json();
      
      if (data.error) {
        setError(data.error);
      } else {
        setPhoneCodeHash(data.phone_code_hash);
        setStep("code");
      }
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyCode = async () => {
    if (!code) {
      setError("Введите код");
      return;
    }
    setLoading(true);
    setError("");
    
    try {
      let phoneNum = phone.trim();
      if (!phoneNum.startsWith("+")) {
        phoneNum = "+" + phoneNum;
      }
      
      const res = await fetch("/api/auth/verify-code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          phone: phoneNum,
          code: code,
        }),
      });
      const data = await res.json();
      
      if (data.error) {
        setError(data.error);
      } else {
        setUser(data.user);
        setSession(data.session);
        loadContacts(data.session);
        setStep("dashboard");
      }
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const loadContacts = async (sessionToken: string) => {
    try {
      const res = await fetch("/api/contacts", {
        headers: { "Authorization": `Bearer ${sessionToken}` },
      });
      const data = await res.json();
      if (data.contacts) {
        setContacts(data.contacts);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleLogout = async () => {
    if (session) {
      try {
        await fetch("/api/auth/logout", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session }),
        });
      } catch (e) {
        console.error(e);
      }
    }
    setSession("");
    setUser(null);
    setContacts([]);
    setStep("phone");
    setPhone("");
    setCode("");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center text-white mb-8">
          Telegram Caller
        </h1>

        {step === "phone" && (
          <div className="max-w-md mx-auto bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
            <h2 className="text-2xl font-semibold text-white mb-6 text-center">
              Вход / Регистрация
            </h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-300 mb-1">API ID</label>
                <input
                  type="text"
                  value={apiId}
                  onChange={(e) => setApiId(e.target.value)}
                  className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-pink-500"
                  placeholder="Получите на my.telegram.org"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-300 mb-1">API Hash</label>
                <input
                  type="text"
                  value={apiHash}
                  onChange={(e) => setApiHash(e.target.value)}
                  className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-pink-500"
                  placeholder="Получите на my.telegram.org"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-300 mb-1">Номер телефона</label>
                <input
                  type="text"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-pink-500"
                  placeholder="+79991234567"
                />
              </div>
              
              {error && (
                <div className="bg-red-500/20 border border-red-500 rounded-lg p-3 text-red-300 text-sm">
                  {error}
                </div>
              )}
              
              <button
                onClick={handleSendCode}
                disabled={loading}
                className="w-full bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 disabled:opacity-50 text-white font-semibold py-3 rounded-lg transition-all"
              >
                {loading ? "Отправка..." : "Получить код"}
              </button>
            </div>
            
            <p className="text-center text-gray-400 text-sm mt-4">
              Код придет в ваш Telegram
            </p>
          </div>
        )}

        {step === "code" && (
          <div className="max-w-md mx-auto bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
            <h2 className="text-2xl font-semibold text-white mb-6 text-center">
              Подтверждение
            </h2>
            
            <p className="text-gray-300 text-center mb-6">
              Введите код, отправленный в Telegram на номер<br />
              <span className="text-white font-semibold">{phone}</span>
            </p>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-300 mb-1">Код из Telegram</label>
                <input
                  type="text"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-pink-500 text-center text-2xl tracking-widest"
                  placeholder="12345"
                  maxLength={5}
                />
              </div>
              
              {error && (
                <div className="bg-red-500/20 border border-red-500 rounded-lg p-3 text-red-300 text-sm">
                  {error}
                </div>
              )}
              
              <button
                onClick={handleVerifyCode}
                disabled={loading || code.length < 3}
                className="w-full bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 disabled:opacity-50 text-white font-semibold py-3 rounded-lg transition-all"
              >
                {loading ? "Проверка..." : "Войти"}
              </button>
              
              <button
                onClick={() => {
                  setStep("phone");
                  setCode("");
                  setError("");
                }}
                className="w-full text-gray-400 hover:text-white text-sm py-2"
              >
                Назад
              </button>
            </div>
          </div>
        )}

        {step === "dashboard" && user && (
          <div className="max-w-2xl mx-auto space-y-6">
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Вход выполнен</p>
                  <h2 className="text-2xl font-semibold text-white">
                    {user.first_name} {user.last_name || ""}
                  </h2>
                  <p className="text-gray-400">@{user.username || "нет username"}</p>
                  <p className="text-gray-500 text-sm">ID: {user.id}</p>
                </div>
                <button
                  onClick={handleLogout}
                  className="bg-red-500/20 hover:bg-red-500/30 text-red-300 px-4 py-2 rounded-lg transition-colors"
                >
                  Выйти
                </button>
              </div>
            </div>
            
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
              <h3 className="text-xl font-semibold text-white mb-4">Контакты</h3>
              {contacts.length === 0 ? (
                <p className="text-gray-400">Контактов не найдено</p>
              ) : (
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {contacts.map((contact) => (
                    <div
                      key={contact.id}
                      className="flex items-center justify-between bg-white/5 rounded-lg p-3 hover:bg-white/10 transition-colors"
                    >
                      <div>
                        <p className="text-white font-medium">{contact.name}</p>
                        <p className="text-gray-400 text-sm">{contact.phone || "@" + contact.username}</p>
                      </div>
                      <button className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
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