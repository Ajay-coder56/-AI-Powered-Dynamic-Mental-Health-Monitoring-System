import React, { useState, useEffect } from "react";
import { Button, Card } from "../../components/ds";
import { checkInsService } from "../../services/checkIns";
import CheckInResultScreen from "./CheckInResultScreen";

interface VoiceCheckInProps {
  userId: string;
  onComplete: () => void;
  onBack: () => void;
}

type Stage = "ready" | "recording" | "processing" | "done";

export default function VoiceCheckIn({ userId, onComplete, onBack }: VoiceCheckInProps) {
  const [stage, setStage] = useState<Stage>("ready");
  const [seconds, setSeconds] = useState(0);
  const [selectedLanguage, setSelectedLanguage] = useState("Hindi");
  const [resultData, setResultData] = useState<any>(null);

  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;
    if (stage === "recording") {
      interval = setInterval(() => setSeconds((s) => s + 1), 1000);
    }
    return () => clearInterval(interval);
  }, [stage]);

  const mediaRecorder = React.useRef<MediaRecorder | null>(null);
  const audioChunks = React.useRef<Blob[]>([]);

  // We no longer need the processing timeout because the real API call will take time
  useEffect(() => {
    // Empty the effect, we handle transition to 'done' after API resolves
  }, [stage]);

  const formatTime = (s: number) => `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;

  const languages = ["Hindi", "Tamil", "Kannada", "Bengali", "Marathi", "Telugu", "English"];

  const handleRecord = async () => {
    if (stage === "ready") {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder.current = new MediaRecorder(stream);
        audioChunks.current = [];

        mediaRecorder.current.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunks.current.push(event.data);
          }
        };

        mediaRecorder.current.onstop = async () => {
          const audioBlob = new Blob(audioChunks.current, { type: "audio/webm" });
          
          try {
            // Keep same baseline scores
            const domainScores = [
              { domain: "mood", score: 6 },
              { domain: "sleep", score: 5 },
              { domain: "safety", score: 2 },
              { domain: "social_support", score: 4 },
              { domain: "legal_anxiety", score: 6 },
            ];

            const result = await checkInsService.submitVoiceCheckIn(userId, audioBlob, domainScores, "neutral", seconds || 120);
            setResultData(result);
          } catch (err) {
            console.error("Voice check-in submission failed", err);
          } finally {
            setStage("done");
          }
        };

        mediaRecorder.current.start();
        setStage("recording");
        setSeconds(0);
      } catch (err) {
        console.error("Microphone access denied", err);
        alert("Microphone access is required for voice check-in.");
      }
    } else if (stage === "recording") {
      setStage("processing");
      if (mediaRecorder.current && mediaRecorder.current.state === "recording") {
        mediaRecorder.current.stop();
        mediaRecorder.current.stream.getTracks().forEach((track) => track.stop());
      }
    }
  };

  if (stage === "done") {
    let risk: "low" | "medium" | "high" = "low";
    let factors: string[] = [];
    
    if (resultData) {
      if (resultData.risk_level === "critical" || resultData.risk_level === "high") risk = "high";
      else if (resultData.risk_level === "moderate") risk = "medium";
      else risk = "low";
      factors = resultData.contributing_factors || [];
    } else {
      risk = "medium";
    }
    
    return <CheckInResultScreen riskLevel={risk} factors={factors} onComplete={onComplete} />;
  }

  return (
    <div className="flex flex-col min-h-full bg-white">
      {/* Header */}
      <div className="flex items-center gap-3 px-5 pt-5 pb-4">
        <button
          onClick={onBack}
          className="w-9 h-9 rounded-xl bg-slate-100 flex items-center justify-center text-slate-600 hover:bg-slate-200 transition-smooth"
        >
          ←
        </button>
        <div>
          <h2 className="text-lg font-bold font-display text-navy-900">Voice Check-in</h2>
          <p className="text-xs text-slate-500">Speak freely — your words are private</p>
        </div>
      </div>

      {/* Language selector */}
      <div className="px-5 mb-5">
        <p className="text-xs text-slate-500 font-semibold mb-2">Select language / भाषा चुनें</p>
        <div className="flex flex-wrap gap-2">
          {languages.map((lang) => (
            <button
              key={lang}
              onClick={() => setSelectedLanguage(lang)}
              className={`text-xs px-3 py-1.5 rounded-full border font-semibold transition-smooth ${
                selectedLanguage === lang
                  ? "bg-navy-700 text-white border-navy-700"
                  : "bg-white text-slate-600 border-slate-200 hover:border-navy-300"
              }`}
            >
              {lang}
            </button>
          ))}
        </div>
      </div>

      {/* Privacy notice */}
      <div className="mx-5 mb-5">
        <Card padding="sm" className="bg-navy-50 border-navy-100">
          <div className="flex items-start gap-2">
            <span className="text-base mt-0.5">🔒</span>
            <p className="text-xs text-navy-700 leading-relaxed">
              Your voice recording is <strong>encrypted and private</strong>. Only your assigned counsellor can access it. It is never shared without your consent.
            </p>
          </div>
        </Card>
      </div>

      {/* Main recording area */}
      <div className="flex-1 flex flex-col items-center justify-center px-5 gap-6">
        {stage === "ready" && (
          <>
            <div className="text-center mb-2">
              <p className="text-base font-semibold text-navy-900 font-display mb-1">
                How are you feeling today?
              </p>
              <p className="text-sm text-slate-500 leading-relaxed px-4">
                Speak in your own language. Tell us how you have been feeling, sleeping, and any worries on your mind.
              </p>
            </div>

            {/* Idle mic visual */}
            <div className="relative flex items-center justify-center">
              <div className="w-28 h-28 rounded-full bg-navy-50 border-2 border-navy-200 flex items-center justify-center">
                <span className="text-5xl">🎙️</span>
              </div>
            </div>

            <Button variant="primary" size="xl" onClick={handleRecord} className="px-10">
              Tap to Start Recording
            </Button>

            <p className="text-xs text-slate-400 text-center">
              Recommended: speak for 2–5 minutes
            </p>
          </>
        )}

        {stage === "recording" && (
          <>
            <div className="text-center mb-2">
              <p className="text-base font-semibold text-critical-700 font-display mb-1">Recording…</p>
              <p className="text-sm text-slate-500">Tap the button when you are done speaking</p>
            </div>

            {/* Pulsing mic + waveform */}
            <div className="relative flex items-center justify-center">
              <div className="absolute w-36 h-36 rounded-full bg-critical-100 animate-pulse-ring" />
              <div className="w-28 h-28 rounded-full bg-critical-50 border-2 border-critical-400 flex items-center justify-center relative z-10 shadow-lg">
                <span className="text-5xl">🎙️</span>
              </div>
            </div>

            {/* Waveform */}
            <div className="flex items-center gap-1.5 h-10">
              {Array.from({ length: 20 }).map((_, i) => (
                <div
                  key={i}
                  className={`w-1.5 rounded-full bg-critical-400 animate-wave-${(i % 5) + 1}`}
                  style={{ height: 8 + Math.random() * 20 }}
                />
              ))}
            </div>

            <div className="font-mono-data text-2xl font-bold text-navy-900">
              {formatTime(seconds)}
            </div>

            <Button variant="danger" size="xl" onClick={handleRecord} className="px-10">
              ⏹ Stop Recording
            </Button>
          </>
        )}

        {stage === "processing" && (
          <div className="flex flex-col items-center justify-center flex-1 w-full animate-fade-in -mt-10">
            {/* Soft glowing animation */}
            <div className="relative w-48 h-48 flex items-center justify-center mb-8">
              <div className="absolute w-32 h-32 bg-blue-100 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse" style={{ animationDuration: '4s' }} />
              <div className="absolute w-28 h-28 bg-emerald-100 rounded-full mix-blend-multiply filter blur-xl opacity-70 translate-x-4 animate-pulse" style={{ animationDuration: '4s', animationDelay: '1s' }} />
              <div className="absolute w-24 h-24 bg-amber-100 rounded-full mix-blend-multiply filter blur-xl opacity-70 -translate-y-4 animate-pulse" style={{ animationDuration: '4s', animationDelay: '2s' }} />
              <div className="w-16 h-16 bg-white rounded-full shadow-sm flex items-center justify-center text-3xl z-10 border border-slate-50">
                ✨
              </div>
            </div>
            
            <h2 className="text-2xl font-bold font-display text-navy-900 mb-2 text-center">
              Understanding your check-in...
            </h2>
            <p className="text-sm text-slate-500 text-center max-w-[240px]">
              This may take a few moments.
            </p>
          </div>
        )}

      </div>

      {stage === "ready" && (
        <div className="px-5 pb-6">
          <Card padding="md" className="border-slate-100">
            <p className="text-xs font-semibold text-slate-700 font-display mb-2">Prompt ideas to get started:</p>
            <ul className="text-xs text-slate-500 space-y-1">
              <li>• How have you been feeling this week?</li>
              <li>• How is your sleep and appetite?</li>
              <li>• Are there any worries about your case?</li>
              <li>• Is there anyone supporting you right now?</li>
            </ul>
          </Card>
        </div>
      )}
    </div>
  );
}
