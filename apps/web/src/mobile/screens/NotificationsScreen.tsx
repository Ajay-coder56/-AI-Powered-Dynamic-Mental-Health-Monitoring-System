import React from "react";
import { Card } from "../../components/ds";

interface Props {
  onBack: () => void;
}

export default function NotificationsScreen({ onBack }: Props) {
  const notifications = [
    {
      id: 1,
      icon: "📅",
      title: "Hearing Reminder",
      message: "Your next court hearing is in 7 days (Sep 18).",
      time: "2 hours ago",
      color: "bg-risk-50 border-risk-100",
      read: false,
    },
    {
      id: 2,
      icon: "💬",
      title: "Message from Dr. Meera",
      message: "Hello Priya, just checking in. Are we still on for Friday?",
      time: "Yesterday",
      color: "bg-navy-50 border-navy-100",
      read: true,
    },
    {
      id: 3,
      icon: "✅",
      title: "Check-in Complete",
      message: "Your weekly summary is ready to view in Trends.",
      time: "Mon, Sep 2",
      color: "bg-safe-50 border-safe-100",
      read: true,
    }
  ];

  return (
    <div className="flex flex-col min-h-full bg-white">
      {/* Header */}
      <div className="flex items-center gap-3 px-5 pt-5 pb-4 border-b border-slate-100">
        <button
          onClick={onBack}
          className="w-9 h-9 rounded-xl bg-slate-100 flex items-center justify-center text-slate-600 hover:bg-slate-200 transition-smooth"
        >
          ←
        </button>
        <h2 className="text-lg font-bold font-display text-navy-900">Notifications</h2>
      </div>

      <div className="flex-1 overflow-y-auto px-5 py-4 space-y-3 bg-surface">
        {notifications.map((n) => (
          <Card key={n.id} padding="md" className={`${n.color} relative overflow-hidden`}>
            {!n.read && (
              <div className="absolute top-3 right-3 w-2.5 h-2.5 bg-critical-500 rounded-full" />
            )}
            <div className="flex gap-3">
              <span className="text-2xl mt-1">{n.icon}</span>
              <div>
                <p className="text-sm font-bold text-navy-900 mb-1 pr-4">{n.title}</p>
                <p className="text-xs text-slate-600 leading-relaxed mb-2">{n.message}</p>
                <p className="text-xs text-slate-400 font-semibold">{n.time}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
