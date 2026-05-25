from typing import List, Dict, Any
import hashlib

class RedditNormalizer:
    def normalize(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        for post in posts:
            post_id = hashlib.md5(f"reddit-{post['subreddit']}-{post['permalink']}".encode()).hexdigest()
            normalized.append({
                "id": post_id,
                "title": post['title'],
                "summary": f"Discussion on r/{post['subreddit']} with {post['num_comments']} comments and {post['score']} upvotes.",
                "source": f"Reddit: r/{post['subreddit']}",
                "url": f"https://www.reddit.com{post['permalink']}",
                "timestamp": "Live",
                "reddit_metrics": {
                    "score": post['score'],
                    "comments": post['num_comments'],
                    "subreddit": post['subreddit']
                }
            })
        return normalized

reddit_normalizer = RedditNormalizer()
