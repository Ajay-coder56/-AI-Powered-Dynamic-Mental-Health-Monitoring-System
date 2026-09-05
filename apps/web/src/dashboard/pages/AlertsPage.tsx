import React, { useState } from "react";
import { Card, AlertCard, SectionHeader, Chip, StatCard, Modal, Button, RiskBadge } from "../../components/ds";
import { alerts as initialAlerts } from "../../data/sampleData";

interface AlertsPageProps {
  onSelectCase: (id: string) => void;
}

export default function AlertsPage({ onSelectCase }: AlertsPageProps) {
  const [alertList, setAlertList] = useState(initialAlerts);
  const [filterSeverity, setFilterSeverity] = useState<"all" | "critical" | "high" | "moderate" | "low">("all");
  const [filterStatus, setFilterStatus] = useState<"all" | "active" | "resolved">("active");
  const [sortOrder, setSortOrder] = useState<"newest" | "oldest">("newest");
  const [selectedAlert, setSelectedAlert] = useState<typeof initialAlerts[0] | null>(null);

  const markResolved = (id: string) => {
    setAlertList((prev) => prev.map((a) => (a.id === id ? { ...a, isResolved: true, isRead: true } : a)));
    if (selectedAlert?.id === id) setSelectedAlert(null);
  };

  const markRead = (id: string) => {
    setAlertList((prev) => prev.map((a) => (a.id === id ? { ...a, isRead: true } : a)));
  };

  const filtered = alertList
    .filter((a) => {
      const severityOk = filterSeverity === "all" || a.severity === filterSeverity;
      const statusOk =
        filterStatus === "all" ||
        (filterStatus === "active" && !a.isResolved) ||
        (filterStatus === "resolved" && a.isResolved);
      return severityOk && statusOk;
    })
    .sort((a, b) => {
      const timeA = new Date(a.triggeredAt).getTime();
      const timeB = new Date(b.triggeredAt).getTime();
      return sortOrder === "newest" ? timeB - timeA : timeA - timeB;
    });

  const stats = {
    critical: alertList.filter((a) => a.severity === "critical" && !a.isResolved).length,
    high: alertList.filter((a) => a.severity === "high" && !a.isResolved).length,
    moderate: alertList.filter((a) => a.severity === "moderate" && !a.isResolved).length,
    resolved: alertList.filter((a) => a.isResolved).length,
  };

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold font-display text-navy-900">Alerts</h1>
        <p className="text-sm text-slate-500 mt-1">
          {alertList.filter((a) => !a.isResolved).length} active alerts require attention
        </p>
      </div>

      {/* Summary stats */}
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <StatCard label="Critical" value={stats.critical} icon={<span className="text-xl">🔴</span>} color="critical" />
        <StatCard label="High Risk" value={stats.high} icon={<span className="text-xl">🟠</span>} color="orange" />
        <StatCard label="Moderate" value={stats.moderate} icon={<span className="text-xl">🟡</span>} color="risk" />
        <StatCard label="Resolved Today" value={stats.resolved} icon={<span className="text-xl">✅</span>} color="safe" />
      </div>

      {/* Filters */}
      <Card padding="md">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:flex-wrap">
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className="text-xs text-slate-400 font-semibold">Status:</span>
            {(["all", "active", "resolved"] as const).map((s) => (
              <Chip key={s} active={filterStatus === s} onClick={() => setFilterStatus(s)}>
                {s.charAt(0).toUpperCase() + s.slice(1)}
              </Chip>
            ))}
          </div>
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className="text-xs text-slate-400 font-semibold">Severity:</span>
            {(["all", "critical", "high", "moderate", "low"] as const).map((s) => (
              <Chip key={s} active={filterSeverity === s} onClick={() => setFilterSeverity(s)}>
                {s === "all" ? "All" : s.charAt(0).toUpperCase() + s.slice(1)}
              </Chip>
            ))}
          </div>
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className="text-xs text-slate-400 font-semibold">Sort:</span>
            <select
              value={sortOrder}
              onChange={(e) => setSortOrder(e.target.value as any)}
              className="text-xs font-semibold bg-slate-50 border border-slate-200 text-slate-600 rounded-lg px-2.5 py-1.5 outline-none"
            >
              <option value="newest">Newest first</option>
              <option value="oldest">Oldest first</option>
            </select>
          </div>
          {alertList.some((a) => !a.isRead && !a.isResolved) && (
            <button
              onClick={() => setAlertList((prev) => prev.map((a) => ({ ...a, isRead: true })))}
              className="text-xs text-navy-700 font-semibold hover:underline ml-auto"
            >
              Mark all read
            </button>
          )}
        </div>
      </Card>

      {/* Alert list */}
      <div className="space-y-8">
        {filtered.length === 0 ? (
          <Card padding="lg">
            <div className="py-12 text-center">
              <p className="text-3xl mb-3">✅</p>
              <p className="text-base font-semibold font-display text-slate-700">No alerts in this view</p>
              <p className="text-sm text-slate-400 mt-1">Try adjusting the filters above</p>
            </div>
          </Card>
        ) : (
          (["critical", "high", "moderate", "low"] as const).map(group => {
            const groupAlerts = filtered.filter(a => a.severity === group);
            if (groupAlerts.length === 0) return null;
            
            const titleMap = {
              critical: "Critical Alerts",
              high: "High Priority",
              moderate: "Moderate Attention",
              low: "Information"
            };
            
            return (
              <div key={group} className="space-y-4">
                <h3 className="text-xs font-bold font-display text-slate-400 uppercase tracking-widest border-b border-slate-100 pb-2">
                  {titleMap[group]} ({groupAlerts.length})
                </h3>
                {groupAlerts.map(alert => (
                  <Card key={alert.id} padding="lg" className={`border-l-[6px] ${
                    group === "critical" ? "border-l-critical-500 bg-white" : 
                    group === "high" ? "border-l-orange-500 bg-white" : 
                    group === "moderate" ? "border-l-risk-400 bg-white" : 
                    "border-l-navy-400 bg-slate-50"
                  }`}>
                    <div className="flex flex-col md:flex-row gap-5 md:items-start justify-between">
                      <div className="space-y-3 flex-1">
                        <div className="flex items-center gap-3 flex-wrap">
                           <span className="text-xs font-bold uppercase tracking-wider text-navy-700 bg-navy-50 border border-navy-100 px-2.5 py-1 rounded-lg">
                             {alert.type}
                           </span>
                           <span className="text-xs font-bold font-mono-data text-slate-600 bg-slate-100 px-2 py-1 rounded-lg">
                             Case BEN-{(alert.caseNumber.match(/\d+$/)?.[0] || '2048')}
                           </span>
                           <RiskBadge level={alert.severity} size="sm" />
                           <span className="text-xs font-semibold text-slate-400 ml-auto md:ml-0">
                             {new Date(alert.triggeredAt).toLocaleString("en-IN", {
                                month: "short", day: "numeric", hour: "2-digit", minute: "2-digit"
                             })}
                           </span>
                        </div>
                        
                        <div className="text-sm font-semibold text-slate-800 leading-snug">
                          {alert.message}
                        </div>
                        
                        {alert.aiExplanation && (
                          <div className="text-xs text-slate-600 bg-slate-50 border border-slate-100 p-2.5 rounded-xl leading-relaxed">
                            <span className="font-bold">Reasoning: </span> {alert.aiExplanation}
                          </div>
                        )}
                        
                        <div className="text-xs font-bold text-safe-700 bg-safe-50 border border-safe-100 inline-block px-3 py-1.5 rounded-lg mt-1">
                          Recommended Action: {group === 'critical' ? 'Contact counsellor immediately' : group === 'high' ? 'Review intervention plan' : 'Monitor closely'}
                        </div>
                      </div>
                      
                      <div className="flex flex-row md:flex-col gap-2 min-w-[160px] shrink-0 w-full md:w-auto mt-4 md:mt-0">
                         <Button variant="primary" size="sm" onClick={() => onSelectCase(alert.caseId)}>
                           Review case
                         </Button>
                         <Button variant="secondary" size="sm">
                           Assign intervention
                         </Button>
                         <button 
                           onClick={() => markResolved(alert.id)}
                           className="px-3 py-2 text-xs font-semibold text-slate-500 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-xl transition-colors text-center"
                         >
                           Dismiss
                         </button>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            );
          })
        )}
      </div>

      {/* Alert detail modal */}
      <Modal
        open={!!selectedAlert}
        onClose={() => setSelectedAlert(null)}
        title={`Alert: ${selectedAlert?.type}`}
        maxWidth="max-w-xl"
      >
        {selectedAlert && (
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <RiskBadge level={selectedAlert.severity} size="lg" />
              <div>
                <p className="text-sm font-bold font-display text-navy-900">{selectedAlert.victimName}</p>
                <p className="text-xs font-mono-data text-slate-500">{selectedAlert.caseNumber}</p>
              </div>
            </div>

            <Card padding="md" className="bg-slate-50 border-0">
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Alert Message</p>
              <p className="text-sm text-slate-700 leading-relaxed">{selectedAlert.message}</p>
            </Card>

            <Card padding="md" className="bg-navy-50 border-navy-100">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-base">🤖</span>
                <p className="text-xs font-semibold text-navy-700 uppercase tracking-wider">AI Explanation</p>
              </div>
              <p className="text-sm text-slate-700 leading-relaxed">{selectedAlert.aiExplanation}</p>
              <p className="text-xs text-slate-400 mt-2">Decision-support indicator · Not a clinical assessment</p>
            </Card>

            <div className="text-xs text-slate-400">
              Triggered: {new Date(selectedAlert.triggeredAt).toLocaleString("en-IN", {
                weekday: "long", day: "2-digit", month: "long", year: "numeric",
                hour: "2-digit", minute: "2-digit",
              })}
            </div>

            <div className="flex gap-2 flex-wrap">
              <Button variant="primary" size="md" onClick={() => { onSelectCase(selectedAlert.caseId); setSelectedAlert(null); }}>
                View Case →
              </Button>
              {!selectedAlert.isResolved && (
                <Button variant="secondary" size="md" onClick={() => markResolved(selectedAlert.id)}>
                  ✅ Mark Resolved
                </Button>
              )}
              <Button variant="outline" size="md" onClick={() => setSelectedAlert(null)}>
                Close
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
