"""
Quick check if current auth state is still valid
"""
from playwright.sync_api import sync_playwright
import os

print("Checking if auth state is valid...")

if not os.path.exists("storage/auth_state.json"):
    print("❌ No auth_state.json found")
    print("Please run: python scripts/record_login.py")
    exit(1)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    
    try:
        context = browser.new_context(storage_state="storage/auth_state.json")
        page = context.new_page()
        
        print("Navigating to ChatGPT...")
        page.goto("https://chatgpt.com/")
        
        print("Waiting for page to load...")
        page.wait_for_timeout(3000)
        
        # Check if we're logged in
        try:
            page.locator("#prompt-textarea").wait_for(timeout=5000)
            print("✅ Authentication is VALID! You're logged in.")
            print("✅ You can run: python run_tech_test.py")
        except:
            print("❌ Authentication is INVALID or expired")
            print("Please run: python scripts/record_login.py")
        
        page.wait_for_timeout(2000)
        
    finally:
        browser.close()

