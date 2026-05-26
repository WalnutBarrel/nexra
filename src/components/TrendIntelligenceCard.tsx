import { TrendingUp, Activity, Users, MessageSquare, Zap, GitBranch, Star, RadioTower, Sparkles } from "lucide-react";

interface TrendIntelligenceCardProps {
  topic: string;
  category: string;
  ecosystem?: string;
  trend: string;
  score: number;
  sources: number;
  mentions: number;
  narrative: string;
  has_github?: boolean;
  github_stars?: number;
  has_reddit?: boolean;
  dominant_sentiment?: string;
  discussion_intensity?: number;
  delta_24h?: number;
  delta_7d?: number;
  lifecycle_state?: string;
  credibility_score?: number;
  signal_quality?: string;
  divergence_markers?: string[];
  evidence_basis?: string[];
  relationships?: Array<{
    entity: string;
    type: string;
    confidence: number;
  }>;
}

export function TrendIntelligenceCard({
  topic,
  category,
  ecosystem,
  trend,
  score,
  credibility_score,
  signal_quality,
  divergence_markers,
  evidence_basis,
  sources,
  mentions,
  narrative,
  has_github,
  github_stars,
  has_reddit,
  dominant_sentiment,
  discussion_intensity,
  delta_24h,
  delta_7d,
  lifecycle_state,
  relationships
}: TrendIntelligenceCardProps) {
  
  // Calculate grid columns based on available telemetry
  const colCount = 3 + (has_github ? 1 : 0) + (has_reddit ? 2 : 0);
  const gridClass = colCount === 3 ? "grid-cols-3" : colCount === 4 ? "grid-cols-4" : colCount === 5 ? "grid-cols-3 sm:grid-cols-5" : "grid-cols-3 sm:grid-cols-6";

  return (
    <div className="group relative flex flex-col rounded-xl border border-white/5 bg-[#111111] p-6 transition-all duration-300 hover:border-white/10 hover:shadow-lg hover:shadow-black/60 font-sans">
      
      {/* Top Row: Topic & Primary Status */}
      <div className="mb-4 flex flex-col sm:flex-row sm:items-center justify-between border-b border-white/5 pb-4 gap-3 sm:gap-0">
        <div className="flex flex-wrap items-center gap-3">
          <TrendingUp className="w-5 h-5 text-accent/80" />
          <h3 className="text-xl font-medium tracking-tight text-foreground/90">{topic}</h3>
          
          <div className="flex items-center gap-2">
            <div className="hidden sm:flex items-center gap-1.5 px-2 py-0.5 rounded border border-white/5 bg-white/[0.02] text-[10px] uppercase font-mono tracking-widest text-muted-foreground/60">
              {category}
            </div>
            
            {ecosystem && (
              <div className="flex items-center gap-1.5 px-2 py-0.5 rounded border border-white/10 bg-white/5 text-[10px] uppercase font-mono tracking-widest text-foreground/80">
                Cluster: {ecosystem}
              </div>
            )}
            
            {lifecycle_state && (
              <div className="flex items-center gap-1.5 px-2 py-0.5 rounded border border-accent/20 bg-accent/5 text-[10px] uppercase font-mono tracking-widest text-accent/90">
                {lifecycle_state}
              </div>
            )}
            {signal_quality && (
              <div className={`flex items-center gap-1.5 px-2 py-0.5 rounded border text-[10px] uppercase font-mono tracking-widest ${
                signal_quality === 'High' ? 'bg-green-500/10 border-green-500/20 text-green-400' :
                signal_quality === 'Medium' ? 'bg-amber-500/10 border-amber-500/20 text-amber-400' :
                'bg-white/5 border-white/10 text-muted-foreground/80'
              }`}>
                Signal: {signal_quality}
              </div>
            )}
          </div>
        </div>
        <div className="flex items-center gap-2 flex-wrap">
          {has_github && (
            <div className="flex items-center gap-1.5 px-2 py-1 rounded bg-white/5 border border-white/10 text-[10px] uppercase font-mono tracking-widest text-foreground/80">
              <GitBranch className="w-3 h-3" />
              Traction
            </div>
          )}
          {has_reddit && dominant_sentiment && (
            <div className="hidden sm:flex items-center gap-1.5 px-2 py-1 rounded bg-white/5 border border-white/10 text-[10px] uppercase font-mono tracking-widest text-foreground/80">
              <Sparkles className="w-3 h-3 text-amber-400/80" />
              {dominant_sentiment}
            </div>
          )}
          {credibility_score !== undefined && (
             <div className="flex items-center gap-1.5 px-2 py-1 rounded bg-white/5 border border-white/10 text-[10px] uppercase font-mono tracking-widest text-foreground/80">
               Credibility: {Math.round(credibility_score)}
             </div>
          )}
          <div className="flex items-center gap-1.5 px-2 py-1 rounded bg-accent/5 border border-accent/20 text-[10px] uppercase font-mono tracking-widest text-accent/80">
            <Zap className="w-3 h-3" />
            Velocity: {score} 
            {delta_24h !== undefined && (
              <span className={delta_24h >= 0 ? "text-green-400" : "text-red-400"}>
                ({delta_24h >= 0 ? '+' : ''}{delta_24h}%)
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Narrative */}
      <div className="mb-4 relative">
        <div className="absolute left-0 top-0 bottom-0 w-[2px] bg-accent/30 rounded-full"></div>
        <p className="pl-4 text-sm text-foreground/80 leading-relaxed font-serif italic tracking-wide">
          "{narrative}"
        </p>
      </div>

      {/* Relationship Telemetry */}
      {relationships && relationships.length > 0 && (
        <div className="mb-4 flex flex-wrap items-center gap-2 text-xs font-mono">
          <span className="text-muted-foreground/60 uppercase tracking-widest text-[9px] mr-1">Correlations:</span>
          {relationships.map((rel, i) => (
            <div key={i} className="flex items-center gap-1.5 px-2 py-0.5 rounded bg-black/40 border border-white/5 text-foreground/70">
              <span>{rel.type}</span>
              <span className="text-accent/80 font-semibold">{rel.entity}</span>
            </div>
          ))}
        </div>
      )}

      {/* Divergence Markers */}
      {divergence_markers && divergence_markers.length > 0 && (
        <div className="mb-4 flex flex-col gap-1.5 border-l-2 border-amber-500/30 pl-3">
          {divergence_markers.map((marker, i) => (
            <div key={i} className="text-[10px] uppercase font-mono tracking-widest text-amber-500/70">
              [DIVERGENCE] {marker}
            </div>
          ))}
        </div>
      )}

      {/* Evidence Basis */}
      {evidence_basis && evidence_basis.length > 0 && (
        <div className="mb-6">
          <div className="text-[10px] uppercase font-mono tracking-widest text-muted-foreground/50 mb-2">Evidence Basis:</div>
          <ul className="space-y-1.5 border-l border-white/5 pl-3">
            {evidence_basis.map((evidence, i) => (
              <li key={i} className="text-[11px] text-muted-foreground/70 font-mono flex items-start">
                <span className="text-accent/50 mr-2 text-[10px] mt-0.5">{'>'}</span>
                {evidence}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Micro-Telemetry Grid */}
      <div className={`grid ${gridClass} gap-3 sm:gap-4 mt-auto border-t border-white/5 pt-4`}>
        {has_github && (
          <div className="flex flex-col gap-1 p-2 sm:p-3 rounded bg-black/20 border border-white/5">
            <div className="flex items-center gap-1.5 text-[9px] sm:text-[10px] uppercase font-mono tracking-widest text-muted-foreground/60">
              <Star className="w-3 h-3" /> GitHub
            </div>
            <span className="text-xs sm:text-sm font-mono font-medium text-foreground/90">
              {github_stars ? `${(github_stars / 1000).toFixed(1)}k` : 'Active'}
            </span>
          </div>
        )}
        {has_reddit && (
          <>
            <div className="flex flex-col gap-1 p-2 sm:p-3 rounded bg-black/20 border border-white/5">
              <div className="flex items-center gap-1.5 text-[9px] sm:text-[10px] uppercase font-mono tracking-widest text-muted-foreground/60">
                <RadioTower className="w-3 h-3" /> Sentiment
              </div>
              <span className="text-xs sm:text-sm font-mono font-medium text-foreground/90 capitalize truncate">
                {dominant_sentiment || 'Neutral'}
              </span>
            </div>
            <div className="flex flex-col gap-1 p-2 sm:p-3 rounded bg-black/20 border border-white/5">
              <div className="flex items-center gap-1.5 text-[9px] sm:text-[10px] uppercase font-mono tracking-widest text-muted-foreground/60">
                <MessageSquare className="w-3 h-3" /> Intensity
              </div>
              <span className="text-xs sm:text-sm font-mono font-medium text-foreground/90">
                {discussion_intensity}
              </span>
            </div>
          </>
        )}
        <div className="flex flex-col gap-1 p-2 sm:p-3 rounded bg-black/20 border border-white/5">
          <div className="flex items-center gap-1.5 text-[9px] sm:text-[10px] uppercase font-mono tracking-widest text-muted-foreground/60">
            <Activity className="w-3 h-3" /> Velocity
          </div>
          <span className="text-xs sm:text-sm font-mono font-medium text-foreground/90">{score}/100</span>
        </div>
        <div className="flex flex-col gap-1 p-2 sm:p-3 rounded bg-black/20 border border-white/5">
          <div className="flex items-center gap-1.5 text-[9px] sm:text-[10px] uppercase font-mono tracking-widest text-muted-foreground/60">
            <Users className="w-3 h-3" /> Sources
          </div>
          <span className="text-xs sm:text-sm font-mono font-medium text-foreground/90">{sources}</span>
        </div>
        {!has_reddit && (
          <div className="flex flex-col gap-1 p-2 sm:p-3 rounded bg-black/20 border border-white/5">
            <div className="flex items-center gap-1.5 text-[9px] sm:text-[10px] uppercase font-mono tracking-widest text-muted-foreground/60">
              <MessageSquare className="w-3 h-3" /> Signals
            </div>
            <span className="text-xs sm:text-sm font-mono font-medium text-foreground/90">{mentions}</span>
          </div>
        )}
      </div>

    </div>
  );
}
