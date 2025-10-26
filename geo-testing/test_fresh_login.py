#!/usr/bin/env python3
"""
Test fresh login - clears all cookies first to test real login flow
"""
import os
import time
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

print("=" * 80)
print("🧪 TESTING FRESH LOGIN (No Cached Cookies)")
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
    
    # NO storage_state = fresh browser with no cookies
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    page = context.new_page()
    
    try:
        print("🌐 Opening ChatGPT (fresh browser, no cookies)...")
        page.goto("https://chatgpt.com/")
        time.sleep(3)
        
        print("🔐 Starting login process...")
        
        try:
            # Click login button
            print("  Step 1: Looking for login button...")
            login_button = page.get_by_test_id("login-button")
            if login_button.is_visible(timeout=5000):
                print("  ✅ Found login button")
                login_button.click()
                time.sleep(2)
            else:
                print("  ⚠️ Login button not visible")
            
            # Enter email
            print("  Step 2: Entering email...")
            email_field = page.get_by_role("textbox", name="Email address")
            email_field.wait_for(timeout=5000)
            email_field.fill(email)
            print(f"  ✅ Entered email: {email}")
            
            continue_btn = page.get_by_role("button", name="Continue", exact=True)
            continue_btn.click()
            time.sleep(3)
            
            # Enter password
            print("  Step 3: Entering password...")
            password_field = page.get_by_role("textbox", name="Password")
            password_field.wait_for(timeout=5000)
            password_field.fill(password)
            print("  ✅ Entered password")
            
            password_continue = page.get_by_role("button", name="Continue", exact=True)
            password_continue.click()
            print("  ⏳ Waiting for login to complete...")
            time.sleep(8)
            
            # Wait for chat interface
            print("  Step 4: Checking if chat interface loaded...")
            try:
                page.locator("#prompt-textarea").wait_for(timeout=15000)
                print("\n✅ SUCCESS! LOGIN WORKED!")
                print("✅ Chat interface loaded!")
                
                # Test typing
                print("\n🧪 Testing chat interaction...")
                textarea = page.locator("#prompt-textarea")
                textarea.fill("Hi! Just testing.")
                print("✅ Can type in chat input!")
                
                print("\n🎉 FRESH LOGIN TEST PASSED!")
                print("✅ The automated login works perfectly without cached cookies!")
                
            except Exception as e:
                print(f"\n❌ FAILED to load chat interface: {e}")
                print("\nCurrent page URL:", page.url)
                print("\nTaking screenshot for debugging...")
                page.screenshot(path="login_failed.png")
                print("Screenshot saved: login_failed.png")
                
                # Check for any error messages
                error_text = page.locator("text=error", {"hasText": True}).all()
                if error_text:
                    print("\nFound error messages:")
                    for err in error_text:
                        print(f"  - {err.inner_text()}")
                
                exit(1)
            
        except Exception as e:
            print(f"\n❌ LOGIN FAILED: {e}")
            print()
            print("Debugging info:")
            print(f"  Current URL: {page.url}")
            print()
            
            # Take screenshot
            page.screenshot(path="login_error.png")
            print("Screenshot saved: login_error.png")
            
            # Print page content for debugging
            print("\nVisible text on page:")
            print(page.inner_text("body")[:500])
            
            exit(1)
        
        time.sleep(5)
        
    finally:
        browser.close()

print("\n" + "=" * 80)

