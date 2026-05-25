"use client";

import { Folder, Pin, Clock, MoreVertical, Search, Plus, Filter, Users, GlobeLock } from "lucide-react";
import { useState } from "react";

const DOSSIER_COLLECTIONS = [
  { id: 1, name: "Global Threat Intel", count: 24, lastUpdated: "2h ago", isPinned: true },
  { id: 2, name: "Supply Chain Disruptions", count: 12, lastUpdated: "5h ago", isPinned: true },
  { id: 3, name: "Q4 Competitor Analysis", count: 8, lastUpdated: "1d ago", isPinned: false },
  { id: 4, name: "Policy & Regulatory Sweeps", count: 42, lastUpdated: "3d ago", isPinned: false },
];

const RECENT_INVESTIGATIONS = [
  { domain: "openai.com", analyst: "J. Doe", time: "10 mins ago", type: "Security Sweep" },
  { domain: "anthropic.com", analyst: "A. Smith", time: "1 hour ago", type: "Full Intelligence" },
  { domain: "bloomberg.com", analyst: "System", time: "2 hours ago", type: "Automated Routine" },
];

export default function WorkspaceCollections() {
  const [activeTab, setActiveTab] = useState("collections");

  return (
    <div className="flex flex-col w-full min-h-screen pb-20 pt-8 px-8 lg:px-12 max-w-[1600px] mx-auto animate-in fade-in">
      
      {/* Workspace Header */}
      <div className="mb-8 flex flex-col gap-4 border-b border-border/50 pb-8">
        <div className="flex items-center gap-3 text-xs font-medium text-muted-foreground uppercase tracking-wider">
          <GlobeLock className="w-4 h-4" />
          Acme Corp Intelligence Division
        </div>
        <div className="flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-medium tracking-tight text-foreground">Collaborative Workspace</h1>
            <p className="mt-2 text-sm text-muted-foreground">Manage dossier collections, track analyst activity, and organize intelligence.</p>
          </div>
          <div className="flex gap-3">
            <button className="flex items-center gap-2 text-xs font-medium px-4 py-2 rounded-md border border-border/50 bg-secondary/10 hover:bg-secondary/20 transition-colors text-foreground">
              <Users className="w-3.5 h-3.5" /> Manage Analysts
            </button>
            <button className="flex items-center gap-2 text-xs font-medium px-4 py-2 rounded-md border border-accent/20 bg-accent/10 hover:bg-accent/20 transition-colors text-accent">
              <Plus className="w-3.5 h-3.5" /> New Collection
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Main Content Area */}
        <div className="lg:col-span-8 flex flex-col gap-6">
           
           {/* Filters */}
           <div className="flex gap-4 items-center mb-2">
             <div className="relative flex-1">
               <Search className="w-4 h-4 text-muted-foreground absolute left-3 top-2.5" />
               <input 
                 type="text" 
                 placeholder="Search collections and dossiers..." 
                 className="w-full bg-secondary/5 border border-border/50 rounded-md pl-9 pr-4 py-2 text-sm focus:outline-none focus:border-accent/50 text-foreground transition-colors"
               />
             </div>
             <button className="flex items-center gap-2 text-xs font-medium px-4 py-2 rounded-md border border-border/50 bg-secondary/10 hover:bg-secondary/20 transition-colors text-foreground">
                <Filter className="w-3.5 h-3.5" /> Filter
             </button>
           </div>

           {/* Collections Grid */}
           <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
             {DOSSIER_COLLECTIONS.map(collection => (
               <div key={collection.id} className="p-5 rounded-xl border border-border/50 bg-secondary/5 hover:bg-secondary/10 transition-colors group cursor-pointer flex flex-col justify-between">
                 <div className="flex justify-between items-start mb-6">
                   <div className="w-10 h-10 rounded-lg bg-background border border-border/50 flex items-center justify-center">
                     <Folder className="w-4 h-4 text-accent" />
                   </div>
                   <div className="flex gap-2">
                     {collection.isPinned && <Pin className="w-3.5 h-3.5 text-muted-foreground fill-muted-foreground" />}
                     <button className="text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity">
                       <MoreVertical className="w-4 h-4" />
                     </button>
                   </div>
                 </div>
                 <div>
                   <h3 className="text-base font-medium text-foreground">{collection.name}</h3>
                   <div className="flex gap-4 mt-2 text-xs text-muted-foreground">
                     <span>{collection.count} Dossiers</span>
                     <span>•</span>
                     <span className="flex items-center gap-1">
                       <Clock className="w-3 h-3" /> Updated {collection.lastUpdated}
                     </span>
                   </div>
                 </div>
               </div>
             ))}
           </div>
        </div>

        {/* Sidebar: Activity & Audits */}
        <div className="lg:col-span-4 flex flex-col gap-6">
          <div className="rounded-xl border border-border/50 bg-background overflow-hidden flex flex-col">
             
             <div className="px-6 py-4 border-b border-border/50 bg-secondary/10 flex items-center justify-between">
               <h3 className="text-sm font-medium text-foreground uppercase tracking-wider">Analyst Activity Trail</h3>
               <span className="text-[10px] font-medium text-emerald-500 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20 uppercase tracking-widest">Live</span>
             </div>

             <div className="flex-1 p-6 flex flex-col gap-6">
               {RECENT_INVESTIGATIONS.map((inv, idx) => (
                 <div key={idx} className="flex gap-4">
                    <div className="flex flex-col items-center mt-1">
                      <div className="w-2 h-2 rounded-full bg-accent"></div>
                      {idx !== RECENT_INVESTIGATIONS.length - 1 && <div className="w-px h-full bg-border/50 mt-1"></div>}
                    </div>
                    <div className="flex flex-col gap-1 pb-4">
                      <div className="flex items-center gap-2">
                        <span className="text-sm text-foreground font-medium">{inv.analyst}</span>
                        <span className="text-xs text-muted-foreground">ran {inv.type}</span>
                      </div>
                      <span className="text-sm text-accent font-mono">{inv.domain}</span>
                      <span className="text-[10px] text-muted-foreground uppercase tracking-widest mt-1">{inv.time}</span>
                    </div>
                 </div>
               ))}
             </div>
             
          </div>
        </div>

      </div>
    </div>
  );
}
