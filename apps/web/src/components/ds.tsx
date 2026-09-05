import React from "react";
import type { RiskLevel } from "../data/sampleData";

// ─── Risk helpers ───────────────────────────────────────────────────────────

export function getRiskConfig(level: RiskLevel | string) {
  switch (level) {
    case "critical":
      return {
        label: "Critical",
        bg: "bg-critical-50",
        border: "border-critical-200",
        text: "text-critical-700",
        dot: "bg-critical-600",
        badge: "bg-critical-100 text-critical-700",
        ring: "ring-critical-200",
        hex: "#E11D48",
      };
    case "high":
      return {
        label: "High Risk",
        bg: "bg-orange-50",
        border: "border-orange-200",
        text: "text-orange-700",
        dot: "bg-orange-500",
        badge: "bg-orange-100 text-orange-700",
        ring: "ring-orange-200",
        hex: "#EA580C",
      };
    case "moderate":
      return {
        label: "Moderate",
        bg: "bg-risk-50",
        border: "border-risk-200",
        text: "text-risk-700",
        dot: "bg-risk-500",
        badge: "bg-risk-100 text-risk-700",
        ring: "ring-risk-200",
        hex: "#D97706",
      };
    case "stable":
    case "low":
      return {
        label: "Stable",
        bg: "bg-safe-50",
        border: "border-safe-200",
        text: "text-safe-700",
        dot: "bg-safe-500",
        badge: "bg-safe-100 text-safe-700",
        ring: "ring-safe-200",
        hex: "#10B981",
      };
  }
}

export function getScoreColor(score: number): string {
  if (score >= 80) return "#E11D48";
  if (score >= 60) return "#EA580C";
  if (score >= 40) return "#D97706";
  return "#16A34A";
}

// ─── RiskBadge ──────────────────────────────────────────────────────────────

interface RiskBadgeProps {
  level: RiskLevel | string;
  size?: "sm" | "md" | "lg";
  showDot?: boolean;
}

export function RiskBadge({ level, size = "md", showDot = true }: RiskBadgeProps) {
  const cfg = getRiskConfig(level);
  const sizeClasses = {
    sm: "text-xs px-2 py-0.5",
    md: "text-xs px-2.5 py-1",
    lg: "text-sm px-3 py-1.5",
  }[size];

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full font-semibold font-display ${cfg.badge} ${sizeClasses}`}>
      {showDot && <span className={`w-1.5 h-1.5 rounded-full ${cfg.dot} shrink-0`} />}
      {cfg.label}
    </span>
  );
}

// ─── Button ─────────────────────────────────────────────────────────────────

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "danger" | "outline";
  size?: "sm" | "md" | "lg" | "xl";
  fullWidth?: boolean;
  loading?: boolean;
  children: React.ReactNode;
}

export function Button({
  variant = "primary",
  size = "md",
  fullWidth = false,
  loading = false,
  children,
  className = "",
  disabled,
  ...props
}: ButtonProps) {
  const base =
    "inline-flex items-center justify-center gap-2 font-semibold font-display rounded-xl transition-smooth focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-60 disabled:cursor-not-allowed";

  const variants = {
    primary: "bg-navy-700 hover:bg-navy-800 text-white focus-visible:ring-navy-500 shadow-sm",
    secondary: "bg-navy-50 hover:bg-navy-100 text-navy-900 focus-visible:ring-navy-300",
    ghost: "hover:bg-navy-50 text-navy-700 focus-visible:ring-navy-300",
    danger: "bg-critical-600 hover:bg-critical-700 text-white focus-visible:ring-critical-400 shadow-sm",
    outline: "border border-navy-200 hover:bg-navy-50 text-navy-700 focus-visible:ring-navy-300",
  };

  const sizes = {
    sm: "text-sm px-3 py-1.5",
    md: "text-sm px-4 py-2.5",
    lg: "text-base px-5 py-3",
    xl: "text-lg px-6 py-4",
  };

  return (
    <button
      className={`${base} ${variants[variant]} ${sizes[size]} ${fullWidth ? "w-full" : ""} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <span className="w-4 h-4 rounded-full border-2 border-current border-r-transparent animate-spin" />
      ) : null}
      {children}
    </button>
  );
}

