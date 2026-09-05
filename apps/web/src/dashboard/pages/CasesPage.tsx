import React, { useState } from "react";
import {
  Card,
  RiskBadge,
  TrendChip,
  Avatar,
  RiskGauge,
  Chip,
  SectionHeader,
  Button,
} from "../../components/ds";
import { cases } from "../../data/sampleData";
import type { RiskLevel } from "../../data/sampleData";

interface CasesPageProps {
  onSelectCase: (id: string) => void;
}

export default function CasesPage({ onSelectCase }: CasesPageProps) {
  const [search, setSearch] = useState("");
  const [view, setView] = useState<"table" | "cards">("table");

  const filtered = cases
    .filter((c) => {
      const q = search.toLowerCase();
      return (
        c.victimName.toLowerCase().includes(q) ||
        c.caseNumber.toLowerCase().includes(q) ||
        c.id.toLowerCase().includes(q) ||
        c.caseType.toLowerCase().includes(q)
      );
    });

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h1 className="text-2xl font-bold font-display text-navy-900">All Cases</h1>
          <p className="text-sm text-slate-500 mt-1">
            {filtered.length} of {cases.length} cases shown
          </p>
        </div>
        <Button variant="primary" size="sm">
          + Add New Case
        </Button>
      </div>

      {/* Filters */}
      <Card padding="md">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:flex-wrap">
          {/* Search */}
          <div className="relative flex-1 min-w-[200px]">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">🔍</span>
            <input
              type="text"
              placeholder="Search by Case ID..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-4 py-2.5 text-sm border border-slate-200 rounded-xl bg-white focus:outline-none focus:ring-2 focus:ring-navy-300 focus:border-navy-400 transition-smooth placeholder-slate-400 font-medium"
            />
          </div>

          <select className="text-sm font-medium border border-slate-200 rounded-xl px-4 py-2.5 bg-white text-slate-700 outline-none focus:border-navy-400 cursor-pointer">
            <option>All Risk Levels</option>
            <option>Critical</option>
            <option>High</option>
            <option>Moderate</option>
            <option>Stable</option>
          </select>

          <input type="date" className="text-sm font-medium border border-slate-200 rounded-xl px-4 py-2.5 bg-white text-slate-700 outline-none focus:border-navy-400 cursor-pointer" />
          
          <select className="text-sm font-medium border border-slate-200 rounded-xl px-4 py-2.5 bg-white text-slate-700 outline-none focus:border-navy-400 cursor-pointer">
            <option>All Statuses</option>
            <option>Active</option>
            <option>Monitoring</option>
            <option>Resolved</option>
          </select>

          <select className="text-sm font-medium border border-slate-200 rounded-xl px-4 py-2.5 bg-white text-slate-700 outline-none focus:border-navy-400 cursor-pointer">
            <option>Any Upcoming Event</option>
            <option>Final Hearing</option>
            <option>Mediation</option>
            <option>Deposition</option>
          </select>

          {/* View toggle */}
          <div className="flex bg-slate-100 rounded-xl p-0.5 shrink-0 ml-auto">
            <button
              onClick={() => setView("table")}
              className={`px-4 py-2 rounded-lg text-xs font-bold transition-smooth ${view === "table" ? "bg-white shadow-sm text-navy-900" : "text-slate-500"}`}
            >
              Table
            </button>
            <button
              onClick={() => setView("cards")}
              className={`px-4 py-2 rounded-lg text-xs font-bold transition-smooth ${view === "cards" ? "bg-white shadow-sm text-navy-900" : "text-slate-500"}`}
            >
              Cards
            </button>
          </div>
        </div>
      </Card>

      {/* Table view */}
      {view === "table" ? (
        <Card padding="lg">
          <div className="overflow-x-auto">
            <table className="w-full min-w-[720px]">
              <thead>
                <tr className="border-b border-slate-100">
                  {["Case ID", "Beneficiary", "Risk Level", "Risk Trend", "Last Check-in", "Upcoming Event", "Assigned Counsellor", "Status", "Action"].map((h) => (
                    <th key={h} className="text-xs font-semibold text-slate-400 text-left pb-3 pr-4 uppercase tracking-wider whitespace-nowrap">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {filtered.map((c) => (
                  <tr
                    key={c.id}
                    onClick={() => onSelectCase(c.id)}
                    className="border-b border-slate-50 hover:bg-slate-50 cursor-pointer transition-smooth"
                  >
                    <td className="py-3.5 pr-4">
                      <span className="text-xs font-mono-data text-slate-600 whitespace-nowrap">{c.caseNumber}</span>
                    </td>
                    <td className="py-3.5 pr-4">
                      <div className="flex items-center gap-2.5">
                        <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-xs font-bold text-slate-500">
                          {c.id.split('-')[2]?.slice(0, 2) || '00'}
                        </div>
                        <div>
                          <p className="text-sm font-semibold text-navy-900 font-display whitespace-nowrap">BEN-{c.id.split('-')[2]}</p>
                          <p className="text-xs text-slate-400">Anonymized</p>
                        </div>
                      </div>
                    </td>
                    <td className="py-3.5 pr-4">
                      <RiskBadge level={c.riskLevel} size="sm" />
                    </td>
                    <td className="py-3.5 pr-4">
                      <TrendChip trend={c.trend} />
                    </td>
                    <td className="py-3.5 pr-4">
                      <span className="text-xs text-slate-600 whitespace-nowrap">{c.lastCheckIn}</span>
                    </td>
                    <td className="py-3.5 pr-4">
                      <span className="text-xs text-risk-700 font-semibold whitespace-nowrap">{c.hearingDate}</span>
                    </td>
                    <td className="py-3.5 pr-4">
                      <span className="text-xs text-slate-600 whitespace-nowrap">{c.assignedCounsellor}</span>
                    </td>
                    <td className="py-3.5 pr-4">
                      <span className="text-xs bg-safe-100 text-safe-700 px-2.5 py-1 rounded-full font-semibold capitalize">{c.status}</span>
                    </td>
                    <td className="py-3.5">
                      <button className="text-xs font-bold text-navy-600 hover:text-navy-800 bg-navy-50 hover:bg-navy-100 px-3 py-1.5 rounded-lg transition-colors">
                        View Profile
                      </button>
                    </td>
                  </tr>
                ))}
                {filtered.length === 0 && (
                  <tr>
                    <td colSpan={9} className="py-12 text-center text-slate-400">
                      <p className="text-2xl mb-2">🔍</p>
                      <p className="text-sm">No cases match your filters</p>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </Card>
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {filtered.map((c) => (
            <Card key={c.id} padding="lg" hoverable onClick={() => onSelectCase(c.id)}>
              <div className="flex items-start justify-between gap-3 mb-3">
                <div className="flex items-center gap-3">
                  <Avatar name={c.victimName} />
                  <div>
                    <p className="text-sm font-bold font-display text-navy-900">{c.victimName}</p>
                    <p className="text-xs text-slate-400">{c.victimAge} yrs · {c.city}</p>
                  </div>
                </div>
                <RiskGauge score={c.riskScore} size={56} />
              </div>

              <div className="flex flex-wrap gap-1.5 mb-3">
                <RiskBadge level={c.riskLevel} size="sm" />
                <TrendChip trend={c.trend} />
                <span className="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full">{c.caseType}</span>
              </div>

              <div className="text-xs text-slate-500 space-y-1 border-t border-slate-100 pt-3">
                <div className="flex justify-between">
                  <span>Case No.</span>
                  <span className="font-mono-data text-navy-700">{c.caseNumber}</span>
                </div>
                <div className="flex justify-between">
                  <span>Last Check-in</span>
                  <span>{c.lastCheckIn}</span>
                </div>
                <div className="flex justify-between">
                  <span>Next Hearing</span>
                  <span className="text-risk-700 font-semibold">{c.hearingDate}</span>
                </div>
              </div>

              {c.alertCount > 0 && (
                <div className="mt-3 bg-critical-50 text-critical-700 text-xs font-semibold px-3 py-1.5 rounded-xl">
                  🚨 {c.alertCount} active alert{c.alertCount > 1 ? "s" : ""}
                </div>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
