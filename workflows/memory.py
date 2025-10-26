from playwright.sync_api import Page
import time

def clear_memory(page: Page) -> None:
    """Clear all ChatGPT memory."""
    # Open user menu
    page.locator("#prompt-textarea").click()
    page.get_by_text("Example User").click()  # Adjust if your name differs
    
    # Navigate to Personalization
    page.get_by_role("menuitem", name="Personalization").click()
    page.get_by_role("button", name="Manage").click()
    
    # Clear memory
    page.get_by_test_id("reset-memories-button").click()
    page.get_by_test_id("confirm-reset-memories-button").click()
    
    # Close modals
    page.get_by_test_id("modal-memories").get_by_test_id("close-button").click()
    page.get_by_role("tablist").get_by_test_id("close-button").click()
    
    time.sleep(1)  # Let it settle

def set_persona(page: Page, persona_text: str) -> None:
    """Add persona to ChatGPT memory by chatting."""
    # Type persona in chat
    page.locator("#prompt-textarea").fill("Save this to memory: " + persona_text)
    page.get_by_test_id("send-button").click()
    
    # Wait for response
    page.wait_for_timeout(3000)
    
    # Start new chat to clear context
    page.goto("https://chatgpt.com/")
    page.locator("#prompt-textarea").wait_for(timeout=5000)