// ─── Card ────────────────────────────────────────────────────────────────────

interface CardProps {
  children: React.ReactNode;
  className?: string;
  padding?: "none" | "sm" | "md" | "lg";
  hoverable?: boolean;
  onClick?: () => void;
}

export function Card({
  children,
  className = "",
  padding = "md",
  hoverable = false,
  onClick,
}: CardProps) {
  const paddings = {
    none: "",
    sm: "p-3",
    md: "p-4",
    lg: "p-6",
  };

  return (
    <div
      onClick={onClick}
      className={`bg-white rounded-2xl border border-slate-100 shadow-sm ${paddings[padding]} ${
        hoverable ? "cursor-pointer hover:shadow-md hover:border-navy-200 transition-smooth" : ""
      } ${className}`}
    >
      {children}
    </div>
  );
}

// ─── StatCard ────────────────────────────────────────────────────────────────

interface StatCardProps {
  label: string;
  value: string | number;
  sub?: string;
  icon: React.ReactNode;
  color?: "navy" | "safe" | "risk" | "critical" | "orange";
  trend?: "up" | "down" | "neutral";
  trendValue?: string;
}

export function StatCard({ label, value, sub, icon, color = "navy", trend, trendValue }: StatCardProps) {
  const colorMap = {
    navy: { bg: "bg-navy-50", text: "text-navy-700", iconBg: "bg-navy-100" },
    safe: { bg: "bg-safe-50", text: "text-safe-700", iconBg: "bg-safe-100" },
    risk: { bg: "bg-risk-50", text: "text-risk-700", iconBg: "bg-risk-100" },
    critical: { bg: "bg-critical-50", text: "text-critical-700", iconBg: "bg-critical-100" },
    orange: { bg: "bg-orange-50", text: "text-orange-700", iconBg: "bg-orange-100" },
  };
  const c = colorMap[color];

  return (
    <Card padding="lg" className={`${c.bg} border-0`}>
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1">{label}</p>
          <p className={`text-3xl font-bold font-display ${c.text}`}>{value}</p>
          {sub && <p className="text-xs text-slate-400 mt-0.5">{sub}</p>}
          {trend && trendValue && (
            <p className={`text-xs font-medium mt-1 ${trend === "up" ? "text-critical-600" : trend === "down" ? "text-safe-600" : "text-slate-500"}`}>
              {trend === "up" ? "↑" : trend === "down" ? "↓" : "→"} {trendValue}
            </p>
          )}
        </div>
        <div className={`${c.iconBg} ${c.text} p-3 rounded-xl shrink-0`}>{icon}</div>
      </div>
    </Card>
  );
}

// ─── AlertCard ───────────────────────────────────────────────────────────────

interface AlertCardProps {
  severity: "low" | "moderate" | "high" | "critical";
  type: string;
  message: string;
  victimName: string;
  caseNumber: string;
  time: string;
  isRead: boolean;
  isResolved: boolean;
  onView?: () => void;
  onResolve?: () => void;
}

export function AlertCard({
  severity,
  type,
  message,
  victimName,
  caseNumber,
  time,
  isRead,
  isResolved,
  onView,
  onResolve,
}: AlertCardProps) {
  const cfg = getRiskConfig(severity);

  return (
    <div
      className={`rounded-2xl border p-4 ${cfg.border} ${isResolved ? "opacity-60" : ""} ${
        !isRead ? cfg.bg : "bg-white"
      } transition-smooth`}
    >
      <div className="flex items-start gap-3">
        <span className={`mt-0.5 w-2.5 h-2.5 rounded-full shrink-0 ${cfg.dot} ${!isRead && !isResolved ? "animate-pulse" : ""}`} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center flex-wrap gap-2 mb-1">
            <RiskBadge level={severity} size="sm" />
            <span className="text-xs font-semibold text-slate-700">{type}</span>
            {isResolved && (
              <span className="text-xs bg-safe-100 text-safe-700 px-2 py-0.5 rounded-full font-semibold">Resolved</span>
            )}
          </div>
          <p className="text-sm text-slate-600 leading-snug mb-2">{message}</p>
          <div className="flex items-center justify-between flex-wrap gap-2">
            <div>
              <span className="text-xs font-semibold text-navy-700">{victimName}</span>
              <span className="text-xs text-slate-400 ml-2 font-mono-data">{caseNumber}</span>
            </div>
            <span className="text-xs text-slate-400">{formatAlertTime(time)}</span>
          </div>
        </div>
      </div>
      {!isResolved && (
        <div className="flex gap-2 mt-3 ml-5">
          <button
            onClick={onView}
            className="text-xs text-navy-700 font-semibold hover:underline"
          >
            View Case →
          </button>
          <button
            onClick={onResolve}
            className="text-xs text-safe-700 font-semibold hover:underline ml-3"
          >
            Mark Resolved
          </button>
        </div>
      )}
    </div>
  );
}

