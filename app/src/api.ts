/**
 * API layer for Ma'at Legal AI Backend.
 * All endpoints require X-API-Key header for authentication.
 */

const API_BASE = "http://localhost:8000";
const API_KEY = "maat-local-dev-key-777";

const headers = (): HeadersInit => ({
  "Content-Type": "application/json",
  "X-API-Key": API_KEY,
});

/* ── Types ── */

export interface SessionItem {
  session_id: string;
  preview: string;
  message_count: number;
}

export interface Message {
  type: "human" | "ai";
  content: string;
}

export interface ChatResponse {
  session_id: string;
  generation: string;
  law_domain: string;
}

/* ── Endpoints ── */

/** Start a new chat session */
export async function startSession(): Promise<{ session_id: string; message: string }> {
  const res = await fetch(`${API_BASE}/api/v1/chat/start`, {
    method: "POST",
    headers: headers(),
  });
  if (!res.ok) throw new Error(`Failed to start session: ${res.statusText}`);
  return res.json();
}

/** List all available chat sessions */
export async function getSessions(): Promise<SessionItem[]> {
  const res = await fetch(`${API_BASE}/api/v1/chat/sessions`, {
    headers: headers(),
  });
  if (!res.ok) throw new Error(`Failed to fetch sessions: ${res.statusText}`);
  const data = await res.json();
  return data.sessions;
}

/** Get chat history for a session */
export async function getHistory(sessionId: string): Promise<Message[]> {
  const res = await fetch(`${API_BASE}/api/v1/chat/${sessionId}`, {
    headers: headers(),
  });
  if (!res.ok) throw new Error(`Failed to fetch history: ${res.statusText}`);
  const data = await res.json();
  return data.history;
}

/** Send a message to a session and get the AI response */
export async function sendMessage(sessionId: string, query: string): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/v1/chat/${sessionId}`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ query }),
  });
  if (!res.ok) throw new Error(`Failed to send message: ${res.statusText}`);
  return res.json();
}

/** Delete a chat session */
export async function deleteSession(sessionId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/api/v1/chat/${sessionId}`, {
    method: "DELETE",
    headers: headers(),
  });
  if (!res.ok) throw new Error(`Failed to delete session: ${res.statusText}`);
}
