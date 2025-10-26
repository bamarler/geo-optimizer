"""
Run automated GEO testing with personas and prompts loaded from MongoDB.
"""
import json
import time
import re
from pathlib import Path
from playwright.sync_api import sync_playwright
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv
import sys
from datetime import datetime
from workflows.memory import clear_memory, set_persona
from workflows.chat import send_prompt, extract_response

load_dotenv()

def extract_brand_name(website_title: str, website_url: str) -> list:
    """
    Extract brand name from website title or URL for accurate brand detection.
    
    Examples:
        "MongoDB - Build Better", "mongodb.com" → ["mongodb", "mongodb.com", "mongodb - build better"]
        "GummySearch - Reddit", "gummysearch.com" → ["gummysearch", "gummysearch.com"]
    
    Returns a list of possible brand variations to check.
    """
    brand_keywords = []
    
    # 1. Extract from URL domain
    # Remove protocol and www
    domain = website_url.replace('https://', '').replace('http://', '').replace('www.', '')
    # Get the main domain name (before .com, .io, etc.)
    domain_name = domain.split('.')[0] if '.' in domain else domain
    if domain_name:
        brand_keywords.append(domain_name.lower())
    
    # 2. Extract from title (before any dash, pipe, or special separator)
    title_clean = website_title.split('-')[0].split('|')[0].split('—')[0].strip()
    if title_clean and len(title_clean) > 2:  # Avoid single letters
        brand_keywords.append(title_clean.lower())
    
    # 3. Add full domain for exact matches
    if domain:
        brand_keywords.append(domain.lower())
    
    # 4. Add full title for exact matches
    brand_keywords.append(website_title.lower())
    
    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for keyword in brand_keywords:
        if keyword not in seen and keyword:
            seen.add(keyword)
            unique_keywords.append(keyword)
    
    return unique_keywords

