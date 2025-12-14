"""
Content Enrichment Service for the textbook generation system.

This module implements integration with external educational content sources like
Wikipedia, arXiv, and Open Educational Resources to enrich textbook material.
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import quote
import aiohttp
import requests


class ContentEnrichmentService:
    """
    Service class for enriching textbook content with information from external educational sources.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def enrich_content(self,
                           topic: str,
                           content: str,
                           sources: List[str] = None,
                           max_results: int = 5) -> Dict[str, Any]:
        """
        Enrich content with information from specified sources.

        Args:
            topic: The main topic to search for
            content: The existing content to enrich
            sources: List of sources to use (e.g., ['wikipedia', 'arxiv'])
            max_results: Maximum number of results to return

        Returns:
            Dictionary containing enriched content and metadata
        """
        if sources is None:
            sources = ['wikipedia']  # Default source

        enriched_data = {
            'original_content': content,
            'enriched_content': content,
            'sources_used': [],
            'references': [],
            'metadata': {}
        }

        for source in sources:
            try:
                if source.lower() == 'wikipedia':
                    wiki_data = await self._search_wikipedia(topic, max_results)
                    enriched_data = self._integrate_wikipedia_data(enriched_data, wiki_data)
                    enriched_data['sources_used'].append('wikipedia')
                elif source.lower() == 'arxiv':
                    arxiv_data = await self._search_arxiv(topic, max_results)
                    enriched_data = self._integrate_arxiv_data(enriched_data, arxiv_data)
                    enriched_data['sources_used'].append('arxiv')
                elif source.lower() == 'oer':
                    oer_data = await self._search_oer(topic, max_results)
                    enriched_data = self._integrate_oer_data(enriched_data, oer_data)
                    enriched_data['sources_used'].append('oer')
            except Exception as e:
                self.logger.warning(f"Failed to enrich content from {source}: {str(e)}")

        return enriched_data

    async def _search_wikipedia(self, topic: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search Wikipedia for information related to the topic.

        Args:
            topic: The topic to search for
            max_results: Maximum number of results to return

        Returns:
            List of Wikipedia search results
        """
        search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(topic)}"

        try:
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{
                        'title': data.get('title', ''),
                        'extract': data.get('extract', ''),
                        'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                        'source': 'wikipedia'
                    }]
                else:
                    # If direct search fails, try search API
                    search_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={quote(topic)}&srlimit={max_results}"
                    async with self.session.get(search_url) as search_response:
                        if search_response.status == 200:
                            search_data = await search_response.json()
                            results = []
                            for item in search_data.get('query', {}).get('search', [])[:max_results]:
                                results.append({
                                    'title': item.get('title', ''),
                                    'extract': item.get('snippet', ''),
                                    'url': f"https://en.wikipedia.org/wiki/{quote(item.get('title', ''))}",
                                    'source': 'wikipedia'
                                })
                            return results
        except Exception as e:
            self.logger.error(f"Error searching Wikipedia: {str(e)}")
            return []

    async def _search_arxiv(self, topic: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search arXiv for academic papers related to the topic.

        Args:
            topic: The topic to search for
            max_results: Maximum number of results to return

        Returns:
            List of arXiv search results
        """
        search_url = f"http://export.arxiv.org/api/query?search_query=all:{quote(topic)}&start=0&max_results={max_results}"

        try:
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    import xml.etree.ElementTree as ET
                    content = await response.text()
                    root = ET.fromstring(content)

                    # Define namespaces
                    ns = {
                        'atom': 'http://www.w3.org/2005/Atom',
                        'arxiv': 'http://arxiv.org/schemas/atom'
                    }

                    results = []
                    for entry in root.findall('atom:entry', ns):
                        title = entry.find('atom:title', ns).text if entry.find('atom:title', ns) is not None else ''
                        summary = entry.find('atom:summary', ns).text if entry.find('atom:summary', ns) is not None else ''
                        url = ''
                        for link in entry.findall('atom:link', ns):
                            if link.get('type') == 'text/html':
                                url = link.get('href', '')
                                break

                        results.append({
                            'title': title,
                            'summary': summary,
                            'url': url,
                            'source': 'arxiv'
                        })

                    return results
        except Exception as e:
            self.logger.error(f"Error searching arXiv: {str(e)}")
            return []

    async def _search_oer(self, topic: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search Open Educational Resources for educational content related to the topic.

        Args:
            topic: The topic to search for
            max_results: Maximum number of results to return

        Returns:
            List of OER search results
        """
        # For this implementation, we'll use a placeholder approach
        # In a real implementation, we would connect to OER repositories
        results = []

        # Placeholder implementation - in reality, this would connect to OER APIs
        for i in range(min(2, max_results)):  # Limit to 2 for demo
            results.append({
                'title': f"Open Educational Resource for {topic} - Part {i+1}",
                'content': f"This is educational content related to {topic} from open educational resources.",
                'url': f"https://example-oer.com/{topic.replace(' ', '-')}-{i+1}",
                'source': 'oer'
            })

        return results

    def _integrate_wikipedia_data(self, enriched_data: Dict[str, Any], wiki_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Integrate Wikipedia data into the enriched content.

        Args:
            enriched_data: Current enriched data
            wiki_data: Wikipedia search results

        Returns:
            Updated enriched data
        """
        for item in wiki_data:
            reference = {
                'title': item['title'],
                'url': item['url'],
                'source': item['source'],
                'type': 'factual_information'
            }
            enriched_data['references'].append(reference)

            # Add a note about the Wikipedia source to the content
            if item.get('extract'):
                enriched_data['enriched_content'] += f"\n\nWikipedia Summary: {item['extract']}\n\n"

        return enriched_data

    def _integrate_arxiv_data(self, enriched_data: Dict[str, Any], arxiv_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Integrate arXiv data into the enriched content.

        Args:
            enriched_data: Current enriched data
            arxiv_data: arXiv search results

        Returns:
            Updated enriched data
        """
        for item in arxiv_data:
            reference = {
                'title': item['title'],
                'url': item['url'],
                'source': item['source'],
                'type': 'academic_paper'
            }
            enriched_data['references'].append(reference)

            # Add a note about the arXiv source to the content
            if item.get('summary'):
                enriched_data['enriched_content'] += f"\n\nAcademic Paper Summary: {item['summary']}\n\n"

        return enriched_data

    def _integrate_oer_data(self, enriched_data: Dict[str, Any], oer_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Integrate OER data into the enriched content.

        Args:
            enriched_data: Current enriched data
            oer_data: OER search results

        Returns:
            Updated enriched data
        """
        for item in oer_data:
            reference = {
                'title': item['title'],
                'url': item['url'],
                'source': item['source'],
                'type': 'educational_resource'
            }
            enriched_data['references'].append(reference)

            # Add OER content to the enriched content
            if item.get('content'):
                enriched_data['enriched_content'] += f"\n\nEducational Resource: {item['content']}\n\n"

        return enriched_data

    async def get_topic_overview(self, topic: str) -> Optional[Dict[str, Any]]:
        """
        Get a general overview of a topic from educational sources.

        Args:
            topic: The topic to get an overview for

        Returns:
            Dictionary with topic overview information
        """
        try:
            # Try Wikipedia first for a general overview
            wiki_results = await self._search_wikipedia(topic, max_results=1)
            if wiki_results:
                return {
                    'title': wiki_results[0]['title'],
                    'summary': wiki_results[0]['extract'],
                    'url': wiki_results[0]['url'],
                    'source': 'wikipedia',
                    'reliability': 'high'
                }

            # If no Wikipedia result, try OER
            oer_results = await self._search_oer(topic, max_results=1)
            if oer_results:
                return {
                    'title': oer_results[0]['title'],
                    'summary': oer_results[0]['content'],
                    'url': oer_results[0]['url'],
                    'source': 'oer',
                    'reliability': 'medium'
                }

        except Exception as e:
            self.logger.error(f"Error getting topic overview: {str(e)}")

        return None

    async def validate_source_reliability(self, url: str) -> Dict[str, Any]:
        """
        Validate the reliability of a source URL.

        Args:
            url: The URL to validate

        Returns:
            Dictionary with reliability information
        """
        # This is a simplified implementation
        # In a real system, this would check domain reputation, update frequency, etc.
        reliability_indicators = {
            'wikipedia.org': {'reliability': 'high', 'authority': 'crowd_sourced'},
            'arxiv.org': {'reliability': 'high', 'authority': 'academic'},
            'edu': {'reliability': 'high', 'authority': 'educational'},
            'org': {'reliability': 'medium', 'authority': 'organization'},
            'com': {'reliability': 'variable', 'authority': 'commercial'}
        }

        domain_parts = url.lower().split('.')
        reliability = 'low'
        authority = 'unknown'

        for key, value in reliability_indicators.items():
            if key in url:
                reliability = value['reliability']
                authority = value['authority']
                break

        return {
            'url': url,
            'reliability': reliability,
            'authority': authority,
            'valid': reliability in ['high', 'medium']
        }


# Example usage:
# async def main():
#     service = ContentEnrichmentService()
#     enriched = await service.enrich_content("Machine Learning", "Basic content", ["wikipedia"])
#     print(f"Enriched content from: {enriched['sources_used']}")