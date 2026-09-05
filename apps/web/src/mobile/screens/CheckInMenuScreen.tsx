import React from "react";
import { Card } from "../../components/ds";

interface Props {
  onStartText: () => void;
  onStartVoice: () => void;
}

export default function CheckInMenuScreen({ onStartText, onStartVoice }: Props) {
  return (
    <div className="flex flex-col gap-6 px-5 pt-6 pb-8">
      <div>
        <h1 className="text-2xl font-bold font-display text-navy-900">Daily Check-in</h1>
        <p className="text-sm text-slate-500 mt-1">
          Take a few minutes to share how you're feeling today.
        </p>
      </div>

      <div className="space-y-4">
        <button onClick={onStartVoice} className="w-full text-left active:scale-98 transition-transform">
          <Card padding="lg" className="bg-navy-700 border-0 text-white hover:bg-navy-800 transition-colors">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-white/20 rounded-2xl flex items-center justify-center shrink-0">
                <span className="text-3xl">🎙️</span>
              </div>
              <div>
                <p className="text-lg font-bold font-display mb-1">Voice Check-in</p>
                <p className="text-xs text-navy-200 leading-relaxed">
                  Speak naturally in your own language. Fast and easy.
                </p>
              </div>
            </div>
            <div className="mt-4 flex items-center justify-between">
              <span className="text-xs font-semibold bg-white/10 px-3 py-1.5 rounded-full">~3 mins</span>
              <span className="font-bold">Start →</span>
            </div>
          </Card>
        </button>

        <button onClick={onStartText} className="w-full text-left active:scale-98 transition-transform">
          <Card padding="lg" className="bg-white border-2 border-slate-100 hover:border-navy-200 transition-colors">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-navy-50 text-navy-700 rounded-2xl flex items-center justify-center shrink-0">
                <span className="text-3xl">📝</span>
              </div>
              <div>
                <p className="text-lg font-bold font-display text-navy-900 mb-1">Text Questionnaire</p>
                <p className="text-xs text-slate-500 leading-relaxed">
                  Answer a few simple questions by tapping emojis.
                </p>
              </div>
            </div>
            <div className="mt-4 flex items-center justify-between text-navy-700">
              <span className="text-xs font-semibold bg-slate-50 px-3 py-1.5 rounded-full">~5 mins</span>
              <span className="font-bold">Start →</span>
            </div>
          </Card>
        </button>
      </div>

      <div className="mt-4">
        <Card padding="md" className="bg-safe-50 border-safe-100">
          <div className="flex items-start gap-3">
            <span className="text-lg mt-0.5">💡</span>
            <p className="text-xs text-safe-800 leading-relaxed">
              <strong>Why check in?</strong> Regular check-ins help your counsellor understand your situation better and provide you with the right support at the right time.
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
}
