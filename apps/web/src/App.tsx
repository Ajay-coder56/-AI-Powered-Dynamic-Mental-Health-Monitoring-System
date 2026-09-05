import React, { useState } from "react";
import MobileShell from "./mobile/MobileShell";
import DashboardShell from "./dashboard/DashboardShell";

type Interface = "landing" | "mobile" | "dashboard";

export default function App() {
  const [view, setView] = useState<Interface>("landing");

  if (view === "mobile") {
    return (
      <div className="flex flex-col h-full bg-slate-200">
        {/* Back bar */}
        <div className="bg-white border-b border-slate-200 px-4 py-2 flex items-center justify-between shrink-0">
          <button
            onClick={() => setView("landing")}
            className="text-xs text-navy-700 font-semibold hover:underline"
          >
            ← Back to Interface Selector
          </button>
          <span className="text-xs text-slate-400 font-semibold">📱 Victim Mobile App · MindSafe</span>
        </div>
        {/* Phone frame */}
        <div className="flex-1 flex items-center justify-center p-4 overflow-hidden">
          <div
            className="relative bg-white shadow-2xl overflow-hidden flex flex-col"
            style={{
              width: 390,
              height: "min(780px, calc(100vh - 100px))",
              maxHeight: "100%",
              borderRadius: 40,
              border: "8px solid #1B3270",
            }}
          >
            {/* Notch */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-28 h-7 bg-navy-950 rounded-b-2xl z-10" />
            <div className="flex-1 overflow-hidden pt-7">
              <MobileShell />
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (view === "dashboard") {
    return (
      <div className="flex flex-col h-full">
        {/* Back bar */}
        <div className="bg-white border-b border-slate-200 px-4 py-2 flex items-center justify-between shrink-0 z-50">
          <button
            onClick={() => setView("landing")}
            className="text-xs text-navy-700 font-semibold hover:underline"
          >
            ← Back to Interface Selector
          </button>
          <span className="text-xs text-slate-400 font-semibold">🖥️ Counsellor / Case Worker Dashboard · MindSafe</span>
        </div>
        <div className="flex-1 overflow-hidden">
          <DashboardShell />
        </div>
      </div>
    );
  }

  // Landing selector
  return (
    <div className="min-h-full bg-gradient-to-br from-navy-950 via-navy-900 to-navy-800 flex flex-col">
      {/* Header */}
      <header className="px-8 py-6 flex items-center justify-between border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-navy-600 rounded-xl flex items-center justify-center">
            <span className="text-white font-bold text-lg font-display">M</span>
          </div>
          <div>
            <p className="text-white font-bold font-display text-lg leading-none">MindSafe</p>
            <p className="text-slate-300 text-xs mt-0.5">AI Mental Health Monitoring System</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-xs text-slate-300 bg-white/10 border border-white/10 px-3 py-1.5 rounded-full">
            Smart India Hackathon 2026
          </span>
          <span className="text-xs text-slate-300 bg-white/10 border border-white/10 px-3 py-1.5 rounded-full">
            Ministry of WCD · Govt. of India
          </span>
        </div>
      </header>

      {/* Hero */}
      <div className="flex-1 flex flex-col items-center justify-center px-6 py-12 text-center">
        <div className="max-w-2xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-white/10 border border-white/20 rounded-full px-4 py-2 mb-6">
            <span className="w-2 h-2 rounded-full bg-safe-500 animate-pulse" />
            <span className="text-xs text-white font-semibold">AI-Powered · Multilingual · Privacy-First</span>
          </div>

          <h1 className="text-4xl sm:text-5xl font-bold font-display leading-tight mb-4" style={{ color: '#FFFFFF' }}>
            Dynamic Mental Health<br />
            <span style={{ color: '#60A5FA' }}>Monitoring System</span>
          </h1>

          <p className="text-base leading-relaxed mb-2 max-w-xl mx-auto" style={{ color: '#D6DEEF' }}>
            Proactive mental health support and early distress detection for vulnerable victims
            during prolonged legal proceedings.
          </p>
          <p className="text-sm mb-10" style={{ color: '#AAB8D3' }}>
            Select an interface below to explore the prototype
          </p>

          {/* Interface cards */}
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 max-w-xl mx-auto">
            <button
              onClick={() => setView("mobile")}
              className="group bg-white/8 hover:bg-white/12 border border-white/15 hover:border-blue-400/50 rounded-2xl p-6 text-left transition-all duration-300 hover:shadow-2xl hover:shadow-navy-900/50 hover:-translate-y-0.5"
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 bg-navy-700 group-hover:bg-navy-600 rounded-xl flex items-center justify-center text-2xl transition-smooth">
                  📱
                </div>
                <div>
                  <p className="font-bold font-display text-base" style={{ color: '#FFFFFF' }}>Victim / Citizen</p>
                  <p className="text-xs" style={{ color: '#AAB8D3' }}>Mobile App</p>
                </div>
              </div>
              <p className="text-sm leading-relaxed mb-4" style={{ color: '#D6DEEF' }}>
                Simple, accessible mobile experience for daily check-ins. Supports voice and questionnaire modes, 11 Indian languages.
              </p>
              <ul className="space-y-1.5">
                {["Daily wellbeing check-in", "Voice & text modes", "Multilingual support", "Progress tracking", "Emergency help & support"].map((f) => (
                  <li key={f} className="text-xs flex items-center gap-2" style={{ color: '#D6DEEF' }}>
                    <span className="text-safe-500">✓</span> {f}
                  </li>
                ))}
              </ul>
              <div className="mt-5 flex items-center justify-between">
                <span className="text-xs" style={{ color: '#AAB8D3' }}>Designed for low digital literacy</span>
                <span className="text-sm font-semibold group-hover:translate-x-1 transition-transform" style={{ color: '#FFFFFF' }}>→</span>
              </div>
            </button>

            <button
              onClick={() => setView("dashboard")}
              className="group bg-white/8 hover:bg-white/12 border border-white/15 hover:border-blue-400/50 rounded-2xl p-6 text-left transition-all duration-300 hover:shadow-2xl hover:shadow-navy-900/50 hover:-translate-y-0.5"
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 bg-navy-700 group-hover:bg-navy-600 rounded-xl flex items-center justify-center text-2xl transition-smooth">
                  🖥️
                </div>
                <div>
                  <p className="font-bold font-display text-base" style={{ color: '#FFFFFF' }}>Counsellor / Case Worker</p>
                  <p className="text-xs" style={{ color: '#AAB8D3' }}>Web Dashboard</p>
                </div>
              </div>
              <p className="text-sm leading-relaxed mb-4" style={{ color: '#D6DEEF' }}>
                Professional data-dense dashboard for monitoring multiple cases, managing alerts, and accessing AI-powered risk analysis.
              </p>
              <ul className="space-y-1.5">
                {["Risk score monitoring", "AI-generated alerts", "Case trend analysis", "Session history", "Pre-hearing risk detection"].map((f) => (
                  <li key={f} className="text-xs flex items-center gap-2" style={{ color: '#D6DEEF' }}>
                    <span className="text-safe-500">✓</span> {f}
                  </li>
                ))}
              </ul>
              <div className="mt-5 flex items-center justify-between">
                <span className="text-xs" style={{ color: '#AAB8D3' }}>Professional-grade analytics</span>
                <span className="text-sm font-semibold group-hover:translate-x-1 transition-transform" style={{ color: '#FFFFFF' }}>→</span>
              </div>
            </button>
          </div>

          {/* Disclaimer */}
          <div className="mt-10 max-w-lg mx-auto bg-white/8 border border-white/15 rounded-xl px-5 py-4">
            <p className="text-xs leading-relaxed" style={{ color: '#D6DEEF' }}>
              <strong style={{ color: '#FFFFFF' }}>Important:</strong> The AI risk scores shown in this system are decision-support indicators to assist trained counsellors. They do not constitute medical or psychological diagnoses. All interventions must be guided by qualified mental health professionals.
            </p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-white/10 px-8 py-4 flex items-center justify-between flex-wrap gap-2">
        <p className="text-xs" style={{ color: '#AAB8D3' }}>
          MindSafe · Built for Smart India Hackathon 2026 · Ministry of Women and Child Development
        </p>
        <div className="flex items-center gap-4">
          <span className="text-xs" style={{ color: '#AAB8D3' }}>🔒 Privacy-First</span>
          <span className="text-xs" style={{ color: '#AAB8D3' }}>🌐 Multilingual</span>
          <span className="text-xs" style={{ color: '#AAB8D3' }}>♿ Accessible</span>
        </div>
      </footer>
    </div>
  );
}
