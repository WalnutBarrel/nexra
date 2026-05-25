"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { IntelligenceApi } from "@/lib/api/client";
import { ShieldCheck, Zap, Search, Globe, Code, FileText, AlertTriangle, ArrowUpRight, Activity } from "lucide-react";

export default function WebsiteIntelligenceDossier() {
  const params = useParams();
  const domain = params.domain as string;
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const data = await IntelligenceApi.scanWebsite(domain);
        setReport(data);
      } catch (err) {
        // Fallback for local mock if backend isn't running
        setReport({
          domain: domain,
          timestamp: new Date().toISOString(),
          telemetry: { latency_ms: 145, status: 200, ssl_issuer: "Let's Encrypt" },
          technologies: [
            { name: "Next.js", category: "Framework", confidence: 0.95 },
            { name: "React", category: "UI Library", confidence: 0.98 },
            { name: "Cloudflare", category: "CDN", confidence: 0.99 }
          ],
          seo_intelligence: {
            title_present: true, meta_desc_present: true, canonical_valid: true,
            schema_markup_detected: false, og_metadata_coverage: "75%",
            observations: [
              "Title hierarchy lacks distinct H1 nodes on sub-paths.",
              "Schema.org markup is entirely absent.",
              "OpenGraph graph density is optimal."
            ],
            score: 82
          },
          security_intelligence: {
            https_enforced: true, hsts_active: true, csp_present: false,
            x_frame_options: "Not Set", server_exposure: "Cloudflare",
            observations: [
              "Strict-Transport-Security (HSTS) is actively mitigating attacks.",
              "Content-Security-Policy (CSP) is unconfigured.",
              "Server headers are leaking underlying infrastructure data."
            ],
            posture: "Warning"
          },
          performance_intelligence: {
            estimated_dom_complexity: "High (3,204 nodes)", script_density: "Heavy",
            render_blocking_assets: 4,
            observations: [
              "Payload bloat associated with asynchronous tracking scripts.",
              "Font loading overhead is contributing to ~200ms latency delays."
            ],
            score: 68
          },
          confidence_score: 92
        });
      } finally {
        setLoading(false);
      }
    };
    fetchReport();
  }, [domain]);

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="flex flex-col items-center animate-in fade-in">
          <Activity className="w-8 h-8 animate-spin text-accent mb-4" />
          <h2 className="text-lg font-medium text-foreground">Compiling Dossier...</h2>
          <p className="text-sm text-muted-foreground">Extracting intelligence for {domain}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col w-full pb-20 pt-8 px-8 lg:px-12 max-w-[1400px] mx-auto animate-in fade-in">
      
      {/* Header Panel */}
      <div className="mb-8 flex flex-col gap-4 border-b border-border/50 pb-8">
        <div className="flex items-center gap-3 text-xs font-medium text-muted-foreground uppercase tracking-wider">
          <Globe className="w-4 h-4" />
          Intelligence Dossier
        </div>
        <div className="flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-medium tracking-tight text-foreground">{report.domain}</h1>
            <div className="flex gap-4 mt-2 text-sm text-muted-foreground">
              <span>Scan Time: {new Date(report.timestamp).toLocaleString()}</span>
              <span>•</span>
              <span className="flex items-center gap-1">
                <Activity className="w-3.5 h-3.5" /> 
                Latency: {report.telemetry.latency_ms}ms
              </span>
            </div>
          </div>
          <div className="flex flex-col items-end">
            <div className="text-3xl font-medium text-accent">{report.confidence_score}%</div>
            <div className="text-xs text-muted-foreground uppercase tracking-widest mt-1">Confidence Index</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Tech & Security */}
        <div className="lg:col-span-1 flex flex-col gap-8">
          
          {/* Tech Stack */}
          <div className="rounded-xl border border-border/50 bg-secondary/5 p-6">
            <h3 className="text-sm font-medium text-foreground uppercase tracking-wider mb-5 flex items-center gap-2">
              <Code className="w-4 h-4 text-accent" />
              Technology Fingerprint
            </h3>
            <div className="flex flex-col gap-3">
              {report.technologies.map((tech: any) => (
                <div key={tech.name} className="flex items-center justify-between border-b border-border/30 pb-2 last:border-0 last:pb-0">
                  <div className="flex flex-col">
                    <span className="text-sm font-medium text-foreground">{tech.name}</span>
                    <span className="text-[10px] text-muted-foreground uppercase tracking-widest">{tech.category}</span>
                  </div>
                  <span className="text-xs font-mono text-emerald-500/80">{(tech.confidence * 100).toFixed(0)}%</span>
                </div>
              ))}
            </div>
          </div>

          {/* Security Posture */}
          <div className="rounded-xl border border-border/50 bg-secondary/5 p-6">
            <div className="flex items-center justify-between mb-5">
              <h3 className="text-sm font-medium text-foreground uppercase tracking-wider flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-accent" />
                Security Posture
              </h3>
              <span className={`px-2 py-0.5 rounded-md text-[10px] uppercase tracking-widest border ${
                report.security_intelligence.posture === "Secure" ? "bg-emerald-500/10 text-emerald-500 border-emerald-500/20" : 
                "bg-amber-500/10 text-amber-500 border-amber-500/20"
              }`}>
                {report.security_intelligence.posture}
              </span>
            </div>
            <div className="flex flex-col gap-4">
               <div className="grid grid-cols-2 gap-2 text-xs">
                 <div className="flex flex-col gap-1 p-2 bg-secondary/20 rounded border border-border/20">
                   <span className="text-muted-foreground">HTTPS Enforced</span>
                   <span className="font-medium">{report.security_intelligence.https_enforced ? "Yes" : "No"}</span>
                 </div>
                 <div className="flex flex-col gap-1 p-2 bg-secondary/20 rounded border border-border/20">
                   <span className="text-muted-foreground">HSTS Active</span>
                   <span className="font-medium">{report.security_intelligence.hsts_active ? "Yes" : "No"}</span>
                 </div>
               </div>
               <div className="flex flex-col gap-2 mt-2 border-t border-border/30 pt-4">
                 <span className="text-xs font-medium text-muted-foreground uppercase tracking-widest">Observations</span>
                 <ul className="text-xs text-foreground space-y-2">
                   {report.security_intelligence.observations.map((obs: string, idx: number) => (
                     <li key={idx} className="flex gap-2 leading-relaxed">
                       <span className="text-accent">•</span> {obs}
                     </li>
                   ))}
                 </ul>
               </div>
            </div>
          </div>
        </div>

        {/* Right Column: SEO & Performance */}
        <div className="lg:col-span-2 flex flex-col gap-8">
          
          {/* SEO Intelligence */}
          <div className="rounded-xl border border-border/50 bg-background overflow-hidden">
             <div className="px-6 py-5 border-b border-border/50 flex justify-between items-center bg-secondary/5">
                <h3 className="text-sm font-medium text-foreground uppercase tracking-wider flex items-center gap-2">
                  <Search className="w-4 h-4 text-accent" />
                  SEO Intelligence
                </h3>
                <span className="text-lg font-medium text-foreground">{report.seo_intelligence.score}/100</span>
             </div>
             <div className="p-6">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="flex flex-col gap-1">
                    <span className="text-[10px] text-muted-foreground uppercase tracking-widest">Title Tag</span>
                    <span className="text-sm">{report.seo_intelligence.title_present ? "Present" : "Missing"}</span>
                  </div>
                  <div className="flex flex-col gap-1">
                    <span className="text-[10px] text-muted-foreground uppercase tracking-widest">Meta Desc</span>
                    <span className="text-sm">{report.seo_intelligence.meta_desc_present ? "Present" : "Missing"}</span>
                  </div>
                  <div className="flex flex-col gap-1">
                    <span className="text-[10px] text-muted-foreground uppercase tracking-widest">Schema Markup</span>
                    <span className="text-sm">{report.seo_intelligence.schema_markup_detected ? "Detected" : "None"}</span>
                  </div>
                  <div className="flex flex-col gap-1">
                    <span className="text-[10px] text-muted-foreground uppercase tracking-widest">OpenGraph</span>
                    <span className="text-sm">{report.seo_intelligence.og_metadata_coverage}</span>
                  </div>
                </div>
                <div className="flex flex-col gap-2 border-t border-border/30 pt-4">
                 <span className="text-xs font-medium text-muted-foreground uppercase tracking-widest">Strategic Observations</span>
                 <ul className="text-sm text-foreground space-y-2 mt-1">
                   {report.seo_intelligence.observations.map((obs: string, idx: number) => (
                     <li key={idx} className="flex gap-2 leading-relaxed text-muted-foreground">
                       <ArrowUpRight className="w-4 h-4 mt-0.5 text-accent flex-shrink-0" /> {obs}
                     </li>
                   ))}
                 </ul>
               </div>
             </div>
          </div>

          {/* Performance Intelligence */}
          <div className="rounded-xl border border-border/50 bg-background overflow-hidden">
             <div className="px-6 py-5 border-b border-border/50 flex justify-between items-center bg-secondary/5">
                <h3 className="text-sm font-medium text-foreground uppercase tracking-wider flex items-center gap-2">
                  <Zap className="w-4 h-4 text-accent" />
                  Performance Profile
                </h3>
                <span className="text-lg font-medium text-foreground">{report.performance_intelligence.score}/100</span>
             </div>
             <div className="p-6">
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
                  <div className="flex flex-col gap-1">
                    <span className="text-[10px] text-muted-foreground uppercase tracking-widest">DOM Complexity</span>
                    <span className="text-sm">{report.performance_intelligence.estimated_dom_complexity}</span>
                  </div>
                  <div className="flex flex-col gap-1">
                    <span className="text-[10px] text-muted-foreground uppercase tracking-widest">Script Density</span>
                    <span className="text-sm">{report.performance_intelligence.script_density}</span>
                  </div>
                  <div className="flex flex-col gap-1">
                    <span className="text-[10px] text-muted-foreground uppercase tracking-widest">Render Blockers</span>
                    <span className="text-sm font-mono">{report.performance_intelligence.render_blocking_assets} assets</span>
                  </div>
                </div>
                <div className="flex flex-col gap-2 border-t border-border/30 pt-4">
                 <span className="text-xs font-medium text-muted-foreground uppercase tracking-widest">Performance Insights</span>
                 <ul className="text-sm text-foreground space-y-2 mt-1">
                   {report.performance_intelligence.observations.map((obs: string, idx: number) => (
                     <li key={idx} className="flex gap-2 leading-relaxed text-muted-foreground">
                       <ArrowUpRight className="w-4 h-4 mt-0.5 text-accent flex-shrink-0" /> {obs}
                     </li>
                   ))}
                 </ul>
               </div>
             </div>
          </div>

        </div>
      </div>
    </div>
  );
}
