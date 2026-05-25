"use client";

import { useState, useEffect } from "react";
import { IntelligenceApi } from "@/lib/api/client";
import { Terminal, Rss, Clock } from "lucide-react";

export function LiveIngestionFeed() {
  const [feed, setFeed] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchLiveNews() {
      try {
        const response: any = await IntelligenceApi.getLiveNews();
        setFeed(response.data || []);
      } catch (e) {
        console.error("Failed to fetch live news", e);
      } finally {
        setLoading(false);
      }
    }
    fetchLiveNews();
    
    // Poll every 60 seconds
    const interval = setInterval(fetchLiveNews, 60000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div className="text-sm text-muted-foreground animate-pulse flex items-center gap-2"><Terminal className="w-4 h-4"/> Establishing secure telemetry connection...</div>;
  }

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-xs font-medium text-emerald-500 uppercase tracking-wider">
          <Rss className="w-3.5 h-3.5" />
          Live Ingestion Stream
        </div>
        <div className="flex items-center gap-2 text-[10px] text-muted-foreground font-mono">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          {feed.length} signals tracked
        </div>
      </div>
      
      <div className="flex flex-col gap-2 max-h-[400px] overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-secondary/50">
        {feed.map((item, idx) => (
          <div key={idx} className="flex flex-col gap-1.5 p-3 rounded-lg border border-border/40 bg-secondary/5 hover:bg-secondary/20 transition-colors">
            <div className="flex justify-between items-start gap-4">
              <a href={item.url} target="_blank" rel="noreferrer" className="text-sm font-medium text-foreground hover:text-accent transition-colors line-clamp-1">
                {item.title}
              </a>
              <span className="text-[10px] text-muted-foreground whitespace-nowrap font-mono">
                {Math.round((Date.now()/1000 - item.timestamp) / 60)}m ago
              </span>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-[10px] text-muted-foreground/80 uppercase tracking-wider bg-secondary/30 px-1.5 py-0.5 rounded">
                {item.source}
              </span>
              
              <div className="flex items-center gap-2">
                 {item.tags?.slice(0, 2).map((tag: string) => (
                    <span key={tag} className="text-[9px] text-muted-foreground/70 uppercase">#{tag}</span>
                 ))}
                 <span className={`text-[10px] font-bold ${item.sentiment === 'positive' ? 'text-emerald-500' : item.sentiment === 'negative' ? 'text-rose-500' : 'text-slate-500'}`}>
                    {item.sentiment.toUpperCase()}
                 </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
