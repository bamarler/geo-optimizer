from playwright.sync_api import Page
import time

def clear_memory(page: Page) -> None:
    """Clear all ChatGPT memory."""
    # Open user menu by clicking on avatar/profile button
    try:
        # Try multiple ways to open user menu
        try:
            # Method 1: Click on user button (more reliable)
            page.locator('button[id^="headlessui-menu-button"]').first.click()
        except:
            # Method 2: Click on profile/avatar area
            page.locator('[data-testid="profile-button"]').click()
        
        time.sleep(1)
        
        # Navigate to Personalization (Settings)
        page.get_by_role("menuitem", name="Personalization").click()
        time.sleep(1)
        
        page.get_by_role("button", name="Manage").click()
        time.sleep(1)
        
        # Clear memory
        page.get_by_test_id("reset-memories-button").click()
        time.sleep(0.5)
        
        page.get_by_test_id("confirm-reset-memories-button").click()
        time.sleep(1)
        
        # Close modals
        page.get_by_test_id("modal-memories").get_by_test_id("close-button").click()
        time.sleep(0.5)
        
        page.get_by_role("tablist").get_by_test_id("close-button").click()
        time.sleep(1)
        
    except Exception as e:
        print(f"Error in clear_memory: {e}")
        # Try to close any open modals
        try:
            page.keyboard.press("Escape")
            page.keyboard.press("Escape")
        except:
            pass
        raise

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