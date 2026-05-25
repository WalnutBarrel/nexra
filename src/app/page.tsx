"use client";

import { useState } from "react";
import { SearchHero } from "@/components/SearchHero";
import { TrendingIntelligence } from "@/components/TrendingIntelligence";
import { LiveIngestionFeed } from "@/components/LiveIngestionFeed";
import { NewsIntelligenceCard } from "@/components/NewsIntelligenceCard";
import { WebsiteIntelligenceCard } from "@/components/WebsiteIntelligenceCard";
import { TrendIntelligenceCard } from "@/components/TrendIntelligenceCard";
import { SearchingState, NoResultsState } from "@/components/SearchStates";
import { IntelligenceApi } from "@/lib/api/client";

type SearchState = "empty" | "searching" | "results" | "no-results";

// Fallback data in case the backend API isn't running locally yet.
const FALLBACK_MOCK_NEWS = [
  {
    title: "Global Supply Chains Adopt Autonomous Agentic AI",
    source: "Nexra AI Ingestion",
    timestamp: "1 hour ago",
    summary: "New intelligence extracted from tech sector RSS feeds indicates a massive shift toward fully autonomous supply chain management systems powered by LLMs.",
    sentiment: "positive" as const,
    credibilityScore: 92,
    tags: ["Supply Chain", "Agentic AI"],
  }
];

export default function Home() {
  const [searchState, setSearchState] = useState<SearchState>("empty");
  const [currentQuery, setCurrentQuery] = useState("");
  const [newsData, setNewsData] = useState<any[]>([]);
  const [websiteData, setWebsiteData] = useState<any[]>([]);
  const [trendData, setTrendData] = useState<any[]>([]);
  const [queryIntent, setQueryIntent] = useState<string>("NEWS_INTELLIGENCE");

  const classifyLocalIntent = (q: string) => {
    const domainPattern = /([a-zA-Z0-9-]+\.(com|io|ai|dev|org|net|co|app))|^(https?:\/\/)/i;
    if (domainPattern.test(q)) return "domain";
    if (q.toLowerCase().includes("trend") || q.toLowerCase().includes("accelerat") || q.toLowerCase().includes("emerg") || q.toLowerCase().includes("tooling")) return "trend";
    return "news";
  };

  const handleSearch = async (query: string) => {
    setCurrentQuery(query);
    setSearchState("searching");
    
    try {
      // Connect to the real intelligence engine endpoint
      const response: any = await IntelligenceApi.search(query);
      
      if (query.toLowerCase().includes("none") || query.toLowerCase().includes("error")) {
        setSearchState("no-results");
      } else {
        setNewsData(response.news_results?.length ? response.news_results : (response.intent === "NEWS_INTELLIGENCE" ? FALLBACK_MOCK_NEWS : []));
        setWebsiteData(response.website_results || []);
        setTrendData(response.trend_results || []);
        setQueryIntent(response.intent || classifyLocalIntent(query).toUpperCase());
        setSearchState("results");
      }
    } catch (error) {
      console.error("Backend fetch failed, falling back to mock results", error);
      setTimeout(() => {
        setNewsData(FALLBACK_MOCK_NEWS);
        setSearchState("results");
      }, 1000);
    }
  };

  return (
    <div className="flex flex-col w-full pb-20">
      <SearchHero onSearch={handleSearch} />
      
      <div className="px-8 lg:px-12 max-w-7xl mx-auto w-full transition-all duration-500">
        {searchState === "empty" && (
          <div className="animate-in fade-in duration-500 grid grid-cols-1 lg:grid-cols-2 gap-12 mt-8">
            <LiveIngestionFeed />
            <TrendingIntelligence />
          </div>
        )}

        {searchState === "searching" && (
          <SearchingState queryType={classifyLocalIntent(currentQuery) as any} />
        )}

        {searchState === "no-results" && (
          <NoResultsState query={currentQuery} />
        )}

        {searchState === "results" && (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="mb-8 flex items-center justify-between">
              <h2 className="text-xl font-medium tracking-tight text-foreground">
                Intelligence Results for "{currentQuery}"
              </h2>
              <button 
                onClick={() => setSearchState("empty")}
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                Clear Search
              </button>
            </div>

            <div className={`grid grid-cols-1 lg:grid-cols-12 gap-8`}>
              
              {queryIntent === 'TREND_ANALYSIS' ? (
                <div className="lg:col-span-12 flex flex-col gap-6">
                  <div className="flex items-center gap-2 text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">
                    Empirical Trend Analysis
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {trendData.map((trend, idx) => (
                      <div key={idx} className="animate-in fade-in slide-in-from-bottom-4 fill-mode-backwards" style={{ animationDelay: `${idx * 150}ms` }}>
                        <TrendIntelligenceCard {...trend} />
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <>
                  <div className={`flex flex-col gap-6 ${queryIntent === 'DOMAIN_SCAN' ? 'lg:col-span-8 lg:order-1' : 'lg:col-span-4 lg:order-2'}`}>
                    <div className="flex items-center gap-2 text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">
                      Domain Intelligence
                    </div>
                    <div className="flex flex-col gap-4">
                      {websiteData.length > 0 ? websiteData.map((site, idx) => (
                        <div key={idx} className="animate-in fade-in slide-in-from-bottom-4 fill-mode-backwards" style={{ animationDelay: `${idx * 150 + 200}ms` }}>
                          <WebsiteIntelligenceCard {...site} />
                        </div>
                      )) : (
                        <div className="text-sm text-muted-foreground/80 p-5 border border-white/5 rounded-xl bg-[#111111] shadow-inner shadow-black/50">
                          <div className="flex items-center gap-2 mb-2 font-mono text-[10px] uppercase tracking-widest text-accent/80">
                            <span className="w-2 h-2 bg-accent/50 rounded-sm animate-pulse"></span>
                            Passive Inspection Active
                          </div>
                          Awaiting structured domain telemetry payload from scanning pipeline...
                        </div>
                      )}
                    </div>
                  </div>

                  <div className={`flex flex-col gap-6 ${queryIntent === 'DOMAIN_SCAN' ? 'lg:col-span-4 lg:order-2' : 'lg:col-span-8 lg:order-1'}`}>
                    <div className="flex items-center gap-2 text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">
                      {queryIntent === 'DOMAIN_SCAN' ? 'Contextual Signals' : 'News & Reports'}
                    </div>
                    <div className={`grid grid-cols-1 ${queryIntent === 'DOMAIN_SCAN' ? 'md:grid-cols-1' : 'md:grid-cols-2'} gap-6`}>
                      {newsData.length > 0 ? newsData.map((news, idx) => (
                        <div key={idx} className="animate-in fade-in slide-in-from-bottom-4 fill-mode-backwards" style={{ animationDelay: `${idx * 150}ms` }}>
                          <NewsIntelligenceCard {...news} />
                        </div>
                      )) : (
                        <div className="text-sm text-muted-foreground p-4 border border-white/5 rounded-xl bg-[#111111]">
                          No active contextual signals detected for target infrastructure.
                        </div>
                      )}
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