function formatAlertTime(iso: string) {
  const d = new Date(iso);
  const now = new Date();
  const diff = now.getTime() - d.getTime();
  const hours = Math.floor(diff / 3600000);
  if (hours < 1) return "Just now";
  if (hours < 24) return `${hours}h ago`;
  return d.toLocaleDateString("en-IN", { day: "2-digit", month: "short" });
}

// ─── ProgressBar ─────────────────────────────────────────────────────────────

interface ProgressBarProps {
  value: number;
  max?: number;
  color?: string;
  size?: "sm" | "md";
  label?: string;
  showValue?: boolean;
}

export function ProgressBar({ value, max = 100, color, size = "md", label, showValue }: ProgressBarProps) {
  const pct = Math.min(100, (value / max) * 100);
  const autoColor = color ?? (pct >= 80 ? "#E11D48" : pct >= 60 ? "#EA580C" : pct >= 40 ? "#D97706" : "#16A34A");
  const height = size === "sm" ? "h-1.5" : "h-2.5";

  return (
    <div className="w-full">
      {(label || showValue) && (
        <div className="flex justify-between mb-1">
          {label && <span className="text-xs text-slate-500">{label}</span>}
          {showValue && <span className="text-xs font-semibold text-slate-600">{value}</span>}
        </div>
      )}
      <div className={`w-full bg-slate-100 rounded-full ${height} overflow-hidden`}>
        <div
          className={`${height} rounded-full transition-all duration-700`}
          style={{ width: `${pct}%`, backgroundColor: autoColor }}
        />
      </div>
    </div>
  );
}

// ─── RiskGauge (circular) ─────────────────────────────────────────────────────

interface RiskGaugeProps {
  score: number;
  size?: number;
  label?: string;
}

export function RiskGauge({ score, size = 120, label }: RiskGaugeProps) {
  // Scale stroke and font proportionally so small gauges (size=32) don't overflow
  const strokeWidth = Math.max(3, Math.round(size * 0.1));
  const r = (size - strokeWidth * 2) / 2;
  const circ = 2 * Math.PI * r;
  const pct = score / 100;
  const stroke = circ * (1 - pct);
  const color = getScoreColor(score);

  // Inner text: large gauge shows score + /100, small gauge shows score only (tiny font)
  const isSmall = size < 60;
  const scoreFontSize = isSmall ? Math.max(8, Math.round(size * 0.28)) : undefined;

  return (
    <div className="flex flex-col items-center gap-1">
      <div style={{ width: size, height: size }} className="relative">
        <svg width={size} height={size} className="-rotate-90">
          <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#E2E8F0" strokeWidth={strokeWidth} />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={r}
            fill="none"
            stroke={color}
            strokeWidth={strokeWidth}
            strokeDasharray={circ}
            strokeDashoffset={stroke}
            strokeLinecap="round"
            style={{ transition: "stroke-dashoffset 0.8s ease" }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span
            className={isSmall ? "font-bold font-display leading-none" : "text-2xl font-bold font-display"}
            style={{ color, ...(isSmall ? { fontSize: scoreFontSize } : {}) }}
          >
            {score}
          </span>
          {!isSmall && <span className="text-xs text-slate-400">/100</span>}
        </div>
      </div>
      {label && <span className="text-xs font-semibold text-slate-500">{label}</span>}
    </div>
  );
}

// ─── SectionHeader ────────────────────────────────────────────────────────────

interface SectionHeaderProps {
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
}

export function SectionHeader({ title, subtitle, action }: SectionHeaderProps) {
  return (
    <div className="flex items-center justify-between gap-4 mb-4">
      <div>
        <h2 className="text-base font-bold font-display" style={{ color: '#172033' }}>{title}</h2>
        {subtitle && <p className="text-xs mt-0.5" style={{ color: '#52627A' }}>{subtitle}</p>}
      </div>
      {action && <div>{action}</div>}
    </div>
  );
}

// ─── Modal ───────────────────────────────────────────────────────────────────

interface ModalProps {
  open: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  maxWidth?: string;
}

export function Modal({ open, onClose, title, children, maxWidth = "max-w-lg" }: ModalProps) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-navy-950/40 backdrop-blur-sm" />
      <div
        className={`relative bg-white rounded-2xl shadow-2xl ${maxWidth} w-full max-h-[90vh] overflow-y-auto animate-fade-in`}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between p-5 border-b border-slate-100">
          <h3 className="text-base font-bold font-display text-navy-900">{title}</h3>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg hover:bg-slate-100 flex items-center justify-center text-slate-400 hover:text-slate-600 transition-smooth"
          >
            ✕
          </button>
        </div>
        <div className="p-5">{children}</div>
      </div>
    </div>
  );
}

