import React, { useState } from "react";
import { usersService } from "../../services/users";

interface Props { 
  userId: string;
  onNext: () => void; 
}

export default function ConsentScreen({ userId, onNext }: Props) {
  const [agreed, setAgreed] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    try {
      await usersService.submitConsent(userId);
      onNext();
    } catch (err: any) {
      console.error(err);
      setError("Failed to record consent. Please try again.");
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white px-5 pt-8 pb-6">
      <div className="mb-6 shrink-0">
        <p className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Step 3 of 3</p>
        <h1 className="text-2xl font-bold font-display text-navy-900">Your Privacy Matters</h1>
        <p className="text-sm text-slate-500 mt-1">Please read how we protect your data.</p>
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 pb-6">
        <div className="bg-safe-50 border border-safe-100 rounded-2xl p-4">
          <div className="flex gap-3">
            <span className="text-xl">🔐</span>
            <div>
              <p className="text-sm font-bold text-navy-900 mb-1">100% Private & Encrypted</p>
              <p className="text-xs text-slate-600 leading-relaxed">
                Your check-ins, voice notes, and wellbeing scores are encrypted. No one can see them except you and your assigned counsellor.
              </p>
            </div>
          </div>
        </div>

        <div className="bg-navy-50 border border-navy-100 rounded-2xl p-4">
          <div className="flex gap-3">
            <span className="text-xl">👩‍⚕️</span>
            <div>
              <p className="text-sm font-bold text-navy-900 mb-1">Shared with your Counsellor</p>
              <p className="text-xs text-slate-600 leading-relaxed">
                Your designated counsellor will review your check-ins to provide you with the best possible support and guidance.
              </p>
            </div>
          </div>
        </div>

        <div className="bg-slate-50 border border-slate-100 rounded-2xl p-4">
          <div className="flex gap-3">
            <span className="text-xl">🚫</span>
            <div>
              <p className="text-sm font-bold text-navy-900 mb-1">Never Sold or Shared</p>
              <p className="text-xs text-slate-600 leading-relaxed">
                We will never sell your data to third parties, nor share it with law enforcement without a direct court order.
              </p>
            </div>
          </div>
        </div>

        <div className="bg-critical-50 border border-critical-100 rounded-2xl p-4">
          <div className="flex gap-3">
            <span className="text-xl">🆘</span>
            <div>
              <p className="text-sm font-bold text-navy-900 mb-1">Emergency Intervention</p>
              <p className="text-xs text-slate-600 leading-relaxed">
                If our system detects that you are in immediate life-threatening danger, your counsellor may contact emergency services to protect you.
              </p>
            </div>
          </div>
        </div>

        {error && (
          <div className="bg-critical-50 text-critical-700 p-3 rounded-lg text-sm text-center font-semibold">
            {error}
          </div>
        )}

        <label className="flex items-start gap-3 p-4 border-2 border-slate-200 rounded-2xl mt-4 cursor-pointer hover:bg-slate-50 transition-colors">
          <input
            type="checkbox"
            className="mt-1 w-5 h-5 rounded text-navy-700 focus:ring-navy-700"
            checked={agreed}
            onChange={(e) => setAgreed(e.target.checked)}
          />
          <span className="text-sm font-semibold text-navy-900">
            I understand and agree to the privacy policy and terms of service.
          </span>
        </label>
      </div>

      <button
        onClick={handleSubmit}
        disabled={!agreed || loading}
        className="w-full py-4 bg-navy-800 text-white rounded-2xl font-bold text-base font-display disabled:opacity-40 active:scale-95 transition-transform"
      >
        {loading ? "Recording Consent..." : "Complete Setup →"}
      </button>
    </div>
  );
}
