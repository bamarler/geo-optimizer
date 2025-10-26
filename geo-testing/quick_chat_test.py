"""
Quick Chat Test - Simple demo of chat workflow
Sends a single prompt and extracts the response
"""
from playwright.sync_api import sync_playwright
from workflows.login import load_auth_session
from workflows.chat import send_prompt, extract_response

def quick_test():
    """Run a quick single-prompt test"""
    
    print("=" * 70)
    print("Quick Chat Test - ChatGPT Interaction Demo")
    print("=" * 70)
    
    # You can customize this prompt
    test_prompt = "Tell me a fun fact about Boston in one sentence."
    
    print(f"\n💬 Test Prompt: '{test_prompt}'")
    print("\n🚀 Starting browser...")
    
    with sync_playwright() as playwright:
        # Launch browser
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(
            storage_state="storage/auth_state.json",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        
        # Load authenticated session
        print("🔐 Loading authenticated session...")
        load_auth_session(context, page)
        print("✅ Logged in!")
        
        # Send prompt
        print(f"\n📤 Sending prompt...")
        send_prompt(page, test_prompt)
        
        # Extract response
        print("⏳ Waiting for response...")
        response_data = extract_response(page, turn_number=2)
        
        # Display results
        print("\n" + "=" * 70)
        print("✅ RESPONSE RECEIVED")
        print("=" * 70)
        
        print(f"\n📝 Response Text:")
        print("-" * 70)
        print(response_data['text'])
        print("-" * 70)
        
        print(f"\n📊 Response Stats:")
        print(f"   Length: {len(response_data['text'])} characters")
        print(f"   Citations: {len(response_data['citations'])}")
        print(f"   Has Citations: {response_data['has_citations']}")
        
        if response_data['citations']:
            print(f"\n🔗 Citations Found:")
            for citation in response_data['citations']:
                print(f"   {citation['position']}. {citation['title']}")
                print(f"      URL: {citation['url']}")
        
        # Wait a moment so you can see the result
        print("\n⏸️  Browser will close in 3 seconds...")
        page.wait_for_timeout(3000)
        
        # Close browser
        context.close()
        browser.close()
    
    print("\n✅ Test complete!")
    print("\n💡 Try modifying the 'test_prompt' variable to test different prompts")

if __name__ == "__main__":
    try:
        quick_test()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Activated the virtual environment: source venv/bin/activate")
        print("   2. Valid auth state in storage/auth_state.json")
        print("   3. Internet connection")

