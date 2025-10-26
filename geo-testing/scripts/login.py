#!/usr/bin/env python3
"""
Interactive ChatGPT Login Script

Two methods:
1. MANUAL LOGIN (Recommended) - You login manually, we save the session
2. AUTOMATED LOGIN - Uses credentials from .env file

Usage:
    python scripts/login.py --manual     # Manual login (safer)
    python scripts/login.py --auto       # Auto login with credentials from .env
"""
import os
import sys
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()


def manual_login():
    """
    Opens browser, lets you login manually, then saves the session
    Best for security - no passwords in code
    """
    print("=" * 80)
    print("🔐 MANUAL CHATGPT LOGIN")
    print("=" * 80)
    print()
    print("Instructions:")
    print("1. Browser will open to ChatGPT")
    print("2. Please login manually")
    print("3. Wait until you see the chat interface")
    print("4. Press ENTER in this terminal when done")
    print()
    input("Press ENTER to start...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        
        print("\n🌐 Opening ChatGPT...")
        page.goto("https://chatgpt.com/")
        
        print("\n👤 Please login in the browser window...")
        print("⏳ Waiting for you to complete login...")
        
        input("\n✅ Press ENTER when you're logged in and see the chat interface: ")
        
        # Verify login
        try:
            page.locator("#prompt-textarea").wait_for(timeout=5000)
            print("\n✅ Login verified!")
        except:
            print("\n⚠️  Couldn't verify login. Saving anyway...")
        
        # Save auth state
        os.makedirs("storage", exist_ok=True)
        context.storage_state(path="storage/auth_state.json")
        
        print("\n💾 Session saved to: storage/auth_state.json")
        print("✅ You're all set! Run your tests now.")
        
        context.close()
        browser.close()


def auto_login():
    """
    Automated login using credentials from .env file
    Requires: CHATGPT_EMAIL and CHATGPT_PASSWORD in .env
    """
    email = os.getenv("CHATGPT_EMAIL")
    password = os.getenv("CHATGPT_PASSWORD")
    
    if not email or not password:
        print("❌ Missing credentials!")
        print()
        print("Add these to your .env file:")
        print("  CHATGPT_EMAIL=your@email.com")
        print("  CHATGPT_PASSWORD=yourpassword")
        print()
        print("Or use manual login: python scripts/login.py --manual")
        sys.exit(1)
    
    print("=" * 80)
    print("🤖 AUTOMATED CHATGPT LOGIN")
    print("=" * 80)
    print(f"Email: {email[:3]}***{email[-10:]}")
    print()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        
        print("🌐 Opening ChatGPT...")
        page.goto("https://chatgpt.com/")
        page.wait_for_timeout(2000)
        
        try:
            print("👤 Clicking login button...")
            page.get_by_test_id("login-button").click()
            page.wait_for_timeout(1000)
            
            print("📧 Entering email...")
            page.get_by_role("textbox", name="Email address").fill(email)
            page.get_by_role("button", name="Continue", exact=True).click()
            page.wait_for_timeout(2000)
            
            print("🔑 Entering password...")
            page.get_by_role("textbox", name="Password").fill(password)
            page.get_by_role("button", name="Continue", exact=True).click()
            page.wait_for_timeout(5000)
            
            # Wait for chat interface
            print("⏳ Waiting for chat interface...")
            page.locator("#prompt-textarea").wait_for(timeout=15000)
            
            print("✅ Login successful!")
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            print()
            print("Possible issues:")
            print("  • Wrong credentials")
            print("  • 2FA enabled (use manual login instead)")
            print("  • ChatGPT UI changed")
            print()
            print("Try manual login: python scripts/login.py --manual")
            context.close()
            browser.close()
            sys.exit(1)
        
        # Save auth state
        os.makedirs("storage", exist_ok=True)
        context.storage_state(path="storage/auth_state.json")
        
        print("\n💾 Session saved to: storage/auth_state.json")
        print("✅ You're all set! Run your tests now.")
        
        page.wait_for_timeout(2000)
        context.close()
        browser.close()


if __name__ == "__main__":
    if "--auto" in sys.argv:
        auto_login()
    elif "--manual" in sys.argv:
        manual_login()
    else:
        print("Usage:")
        print("  python scripts/login.py --manual   # Manual login (recommended)")
        print("  python scripts/login.py --auto     # Auto login from .env")
        print()
        print("For automated login, add to .env:")
        print("  CHATGPT_EMAIL=your@email.com")
        print("  CHATGPT_PASSWORD=yourpassword")

