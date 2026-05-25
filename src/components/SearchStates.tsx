import { Loader2, SearchX } from "lucide-react";

export function SearchingState() {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center animate-in fade-in duration-500">
      <Loader2 className="w-8 h-8 animate-spin text-accent mb-4" />
      <h3 className="text-lg font-medium text-foreground mb-2">Searching Intelligence...</h3>
      <p className="text-sm text-muted-foreground max-w-md mx-auto">
        Scanning global signals, articles, and domains to synthesize a comprehensive report.
      </p>
    </div>
  );
}

export function NoResultsState({ query }: { query: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center animate-in fade-in duration-500">
      <div className="w-12 h-12 rounded-full bg-secondary/50 border border-border flex items-center justify-center mb-4">
        <SearchX className="w-5 h-5 text-muted-foreground" />
      </div>
      <h3 className="text-lg font-medium text-foreground mb-2">No Intelligence Found</h3>
      <p className="text-sm text-muted-foreground max-w-md mx-auto">
        We couldn't find any significant data regarding "{query}". Try adjusting your parameters or use a broader topic.
      </p>
    </div>
  );
}
