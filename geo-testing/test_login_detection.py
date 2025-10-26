#!/usr/bin/env python3
"""
Test the improved login detection logic
"""
import os
import time
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

print("=" * 80)
print("🧪 TESTING IMPROVED LOGIN DETECTION")
print("=" * 80)

email = os.getenv("CHATGPT_EMAIL")
password = os.getenv("CHATGPT_PASSWORD")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    # Fresh context - no cookies
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    page = context.new_page()
    
    try:
        print("\n🌐 Opening ChatGPT (fresh browser, no login)...")
        page.goto("https://chatgpt.com/")
        time.sleep(3)
        
        # Test the detection logic
        print("\n🔍 Step 1: Check if 'Log in' button is visible...")
        login_needed = False
        try:
            login_button = page.get_by_role("button", name="Log in")
            if login_button.is_visible(timeout=2000):
                login_needed = True
                print("  ✅ DETECTED: 'Log in' button is visible")
                print("  ✅ Correctly identified: NOT logged in")
        except Exception as e:
            print(f"  ⚠️ No 'Log in' button found: {e}")
        
        if not login_needed:
            print("\n🔍 Step 2: Verify by checking textarea...")
            try:
                page.locator("#prompt-textarea").wait_for(timeout=3000)
                print("  ✅ Textarea found, user is logged in")
            except:
                login_needed = True
                print("  ⚠️ Textarea not found, need to login")
        
        if login_needed:
            print("\n✅ DETECTION PASSED: Correctly identified login is needed")
            print("\n🔐 Now testing actual login flow...")
            
            try:
                # Click login
                page.get_by_role("button", name="Log in").click(timeout=5000)
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
                
                # Verify login
                print("  → Waiting for chat interface...")
                page.locator("#prompt-textarea").wait_for(timeout=15000)
                print("\n✅ LOGIN SUCCESSFUL!")
                
                # Final verification
                print("\n🔍 Final verification...")
                textarea = page.locator("#prompt-textarea")
                if textarea.is_visible():
                    print("✅ Textarea is visible and interactable")
                    print("\n🎉 ALL TESTS PASSED!")
                    print("✅ Login detection works correctly")
                    print("✅ Login flow works correctly")
                    print("✅ Ready for production use!")
                else:
                    print("❌ Textarea not visible after login")
                    
            except Exception as e:
                print(f"\n❌ Login failed: {e}")
                page.screenshot(path="detection_test_failed.png")
        else:
            print("\n⚠️ UNEXPECTED: Already logged in (cookies from previous session)")
        
        time.sleep(3)
        
    finally:
        browser.close()

print("\n" + "=" * 80)

