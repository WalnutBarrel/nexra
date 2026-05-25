import Link from "next/link";
import { LayoutGrid, Library, Settings, Search, BookOpen } from "lucide-react";

const NAV_ITEMS = [
  { name: "Discover", icon: Search, href: "#" },
  { name: "Library", icon: Library, href: "#" },
  { name: "Collections", icon: LayoutGrid, href: "#" },
  { name: "Journal", icon: BookOpen, href: "#" },
];

export function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 w-64 border-r border-border bg-background flex flex-col z-10">
      <div className="flex h-14 items-center px-6 border-b border-border/50">
        <span className="font-semibold text-lg tracking-tight text-foreground">
          Nexra
        </span>
      </div>

      <div className="flex-1 overflow-y-auto py-6 px-4 flex flex-col gap-1">
        <div className="text-xs font-medium text-muted-foreground mb-2 px-2 uppercase tracking-wider">
          Platform
        </div>
        {NAV_ITEMS.map((item) => (
          <Link
            key={item.name}
            href={item.href}
            className="flex items-center gap-3 rounded-md px-2 py-2 text-sm text-muted-foreground hover:text-foreground hover:bg-white/5 transition-colors duration-200"
          >
            <item.icon className="w-4 h-4" />
            {item.name}
          </Link>
        ))}
      </div>

      <div className="p-4 border-t border-border/50">
        <button className="flex w-full items-center gap-3 rounded-md px-2 py-2 text-sm text-muted-foreground hover:text-foreground hover:bg-white/5 transition-colors duration-200">
          <Settings className="w-4 h-4" />
          Settings
        </button>
      </div>
    </aside>
  );
}
