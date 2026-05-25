import { ShieldCheck, Server, AlertTriangle, ArrowUpRight, Activity, Clock, Database, DatabaseBackup, Gauge, Cpu, Workflow } from "lucide-react";

const INFRA_METRICS = [
  { label: "API Global Latency (p99)", value: "240ms", trend: "-12ms", icon: Activity },
  { label: "Active RQ Workers", value: "14", trend: "Stable", icon: Workflow },
  { label: "Redis Cache Hit Ratio", value: "94.2%", trend: "+1.2%", icon: DatabaseBackup },
  { label: "Rate Limits Triggered", value: "1,402", trend: "+52", icon: ShieldCheck },
];

const QUEUE_TELEMETRY = [
  { name: "Website Scanner (High Priority)", depth: 420, workers: 8, status: "Processing", latency: "1.2s" },
  { name: "AI Report Synthesis", depth: 15, workers: 4, status: "Idle", latency: "8.4s" },
  { name: "Bulk Export Generation", depth: 0, workers: 2, status: "Idle", latency: "0ms" },
];

const DEAD_LETTER_QUEUE = [
  { job_id: "scan_5f21a", queue: "Scanner", error: "SSL Handshake Failed", retries: 3 },
  { job_id: "ai_11b9x", queue: "Synthesis", error: "Context Length Exceeded", retries: 1 },
  { job_id: "export_991z", queue: "Exports", error: "S3 Upload Timeout", retries: 5 },
];

export default function OperationalCommandCenter() {
  return (
    <div className="flex flex-col w-full pb-20 pt-8 px-8 lg:px-12 max-w-[1600px] mx-auto animate-in fade-in">
      <div className="mb-10 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-medium tracking-tight text-foreground flex items-center gap-3">
            <Gauge className="w-8 h-8 text-emerald-500" />
            Infrastructure Telemetry
          </h1>
          <p className="text-sm text-muted-foreground mt-2">Live monitoring of Redis caching, RQ workers, and system health.</p>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className="flex items-center gap-2 text-xs font-medium text-emerald-500 bg-emerald-500/10 px-3 py-1.5 rounded-md border border-emerald-500/20 uppercase tracking-widest">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            All Systems Nominal
          </span>
          <span className="text-[10px] text-muted-foreground font-mono mt-1">Trace ID: 9f8a-211b-430c</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {INFRA_METRICS.map((metric) => (
          <div key={metric.label} className="p-5 rounded-xl border border-border/50 bg-secondary/5">
            <div className="flex items-center justify-between mb-4">
              <metric.icon className="w-4 h-4 text-muted-foreground" />
              <span className={`text-xs font-medium ${metric.label.includes('Rate Limits') ? 'text-amber-500/80' : 'text-emerald-500/80'}`}>{metric.trend}</span>
            </div>
            <div className="text-2xl font-mono text-foreground mb-1">{metric.value}</div>
            <div className="text-xs text-muted-foreground uppercase tracking-wider">{metric.label}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 flex flex-col gap-6">
          
          {/* Active Queues */}
          <div className="rounded-xl border border-border/50 bg-background overflow-hidden">
            <div className="px-5 py-4 border-b border-border/50 flex justify-between items-center bg-secondary/10">
              <h3 className="text-sm font-medium text-foreground uppercase tracking-wider flex items-center gap-2">
                <Server className="w-4 h-4 text-accent" /> Redis Queues (RQ)
              </h3>
            </div>
            <div className="w-full overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-muted-foreground uppercase tracking-wider bg-secondary/5">
                  <tr>
                    <th className="px-5 py-3 font-medium">Queue Name</th>
                    <th className="px-5 py-3 font-medium">Depth</th>
                    <th className="px-5 py-3 font-medium">Workers</th>
                    <th className="px-5 py-3 font-medium">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border/30">
                  {QUEUE_TELEMETRY.map((item, idx) => (
                    <tr key={idx} className="hover:bg-secondary/10 transition-colors">
                      <td className="px-5 py-4 font-medium text-foreground">{item.name}</td>
                      <td className="px-5 py-4 font-mono text-accent">{item.depth}</td>
                      <td className="px-5 py-4 font-mono text-muted-foreground">{item.workers} active</td>
                      <td className="px-5 py-4">
                        <span className={`px-2 py-0.5 rounded-md text-[10px] uppercase tracking-widest border flex items-center gap-1 w-max ${
                          item.status === "Processing" ? "bg-emerald-500/10 text-emerald-500 border-emerald-500/20" : 
                          "bg-secondary/30 text-muted-foreground border-border/40"
                        }`}>
                          {item.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Subsystem Health Blocks */}
          <div className="grid grid-cols-2 gap-4">
             <div className="p-6 rounded-xl border border-border/50 bg-secondary/5">
                <h3 className="text-sm font-medium text-foreground uppercase tracking-wider mb-5 flex items-center gap-2">
                  <Database className="w-4 h-4 text-accent" />
                  PostgreSQL Persistence
                </h3>
                <div className="flex flex-col gap-4 font-mono text-sm">
                  <div className="flex justify-between border-b border-border/30 pb-2">
                    <span className="text-muted-foreground">Connection Pool</span>
                    <span className="text-emerald-500">42/50</span>
                  </div>
                  <div className="flex justify-between border-b border-border/30 pb-2">
                    <span className="text-muted-foreground">Transaction Rate</span>
                    <span className="text-foreground">1,204/sec</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Active Migrations</span>
                    <span className="text-foreground">0 pending</span>
                  </div>
                </div>
             </div>

             <div className="p-6 rounded-xl border border-border/50 bg-secondary/5">
                <h3 className="text-sm font-medium text-foreground uppercase tracking-wider mb-5 flex items-center gap-2">
                  <DatabaseBackup className="w-4 h-4 text-accent" />
                  Redis Caching Layer
                </h3>
                <div className="flex flex-col gap-4 font-mono text-sm">
                  <div className="flex justify-between border-b border-border/30 pb-2">
                    <span className="text-muted-foreground">Total Keys</span>
                    <span className="text-foreground">1.4M</span>
                  </div>
                  <div className="flex justify-between border-b border-border/30 pb-2">
                    <span className="text-muted-foreground">Memory Used</span>
                    <span className="text-foreground">2.4 GB / 8 GB</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Eviction Policy</span>
                    <span className="text-accent">volatile-lru</span>
                  </div>
                </div>
             </div>
          </div>

        </div>

        <div className="lg:col-span-1 flex flex-col gap-6">
          <div className="rounded-xl border border-border/50 bg-rose-500/5 p-5 flex-1 border-rose-500/20">
             <h3 className="text-sm font-medium text-rose-500 uppercase tracking-wider mb-4 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" />
                Dead Letter Queue (DLQ)
             </h3>
             <p className="text-xs text-muted-foreground mb-6">Jobs that have permanently failed beyond standard retry policies and require manual intervention.</p>
             
             <div className="flex flex-col gap-4 text-xs font-mono">
                {DEAD_LETTER_QUEUE.map((log, idx) => (
                  <div key={idx} className="flex flex-col gap-2 border-b border-border/30 pb-4 last:border-0 last:pb-0">
                    <div className="flex justify-between items-start text-rose-500/80">
                      <span>Job: {log.job_id}</span>
                      <span className="text-[10px] uppercase bg-rose-500/10 px-1 rounded">Retries: {log.retries}</span>
                    </div>
                    <div className="text-muted-foreground flex gap-2">
                      <span className="text-foreground">{log.queue}:</span> 
                      <span>{log.error}</span>
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
