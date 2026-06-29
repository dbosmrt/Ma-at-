import { Message } from "../api";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface ChatAreaProps {
  messages: Message[];
  isLoading: boolean;
  onSuggestionClick: (text: string) => void;
  lawDomain: string | null;
}

const SUGGESTIONS = [
  { icon: "⚖️", text: "What are the grounds for divorce under Hindu Marriage Act?" },
  { icon: "📜", text: "Explain the difference between IPC Section 302 and 304" },
  { icon: "🏠", text: "What are a tenant's rights under the Rent Control Act?" },
  { icon: "💼", text: "What legal remedies exist for wrongful termination?" },
];

export default function ChatArea({ messages, isLoading, onSuggestionClick, lawDomain }: ChatAreaProps) {
  const hasMessages = messages.length > 0;

  return (
    <div className="chat-area" id="chat-area">
      {/* Header */}
      <div className="chat-header">
        <span className="chat-header-title">
          {hasMessages ? "Chat with Ma'at" : "New Conversation"}
        </span>
        {lawDomain && lawDomain !== "General" && (
          <span className="chat-header-badge">{lawDomain}</span>
        )}
      </div>

      {/* Messages or Welcome */}
      {hasMessages ? (
        <div className="messages-container" id="messages-container">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message-row ${msg.type}`}>
              {msg.type === "ai" && (
                <div className="message-avatar ai">M</div>
              )}
              <div className={`message-bubble ${msg.type} markdown-body`}>
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {msg.content}
                </ReactMarkdown>
              </div>
              {msg.type === "human" && (
                <div className="message-avatar human">You</div>
              )}
            </div>
          ))}

          {/* Typing indicator */}
          {isLoading && (
            <div className="typing-indicator">
              <div className="message-avatar ai">M</div>
              <div className="typing-dots">
                <div className="typing-dot" />
                <div className="typing-dot" />
                <div className="typing-dot" />
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="welcome-container" id="welcome-container">
          <div className="welcome-icon">M</div>
          <h1 className="welcome-title">Welcome to Ma'at</h1>
          <p className="welcome-subtitle">
            Your AI-powered Indian Legal Assistant. Ask me anything about Indian law — 
            from constitutional rights to criminal procedures.
          </p>
          <div className="welcome-suggestions">
            {SUGGESTIONS.map((s, idx) => (
              <div
                key={idx}
                className="suggestion-card"
                onClick={() => onSuggestionClick(s.text)}
                id={`suggestion-${idx}`}
              >
                <div className="suggestion-icon">{s.icon}</div>
                <div className="suggestion-text">{s.text}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
