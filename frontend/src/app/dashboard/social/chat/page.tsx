"use client";

import { useState, useEffect, useRef } from "react";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { DashboardHeader } from "@/components/layout/dashboard-header";
import { SocialNav } from "@/components/layout/social-nav";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import {
  Send,
  Plus,
  MessageSquare,
  BookOpen,
  Loader2,
  Trash2,
  ArrowLeft,
} from "lucide-react";
import { chatService, type ChatSession, type ChatMessage } from "@/lib/services/chat.service";
import { useAuth } from "@/contexts/auth.context";
import { useRouter } from "next/navigation";

export default function ChatPage() {
  const { user } = useAuth();
  const router = useRouter();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [currentSession, setCurrentSession] = useState<number | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [loadingSessions, setLoadingSessions] = useState(true);

  // Load sessions on mount
  useEffect(() => {
    loadSessions();
  }, []);

  // Load messages when session changes
  useEffect(() => {
    if (currentSession) {
      loadMessages(currentSession);
    }
  }, [currentSession]);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const loadSessions = async () => {
    try {
      setLoadingSessions(true);
      const response = await chatService.getSessions();
      if (response.success && response.data) {
        setSessions(response.data.sessions);
        
        // If no current session and sessions exist, select the first one
        if (!currentSession && response.data.sessions.length > 0) {
          setCurrentSession(response.data.sessions[0].id);
        }
      }
    } catch (error) {
      console.error("Failed to load sessions:", error);
    } finally {
      setLoadingSessions(false);
    }
  };

  const loadMessages = async (sessionId: number) => {
    try {
      const response = await chatService.getSession(sessionId);
      if (response.success && response.data) {
        setMessages(response.data.messages);
      }
    } catch (error) {
      console.error("Failed to load messages:", error);
    }
  };

  const createNewSession = async () => {
    try {
      const response = await chatService.createSession();
      if (response.success && response.data) {
        await loadSessions();
        setCurrentSession(response.data.id);
        setMessages([]);
      }
    } catch (error) {
      console.error("Failed to create session:", error);
    }
  };

  const deleteSession = async (sessionId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    
    if (!confirm("Are you sure you want to delete this conversation?")) {
      return;
    }

    try {
      await chatService.deleteSession(sessionId);
      
      // Reload sessions
      await loadSessions();
      
      // If deleted current session, clear it
      if (currentSession === sessionId) {
        setCurrentSession(null);
        setMessages([]);
      }
    } catch (error) {
      console.error("Failed to delete session:", error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || !currentSession || isLoading) return;

    const question = inputMessage.trim();
    setInputMessage("");
    setIsLoading(true);

    // Add user message optimistically
    const userMessage: ChatMessage = {
      id: Date.now(),
      session_id: currentSession,
      role: "user",
      message: question,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await chatService.askTutor(currentSession, question);
      
      if (response.success && response.data) {
        // Add assistant message
        const assistantMessage: ChatMessage = {
          id: response.data.message_id,
          session_id: response.data.session_id,
          role: "assistant",
          message: response.data.answer,
          sources: response.data.sources,
          created_at: new Date().toISOString(),
        };
        
        setMessages((prev) => [...prev, assistantMessage]);
        
        // Reload sessions to update last message
        await loadSessions();
      }
    } catch (error: any) {
      console.error("Failed to send message:", error);
      
      // Show error message
      const errorMessage: ChatMessage = {
        id: Date.now() + 1,
        session_id: currentSession,
        role: "assistant",
        message: "Sorry, I encountered an error. Please try again.",
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <ProtectedRoute>
      <div className="h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex flex-col overflow-hidden">
        <DashboardHeader />
        <SocialNav />

        <div className="flex-1 flex overflow-hidden">
          {/* Sidebar */}
          {isSidebarOpen && (
            <div className="w-80 bg-white border-r flex flex-col">
              <div className="p-4 border-b">
                <Button
                  onClick={() => router.push("/dashboard")}
                  variant="ghost"
                  className="w-full mb-4"
                >
                  <ArrowLeft className="mr-2 h-4 w-4" />
                  Back to Dashboard
                </Button>
                
                <Button onClick={createNewSession} className="w-full">
                  <Plus className="mr-2 h-4 w-4" />
                  New Conversation
                </Button>
              </div>

              <div className="flex-1 overflow-y-auto p-4 space-y-2">
                {loadingSessions ? (
                  <div className="flex items-center justify-center py-8">
                    <Loader2 className="h-6 w-6 animate-spin text-primary" />
                  </div>
                ) : sessions.length === 0 ? (
                  <div className="text-center py-8 text-gray-500 text-sm">
                    No conversations yet.
                    <br />
                    Start a new one!
                  </div>
                ) : (
                  sessions.map((session) => (
                    <div
                      key={session.id}
                      onClick={() => setCurrentSession(session.id)}
                      className={`p-3 rounded-lg cursor-pointer transition-colors group relative ${
                        currentSession === session.id
                          ? "bg-primary text-white"
                          : "hover:bg-gray-100"
                      }`}
                    >
                      <div className="flex items-start">
                        <MessageSquare className="h-4 w-4 mr-2 mt-0.5 flex-shrink-0" />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium truncate">
                            {session.title}
                          </p>
                          {session.last_message && (
                            <p className="text-xs opacity-75 truncate mt-1">
                              {session.last_message}
                            </p>
                          )}
                        </div>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={(e) => deleteSession(session.id, e)}
                          className={`ml-2 opacity-0 group-hover:opacity-100 transition-opacity p-1 h-auto ${
                            currentSession === session.id
                              ? "text-white hover:text-white hover:bg-white/20"
                              : ""
                          }`}
                        >
                          <Trash2 className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          {/* Main Chat Area */}
          <div className="flex-1 flex flex-col">
            {!currentSession ? (
              <div className="flex-1 flex items-center justify-center p-8">
                <div className="text-center max-w-md">
                  <div className="bg-primary/10 p-6 rounded-full inline-block mb-4">
                    <BookOpen className="h-16 w-16 text-primary" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    AI Study Companion
                  </h2>
                  <p className="text-gray-600 mb-6">
                    Welcome! I'm your AI tutor for Social Studies. Ask me anything about
                    History, Geography, Politics, or Economics.
                  </p>
                  <Button onClick={createNewSession} size="lg">
                    <Plus className="mr-2 h-5 w-5" />
                    Start New Conversation
                  </Button>
                </div>
              </div>
            ) : (
              <>
                {/* Chat Header — title + delete */}
                <div className="border-b bg-white px-6 py-3 flex items-center justify-between shadow-sm flex-shrink-0">
                  <div className="flex items-center gap-3">
                    <div className="bg-primary/10 p-1.5 rounded-lg">
                      <MessageSquare className="h-4 w-4 text-primary" />
                    </div>
                    <h2 className="font-semibold text-gray-800 text-sm truncate max-w-[420px]">
                      {sessions.find((s) => s.id === currentSession)?.title ?? "Conversation"}
                    </h2>
                  </div>

                  <Button
                    id="delete-current-conversation-btn"
                    variant="ghost"
                    size="sm"
                    onClick={(e) => deleteSession(currentSession, e)}
                    className="flex items-center gap-1.5 text-red-500 hover:text-red-600 hover:bg-red-50 transition-colors text-xs font-medium"
                    title="Delete this conversation"
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                    Delete chat
                  </Button>
                </div>

                {/* Messages */}

                <div className="flex-1 overflow-y-auto p-6 space-y-4">
                  {messages.length === 0 && (
                    <div className="text-center py-12">
                      <p className="text-gray-500">
                        Start by asking a question about Social Studies!
                      </p>
                    </div>
                  )}

                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${
                        message.role === "user" ? "justify-end" : "justify-start"
                      }`}
                    >
                      <div
                        className={`max-w-3xl rounded-lg p-4 ${
                          message.role === "user"
                            ? "bg-primary text-white"
                            : "bg-white shadow-sm border"
                        }`}
                      >
                        <p className="text-sm whitespace-pre-wrap">{message.message}</p>

                        {message.sources && message.sources.length > 0 && (
                          <div className="mt-3 pt-3 border-t border-gray-200">
                            <p className="text-xs font-semibold mb-2 text-gray-700">
                              Sources:
                            </p>
                            <div className="space-y-1">
                              {message.sources.map((source, idx) => (
                                <div key={idx} className="text-xs text-gray-600">
                                  <span className="font-medium">{source.category}</span> -{" "}
                                  Page {source.page}
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}

                  {isLoading && (
                    <div className="flex justify-start">
                      <div className="bg-white shadow-sm border rounded-lg p-4">
                        <Loader2 className="h-5 w-5 animate-spin text-primary" />
                      </div>
                    </div>
                  )}

                  <div ref={messagesEndRef} />
                </div>

                {/* Input — fixed at bottom, never scrolls */}
                <div className="border-t bg-white p-4 flex-shrink-0">
                  <div className="max-w-4xl mx-auto flex gap-2">
                    <Input
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder="Ask a question about Social Studies..."
                      disabled={isLoading}
                      className="flex-1"
                    />
                    <Button
                      onClick={sendMessage}
                      disabled={!inputMessage.trim() || isLoading}
                      size="icon"
                    >
                      {isLoading ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <Send className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
