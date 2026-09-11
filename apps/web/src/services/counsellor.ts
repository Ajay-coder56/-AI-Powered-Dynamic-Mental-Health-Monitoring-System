import { apiClient } from './api';

export interface CaseResponse {
  id: string;
  patientName: string;
  riskLevel: string;
  riskScore: number;
  trend: string;
  nextSession?: string;
  streak: number;
  status: string;
}

export interface ExplainabilityResult {
  summary: string;
  risk_score: number;
  risk_level: string;
  top_contributing_factors: Array<{
    domain: string;
    score: number;
    contribution_level: string;
    reason: string;
  }>;
  modality_contributions: Array<{
    modality: string;
    score?: number;
    confidence?: number;
    weight?: number;
    availability: string;
    contribution: string;
    reason: string;
  }>;
  missing_modalities: string[];
  conflicting_modalities: boolean;
  temporal_summary?: {
    current_risk: number;
    trend: string;
    slope_per_day?: number;
    persistence: boolean;
    recent_change?: number;
    early_warning_status: string;
    data_quality: string;
    explanation: string;
  };
  reliability: string;
  human_review_note: string;
  limitations: string;
}

export const getCases = async (): Promise<CaseResponse[]> => {
  const response = await apiClient.get('/cases');
  return response.data;
};

export const getCaseExplanation = async (caseId: string): Promise<ExplainabilityResult> => {
  const response = await apiClient.get(`/cases/${caseId}/explanation`);
  return response.data;
};

export interface AlertResponse {
  id: string;
  case_id: string;
  severity: string;
  type: string;
  title: string;
  message: string;
  ai_explanation?: string;
  recommended_actions?: string[];
  created_at: string;
  is_read: boolean;
  is_resolved: boolean;
}

export const getAlerts = async (): Promise<AlertResponse[]> => {
  const response = await apiClient.get('/alerts');
  return response.data;
};

export const acknowledgeAlert = async (alertId: string): Promise<void> => {
  await apiClient.post(`/alerts/${alertId}/acknowledge`);
};

export const resolveAlert = async (alertId: string): Promise<void> => {
  await apiClient.post(`/alerts/${alertId}/resolve`);
};

export const dismissAlert = async (alertId: string): Promise<void> => {
  await apiClient.post(`/alerts/${alertId}/dismiss`);
};

export const addCaseNote = async (caseId: string, content: string): Promise<void> => {
  await apiClient.post(`/cases/${caseId}/notes`, { content });
};
