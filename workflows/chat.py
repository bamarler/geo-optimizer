from playwright.sync_api import Page
from typing import Dict
import time

def send_prompt(page: Page, prompt: str) -> None:
    """Send a prompt to ChatGPT."""
    page.locator("#prompt-textarea").fill(prompt)
    page.get_by_test_id("send-button").click()

def extract_response(page: Page, turn_number: int = 2) -> Dict[str, any]:
    """
    Extract response text and citations from ChatGPT.
    
    Args:
        turn_number: Which conversation turn to extract (2 = first response)
    
    Returns:
        Dict with 'text', 'citations', and 'has_citations'
    """
    # Wait for response to appear
    response_locator = page.get_by_test_id(f"conversation-turn-{turn_number}")
    response_locator.wait_for(timeout=60000)
    
    # Wait a bit more for citations to load
    time.sleep(2)
    
    # Extract text
    response_text = response_locator.inner_text()
    
    # Extract citations (links in response)
    citations = []
    citation_links = response_locator.locator("a[href]").all()
    
    for idx, link in enumerate(citation_links, 1):
        try:
            url = link.get_attribute("href")
            title = link.inner_text() or f"Citation {idx}"
            citations.append({
                "position": idx,
                "title": title,
                "url": url
            })
        except Exception:
            pass
    
    return {
        "text": response_text,
        "citations": citations,
        "has_citations": len(citations) > 0
    }