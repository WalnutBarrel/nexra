import { Bell, Command, User } from "lucide-react";

export function TopNav() {
  return (
    <header className="sticky top-0 z-10 flex h-14 items-center justify-between border-b border-border bg-background/80 px-6 backdrop-blur-sm">
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <span>Overview</span>
        <span className="text-border">/</span>
        <span className="text-foreground font-medium">Discover</span>
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
