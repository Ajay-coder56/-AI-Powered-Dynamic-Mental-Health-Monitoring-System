import React, { useState, useEffect } from "react";
import { Card, RiskBadge, ProgressBar, SectionHeader } from "../../components/ds";
import { mobileUserTrend } from "../../data/sampleData";
import { checkInsService } from "../../services/checkIns";
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

interface TrendsScreenProps {
  userId: string;
}

export default function TrendsScreen({ userId }: TrendsScreenProps) {
  const [period, setPeriod] = useState<"7d" | "30d">("30d");
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setLoading(true);
        const data = await checkInsService.getCheckInHistory(userId);
        setHistory(data);
      } catch (err) {
        console.error(err);
        setError("Failed to load past check-ins.");
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, [userId]);

  const data = period === "7d" ? mobileUserTrend.slice(-7) : mobileUserTrend;

  const latest = data[data.length - 1]?.score ?? 0;
  const earliest = data[0]?.score ?? 0;
  const change = earliest - latest;

  return (
    <div className="flex flex-col gap-4 pb-6">
      {/* Header */}
      <div className="px-5 pt-5">
        <h1 className="text-2xl font-bold font-display text-navy-900">My Progress</h1>
        <p className="text-sm text-slate-500 mt-1">Track your wellbeing over time</p>
      </div>

      {/* Summary cards */}
      <div className="px-5 grid grid-cols-3 gap-3">
        <Card padding="sm" className="text-center bg-navy-50 border-0">
          <p className="text-xl font-bold font-display text-navy-900">{latest}</p>
          <p className="text-xs text-slate-500 mt-0.5">Today</p>
        </Card>
        <Card padding="sm" className="text-center bg-safe-50 border-0">
          <p className="text-xl font-bold font-display text-safe-700">+{change}</p>
          <p className="text-xs text-slate-500 mt-0.5">Improved</p>
        </Card>
        <Card padding="sm" className="text-center bg-slate-50 border-0">
          <p className="text-xl font-bold font-display text-slate-700">34</p>
          <p className="text-xs text-slate-500 mt-0.5">Sessions</p>
        </Card>
      </div>

      {/* Trend chart */}
      <div className="px-5">
        <Card padding="md">
          <div className="flex items-center justify-between mb-3">
            <SectionHeader title="Wellbeing Score Trend (Mock Data)" />
            <div className="flex gap-1">
              {(["7d", "30d"] as const).map((p) => (
                <button
                  key={p}
                  onClick={() => setPeriod(p)}
                  className={`text-xs px-2.5 py-1 rounded-lg font-semibold transition-smooth ${
                    period === p ? "bg-navy-700 text-white" : "bg-slate-100 text-slate-600"
                  }`}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>
          <ResponsiveContainer width="100%" height={180}>
            <LineChart data={data} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
              <XAxis dataKey="label" tick={{ fontSize: 10, fill: "#94A3B8" }} tickLine={false} axisLine={false} interval="preserveStartEnd" />
              <YAxis domain={[0, 100]} tick={{ fontSize: 10, fill: "#94A3B8" }} tickLine={false} axisLine={false} />
              <ReferenceLine y={60} stroke="#EA580C" strokeDasharray="3 3" strokeOpacity={0.4} label={{ value: "High", position: "insideTopRight", fontSize: 9, fill: "#EA580C" }} />
              <ReferenceLine y={40} stroke="#D97706" strokeDasharray="3 3" strokeOpacity={0.4} label={{ value: "Mod", position: "insideTopRight", fontSize: 9, fill: "#D97706" }} />
              <Tooltip
                contentStyle={{ fontSize: 12, borderRadius: 10, border: "1px solid #E2E8F0", boxShadow: "0 4px 12px rgba(0,0,0,0.08)" }}
                formatter={(v) => [`${v ?? ""}`, "Risk Score"]}
              />
              <Line
                type="monotone"
                dataKey="score"
                stroke="#1E3A8A"
                strokeWidth={2.5}
                dot={{ r: 3, fill: "#1E3A8A", strokeWidth: 0 }}
                activeDot={{ r: 5, fill: "#1E3A8A" }}
              />
            </LineChart>
          </ResponsiveContainer>
          <p className="text-xs text-slate-400 mt-1 text-center">Lower score = better wellbeing · Not a clinical diagnosis</p>
        </Card>
      </div>

      {/* Domain breakdown */}
      <div className="px-5">
        <Card padding="md">
          <p className="text-sm font-bold font-display text-navy-900 mb-4">This Week's Areas</p>
          <div className="space-y-4">
            {[
              { label: "Mood & Emotions", score: 72, emoji: "😊" },
              { label: "Sleep Quality", score: 45, emoji: "😴" },
              { label: "Physical Wellbeing", score: 60, emoji: "💪" },
              { label: "Sense of Safety", score: 80, emoji: "🛡️" },
              { label: "Social Support", score: 55, emoji: "🤝" },
            ].map(({ label, score, emoji }) => (
              <div key={label}>
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center gap-2">
                    <span className="text-base">{emoji}</span>
                    <span className="text-sm text-slate-700 font-medium">{label}</span>
                  </div>
                  <span className="text-sm font-bold font-display text-navy-900">{score}</span>
                </div>
                <ProgressBar value={score} size="sm" />
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Past check-ins */}
      <div className="px-5">
        <SectionHeader title="Past Check-ins" subtitle="Your recent sessions" />
        
        {loading ? (
          <div className="py-8 text-center text-slate-500 text-sm">Loading history...</div>
        ) : error ? (
          <div className="py-4 text-center text-critical-600 text-sm">{error}</div>
        ) : history.length === 0 ? (
          <div className="py-8 text-center text-slate-500 text-sm">No check-ins yet.</div>
        ) : (
          <div className="space-y-3">
            {history.map((session) => (
              <Card key={session.id} padding="md" hoverable>
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-center gap-3">
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-xl ${
                      session.mode === "voice" ? "bg-navy-50" : "bg-slate-50"
                    }`}>
                      {session.mode === "voice" ? "🎙️" : "📝"}
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-navy-900 font-display">
                        {new Date(session.created_at).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric", hour: '2-digit', minute: '2-digit' })}
                      </p>
                      <p className="text-xs text-slate-500 capitalize">{session.mode} check-in</p>
                    </div>
                  </div>
                  <div className="text-right shrink-0">
                    <p className="text-lg font-bold font-display text-navy-900">{session.risk_score ?? 0}</p>
                    <RiskBadge level={session.risk_level === 'critical' ? 'high' : session.risk_level === 'moderate' ? 'medium' : session.risk_level || 'low'} size="sm" showDot={false} />
                  </div>
                </div>
                <div className="mt-3 flex flex-wrap gap-1.5">
                  {session.domain_scores?.map((d: any, i: number) => (
                    <span key={i} className="text-xs bg-slate-100 text-slate-600 px-2.5 py-1 rounded-full">
                      {d.domain} ({d.score}/10)
                    </span>
                  ))}
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Milestone */}
      <div className="px-5">
        <Card padding="md" className="bg-gradient-to-br from-navy-900 to-navy-800 border-0 text-white">
          <div className="flex items-center gap-3">
            <span className="text-3xl">🏆</span>
            <div>
              <p className="text-sm font-bold font-display">{history.length} Check-ins Completed!</p>
              <p className="text-xs text-navy-300 mt-0.5">You are doing great. Every step matters.</p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
