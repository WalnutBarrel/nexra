from typing import List, Dict, Any

class RedditExtractor:
    def extract_posts(self, json_data: Dict[str, Any], subreddit: str) -> List[Dict[str, Any]]:
        posts = []
        try:
            children = json_data.get("data", {}).get("children", [])
            for child in children:
                data = child.get("data", {})
                if data:
                    posts.append({
                        "title": data.get("title", ""),
                        "score": data.get("score", 0),
                        "num_comments": data.get("num_comments", 0),
                        "url": data.get("url", ""),
                        "created_utc": data.get("created_utc", 0),
                        "subreddit": subreddit,
                        "permalink": data.get("permalink", "")
                    })
        except Exception as e:
            pass
        return posts

reddit_extractor = RedditExtractor()
