import React, { useEffect, useState } from "react";
import { Card, RiskGauge, Button } from "../../components/ds";
import { mobileUserTrend } from "../../data/sampleData";
import { usersService } from "../../services/users";
import { checkInsService } from "../../services/checkIns";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

interface HomeScreenProps {
  userId: string;
  onStartCheckIn: () => void;
  onStartVoice: () => void;
}

export default function HomeScreen({ userId, onStartCheckIn, onStartVoice }: HomeScreenProps) {
  const [user, setUser] = useState<any>(null);
  const [latestCheckIn, setLatestCheckIn] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [userData, history] = await Promise.all([
          usersService.getUser(userId),
          checkInsService.getCheckInHistory(userId)
        ]);
        setUser(userData);
        if (history && history.length > 0) {
          setLatestCheckIn(history[0]);
        }
      } catch (err) {
        console.error(err);
        setError("Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [userId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-sm text-slate-500">Loading your space...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-sm text-critical-600">{error}</p>
      </div>
    );
  }

  const firstName = user?.name ? user.name.split(" ")[0] : "User";
  const score = latestCheckIn ? latestCheckIn.wellbeing_score || 50 : 0;
  
  // Format last checked in time safely
  let lastCheckedIn = "Never";
  if (latestCheckIn && latestCheckIn.created_at) {
    const date = new Date(latestCheckIn.created_at);
    lastCheckedIn = date.toLocaleDateString() + ", " + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }
  
  const hearingDays = 7;

  return (
    <div className="flex flex-col gap-4 pb-4">
      {/* Greeting */}
      <div className="px-5 pt-5">
        <p className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Good Morning</p>
        <h1 className="text-2xl font-bold font-display text-navy-900 mt-0.5">{firstName}</h1>
        <p className="text-sm text-slate-500 mt-1">Your wellbeing matters. We are here with you.</p>
      </div>

      {/* Wellbeing Card — supportive framing */}
      <div className="px-5">
        <Card padding="lg" className="bg-gradient-to-br from-navy-900 to-navy-700 border-0 text-white">
          <div className="flex items-center justify-between gap-4">
            <div className="flex-1">
              <p className="text-xs font-semibold uppercase tracking-wider mb-1" style={{ color: '#AAB8D3' }}>
                Latest Check-in
              </p>
              <p className="text-2xl font-bold font-display mb-1" style={{ color: '#FFFFFF' }}>
                {latestCheckIn ? "You're doing okay 🌿" : "No check-ins yet"}
              </p>
              {latestCheckIn && (
                <div className="flex items-center gap-2 mt-2">
                  <span className="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full bg-safe-500/20 border border-safe-500/30" style={{ color: '#4ADE80' }}>
                    <span className="w-1.5 h-1.5 rounded-full bg-safe-400 inline-block" />
                    {latestCheckIn.risk_level} concern
                  </span>
                </div>
              )}
              <p className="text-xs mt-3" style={{ color: '#AAB8D3' }}>
                Last check-in: {lastCheckedIn}
              </p>
            </div>
            <div className="shrink-0 flex flex-col items-center gap-1">
              <RiskGauge score={score} size={80} />
              <p className="text-xs text-center" style={{ color: '#AAB8D3' }}>{score}/100</p>
            </div>
          </div>

          {/* Subtle progress bar */}
          <div className="mt-4">
            <div className="flex justify-between text-xs mb-1" style={{ color: '#AAB8D3' }}>
              <span>Wellbeing level</span>
              <span>{latestCheckIn ? "Improving ↓" : ""}</span>
            </div>
            <div className="h-1.5 bg-navy-800/60 rounded-full overflow-hidden">
              <div
                className="h-1.5 rounded-full transition-all duration-1000"
                style={{ width: `${score}%`, backgroundColor: '#22C55E' }}
              />
            </div>
          </div>
        </Card>
      </div>

      {/* Today's Check-in CTA */}
      <div className="px-5">
        <Card padding="md" className="border-safe-200 bg-safe-50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-safe-100 rounded-xl flex items-center justify-center text-xl shrink-0">
              ✅
            </div>
            <div className="flex-1">
              <p className="text-sm font-bold text-navy-900 font-display">Daily Check-in Due</p>
              <p className="text-xs text-slate-500">Takes 3–5 minutes. You can do it!</p>
            </div>
          </div>
          <div className="flex gap-2 mt-3">
            <Button variant="primary" size="md" className="flex-1" onClick={onStartCheckIn}>
              📝 Answer Questions
            </Button>
            <Button variant="outline" size="md" className="flex-1" onClick={onStartVoice}>
              🎙️ Voice Check-in
            </Button>
          </div>
        </Card>
      </div>

      {/* Hearing reminder */}
      <div className="px-5">
        <Card padding="md" className="border-risk-200 bg-risk-50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-risk-100 rounded-xl flex items-center justify-center text-xl shrink-0">
              ⚖️
            </div>
            <div className="flex-1">
              <p className="text-sm font-bold text-navy-900 font-display">Court Hearing</p>
              <p className="text-xs text-slate-600">
                Next hearing in <span className="font-bold text-risk-700">{hearingDays} days</span> — Sep 18, 2026
              </p>
            </div>
          </div>
          <p className="text-xs text-slate-500 mt-2 leading-relaxed">
            Feeling anxious about the hearing is normal. Speak to your counsellor anytime.
          </p>
          <button className="text-xs text-navy-700 font-semibold mt-2 hover:underline">
            Contact Dr. Meera Iyer →
          </button>
        </Card>
      </div>

      {/* Check-in streak */}
      <div className="px-5">
        <Card padding="md">
          <div className="flex items-center justify-between mb-3">
            <p className="text-sm font-bold text-navy-900 font-display">Your Streak 🔥</p>
            <span className="text-xs text-slate-400">34 total sessions</span>
          </div>
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-risk-50 rounded-xl flex items-center justify-center">
              <span className="text-2xl font-bold font-display text-risk-600">12</span>
            </div>
            <div>
              <p className="text-sm font-semibold text-navy-900">12 Days in a Row</p>
              <p className="text-xs text-slate-500">Keep going — every check-in matters</p>
            </div>
          </div>
          {/* Week dots */}
          <div className="flex gap-2 mt-3">
            {["M", "T", "W", "T", "F", "S", "S"].map((day, i) => (
              <div key={i} className="flex flex-col items-center gap-1 flex-1">
                <div
                  className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
                    i < 6 ? "bg-safe-100 text-safe-700" : "bg-slate-100 text-slate-400"
                  }`}
                >
                  {i < 6 ? "✓" : "–"}
                </div>
                <span className="text-xs text-slate-400">{day}</span>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Mini trend chart */}
      <div className="px-5">
        <Card padding="md">
          <div className="flex items-center justify-between mb-3">
            <p className="text-sm font-bold text-navy-900 font-display">Last 30 Days (Mock Data)</p>
            <span className="text-xs text-safe-600 font-semibold bg-safe-50 px-2 py-0.5 rounded-full">↓ Improving</span>
          </div>
          <ResponsiveContainer width="100%" height={80}>
            <LineChart data={mobileUserTrend} margin={{ top: 4, right: 4, left: -30, bottom: 0 }}>
              <XAxis dataKey="label" tick={{ fontSize: 10, fill: "#94A3B8" }} tickLine={false} axisLine={false} interval={4} />
              <YAxis domain={[0, 100]} tick={false} axisLine={false} />
              <Tooltip
                contentStyle={{ fontSize: 12, borderRadius: 8, border: "1px solid #E2E8F0" }}
                formatter={(v) => [`${v ?? ""}`, "Risk Score"]}
              />
              <Line
                type="monotone"
                dataKey="score"
                stroke="#1E3A8A"
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4, fill: "#1E3A8A" }}
              />
            </LineChart>
          </ResponsiveContainer>
          <p className="text-xs text-slate-400 mt-1">Lower score = better wellbeing</p>
        </Card>
      </div>
    </div>
  );
}
