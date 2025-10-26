#!/usr/bin/env python3
"""
Test the automated login functionality
"""
import os
import time
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

print("=" * 80)
print("🧪 TESTING AUTOMATED LOGIN")
print("=" * 80)

email = os.getenv("CHATGPT_EMAIL")
password = os.getenv("CHATGPT_PASSWORD")

if not email or not password:
    print("❌ Missing CHATGPT_EMAIL or CHATGPT_PASSWORD in .env")
    exit(1)

print(f"\n📧 Email: {email}")
print(f"🔑 Password: {'*' * len(password)}")
print()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    page = context.new_page()
    
    try:
        print("🌐 Opening ChatGPT...")
        page.goto("https://chatgpt.com/")
        time.sleep(2)
        
        # Check if already logged in
        try:
            page.locator("#prompt-textarea").wait_for(timeout=3000)
            print("✅ Already logged in! (Cookies from previous session)")
        except:
            # Need to login
            print("🔐 Not logged in. Starting login process...")
            
            try:
                # Click login button
                print("  → Clicking login button...")
                page.get_by_test_id("login-button").click(timeout=5000)
                time.sleep(2)
                
                # Enter email
                print("  → Entering email...")
                page.get_by_role("textbox", name="Email address").fill(email)
                page.get_by_role("button", name="Continue", exact=True).click()
                time.sleep(2)
                
                # Enter password
                print("  → Entering password...")
                page.get_by_role("textbox", name="Password").fill(password)
                page.get_by_role("button", name="Continue", exact=True).click()
                time.sleep(5)
                
                # Wait for chat interface
                print("  → Waiting for chat interface...")
                page.locator("#prompt-textarea").wait_for(timeout=15000)
                
                print("\n✅ LOGIN SUCCESSFUL!")
                print("✅ Chat interface loaded!")
                
            except Exception as e:
                print(f"\n❌ LOGIN FAILED: {e}")
                print()
                print("Possible issues:")
                print("  • Wrong credentials in .env")
                print("  • 2FA enabled (disable or use manual login)")
                print("  • ChatGPT UI changed")
                print("  • Network issue")
                exit(1)
        
        # Verify we can interact with chat
        print("\n🧪 Testing chat interaction...")
        textarea = page.locator("#prompt-textarea")
        textarea.fill("Hi! Just testing.")
        print("✅ Can type in chat input!")
        
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ The automated login works perfectly!")
        print("\n📝 You can now run the full GEO test:")
        print("   python run_from_db.py <persona_set_id> <prompts_id>")
        
        time.sleep(3)
        
    finally:
        browser.close()

print("\n" + "=" * 80)