// ─── TrendChip ───────────────────────────────────────────────────────────────

interface TrendChipProps {
  trend: "improving" | "stable" | "declining";
}

export function TrendChip({ trend }: TrendChipProps) {
  const map = {
    improving: { label: "↓ Improving", cls: "bg-safe-100 text-safe-700" },
    stable: { label: "→ Stable", cls: "bg-slate-100 text-slate-600" },
    declining: { label: "↑ Worsening", cls: "bg-critical-100 text-critical-700" },
  };
  const { label, cls } = map[trend];
  return (
    <span className={`text-xs font-semibold px-2.5 py-1 rounded-full font-display ${cls}`}>{label}</span>
  );
}

// ─── Divider ─────────────────────────────────────────────────────────────────

export function Divider({ className = "" }: { className?: string }) {
  return <div className={`border-t border-slate-100 ${className}`} />;
}

// ─── EmptyState ──────────────────────────────────────────────────────────────

interface EmptyStateProps {
  icon: React.ReactNode;
  title: string;
  description?: string;
}

export function EmptyState({ icon, title, description }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="text-slate-300 mb-3">{icon}</div>
      <p className="font-semibold text-slate-600 font-display">{title}</p>
      {description && <p className="text-sm text-slate-400 mt-1 max-w-xs">{description}</p>}
    </div>
  );
}

// ─── Avatar ──────────────────────────────────────────────────────────────────

interface AvatarProps {
  name: string;
  size?: "sm" | "md" | "lg";
  className?: string;
}

export function Avatar({ name, size = "md", className = "" }: AvatarProps) {
  const initials = name
    .split(" ")
    .map((n) => n[0])
    .slice(0, 2)
    .join("")
    .toUpperCase();

  const sizes = { sm: "w-7 h-7 text-xs", md: "w-9 h-9 text-sm", lg: "w-11 h-11 text-base" };

  const colors = [
    "bg-navy-100 text-navy-700",
    "bg-safe-100 text-safe-700",
    "bg-risk-100 text-risk-700",
    "bg-purple-100 text-purple-700",
    "bg-teal-100 text-teal-700",
  ];
  const colorIdx = name.charCodeAt(0) % colors.length;

  return (
    <div
      className={`${sizes[size]} ${colors[colorIdx]} rounded-full flex items-center justify-center font-bold font-display shrink-0 ${className}`}
    >
      {initials}
    </div>
  );
}

// ─── Chip / Tag ──────────────────────────────────────────────────────────────

interface ChipProps {
  children: React.ReactNode;
  active?: boolean;
  onClick?: () => void;
}

export function Chip({ children, active, onClick }: ChipProps) {
  return (
    <button
      onClick={onClick}
      className={`text-xs font-semibold px-3 py-1.5 rounded-full border transition-smooth font-display ${
        active
          ? "bg-navy-700 text-white border-navy-700"
          : "bg-white text-slate-600 border-slate-200 hover:border-navy-300 hover:text-navy-700"
      }`}
    >
      {children}
    </button>
  );
}
