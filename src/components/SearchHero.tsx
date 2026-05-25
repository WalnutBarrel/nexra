"use client";

import { Search, Sparkles } from "lucide-react";
import { useState, useRef, useEffect } from "react";

interface SearchHeroProps {
  onSearch: (query: string) => void;
}

export function SearchHero({ onSearch }: SearchHeroProps) {
  const [query, setQuery] = useState("");
  const [isFocused, setIsFocused] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        inputRef.current?.focus();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
      inputRef.current?.blur();
      setIsFocused(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center py-8 px-4 w-full transition-all duration-500">
      <div className="mb-4 flex items-center gap-2 rounded-full border border-border/50 bg-secondary/30 px-3 py-1 text-[10px] uppercase font-mono tracking-widest text-muted-foreground backdrop-blur-sm transition-opacity duration-300">
        <Sparkles className="w-3 h-3 text-accent" />
        <span>Nexra Intelligence Engine v2.0</span>
      </div>
      
      <h1 className="text-3xl md:text-4xl font-medium tracking-tight text-foreground mb-6 text-center max-w-2xl transition-all duration-300 leading-tight">
        What do you want to explore today?
      </h1>

      <div className="relative w-full max-w-2xl group z-20">
        {/* Animated focus glow */}
        <div className={`absolute -inset-1 rounded-2xl bg-accent/10 blur-xl transition-opacity duration-500 ${isFocused ? 'opacity-100' : 'opacity-0'}`}></div>
        
        <form onSubmit={handleSubmit} className="relative flex flex-col w-full rounded-xl border border-white/10 bg-[#111111] shadow-lg shadow-accent/5 transition-all duration-300 focus-within:border-accent/40 focus-within:ring-1 focus-within:ring-accent/20">
          <div className="flex items-center px-4 py-3.5">
            <Search className={`w-4 h-4 transition-colors duration-300 mr-3 ${isFocused ? 'text-accent' : 'text-muted-foreground'}`} />
            <input
              ref={inputRef}
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onFocus={() => setIsFocused(true)}
              onBlur={() => setTimeout(() => setIsFocused(false), 200)}
              placeholder="Search knowledge base, insights, or documents..."
              className="w-full bg-transparent text-foreground placeholder:text-muted-foreground/60 outline-none text-base font-medium"
            />
            <div className="flex items-center gap-0.5 ml-3 text-[10px] text-muted-foreground/80 bg-black/40 px-1.5 py-0.5 rounded border border-white/5">
              <kbd className="font-sans">⌘</kbd>
              <kbd className="font-sans">K</kbd>
            </div>
          </div>

          {/* Search Suggestions Dropdown */}
          {isFocused && (
            <div className="absolute top-full left-0 right-0 mt-2 rounded-xl border border-border bg-background shadow-xl overflow-hidden animate-in fade-in slide-in-from-top-2 duration-200">
              <div className="p-2 flex flex-col">
                <div className="px-3 py-2 text-xs font-medium text-muted-foreground uppercase tracking-wider">
                  Suggestions
                </div>
                <button type="button" onMouseDown={() => setQuery("Artificial Intelligence")} className="text-left px-3 py-2 text-sm text-foreground hover:bg-secondary/40 rounded-md transition-colors">
                  Artificial Intelligence
                </button>
                <button type="button" onMouseDown={() => setQuery("Global Market Analysis")} className="text-left px-3 py-2 text-sm text-foreground hover:bg-secondary/40 rounded-md transition-colors">
                  Global Market Analysis
                </button>
                <button type="button" onMouseDown={() => setQuery("Quantum Computing")} className="text-left px-3 py-2 text-sm text-foreground hover:bg-secondary/40 rounded-md transition-colors">
                  Quantum Computing
                </button>
              </div>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}
