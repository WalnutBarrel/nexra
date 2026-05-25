import { Globe, Gauge, Lock, Search, Share2 } from "lucide-react";

interface WebsiteIntelligenceCardProps {
  domain: string;
  technologies: string[];
  seoScore: number;
  performanceScore: number;
  securityStatus: "secure" | "warning" | "critical";
  socialLinks: number;
}

export function WebsiteIntelligenceCard({
  domain,
  technologies,
  seoScore,
  performanceScore,
  securityStatus,
  socialLinks,
}: WebsiteIntelligenceCardProps) {
  const securityColor = 
    securityStatus === "secure" ? "text-emerald-500/80" : 
    securityStatus === "warning" ? "text-amber-500/80" : "text-rose-500/80";

  return (
    <div className="group relative flex flex-col rounded-xl border border-white/5 bg-[#111111] p-5 transition-all duration-300 hover:border-white/10 hover:shadow-sm hover:shadow-black/50">
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Globe className="w-4 h-4 text-muted-foreground" />
          <h3 className="text-base font-medium text-foreground">{domain}</h3>
        </div>
        <div className="flex items-center gap-1" title="Security Status">
          <Lock className={`w-3.5 h-3.5 ${securityColor}`} />
          <span className="text-xs text-muted-foreground capitalize">{securityStatus}</span>
        </div>
      </div>

      <div className="mb-4 flex flex-wrap gap-2">
        {technologies.map((tech) => (
          <span key={tech} className="rounded-md bg-secondary/30 px-2 py-0.5 text-xs text-muted-foreground border border-border/20">
            {tech}
          </span>
        ))}
      </div>

      <div className="mt-auto grid grid-cols-3 gap-2 pt-4 border-t border-border/30">
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-1 text-xs text-muted-foreground">
            <Search className="w-3 h-3" />
            SEO
          </div>
          <span className="text-sm font-medium text-foreground">{seoScore}/100</span>
        </div>
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-1 text-xs text-muted-foreground">
            <Gauge className="w-3 h-3" />
            Perf
          </div>
          <span className="text-sm font-medium text-foreground">{performanceScore}/100</span>
        </div>
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-1 text-xs text-muted-foreground">
            <Share2 className="w-3 h-3" />
            Social
          </div>
          <span className="text-sm font-medium text-foreground">{socialLinks} refs</span>
        </div>
      </div>
    </div>
  );
}
