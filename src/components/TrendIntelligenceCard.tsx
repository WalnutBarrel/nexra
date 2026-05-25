import { TrendingUp, Activity, Users, MessageSquare, Zap } from "lucide-react";

interface TrendIntelligenceCardProps {
  topic: string;
  category: string;
  trend: string;
  score: number;
  sources: number;
  mentions: number;
  narrative: string;
}

export function TrendIntelligenceCard({
  topic,
  category,
  trend,
  score,
  sources,
  mentions,
  narrative
}: TrendIntelligenceCardProps) {
  return (
    <div className="group relative flex flex-col rounded-xl border border-white/5 bg-[#111111] p-6 transition-all duration-300 hover:border-white/10 hover:shadow-lg hover:shadow-black/60 font-sans">
      
      {/* Top Row: Topic & Primary Status */}
      <div className="mb-4 flex items-center justify-between border-b border-white/5 pb-4">
        <div className="flex items-center gap-3">
          <TrendingUp className="w-5 h-5 text-accent/80" />
          <h3 className="text-xl font-medium tracking-tight text-foreground/90">{topic}</h3>
          <div className="hidden sm:flex items-center gap-1.5 px-2 py-0.5 rounded border border-white/5 bg-white/[0.02] text-[10px] uppercase font-mono tracking-widest text-muted-foreground/60">
            {category}
          </div>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 px-2 py-1 rounded bg-accent/5 border border-accent/20 text-[10px] uppercase font-mono tracking-widest text-accent/80">
            <Zap className="w-3 h-3" />
            Velocity: {score}
          </div>
        </div>
      </div>

      {/* Narrative */}
      <div className="mb-6 relative">
        <div className="absolute left-0 top-0 bottom-0 w-[2px] bg-accent/30 rounded-full"></div>
        <p className="pl-4 text-sm text-foreground/80 leading-relaxed font-serif italic tracking-wide">
          "{narrative}"
        </p>
      </div>

      {/* Micro-Telemetry Grid */}
      <div className="grid grid-cols-3 gap-4 mt-auto border-t border-white/5 pt-4">
        <div className="flex flex-col gap-1 p-3 rounded bg-black/20 border border-white/5">
          <div className="flex items-center gap-1.5 text-[10px] uppercase font-mono tracking-widest text-muted-foreground/60">
            <Activity className="w-3 h-3" /> Velocity
          </div>
          <span className="text-sm font-mono font-medium text-foreground/90">{score}/100</span>
        </div>
        <div className="flex flex-col gap-1 p-3 rounded bg-black/20 border border-white/5">
          <div className="flex items-center gap-1.5 text-[10px] uppercase font-mono tracking-widest text-muted-foreground/60">
            <Users className="w-3 h-3" /> Sources
          </div>
          <span className="text-sm font-mono font-medium text-foreground/90">{sources} feeds</span>
        </div>
        <div className="flex flex-col gap-1 p-3 rounded bg-black/20 border border-white/5">
          <div className="flex items-center gap-1.5 text-[10px] uppercase font-mono tracking-widest text-muted-foreground/60">
            <MessageSquare className="w-3 h-3" /> Mentions
          </div>
          <span className="text-sm font-mono font-medium text-foreground/90">{mentions} signals</span>
        </div>
      </div>

    </div>
  );
}
