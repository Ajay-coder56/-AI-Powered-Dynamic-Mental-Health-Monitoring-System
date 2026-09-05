export type RiskLevel = "stable" | "moderate" | "high" | "critical";

export interface Case {
  id: string;
  caseNumber: string;
  victimName: string;
  victimAge: number;
  gender: string;
  caseType: string;
  courtName: string;
  assignedCounsellor: string;
  riskScore: number;
  riskLevel: RiskLevel;
  lastCheckIn: string;
  nextCheckIn: string;
  checkInStreak: number;
  totalSessions: number;
  caseStartDate: string;
  hearingDate: string;
  language: string;
  city: string;
  status: "active" | "monitoring" | "resolved";
  trend: "improving" | "stable" | "declining";
  alertCount: number;
}

export interface Alert {
  id: string;
  caseId: string;
  victimName: string;
  caseNumber: string;
  severity: "low" | "moderate" | "high" | "critical";
  type: string;
  message: string;
  triggeredAt: string;
  isRead: boolean;
  isResolved: boolean;
  aiExplanation: string;
}

export interface CheckInSession {
  id: string;
  date: string;
  riskScore: number;
  riskLevel: RiskLevel;
  mode: "voice" | "text";
  duration: string;
  keyFindings: string[];
  aiSummary: string;
}

export interface TrendDataPoint {
  date: string;
  score: number;
  label: string;
}

export const cases: Case[] = [
  {
    id: "c001",
    caseNumber: "DV/MH/2024/0847",
    victimName: "Priya Sharma",
    victimAge: 32,
    gender: "Female",
    caseType: "Domestic Violence",
    courtName: "Family Court, Mumbai",
    assignedCounsellor: "Dr. Meera Iyer",
    riskScore: 78,
    riskLevel: "high",
    lastCheckIn: "2026-09-02",
    nextCheckIn: "2026-09-04",
    checkInStreak: 12,
    totalSessions: 34,
    caseStartDate: "2024-11-15",
    hearingDate: "2026-09-18",
    language: "Hindi",
    city: "Mumbai",
    status: "active",
    trend: "declining",
    alertCount: 3,
  },
  {
    id: "c002",
    caseNumber: "SC/KA/2024/1203",
    victimName: "Kavitha Reddy",
    victimAge: 28,
    gender: "Female",
    caseType: "Sexual Violence",
    courtName: "Sessions Court, Bengaluru",
    assignedCounsellor: "Ms. Anitha Krishnan",
    riskScore: 41,
    riskLevel: "moderate",
    lastCheckIn: "2026-09-03",
    nextCheckIn: "2026-09-05",
    checkInStreak: 28,
    totalSessions: 51,
    caseStartDate: "2024-08-20",
    hearingDate: "2026-09-25",
    language: "Kannada",
    city: "Bengaluru",
    status: "monitoring",
    trend: "improving",
    alertCount: 0,
  },
  {
    id: "c003",
    caseNumber: "DV/TN/2025/0312",
    victimName: "Lakshmi Patel",
    victimAge: 45,
    gender: "Female",
    caseType: "Domestic Violence",
    courtName: "Family Court, Chennai",
    assignedCounsellor: "Dr. Meera Iyer",
    riskScore: 92,
    riskLevel: "critical",
    lastCheckIn: "2026-09-01",
    nextCheckIn: "2026-09-03",
    checkInStreak: 3,
    totalSessions: 18,
    caseStartDate: "2025-02-10",
    hearingDate: "2026-09-10",
    language: "Tamil",
    city: "Chennai",
    status: "active",
    trend: "declining",
    alertCount: 5,
  },
  {
    id: "c004",
    caseNumber: "HC/RJ/2024/0589",
    victimName: "Sunita Devi",
    victimAge: 38,
    gender: "Female",
    caseType: "Harassment",
    courtName: "High Court, Jaipur",
    assignedCounsellor: "Ms. Preethi Nair",
    riskScore: 23,
    riskLevel: "stable",
    lastCheckIn: "2026-09-03",
    nextCheckIn: "2026-09-07",
    checkInStreak: 45,
    totalSessions: 67,
    caseStartDate: "2024-06-01",
    hearingDate: "2026-10-02",
    language: "Hindi",
    city: "Jaipur",
    status: "monitoring",
    trend: "improving",
    alertCount: 0,
  },
  {
    id: "c005",
    caseNumber: "DV/WB/2025/0741",
    victimName: "Anjali Bose",
    victimAge: 26,
    gender: "Female",
    caseType: "Domestic Violence",
    courtName: "Family Court, Kolkata",
    assignedCounsellor: "Ms. Anitha Krishnan",
    riskScore: 65,
    riskLevel: "moderate",
    lastCheckIn: "2026-09-02",
    nextCheckIn: "2026-09-04",
    checkInStreak: 8,
    totalSessions: 22,
    caseStartDate: "2025-04-18",
    hearingDate: "2026-09-22",
    language: "Bengali",
    city: "Kolkata",
    status: "active",
    trend: "stable",
    alertCount: 1,
  },
  {
    id: "c006",
    caseNumber: "SC/UP/2024/1567",
    victimName: "Rekha Gupta",
    victimAge: 34,
    gender: "Female",
    caseType: "Sexual Violence",
    courtName: "Sessions Court, Lucknow",
    assignedCounsellor: "Ms. Preethi Nair",
    riskScore: 55,
    riskLevel: "moderate",
    lastCheckIn: "2026-09-01",
    nextCheckIn: "2026-09-05",
    checkInStreak: 15,
    totalSessions: 39,
    caseStartDate: "2024-10-30",
    hearingDate: "2026-09-30",
    language: "Hindi",
    city: "Lucknow",
    status: "active",
    trend: "stable",
    alertCount: 2,
  },
];

