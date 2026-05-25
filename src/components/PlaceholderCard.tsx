import { ArrowUpRight } from "lucide-react";

interface PlaceholderCardProps {
  category: string;
  title: string;
  description: string;
  date: string;
}

export function PlaceholderCard({ category, title, description, date }: PlaceholderCardProps) {
  return (
    <div className="group relative flex flex-col justify-between rounded-xl border border-border/50 bg-secondary/20 p-5 transition-all duration-300 hover:border-border hover:bg-secondary/40">
      <div>
        <div className="mb-3 flex items-center justify-between">
          <span className="text-xs font-medium uppercase tracking-wider text-accent">
            {category}
          </span>
          <ArrowUpRight className="w-4 h-4 text-muted-foreground opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
        </div>
        <h3 className="mb-2 text-base font-medium leading-snug text-foreground">
          {title}
        </h3>
        <p className="text-sm text-muted-foreground line-clamp-2 leading-relaxed">
          {description}
        </p>
      </div>
      <div className="mt-6 flex items-center text-xs text-muted-foreground/70">
        <span>{date}</span>
      </div>
    </div>
  );
}
