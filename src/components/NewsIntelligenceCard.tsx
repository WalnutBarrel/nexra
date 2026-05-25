import { FileText, ShieldCheck, Activity } from "lucide-react";

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

  return (
    <div className="group relative flex flex-col rounded-xl border border-border/50 bg-background p-5 transition-all duration-300 hover:border-border hover:shadow-sm">
      <div className="mb-4 flex items-center justify-between text-xs text-muted-foreground">
        <div className="flex items-center gap-2">
          <FileText className="w-3.5 h-3.5" />
          <span className="font-medium text-foreground">{source}</span>
          <span>•</span>
          <span>{timestamp}</span>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1" title="Sentiment">
            <Activity className={`w-3.5 h-3.5 ${sentimentColor}`} />
            <span className="capitalize">{sentiment}</span>
          </div>
          <div className="flex items-center gap-1" title="Credibility Score">
            <ShieldCheck className="w-3.5 h-3.5 text-accent" />
            <span>{credibilityScore}%</span>
          </div>
        </div>
      </div>
      
      <h3 className="mb-2 text-lg font-medium leading-tight text-foreground">
        {title}
      </h3>
      
      <div className="relative mb-4">
        <div className="absolute left-0 top-0 bottom-0 w-0.5 bg-accent/30 rounded-full"></div>
        <p className="pl-3 text-sm text-muted-foreground leading-relaxed line-clamp-3">
          {summary}
        </p>
      </div>

      <div className="mt-auto flex flex-wrap gap-2 pt-2">
        {tags.map((tag) => (
          <span key={tag} className="rounded-md border border-border/40 bg-secondary/20 px-2 py-0.5 text-[10px] uppercase tracking-widest text-muted-foreground transition-colors hover:text-foreground hover:bg-secondary/40">
            {tag}
          </span>
        ))}
      </div>
    </div>
  );
}
