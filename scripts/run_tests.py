import json
import time
from pathlib import Path
from utils.browser import launch_browser_with_auth
from utils.database import Database
from workflows.login import load_auth_session
from workflows.memory import clear_memory, set_persona
from workflows.chat import send_prompt, extract_response

def run_geo_tests():
    db = Database()
    
    # Load test data
    personas = list(Path("data/personas").glob("*.json"))
    with open("data/prompts/test_prompts.json") as f:
        prompts = json.load(f)["prompts"]
    
    for persona_file in personas:
        with open(persona_file) as f:
            persona = json.load(f)
        
        print(f"\n{'='*60}")
        print(f"Testing Persona: {persona['name']}")
        print(f"{'='*60}")
        
        # Launch browser with location override
        playwright, browser, context, page = launch_browser_with_auth(
            location=persona.get("location")
        )
        
        try:
            # Setup
            load_auth_session(context, page)
            clear_memory(page)
            set_persona(page, persona["memory_text"])
            
            # Test each prompt
            for prompt in prompts:
                print(f"\nPrompt: {prompt['text']}")
                
                send_prompt(page, prompt["text"])
                time.sleep(3)  # Wait for response
                
                response = extract_response(page, turn_number=2)
                
                # Save to database
                db.insert_test_result({
                    "persona_id": persona["id"],
                    "persona_name": persona["name"],
                    "location": persona.get("location", {}),
                    "prompt_id": prompt["id"],
                    "prompt_text": prompt["text"],
                    "response_text": response["text"],
                    "citations": response["citations"],
                    "expected_geo": prompt["expected_geo"],
                    "has_citations": response["has_citations"]
                })
                
                print(f"✓ Response saved ({len(response['citations'])} citations)")
                
                # Start new chat for next prompt
                page.goto("https://chatgpt.com/")
                time.sleep(2)
        
        finally:
            context.close()
            browser.close()
            playwright.stop()
    
    db.close()
    print("\n✓ All tests complete!")

if __name__ == "__main__":
    run_geo_tests()