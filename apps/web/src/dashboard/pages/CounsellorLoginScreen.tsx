import React, { useState } from "react";
import { Button, Card } from "../../components/ds";
import { authService } from "../../services/auth";

interface Props {
  onLogin: () => void;
}

export default function CounsellorLoginScreen({ onLogin }: Props) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [email, setEmail] = useState("dr.meera.iyer@wcd.gov.in");
  const [password, setPassword] = useState("password123");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await authService.login(email, password);
      onLogin();
    } catch (err: any) {
      console.error(err);
      if (err.response) {
        if (err.response.status === 401) {
          setError("Invalid credentials. Please check your email and password.");
        } else if (err.response.status >= 500) {
          setError("Server error. Please try again.");
        } else {
          setError(err.response.data?.detail || "Login failed. Please try again.");
        }
      } else if (err.request) {
        setError("Unable to connect to the server. Please check that the backend/API gateway is running.");
      } else {
        setError("An unexpected error occurred. Please try again.");
      }
      setLoading(false);
    }
  };

  return (
    <div className="min-h-full bg-surface flex flex-col items-center justify-center p-6 h-screen">
      <div className="w-full max-w-md">
        <div className="flex flex-col items-center text-center mb-8">
          <div className="w-16 h-16 bg-navy-600 rounded-2xl flex items-center justify-center shadow-lg mb-4">
            <span className="text-white text-3xl font-bold font-display">M</span>
          </div>
          <h1 className="text-2xl font-bold font-display text-navy-900">MindSafe Portal</h1>
          <p className="text-sm text-slate-500 mt-2">Authorized Counsellor & Case Worker Access</p>
        </div>

        <Card padding="lg" className="border-slate-200 shadow-xl shadow-slate-200/50">
          <form onSubmit={handleLogin} className="space-y-5">
            {error && (
              <div className="bg-critical-50 text-critical-700 p-3 rounded-lg text-sm text-center font-semibold">
                {error}
              </div>
            )}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Govt. Employee ID / Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm font-semibold text-navy-900 focus:outline-none focus:border-navy-500 transition-smooth"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Secure Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm font-semibold text-navy-900 focus:outline-none focus:border-navy-500 transition-smooth"
                required
              />
            </div>
            <Button
              type="submit"
              variant="primary"
              fullWidth
              size="lg"
              disabled={loading}
              className="mt-2"
            >
              {loading ? "Authenticating..." : "Access Dashboard"}
            </Button>
          </form>
          <div className="mt-6 pt-6 border-t border-slate-100 text-center">
            <p className="text-xs text-slate-400">Restricted Govt. of India System. Unauthorized access is prohibited.</p>
          </div>
        </Card>
      </div>
    </div>
  );
}
