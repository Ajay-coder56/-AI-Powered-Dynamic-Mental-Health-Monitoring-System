import React, { useState } from "react";

interface Props { onNext: () => void; }

const LANGUAGES = [
  { code: "en", name: "English", english: "English" },
  { code: "hi", name: "हिंदी", english: "Hindi" },
  { code: "mr", name: "मराठी", english: "Marathi" },
  { code: "bn", name: "বাংলা", english: "Bengali" },
  { code: "ta", name: "தமிழ்", english: "Tamil" },
  { code: "te", name: "తెలుగు", english: "Telugu" },
];

export default function LanguageScreen({ onNext }: Props) {
  const [selected, setSelected] = useState("hi");
  const [search, setSearch] = useState("");
  const [playing, setPlaying] = useState<string | null>(null);

  const filteredLanguages = LANGUAGES.filter(lang => 
    lang.name.toLowerCase().includes(search.toLowerCase()) || 
    lang.english.toLowerCase().includes(search.toLowerCase())
  );

  const handlePlayAudio = (e: React.MouseEvent, code: string) => {
    e.stopPropagation(); // Prevent card selection
    setPlaying(code);
    setTimeout(() => setPlaying(null), 1500); // Mock playing state
  };

  return (
    <div className="flex flex-col h-full bg-slate-50 px-5 pt-8 pb-6">
      
      {/* Header */}
      <div className="mb-5 shrink-0">
        <h1 className="text-3xl font-bold font-display text-navy-900 leading-tight">Choose your language</h1>
        <p className="text-base text-slate-500 mt-2">अपनी भाषा चुनें</p>
      </div>

      {/* Search Bar */}
      <div className="relative mb-5 shrink-0">
        <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-xl">🔍</span>
        <input 
          type="text" 
          placeholder="Search language..." 
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full bg-white border-2 border-slate-200 rounded-2xl py-4 pl-12 pr-4 text-lg font-semibold outline-none focus:border-navy-700 transition-colors shadow-sm placeholder:text-slate-300"
        />
      </div>

      {/* Language List */}
      <div className="flex flex-col gap-3 flex-1 overflow-y-auto pb-4 px-1">
        {filteredLanguages.map((lang) => (
          <button
            key={lang.code}
            onClick={() => setSelected(lang.code)}
            className={`w-full flex items-center p-4 rounded-2xl border-2 text-left transition-all active:scale-[0.98] ${
              selected === lang.code
                ? "border-navy-700 bg-white shadow-md shadow-navy-900/5 ring-1 ring-navy-700"
                : "border-slate-200 bg-white hover:border-slate-300 shadow-sm"
            }`}
          >
            {/* Language Text */}
            <div className="flex-1">
              <p className={`text-2xl font-bold font-display mb-1 ${selected === lang.code ? "text-navy-900" : "text-slate-700"}`}>
                {lang.name}
              </p>
              <p className="text-sm font-medium text-slate-500">{lang.english}</p>
            </div>
            
            {/* Audio Preview Icon */}
            <div 
              onClick={(e) => handlePlayAudio(e, lang.code)}
              className={`w-12 h-12 rounded-full flex items-center justify-center mr-4 transition-colors shrink-0 ${
                playing === lang.code ? "bg-navy-100 text-navy-700" : "bg-slate-100 text-slate-600 hover:bg-slate-200"
              }`}
            >
              <span className="text-2xl">{playing === lang.code ? "🔉" : "🔊"}</span>
            </div>

            {/* Radio Indicator */}
            <div className={`w-8 h-8 rounded-full border-2 flex items-center justify-center shrink-0 ${
              selected === lang.code ? "border-navy-700 bg-navy-700" : "border-slate-300 bg-slate-50"
            }`}>
              {selected === lang.code && <div className="w-3 h-3 rounded-full bg-white" />}
            </div>
          </button>
        ))}
      </div>

      {/* Footer / Continue CTA */}
      <div className="shrink-0 pt-2">
        <button
          onClick={onNext}
          className="w-full py-4 bg-navy-800 text-white rounded-2xl font-bold text-xl font-display shadow-lg shadow-navy-900/20 active:scale-95 transition-transform flex items-center justify-center gap-2"
        >
          Continue <span>→</span>
        </button>
      </div>
    </div>
  );
}
