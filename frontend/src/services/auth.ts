import { apiClient } from '../api/client';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface UserProfile {
  email: string;
  is_superuser: boolean;
  subnet_access: string;
}

class AuthService {
  private static TOKEN_KEY = 'token';

  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await apiClient.post<AuthResponse>('/api/v1/auth/login', formData);
    const { access_token } = response.data;
    
    localStorage.setItem(AuthService.TOKEN_KEY, access_token);
    return response.data;
  }

  async getCurrentUser(): Promise<UserProfile> {
    const response = await apiClient.get<UserProfile>('/api/v1/auth/me');
    return response.data;
  }

  getToken(): string | null {
    return localStorage.getItem(AuthService.TOKEN_KEY);
  }

  logout(): void {
    localStorage.removeItem(AuthService.TOKEN_KEY);
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }
}

export const authService = new AuthService(); 