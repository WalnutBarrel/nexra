import { Bell, Command, User } from "lucide-react";

export function TopNav() {
  return (
    <header className="sticky top-0 z-10 flex h-14 items-center justify-between border-b border-border bg-background/80 px-6 backdrop-blur-sm">
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <span>Overview</span>
        <span className="text-border">/</span>
        <span className="text-foreground font-medium mr-4">Discover</span>
        <div className="hidden sm:flex items-center gap-2 text-[10px] uppercase font-mono tracking-wider text-muted-foreground/80 bg-secondary/30 px-2 py-1 rounded border border-white/5">
          <span className="relative flex h-1.5 w-1.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-emerald-500"></span>
          </span>
          Live Ingestion Active (3 Workers)
        </div>
      </div>

      <div className="flex items-center gap-4">
        <button className="text-muted-foreground hover:text-foreground transition-colors">
          <Bell className="w-4 h-4" />
        </button>
        <button className="flex h-8 w-8 items-center justify-center rounded-full bg-secondary text-secondary-foreground hover:bg-secondary/80 transition-colors">
          <User className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
}
