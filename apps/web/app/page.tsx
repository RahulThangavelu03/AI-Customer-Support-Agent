"use client";

import { FormEvent, useState } from "react";

const DEMO_MODE = true;

export default function Home() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<
    { role: "user" | "agent"; content: string }[]
  >([]);


  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
  event.preventDefault();

  if (!message.trim()) return;

  const userMessage = message;

  setMessages((current) => [
    ...current,
    { role: "user", content: userMessage },
  ]);

  setMessage("");

  if (DEMO_MODE) {
    setTimeout(() => {
      setMessages((current) => [
        ...current,
        {
          role: "agent",
          content:
            "Your refund for order O1004 has been processed successfully. A refund of $2999 will be returned to your original payment method.",
        },
      ]);
    }, 700);

    return;
  }

  try {
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: userMessage,
      }),
    });

    if (!response.ok) {
      throw new Error("Request failed");
    }

    const data = await response.json();

    setMessages((current) => [
      ...current,
      { role: "agent", content: data.response },
    ]);
  } catch (error) {
    console.error(error);

    setMessages((current) => [
      ...current,
      {
        role: "agent",
        content: "Sorry, something went wrong while contacting support.",
      },
    ]);
  }
}
  return (
    <main className="min-h-screen bg-zinc-100 px-4 py-8">
      <div className="mx-auto flex h-[calc(100vh-4rem)] max-w-4xl flex-col overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-sm">
        {/* Header */}
        <header className="border-b border-zinc-200 px-6 py-5">
          <h1 className="text-xl font-semibold text-zinc-900">
            AI Customer Support
          </h1>
          <p className="mt-1 text-sm text-zinc-500">
            Refund and order support assistant
          </p>
        </header>

        {/* Chat */}
        <section className="flex-1 overflow-y-auto p-6">
          {messages.length === 0 ? (
            <div className="flex h-full items-center justify-center">
              <div className="max-w-md text-center">
                <h2 className="text-2xl font-semibold text-zinc-900">
                  How can we help?
                </h2>
                <p className="mt-2 text-sm text-zinc-500">
                  Ask about an order or request a refund.
                </p>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((item, index) => (
                <div
                  key={index}
                  className={`flex ${
                    item.role === "user"
                      ? "justify-end"
                      : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm ${
                      item.role === "user"
                        ? "bg-zinc-900 text-white"
                        : "bg-zinc-100 text-zinc-900"
                    }`}
                  >
                    {item.content}
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* Input */}
        <form
          onSubmit={handleSubmit}
          className="border-t border-zinc-200 p-4"
        >
          <div className="flex gap-3">
            <input
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              placeholder="Ask about an order or refund..."
              className="flex-1 rounded-xl border border-zinc-300 px-4 py-3 text-sm outline-none focus:border-zinc-500"
            />

            <button
              type="submit"
              className="rounded-xl bg-zinc-900 px-6 py-3 text-sm font-medium text-white transition hover:bg-zinc-700"
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </main>
  );
}