import React from "react";
import { Card } from "../../components/ds";

interface Props {
  riskLevel: "low" | "medium" | "high";
  factors?: string[];
  onComplete: () => void;
}

export default function CheckInResultScreen({ riskLevel, factors = [], onComplete }: Props) {
  // Mapping risk levels to supportive content
  const content = {
    low: {
      status: "Doing okay",
      color: "bg-safe-50 border-safe-200 text-safe-700",
      icon: "🌿",
      message: "You appear to be managing fairly well right now. Keep up your healthy routines.",
      showEmergency: false,
    },
    medium: {
      status: "Needs attention",
      color: "bg-amber-50 border-amber-200 text-amber-700",
      icon: "🌤️",
      message: "Your recent responses suggest you may benefit from some extra support. Consider taking time for yourself.",
      showEmergency: false,
    },
    high: {
      status: "High concern",
      color: "bg-critical-50 border-critical-200 text-critical-700",
      icon: "🫂",
      message: "It sounds like you are going through a very tough time. Would you like to talk to someone now?",
      showEmergency: true,
    }
  };

  const current = content[riskLevel];

  // Default factors if none provided
  const displayFactors = factors.length > 0 ? factors : [
    "Your sleep quality over the last few days",
    "Current stress related to your legal case",
    "Your reported feelings of support from family"
  ];

  return (
    <div className="flex flex-col min-h-full bg-slate-50 px-5 pt-8 pb-8">
      {/* Header */}
      <div className="flex flex-col items-center justify-center mb-8">
        <div className="w-20 h-20 bg-white rounded-full shadow-sm flex items-center justify-center text-4xl mb-4 border border-slate-100">
          ✅
        </div>
        <h1 className="text-2xl font-bold font-display text-navy-900 text-center">
          Your check-in is complete
        </h1>
        <p className="text-sm text-slate-500 text-center mt-2 px-4 leading-relaxed">
          Thank you for taking the time to share how you're feeling today.
        </p>
      </div>

      <div className="space-y-4 flex-1">
        {/* Status Card */}
        <Card padding="lg" className={`${current.color} shadow-sm relative overflow-hidden`}>
          <div className="absolute top-0 right-0 w-24 h-24 bg-white/40 rounded-full filter blur-xl -translate-y-1/2 translate-x-1/2" />
          <div className="flex items-center gap-3 mb-3 relative z-10">
            <span className="text-2xl">{current.icon}</span>
            <p className="font-bold font-display text-lg tracking-tight">
              {current.status}
            </p>
          </div>
          <p className="text-sm font-medium leading-relaxed relative z-10">
            {current.message}
          </p>
        </Card>

        {/* Disclaimer */}
        <p className="text-xs text-slate-400 text-center px-4">
          Note: This is a supportive summary, not a medical or psychological diagnosis.
        </p>

        {/* High Risk Override Area */}
        {current.showEmergency && (
          <button className="w-full text-left active:scale-98 transition-transform">
            <Card padding="md" className="bg-critical-600 border-0 text-white shadow-lg shadow-critical-500/30">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center text-2xl shrink-0">
                  🆘
                </div>
                <div>
                  <p className="text-base font-bold font-display">24/7 Emergency Support</p>
                  <p className="text-xs text-critical-100">Tap to call helpline immediately</p>
                </div>
              </div>
            </Card>
          </button>
        )}

        {/* What influenced this result? */}
        <div className="pt-2">
          <p className="text-sm font-bold text-navy-900 mb-3 px-1">What influenced this result?</p>
          <Card padding="md" className="bg-white border-slate-200">
            <ul className="space-y-3">
              {displayFactors.map((f, i) => (
                <li key={i} className="flex items-start gap-3">
                  <span className="text-slate-300 text-xs mt-0.5">●</span>
                  <p className="text-sm text-slate-600 leading-snug">{f}</p>
                </li>
              ))}
            </ul>
          </Card>
        </div>

        {/* Recommended Support */}
        <div className="pt-2">
          <p className="text-sm font-bold text-navy-900 mb-3 px-1">Recommended support</p>
          <button className="w-full text-left active:scale-98 transition-transform mb-3">
            <Card padding="md" className="bg-navy-50 border-navy-100 hover:bg-navy-100 transition-colors">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-navy-700 rounded-xl flex items-center justify-center text-white font-bold shrink-0">
                  MI
                </div>
                <div className="flex-1">
                  <p className="text-base font-bold font-display text-navy-900">Talk to a counsellor</p>
                  <p className="text-xs text-slate-600">Send a message to Dr. Meera</p>
                </div>
                <span className="text-slate-400">→</span>
              </div>
            </Card>
          </button>
          
          <button className="w-full text-left active:scale-98 transition-transform">
            <Card padding="md" className="bg-white border-slate-200 hover:bg-slate-50 transition-colors">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-slate-100 rounded-xl flex items-center justify-center text-xl shrink-0">
                  🧘
                </div>
                <div className="flex-1">
                  <p className="text-base font-bold font-display text-navy-900">Relaxation Exercises</p>
                  <p className="text-xs text-slate-600">Simple breathing guides</p>
                </div>
                <span className="text-slate-400">→</span>
              </div>
            </Card>
          </button>
        </div>
      </div>

      <div className="pt-8 pb-2">
        <button
          onClick={onComplete}
          className="w-full py-4 bg-navy-800 text-white rounded-2xl font-bold text-lg font-display shadow-lg shadow-navy-900/20 active:scale-95 transition-transform"
        >
          Back to Home
        </button>
        <p className="text-center text-xs text-slate-500 mt-4 font-medium">
          Complete another check-in later
        </p>
      </div>
    </div>
  );
}
