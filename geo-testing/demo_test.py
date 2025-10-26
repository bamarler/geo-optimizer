"""
Demo script to test GEO Testing framework setup
This script demonstrates the workflow without requiring authentication
"""
from playwright.sync_api import sync_playwright
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_browser_launch():
    """Test that Playwright and browser are working"""
    print("🚀 Testing Playwright browser launch...")
    
    with sync_playwright() as playwright:
        # Launch browser
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        
        # Navigate to a test page
        print("📍 Navigating to example.com...")
        page.goto("https://example.com")
        
        # Get page title
        title = page.title()
        print(f"✅ Page title: {title}")
        
        # Wait a moment so you can see the browser
        page.wait_for_timeout(2000)
        
        # Close browser
        print("🔒 Closing browser...")
        context.close()
        browser.close()
        
    print("✅ Browser test successful!")

def test_workflows_import():
    """Test that workflow modules can be imported"""
    print("\n📦 Testing workflow imports...")
    
    try:
        from workflows import login, chat, memory
        print("✅ login module imported")
        print("✅ chat module imported")
        print("✅ memory module imported")
        
        # Check functions exist
        assert hasattr(login, 'load_auth_session')
        assert hasattr(chat, 'send_prompt')
        assert hasattr(chat, 'extract_response')
        assert hasattr(memory, 'clear_memory')
        assert hasattr(memory, 'set_persona')
        
        print("✅ All workflow functions found")
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False
    
    return True

def check_auth_state():
    """Check if authentication state exists"""
    print("\n🔐 Checking authentication state...")
    
    auth_path = "storage/auth_state.json"
    if os.path.exists(auth_path):
        size = os.path.getsize(auth_path)
        print(f"✅ Auth state found ({size:,} bytes)")
        print("   You can use authenticated scripts!")
        return True
    else:
        print("⚠️  No auth state found")
        print("   Run scripts/record_login.py first with your credentials")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("GEO Testing Framework - Setup Verification")
    print("=" * 60)
    
    # Test 1: Browser launch
    try:
        test_browser_launch()
    except Exception as e:
        print(f"❌ Browser test failed: {e}")
        sys.exit(1)
    
    # Test 2: Workflow imports
    if not test_workflows_import():
        sys.exit(1)
    
    # Test 3: Auth state check
    has_auth = check_auth_state()
    
    print("\n" + "=" * 60)
    print("✅ Setup verification complete!")
    print("=" * 60)
    
    if has_auth:
        print("\n📌 Next steps:")
        print("   1. Run: python scripts/record_chat.py")
        print("   2. Or create your own test scripts using the workflows")
    else:
        print("\n📌 Next steps:")
        print("   1. Update scripts/record_login.py with YOUR credentials")
        print("   2. Run: python scripts/record_login.py")
        print("   3. Then run: python scripts/record_chat.py")
    
    print("\n💡 Tip: All scripts work with the virtual environment active")
    print("   Activate with: source venv/bin/activate")

