import React, { useEffect, useState } from "react";
import { useApp } from "@store/AppContext";
import ChatBot from "@features/ChatBot";
import financeAPI from "@services/financeAPI";

export default function AIPage() {
  const { state } = useApp();
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);
  const [insights, setInsights] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [execMsg, setExecMsg] = useState(null);
  const [wfRunning, setWfRunning] = useState(false);
  const [wfOutput, setWfOutput] = useState(null);
  const [executingIndex, setExecutingIndex] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        if (!state.user?.id) return;
        const s = await financeAPI.getWorkflowStatus(state.user.id);
        setStatus(s);
        // Load insights from dashboard endpoint for the AI page
        const dash = await financeAPI.getDashboard({
          user_id: state.user.id,
          timeframe: "30d",
        });
        if (Array.isArray(dash?.insights)) setInsights(dash.insights);
        if (Array.isArray(dash?.suggestions)) setSuggestions(dash.suggestions);
      } catch (e) {
        setError(e.message);
      }
    };
    load();
  }, [state.user?.id]);

  const executeSuggestion = async (sug, idx) => {
    try {
      setExecMsg(null);
      setExecutingIndex(idx);
      const res = await financeAPI.apiCall("/chat/execute", {
        method: "POST",
        body: JSON.stringify({
          user_id: state.user.id,
          action: sug.action,
          params: sug.params,
        }),
      });
      if (res?.status === "ok") {
        // Mark this suggestion as executed locally
        setSuggestions((prev) =>
          prev.map((s, i) => (i === idx ? { ...s, _executed: true } : s))
        );
        setExecMsg(`Done: ${sug.label}`);
      } else {
        setExecMsg(`Failed to execute: ${sug.label}`);
      }
    } catch (e) {
      setExecMsg(`Failed: ${e.message}`);
    } finally {
      setExecutingIndex(null);
    }
  };

  const runWorkflow = async () => {
    if (!state.user?.id) return;
    try {
      setWfRunning(true);
      setWfOutput(null);
      const res = await financeAPI.runWorkflow({
        message: "Run workflow",
        user_id: state.user.id,
        workflow_stage:
          status?.current_stage || state.workflowStage || "Started",
        context: {},
      });
      setWfOutput(res);
    } catch (e) {
      setWfOutput({ error: e.message });
    } finally {
      setWfRunning(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h1 className="text-2xl font-bold mb-2">AI Assistant</h1>
        <p className="text-gray-600">
          Chat with the finance agent and view workflow progress.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-2">Workflow Progress</h2>
          {error && <p className="text-red-600 text-sm">{error}</p>}
          {status ? (
            <ul className="text-sm text-gray-700 list-disc ml-5 space-y-1">
              <li>
                Current stage:{" "}
                {String(
                  status.current_stage || status.stage || state.workflowStage
                )}
              </li>
              {Array.isArray(status.next_steps) &&
                status.next_steps.length > 0 && (
                  <li>Next steps: {status.next_steps.join(", ")}</li>
                )}
            </ul>
          ) : (
            <p className="text-gray-500 text-sm">No status yet.</p>
          )}
          <div className="mt-4">
            <button
              onClick={runWorkflow}
              disabled={wfRunning || !state.user?.id}
              className={`px-3 py-1 text-sm rounded text-white ${
                wfRunning ? "bg-gray-400" : "bg-green-600 hover:bg-green-700"
              }`}
            >
              {wfRunning ? "Running..." : "Run Workflow"}
            </button>
          </div>
          {wfOutput && (
            <div className="mt-4 border rounded p-3 bg-gray-50">
              {wfOutput.error ? (
                <p className="text-red-600 text-sm">{wfOutput.error}</p>
              ) : (
                <>
                  {Array.isArray(wfOutput.explanations) &&
                  wfOutput.explanations.length > 0 ? (
                    <ul className="list-disc ml-5 space-y-1 text-sm text-gray-800">
                      {wfOutput.explanations.map((ex, i) => (
                        <li key={i}>
                          <span className="font-medium">
                            {ex.step || ex.what || `Step ${i + 1}`}:
                          </span>{" "}
                          <span className="opacity-90">{ex.what || ""}</span>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-gray-600 text-sm">No steps returned.</p>
                  )}
                  {wfOutput.response && (
                    <p className="text-sm text-gray-700 mt-2">
                      <span className="font-semibold">Summary:</span>{" "}
                      {wfOutput.response}
                    </p>
                  )}
                </>
              )}
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Chat</h2>
          <ChatBot variant="inline" />
        </div>
      </div>

      {/* AI Insights and Suggestions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">AI Insights</h2>
        <div className="space-y-3">
          {insights?.map((insight, i) => (
            <div
              key={i}
              className="p-3 rounded-lg border bg-blue-50 border-blue-200 text-blue-800"
            >
              <h4 className="font-medium mb-1">{insight.title}</h4>
              <p className="text-sm opacity-90">{insight.description}</p>
              {insight.category && (
                <p className="text-xs mt-1 opacity-75">
                  Category: {insight.category}
                </p>
              )}
            </div>
          ))}
          {(!insights || insights.length === 0) && (
            <p className="text-gray-500 text-sm">No insights available.</p>
          )}
        </div>
        <div className="mt-6">
          <h3 className="text-md font-semibold mb-3">Suggested Actions</h3>
          {execMsg && <p className="text-sm mb-2">{execMsg}</p>}
          <div className="space-y-2">
            {suggestions?.map((sug, i) => (
              <div key={i} className="p-3 rounded-lg border bg-gray-50">
                {sug._executed ? (
                  <div className="flex items-center text-green-700">
                    <svg
                      className="w-5 h-5 mr-2 text-green-600"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                      ></path>
                    </svg>
                    <p className="text-sm font-medium">Executed successfully</p>
                  </div>
                ) : (
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium">{sug.label}</p>
                      {sug.explain && (
                        <p className="text-xs text-gray-600 mt-1">
                          {sug.explain}
                        </p>
                      )}
                    </div>
                    <button
                      onClick={() => executeSuggestion(sug, i)}
                      disabled={executingIndex === i}
                      className={`px-3 py-1 text-sm rounded text-white ${
                        executingIndex === i
                          ? "bg-gray-400"
                          : "bg-blue-600 hover:bg-blue-700"
                      }`}
                    >
                      {executingIndex === i ? "Executing..." : "Execute"}
                    </button>
                  </div>
                )}
              </div>
            ))}
            {(!suggestions || suggestions.length === 0) && (
              <p className="text-gray-500 text-sm">
                No suggestions at this time.
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
