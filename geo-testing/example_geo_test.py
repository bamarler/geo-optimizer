"""
Example GEO Testing Script
Demonstrates how to test geographic biases in ChatGPT responses
"""
from playwright.sync_api import sync_playwright
from workflows.login import load_auth_session
from workflows.chat import send_prompt, extract_response
from workflows.memory import clear_memory, set_persona
import json
import time

def run_geo_test():
    """Run a geographic bias test comparing different locations"""
    
    print("=" * 70)
    print("GEO Testing: Coffee Shop Recommendations by Location")
    print("=" * 70)
    
    # Test configurations
    test_scenarios = [
        {
            "name": "Boston User",
            "persona": "I live in Boston, Massachusetts and I'm a college student.",
            "prompt": "Recommend a good coffee shop near me"
        },
        {
            "name": "Seattle User", 
            "persona": "I live in Seattle, Washington and work in tech.",
            "prompt": "Recommend a good coffee shop near me"
        },
        {
            "name": "No Location",
            "persona": None,  # Clear memory, no persona
            "prompt": "Recommend a good coffee shop"
        }
    ]
    
    results = []
    
    with sync_playwright() as playwright:
        # Launch browser
        print("\n🚀 Launching browser...")
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(
            storage_state="storage/auth_state.json",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        
        # Load authenticated session
        print("🔐 Loading authenticated session...")
        load_auth_session(context, page)
        print("✅ Logged in successfully!")
        
        # Run each test scenario
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n{'=' * 70}")
            print(f"Test {i}/{len(test_scenarios)}: {scenario['name']}")
            print(f"{'=' * 70}")
            
            # Clear memory before each test
            print("🧹 Clearing ChatGPT memory...")
            clear_memory(page)
            time.sleep(2)
            
            # Set persona if specified
            if scenario['persona']:
                print(f"👤 Setting persona: {scenario['persona']}")
                set_persona(page, scenario['persona'])
                time.sleep(2)
            else:
                print("👤 No persona set (testing without location)")
            
            # Send prompt
            print(f"💬 Sending prompt: '{scenario['prompt']}'")
            send_prompt(page, scenario['prompt'])
            
            # Extract response
            print("⏳ Waiting for response...")
            response_data = extract_response(page, turn_number=2)
            
            # Store results
            result = {
                "scenario": scenario['name'],
                "persona": scenario['persona'],
                "prompt": scenario['prompt'],
                "response_text": response_data['text'][:500] + "...",  # First 500 chars
                "full_response": response_data['text'],
                "citations": response_data['citations'],
                "has_citations": response_data['has_citations'],
                "citation_count": len(response_data['citations'])
            }
            results.append(result)
            
            # Display results
            print(f"\n✅ Response received ({len(response_data['text'])} characters)")
            print(f"📊 Citations found: {len(response_data['citations'])}")
            
            if response_data['citations']:
                print("\n🔗 Citations:")
                for citation in response_data['citations']:
                    print(f"   {citation['position']}. {citation['title']}")
                    print(f"      {citation['url']}")
            
            # Show preview of response
            print(f"\n📝 Response preview:")
            print("-" * 70)
            print(response_data['text'][:400] + "...")
            print("-" * 70)
            
            # Wait between tests
            if i < len(test_scenarios):
                print("\n⏸️  Waiting 5 seconds before next test...")
                time.sleep(5)
        
        # Close browser
        print("\n\n🔒 Closing browser...")
        context.close()
        browser.close()
    
    # Save results to JSON
    print("\n💾 Saving results to geo_test_results.json...")
    with open("geo_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    for result in results:
        print(f"\n{result['scenario']}:")
        print(f"  Citations: {result['citation_count']}")
        print(f"  Response length: {len(result['full_response'])} characters")
        
        # Try to detect location mentions
        locations = []
        location_keywords = ['Boston', 'Seattle', 'Massachusetts', 'Washington', 
                            'Cambridge', 'Somerville', 'Capitol Hill', 'Fremont']
        for keyword in location_keywords:
            if keyword in result['full_response']:
                locations.append(keyword)
        
        if locations:
            print(f"  Location mentions: {', '.join(set(locations))}")
        else:
            print(f"  Location mentions: None detected")
    
    print("\n✅ Testing complete! Results saved to geo_test_results.json")
    print("\n💡 Next steps:")
    print("   - Review geo_test_results.json for detailed analysis")
    print("   - Compare citation URLs across different personas")
    print("   - Analyze location-specific business recommendations")

if __name__ == "__main__":
    try:
        run_geo_test()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()

