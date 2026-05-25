import asyncio
import logging
from typing import List

from api.scrapers.rss.parser import rss_parser_service
from api.scrapers.extractors.html import html_extractor_service
from api.ai.processor import ai_processing_service

logger = logging.getLogger(__name__)

class IngestionPipeline:
    """Orchestrator for the intelligence ingestion pipeline."""
    
    async def run_pipeline(self):
        """Run the end-to-end ingestion job."""
        logger.info("Starting intelligence ingestion pipeline run.")
        
        for source in rss_parser_service.registered_sources:
            try:
                # 1. Fetch & Parse RSS
                new_items = await rss_parser_service.process_feed(source["id"], source["url"])
                
                for item in new_items:
                    # 2. Extract clean HTML
                    html = await html_extractor_service.fetch_html(item["link"])
                    clean_article = html_extractor_service.extract_article(html)
                    
                    # 3. AI Processing
                    enriched_article = await ai_processing_service.process_article({
                        **item,
                        **clean_article,
                        "source_id": source["id"]
                    })
                    
                    # 4. Save to Database (Mocking DB insertion here)
                    logger.info(f"Successfully processed: {enriched_article['title']}")
                    
            except Exception as e:
                logger.error(f"Failed to process source {source['id']}: {str(e)}")
                # Log to scrape_logs DB table...

ingestion_pipeline = IngestionPipeline()
