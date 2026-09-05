import React, { useState } from "react";
import { Button, Card, ProgressBar } from "../../components/ds";
import { questions } from "../../data/sampleData";
import { checkInsService } from "../../services/checkIns";
import CheckInResultScreen from "./CheckInResultScreen";

interface QuestionnaireScreenProps {
  userId: string;
  onComplete: () => void;
  onBack: () => void;
}

export default function QuestionnaireScreen({ userId, onComplete, onBack }: QuestionnaireScreenProps) {
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [stage, setStage] = useState<"questions" | "processing" | "done">("questions");
  const [resultData, setResultData] = useState<any>(null);

  const q = questions[currentQ];
  const progress = ((currentQ + (answers[q?.id] !== undefined ? 1 : 0)) / questions.length) * 100;
  const selected = answers[q?.id];

  const handleSelect = (value: number) => {
    setAnswers((prev) => ({ ...prev, [q.id]: value }));
  };

  const handleNext = async () => {
    if (currentQ < questions.length - 1) {
      setCurrentQ((p) => p + 1);
    } else {
      setStage("processing");
      try {
        // Map 1-5 (where 5 is good) to 0-10 (where 10 is max distress)
        // Formula: distress = (5 - value) * 2.5
        const mapScore = (val: number) => Math.round((5 - val) * 2.5);
        
        const payload = {
          mode: "questionnaire",
          mood: answers["q1"] >= 3 ? "positive" : "negative",
          domain_scores: [
            { domain: "mood", score: mapScore(answers["q1"] || 3) },
            { domain: "sleep", score: mapScore(answers["q2"] || 3) },
            { domain: "safety", score: mapScore(answers["q3"] || 3) },
            { domain: "social_support", score: mapScore(answers["q4"] || 3) },
            { domain: "legal_anxiety", score: mapScore(answers["q5"] || 3) },
          ],
          duration_seconds: 120, // dummy duration
        };

        const result = await checkInsService.submitCheckIn(userId, payload);
        // We can pass the result to the Result Screen
        setResultData(result);
        setStage("done");
      } catch (err) {
        console.error("Check-in submission failed", err);
        // Fallback or error handling
        setStage("done");
      }
    }
  };

  const handleBack = () => {
    if (currentQ > 0) setCurrentQ((p) => p - 1);
    else onBack();
  };

  if (stage === "processing") {
    return (
      <div className="flex flex-col min-h-full bg-white">
        <div className="flex flex-col items-center justify-center flex-1 w-full animate-fade-in -mt-10">
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
      </div>
    );
  }

  if (stage === "done") {
    let risk: "low" | "medium" | "high" = "low";
    let factors: string[] = [];
    
    if (resultData) {
      // Map backend risk_level to frontend risk
      if (resultData.risk_level === "critical" || resultData.risk_level === "high") risk = "high";
      else if (resultData.risk_level === "moderate") risk = "medium";
      else risk = "low";
      
      factors = resultData.contributing_factors || [];
    }
    
    return <CheckInResultScreen riskLevel={risk} factors={factors} onComplete={onComplete} />;
  }

  return (
    <div className="flex flex-col min-h-full bg-white">
      {/* Header */}
      <div className="flex items-center gap-3 px-5 pt-5 pb-3">
        <button
          onClick={handleBack}
          className="w-9 h-9 rounded-xl bg-slate-100 flex items-center justify-center text-slate-600 hover:bg-slate-200 transition-smooth"
        >
          ←
        </button>
        <div className="flex-1">
          <h2 className="text-lg font-bold font-display text-navy-900">Daily Check-in</h2>
          <p className="text-xs text-slate-500">
            Question {currentQ + 1} of {questions.length}
          </p>
        </div>
      </div>

      {/* Progress */}
      <div className="px-5 mb-5">
        <ProgressBar value={progress} max={100} color="#1E3A8A" size="sm" />
      </div>

      {/* Question */}
      <div className="flex-1 flex flex-col px-5 animate-fade-in" key={currentQ}>
        {/* Step dots */}
        <div className="flex gap-2 mb-5">
          {questions.map((_, i) => (
            <div
              key={i}
              className={`h-1.5 flex-1 rounded-full transition-smooth ${
                i < currentQ ? "bg-navy-700" : i === currentQ ? "bg-navy-400" : "bg-slate-100"
              }`}
            />
          ))}
        </div>

        <div className="mb-2">
          <span className="text-xs font-semibold text-navy-500 bg-navy-50 px-2.5 py-1 rounded-full">
            Q{currentQ + 1}
          </span>
        </div>

        <h3 className="text-xl font-bold font-display text-navy-900 leading-snug mb-2">
          {q.text}
        </h3>
        <p className="text-sm text-slate-500 mb-6">{q.hint}</p>

        {/* Emoji options */}
        <div className="flex flex-col gap-3">
          {q.options.map((opt) => (
            <button
              key={opt.value}
              onClick={() => handleSelect(opt.value)}
              className={`flex items-center gap-4 p-4 rounded-2xl border-2 text-left transition-smooth ${
                selected === opt.value
                  ? "border-navy-700 bg-navy-50 shadow-sm"
                  : "border-slate-100 bg-white hover:border-navy-200 hover:bg-slate-50"
              }`}
            >
              <span className="text-3xl">{opt.emoji}</span>
              <div className="flex-1">
                <p
                  className={`text-sm font-semibold font-display ${
                    selected === opt.value ? "text-navy-900" : "text-slate-700"
                  }`}
                >
                  {opt.label}
                </p>
              </div>
              <div
                className={`w-5 h-5 rounded-full border-2 flex items-center justify-center shrink-0 ${
                  selected === opt.value
                    ? "border-navy-700 bg-navy-700"
                    : "border-slate-300"
                }`}
              >
                {selected === opt.value && (
                  <div className="w-2.5 h-2.5 rounded-full bg-white" />
                )}
              </div>
            </button>
          ))}
        </div>

        <div className="flex-1" />

        {/* Privacy note */}
        <div className="py-3">
          <p className="text-xs text-slate-400 text-center">
            🔒 Your answers are private and encrypted
          </p>
        </div>

        <Button
          variant="primary"
          size="lg"
          fullWidth
          disabled={selected === undefined}
          onClick={handleNext}
          className="mb-2"
        >
          {currentQ === questions.length - 1 ? "Submit Check-in" : "Next Question →"}
        </Button>
      </div>
    </div>
  );
}
