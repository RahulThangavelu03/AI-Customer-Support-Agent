
"use client";

import { useEffect, useState } from "react";

type ActivityLog = {
  type: "tool_requested" | "tool_result";
  tool: string;
  arguments?: Record<string, unknown>;
  result?: Record<string, unknown> | string;
};

export default function AdminPage() {
  const [logs, setLogs] = useState<ActivityLog[]>([]);


useEffect(() => {
  try {
    const storedLogs = sessionStorage.getItem("agent_activity_logs");

    if (storedLogs) {
      setLogs(JSON.parse(storedLogs));
    }
  } catch (error) {
    console.error("Failed to load agent activity logs:", error);
  }
}, []);

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
            Monitor customer-support agent tool execution.
          </p>
        </header>

        <section className="rounded-2xl border border-zinc-200 bg-white shadow-sm">
          <div className="flex items-center justify-between border-b border-zinc-200 px-6 py-4">
            <div>
              <h2 className="font-semibold text-zinc-900">
                Activity Log
              </h2>

              <p className="text-sm text-zinc-500">
                Activity from the current support session
              </p>
            </div>


            <div className="text-sm text-zinc-500">
              {logs.length} log entries
                </div>
          </div>

          {logs.length === 0 ? (
            <div className="px-6 py-12 text-center">
              <p className="text-sm text-zinc-500">
                No agent activity recorded yet.
              </p>

              <p className="mt-1 text-xs text-zinc-400">
                Start a conversation from the customer support page.
              </p>
            </div>
          ) : (
            <div className="divide-y divide-zinc-100">
              {logs.map((log, index) => {
                const isRequest = log.type === "tool_requested";

                return (
                  <div
                    key={index}
                    className="flex gap-4 px-6 py-5"
                  >
                    <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-zinc-100 text-xs font-semibold text-zinc-600">
                      {index + 1}
                    </div>

                    <div className="flex-1">
                      <h3 className="font-medium text-zinc-900">
                        {isRequest
                          ? `Tool requested: ${log.tool}`
                          : `Tool result: ${log.tool}`}
                      </h3>

                      <div className="mt-2 rounded-lg bg-zinc-50 p-3">
                        <pre className="overflow-x-auto whitespace-pre-wrap text-xs text-zinc-600">
                          {JSON.stringify(
                            isRequest ? log.arguments : log.result,
                            null,
                            2
                          )}
                        </pre>
                      </div>
                    </div>

                    <span className="self-start rounded-full bg-green-50 px-2.5 py-1 text-xs font-medium text-green-700">
                      completed
                    </span>
                  </div>
                );
              })}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}

