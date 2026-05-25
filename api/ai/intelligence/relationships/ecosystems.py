from typing import List, Dict, Any

class EcosystemClassifier:
    def classify_ecosystem(self, entity_name: str, relationships: List[Dict[str, Any]]) -> str:
        """Determines the overarching ecosystem for an entity based on its name and relationships."""
        # Simple heuristic mapping for this lightweight phase
        name = entity_name.lower()
        
        ide_keywords = ["cursor", "windsurf", "copilot", "ide", "editor"]
        llm_infra_keywords = ["ollama", "vllm", "llama.cpp", "gguf", "inference"]
        agent_keywords = ["langgraph", "langchain", "autogen", "crewai", "agent"]
        
        if any(k in name for k in ide_keywords):
            return "AI IDE Tooling"
        if any(k in name for k in llm_infra_keywords):
            return "Local LLM Infrastructure"
        if any(k in name for k in agent_keywords):
            return "AI Agent Frameworks"
            
        # Check relationships
        for rel in relationships:
            rel_name = rel.get("entity_b", "").lower() if rel.get("entity_a", "").lower() == name else rel.get("entity_a", "").lower()
            if any(k in rel_name for k in ide_keywords):
                return "AI IDE Tooling"
            if any(k in rel_name for k in llm_infra_keywords):
                return "Local LLM Infrastructure"
            if any(k in rel_name for k in agent_keywords):
                return "AI Agent Frameworks"
                
        return "General AI Infrastructure"

ecosystem_classifier = EcosystemClassifier()
