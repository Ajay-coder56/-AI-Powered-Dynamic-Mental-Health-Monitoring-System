import React, { useState } from "react";
import {
  Card,
  Button,
  RiskBadge,
  RiskGauge,
  TrendChip,
  ProgressBar,
  Avatar,
  SectionHeader,
  Modal,
  Divider,
} from "../../components/ds";
import { cases, priyaTrend, counsellorSessions } from "../../data/sampleData";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  ReferenceLine,
} from "recharts";

interface CaseDetailPageProps {
  caseId: string;
  onBack: () => void;
}

export default function CaseDetailPage({ caseId, onBack }: CaseDetailPageProps) {
  const c = cases.find((x) => x.id === caseId) ?? cases[0];
  const [showAI, setShowAI] = useState(false);
  const [showSchedule, setShowSchedule] = useState(false);
  const [activeTab, setActiveTab] = useState<"overview" | "history" | "ai">("overview");

  return (
    <div className="flex flex-col gap-6">
      {/* Back + title */}
      <div className="flex items-center gap-3">
        <button
          onClick={onBack}
          className="text-sm text-navy-700 font-semibold hover:underline flex items-center gap-1"
        >
          ← Cases
        </button>
        <span className="text-slate-300">/</span>
        <span className="text-sm text-slate-500 font-mono-data">BEN-{c.id.split('-')[2]}</span>
      </div>

      {/* Case header card */}
      <Card padding="lg">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center text-lg font-bold text-slate-500 shrink-0">
              {c.id.split('-')[2]?.slice(0, 2) || '00'}
            </div>
            <div>
              <h2 className="text-xl font-bold font-display text-navy-900">Case ID: BEN-{c.id.split('-')[2]}</h2>
              <p className="text-sm text-slate-500 mt-0.5">
                Anonymized Beneficiary · {c.city} · {c.language}
              </p>
              <div className="flex flex-wrap items-center gap-2 mt-2">
                <RiskBadge level={c.riskLevel} size="md" />
                <TrendChip trend={c.trend} />
                <span className="text-xs bg-slate-100 text-slate-600 px-2.5 py-1 rounded-full font-semibold">
                  {c.caseType}
                </span>
                {c.alertCount > 0 && (
                  <span className="text-xs bg-critical-100 text-critical-700 font-bold px-2.5 py-1 rounded-full">
                    {c.alertCount} active alerts
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Score and Actions */}
          <div className="flex items-center gap-4">
            <RiskGauge score={c.riskScore} size={100} label="Risk Score" />
            <div className="flex flex-col gap-2 min-w-[160px]">
              <Button variant="primary" size="sm" onClick={() => setShowSchedule(true)}>
                📅 Schedule counselling
              </Button>
              <Button variant="secondary" size="sm">
                📞 Contact beneficiary
              </Button>
              <Button variant="outline" size="sm">
                ➕ Create intervention
              </Button>
              <Button variant="outline" size="sm">
                📝 Add note
              </Button>
              <button className="px-3 py-1.5 text-xs font-semibold rounded-lg transition-smooth border border-critical-200 text-critical-700 bg-white hover:bg-critical-50">
                ⚠️ Escalate case
              </button>
            </div>
          </div>
        </div>

        <Divider className="my-4" />

        {/* Case meta grid */}
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
          {[
            { label: "Case Number", value: c.caseNumber, mono: true },
            { label: "Court", value: c.courtName },
            { label: "Next Hearing", value: c.hearingDate, urgent: true },
            { label: "Case Started", value: c.caseStartDate },
            { label: "Counsellor", value: c.assignedCounsellor },
            { label: "Total Sessions", value: `${c.totalSessions}` },
            { label: "Check-in Streak", value: `${c.checkInStreak} days 🔥` },
            { label: "Status", value: c.status.charAt(0).toUpperCase() + c.status.slice(1) },
          ].map(({ label, value, mono, urgent }) => (
            <div key={label}>
              <p className="text-xs text-slate-400 font-semibold uppercase tracking-wider mb-0.5">{label}</p>
              <p className={`text-sm font-semibold ${mono ? "font-mono-data" : "font-display"} ${urgent ? "text-risk-700" : "text-navy-900"}`}>
                {value}
              </p>
            </div>
          ))}
        </div>
      </Card>

      {/* Tabs */}
      <div className="flex gap-1 bg-slate-100 p-1 rounded-xl w-fit">
        {(["overview", "check-ins", "interventions"] as const).map((t) => (
          <button
            key={t}
            onClick={() => setActiveTab(t as any)}
            className={`px-4 py-2 rounded-lg text-sm font-semibold font-display transition-smooth capitalize ${
              activeTab === t ? "bg-white shadow-sm text-navy-900" : "text-slate-500 hover:text-slate-700"
            }`}
          >
            {t === "check-ins" ? "Check-ins & Voice" : t === "interventions" ? "Alerts & Interventions" : t}
          </button>
        ))}
      </div>

      {activeTab === "overview" && (
        <div className="flex flex-col gap-6">
          <div className="grid grid-cols-1 gap-6 xl:grid-cols-3">
            {/* Trend chart */}
            <div className="xl:col-span-2">
              <Card padding="lg">
                <SectionHeader title="Risk Score Trend" subtitle="Last 30 days · Lower = better wellbeing" />
                <ResponsiveContainer width="100%" height={240}>
                  <LineChart data={priyaTrend} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
                    <XAxis dataKey="label" tick={{ fontSize: 11, fill: "#94A3B8" }} tickLine={false} axisLine={false} />
                    <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: "#94A3B8" }} tickLine={false} axisLine={false} />
                    <ReferenceLine y={80} stroke="#E11D48" strokeDasharray="4 4" strokeOpacity={0.5}
                      label={{ value: "Critical", position: "insideTopRight", fontSize: 10, fill: "#E11D48" }} />
                    <ReferenceLine y={60} stroke="#EA580C" strokeDasharray="4 4" strokeOpacity={0.5}
                      label={{ value: "High", position: "insideTopRight", fontSize: 10, fill: "#EA580C" }} />
                    <ReferenceLine y={40} stroke="#D97706" strokeDasharray="4 4" strokeOpacity={0.4}
                      label={{ value: "Mod", position: "insideTopRight", fontSize: 10, fill: "#D97706" }} />
                    <Tooltip
                      contentStyle={{ fontSize: 12, borderRadius: 10, border: "1px solid #E2E8F0", boxShadow: "0 4px 12px rgba(0,0,0,0.08)" }}
                      formatter={(v) => [`${v ?? ""}/100`, "Risk Score"]}
                    />
                    <Line type="monotone" dataKey="score" stroke="#1E3A8A" strokeWidth={2.5}
                      dot={{ r: 3, fill: "#1E3A8A", strokeWidth: 0 }}
                      activeDot={{ r: 5, fill: "#1E3A8A" }} />
                  </LineChart>
                </ResponsiveContainer>
                <p className="text-xs text-slate-400 mt-2">
                  ⚠️ This score is a decision-support indicator only and does not constitute a clinical diagnosis.
                </p>
              </Card>
            </div>

            {/* Domain breakdown */}
            <div className="flex flex-col gap-4">
              <Card padding="lg">
                <SectionHeader title="Domain Scores" subtitle="From latest check-in" />
                <div className="space-y-4">
                  {[
                    { label: "Mood & Emotions", score: 74 },
                    { label: "Sleep Quality", score: 68 },
                    { label: "Safety", score: 55 },
                    { label: "Social Support", score: 48 },
                    { label: "Legal Anxiety", score: 82 },
                  ].map(({ label, score }) => (
                    <div key={label}>
                      <div className="flex justify-between mb-1">
                        <span className="text-xs text-slate-600">{label}</span>
                        <span className="text-xs font-bold font-display text-slate-700">{score}</span>
                      </div>
                      <ProgressBar value={score} size="sm" />
                    </div>
                  ))}
                </div>
              </Card>

              <Card padding="lg" className="border-slate-200">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-lg">🤖</span>
                  <p className="text-sm font-bold font-display text-navy-900">Factors contributing to current risk</p>
                </div>
                <p className="text-xs text-slate-500 mb-5 leading-relaxed">
                  AI-generated decision support — counsellor review required.
                </p>
                
                <div className="space-y-4">
                  {[
                    { title: "Voice stress indicators", value: 18, color: "#E11D48", width: "90%" },
                    { title: "Negative sentiment trend", value: 14, color: "#EA580C", width: "70%" },
                    { title: "Reduced sleep", value: 11, color: "#EA580C", width: "55%" },
                    { title: "Upcoming legal milestone", value: 9, color: "#D97706", width: "45%" },
                    { title: "Reduced check-in frequency", value: 6, color: "#D97706", width: "30%" },
                    { title: "Consistent family support", value: -8, color: "#10B981", width: "40%" },
                  ].map((f, i) => (
                    <div key={i}>
                      <div className="flex items-end justify-between mb-1.5">
                        <span className="text-xs font-semibold text-navy-800">{f.title}</span>
                        <span className="text-xs font-bold font-mono-data" style={{ color: f.color }}>
                          {f.value > 0 ? '+' : ''}{f.value}
                        </span>
                      </div>
                      <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                        <div className="h-full rounded-full transition-all duration-1000" style={{ backgroundColor: f.color, width: f.width }} />
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          </div>

          {/* Legal Case Timeline component */}
          <Card padding="lg">
            <SectionHeader title="⚖️ Legal Case Timeline" subtitle="Visualizing how legal case-management data intersects with mental health markers" />
            <div className="mt-4">
              <div className="space-y-0 relative max-w-4xl">
                <div className="absolute left-6 top-6 bottom-6 w-0.5 bg-slate-200" />
                
                {[
                  { type: 'legal', date: 'Aug 1, 2026', title: 'Case registered', desc: 'Initial filing for protection order.' },
                  { type: 'legal', date: 'Aug 15, 2026', title: 'Hearing scheduled', desc: 'Court date set for September 10, 2026.' },
                  { type: 'legal', date: 'Upcoming: Sep 10', title: 'Upcoming hearing', desc: 'Cross-examination expected.', highlight: true },
                  { type: 'health', date: 'Sep 1 - Sep 3', title: 'Risk increased', desc: 'Risk score surged from 58 to 82 as hearing approaches.' },
                  { type: 'alert', date: 'Sep 3, 2026', title: 'AI generated alert', desc: 'High stress indicators flagged in voice journal.' },
                  { type: 'intervention', date: 'Sep 4, 2026', title: 'Counsellor intervention', desc: 'Emergency outreach completed. Pre-hearing coping strategies discussed.' },
                  { type: 'legal', date: 'Pending', title: 'Legal decision', desc: 'Awaiting court verdict.', future: true },
                  { type: 'legal', date: 'Pending', title: 'Follow-up', desc: 'Post-decision safety protocol.', future: true },
                ].map((ev, i) => (
                  <div key={i} className="relative flex items-start gap-6 pb-6 group">
                    <div className="relative z-10 w-12 h-12 rounded-full border-4 border-white flex items-center justify-center shrink-0 shadow-sm" style={{
                      backgroundColor: ev.type === 'alert' ? '#FEF2F2' : ev.type === 'health' ? '#FFFBEB' : ev.type === 'intervention' ? '#F0FDF4' : ev.future ? '#F8FAFC' : '#F1F5F9'
                    }}>
                      <span className="text-xl">
                        {ev.type === 'legal' ? '⚖️' : ev.type === 'health' ? '📈' : ev.type === 'alert' ? '🤖' : '📞'}
                      </span>
                    </div>
                    
                    <div className={`flex-1 p-4 rounded-xl border ${
                      ev.type === 'alert' ? 'border-critical-200 bg-critical-50' : 
                      ev.type === 'health' ? 'border-orange-200 bg-orange-50' : 
                      ev.type === 'intervention' ? 'border-safe-200 bg-safe-50' : 
                      ev.highlight ? 'border-navy-300 bg-navy-50 shadow-sm' :
                      ev.future ? 'border-slate-100 bg-slate-50 opacity-60' : 'border-slate-200 bg-white hover:border-slate-300'
                    } transition-colors`}>
                      <div className="flex flex-wrap items-center justify-between gap-2 mb-1">
                        <p className={`text-sm font-bold font-display ${
                          ev.type === 'alert' ? 'text-critical-700' : 
                          ev.type === 'intervention' ? 'text-safe-700' : 
                          ev.type === 'health' ? 'text-orange-800' : 'text-navy-900'
                        }`}>
                          {ev.title}
                        </p>
                        <span className="text-xs font-bold text-slate-400 bg-white/60 px-2 py-0.5 rounded uppercase tracking-wider">{ev.date}</span>
                      </div>
                      <p className={`text-xs ${ev.future ? 'text-slate-400' : 'text-slate-600'} leading-relaxed`}>{ev.desc}</p>
                      
                      {ev.type === 'legal' && (
                        <p className="text-[10px] uppercase tracking-wider font-semibold text-slate-400 mt-2 border-t border-black/5 pt-1 w-fit">
                          Case-management data
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        </div>
      )}

      {activeTab === "check-ins" && (
        <div className="space-y-4">
          <Card padding="lg" className="border-navy-100 bg-navy-50/50">
            <SectionHeader title="🎙️ Voice Analysis Trend" subtitle="Emotional markers detected across recent audio check-ins" />
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-4 mt-2">
              <div className="bg-white p-3 rounded-xl border border-slate-100">
                <p className="text-xs text-slate-500 font-semibold mb-1">Speech Rate</p>
                <p className="text-sm font-bold text-navy-900">Elevated (140 wpm)</p>
                <p className="text-xs text-risk-600 mt-1">↑ 12% vs baseline</p>
              </div>
              <div className="bg-white p-3 rounded-xl border border-slate-100">
                <p className="text-xs text-slate-500 font-semibold mb-1">Vocal Tremor</p>
                <p className="text-sm font-bold text-navy-900">Detected</p>
                <p className="text-xs text-risk-600 mt-1">Moderate intensity</p>
              </div>
              <div className="bg-white p-3 rounded-xl border border-slate-100">
                <p className="text-xs text-slate-500 font-semibold mb-1">Pitch Variance</p>
                <p className="text-sm font-bold text-navy-900">Reduced</p>
                <p className="text-xs text-slate-400 mt-1">Suggests fatigue</p>
              </div>
              <div className="bg-white p-3 rounded-xl border border-slate-100">
                <p className="text-xs text-slate-500 font-semibold mb-1">Overall Sentiment</p>
                <p className="text-sm font-bold text-navy-900">Negative</p>
                <p className="text-xs text-slate-400 mt-1">Consistent 3 days</p>
              </div>
            </div>
          </Card>

          <SectionHeader title="Recent Check-ins" subtitle="Chronological history of text and voice interactions" className="mt-6 mb-2" />
          
          {counsellorSessions.map((s) => (
            <Card key={s.id} padding="lg">
              <div className="flex items-start justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-xl ${s.mode === "voice" ? "bg-navy-50" : "bg-slate-50"}`}>
                    {s.mode === "voice" ? "🎙️" : "📝"}
                  </div>
                  <div>
                    <p className="text-sm font-bold font-display text-navy-900">
                      {new Date(s.date).toLocaleDateString("en-IN", { weekday: "long", day: "2-digit", month: "long", year: "numeric" })}
                    </p>
                    <p className="text-xs text-slate-500 capitalize">{s.mode} check-in · {s.duration}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 shrink-0">
                  <div className="text-right">
                    <p className="text-xl font-bold font-display text-navy-900">{s.riskScore}</p>
                    <RiskBadge level={s.riskLevel} size="sm" />
                  </div>
                </div>
              </div>

              <Divider className="my-3" />

              <div className="grid gap-3 sm:grid-cols-2">
                <div>
                  <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Key Findings</p>
                  <ul className="space-y-1">
                    {s.keyFindings.map((f, i) => (
                      <li key={i} className="text-xs text-slate-600 flex items-start gap-1.5">
                        <span className="w-1 h-1 rounded-full bg-navy-400 mt-1.5 shrink-0" />
                        {f}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">AI Summary</p>
                  <p className="text-xs text-slate-600 leading-relaxed">{s.aiSummary}</p>
                  <p className="text-xs text-slate-400 mt-1">Decision-support indicator only.</p>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {activeTab === "interventions" && (
        <div className="flex flex-col gap-6">
          {/* Quick Actions */}
          <Card padding="lg">
            <SectionHeader title="Create Intervention" subtitle="Initiate a new action for this beneficiary" />
            <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-3 mt-4">
              {[
                { icon: "📞", label: "Contact beneficiary" },
                { icon: "📅", label: "Schedule counselling" },
                { icon: "🏥", label: "Refer to support" },
                { icon: "⚖️", label: "Request legal aid" },
                { icon: "⚠️", label: "Escalate to authority" },
                { icon: "📝", label: "Record intervention" },
              ].map((a, i) => (
                <button key={i} className="flex flex-col items-center justify-center p-4 rounded-xl border border-slate-200 hover:border-navy-400 hover:bg-navy-50 transition-smooth text-center gap-2">
                  <span className="text-2xl">{a.icon}</span>
                  <span className="text-[11px] font-bold text-navy-900 leading-tight uppercase tracking-wider">{a.label}</span>
                </button>
              ))}
            </div>
          </Card>

          <div className="grid gap-6 xl:grid-cols-2">
            {/* Active Interventions */}
            <Card padding="lg">
              <SectionHeader title="Active Interventions" subtitle="Currently pending or in progress" />
              <div className="space-y-4 mt-4">
                {[
                  { type: "Refer to mental-health support", priority: "High", assigned: "Dr. Meera Iyer", date: "Sep 3, 2026", status: "In progress", notes: "Referral sent to District Hospital psychiatry wing. Awaiting appointment confirmation." },
                  { type: "Request legal aid", priority: "Moderate", assigned: "Legal Team A", date: "Sep 2, 2026", status: "Pending", notes: "Requested pro-bono consultation for upcoming hearing." },
                ].map((inv, i) => (
                  <div key={i} className="p-4 rounded-xl border border-slate-200 bg-slate-50">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-bold font-display text-navy-900">{inv.type}</span>
                      <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded ${
                        inv.status === 'Pending' ? 'bg-orange-100 text-orange-700' : 'bg-navy-100 text-navy-700'
                      }`}>{inv.status}</span>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-2 mb-3">
                      <div>
                        <span className="text-[10px] uppercase tracking-wider text-slate-400 font-semibold block">Priority</span>
                        <span className={`text-xs font-bold ${inv.priority === 'High' ? 'text-risk-600' : 'text-orange-600'}`}>{inv.priority}</span>
                      </div>
                      <div>
                        <span className="text-[10px] uppercase tracking-wider text-slate-400 font-semibold block">Date</span>
                        <span className="text-xs font-bold text-slate-700">{inv.date}</span>
                      </div>
                      <div className="col-span-2">
                        <span className="text-[10px] uppercase tracking-wider text-slate-400 font-semibold block">Assigned to</span>
                        <span className="text-xs font-bold text-slate-700">{inv.assigned}</span>
                      </div>
                    </div>
                    
                    <div className="text-xs text-slate-600 bg-white p-2.5 rounded-lg border border-slate-100">
                      <span className="font-semibold text-slate-800">Notes: </span>{inv.notes}
                    </div>
                  </div>
                ))}
              </div>
            </Card>

            {/* Intervention History Timeline */}
            <Card padding="lg">
              <SectionHeader title="Intervention History" subtitle="Completed actions timeline" />
              <div className="space-y-0 relative mt-4">
                <div className="absolute left-[11px] top-2 bottom-6 w-0.5 bg-slate-200" />
                
                {[
                  { type: "Contact beneficiary", priority: "High", assigned: "Dr. Meera Iyer", date: "Sep 1, 2026", status: "Completed", notes: "Emergency call completed. De-escalated panic attack regarding upcoming trial." },
                  { type: "Schedule counselling", priority: "Moderate", assigned: "Dr. Meera Iyer", date: "Aug 25, 2026", status: "Completed", notes: "Completed weekly 45-minute CBT session." },
                  { type: "Record intervention", priority: "Information", assigned: "System", date: "Aug 24, 2026", status: "Completed", notes: "Automated check-in reminder SMS delivered." }
                ].map((inv, idx) => (
                  <div key={idx} className="flex gap-4 relative pb-6 group">
                    <div className="w-6 h-6 rounded-full bg-slate-100 border-2 border-white shrink-0 mt-0.5 relative z-10 flex items-center justify-center shadow-sm">
                      <span className="w-2 h-2 rounded-full bg-safe-500" />
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-1">
                        <p className="text-sm font-bold font-display text-navy-900">{inv.type}</p>
                        <span className="text-[10px] font-bold bg-safe-100 text-safe-700 px-2 py-0.5 rounded uppercase tracking-wider">{inv.status}</span>
                      </div>
                      
                      <div className="flex flex-wrap items-center gap-x-4 gap-y-1 mt-1 mb-2">
                        <span className="text-xs text-slate-500"><span className="font-semibold">Priority:</span> {inv.priority}</span>
                        <span className="text-xs text-slate-500"><span className="font-semibold">Assigned:</span> {inv.assigned}</span>
                        <span className="text-xs text-slate-500"><span className="font-semibold">Date:</span> {inv.date}</span>
                      </div>
                      
                      <p className="text-xs text-slate-600 leading-relaxed bg-slate-50 p-2.5 rounded-xl border border-slate-100">{inv.notes}</p>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        </div>
      )}

      {/* AI Modal */}
      <Modal open={showAI} onClose={() => setShowAI(false)} title="🤖 AI Risk Explanation" maxWidth="max-w-xl">
        <div className="space-y-4">
          <div className="flex items-center gap-3 p-3 bg-navy-50 rounded-xl">
            <RiskGauge score={c.riskScore} size={64} />
            <div>
              <p className="text-lg font-bold font-display text-navy-900">Score: {c.riskScore}/100</p>
              <RiskBadge level={c.riskLevel} />
            </div>
          </div>
          <p className="text-sm text-slate-700 leading-relaxed">
            {counsellorSessions[0].aiSummary}
          </p>
          <p className="text-xs text-slate-400 border-t border-slate-100 pt-3">
            ⚠️ This is an AI-generated decision-support indicator. It must not be used as a substitute for professional clinical assessment.
          </p>
          <Button variant="primary" fullWidth onClick={() => setShowAI(false)}>Close</Button>
        </div>
      </Modal>

      {/* Schedule Modal */}
      <Modal open={showSchedule} onClose={() => setShowSchedule(false)} title="Schedule Session">
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            {["Today, 2:00 PM", "Today, 4:00 PM", "Fri Sep 6, 10:00 AM", "Fri Sep 6, 2:00 PM", "Mon Sep 9, 11:00 AM", "Mon Sep 9, 3:00 PM"].map((slot) => (
              <button key={slot} className="p-3 text-sm border border-slate-200 rounded-xl hover:border-navy-400 hover:bg-navy-50 text-left font-semibold text-navy-900 transition-smooth">
                {slot}
              </button>
            ))}
          </div>
          <div className="flex gap-2">
            <Button variant="primary" size="md" className="flex-1">Confirm Session</Button>
            <Button variant="outline" size="md" onClick={() => setShowSchedule(false)}>Cancel</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
