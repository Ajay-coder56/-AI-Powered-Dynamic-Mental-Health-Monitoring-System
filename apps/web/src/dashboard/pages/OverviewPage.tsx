import React, { useState } from "react";
import {
  StatCard,
  AlertCard,
  Card,
  SectionHeader,
  RiskBadge,
  TrendChip,
  Avatar,
  RiskGauge,
} from "../../components/ds";
import { cases, alerts, riskDistribution, weeklyCheckIns } from "../../data/sampleData";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Legend,
} from "recharts";

interface OverviewPageProps {
  onSelectCase: (id: string) => void;
  onGoAlerts: () => void;
}

export default function OverviewPage({ onSelectCase, onGoAlerts }: OverviewPageProps) {
  const [alertList, setAlertList] = useState(alerts);
  const unresolvedAlerts = alertList.filter((a) => !a.isResolved);
  const criticalCases = cases.filter((c) => c.riskLevel === "critical" || c.riskLevel === "high");

  const markResolved = (id: string) => {
    setAlertList((prev) => prev.map((a) => (a.id === id ? { ...a, isResolved: true } : a)));
  };

  return (
    <div className="flex flex-col gap-6">
      {/* Page title */}
      <div>
        <h1 className="text-2xl font-bold font-display text-navy-900">Good morning, Counsellor</h1>
        <p className="text-sm text-slate-500 mt-1">
          Thu, 3 Sep 2026 · All cases under your supervision
        </p>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-2 gap-4 xl:grid-cols-4">
        <StatCard
          label="Total Active Cases"
          value="48"
          sub="Across 6 districts"
          icon={<span className="text-xl">👥</span>}
          color="navy"
        />
        <StatCard
          label="Critical & High Risk"
          value="11"
          sub="Requires immediate review"
          icon={<span className="text-xl">🚨</span>}
          color="critical"
          trend="up"
          trendValue="3 more than last week"
        />
        <StatCard
          label="Needs Attention"
          value="15"
          sub="Monitoring closely (Moderate)"
          icon={<span className="text-xl">⚠️</span>}
          color="risk"
          trend="neutral"
          trendValue="Same as last week"
        />
        <StatCard
          label="Stable"
          value="22"
          sub="Doing well"
          icon={<span className="text-xl">✅</span>}
          color="safe"
          trend="neutral"
          trendValue="2 more than last week"
        />
      </div>

      {/* Global Filters */}
      <div className="flex flex-wrap items-center gap-3 bg-white p-3 rounded-2xl border border-slate-100 shadow-sm">
        <div className="flex items-center gap-2 text-slate-400 pl-2 pr-1">
          <span className="text-lg">⚙️</span>
          <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Filters</span>
        </div>
        <select className="bg-slate-50 border border-slate-200 text-slate-700 text-sm font-medium rounded-xl px-4 py-2.5 outline-none focus:border-navy-500 focus:bg-white transition-colors cursor-pointer">
          <option>All Districts</option>
          <option>Mumbai</option>
          <option>Pune</option>
          <option>Nagpur</option>
          <option>Thane</option>
        </select>
        <select className="bg-slate-50 border border-slate-200 text-slate-700 text-sm font-medium rounded-xl px-4 py-2.5 outline-none focus:border-navy-500 focus:bg-white transition-colors cursor-pointer">
          <option>All Risk Levels</option>
          <option>Critical</option>
          <option>High</option>
          <option>Moderate</option>
          <option>Stable</option>
        </select>
        <select className="bg-slate-50 border border-slate-200 text-slate-700 text-sm font-medium rounded-xl px-4 py-2.5 outline-none focus:border-navy-500 focus:bg-white transition-colors cursor-pointer">
          <option>All Case Statuses</option>
          <option>Active</option>
          <option>Pending Review</option>
          <option>Closed</option>
        </select>
        <input type="date" className="bg-slate-50 border border-slate-200 text-slate-700 text-sm font-medium rounded-xl px-4 py-2.5 outline-none focus:border-navy-500 focus:bg-white transition-colors cursor-pointer" />
      </div>

      {/* ── Upcoming Legal Milestones ───────────────────────────────── */}
      <Card padding="lg">
        <SectionHeader
          title="Upcoming Legal Milestones"
          subtitle="Cases with hearings in the next 14 days — pre-emptive counselling recommended"
        />
        <div className="overflow-x-auto">
          <table className="w-full min-w-[700px]">
            <thead>
              <tr className="border-b border-slate-100">
                {["Case ID", "Upcoming Event", "Days Left", "Current Risk", "Trend", "Suggested Action"].map((h) => (
                  <th key={h} className="text-xs font-semibold text-slate-400 text-left pb-3 pr-4 uppercase tracking-wider">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[
                {
                  id: "MH-2026-0041",
                  event: "Final hearing",
                  days: 5,
                  risk: "High" as const,
                  riskColor: "#EF4444",
                  riskBg: "#FEF2F2",
                  trend: "↑ Increasing",
                  trendColor: "#EF4444",
                  action: "Schedule proactive counselling session before hearing",
                },
                {
                  id: "MH-2026-0028",
                  event: "Cross-examination",
                  days: 8,
                  risk: "Critical" as const,
                  riskColor: "#BE123C",
                  riskBg: "#FFF1F2",
                  trend: "↑ Increasing",
                  trendColor: "#EF4444",
                  action: "Immediate counsellor contact + safety protocol review",
                },
                {
                  id: "MH-2026-0015",
                  event: "Mediation session",
                  days: 10,
                  risk: "Moderate" as const,
                  riskColor: "#D97706",
                  riskBg: "#FFFBEB",
                  trend: "→ Stable",
                  trendColor: "#94A3B8",
                  action: "Check-in call 2 days before; provide coping resources",
                },
                {
                  id: "MH-2026-0037",
                  event: "Witness deposition",
                  days: 13,
                  risk: "Moderate" as const,
                  riskColor: "#D97706",
                  riskBg: "#FFFBEB",
                  trend: "↓ Improving",
                  trendColor: "#16A34A",
                  action: "Continue current support plan; monitor check-in frequency",
                },
              ].map((row) => (
                <tr key={row.id} className="border-b border-slate-50 hover:bg-slate-50 transition-smooth">
                  <td className="py-3 pr-4">
                    <span className="text-xs font-mono-data text-slate-700 font-semibold">{row.id}</span>
                  </td>
                  <td className="py-3 pr-4">
                    <span className="text-sm font-semibold text-navy-900">{row.event}</span>
                  </td>
                  <td className="py-3 pr-4">
                    <span
                      className="inline-flex items-center text-xs font-bold px-2.5 py-1 rounded-full"
                      style={{
                        color: row.days <= 7 ? '#BE123C' : '#D97706',
                        backgroundColor: row.days <= 7 ? '#FFF1F2' : '#FFFBEB',
                      }}
                    >
                      {row.days} days
                    </span>
                  </td>
                  <td className="py-3 pr-4">
                    <span
                      className="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full"
                      style={{ color: row.riskColor, backgroundColor: row.riskBg }}
                    >
                      <span className="w-1.5 h-1.5 rounded-full inline-block" style={{ backgroundColor: row.riskColor }} />
                      {row.risk}
                    </span>
                  </td>
                  <td className="py-3 pr-4">
                    <span className="text-xs font-semibold" style={{ color: row.trendColor }}>
                      {row.trend}
                    </span>
                  </td>
                  <td className="py-3">
                    <span className="text-xs text-slate-600 leading-relaxed">{row.action}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Main grid */}
      <div className="grid grid-cols-1 gap-6 xl:grid-cols-3">
        {/* Alerts column */}
        <div className="xl:col-span-2 flex flex-col gap-6">
          {/* Active Alerts */}
          <Card padding="lg">
            <SectionHeader
              title="Active Alerts"
              subtitle={`${unresolvedAlerts.length} alerts require attention`}
              action={
                <button onClick={onGoAlerts} className="text-xs text-navy-700 font-semibold hover:underline">
                  View all →
                </button>
              }
            />
            <div className="space-y-3">
              {unresolvedAlerts.slice(0, 4).map((alert) => (
                <AlertCard
                  key={alert.id}
                  severity={alert.severity}
                  type={alert.type}
                  message={alert.message}
                  victimName={alert.victimName}
                  caseNumber={alert.caseNumber}
                  time={alert.triggeredAt}
                  isRead={alert.isRead}
                  isResolved={alert.isResolved}
                  onView={() => onSelectCase(alert.caseId)}
                  onResolve={() => markResolved(alert.id)}
                />
              ))}
              {unresolvedAlerts.length === 0 && (
                <div className="py-8 text-center text-slate-400">
                  <p className="text-2xl mb-2">✅</p>
                  <p className="text-sm font-semibold">No active alerts</p>
                </div>
              )}
            </div>
          </Card>

          {/* Recent Interventions */}
          <Card padding="lg">
            <SectionHeader title="Recent Interventions" subtitle="Actions taken in the last 24 hours" />
            <div className="pt-2">
              {[
                { time: "10:30 AM", type: "Emergency Call", case: "MH-2026-0028", note: "Connected with victim. De-escalated panic attack. Local support notified." },
                { time: "09:15 AM", type: "Counselling Session", case: "MH-2026-0041", note: "Completed pre-hearing coping strategy session." },
                { time: "Yesterday", type: "Resource Sent", case: "MH-2026-0015", note: "Sent guided meditation and legal FAQ via text." }
              ].map((inv, idx, arr) => (
                <div key={idx} className="flex gap-4 relative">
                  {idx !== arr.length - 1 && <div className="absolute left-[85px] top-6 bottom-0 w-0.5 bg-slate-100 -mb-2" />}
                  <div className="w-[60px] shrink-0 text-right text-xs text-slate-400 font-semibold pt-1">{inv.time}</div>
                  <div className="w-2.5 h-2.5 rounded-full bg-navy-400 shrink-0 mt-1.5 shadow-[0_0_0_4px_#fff]" />
                  <div className="flex-1 pb-6">
                    <p className="text-sm font-bold text-navy-900">{inv.type} <span className="font-normal text-slate-400 mx-1">·</span> <span className="font-semibold text-slate-600">{inv.case}</span></p>
                    <p className="text-sm text-slate-600 mt-1 leading-relaxed">{inv.note}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* Weekly check-in chart */}
          <Card padding="lg">
            <SectionHeader title="Weekly Check-in Completion" subtitle="Daily completed vs missed check-ins" />
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={weeklyCheckIns} margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
                <XAxis dataKey="day" tick={{ fontSize: 12, fill: "#94A3B8" }} tickLine={false} axisLine={false} />
                <YAxis tick={{ fontSize: 11, fill: "#94A3B8" }} tickLine={false} axisLine={false} />
                <Tooltip
                  contentStyle={{ fontSize: 12, borderRadius: 10, border: "1px solid #E2E8F0" }}
                />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="completed" name="Completed" fill="#16A34A" radius={[4, 4, 0, 0]} />
                <Bar dataKey="missed" name="Missed" fill="#FCA5A5" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </div>

        {/* Right column */}
        <div className="flex flex-col gap-6">
          {/* Risk Overview */}
          <Card padding="lg">
            <SectionHeader title="Risk Overview" subtitle="All 48 active cases" />
            <ResponsiveContainer width="100%" height={160}>
              <PieChart>
                <Pie
                  data={riskDistribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={72}
                  dataKey="value"
                  paddingAngle={3}
                >
                  {riskDistribution.map((entry, i) => (
                    <Cell key={i} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ fontSize: 12, borderRadius: 8, border: "1px solid #E2E8F0" }}
                  formatter={(v, name) => [`${v ?? ""} cases`, String(name)]}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="space-y-1.5 mt-2">
              {riskDistribution.map((d) => (
                <div key={d.name} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="w-3 h-3 rounded-full shrink-0" style={{ backgroundColor: d.color }} />
                    <span className="text-xs text-slate-600">{d.name}</span>
                  </div>
                  <span className="text-xs font-bold font-display text-slate-700">{d.value}</span>
                </div>
              ))}
            </div>
          </Card>

          {/* High-priority cases */}
          <Card padding="lg">
            <SectionHeader
              title="High-priority cases"
              subtitle="High & critical risk"
              action={
                <RiskBadge level="critical" size="sm" />
              }
            />
            <div className="space-y-3">
              {criticalCases.map((c) => (
                <div
                  key={c.id}
                  onClick={() => onSelectCase(c.id)}
                  className="flex items-center gap-3 p-3 rounded-xl border border-slate-100 hover:border-navy-200 hover:bg-slate-50 cursor-pointer transition-smooth"
                >
                  <Avatar name={c.victimName} size="md" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold text-navy-900 font-display truncate">{c.victimName}</p>
                    <div className="flex items-center gap-2 mt-0.5">
                      <RiskGauge score={c.riskScore} size={32} />
                      <TrendChip trend={c.trend} />
                    </div>
                  </div>
                  {c.alertCount > 0 && (
                    <span className="text-xs bg-critical-600 text-white px-1.5 py-0.5 rounded-full font-bold shrink-0">
                      {c.alertCount}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </Card>

          {/* Quick stats — Today at a Glance */}
          <Card padding="lg" className="bg-white border border-slate-100">
            {/* Section heading */}
            <p
              className="text-xs font-bold uppercase tracking-widest mb-4"
              style={{ color: '#172033', letterSpacing: '0.08em' }}
            >
              Today at a Glance
            </p>
            <div className="space-y-4">
              {[
                { label: "Counsellors on duty",  value: "6",      accent: "#3B5BDB" },
                { label: "Sessions completed",    value: "34",     accent: "#16A34A" },
                { label: "Avg response time",     value: "18 min", accent: "#D97706" },
                { label: "Cases improving",       value: "12",     accent: "#3B5BDB" },
              ].map(({ label, value, accent }) => (
                <div
                  key={label}
                  className="flex items-center justify-between pl-3 py-0.5"
                  style={{ borderLeft: `3px solid ${accent}` }}
                >
                  <span
                    className="text-xs font-medium leading-tight"
                    style={{ color: '#52627A' }}
                  >
                    {label}
                  </span>
                  <span
                    className="text-xl font-bold font-display tabular-nums"
                    style={{ color: '#172033' }}
                  >
                    {value}
                  </span>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>

      {/* Recent cases table */}
      <Card padding="lg">
        <SectionHeader
          title="Recent Cases"
          subtitle="Showing 6 of 48 cases"
          action={
            <button className="text-xs text-navy-700 font-semibold hover:underline">View all cases →</button>
          }
        />
        <div className="overflow-x-auto">
          <table className="w-full min-w-[640px]">
            <thead>
              <tr className="border-b border-slate-100">
                {["Victim", "Case No.", "Case Type", "Risk Score", "Last Check-in", "Trend", "Alerts"].map((h) => (
                  <th key={h} className="text-xs font-semibold text-left pb-3 pr-4 uppercase tracking-wider" style={{ color: '#52627A' }}>
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {cases.map((c) => (
                <tr
                  key={c.id}
                  onClick={() => onSelectCase(c.id)}
                  className="border-b border-slate-50 hover:bg-slate-50 cursor-pointer transition-smooth"
                >
                  <td className="py-3 pr-4">
                    <div className="flex items-center gap-2.5">
                      <Avatar name={c.victimName} size="sm" />
                      <div>
                        <p className="text-sm font-semibold font-display" style={{ color: '#172033' }}>{c.victimName}</p>
                        <p className="text-xs" style={{ color: '#718096' }}>{c.city} · {c.language}</p>
                      </div>
                    </div>
                  </td>
                  <td className="py-3 pr-4">
                    <span className="text-xs font-mono-data text-slate-600">{c.caseNumber}</span>
                  </td>
                  <td className="py-3 pr-4">
                    <span className="text-xs text-slate-600">{c.caseType}</span>
                  </td>
                  <td className="py-3 pr-4">
                    <div className="flex items-center gap-2">
                      <RiskGauge score={c.riskScore} size={36} />
                      <RiskBadge level={c.riskLevel} size="sm" />
                    </div>
                  </td>
                  <td className="py-3 pr-4">
                    <span className="text-xs text-slate-600">{c.lastCheckIn}</span>
                  </td>
                  <td className="py-3 pr-4">
                    <TrendChip trend={c.trend} />
                  </td>
                  <td className="py-3">
                    {c.alertCount > 0 ? (
                      <span className="text-xs bg-critical-100 text-critical-700 font-bold px-2 py-0.5 rounded-full">
                        {c.alertCount} alert{c.alertCount > 1 ? "s" : ""}
                      </span>
                    ) : (
                      <span className="text-xs text-slate-300">—</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
