import React, { useState } from "react";
import { Card, Button, Modal, SectionHeader } from "../../components/ds";

export default function SupportScreen() {
  const [showEmergency, setShowEmergency] = useState(false);
  const [showContact, setShowContact] = useState(false);

  const resources = [
    {
      emoji: "📞",
      title: "National Crisis Helpline",
      subtitle: "iCall · 24/7 · Free",
      number: "9152987821",
      color: "bg-critical-50 border-critical-100",
    },
    {
      emoji: "🌸",
      title: "Women's Helpline",
      subtitle: "Ministry of WCD · 24/7",
      number: "181",
      color: "bg-navy-50 border-navy-100",
    },
    {
      emoji: "🆘",
      title: "Police Emergency",
      subtitle: "If you are in immediate danger",
      number: "112",
      color: "bg-critical-50 border-critical-100",
    },
    {
      emoji: "⚖️",
      title: "Legal Aid Helpline",
      subtitle: "NALSA · Free Legal Aid",
      number: "15100",
      color: "bg-safe-50 border-safe-100",
    },
  ];

  const articles = [
    { emoji: "🧘", title: "Simple Breathing Exercises", time: "3 min read" },
    { emoji: "😴", title: "Improving Sleep During Stressful Times", time: "5 min read" },
    { emoji: "🤝", title: "Talking to Someone You Trust", time: "4 min read" },
    { emoji: "⚖️", title: "Understanding Your Legal Rights", time: "6 min read" },
    { emoji: "💪", title: "Building Resilience Day by Day", time: "4 min read" },
  ];

  return (
    <div className="flex flex-col gap-4 pb-6">
      {/* Header */}
      <div className="px-5 pt-5">
        <h1 className="text-2xl font-bold font-display text-navy-900">Support & Help</h1>
        <p className="text-sm text-slate-500 mt-1">You are not alone. Help is always available.</p>
      </div>

      {/* Emergency CTA */}
      <div className="px-5">
        <button
          onClick={() => setShowEmergency(true)}
          className="w-full bg-critical-600 hover:bg-critical-700 text-white rounded-2xl p-5 flex items-center gap-4 transition-smooth shadow-lg shadow-critical-200/50"
        >
          <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center text-2xl shrink-0">
            🆘
          </div>
          <div className="text-left">
            <p className="text-lg font-bold font-display">Emergency Help</p>
            <p className="text-sm text-critical-100">Tap if you need immediate assistance</p>
          </div>
          <span className="ml-auto text-2xl">→</span>
        </button>
      </div>

      {/* Counsellor card */}
      <div className="px-5">
        <Card padding="md" className="bg-navy-50 border-navy-100">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-12 h-12 bg-navy-700 rounded-xl flex items-center justify-center text-white font-bold font-display text-lg">
              MI
            </div>
            <div>
              <p className="text-sm font-bold font-display text-navy-900">Dr. Meera Iyer</p>
              <p className="text-xs text-slate-500">Your Assigned Counsellor</p>
              <div className="flex items-center gap-1.5 mt-0.5">
                <span className="w-2 h-2 rounded-full bg-safe-500" />
                <span className="text-xs text-safe-700 font-semibold">Available today</span>
              </div>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="primary" size="md" className="flex-1" onClick={() => setShowContact(true)}>
              📞 Call Now
            </Button>
            <Button variant="secondary" size="md" className="flex-1">
              💬 Message
            </Button>
          </div>
          <p className="text-xs text-slate-400 mt-2 text-center">
            Next scheduled session: Fri, Sep 6 at 11:00 AM
          </p>
        </Card>
      </div>

      {/* Crisis resources */}
      <div className="px-5">
        <SectionHeader title="Crisis Resources" subtitle="Free and confidential helplines" />
        <div className="space-y-2">
          {resources.map((r) => (
            <Card key={r.number} padding="md" className={r.color} hoverable>
              <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{r.emoji}</span>
                  <div>
                    <p className="text-sm font-semibold text-navy-900 font-display">{r.title}</p>
                    <p className="text-xs text-slate-500">{r.subtitle}</p>
                  </div>
                </div>
                <a
                  href={`tel:${r.number}`}
                  className="shrink-0 font-mono-data text-sm font-bold text-navy-700 bg-white px-3 py-1.5 rounded-xl border border-navy-100 hover:bg-navy-700 hover:text-white transition-smooth"
                >
                  {r.number}
                </a>
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* Self-help */}
      <div className="px-5">
        <SectionHeader title="Self-care Resources" subtitle="Articles and exercises to help you" />
        <div className="space-y-2">
          {articles.map((a) => (
            <Card key={a.title} padding="md" hoverable className="hover:bg-slate-50">
              <div className="flex items-center gap-3">
                <span className="text-xl">{a.emoji}</span>
                <div className="flex-1">
                  <p className="text-sm font-semibold text-navy-900 font-display">{a.title}</p>
                  <p className="text-xs text-slate-400">{a.time}</p>
                </div>
                <span className="text-slate-300 text-lg">→</span>
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* Case info */}
      <div className="px-5">
        <Card padding="md" className="border-slate-100 bg-slate-50">
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Your Case</p>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-xs text-slate-500">Case Number</span>
              <span className="text-xs font-mono-data font-semibold text-navy-700">DV/MH/2024/0847</span>
            </div>
            <div className="flex justify-between">
              <span className="text-xs text-slate-500">Court</span>
              <span className="text-xs font-semibold text-navy-900">Family Court, Mumbai</span>
            </div>
            <div className="flex justify-between">
              <span className="text-xs text-slate-500">Next Hearing</span>
              <span className="text-xs font-semibold text-risk-700">Sep 18, 2026</span>
            </div>
          </div>
          <button className="text-xs text-navy-700 font-semibold mt-3 hover:underline">
            View full case details →
          </button>
        </Card>
      </div>

      {/* Privacy note */}
      <div className="px-5">
        <Card padding="md" className="bg-navy-950 border-0 text-white">
          <div className="flex items-start gap-3">
            <span className="text-xl mt-0.5">🔐</span>
            <div>
              <p className="text-sm font-bold font-display mb-1">Your Privacy is Protected</p>
              <p className="text-xs text-navy-300 leading-relaxed">
                All your check-in data, voice recordings, and personal information are encrypted and stored securely. Only your assigned counsellor can access your records. Your data is never sold or shared without your explicit consent.
              </p>
            </div>
          </div>
        </Card>
      </div>

      {/* Emergency Modal */}
      <Modal open={showEmergency} onClose={() => setShowEmergency(false)} title="🆘 Emergency Help">
        <div className="space-y-3">
          <Card padding="md" className="bg-critical-50 border-critical-200">
            <p className="text-sm font-semibold text-critical-800 mb-1">If you are in immediate danger:</p>
            <a href="tel:112" className="flex items-center justify-between">
              <span className="text-base font-bold text-critical-700">Police Emergency</span>
              <span className="font-mono-data text-xl font-bold text-critical-700 bg-critical-100 px-3 py-1.5 rounded-xl">112</span>
            </a>
          </Card>
          {resources.map((r) => (
            <a key={r.number} href={`tel:${r.number}`} className="flex items-center justify-between p-3 rounded-xl bg-slate-50 hover:bg-slate-100 transition-smooth">
              <div className="flex items-center gap-2">
                <span className="text-lg">{r.emoji}</span>
                <div>
                  <p className="text-sm font-semibold text-navy-900">{r.title}</p>
                  <p className="text-xs text-slate-500">{r.subtitle}</p>
                </div>
              </div>
              <span className="font-mono-data text-sm font-bold text-navy-700">{r.number}</span>
            </a>
          ))}
          <Button variant="outline" fullWidth size="md" onClick={() => setShowEmergency(false)}>
            Close
          </Button>
        </div>
      </Modal>

      {/* Contact Modal */}
      <Modal open={showContact} onClose={() => setShowContact(false)} title="Contact Your Counsellor">
        <div className="space-y-4">
          <div className="flex items-center gap-3 p-4 bg-navy-50 rounded-xl">
            <div className="w-12 h-12 bg-navy-700 rounded-xl flex items-center justify-center text-white font-bold">MI</div>
            <div>
              <p className="font-bold font-display text-navy-900">Dr. Meera Iyer</p>
              <p className="text-xs text-slate-500">Clinical Psychologist · Mumbai</p>
            </div>
          </div>
          <p className="text-sm text-slate-600">Choose how you would like to reach out:</p>
          <div className="space-y-2">
            <a href="tel:+912212345678" className="flex items-center gap-3 p-3 bg-safe-50 rounded-xl hover:bg-safe-100 transition-smooth">
              <span className="text-xl">📞</span>
              <div>
                <p className="text-sm font-semibold text-navy-900">Call Directly</p>
                <p className="text-xs text-slate-500">Mon–Fri, 9 AM – 6 PM</p>
              </div>
            </a>
            <button className="w-full flex items-center gap-3 p-3 bg-slate-50 rounded-xl hover:bg-slate-100 transition-smooth text-left">
              <span className="text-xl">💬</span>
              <div>
                <p className="text-sm font-semibold text-navy-900">Send a Message</p>
                <p className="text-xs text-slate-500">Response within 2 hours</p>
              </div>
            </button>
            <button className="w-full flex items-center gap-3 p-3 bg-slate-50 rounded-xl hover:bg-slate-100 transition-smooth text-left">
              <span className="text-xl">📅</span>
              <div>
                <p className="text-sm font-semibold text-navy-900">Book a Session</p>
                <p className="text-xs text-slate-500">Next available: Sep 6, 11:00 AM</p>
              </div>
            </button>
          </div>
          <Button variant="outline" fullWidth onClick={() => setShowContact(false)}>Close</Button>
        </div>
      </Modal>
    </div>
  );
}
