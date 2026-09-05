import React, { useState, useEffect } from "react";

interface Props { onNext: () => void; }

type Step = "phone" | "otp";

export default function OTPLoginScreen({ onNext }: Props) {
  const [step, setStep] = useState<Step>("phone");
  const [phone, setPhone] = useState("");
  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const [countdown, setCountdown] = useState(30);
  const [verified, setVerified] = useState(false);

  useEffect(() => {
    if (step === "otp" && countdown > 0) {
      const t = setTimeout(() => setCountdown((c) => c - 1), 1000);
      return () => clearTimeout(t);
    }
  }, [step, countdown]);

  const handleOtpChange = (i: number, val: string) => {
    if (!/^\d?$/.test(val)) return;
    const next = [...otp];
    next[i] = val;
    setOtp(next);
    // Auto-advance
    if (val && i < 5) {
      const el = document.getElementById(`otp-${i + 1}`);
      el?.focus();
    }
    // Auto-verify when all filled
    if (next.every((d) => d !== "") && next.join("") === "123456") {
      setTimeout(() => setVerified(true), 300);
    }
  };

  if (verified) {
    return (
      <div className="flex flex-col h-full bg-white items-center justify-center px-6 gap-5 animate-fade-in">
        <div className="w-20 h-20 bg-safe-100 rounded-full flex items-center justify-center">
          <span className="text-4xl">✅</span>
        </div>
        <h2 className="text-2xl font-bold font-display text-navy-900 text-center">Verified!</h2>
        <p className="text-sm text-slate-500 text-center">Your identity is confirmed securely.</p>
        <button
          onClick={onNext}
          className="w-full py-4 bg-navy-800 text-white rounded-2xl font-bold text-base font-display active:scale-95 transition-transform"
        >
          Continue →
        </button>
      </div>
    );
  }

  if (step === "otp") {
    return (
      <div className="flex flex-col h-full bg-white px-5 pt-8 pb-6">
        <button onClick={() => setStep("phone")} className="w-9 h-9 rounded-xl bg-slate-100 flex items-center justify-center text-slate-600 mb-6 shrink-0">←</button>
        <div className="mb-8 shrink-0">
          <p className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Step 2 of 3</p>
          <h1 className="text-2xl font-bold font-display text-navy-900">Enter OTP</h1>
          <p className="text-sm text-slate-500 mt-1">We sent a 6-digit code to<br /><span className="font-semibold text-navy-900">+91 {phone}</span></p>
        </div>

        {/* OTP boxes */}
        <div className="flex gap-2 justify-center mb-4 shrink-0">
          {otp.map((digit, i) => (
            <input
              key={i}
              id={`otp-${i}`}
              type="text"
              inputMode="numeric"
              maxLength={1}
              value={digit}
              onChange={(e) => handleOtpChange(i, e.target.value)}
              className={`w-12 h-14 text-center text-2xl font-bold font-display rounded-2xl border-2 outline-none transition-all ${
                digit ? "border-navy-700 bg-navy-50 text-navy-900" : "border-slate-200 text-slate-900"
              }`}
            />
          ))}
        </div>

        <p className="text-center text-xs text-slate-400 mb-6 shrink-0">
          {countdown > 0
            ? `Resend code in ${countdown}s`
            : <button className="text-navy-700 font-semibold underline" onClick={() => setCountdown(30)}>Resend OTP</button>
          }
        </p>

        <div className="bg-blue-50 border border-blue-100 rounded-2xl px-4 py-3 mb-6 shrink-0">
          <p className="text-xs text-blue-700 font-semibold">💡 Demo tip: Enter 123456 to continue</p>
        </div>

        <div className="flex-1" />
        <p className="text-xs text-center text-slate-400 shrink-0">🔒 Encrypted · Your data is safe</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-white px-5 pt-8 pb-6">
      <div className="mb-8 shrink-0">
        <p className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Step 2 of 3</p>
        <h1 className="text-2xl font-bold font-display text-navy-900">Enter your phone number</h1>
        <p className="text-sm text-slate-500 mt-1">We will send you a one-time code.</p>
      </div>

      <div className="mb-6">
        <div className="flex items-center gap-3 border-2 border-slate-200 rounded-2xl px-4 py-3.5 focus-within:border-navy-700 transition-colors">
          <span className="text-sm font-semibold text-slate-600 shrink-0">🇮🇳 +91</span>
          <div className="w-px h-5 bg-slate-200" />
          <input
            type="tel"
            inputMode="numeric"
            maxLength={10}
            placeholder="10-digit mobile number"
            value={phone}
            onChange={(e) => setPhone(e.target.value.replace(/\D/g, ""))}
            className="flex-1 text-base font-semibold text-navy-900 outline-none placeholder:text-slate-300"
          />
        </div>
      </div>

      <div className="flex-1" />

      <button
        onClick={() => phone.length === 10 && setStep("otp")}
        disabled={phone.length !== 10}
        className="w-full py-4 bg-navy-800 text-white rounded-2xl font-bold text-base font-display disabled:opacity-40 active:scale-95 transition-transform"
      >
        Send OTP →
      </button>
      <p className="text-center text-xs text-slate-400 mt-3">🔒 Your number is never shared</p>
    </div>
  );
}
