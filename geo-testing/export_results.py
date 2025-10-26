"""
Export test results from MongoDB to JSON files
"""
from utils.database import Database
import json
from datetime import datetime
from pathlib import Path

def export_all_results():
    """Export all test results to JSON file"""
    
    print("=" * 70)
    print("Exporting Test Results from MongoDB")
    print("=" * 70)
    
    db = Database()
    
    # Get all results
    all_results = list(db.results.find())
    
    if not all_results:
        print("\n⚠️  No results to export")
        db.close()
        return
    
    # Create exports directory
    exports_dir = Path("exports")
    exports_dir.mkdir(exist_ok=True)
    
    # Convert ObjectId to string for JSON serialization
    for result in all_results:
        if '_id' in result:
            result['_id'] = str(result['_id'])
        if 'timestamp' in result:
            result['timestamp'] = result['timestamp'].isoformat()
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = exports_dir / f"geo_test_results_{timestamp}.json"
    
    # Export to JSON
    print(f"\n📝 Exporting {len(all_results)} records...")
    with open(filename, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"✅ Results exported to: {filename}")
    print(f"   File size: {filename.stat().st_size:,} bytes")
    
    # Create summary
    summary_filename = exports_dir / f"summary_{timestamp}.json"
    
    summary = {
        "export_date": timestamp,
        "total_records": len(all_results),
        "statistics": db.get_test_run_stats(),
        "personas": list(set(r.get('persona_id') for r in all_results)),
        "prompts": list(set(r.get('prompt_id') for r in all_results))
    }
    
    with open(summary_filename, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Summary exported to: {summary_filename}")
    
    # Export by persona
    print(f"\n📊 Creating per-persona exports...")
    personas = {}
    for result in all_results:
        persona_id = result.get('persona_id', 'unknown')
        if persona_id not in personas:
            personas[persona_id] = []
        personas[persona_id].append(result)
    
    personas_dir = exports_dir / "by_persona"
    personas_dir.mkdir(exist_ok=True)
    
    for persona_id, results in personas.items():
        persona_file = personas_dir / f"{persona_id}_{timestamp}.json"
        with open(persona_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"   ✓ {persona_id}: {len(results)} records")
    
    # Export by prompt
    print(f"\n📊 Creating per-prompt exports...")
    prompts = {}
    for result in all_results:
        prompt_id = result.get('prompt_id', 'unknown')
        if prompt_id not in prompts:
            prompts[prompt_id] = []
        prompts[prompt_id].append(result)
    
    prompts_dir = exports_dir / "by_prompt"
    prompts_dir.mkdir(exist_ok=True)
    
    for prompt_id, results in prompts.items():
        prompt_file = prompts_dir / f"{prompt_id}_{timestamp}.json"
        with open(prompt_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"   ✓ {prompt_id}: {len(results)} records")
    
    db.close()
    
    print("\n" + "=" * 70)
    print("✅ Export Complete!")
    print("=" * 70)
    print(f"\nExported files:")
    print(f"  • All results: {filename}")
    print(f"  • Summary: {summary_filename}")
    print(f"  • By persona: {personas_dir}/ ({len(personas)} files)")
    print(f"  • By prompt: {prompts_dir}/ ({len(prompts)} files)")

if __name__ == "__main__":
    export_all_results()

