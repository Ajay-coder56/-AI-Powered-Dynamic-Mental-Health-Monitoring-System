import React from "react";

interface Props { onNext: () => void; }

export default function WelcomeScreen({ onNext }: Props) {
  return (
    <div className="flex flex-col h-full bg-slate-50 px-6 pt-10 pb-8">
      
      {/* Top Bar: Language Indicator */}
      <div className="flex justify-end shrink-0 mb-8">
        <button className="flex items-center gap-1.5 bg-white border border-slate-200 px-3 py-1.5 rounded-full text-xs font-semibold text-slate-600 shadow-sm hover:bg-slate-50 transition-smooth">
          <span>🌐</span> English / हिंदी
        </button>
      </div>

      <div className="flex-1 flex flex-col justify-center items-center -mt-10">
        {/* Soft, Human-centered Illustration */}
        <div className="relative w-40 h-40 flex items-center justify-center mb-10">
          <div className="absolute w-32 h-32 bg-blue-100 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse" style={{ animationDuration: '4s' }} />
          <div className="absolute w-28 h-28 bg-amber-100 rounded-full mix-blend-multiply filter blur-xl opacity-70 translate-x-6 -translate-y-4" />
          <div className="w-24 h-24 bg-white rounded-full shadow-sm flex items-center justify-center text-5xl z-10 border border-slate-100 text-slate-700">
            🫂
          </div>
        </div>

        {/* Messaging */}
        <div className="text-center px-2 mb-10">
          <h1 className="text-3xl font-bold font-display text-navy-900 mb-3 tracking-tight">
            Your well-being matters.
          </h1>
          <p className="text-base text-slate-600 leading-relaxed max-w-[280px] mx-auto">
            Regular check-ins can help you get support when you need it.
          </p>
        </div>
      </div>

      {/* Action Area */}
      <div className="shrink-0 space-y-4">
        {/* Privacy reassurance */}
        <div className="flex items-center justify-center gap-2 mb-2">
          <span className="text-safe-600 text-sm">🔒</span>
          <p className="text-xs font-semibold text-slate-500">100% Private & Secure</p>
        </div>

        {/* CTAs */}
        <button
          onClick={onNext}
          className="w-full py-4 bg-navy-800 text-white rounded-2xl font-bold text-lg font-display shadow-lg shadow-navy-900/20 active:scale-95 transition-transform"
        >
          Get Started
        </button>
        
        <button
          onClick={onNext}
          className="w-full py-4 bg-transparent text-navy-700 rounded-2xl font-bold text-base font-display active:bg-slate-100 transition-colors"
        >
          I already have an account
        </button>
      </div>
    </div>
  );
}
