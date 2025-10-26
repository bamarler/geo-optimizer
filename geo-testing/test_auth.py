#!/usr/bin/env python3
"""
Quick test to verify authentication works for run_from_db.py
"""
import os
from playwright.sync_api import sync_playwright

print("=" * 80)
print("🧪 TESTING AUTHENTICATION SETUP")
print("=" * 80)

# Check if auth file exists
script_dir = os.path.dirname(os.path.abspath(__file__))
auth_state_path = os.path.join(script_dir, 'storage', 'auth_state.json')

print(f"\n📂 Auth file path: {auth_state_path}")

if not os.path.exists(auth_state_path):
    print("❌ Auth state file NOT found!")
    print()
    print("To fix, run ONE of these:")
    print("  1. python scripts/login.py --manual  (recommended)")
    print("  2. python scripts/login.py --auto    (requires .env credentials)")
    exit(1)

print("✅ Auth state file found!")

# Test loading the auth state
print("\n🚀 Testing auth state with ChatGPT...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    
    try:
        context = browser.new_context(
            storage_state=auth_state_path,
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        
        print("🌐 Opening ChatGPT...")
        page.goto("https://chatgpt.com/")
        
        print("⏳ Waiting for page to load...")
        page.wait_for_timeout(3000)
        
        # Check if logged in
        try:
            page.locator("#prompt-textarea").wait_for(timeout=5000)
            print("\n✅ SUCCESS! You're logged in to ChatGPT!")
            print("✅ Authentication works correctly!")
            print("\n🎉 You can now run: python run_from_db.py <persona_set_id> <prompts_id>")
        except:
            print("\n❌ FAILED! Not logged in.")
            print()
            print("Your session expired. Please re-authenticate:")
            print("  python scripts/login.py --manual")
        
        page.wait_for_timeout(2000)
        
    finally:
        browser.close()

print("\n" + "=" * 80)

