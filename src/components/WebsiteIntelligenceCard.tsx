import { Globe, Lock, Activity, ShieldAlert, CheckCircle2, Server, Clock, Database, Globe2, ShieldCheck } from "lucide-react";
import { useState, useEffect } from "react";

interface WebsiteIntelligenceCardProps {
  domain: string;
  narrative?: string;
  telemetry?: {
    latency_ms: number;
    status: number;
    ssl_issuer: string;
    scan_duration_ms: number;
    redirect_depth: number;
    tls_status: string;
  };
  technologies: any[];
  seo_intelligence?: any;
  security_intelligence?: any;
  performance_intelligence?: any;
  confidence_score?: number;
}

export function WebsiteIntelligenceCard({
  domain,
  narrative,
  telemetry,
  technologies,
  seo_intelligence,
  security_intelligence,
  performance_intelligence,
  confidence_score,
}: WebsiteIntelligenceCardProps) {
  const [isAnalyzing, setIsAnalyzing] = useState(true);
  const [phase, setPhase] = useState("Analyzing SEO structure...");

  useEffect(() => {
    if (!isAnalyzing) return;
    const phases = [
      "Analyzing SEO structure...",
      "Performance telemetry pending...",
      "Social reference extraction active...",
      "Awaiting infrastructure metrics...",
    ];
    let idx = 0;
    const interval = setInterval(() => {
      idx++;
      if (idx < phases.length) {
        setPhase(phases[idx]);
      } else {
        clearInterval(interval);
        setIsAnalyzing(false);
      }
    }, 400);

    return () => clearInterval(interval);
  }, [isAnalyzing]);

  const securityStatus = security_intelligence?.posture?.toLowerCase() || "unknown";
  const isSecure = telemetry?.tls_status === "Secure";
  const seoScore = seo_intelligence?.score || 0;
  const perfScore = performance_intelligence?.score || 0;
  const confidence = confidence_score || 0;

  return (
    <div className="group relative flex flex-col rounded-xl border border-white/5 bg-[#111111] p-6 transition-all duration-300 hover:border-white/10 hover:shadow-lg hover:shadow-black/60 font-sans">
      
      {/* Top Row: Domain & Primary Status */}
      <div className="mb-4 flex items-center justify-between border-b border-white/5 pb-4">
        <div className="flex items-center gap-3">
          <Globe className="w-5 h-5 text-muted-foreground/80" />
          <h3 className="text-xl font-medium tracking-tight text-foreground/90">{domain}</h3>
          {isSecure && (
            <div className="hidden sm:flex items-center gap-1.5 px-2 py-0.5 rounded border border-emerald-500/20 bg-emerald-500/5 text-[10px] uppercase font-mono tracking-widest text-emerald-500/80">
              <ShieldCheck className="w-3 h-3" />
              TLS Verified
            </div>
          )}
        </div>
        <div className="flex items-center gap-2">
          {isAnalyzing ? (
            <div className="flex items-center gap-2 px-2 py-1 rounded bg-accent/5 border border-accent/20 text-[10px] uppercase font-mono tracking-widest text-accent/80 animate-pulse">
              <Activity className="w-3 h-3" />
              Active Scan
            </div>
          ) : (
            <div className={`flex items-center gap-1.5 text-[10px] uppercase font-mono tracking-widest ${confidence > 80 ? 'text-emerald-500/70' : 'text-amber-500/70'}`}>
              Confidence: {confidence > 0 ? `${confidence}%` : 'Degraded'}
            </div>
          )}
        </div>
      </div>

      {/* Narrative */}
      <div className="mb-6 relative">
        <div className="absolute left-0 top-0 bottom-0 w-[2px] bg-accent/30 rounded-full"></div>
        {isAnalyzing ? (
          <p className="pl-4 text-sm text-muted-foreground/50 italic font-mono animate-pulse">
            Generating infrastructure narrative...
          </p>
        ) : (
          <p className="pl-4 text-sm text-foreground/80 leading-relaxed font-serif italic tracking-wide">
            "{narrative || 'Infrastructure inspection failed or timed out.'}"
          </p>
        )}
      </div>

      {/* Micro-Telemetry Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-1.5 text-[10px] uppercase font-mono tracking-widest text-muted-foreground/60">
            <Server className="w-3 h-3" /> Status
          </div>
          <span className="text-xs font-mono text-foreground/80">{telemetry?.status || 'ERR'}</span>
        </div>
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-1.5 text-[10px] uppercase font-mono tracking-widest text-muted-foreground/60">
            <Clock className="w-3 h-3" /> Latency
          </div>
          <span className="text-xs font-mono text-foreground/80">{telemetry?.latency_ms ? `${telemetry.latency_ms}ms` : '---'}</span>
        </div>
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-1.5 text-[10px] uppercase font-mono tracking-widest text-muted-foreground/60">
            <Lock className="w-3 h-3" /> Issuer
          </div>
          <span className="text-xs font-mono text-foreground/80 truncate pr-2">{telemetry?.ssl_issuer || 'Unknown'}</span>
        </div>
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-1.5 text-[10px] uppercase font-mono tracking-widest text-muted-foreground/60">
            <Activity className="w-3 h-3" /> Duration
          </div>
          <span className="text-xs font-mono text-foreground/80">{telemetry?.scan_duration_ms ? `${telemetry.scan_duration_ms}ms` : '---'}</span>
        </div>
      </div>

      {/* Tech Stack */}
      <div className="mb-6">
        <div className="text-[10px] uppercase font-mono tracking-widest text-muted-foreground/60 mb-2 border-b border-white/5 pb-1 inline-block">
          Detected Signatures
        </div>
        <div className="flex flex-wrap gap-1.5 mt-1">
          {technologies && technologies.map((tech, idx) => {
            const name = typeof tech === "string" ? tech : tech.name;
            const category = typeof tech === "string" ? "Stack" : tech.category || "Stack";
            return (
              <span key={idx} className="flex items-center gap-1.5 rounded border border-white/5 bg-white/[0.02] px-2 py-1 text-[11px] text-muted-foreground/80 transition-colors hover:text-foreground/90 hover:bg-white/[0.05]">
                <span className="w-1 h-1 rounded-full bg-accent/40"></span>
                {name} <span className="opacity-40 ml-1 font-mono text-[9px] uppercase">{category}</span>
              </span>
            );
          })}
        </div>
      </div>

      {/* Performance & SEO Scores */}
      <div className="mt-auto border-t border-white/5 pt-4">
        {isAnalyzing ? (
          <div className="flex items-center justify-center py-2 text-xs font-mono uppercase tracking-widest text-accent/60 animate-pulse">
            <Activity className="w-3 h-3 mr-2" />
            {phase}
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-4">
            <div className="flex items-center justify-between p-3 rounded bg-black/20 border border-white/5">
              <span className="text-[10px] uppercase font-mono tracking-widest text-muted-foreground/60">SEO Score</span>
              <span className={`text-sm font-mono font-medium ${seoScore > 0 ? 'text-foreground/90' : 'text-rose-500/80'}`}>
                {seoScore > 0 ? `${seoScore}/100` : 'Failed'}
              </span>
            </div>
            <div className="flex items-center justify-between p-3 rounded bg-black/20 border border-white/5">
              <span className="text-[10px] uppercase font-mono tracking-widest text-muted-foreground/60">Perf Score</span>
              <span className={`text-sm font-mono font-medium ${perfScore > 0 ? 'text-foreground/90' : 'text-rose-500/80'}`}>
                {perfScore > 0 ? `${perfScore}/100` : 'Failed'}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
