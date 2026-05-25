"use client";

import { useState, useEffect } from "react";
import { TrendingUp, TrendingDown, Activity } from "lucide-react";
import { IntelligenceApi } from "@/lib/api/client";

export function TrendingIntelligence() {
  const [trends, setTrends] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadTrends() {
      try {
        const response: any = await IntelligenceApi.getTrending();
        setTrends(response.data || []);
      } catch (e) {
        console.error("Failed to fetch trends", e);
      } finally {
        setLoading(false);
      }
    }
    loadTrends();
  }, []);

  if (loading) {
    return <div className="text-sm text-muted-foreground animate-pulse">Computing telemetry...</div>;
  }

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center gap-2 text-xs font-medium text-muted-foreground uppercase tracking-wider">
        <Activity className="w-3.5 h-3.5" />
        Accelerating Trends
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {trends.map((item, idx) => (
          <div
            key={idx}
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
              <span className="text-xs text-muted-foreground font-mono">{item.score}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
