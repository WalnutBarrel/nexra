from typing import List, Dict, Any
import hashlib

class GithubNormalizer:
    def normalize(self, repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        for rank, repo in enumerate(repos, 1):
            repo_id = hashlib.md5(f"github-{repo['name']}".encode()).hexdigest()
            normalized.append({
                "id": repo_id,
                "title": f"GitHub Trending: {repo['name']}",
                "summary": repo['description'],
                "source": "GitHub Trending",
                "url": f"https://github.com/{repo['name']}",
                "timestamp": "Live",
                "github_metrics": {
                    "stars": repo['stars'],
                    "language": repo['language'],
                    "rank": rank
                }
            })
        return normalized

github_normalizer = GithubNormalizer()
