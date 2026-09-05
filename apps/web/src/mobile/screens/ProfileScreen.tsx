import React from "react";
import { Card } from "../../components/ds";

interface Props {
  onOpenTrends: () => void;
  onLogout: () => void;
}

export default function ProfileScreen({ onOpenTrends, onLogout }: Props) {
  return (
    <div className="flex flex-col gap-6 px-5 pt-6 pb-8">
      <div>
        <h1 className="text-2xl font-bold font-display text-navy-900">My Profile</h1>
      </div>

      <Card padding="lg" className="bg-gradient-to-br from-navy-900 to-navy-800 border-0 text-white flex items-center gap-4">
        <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center text-2xl font-bold font-display">
          P
        </div>
        <div>
          <p className="text-xl font-bold font-display mb-0.5">Priya</p>
          <p className="text-sm text-navy-200 mb-1">+91 98765 43210</p>
          <span className="inline-block px-2.5 py-1 bg-white/10 rounded-full text-xs font-semibold">
            Case: MH-2026-0847
          </span>
        </div>
      </Card>

      <div className="space-y-3">
        <p className="text-xs font-bold uppercase tracking-widest text-slate-400 ml-2">My Journey</p>
        <button onClick={onOpenTrends} className="w-full text-left">
          <Card padding="md" hoverable className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center text-xl">📈</div>
              <p className="text-base font-bold text-navy-900 font-display">Mental Health Trends</p>
            </div>
            <span className="text-slate-400 text-lg">→</span>
          </Card>
        </button>
      </div>

      <div className="space-y-3">
        <p className="text-xs font-bold uppercase tracking-widest text-slate-400 ml-2">Settings</p>
        
        <Card padding="md" className="space-y-1">
          <button className="w-full flex items-center justify-between py-2 active:opacity-70 transition-opacity">
            <div className="flex items-center gap-3">
              <span className="text-lg">🌐</span>
              <p className="text-sm font-semibold text-slate-700">App Language</p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-sm text-slate-500">English</span>
              <span className="text-slate-300">→</span>
            </div>
          </button>
          <div className="h-px bg-slate-100 my-1" />
          <button className="w-full flex items-center justify-between py-2 active:opacity-70 transition-opacity">
            <div className="flex items-center gap-3">
              <span className="text-lg">🔔</span>
              <p className="text-sm font-semibold text-slate-700">Notifications</p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-sm text-slate-500">On</span>
              <span className="text-slate-300">→</span>
            </div>
          </button>
          <div className="h-px bg-slate-100 my-1" />
          <button className="w-full flex items-center justify-between py-2 active:opacity-70 transition-opacity">
            <div className="flex items-center gap-3">
              <span className="text-lg">🔐</span>
              <p className="text-sm font-semibold text-slate-700">Privacy & Data</p>
            </div>
            <span className="text-slate-300">→</span>
          </button>
        </Card>
      </div>

      <button onClick={onLogout} className="mt-4 text-center text-sm font-bold text-critical-600 p-3 active:bg-critical-50 rounded-xl transition-colors">
        Log Out
      </button>

      <p className="text-center text-xs text-slate-400 mt-4">
        MindSafe App v1.0.4<br />Govt. of India
      </p>
    </div>
  );
}
