"use client";

import { useState } from "react";
import { SearchHero } from "@/components/SearchHero";
import { TrendingIntelligence } from "@/components/TrendingIntelligence";
import { LiveIngestionFeed } from "@/components/LiveIngestionFeed";
import { NewsIntelligenceCard } from "@/components/NewsIntelligenceCard";
import { WebsiteIntelligenceCard } from "@/components/WebsiteIntelligenceCard";
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

  const handleSearch = async (query: string) => {
    setCurrentQuery(query);
    setSearchState("searching");
    
    try {
      // Connect to the real intelligence engine endpoint
      const response: any = await IntelligenceApi.search(query);
      
      // We expect the backend to return { results_count: int, news_results: [], website_results: [] }
      // For this mock phase, we'll populate the data natively if the API returns empty arrays
      if (query.toLowerCase().includes("none") || query.toLowerCase().includes("error")) {
        setSearchState("no-results");
      } else {
        setNewsData(response.news_results?.length ? response.news_results : FALLBACK_MOCK_NEWS);
        setWebsiteData(response.website_results || []);
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
          <SearchingState />
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

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              <div className="lg:col-span-8 flex flex-col gap-6">
                <div className="flex items-center gap-2 text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">
                  News & Reports
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {newsData.map((news, idx) => (
                    <NewsIntelligenceCard key={idx} {...news} />
                  ))}
                </div>
              </div>
              
              <div className="lg:col-span-4 flex flex-col gap-6">
                <div className="flex items-center gap-2 text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">
                  Domain Intelligence
                </div>
                <div className="flex flex-col gap-4">
                  {websiteData.length > 0 ? websiteData.map((site, idx) => (
                    <WebsiteIntelligenceCard key={idx} {...site} />
                  )) : (
                    <div className="text-sm text-muted-foreground p-4 border border-border/50 rounded-xl bg-secondary/5">
                      No domain telemetry generated for this query.
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
