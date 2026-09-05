import { apiClient } from './api';

export const usersService = {
  async getUser(userId: string) {
    const res = await apiClient.get(`/users/${userId}`);
    return res.data;
  },

  async submitConsent(userId: string, consentType: string = 'data_collection_and_assessment') {
    const res = await apiClient.post(`/users/${userId}/consent`, {
      consent_type: consentType,
      user_agent: navigator.userAgent,
    });
    return res.data;
  },
};
