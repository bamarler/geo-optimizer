"""
Analyze GEO Test Results from MongoDB
View and analyze geographic bias in ChatGPT responses
"""
from utils.database import Database
import json
from collections import defaultdict

def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def analyze_all_results():
    """Comprehensive analysis of all test results"""
    
    db = Database()
    
    # Overall Statistics
    print_header("📊 OVERALL STATISTICS")
    stats = db.get_test_run_stats()
    print(f"\nTotal Tests Run: {stats['total_tests']}")
    print(f"Tests with Citations: {stats['tests_with_citations']} ({stats['citation_rate']:.1%})")
    print(f"Tests with Geographic Content: {stats['tests_with_geographic_content']} ({stats['geo_content_rate']:.1%})")
    
    # Get all results
    all_results = list(db.results.find())
    
    if not all_results:
        print("\n⚠️  No test results found in database yet.")
        print("💡 Run: python scripts/run_tests.py to generate test data")
        db.close()
        return
    
    # Group by persona
    print_header("👤 RESULTS BY PERSONA")
    persona_groups = defaultdict(list)
    for result in all_results:
        persona_groups[result.get('persona_id', 'unknown')].append(result)
    
    for persona_id, results in persona_groups.items():
        persona_name = results[0].get('persona_name', 'Unknown')
        location = results[0].get('location', {})
        city = location.get('city', 'Unknown')
        
        print(f"\n{persona_name} ({city})")
        print(f"  Tests: {len(results)}")
        
        # Analyze detected locations
        all_detected = []
        for r in results:
            detected = r.get('analysis_flags', {}).get('detected_locations', [])
            all_detected.extend(detected)
        
        if all_detected:
            location_counts = defaultdict(int)
            for loc in all_detected:
                location_counts[loc] += 1
            print(f"  Locations mentioned: {dict(location_counts)}")
        
        # Citation stats
        with_citations = sum(1 for r in results if r.get('has_citations'))
        print(f"  Citation rate: {with_citations}/{len(results)} ({with_citations/len(results):.1%})")
    
    # Group by prompt
    print_header("💬 RESULTS BY PROMPT")
    prompt_groups = defaultdict(list)
    for result in all_results:
        prompt_groups[result.get('prompt_id', 'unknown')].append(result)
    
    for prompt_id, results in prompt_groups.items():
        prompt_text = results[0].get('prompt_text', 'Unknown')
        expected_geo = results[0].get('expected_geo', False)
        
        print(f"\n\"{prompt_text}\"")
        print(f"  Expected GEO bias: {expected_geo}")
        print(f"  Responses: {len(results)}")
        
        # Show how each persona responded
        for r in results:
            persona_name = r.get('persona_name', 'Unknown')
            detected_locs = r.get('analysis_flags', {}).get('detected_locations', [])
            citation_count = r.get('analysis_flags', {}).get('citation_count', 0)
            
            print(f"    • {persona_name}: {len(detected_locs)} locations, {citation_count} citations")
            if detected_locs:
                print(f"      → {', '.join(detected_locs)}")
    
    # Geographic Bias Analysis
    print_header("🌍 GEOGRAPHIC BIAS ANALYSIS")
    
    for prompt_id, results in prompt_groups.items():
        if len(results) < 2:
            continue
        
        prompt_text = results[0].get('prompt_text', 'Unknown')
        print(f"\n\"{prompt_text[:60]}...\"")
        
        # Compare persona location vs mentioned locations
        bias_detected = False
        for r in results:
            persona_city = r.get('location', {}).get('city', '').lower()
            detected_locs = [loc.lower() for loc in r.get('analysis_flags', {}).get('detected_locations', [])]
            
            # Check if persona's city matches detected locations
            if persona_city and persona_city in detected_locs:
                print(f"  ✓ {r.get('persona_name')}: Home city ({persona_city}) mentioned in response")
                bias_detected = True
            elif detected_locs:
                print(f"  • {r.get('persona_name')}: Other locations mentioned: {', '.join(detected_locs)}")
        
        if not bias_detected:
            print(f"  ℹ️  No clear geographic bias detected")
    
    # Citation Domain Analysis
    print_header("🔗 CITATION SOURCES")
    
    all_domains = []
    for result in all_results:
        domains = result.get('analysis_flags', {}).get('citation_domains', [])
        all_domains.extend(domains)
    
    if all_domains:
        domain_counts = defaultdict(int)
        for domain in all_domains:
            domain_counts[domain] += 1
        
        print("\nTop Citation Sources:")
        sorted_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)
        for domain, count in sorted_domains[:10]:
            print(f"  {count:2d}× {domain}")
    else:
        print("\nNo citation sources found")
    
    # Recent Tests
    print_header("🕐 RECENT TESTS")
    
    recent = sorted(all_results, key=lambda x: x.get('timestamp', ''), reverse=True)[:5]
    for r in recent:
        timestamp = r.get('timestamp', 'Unknown')
        persona = r.get('persona_name', 'Unknown')
        prompt = r.get('prompt_text', 'Unknown')[:40]
        
        print(f"\n{timestamp}")
        print(f"  {persona}: \"{prompt}...\"")
        print(f"  Response: {len(r.get('response_text', ''))} chars, {r.get('analysis_flags', {}).get('citation_count', 0)} citations")
    
    # Export option
    print_header("💾 DATA EXPORT")
    print("\nExport options:")
    print("  1. View raw data: db.results.find() in MongoDB")
    print("  2. Export to JSON: python export_results.py")
    print(f"  3. Total records: {len(all_results)}")
    
    db.close()

def compare_prompt_responses(prompt_id: str):
    """Compare how different personas responded to the same prompt"""
    
    db = Database()
    
    print_header(f"🔍 COMPARING RESPONSES FOR: {prompt_id}")
    
    results = db.compare_personas_for_prompt(prompt_id)
    
    if not results:
        print(f"\n⚠️  No results found for prompt: {prompt_id}")
        db.close()
        return
    
    prompt_text = results[0].get('prompt_text', 'Unknown')
    print(f"\nPrompt: \"{prompt_text}\"")
    print(f"Responses: {len(results)}")
    
    for r in results:
        persona_name = r.get('persona_name', 'Unknown')
        location = r.get('location', {}).get('city', 'Unknown')
        response = r.get('response_text', '')
        citations = r.get('citations', [])
        detected_locs = r.get('analysis_flags', {}).get('detected_locations', [])
        
        print(f"\n{'─' * 80}")
        print(f"👤 {persona_name} ({location})")
        print(f"{'─' * 80}")
        print(f"\n{response[:300]}...")
        print(f"\n🔗 Citations: {len(citations)}")
        for citation in citations[:3]:
            print(f"   • {citation.get('title', 'Unknown')}")
            print(f"     {citation.get('url', 'Unknown')}")
        
        print(f"\n📍 Detected Locations: {', '.join(detected_locs) if detected_locs else 'None'}")
    
    db.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Compare specific prompt
        prompt_id = sys.argv[1]
        compare_prompt_responses(prompt_id)
    else:
        # Full analysis
        analyze_all_results()