def run_geo_tests_from_db(persona_set_id: str, prompts_id: str):
    """Run GEO tests with personas and prompts from MongoDB"""

    print("=" * 80)
    print("🚀 RUNNING GEO TEST AUTOMATION FROM MONGODB")
    print("=" * 80)

    # Initialize database
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    db_name = os.getenv("MONGODB_DATABASE", "geo_sundai")
    
    mongo_client = MongoClient(mongo_uri)
    db = mongo_client[db_name]
    personas_collection = db['personas']
    prompts_collection = db['prompts']
    results_collection = db['test_results']

    # Load personas and prompts from MongoDB
    print("\n📂 Loading test data from MongoDB...")
    persona_set = personas_collection.find_one({'_id': ObjectId(persona_set_id)})
    prompts_doc = prompts_collection.find_one({'_id': ObjectId(prompts_id)})

    if not persona_set:
        print(f"❌ Persona set with ID {persona_set_id} not found.")
        return
    if not prompts_doc:
        print(f"❌ Prompts with ID {prompts_id} not found.")
        return

    personas = persona_set['personas']
    prompts = prompts_doc['prompts']
    website_title = persona_set['website_title']
    website_url = persona_set['website_url']

    print(f"   ✓ Loaded {len(personas)} personas for {website_title}")
    print(f"   ✓ Loaded {len(prompts)} prompts")

    print(f"\n📊 Test Plan:")
    print(f"   Website: {website_title} ({website_url})")
    print(f"   Personas: {len(personas)}")
    print(f"   Prompts: {len(prompts)}")
    print(f"   Total Tests: {len(personas) * len(prompts)}")
    print(f"\n🚀 Starting tests...")

    # Track results
    test_count = 0
    total_tests = len(personas) * len(prompts)
    test_run_id = f"run_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    # Track success/failure
    successful_tests = 0
    failed_tests = 0

    # Launch browser ONCE and reuse for all tests
    print(f"\n🚀 Launching browser...")
    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(
        headless=False,
        args=['--disable-blink-features=AutomationControlled']
    )

    # Create browser context (no saved session - we'll login fresh)
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        permissions=["geolocation"]
    )

    page = context.new_page()

    try:
        # LOGIN TO CHATGPT
        print(f"🔐 Logging into ChatGPT...")
        email = os.getenv("CHATGPT_EMAIL")
        password = os.getenv("CHATGPT_PASSWORD")
        
        if not email or not password:
            print(f"❌ Missing CHATGPT_EMAIL or CHATGPT_PASSWORD in .env")
            playwright.stop()
            mongo_client.close()
            return
        
        page.goto("https://chatgpt.com/")
        time.sleep(3)
        
        # Check if we need to login (look for "Log in" button)
        login_needed = False
        try:
            login_button = page.get_by_role("button", name="Log in")
            if login_button.is_visible(timeout=2000):
                login_needed = True
                print(f"🔑 Not logged in. Starting login process...")
        except:
            # No login button found, might be logged in
            pass
        
        if not login_needed:
            # Verify we're actually logged in by checking for textarea
            try:
                page.locator("#prompt-textarea").wait_for(timeout=3000)
                print(f"✅ Already logged in!")
            except:
                login_needed = True
                print(f"🔑 Session expired. Need to login...")
        
        if login_needed:
            # Perform login
            print(f"🔐 Logging in with credentials...")
            try:
                # Click login button
                page.get_by_role("button", name="Log in").click(timeout=5000)
                time.sleep(2)
                
                # Enter email
                page.get_by_role("textbox", name="Email address").fill(email)
                page.get_by_role("button", name="Continue", exact=True).click()
                time.sleep(2)
                
                # Enter password
                page.get_by_role("textbox", name="Password").fill(password)
                page.get_by_role("button", name="Continue", exact=True).click()
                time.sleep(5)
                
                # Wait for chat interface
                page.locator("#prompt-textarea").wait_for(timeout=15000)
                print(f"✅ Login successful!")
                
            except Exception as e:
                print(f"❌ Login failed: {e}")
                print(f"   Please check credentials in .env file")
                print(f"   Current URL: {page.url}")
                playwright.stop()
                mongo_client.close()
                return
        
        # FINAL VERIFICATION: Make sure we're logged in before starting tests
        print(f"\n🔍 Verifying login status before starting tests...")
        try:
            # Check that we can interact with the textarea
            textarea = page.locator("#prompt-textarea")
            textarea.wait_for(timeout=5000)
            if not textarea.is_visible():
                raise Exception("Textarea not visible")
            print(f"✅ Login verified! Ready to start tests.")
        except Exception as e:
            print(f"❌ Not properly logged in: {e}")
            print(f"   Current URL: {page.url}")
            print(f"   Taking screenshot for debugging...")
            page.screenshot(path="login_verification_failed.png")
            playwright.stop()
            mongo_client.close()
            return

        # Test each PROMPT with each PERSONA independently
        for prompt_idx, prompt in enumerate(prompts, 1):
            print(f"\n{'=' * 80}")
            print(f"📝 PROMPT {prompt_idx}/{len(prompts)}: {prompt['prompt']}")
            print(f"{'=' * 80}")
            print(f"Category: {prompt['category']}")
            print(f"Intent: {prompt['intent']}")

            for persona_idx, persona in enumerate(personas, 1):
                test_count += 1

                print(f"\n{'─' * 80}")
                print(f"👤 TEST {test_count}/{total_tests}: {persona['name']} ({persona['location']})")
                print(f"{'─' * 80}")

                # 1. CLEAR MEMORY (start fresh for each test)
                print(f"🧹 Clearing ChatGPT memory...")
                try:
                    clear_memory(page)
                    time.sleep(2)
                    print(f"   ✅ Memory cleared successfully!")
                except Exception as e:
                    print(f"   ❌ FAILED to clear memory: {e}")
                    print(f"   ⚠️ WARNING: Previous persona may leak into this test!")
                    import traceback
                    traceback.print_exc()

                # 2. SET PERSONA (using workflow function)
                persona_memory_text = (
                    f"My name is {persona['name']}. I am {persona['age']} and work as a {persona['occupation']} "
                    f"in {persona['location']}. My main goals are: {', '.join(persona['goals'])}. "
                    f"My pain points include: {', '.join(persona['painPoints'])}. "
                    f"I typically {persona['behavior'].lower()}."
                )
                print(f"👤 Setting persona: {persona['name']}...")
                try:
                    set_persona(page, persona_memory_text)
                    time.sleep(3)
                    print(f"   ✅ Persona set!")
                except Exception as e:
                    print(f"   ⚠️ Could not set persona: {e}")

                # 3. SEND PROMPT (using workflow function)
                print(f"📤 Sending prompt: {prompt['prompt']}")
                try:
                    send_prompt(page, prompt["prompt"])
                except Exception as e:
                    print(f"   ❌ Could not send prompt: {e}")
                    failed_tests += 1
                    continue

                # 4. WAIT FOR RESPONSE (using workflow function)
                print(f"⏳ Waiting for ChatGPT response...")
                time.sleep(5)  # Give it time to think

                # 5. EXTRACT RESPONSE (using workflow function)
                try:
                    # extract_response waits for conversation-turn-2 (first actual response after persona)
                    response = extract_response(page, turn_number=2)
                    
                    print(f"✅ Response received!")
                    print(f"   Length: {len(response['text'])} characters")
                    print(f"   Citations: {len(response['citations'])}")
                    
                    # FIXED: Check if brand mentioned using smart brand extraction
                    brand_keywords = extract_brand_name(website_title, website_url)
                    response_text_lower = response['text'].lower()
                    brand_mentioned = any(keyword in response_text_lower for keyword in brand_keywords)
                    
                    # Debug: Show what we're checking for
                    print(f"   🔍 Checking for brand keywords: {brand_keywords[:2]}...")  # Show first 2
                    if brand_mentioned:
                        print(f"   ✅ BRAND MENTIONED in response!")
                    else:
                        print(f"   ⚠️ Brand NOT mentioned in response")
                    
                    # 6. SAVE TO MONGODB
                    test_result_doc = {
                        "persona_set_id": persona_set_id,
                        "persona_id": persona_idx,
                        "persona_details": persona,
                        "prompts_id": prompts_id,
                        "prompt_id": prompt_idx,
                        "prompt_details": prompt,
                        "website_url": website_url,
                        "website_title": website_title,
                        "response_text": response['text'],
                        "citations": response['citations'],
                        "has_citations": response['has_citations'],
                        "brand_mentioned": brand_mentioned,
                        "test_run_id": test_run_id,
                        "test_number": test_count,
                        "total_tests_in_run": total_tests,
                        "timestamp": datetime.utcnow()
                    }
                    
                    result = results_collection.insert_one(test_result_doc)
                    print(f"   💾 Saved to MongoDB: {result.inserted_id}")
                    successful_tests += 1
                        
                except Exception as e:
                    print(f"   ❌ Error extracting response: {e}")
                    failed_tests += 1
                    import traceback
                    traceback.print_exc()
    
    finally:
        # Clean up browser
        print(f"\n🔒 Closing browser...")
        context.close()
        browser.close()
        playwright.stop()
        mongo_client.close()
    
    # Final summary
    print(f"\n{'=' * 80}")
    print(f"✅ TESTING COMPLETE!")
    print(f"{'=' * 80}")
    print(f"\n📊 RESULTS SUMMARY:")
    print(f"   Total Tests:      {total_tests}")
    print(f"   ✅ Successful:    {successful_tests}")
    print(f"   ❌ Failed:        {failed_tests}")
    print(f"   📈 Success Rate:  {(successful_tests/total_tests*100):.1f}%")
    print(f"\n💾 All results saved to MongoDB:")
    print(f"   Collection: test_results")
    print(f"   Test Run ID: {test_run_id}")
    print(f"\n🎉 GEO testing complete!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python run_from_db.py <persona_set_id> <prompts_id>")
        sys.exit(1)
    
    persona_set_id = sys.argv[1]
    prompts_id = sys.argv[2]
    run_geo_tests_from_db(persona_set_id, prompts_id)
