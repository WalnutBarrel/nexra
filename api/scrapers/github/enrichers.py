from typing import List, Dict, Any

class GithubEnricher:
    def enrich(self, repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        enriched = []
        
        # AI Tooling and Developer Tooling keywords
        ai_keywords = ["llm", "ai", "agent", "gpt", "model", "inference", "prompt", "vector", "embedding", "rag"]
        dev_keywords = ["framework", "tool", "ide", "editor", "compiler", "bundler", "developer", "infrastructure", "platform", "react", "vue"]
        
        for repo in repos:
            desc_lower = repo.get("summary", "").lower()
            title_lower = repo.get("title", "").lower()
            lang_lower = repo["github_metrics"].get("language", "").lower()
            
            text_to_check = f"{desc_lower} {title_lower} {lang_lower}"
            
            is_ai = any(kw in text_to_check for kw in ai_keywords)
            is_dev = any(kw in text_to_check for kw in dev_keywords)
            
            if is_ai or is_dev:
                # Add tagging
                tags = []
                if is_ai: tags.append("AI Tooling")
                if is_dev: tags.append("Developer Tools")
                
                repo["tags"] = tags
                repo["category"] = "AI/Dev Infrastructure"
                enriched.append(repo)
                
        return enriched

github_enricher = GithubEnricher()
