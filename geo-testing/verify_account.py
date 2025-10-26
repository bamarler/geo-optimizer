"""
Verify which ChatGPT account is currently logged in
"""
from playwright.sync_api import sync_playwright
import os

print("=" * 70)
print("Checking which account is logged in...")
print("=" * 70)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state="storage/auth_state.json")
    page = context.new_page()
    
    print("\nNavigating to ChatGPT...")
    page.goto("https://chatgpt.com/")
    
    print("Waiting for page to load...")
    page.wait_for_timeout(3000)
    
    # Try to get account info
    try:
        # Look for account menu
        page.locator("#prompt-textarea").click()
        page.wait_for_timeout(1000)
        
        # Take a screenshot
        page.screenshot(path="account_check.png")
        print("\n✅ Screenshot saved to account_check.png")
        print("   Please check the screenshot to see which account is logged in")
        
    except Exception as e:
        print(f"\n⚠️  Could not check account: {e}")
    
    print("\n⏸️  Browser will stay open for 10 seconds so you can check...")
    page.wait_for_timeout(10000)
    
    browser.close()

print("\n" + "=" * 70)
print("Check complete!")
print("=" * 70)

