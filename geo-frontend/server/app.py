from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
from openai import OpenAI
import json
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'geo_sundai')

# Initialize OpenAI client for persona generation
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# Initialize Perplexity client for website analysis
perplexity_client = OpenAI(
    api_key=PERPLEXITY_API_KEY,
    base_url="https://api.perplexity.ai"
) if PERPLEXITY_API_KEY else None

# Initialize MongoDB
mongo_client = None
db = None
personas_collection = None

if MONGODB_URI:
    try:
        mongo_client = MongoClient(MONGODB_URI)
        db = mongo_client[MONGODB_DATABASE]
        personas_collection = db['personas']
        # Test connection
        mongo_client.admin.command('ping')
        print(f"✅ Connected to MongoDB: {MONGODB_DATABASE}")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")

@app.route('/api/scrape', methods=['POST'])
def scrape_url():
    """
    Analyze a website using Perplexity API with search enabled
    """
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if not perplexity_client:
            return jsonify({
                'error': 'Perplexity API key not configured',
                'message': 'Please add PERPLEXITY_API_KEY to your .env file'
            }), 500
        
        # Use Perplexity with search enabled to analyze the website
        prompt = f"""Analyze the website {url} and provide a comprehensive description including:

1. What the business/website is about
2. Main products or services offered
3. Target audience and customer segments
4. Key value propositions
5. Industry and market position
6. Any unique features or differentiators

Please provide a detailed, structured analysis."""

        response = perplexity_client.chat.completions.create(
            model="sonar",  # Model with search enabled
            messages=[
                {
                    "role": "system",
                    "content": "You are a business analyst expert. Analyze websites thoroughly and provide detailed, structured insights about the business, its offerings, and target audience."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.3,
        )
        
        analysis = response.choices[0].message.content
        
        # Generate a concise one-paragraph summary
        summary_prompt = f"""Based on this detailed analysis, write a single concise paragraph (3-4 sentences) describing what this business is and who it serves:

{analysis}

Write ONLY the paragraph, no extra text."""

        summary_response = perplexity_client.chat.completions.create(
            model="sonar",
            messages=[
                {
                    "role": "user",
                    "content": summary_prompt
                }
            ],
            max_tokens=200,
            temperature=0.3,
        )
        
        brand_summary = summary_response.choices[0].message.content.strip()
        
        # Extract title from URL (simple version)
        title = url.replace('https://', '').replace('http://', '').split('/')[0]
        
        # Structure the response
        scraped_data = {
            'success': True,
            'url': url,
            'title': title,
            'content': analysis,
            'markdown': analysis,
            'brand_summary': brand_summary,  # Add the concise summary
            'metadata': {
                'description': brand_summary,
                'source': 'Perplexity AI with search'
            },
            'language': 'en'
        }
        
        return jsonify(scraped_data), 200
            
    except Exception as e:
        return jsonify({
            'error': 'Failed to analyze website',
            'message': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'perplexity_configured': bool(PERPLEXITY_API_KEY),
        'openai_configured': bool(OPENAI_API_KEY)
    }), 200

@app.route('/api/generate-personas', methods=['POST'])
def generate_personas():
    """
    Generate 1-5 business personas based on scraped website content using Perplexity
    """
    try:
        if not perplexity_client:
            return jsonify({
                'error': 'Perplexity not configured',
                'message': 'Please add PERPLEXITY_API_KEY to your .env file'
            }), 500
        
        data = request.get_json()
        website_content = data.get('content', '')
        website_title = data.get('title', '')
        website_url = data.get('url', '')
        num_personas = data.get('num_personas', 3)
        
        if not website_content:
            return jsonify({'error': 'Content is required'}), 400
        
        # Create prompt for persona generation
        prompt = f"""Based on this business description, generate {num_personas} detailed, realistic customer personas:

Business: {website_title}
Description: {website_content}

For each persona, create:
1. Name (realistic first name only)
2. Age range (e.g., "25-34")
3. Occupation (specific job title)
4. Location (city, country)
5. Goals (2-3 specific goals related to this business)
6. Pain Points (2-3 challenges this business solves)
7. Behavior (how they would use this product/service)
8. Quote (one sentence in first person expressing their need)

Return ONLY valid JSON in this exact format (no extra text):
[
  {{
    "name": "string",
    "age": "string",
    "occupation": "string",
    "location": "string",
    "goals": ["string", "string"],
    "painPoints": ["string", "string"],
    "behavior": "string",
    "quote": "string"
  }}
]

Make personas diverse, realistic, and specific to this business."""

        # Call Perplexity API
        response = perplexity_client.chat.completions.create(
            model="sonar",
            messages=[
                {
                    "role": "system",
                    "content": "You are a marketing expert. Generate realistic customer personas in valid JSON format only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Parse the response
        personas_json = response.choices[0].message.content.strip()
        
        # Clean up any markdown code blocks
        if personas_json.startswith('```'):
            personas_json = personas_json.split('```')[1]
            if personas_json.startswith('json'):
                personas_json = personas_json[4:]
            personas_json = personas_json.strip()
        
        personas = json.loads(personas_json)
        
        return jsonify({
            'success': True,
            'personas': personas,
            'count': len(personas)
        }), 200
        
    except json.JSONDecodeError as e:
        return jsonify({
            'error': 'Failed to parse personas',
            'message': f'Invalid JSON response: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'Persona generation failed',
            'message': str(e)
        }), 500

@app.route('/api/personas/save', methods=['POST'])
def save_personas():
    """
    Save approved personas to MongoDB
    """
    try:
        if personas_collection is None:
            return jsonify({
                'error': 'Database not configured',
                'message': 'MongoDB connection is not available'
            }), 500
        
        data = request.get_json()
        personas = data.get('personas', [])
        website_url = data.get('website_url', '')
        website_title = data.get('website_title', '')
        brand_description = data.get('brand_description', '')
        
        if not personas:
            return jsonify({'error': 'No personas provided'}), 400
        
        # Create a persona set document
        persona_set = {
            'website_url': website_url,
            'website_title': website_title,
            'brand_description': brand_description,
            'personas': personas,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = personas_collection.insert_one(persona_set)
        
        return jsonify({
            'success': True,
            'id': str(result.inserted_id),
            'message': f'Saved {len(personas)} personas for {website_title}'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to save personas',
            'message': str(e)
        }), 500

@app.route('/api/personas', methods=['GET'])
def get_all_personas():
    """
    Get all persona sets from MongoDB
    """
    try:
        if personas_collection is None:
            return jsonify({
                'error': 'Database not configured',
                'message': 'MongoDB connection is not available'
            }), 500
        
        # Get all persona sets, sorted by most recent first
        persona_sets = list(personas_collection.find().sort('created_at', -1).limit(50))
        
        # Convert ObjectId to string for JSON serialization
        for persona_set in persona_sets:
            persona_set['_id'] = str(persona_set['_id'])
        
        return jsonify({
            'success': True,
            'persona_sets': persona_sets,
            'count': len(persona_sets)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve personas',
            'message': str(e)
        }), 500

@app.route('/api/personas/<persona_set_id>', methods=['GET'])
def get_persona_set(persona_set_id):
    """
    Get a specific persona set by ID
    """
    try:
        if personas_collection is None:
            return jsonify({
                'error': 'Database not configured',
                'message': 'MongoDB connection is not available'
            }), 500
        
        persona_set = personas_collection.find_one({'_id': ObjectId(persona_set_id)})
        
        if not persona_set:
            return jsonify({'error': 'Persona set not found'}), 404
        
        persona_set['_id'] = str(persona_set['_id'])
        
        return jsonify({
            'success': True,
            'persona_set': persona_set
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve persona set',
            'message': str(e)
        }), 500

@app.route('/api/generate-prompts', methods=['POST'])
def generate_prompts():
    """
    Generate test prompts based on website analysis using OpenAI GPT-4
    """
    try:
        if not openai_client:
            return jsonify({
                'error': 'OpenAI not configured',
                'message': 'Please add OPENAI_API_KEY to your .env file'
            }), 500
        
        data = request.get_json()
        brand_description = data.get('brand_description', '')
        website_analysis = data.get('website_analysis', '')
        website_title = data.get('website_title', '')
        num_prompts = data.get('num_prompts', 5)
        
        if not brand_description and not website_analysis:
            return jsonify({'error': 'Brand description or website analysis is required'}), 400
        
        content = brand_description or website_analysis
        
        # Create prompt for generating test prompts
        prompt = f"""Based on this business description, generate {num_prompts} realistic search queries that people would use when looking for a SOLUTION to their problem - NOT when searching for this specific brand.

Business: {website_title}
Description: {content}

IMPORTANT: Generate queries about the PROBLEM/NEED this business solves, NOT about the brand itself.

Examples:
- If the business is "Tinder" (dating app), generate: "What are good online dating platforms?" or "How can I meet new people?"
- If the business is "Stripe" (payments), generate: "How do I accept credit cards on my website?" or "Best payment processing for small business"
- If the business is "Notion" (productivity), generate: "What's a good tool for team collaboration?" or "How to organize project notes?"

Generate {num_prompts} diverse prompts that:
1. Focus on the USER'S PROBLEM or NEED (not the brand name)
2. Represent different search intents (informational, transactional, comparison)
3. Vary in specificity (broad problems and specific use cases)
4. Sound like natural questions a potential customer would ask
5. Should trigger the brand to appear in AI responses if the brand is well-optimized

DO NOT mention the brand name "{website_title}" in the prompts.

Return ONLY valid JSON in this exact format (no extra text):
[
  {{
    "prompt": "The actual query or question about the problem/need",
    "category": "informational|transactional|comparison",
    "intent": "What problem the user is trying to solve"
  }}
]

Make prompts realistic and problem-focused."""

        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a search behavior expert who understands user intent. Generate realistic search queries that focus on user PROBLEMS and NEEDS, not brand names. Users should be asking about solutions, not specific companies. Return only valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.8,
            max_tokens=1500
        )
        
        # Parse the response
        prompts_json = response.choices[0].message.content.strip()
        
        # Clean up any markdown code blocks
        if prompts_json.startswith('```'):
            prompts_json = prompts_json.split('```')[1]
            if prompts_json.startswith('json'):
                prompts_json = prompts_json[4:]
            prompts_json = prompts_json.strip()
        
        prompts = json.loads(prompts_json)
        
        return jsonify({
            'success': True,
            'prompts': prompts,
            'count': len(prompts)
        }), 200
        
    except json.JSONDecodeError as e:
        return jsonify({
            'error': 'Failed to parse prompts',
            'message': f'Invalid JSON response: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'Prompt generation failed',
            'message': str(e)
        }), 500

@app.route('/api/prompts/save', methods=['POST'])
def save_prompts():
    """
    Save generated prompts to MongoDB
    """
    try:
        if db is None:
            return jsonify({
                'error': 'Database not configured',
                'message': 'MongoDB connection is not available'
            }), 500
        
        data = request.get_json()
        prompts = data.get('prompts', [])
        persona_set_id = data.get('persona_set_id', '')
        website_url = data.get('website_url', '')
        website_title = data.get('website_title', '')
        
        if not prompts:
            return jsonify({'error': 'No prompts provided'}), 400
        
        # Create a prompts document
        prompts_doc = {
            'persona_set_id': persona_set_id,
            'website_url': website_url,
            'website_title': website_title,
            'prompts': prompts,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        prompts_collection = db['prompts']
        result = prompts_collection.insert_one(prompts_doc)
        
        return jsonify({
            'success': True,
            'id': str(result.inserted_id),
            'message': f'Saved {len(prompts)} prompts for {website_title}'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to save prompts',
            'message': str(e)
        }), 500

@app.route('/api/run-geo-test', methods=['POST'])
def run_geo_test():
    """
    Trigger GEO testing with saved personas and prompts
    """
    try:
        data = request.get_json()
        persona_set_id = data.get('persona_set_id', '')
        prompts_id = data.get('prompts_id', '')
        
        if not persona_set_id or not prompts_id:
            return jsonify({'error': 'persona_set_id and prompts_id are required'}), 400
        
        # Import and run the testing script
        import subprocess
        
        # Path to the geo-testing directory
        geo_testing_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'geo-testing'))
        script_path = os.path.join(geo_testing_path, 'run_from_db.py')
        python_path = os.path.join(geo_testing_path, 'venv', 'bin', 'python')
        
        # Check if paths exist
        if not os.path.exists(script_path):
            return jsonify({'error': f'Script not found: {script_path}'}), 500
        if not os.path.exists(python_path):
            return jsonify({'error': f'Python venv not found: {python_path}'}), 500
        
        # Create log file for this test run
        log_file = os.path.join(geo_testing_path, f'test_run_{persona_set_id}.log')
        
        # Run the test in the background with geo-testing venv
        # Redirect output to log file so we can monitor it
        with open(log_file, 'w') as log:
            process = subprocess.Popen(
                [python_path, script_path, persona_set_id, prompts_id],
                cwd=geo_testing_path,
                stdout=log,
                stderr=subprocess.STDOUT,  # Combine stderr with stdout
                text=True,
                start_new_session=True  # Detach from parent process
            )
        
        return jsonify({
            'success': True,
            'message': 'GEO testing started successfully',
            'persona_set_id': persona_set_id,
            'prompts_id': prompts_id,
            'process_id': process.pid,
            'log_file': log_file
        }), 200
        
    except Exception as e:
        import traceback
        return jsonify({
            'error': 'Failed to start GEO testing',
            'message': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/test-logs/<persona_set_id>', methods=['GET'])
def get_test_logs(persona_set_id):
    """
    Get real-time logs for a running test
    """
    try:
        geo_testing_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'geo-testing'))
        log_file = os.path.join(geo_testing_path, f'test_run_{persona_set_id}.log')
        
        if not os.path.exists(log_file):
            return jsonify({
                'success': False,
                'message': 'Log file not found. Test may not have started yet.'
            }), 404
        
        # Read last 100 lines of log file
        with open(log_file, 'r') as f:
            lines = f.readlines()
            last_lines = lines[-100:] if len(lines) > 100 else lines
        
        return jsonify({
            'success': True,
            'logs': ''.join(last_lines),
            'total_lines': len(lines)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to read logs',
            'message': str(e)
        }), 500

@app.route('/api/test-results/<test_run_id>', methods=['GET'])
def get_test_results(test_run_id):
    """
    Get results for a specific test run with AI analysis
    """
    try:
        if db is None:
            return jsonify({'error': 'Database not configured'}), 500
        
        # Query test_results collection
        results = list(db.test_results.find({
            '$or': [
                {'persona_set_id': test_run_id},
                {'prompts_id': test_run_id},
                {'test_run_id': test_run_id}
            ]
        }).sort('timestamp', -1))
        
        if not results:
            return jsonify({
                'success': False,
                'message': 'No results found yet. Tests may still be running.'
            }), 404
        
        # Convert ObjectId to string and convert datetime
        for result in results:
            result['_id'] = str(result['_id'])
            if 'timestamp' in result:
                result['timestamp'] = result['timestamp'].isoformat()
        
        # Calculate stats
        total = len(results)
        with_citations = sum(1 for r in results if r.get('has_citations'))
        brand_mentioned = sum(1 for r in results if r.get('brand_mentioned'))
        
        # Get website info from first result
        website_title = results[0].get('website_title', 'Unknown')
        website_url = results[0].get('website_url', '')
        
        stats = {
            'total_tests': total,
            'with_citations': with_citations,
            'brand_mentioned': brand_mentioned,
            'brand_mention_rate': brand_mentioned / total if total > 0 else 0,
            'citation_rate': with_citations / total if total > 0 else 0
        }
        
        # Generate AI analysis
        analysis = generate_ai_analysis(results, stats, website_title, website_url)
        
        return jsonify({
            'success': True,
            'results': results,
            'stats': stats,
            'analysis': analysis,
            'website_title': website_title,
            'website_url': website_url
        }), 200
        
    except Exception as e:
        import traceback
        return jsonify({
            'error': 'Failed to get results',
            'message': str(e),
            'traceback': traceback.format_exc()
        }), 500

def generate_ai_analysis(results, stats, website_title, website_url):
    """
    Use OpenAI to analyze test results and provide brand visibility insights
    Analyzes ALL test results, not just samples
    """
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Aggregate data from ALL results
        persona_performance = {}
        prompt_performance = {}
        all_test_details = []
        
        # Analyze ALL results (e.g., 3 personas × 3 prompts = 9 tests)
        for idx, result in enumerate(results, 1):
            persona_name = result.get('persona_details', {}).get('name', f'Persona {idx}')
            prompt_text = result.get('prompt_details', {}).get('prompt', f'Prompt {idx}')
            brand_mentioned = result.get('brand_mentioned', False)
            has_citations = result.get('has_citations', False)
            
            # Track persona performance
            if persona_name not in persona_performance:
                persona_performance[persona_name] = {'mentions': 0, 'tests': 0}
            persona_performance[persona_name]['tests'] += 1
            if brand_mentioned:
                persona_performance[persona_name]['mentions'] += 1
            
            # Track prompt performance
            if prompt_text not in prompt_performance:
                prompt_performance[prompt_text] = {'mentions': 0, 'tests': 0}
            prompt_performance[prompt_text]['tests'] += 1
            if brand_mentioned:
                prompt_performance[prompt_text]['mentions'] += 1
            
            # Collect test details
            all_test_details.append({
                'test_num': idx,
                'persona': persona_name,
                'prompt': prompt_text[:60] + '...' if len(prompt_text) > 60 else prompt_text,
                'brand_mentioned': brand_mentioned,
                'has_citations': has_citations
            })
        
        # Prepare comprehensive data summary
        summary_data = {
            'website': website_title,
            'url': website_url,
            'total_tests': stats['total_tests'],
            'brand_mention_rate': f"{stats['brand_mention_rate'] * 100:.1f}%",
            'citation_rate': f"{stats['citation_rate'] * 100:.1f}%",
            'persona_breakdown': [
                {
                    'name': name, 
                    'mention_rate': f"{(data['mentions']/data['tests']*100):.0f}%",
                    'tests': data['tests']
                }
                for name, data in persona_performance.items()
            ],
            'prompt_breakdown': [
                {
                    'prompt': prompt[:60] + '...' if len(prompt) > 60 else prompt,
                    'mention_rate': f"{(data['mentions']/data['tests']*100):.0f}%",
                    'tests': data['tests']
                }
                for prompt, data in prompt_performance.items()
            ],
            'all_tests': all_test_details
        }
        
        # Call OpenAI for analysis with ALL test data
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a GEO (Generative Engine Optimization) expert analyzing how well a brand appears in AI-generated responses. Analyze ALL test results to provide comprehensive, actionable insights."
                },
                {
                    "role": "user",
                    "content": f"""Analyze ALL GEO test results for {website_title}:

OVERALL METRICS:
- Total Tests Analyzed: {summary_data['total_tests']} (ALL tests included)
- Overall Brand Mention Rate: {summary_data['brand_mention_rate']}
- Overall Citation Rate: {summary_data['citation_rate']}

PERSONA PERFORMANCE (how each persona performed):
{json.dumps(summary_data['persona_breakdown'], indent=2)}

PROMPT PERFORMANCE (how each query performed):
{json.dumps(summary_data['prompt_breakdown'], indent=2)}

COMPLETE TEST RESULTS (all {summary_data['total_tests']} tests):
{json.dumps(summary_data['all_tests'], indent=2)}

Based on analyzing ALL {summary_data['total_tests']} test results above, provide:
1. Overall GEO Performance Score (0-100)
2. Key Insights (3-5 bullet points about patterns you see across ALL tests)
3. Strengths (what's working well across the test set)
4. Weaknesses (what needs improvement based on all tests)
5. Actionable Recommendations (3-5 specific actions based on the complete data)

Important: Your analysis should consider ALL {summary_data['total_tests']} tests, not just samples.

Format as JSON with keys: score, insights, strengths, weaknesses, recommendations"""
                }
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        # Parse AI response
        ai_analysis = response.choices[0].message.content
        
        # Try to parse as JSON, fallback to text
        try:
            import json
            analysis_data = json.loads(ai_analysis)
        except:
            analysis_data = {
                'score': 50,
                'insights': [ai_analysis],
                'strengths': [],
                'weaknesses': [],
                'recommendations': []
            }
        
        return analysis_data
        
    except Exception as e:
        print(f"Error generating AI analysis: {e}")
        return {
            'score': None,
            'insights': [f"Analysis unavailable: {str(e)}"],
            'strengths': [],
            'weaknesses': [],
            'recommendations': []
        }

@app.route('/api/analyze', methods=['POST'])
def analyze_content():
    """
    Analyze scraped content for GEO optimization
    This is a placeholder for future AI-powered analysis
    """
    try:
        data = request.get_json()
        content = data.get('content', '')
        
        # Placeholder analysis - you can integrate with OpenAI or other AI services
        analysis = {
            'word_count': len(content.split()),
            'character_count': len(content),
            'recommendations': [
                {
                    'category': 'Content Structure',
                    'status': 'good',
                    'message': 'Content has proper structure'
                },
                {
                    'category': 'Keyword Optimization',
                    'status': 'warning',
                    'message': 'Consider adding more relevant keywords'
                }
            ]
        }
        
        return jsonify(analysis), 200
        
    except Exception as e:
        return jsonify({'error': 'Analysis failed', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)

