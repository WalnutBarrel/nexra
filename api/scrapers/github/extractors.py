import httpx
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class GithubExtractor:
    def extract_trending_html(self, html: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        repos = []
        
        for article in soup.find_all("article", class_="Box-row"):
            try:
                h2 = article.find("h2", class_="h3")
                a_tag = h2.find("a")
                repo_name = a_tag["href"].strip("/")
                
                desc_p = article.find("p", class_="col-9")
                description = desc_p.text.strip() if desc_p else ""
                
                # Try to parse stars
                div_f6 = article.find("div", class_="f6")
                stars = 0
                language = "Unknown"
                if div_f6:
                    lang_span = div_f6.find("span", itemprop="programmingLanguage")
                    if lang_span:
                        language = lang_span.text.strip()
                        
                    star_a = div_f6.find("a", href=lambda x: x and x.endswith("/stargazers"))
                    if star_a:
                        star_text = star_a.text.strip().replace(",", "")
                        if star_text.isdigit():
                            stars = int(star_text)
                            
                repos.append({
                    "name": repo_name,
                    "description": description,
                    "stars": stars,
                    "language": language
                })
            except Exception as e:
                logger.error(f"Error extracting Github repo: {e}")
                
        return repos

github_extractor = GithubExtractor()
