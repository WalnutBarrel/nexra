import { TrendingUp, TrendingDown, Activity } from "lucide-react";

const TRENDING_DATA = [
  {
    topic: "Autonomous Supply Chains",
    category: "Logistics Tech",
    trend: "up",
    score: 92,
  },
  {
    topic: "Synthetic Data Generation",
    category: "AI Research",
    trend: "up",
    score: 88,
  },
  {
    topic: "Legacy CRM Migration",
    category: "Enterprise IT",
    trend: "down",
    score: 45,
  },
  {
    topic: "Quantum Error Correction",
    category: "Deep Tech",
    trend: "up",
    score: 76,
  },
];

export function TrendingIntelligence() {
  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center gap-2 text-xs font-medium text-muted-foreground uppercase tracking-wider">
        <Activity className="w-3.5 h-3.5" />
        Trending Signals
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {TRENDING_DATA.map((item) => (
          <div
            key={item.topic}
            className="group flex flex-col justify-between rounded-lg border border-border/40 bg-secondary/10 p-4 transition-all hover:bg-secondary/30 hover:border-border"
          >
            <div className="flex justify-between items-start mb-3">
              <span className="text-[10px] font-medium uppercase tracking-widest text-accent bg-accent/10 px-2 py-0.5 rounded-sm">
                {item.category}
              </span>
              {item.trend === "up" ? (
                <TrendingUp className="w-4 h-4 text-emerald-500/80" />
              ) : (
                <TrendingDown className="w-4 h-4 text-rose-500/80" />
              )}
            </div>
            <h4 className="text-sm font-medium text-foreground mb-1 leading-snug">
              {item.topic}
            </h4>
            <div className="flex items-center gap-1.5 mt-2">
              <div className="h-1.5 flex-1 bg-border/50 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-accent/60" 
                  style={{ width: `${item.score}%` }} 
                />
              </div>
              <span className="text-xs text-muted-foreground">{item.score}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
