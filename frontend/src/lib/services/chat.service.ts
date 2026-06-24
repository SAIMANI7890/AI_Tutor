import { api } from "@/lib/api";
import type { APIResponse } from "@/lib/types";

export interface ChatSession {
  id: number;
  user_id: number;
  title: string;
  created_at: string;
  updated_at: string;
  message_count?: number;
  last_message?: string;
}

export interface SourceInfo {
  document: string;
  page: number;
  category: string;
}

export interface ChatMessage {
  id: number;
  session_id: number;
  role: "user" | "assistant";
  message: string;
  sources?: SourceInfo[];
  created_at: string;
}

export interface ChatSessionDetail {
  id: number;
  user_id: number;
  title: string;
  created_at: string;
  updated_at: string;
  messages: ChatMessage[];
}

export interface TutorChatResponse {
  answer: string;
  sources: SourceInfo[];
  message_id: number;
  session_id: number;
}

export const chatService = {
  async createSession(title: string = "New Conversation"): Promise<APIResponse<ChatSession>> {
    const response = await api.post<APIResponse<ChatSession>>("/chat/session", { title });
    return response.data;
  },

  async getSessions(): Promise<APIResponse<{ sessions: ChatSession[] }>> {
    const response = await api.get<APIResponse<{ sessions: ChatSession[] }>>("/chat/sessions");
    return response.data;
  },

  async getSession(sessionId: number): Promise<APIResponse<ChatSessionDetail>> {
    const response = await api.get<APIResponse<ChatSessionDetail>>(`/chat/session/${sessionId}`);
    return response.data;
  },

  async deleteSession(sessionId: number): Promise<APIResponse> {
    const response = await api.delete<APIResponse>(`/chat/session/${sessionId}`);
    return response.data;
  },

  async updateSessionTitle(sessionId: number, title: string): Promise<APIResponse<ChatSession>> {
    const response = await api.put<APIResponse<ChatSession>>(
      `/chat/session/${sessionId}/title`,
      { title }
    );
    return response.data;
  },

  async askTutor(sessionId: number, question: string): Promise<APIResponse<TutorChatResponse>> {
    const response = await api.post<APIResponse<TutorChatResponse>>("/tutor/chat", {
      session_id: sessionId,
      question,
    });
    return response.data;
  },

  async checkTutorHealth(): Promise<APIResponse> {
    const response = await api.get<APIResponse>("/tutor/health");
    return response.data;
  },
};
