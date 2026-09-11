import { apiClient } from './api';

export const authService = {
  async login(email: string, password: string) {
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);
    
    // FastAPI OAuth2PasswordRequestForm expects form-urlencoded
    const res = await apiClient.post('/auth/login', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    
    // Store JWT so the axios interceptor can attach it to subsequent requests
    if (res.data?.access_token) {
      localStorage.setItem('mindsafe_token', res.data.access_token);
    }
    
    return res.data;
  },

  async getMe() {
    const res = await apiClient.get('/auth/me');
    return res.data;
  },
};
