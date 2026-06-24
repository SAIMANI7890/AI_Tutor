import { api } from "@/lib/api";
import type {
  APIResponse,
  AuthResponse,
  LoginData,
  RegisterData,
  User,
  UpdateProfileData,
} from "@/lib/types";

export const authService = {
  async register(data: RegisterData): Promise<APIResponse<AuthResponse>> {
    const response = await api.post<APIResponse<AuthResponse>>("/auth/register", data);
    
    if (response.data.success && response.data.data) {
      // Store token and user
      localStorage.setItem("access_token", response.data.data.access_token);
      localStorage.setItem("user", JSON.stringify(response.data.data.user));
    }
    
    return response.data;
  },

  async login(data: LoginData): Promise<APIResponse<AuthResponse>> {
    const response = await api.post<APIResponse<AuthResponse>>("/auth/login", data);
    
    if (response.data.success && response.data.data) {
      // Store token and user
      localStorage.setItem("access_token", response.data.data.access_token);
      localStorage.setItem("user", JSON.stringify(response.data.data.user));
    }
    
    return response.data;
  },

  async getCurrentUser(): Promise<APIResponse<User>> {
    const response = await api.get<APIResponse<User>>("/auth/me");
    
    if (response.data.success && response.data.data) {
      localStorage.setItem("user", JSON.stringify(response.data.data));
    }
    
    return response.data;
  },

  async updateProfile(data: UpdateProfileData): Promise<APIResponse<User>> {
    const response = await api.put<APIResponse<User>>("/auth/me", data);
    
    if (response.data.success && response.data.data) {
      localStorage.setItem("user", JSON.stringify(response.data.data));
    }
    
    return response.data;
  },

  logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
  },

  getStoredUser(): User | null {
    const userStr = localStorage.getItem("user");
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch {
        return null;
      }
    }
    return null;
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem("access_token");
  },
};
