from pymongo import MongoClient
from datetime import datetime
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        db_name = os.getenv("MONGODB_DATABASE", "geo_sundai")
        collection_name = os.getenv("MONGODB_COLLECTION", "test_results")
        
        print(f"🔌 Connecting to MongoDB...")
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.results = self.db[collection_name]
        
        # Test connection
        try:
            self.client.admin.command('ping')
            print(f"✅ Connected to MongoDB Atlas")
            print(f"   Database: {db_name}")
            print(f"   Collection: {collection_name}")
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            raise
    
    def insert_test_result(self, data: Dict) -> str:
        """
        Insert comprehensive test result with all data needed for analysis.
        
        Data structure:
        - persona_info: Full persona details (id, name, location)
        - prompt_info: Full prompt details (id, text, category, expected_geo)
        - response_data: ChatGPT's response text
        - citations: All extracted citations with URLs
        - metadata: Browser info, timing, test run info
        - analysis_flags: Computed flags for analysis
        """
        # Add timestamp
        data["timestamp"] = datetime.utcnow()
        
        # Add analysis flags
        if "analysis_flags" not in data:
            data["analysis_flags"] = self._compute_analysis_flags(data)
        
        # Insert and return ID
        result = self.results.insert_one(data)
        inserted_id = str(result.inserted_id)
        
        print(f"   💾 Saved: {data.get('persona_id', 'unknown')} × {data.get('prompt_id', 'unknown')} → {inserted_id[:8]}...")
        
        return inserted_id
    
    def _compute_analysis_flags(self, data: Dict) -> Dict:
        """Compute analysis flags from the response data."""
        response_text = data.get("response_text", "").lower()
        citations = data.get("citations", [])
        
        # Detect location mentions
        location_keywords = {
            "san francisco": ["san francisco", "sf", "bay area"],
            "new york": ["new york", "nyc", "manhattan", "brooklyn"],
            "boston": ["boston", "cambridge", "somerville"],
            "seattle": ["seattle", "pike place"],
            "los angeles": ["los angeles", "la", "hollywood"]
        }
        
        detected_locations = []
        for city, keywords in location_keywords.items():
            if any(keyword in response_text for keyword in keywords):
                detected_locations.append(city)
        
        # Analyze citation domains
        citation_domains = []
        for citation in citations:
            url = citation.get("url", "")
            if url:
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(url).netloc
                    citation_domains.append(domain)
                except:
                    pass
        
        # Check for business recommendations
        business_indicators = ["restaurant", "café", "coffee", "shop", "store", "hotel"]
        has_business_recommendation = any(indicator in response_text for indicator in business_indicators)
        
        # Check for specific addresses or streets
        import re
        has_specific_address = bool(re.search(r'\d+\s+\w+\s+(street|st|avenue|ave|road|rd|boulevard|blvd)', response_text, re.IGNORECASE))
        
        return {
            "detected_locations": detected_locations,
            "location_count": len(detected_locations),
            "citation_count": len(citations),
            "citation_domains": citation_domains,
            "has_business_recommendation": has_business_recommendation,
            "has_specific_address": has_specific_address,
            "response_length": len(data.get("response_text", "")),
            "has_geographic_content": len(detected_locations) > 0 or has_specific_address
        }
    
    def get_results_by_persona(self, persona_id: str) -> List[Dict]:
        """Get all test results for a specific persona."""
        return list(self.results.find({"persona_id": persona_id}))
    
    def get_results_by_prompt(self, prompt_id: str) -> List[Dict]:
        """Get all test results for a specific prompt."""
        return list(self.results.find({"prompt_id": prompt_id}))
    
    def compare_personas_for_prompt(self, prompt_id: str) -> List[Dict]:
        """Compare how different personas responded to the same prompt."""
        results = self.results.find({"prompt_id": prompt_id})
        return list(results)
    
    def get_geo_bias_summary(self) -> Dict:
        """Get summary of geographic bias in responses."""
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "persona_id": "$persona_id",
                        "prompt_id": "$prompt_id"
                    },
                    "detected_locations": {"$first": "$analysis_flags.detected_locations"},
                    "persona_location": {"$first": "$location.city"},
                    "has_citations": {"$first": "$has_citations"},
                    "citation_count": {"$first": "$analysis_flags.citation_count"}
                }
            }
        ]
        return list(self.results.aggregate(pipeline))
    
    def get_test_run_stats(self) -> Dict:
        """Get statistics for the entire test run."""
        total_tests = self.results.count_documents({})
        with_citations = self.results.count_documents({"has_citations": True})
        with_geo_content = self.results.count_documents({"analysis_flags.has_geographic_content": True})
        
        return {
            "total_tests": total_tests,
            "tests_with_citations": with_citations,
            "tests_with_geographic_content": with_geo_content,
            "citation_rate": with_citations / total_tests if total_tests > 0 else 0,
            "geo_content_rate": with_geo_content / total_tests if total_tests > 0 else 0
        }
    
    def close(self):
        """Close MongoDB connection."""
        self.client.close()
        print("🔌 MongoDB connection closed")