import { apiClient } from './api';

export interface CheckInPayload {
  mode: string;
  mood: string;
  domain_scores: { domain: string; score: number }[];
  duration_seconds: number;
}

export const checkInsService = {
  async submitCheckIn(userId: string, payload: CheckInPayload) {
    const res = await apiClient.post(`/users/${userId}/check-ins`, payload);
    return res.data;
  },

  async submitVoiceCheckIn(userId: string, audioBlob: Blob, domainScores: any, mood: string, durationSeconds: number) {
    const formData = new FormData();
    formData.append("audio_file", audioBlob, "voice-checkin.webm");
    formData.append("domain_scores", JSON.stringify(domainScores));
    formData.append("mood", mood);
    formData.append("duration_seconds", String(durationSeconds));
    
    const res = await apiClient.post(`/users/${userId}/voice-check-ins`, formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    });
    return res.data;
  },

  async getCheckInHistory(userId: string) {
    const res = await apiClient.get(`/users/${userId}/check-ins`);
    return res.data;
  },
};
