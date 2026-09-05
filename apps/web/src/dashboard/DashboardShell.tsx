import React, { useState, useEffect } from "react";
import OverviewPage from "./pages/OverviewPage";
import CasesPage from "./pages/CasesPage";
import CaseDetailPage from "./pages/CaseDetailPage";
import AlertsPage from "./pages/AlertsPage";
import CounsellorLoginScreen from "./pages/CounsellorLoginScreen";
import { alerts } from "../data/sampleData";
import { authService } from "../services/auth";

type Page = "overview" | "cases" | "alerts" | "case-detail";

const navItems = [
  { id: "overview" as Page, label: "Overview", emoji: "📊" },
  { id: "cases" as Page, label: "All Cases", emoji: "👥" },
  { id: "alerts" as Page, label: "Alerts", emoji: "🔔" },
];

export default function DashboardShell() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [counsellor, setCounsellor] = useState<any>(null);
  const [page, setPage] = useState<Page>("overview");
  const [selectedCaseId, setSelectedCaseId] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {
    if (isAuthenticated) {
      authService.getMe().then(setCounsellor).catch(console.error);
    }
  }, [isAuthenticated]);

  const unreadAlerts = alerts.filter((a) => !a.isRead && !a.isResolved).length;

  const goToCase = (id: string) => {
    setSelectedCaseId(id);
    setPage("case-detail");
  };

  const goToAlerts = () => setPage("alerts");

  const currentPage = page === "case-detail" && selectedCaseId
    ? <CaseDetailPage caseId={selectedCaseId} onBack={() => setPage("cases")} />
    : page === "cases"
    ? <CasesPage onSelectCase={goToCase} />
    : page === "alerts"
    ? <AlertsPage onSelectCase={goToCase} />
    : <OverviewPage onSelectCase={goToCase} onGoAlerts={goToAlerts} />;

  if (!isAuthenticated) {
    return <CounsellorLoginScreen onLogin={() => setIsAuthenticated(true)} />;
  }

  return (
    <div className="flex h-full bg-surface overflow-hidden">
      {/* Sidebar */}
      <aside
        className={`${sidebarOpen ? "w-56" : "w-16"} shrink-0 bg-navy-950 flex flex-col transition-all duration-300 overflow-hidden`}
      >
        {/* Logo */}
        <div className="flex items-center gap-3 px-4 py-5 border-b border-navy-800">
          <div className="w-8 h-8 bg-navy-600 rounded-xl flex items-center justify-center shrink-0">
            <span className="text-white text-sm font-bold font-display">M</span>
          </div>
          {sidebarOpen && (
            <div>
              <p className="text-white text-sm font-bold font-display leading-none">MindSafe</p>
              <p className="text-xs mt-0.5" style={{ color: '#AAB8D3' }}>Counsellor Portal</p>
            </div>
          )}
        </div>

        {/* Nav */}
        <nav className="flex-1 px-2 py-4 space-y-1">
          {navItems.map((item) => {
            const isActive = page === item.id || (page === "case-detail" && item.id === "cases");
            return (
              <button
                key={item.id}
                onClick={() => setPage(item.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold font-display transition-smooth relative ${
                  isActive
                    ? "bg-navy-700 text-white"
                    : "hover:bg-navy-800 hover:text-white"
                }`}
                style={!isActive ? { color: '#D6DEEF' } : undefined}
              >
                <span className="text-base shrink-0">{item.emoji}</span>
                {sidebarOpen && <span>{item.label}</span>}
                {item.id === "alerts" && unreadAlerts > 0 && (
                  <span className={`${sidebarOpen ? "ml-auto" : "absolute top-1 right-1"} bg-critical-600 text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center`}>
                    {unreadAlerts}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Bottom section */}
        <div className="border-t border-navy-800 px-2 py-3 space-y-1">
          {sidebarOpen && counsellor && (
            <div className="px-3 py-2 mb-2">
              <p className="text-xs" style={{ color: '#AAB8D3' }}>Signed in as</p>
              <p className="text-xs font-semibold text-white font-display truncate">{counsellor.name}</p>
              <p className="text-[10px] truncate" style={{ color: '#AAB8D3' }}>{counsellor.email}</p>
            </div>
          )}
          <button
            onClick={() => setSidebarOpen((p) => !p)}
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-navy-800 hover:text-white text-sm transition-smooth"
            style={{ color: '#D6DEEF' }}
          >
            <span className="text-base shrink-0">{sidebarOpen ? "◀" : "▶"}</span>
            {sidebarOpen && <span className="text-xs font-semibold">Collapse</span>}
          </button>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top bar */}
        <header className="bg-white border-b border-slate-100 px-6 py-3.5 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-safe-500" />
            <span className="text-xs text-slate-500 font-semibold">System Active</span>
            <span className="text-slate-200 mx-2">|</span>
            <span className="text-xs text-slate-400">Smart India Hackathon 2026 · MindSafe v1.0</span>
            <span className="text-slate-200 mx-2">|</span>
            <span className="text-[10px] font-bold text-amber-600 bg-amber-50 px-2 py-0.5 rounded-full uppercase tracking-wider">Mock / deferred backend integration</span>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs text-slate-400">Thu, 3 Sep 2026</span>
            <div className="flex items-center gap-1.5 bg-navy-50 border border-navy-100 text-navy-700 text-xs font-semibold px-3 py-1.5 rounded-xl">
              <span className="w-2 h-2 rounded-full bg-navy-600" />
              Govt. of India · MoWCD
            </div>
            <button className="relative w-8 h-8 rounded-lg hover:bg-slate-100 flex items-center justify-center transition-smooth">
              <span className="text-base">🔔</span>
              {unreadAlerts > 0 && (
                <span className="absolute top-0.5 right-0.5 w-4 h-4 bg-critical-600 text-white text-xs font-bold rounded-full flex items-center justify-center">
                  {unreadAlerts}
                </span>
              )}
            </button>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto p-6">
          {currentPage}
        </main>
      </div>
    </div>
  );
}