export const alerts: Alert[] = [
  {
    id: "a001",
    caseId: "c003",
    victimName: "Lakshmi Patel",
    caseNumber: "DV/TN/2025/0312",
    severity: "critical",
    type: "Distress Spike",
    message: "Risk score surged from 68 to 92 within 48 hours. Victim reported feelings of hopelessness and disrupted sleep.",
    triggeredAt: "2026-09-03T07:42:00",
    isRead: false,
    isResolved: false,
    aiExplanation: "The AI model detected a significant increase in negative sentiment across voice and text responses, combined with irregular check-in timing and reports of physical symptoms (headaches, insomnia). A court hearing is scheduled in 7 days, which is a known high-stress period. Immediate counsellor contact is recommended.",
  },
  {
    id: "a002",
    caseId: "c001",
    victimName: "Priya Sharma",
    caseNumber: "DV/MH/2024/0847",
    severity: "high",
    type: "Missed Check-in",
    message: "Victim missed scheduled check-in for 2 consecutive days. Previous session indicated elevated anxiety.",
    triggeredAt: "2026-09-02T18:00:00",
    isRead: false,
    isResolved: false,
    aiExplanation: "Two consecutive missed check-ins combined with the victim's trend of declining scores over the past 10 days warrants proactive outreach. The last interaction recorded high anxiety markers related to upcoming court cross-examination.",
  },
  {
    id: "a003",
    caseId: "c005",
    victimName: "Anjali Bose",
    caseNumber: "DV/WB/2025/0741",
    severity: "moderate",
    type: "Trend Decline",
    message: "7-day rolling risk score has increased by 18 points. Victim reports increased social isolation.",
    triggeredAt: "2026-09-03T09:15:00",
    isRead: true,
    isResolved: false,
    aiExplanation: "A gradual but consistent upward trend in risk score over 7 days suggests developing distress. The victim has mentioned reduced contact with support network. Schedule a check-in call within 48 hours.",
  },
  {
    id: "a004",
    caseId: "c006",
    victimName: "Rekha Gupta",
    caseNumber: "SC/UP/2024/1567",
    severity: "moderate",
    type: "Pre-hearing Anxiety",
    message: "Court hearing in 5 days. Risk indicators elevated in pre-hearing window.",
    triggeredAt: "2026-09-03T11:00:00",
    isRead: true,
    isResolved: false,
    aiExplanation: "Historical pattern analysis shows this victim's risk score typically increases 7-10 days before hearings. Current trajectory is consistent with that pattern. Proactive support session recommended before the hearing date.",
  },
  {
    id: "a005",
    caseId: "c002",
    victimName: "Kavitha Reddy",
    caseNumber: "SC/KA/2024/1203",
    severity: "low",
    type: "Routine Reminder",
    message: "Check-in overdue by 6 hours. Victim has strong compliance history.",
    triggeredAt: "2026-09-03T15:30:00",
    isRead: true,
    isResolved: true,
    aiExplanation: "Low-priority reminder. Victim has a 28-day check-in streak and improving trend. Delay is likely logistical. No urgent action needed.",
  },
];

export const priyaTrend: TrendDataPoint[] = [
  { date: "Aug 5", score: 52, label: "Aug 5" },
  { date: "Aug 8", score: 48, label: "Aug 8" },
  { date: "Aug 11", score: 55, label: "Aug 11" },
  { date: "Aug 14", score: 61, label: "Aug 14" },
  { date: "Aug 17", score: 58, label: "Aug 17" },
  { date: "Aug 20", score: 63, label: "Aug 20" },
  { date: "Aug 23", score: 69, label: "Aug 23" },
  { date: "Aug 26", score: 72, label: "Aug 26" },
  { date: "Aug 29", score: 75, label: "Aug 29" },
  { date: "Sep 1", score: 71, label: "Sep 1" },
  { date: "Sep 2", score: 78, label: "Sep 2" },
];

