from playwright.sync_api import Page, BrowserContext

def load_auth_session(context: BrowserContext, page: Page) -> None:
    """Navigate to ChatGPT with existing auth session."""
    page.goto("https://chatgpt.com/")
    # Wait for chat interface to load
    page.locator("#prompt-textarea").wait_for(timeout=10000)