"use client";

import { useState } from "react";
import { Terminal, Save, Download, Clock, ChevronRight, Activity, Database, ShieldCheck, Cpu } from "lucide-react";
import { WorkspaceApi } from "@/lib/api/client";

const TIMELINE_EVENTS = [
  { time: "Today, 14:22", event: "Security Posture Downgraded (CSP absent)" },
  { time: "Yesterday, 09:15", event: "Framework stack updated to Next.js 15" },
  { time: "Oct 20, 11:00", event: "Initial scan completed. Baseline established." }
];

export default function AnalystWorkspace() {
  const [query, setQuery] = useState("");
  const [queryHistory, setQueryHistory] = useState<{q: string, a: string}[]>([]);
  const [isQuerying, setIsQuerying] = useState(false);
  const [activeDossier, setActiveDossier] = useState("nexra.com");

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    const currentQuery = query;
    setQuery("");
    setIsQuerying(true);

    try {
      // Send contextual query to backend
      const res: any = await WorkspaceApi.queryDossier(currentQuery, { domain: activeDossier });
      setQueryHistory(prev => [...prev, { q: currentQuery, a: res.response }]);
    } catch (err) {
      setQueryHistory(prev => [...prev, { q: currentQuery, a: "System error: Failed to parse query context." }]);
    } finally {
      setIsQuerying(false);
    }
  };

  return (
    <div className="flex flex-col w-full min-h-screen pb-20 pt-8 px-8 lg:px-12 max-w-[1600px] mx-auto animate-in fade-in">
      
      {/* Workspace Header */}
      <div className="mb-8 flex flex-col gap-4 border-b border-border/50 pb-8">
        <div className="flex items-center gap-3 text-xs font-medium text-muted-foreground uppercase tracking-wider">
          <Terminal className="w-4 h-4" />
          Intelligence Workspace
        </div>
        <div className="flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-medium tracking-tight text-foreground">Analyst Console</h1>
            <p className="mt-2 text-sm text-muted-foreground">Synthesize telemetry, query active dossiers, and extract insights.</p>
          </div>
          <div className="flex gap-3">
            <button className="flex items-center gap-2 text-xs font-medium px-4 py-2 rounded-md border border-border/50 bg-secondary/10 hover:bg-secondary/20 transition-colors text-foreground">
              <Save className="w-3.5 h-3.5" /> Save Session
            </button>
            <button className="flex items-center gap-2 text-xs font-medium px-4 py-2 rounded-md border border-accent/20 bg-accent/10 hover:bg-accent/20 transition-colors text-accent">
              <Download className="w-3.5 h-3.5" /> Export PDF
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Column: Dossier Context & Timeline */}
        <div className="lg:col-span-4 flex flex-col gap-8">
          
          <div className="rounded-xl border border-border/50 bg-secondary/5 p-6">
            <h3 className="text-sm font-medium text-foreground uppercase tracking-wider mb-4 flex items-center gap-2">
              <Database className="w-4 h-4 text-accent" />
              Active Dossier Context
            </h3>
            
            <div className="flex items-center justify-between mb-6 p-3 bg-background border border-border/50 rounded-lg">
               <span className="font-medium text-sm text-foreground">{activeDossier}</span>
               <span className="text-xs px-2 py-0.5 rounded border border-emerald-500/20 bg-emerald-500/10 text-emerald-500 uppercase">Loaded</span>
            </div>

            <div className="flex flex-col gap-4 text-xs">
              <div className="flex justify-between items-center border-b border-border/30 pb-2">
                <span className="text-muted-foreground">Confidence Index</span>
                <span className="text-emerald-500 font-mono">92%</span>
              </div>
              <div className="flex justify-between items-center border-b border-border/30 pb-2">
                <span className="text-muted-foreground">Primary Tech Stack</span>
                <span className="text-foreground">Next.js, React</span>
              </div>
              <div className="flex justify-between items-center border-b border-border/30 pb-2">
                <span className="text-muted-foreground">Security Posture</span>
                <span className="text-amber-500">Warning (CSP)</span>
              </div>
            </div>
            
            <div className="mt-6 p-4 rounded bg-background border border-border/50">
               <span className="text-xs font-medium text-muted-foreground uppercase tracking-widest block mb-2">Synthesis</span>
               <p className="text-sm text-foreground leading-relaxed">
                 The target infrastructure presents a highly optimized edge-delivery framework. Significant security vulnerabilities exist regarding Content Security Policy omission.
               </p>
            </div>
          </div>

          {/* Timeline */}
          <div className="rounded-xl border border-border/50 bg-secondary/5 p-6">
            <h3 className="text-sm font-medium text-foreground uppercase tracking-wider mb-5 flex items-center gap-2">
              <Clock className="w-4 h-4 text-accent" />
              Intelligence Timeline
            </h3>
            <div className="flex flex-col gap-5">
              {TIMELINE_EVENTS.map((evt, idx) => (
                <div key={idx} className="flex gap-4">
                  <div className="flex flex-col items-center mt-1">
                    <div className="w-2 h-2 rounded-full bg-accent"></div>
                    {idx !== TIMELINE_EVENTS.length - 1 && <div className="w-px h-full bg-border/50 mt-1"></div>}
                  </div>
                  <div className="flex flex-col gap-1 pb-4">
                    <span className="text-[10px] text-muted-foreground font-mono uppercase">{evt.time}</span>
                    <span className="text-sm text-foreground leading-snug">{evt.event}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* Right Column: Query Console */}
        <div className="lg:col-span-8 flex flex-col">
          <div className="rounded-xl border border-border/50 bg-background overflow-hidden flex flex-col h-[700px]">
             
             <div className="px-6 py-4 border-b border-border/50 bg-secondary/10 flex items-center gap-2">
               <Cpu className="w-4 h-4 text-accent" />
               <h3 className="text-sm font-medium text-foreground uppercase tracking-wider">Contextual Query Console</h3>
             </div>

             <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-6">
                {queryHistory.length === 0 ? (
                  <div className="m-auto text-center max-w-md">
                    <Terminal className="w-10 h-10 text-muted-foreground/30 mx-auto mb-4" />
                    <p className="text-sm text-muted-foreground">
                      Query the active dossier. The synthesis engine understands full historical context and generates analytical briefs without generic phrasing.
                    </p>
                  </div>
                ) : (
                  queryHistory.map((item, idx) => (
                    <div key={idx} className="flex flex-col gap-3">
                      <div className="flex items-start gap-3 text-sm">
                         <span className="text-accent mt-0.5">❯</span>
                         <span className="font-mono text-foreground">{item.q}</span>
                      </div>
                      <div className="pl-6 text-sm text-muted-foreground leading-relaxed border-l-2 border-border/50 py-1 ml-[5px]">
                         {item.a}
                      </div>
                    </div>
                  ))
                )}
                
                {isQuerying && (
                  <div className="flex items-center gap-3 text-sm pl-[27px] py-1 text-muted-foreground">
                    <Activity className="w-3.5 h-3.5 animate-spin text-accent" />
                    Synthesizing response...
                  </div>
                )}
             </div>

             <div className="p-4 bg-secondary/5 border-t border-border/50">
               <form onSubmit={handleQuery} className="flex gap-3">
                 <input 
                   type="text" 
                   value={query}
                   onChange={e => setQuery(e.target.value)}
                   placeholder="Query intelligence context (e.g. 'What are the major performance bottlenecks?')"
                   className="flex-1 bg-background border border-border/50 rounded-md px-4 py-2.5 text-sm focus:outline-none focus:border-accent/50 text-foreground font-mono"
                 />
                 <button 
                   type="submit" 
                   disabled={!query.trim() || isQuerying}
                   className="bg-accent text-accent-foreground px-4 py-2 rounded-md hover:bg-accent/90 disabled:opacity-50 transition-colors flex items-center justify-center"
                 >
                   <ChevronRight className="w-5 h-5" />
                 </button>
               </form>
             </div>

          </div>
        </div>

      </div>
    </div>
  );
}
