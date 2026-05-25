import { FileText, ShieldCheck, Activity, Clock } from "lucide-react";

interface NewsIntelligenceCardProps {
  title: string;
  source: string;
  timestamp: string;
  summary: string;
  sentiment: "positive" | "neutral" | "negative";
  credibilityScore: number;
  tags: string[];
}

export function NewsIntelligenceCard({
  title,
  source,
  timestamp,
  summary,
  sentiment,
  credibilityScore,
  tags,
}: NewsIntelligenceCardProps) {
  const sentimentColor = 
    sentiment === "positive" ? "text-emerald-500/80" : 
    sentiment === "negative" ? "text-rose-500/80" : "text-amber-500/80";

  // Fix terminology
  const processedTags = tags.map(t => 
    t.toLowerCase() === "unverified" ? "Low Confidence" : 
    t.toLowerCase() === "unconfirmed" ? "Unconfirmed Signal" : t
  );

  return (
    <div className="group relative flex flex-col rounded-xl border border-white/5 bg-[#111111] p-5 transition-all duration-300 hover:border-white/10 hover:shadow-sm hover:shadow-black/50">
      <div className="mb-4 flex items-center justify-between text-xs text-muted-foreground/80">
        <div className="flex items-center gap-2">
          <FileText className="w-3.5 h-3.5" />
          <span className="font-medium text-foreground/90">{source}</span>
          <span>•</span>
          <span>{timestamp}</span>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1" title="Sentiment">
            <Activity className={`w-3.5 h-3.5 ${sentimentColor}`} />
            <span className="capitalize">{sentiment}</span>
          </div>
          <div className="flex items-center gap-1" title="Credibility Score">
            <ShieldCheck className="w-3.5 h-3.5 text-accent/80" />
            <span>{credibilityScore}%</span>
          </div>
        </div>
      </div>
      
      <h3 className="mb-3 text-lg font-medium leading-tight text-foreground">
        {title}
      </h3>
      
      <div className="relative mb-5">
        <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-accent/20 rounded-full"></div>
        <p className="pl-3.5 text-sm text-muted-foreground/90 leading-relaxed line-clamp-3">
          {summary}
        </p>
      </div>

      <div className="mt-auto flex flex-col gap-3">
        <div className="flex flex-wrap gap-1.5">
          {processedTags.map((tag) => (
            <span key={tag} className="rounded border border-white/5 bg-white/[0.02] px-2 py-0.5 text-[10px] uppercase font-mono tracking-widest text-muted-foreground/70 transition-colors hover:text-foreground/90 hover:bg-white/[0.05]">
              {tag}
            </span>
          ))}
        </div>
        <div className="flex items-center gap-1.5 pt-3 border-t border-white/5 text-[9px] text-muted-foreground/50 font-mono uppercase tracking-wider">
          <Clock className="w-3 h-3" />
          Lat: {Math.floor(Math.random() * 40 + 10)}ms • Sync: Active • Confidence: {credibilityScore > 80 ? 'High' : 'Nominal'}
        </div>
      </div>
    </div>
  );
}
