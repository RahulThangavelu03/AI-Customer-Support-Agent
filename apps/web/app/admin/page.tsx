"use client";

import { useState } from "react";

const demoLogs = [
  {
    type: "request",
    title: "Request received",
    details: "Customer requested a refund for order O1004.",
    status: "completed",
  },
  {
    type: "tool",
    title: "Tool requested",
    details: "validate_refund → order_id: O1004",
    status: "completed",
  },
  {
    type: "validation",
    title: "Refund validation",
    details: "Order is eligible for a refund of $2999.",
    status: "completed",
  },
  {
    type: "tool",
    title: "Tool requested",
    details: "process_refund → order_id: O1004",
    status: "completed",
  },
  {
    type: "result",
    title: "Refund processed",
    details: "Refund successfully processed for O1004.",
    status: "completed",
  },
  {
    type: "response",
    title: "Agent response",
    details: "Final response sent to the customer.",
    status: "completed",
  },
];

export default function AdminPage() {
  const [logs] = useState(demoLogs);

  return (
    <main className="min-h-screen bg-zinc-100 p-6">
      <div className="mx-auto max-w-6xl">
        <header className="mb-6">
          <p className="text-sm font-medium text-zinc-500">
            ADMIN DASHBOARD
          </p>

          <h1 className="mt-1 text-3xl font-semibold text-zinc-900">
            Agent Activity
          </h1>

          <p className="mt-2 text-sm text-zinc-500">
            Monitor customer-support agent activity and tool execution.
          </p>
        </header>

        <section className="rounded-2xl border border-zinc-200 bg-white shadow-sm">
          <div className="flex items-center justify-between border-b border-zinc-200 px-6 py-4">
            <div>
              <h2 className="font-semibold text-zinc-900">
                Recent Activity
              </h2>

              <p className="text-sm text-zinc-500">
                Live agent execution events
              </p>
            </div>

            <div className="flex items-center gap-2 text-sm text-green-600">
              <span className="h-2 w-2 rounded-full bg-green-500" />
              Agent online
            </div>
          </div>

          <div className="divide-y divide-zinc-100">
            {logs.map((log, index) => (
              <div
                key={index}
                className="flex gap-4 px-6 py-5"
              >
                <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-zinc-100 text-xs font-semibold text-zinc-600">
                  {index + 1}
                </div>

                <div className="flex-1">
                  <div className="flex items-center justify-between gap-4">
                    <h3 className="font-medium text-zinc-900">
                      {log.title}
                    </h3>

                    <span className="rounded-full bg-green-50 px-2.5 py-1 text-xs font-medium text-green-700">
                      {log.status}
                    </span>
                  </div>

                  <p className="mt-1 text-sm text-zinc-500">
                    {log.details}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}