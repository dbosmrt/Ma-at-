import { SessionItem } from "../api";

interface SidebarProps {
  sessions: SessionItem[];
  activeSessionId: string | null;
  sidebarOpen: boolean;
  onNewChat: () => void;
  onSelectSession: (sessionId: string) => void;
  onDeleteSession: (sessionId: string) => void;
  onToggleSidebar: () => void;
}

export default function Sidebar({
  sessions,
  activeSessionId,
  sidebarOpen,
  onNewChat,
  onSelectSession,
  onDeleteSession,
  onToggleSidebar,
}: SidebarProps) {
  return (
    <>
      {/* Mobile hamburger toggle */}
      <button
        className="sidebar-toggle"
        onClick={onToggleSidebar}
        id="sidebar-toggle"
        aria-label="Toggle sidebar"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
          <line x1="3" y1="6" x2="21" y2="6" />
          <line x1="3" y1="12" x2="21" y2="12" />
          <line x1="3" y1="18" x2="21" y2="18" />
        </svg>
      </button>

      <aside className={`sidebar ${sidebarOpen ? "open" : ""}`} id="sidebar">
        <div className="sidebar-header">
          {/* Brand */}
          <div className="sidebar-brand">
            <div className="sidebar-brand-icon">M</div>
            <span className="sidebar-brand-text">Ma'at</span>
          </div>

          {/* New Chat button */}
          <button className="new-chat-btn" onClick={onNewChat} id="new-chat-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
            New Chat
          </button>
        </div>

        {/* Session list */}
        <div className="session-list" id="session-list">
          {sessions.length > 0 ? (
            <>
              <div className="session-list-label">Recent Chats</div>
              {sessions.map((session) => (
                <div
                  key={session.session_id}
                  className={`session-item ${activeSessionId === session.session_id ? "active" : ""}`}
                  onClick={() => onSelectSession(session.session_id)}
                  id={`session-${session.session_id}`}
                >
                  <div className="session-item-content">
                    <div className="session-item-preview">{session.preview}</div>
                    <div className="session-item-meta">
                      {session.message_count} message{session.message_count !== 1 ? "s" : ""}
                    </div>
                  </div>
                  <button
                    className="session-delete-btn"
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteSession(session.session_id);
                    }}
                    aria-label={`Delete session ${session.session_id}`}
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                      <polyline points="3 6 5 6 21 6" />
                      <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
                    </svg>
                  </button>
                </div>
              ))}
            </>
          ) : (
            <div className="sessions-empty">
              <div className="sessions-empty-icon">💬</div>
              <div className="sessions-empty-text">
                No conversations yet.<br />Start a new chat to begin.
              </div>
            </div>
          )}
        </div>

        <div className="sidebar-footer">
          Ma'at Legal AI · v1.0
        </div>
      </aside>
    </>
  );
}
