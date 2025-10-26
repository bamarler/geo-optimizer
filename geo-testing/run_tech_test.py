"""
Run automated GEO testing with tech-focused prompts
Tests 3 personas (student, developer, freelancer) x 5 tech prompts
"""
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from utils.database import Database
from workflows.login import load_auth_session
from workflows.memory import clear_memory, set_persona
from workflows.chat import send_prompt, extract_response

def run_tech_geo_tests():
    """Run GEO tests with tech prompts across different developer personas"""
    
    print("=" * 80)
    print("🚀 RUNNING TECH GEO TEST AUTOMATION")
    print("=" * 80)
    
    # Initialize database
    db = Database()
    
    # Load test data
    print("\n📂 Loading test data...")
    
    # Load specific personas
    persona_files = [
        "data/personas/boston_student.json",
        "data/personas/sf_developer.json", 
        "data/personas/nyc_freelancer.json"
    ]
    
    personas = []
    for persona_file in persona_files:
        if Path(persona_file).exists():
            with open(persona_file) as f:
                personas.append(json.load(f))
                print(f"   ✓ Loaded: {persona_file}")
    
    # Load tech prompts
    with open("data/prompts/tech_prompts.json") as f:
        prompts_data = json.load(f)
        prompts = prompts_data["prompts"]
        print(f"   ✓ Loaded {len(prompts)} tech prompts")
    
    print(f"\n📊 Test Plan:")
    print(f"   Personas: {len(personas)}")
    print(f"   Prompts: {len(prompts)}")
    print(f"   Total Tests: {len(personas) * len(prompts)}")
    print(f"\n🚀 Starting tests...")
    
    # Track results
    test_count = 0
    total_tests = len(personas) * len(prompts)
    
    # Launch browser ONCE and reuse for all tests
    print(f"\n🚀 Launching browser...")
    playwright = sync_playwright().start()
    
    browser = playwright.chromium.launch(
        headless=False,
        args=['--disable-blink-features=AutomationControlled']
    )
    
    context = browser.new_context(
        storage_state="storage/auth_state.json",
        viewport={"width": 1280, "height": 720},
        permissions=["geolocation"]
    )
    
    page = context.new_page()
    
    try:
        # Load authenticated session once
        print(f"🔐 Loading authenticated session...")
        load_auth_session(context, page)
        time.sleep(2)
        
        # Test each PROMPT with each PERSONA independently
        for prompt_idx, prompt in enumerate(prompts, 1):
            print(f"\n{'=' * 80}")
            print(f"📝 PROMPT {prompt_idx}/{len(prompts)}: {prompt['text']}")
            print(f"{'=' * 80}")
            print(f"Category: {prompt['category']}")
            print(f"Expected GEO bias: {prompt['expected_geo']}")
            
            for persona_idx, persona in enumerate(personas, 1):
                test_count += 1
                
                print(f"\n{'─' * 80}")
                print(f"👤 TEST {test_count}/{total_tests}: {persona['name']} ({persona['location']['city']})")
                print(f"{'─' * 80}")
                
                # 1. CLEAR MEMORY (start fresh for each test)
                print(f"🧹 Clearing ChatGPT memory...")
                clear_memory(page)
                time.sleep(2)
                
                # 2. SET PERSONA (fresh persona for this test)
                print(f"👤 Setting persona: {persona['memory_text'][:60]}...")
                set_persona(page, persona["memory_text"])
                time.sleep(3)
                
                # 3. SEND PROMPT
                print(f"📤 Sending prompt...")
                send_prompt(page, prompt["text"])
                
                # 4. WAIT FOR RESPONSE
                print(f"⏳ Waiting for ChatGPT response...")
                time.sleep(5)  # Give it time to think
                
                # 5. EXTRACT RESPONSE
                try:
                    response = extract_response(page, turn_number=2)
                    
                    print(f"✅ Response received!")
                    print(f"   Length: {len(response['text'])} characters")
                    print(f"   Citations: {len(response['citations'])}")
                    
                    # Show preview
                    preview = response['text'][:150].replace('\n', ' ')
                    print(f"   Preview: {preview}...")
                    
                    # 6. SAVE TO MONGODB
                    test_data = {
                        "persona_id": persona["id"],
                        "persona_name": persona["name"],
                        "location": persona["location"],
                        "persona_memory": persona["memory_text"],
                        "prompt_id": prompt["id"],
                        "prompt_text": prompt["text"],
                        "prompt_category": prompt["category"],
                        "response_text": response["text"],
                        "citations": response["citations"],
                        "expected_geo": prompt["expected_geo"],
                        "has_citations": response["has_citations"],
                        "test_run": "tech_geo_test",
                        "test_number": test_count,
                        "total_tests": total_tests
                    }
                    
                    inserted_id = db.insert_test_result(test_data)
                    print(f"   💾 Saved to MongoDB: {inserted_id[:12]}...")
                    
                except Exception as e:
                    print(f"   ❌ Error extracting response: {e}")
                    import traceback
                    traceback.print_exc()
                
                # 7. Start new chat for next test (clean slate)
                print(f"   🔄 Starting new chat for next test...")
                page.goto("https://chatgpt.com/")
                time.sleep(3)
    
    finally:
        # Clean up browser
        print(f"\n🔒 Closing browser...")
        context.close()
        browser.close()
        playwright.stop()
    
    # Final summary
    print(f"\n{'=' * 80}")
    print(f"✅ TESTING COMPLETE!")
    print(f"{'=' * 80}")
    
    # Get final stats from database
    stats = db.get_test_run_stats()
    print(f"\n📊 Final Statistics:")
    print(f"   Total Tests: {stats['total_tests']}")
    print(f"   Tests with Citations: {stats['tests_with_citations']}")
    print(f"   Citation Rate: {stats['citation_rate']:.1%}")
    print(f"   Tests with Geographic Content: {stats['tests_with_geographic_content']}")
    print(f"   Geographic Content Rate: {stats['geo_content_rate']:.1%}")
    
    db.close()
    
    print(f"\n🎉 All data saved to MongoDB!")
    print(f"\n📌 Next steps:")
    print(f"   • Run: python analyze_results.py")
    print(f"   • Run: python export_results.py")
    print(f"   • Check MongoDB Atlas dashboard")

if __name__ == "__main__":
    try:
        run_tech_geo_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Testing interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()

