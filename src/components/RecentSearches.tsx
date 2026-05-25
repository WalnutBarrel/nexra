import { Clock } from "lucide-react";

const RECENT_SEARCHES = [
  "Q3 Semiconductor Capex",
  "EU AI Act Timeline",
  "Spatial Computing Patents",
  "LLM Context Window Trends",
];

export function RecentSearches() {
  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center gap-2 text-xs font-medium text-muted-foreground uppercase tracking-wider">
        <Clock className="w-3.5 h-3.5" />
        Recent Activity
      </div>
      <div className="flex overflow-x-auto gap-2 pb-2 scrollbar-none">
        {RECENT_SEARCHES.map((search) => (
          <button
            key={search}
            className="whitespace-nowrap rounded-full border border-border/40 bg-secondary/20 px-4 py-1.5 text-sm text-muted-foreground transition-all hover:bg-white/5 hover:text-foreground hover:border-border"
          >
            {search}
          </button>
        ))}
      </div>
    </div>
  );
}