export const mobileUserTrend: TrendDataPoint[] = [
  { date: "Aug 4", score: 62, label: "Aug 4" },
  { date: "Aug 7", score: 58, label: "Aug 7" },
  { date: "Aug 10", score: 53, label: "Aug 10" },
  { date: "Aug 13", score: 55, label: "Aug 13" },
  { date: "Aug 16", score: 47, label: "Aug 16" },
  { date: "Aug 19", score: 44, label: "Aug 19" },
  { date: "Aug 22", score: 40, label: "Aug 22" },
  { date: "Aug 25", score: 38, label: "Aug 25" },
  { date: "Aug 28", score: 41, label: "Aug 28" },
  { date: "Sep 1", score: 36, label: "Sep 1" },
  { date: "Sep 3", score: 38, label: "Sep 3" },
];

export const counsellorSessions: CheckInSession[] = [
  {
    id: "s001",
    date: "2026-09-02",
    riskScore: 78,
    riskLevel: "high",
    mode: "voice",
    duration: "8m 24s",
    keyFindings: ["Reported difficulty sleeping", "Mentioned fear of court appearance", "Low appetite noted"],
    aiSummary: "Victim expressed significant anxiety around upcoming cross-examination. Voice stress markers elevated. Sleep disruption confirmed.",
  },
  {
    id: "s002",
    date: "2026-08-29",
    riskScore: 71,
    riskLevel: "high",
    mode: "text",
    duration: "5m 10s",
    keyFindings: ["Social support network available", "Physical symptoms reported (headache)", "Mentioned legal process confusion"],
    aiSummary: "Moderate distress with physical manifestations. Victim unsure about legal timeline. Psychoeducation on process recommended.",
  },
  {
    id: "s003",
    date: "2026-08-25",
    riskScore: 63,
    riskLevel: "moderate",
    mode: "voice",
    duration: "6m 52s",
    keyFindings: ["Improvement in daily routine", "Family support mentioned positively", "Financial stress ongoing"],
    aiSummary: "Relative stabilization observed. Family support is a protective factor. Financial stress remains a secondary stressor.",
  },
];

export const riskDistribution = [
  { name: "Stable", value: 14, color: "#16A34A" },
  { name: "Moderate", value: 23, color: "#D97706" },
  { name: "High", value: 8, color: "#EA580C" },
  { name: "Critical", value: 3, color: "#E11D48" },
];

export const weeklyCheckIns = [
  { day: "Mon", completed: 42, missed: 6 },
  { day: "Tue", completed: 38, missed: 10 },
  { day: "Wed", completed: 45, missed: 3 },
  { day: "Thu", completed: 40, missed: 8 },
  { day: "Fri", completed: 35, missed: 13 },
  { day: "Sat", completed: 28, missed: 5 },
  { day: "Sun", completed: 22, missed: 4 },
];

export const questions = [
  {
    id: "q1",
    text: "How would you describe your mood today?",
    hint: "Think about how you have been feeling overall",
    options: [
      { label: "Very Sad", emoji: "😔", value: 1 },
      { label: "Sad", emoji: "🙁", value: 2 },
      { label: "Okay", emoji: "😐", value: 3 },
      { label: "Good", emoji: "🙂", value: 4 },
      { label: "Very Good", emoji: "😊", value: 5 },
    ],
  },
  {
    id: "q2",
    text: "How well did you sleep last night?",
    hint: "Think about the quality and amount of sleep",
    options: [
      { label: "Very Poor", emoji: "😫", value: 1 },
      { label: "Poor", emoji: "😴", value: 2 },
      { label: "Fair", emoji: "😑", value: 3 },
      { label: "Good", emoji: "😌", value: 4 },
      { label: "Very Good", emoji: "😃", value: 5 },
    ],
  },
  {
    id: "q3",
    text: "Have you felt safe in your surroundings today?",
    hint: "Your safety is our priority",
    options: [
      { label: "Not Safe", emoji: "😨", value: 1 },
      { label: "Worried", emoji: "😟", value: 2 },
      { label: "Somewhat", emoji: "😐", value: 3 },
      { label: "Mostly Safe", emoji: "😊", value: 4 },
      { label: "Fully Safe", emoji: "🛡️", value: 5 },
    ],
  },
  {
    id: "q4",
    text: "Do you feel supported by your friends or family?",
    hint: "Think about people around you",
    options: [
      { label: "Not at All", emoji: "😞", value: 1 },
      { label: "Very Little", emoji: "😕", value: 2 },
      { label: "Some Support", emoji: "😐", value: 3 },
      { label: "Good Support", emoji: "🤝", value: 4 },
      { label: "Very Supported", emoji: "❤️", value: 5 },
    ],
  },
  {
    id: "q5",
    text: "How anxious or worried do you feel about the legal process?",
    hint: "It is okay to feel this way — we are here to help",
    options: [
      { label: "Very Anxious", emoji: "😰", value: 1 },
      { label: "Quite Worried", emoji: "😟", value: 2 },
      { label: "Somewhat", emoji: "😐", value: 3 },
      { label: "Manageable", emoji: "😌", value: 4 },
      { label: "Not Worried", emoji: "😊", value: 5 },
    ],
  },
];
