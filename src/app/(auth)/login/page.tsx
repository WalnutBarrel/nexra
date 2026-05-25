"use client";

import { useState } from "react";
import { Lock, ArrowRight, ShieldCheck, Activity } from "lucide-react";
import { AuthApi } from "@/lib/api/client";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    
    try {
      const res: any = await AuthApi.login({ email, password });
      if (res.access_token) {
        // In a real app, securely set cookie or local state here
        localStorage.setItem("token", res.access_token);
        router.push("/workspace");
      }
    } catch (err) {
      setError("Invalid intelligence credentials.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4">
      <div className="w-full max-w-md animate-in fade-in zoom-in-95 duration-500">
        
        {/* Terminal Header */}
        <div className="mb-8 flex flex-col items-center">
          <div className="w-12 h-12 bg-secondary/10 border border-border/50 rounded-lg flex items-center justify-center mb-4">
            <ShieldCheck className="w-6 h-6 text-foreground" />
          </div>
          <h1 className="text-2xl font-medium tracking-tight text-foreground">Nexra Authorization</h1>
          <p className="text-sm text-muted-foreground mt-2">Secure access to the intelligence platform.</p>
        </div>

        {/* Auth Form */}
        <div className="bg-secondary/5 border border-border/50 rounded-xl p-8">
          <form onSubmit={handleLogin} className="flex flex-col gap-6">
            
            <div className="flex flex-col gap-2">
              <label className="text-xs font-medium text-muted-foreground uppercase tracking-wider flex justify-between">
                <span>Identity Identifier</span>
              </label>
              <div className="relative">
                <input 
                  type="email"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  placeholder="analyst@nexra.com"
                  className="w-full bg-background border border-border/50 rounded-md px-4 py-2.5 text-sm focus:outline-none focus:border-accent/50 text-foreground font-mono transition-colors"
                  required
                />
              </div>
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-xs font-medium text-muted-foreground uppercase tracking-wider flex justify-between">
                <span>Passphrase</span>
                <a href="#" className="text-accent/80 hover:text-accent transition-colors">Recover</a>
              </label>
              <div className="relative">
                <Lock className="w-4 h-4 text-muted-foreground absolute left-3 top-3" />
                <input 
                  type="password"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  placeholder="••••••••••••"
                  className="w-full bg-background border border-border/50 rounded-md pl-10 pr-4 py-2.5 text-sm focus:outline-none focus:border-accent/50 text-foreground font-mono transition-colors"
                  required
                />
              </div>
            </div>

            {error && (
              <div className="text-xs text-rose-500 bg-rose-500/10 border border-rose-500/20 p-3 rounded-md text-center">
                {error}
              </div>
            )}

            <button 
              type="submit"
              disabled={loading}
              className="w-full bg-foreground text-background font-medium px-4 py-3 rounded-md hover:bg-foreground/90 disabled:opacity-50 transition-all flex items-center justify-center gap-2 mt-2"
            >
              {loading ? (
                <>
                  <Activity className="w-4 h-4 animate-spin" />
                  Authenticating...
                </>
              ) : (
                <>
                  Initialize Session <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>
        </div>

        <div className="mt-8 text-center text-xs text-muted-foreground/60 flex items-center justify-center gap-2">
           <Lock className="w-3 h-3" /> End-to-end encrypted session establishment
        </div>
      </div>
    </div>
  );
}
