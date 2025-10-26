"""
Monitor MongoDB in real-time to see test results being saved
"""
from utils.database import Database
import time

def monitor_tests():
    """Watch MongoDB for new test results"""
    
    print("=" * 80)
    print("📊 MONITORING MONGODB - Test Results")
    print("=" * 80)
    
    db = Database()
    
    last_count = 0
    
    try:
        while True:
            # Get current count
            current_count = db.results.count_documents({})
            
            if current_count > last_count:
                # New records added!
                print(f"\n🔔 NEW RECORDS! Total: {current_count}")
                
                # Get the latest records
                latest = list(db.results.find().sort("_id", -1).limit(current_count - last_count))
                
                for record in reversed(latest):
                    persona = record.get('persona_name', 'Unknown')
                    prompt = record.get('prompt_text', 'Unknown')[:50]
                    response_len = len(record.get('response_text', ''))
                    citations = len(record.get('citations', []))
                    
                    print(f"\n   ✅ Test #{record.get('test_number', '?')}/{record.get('total_tests', '?')}")
                    print(f"      Persona: {persona}")
                    print(f"      Prompt: {prompt}...")
                    print(f"      Response: {response_len} chars, {citations} citations")
                    
                    # Show detected locations
                    locations = record.get('analysis_flags', {}).get('detected_locations', [])
                    if locations:
                        print(f"      📍 Locations detected: {', '.join(locations)}")
                
                last_count = current_count
            elif current_count == last_count and current_count > 0:
                print(".", end="", flush=True)
            
            time.sleep(3)  # Check every 3 seconds
    
    except KeyboardInterrupt:
        print("\n\n⏸️  Monitoring stopped")
        
        # Final summary
        print("\n" + "=" * 80)
        print("📊 FINAL SUMMARY")
        print("=" * 80)
        
        stats = db.get_test_run_stats()
        print(f"\nTotal Tests: {stats['total_tests']}")
        print(f"Tests with Citations: {stats['tests_with_citations']}")
        print(f"Tests with Geographic Content: {stats['tests_with_geographic_content']}")
        
        db.close()

if __name__ == "__main__":
    monitor_tests()

