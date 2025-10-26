"""
Check what's actually saved in MongoDB
"""
from utils.database import Database
import json

db = Database()

print("\n" + "=" * 80)
print("📊 MONGODB DATA CHECK")
print("=" * 80)

# Get total count
total = db.results.count_documents({})
print(f"\n✅ Total records in database: {total}")

if total > 0:
    # Get all records
    records = list(db.results.find())
    
    # Group by persona
    print("\n" + "─" * 80)
    print("BY PERSONA:")
    print("─" * 80)
    
    personas = {}
    for r in records:
        p = r.get('persona_name', 'Unknown')
        if p not in personas:
            personas[p] = []
        personas[p].append(r)
    
    for persona, tests in personas.items():
        print(f"\n{persona}: {len(tests)} tests")
        for t in tests:
            prompt = t.get('prompt_text', '')[:40]
            print(f"  • {prompt}...")
    
    # Show sample record
    print("\n" + "─" * 80)
    print("SAMPLE RECORD (first test):")
    print("─" * 80)
    
    sample = records[0]
    print(f"\nPersona: {sample.get('persona_name')}")
    print(f"Location: {sample.get('location', {}).get('city')}")
    print(f"Prompt: {sample.get('prompt_text')}")
    print(f"Response (first 200 chars): {sample.get('response_text', '')[:200]}...")
    print(f"Citations: {len(sample.get('citations', []))}")
    print(f"Analysis Flags:")
    analysis = sample.get('analysis_flags', {})
    for key, value in analysis.items():
        print(f"  • {key}: {value}")
    
    # Stats
    print("\n" + "─" * 80)
    print("STATISTICS:")
    print("─" * 80)
    
    stats = db.get_test_run_stats()
    print(f"Total Tests: {stats['total_tests']}")
    print(f"Tests with Citations: {stats['tests_with_citations']} ({stats['citation_rate']:.1%})")
    print(f"Tests with Geographic Content: {stats['tests_with_geographic_content']} ({stats['geo_content_rate']:.1%})")
    
    print("\n✅ ALL DATA SUCCESSFULLY SAVED TO MONGODB!")
    print("=" * 80)

else:
    print("\n⚠️  No records found")

db.close()

