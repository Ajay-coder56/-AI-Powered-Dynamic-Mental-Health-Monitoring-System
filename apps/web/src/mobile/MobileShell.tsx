import React, { useState } from "react";
import WelcomeScreen from "./screens/WelcomeScreen";
import LanguageScreen from "./screens/LanguageScreen";
import OTPLoginScreen from "./screens/OTPLoginScreen";
import ConsentScreen from "./screens/ConsentScreen";
import HomeScreen from "./screens/HomeScreen";
import CheckInMenuScreen from "./screens/CheckInMenuScreen";
import VoiceCheckIn from "./screens/VoiceCheckIn";
import QuestionnaireScreen from "./screens/QuestionnaireScreen";
import TrendsScreen from "./screens/TrendsScreen";
import SupportScreen from "./screens/SupportScreen";
import ProfileScreen from "./screens/ProfileScreen";
import NotificationsScreen from "./screens/NotificationsScreen";

type Tab = "home" | "checkin" | "support" | "profile";
type OverlayScreen = "voice" | "questionnaire" | "trends" | "notifications" | null;

const tabs = [
  { id: "home" as Tab, label: "Home", emoji: "🏠" },
  { id: "checkin" as Tab, label: "Check-in", emoji: "📝" },
  { id: "support" as Tab, label: "Support", emoji: "💙" },
  { id: "profile" as Tab, label: "Profile", emoji: "👤" },
];

export default function MobileShell() {
  const [onboardingStep, setOnboardingStep] = useState(0);
  const [tab, setTab] = useState<Tab>("home");
  const [overlay, setOverlay] = useState<OverlayScreen>(null);
  const [userId, setUserId] = useState<string>("11111111-1111-1111-1111-111111111111");

  // ─── Onboarding Flow ──────────────────────────────────────────────────────────
  
  if (onboardingStep === 0) return <WelcomeScreen onNext={() => setOnboardingStep(1)} />;
  if (onboardingStep === 1) return <LanguageScreen onNext={() => setOnboardingStep(2)} />;
  if (onboardingStep === 2) return <OTPLoginScreen onNext={() => setOnboardingStep(3)} />;
  if (onboardingStep === 3) return <ConsentScreen userId={userId} onNext={() => setOnboardingStep(4)} />;

  // ─── Main App Flow ────────────────────────────────────────────────────────────

  const closeOverlay = () => setOverlay(null);

  return (
    <div className="relative flex flex-col" style={{ height: "100%", maxHeight: "100%" }}>
      {/* Top Status bar (Hide if in a full-screen overlay like check-in, keep for others) */}
      {overlay !== "voice" && overlay !== "questionnaire" && (
        <>
          <div className="bg-navy-950 px-5 pt-3 pb-3 flex items-center justify-between shrink-0">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 bg-navy-700 rounded-lg flex items-center justify-center border border-navy-600">
                <span className="text-white text-xs font-bold font-display">M</span>
              </div>
              <div>
                <p className="text-white text-sm font-bold font-display leading-none">MindSafe</p>
                <p className="text-navy-400 text-[10px] uppercase tracking-wider mt-0.5">Victim App</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button onClick={() => setOverlay("notifications")} className="relative w-8 h-8 flex items-center justify-center text-white bg-navy-800 rounded-full">
                <span className="text-sm">🔔</span>
                <span className="absolute top-0 right-0 w-2.5 h-2.5 bg-critical-500 rounded-full border-2 border-navy-950" />
              </button>
            </div>
          </div>
          {/* Subtle security banner */}
          <div className="bg-safe-50 border-b border-safe-100 px-5 py-1.5 flex items-center gap-2 shrink-0">
            <span className="w-1.5 h-1.5 rounded-full bg-safe-500 animate-pulse" />
            <span className="text-[10px] font-bold text-safe-700 uppercase tracking-widest">Secure Connection</span>
          </div>
        </>
      )}

      {/* Scrollable content */}
      <div className="flex-1 overflow-y-auto bg-surface" style={{ minHeight: 0 }}>
        {overlay === "voice" ? (
          <VoiceCheckIn userId={userId} onComplete={closeOverlay} onBack={closeOverlay} />
        ) : overlay === "questionnaire" ? (
          <QuestionnaireScreen userId={userId} onComplete={closeOverlay} onBack={closeOverlay} />
        ) : overlay === "trends" ? (
          <TrendsScreen userId={userId} />
        ) : overlay === "notifications" ? (
          <NotificationsScreen onBack={closeOverlay} />
        ) : tab === "home" ? (
          <HomeScreen
            userId={userId}
            onStartCheckIn={() => setOverlay("questionnaire")}
            onStartVoice={() => setOverlay("voice")}
          />
        ) : tab === "checkin" ? (
          <CheckInMenuScreen
            onStartText={() => setOverlay("questionnaire")}
            onStartVoice={() => setOverlay("voice")}
          />
        ) : tab === "support" ? (
          <SupportScreen />
        ) : (
          <ProfileScreen 
            onOpenTrends={() => setOverlay("trends")} 
            onLogout={() => setOnboardingStep(0)} 
          />
        )}
      </div>

      {/* Bottom nav */}
      {!overlay && (
        <div className="shrink-0 bg-white border-t border-slate-100 safe-area-inset-bottom">
          <div className="flex">
            {tabs.map((t) => (
              <button
                key={t.id}
                onClick={() => setTab(t.id)}
                className={`flex-1 flex flex-col items-center py-3 gap-1 transition-smooth ${
                  tab === t.id ? "text-navy-700" : "text-slate-400 hover:text-slate-600"
                }`}
              >
                <span className="text-2xl">{t.emoji}</span>
                <span className={`text-[10px] font-bold uppercase tracking-wider ${tab === t.id ? "text-navy-700" : "text-slate-400"}`}>
                  {t.label}
                </span>
                {tab === t.id && (
                  <span className="w-5 h-1 bg-navy-700 rounded-full mt-0.5 absolute bottom-0" />
                )}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
