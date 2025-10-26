# GEO Testing Framework - Usage Guide

## 🚀 Quick Start

### 1. Installation (Already Done ✅)

```bash
cd /Users/mariagorskikh/sundai_GEO/geo-testing

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install playwright pymongo python-dotenv

# Install browser
playwright install chromium
```

### 2. Verify Setup

```bash
source venv/bin/activate
python demo_test.py
```

---

## 📋 Available Scripts

### Test Scripts (scripts/ directory)

#### `scripts/record_login.py`
**Purpose:** Record authentication session to reuse across tests

**Usage:**
```bash
source venv/bin/activate
python scripts/record_login.py
```

**⚠️ IMPORTANT:** Before running, update the credentials in the file:
```python
page.get_by_role("textbox", name="Email address").fill("YOUR_EMAIL")
page.get_by_role("textbox", name="Password").fill("YOUR_PASSWORD")
```

**Output:** Creates `storage/auth_state.json` with your session

---

#### `scripts/record_chat.py`
**Purpose:** Test basic chat functionality with saved auth

**Usage:**
```bash
source venv/bin/activate
python scripts/record_chat.py
```

**What it does:**
- Loads saved authentication
- Sends an empty prompt
- Expects a specific response about coffee shops
- Validates the response

---

#### `scripts/record_memory_clear.py`
**Purpose:** Demonstrates how to clear ChatGPT memory

**Usage:**
```bash
source venv/bin/activate
python scripts/record_memory_clear.py
```

**What it does:**
- Opens ChatGPT with saved auth
- Navigates to personalization settings
- Clears all saved memories
- Closes browser

---

### Demo Scripts (root directory)

#### `demo_test.py`
**Purpose:** Verify installation and setup

**Usage:**
```bash
source venv/bin/activate
python demo_test.py
```

**Checks:**
- ✅ Playwright browser launch
- ✅ Workflow module imports
- ✅ Authentication state presence

---

#### `example_geo_test.py` ⭐
**Purpose:** Full GEO testing workflow example

**Usage:**
```bash
source venv/bin/activate
python example_geo_test.py
```

**What it does:**
1. Tests 3 scenarios:
   - Boston user asking for coffee shops
   - Seattle user asking for coffee shops
   - No location set (control)

2. For each scenario:
   - Clears ChatGPT memory
   - Sets persona (location/context)
   - Sends prompt
   - Extracts response + citations
   - Analyzes location mentions

3. Saves results to `geo_test_results.json`

**Output:**
- Console output with progress
- `geo_test_results.json` with detailed results
- Comparison of location-based responses

---

## 🧪 Creating Custom Tests

### Basic Chat Test

```python
from playwright.sync_api import sync_playwright
from workflows.login import load_auth_session
from workflows.chat import send_prompt, extract_response

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="storage/auth_state.json")
    page = context.new_page()
    
    # Load auth session
    load_auth_session(context, page)
    
    # Send a prompt
    send_prompt(page, "What's the weather like?")
    
    # Get response
    response = extract_response(page, turn_number=2)
    print(response['text'])
    print(f"Citations: {response['citations']}")
    
    context.close()
    browser.close()
```

---

### Testing with Personas

```python
from playwright.sync_api import sync_playwright
from workflows.login import load_auth_session
from workflows.chat import send_prompt, extract_response
from workflows.memory import clear_memory, set_persona

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="storage/auth_state.json")
    page = context.new_page()
    
    load_auth_session(context, page)
    
    # Clear existing memory
    clear_memory(page)
    
    # Set a persona
    set_persona(page, "I'm a software engineer in San Francisco who loves hiking")
    
    # Test prompt
    send_prompt(page, "Recommend weekend activities")
    response = extract_response(page)
    
    # Analyze results
    print(response['text'])
    
    context.close()
    browser.close()
```

---

## 📊 Workflow Functions Reference

### `workflows/login.py`

#### `load_auth_session(context, page)`
Loads saved authentication and navigates to ChatGPT

**Parameters:**
- `context`: Playwright BrowserContext
- `page`: Playwright Page

**Returns:** None (navigates to ChatGPT)

---

### `workflows/chat.py`

#### `send_prompt(page, prompt)`
Sends a message to ChatGPT

**Parameters:**
- `page`: Playwright Page
- `prompt`: String message to send

**Returns:** None

---

#### `extract_response(page, turn_number=2)`
Extracts ChatGPT's response with citations

**Parameters:**
- `page`: Playwright Page
- `turn_number`: Which conversation turn (2 = first response)

**Returns:** Dictionary with:
```python
{
    "text": "Full response text",
    "citations": [
        {
            "position": 1,
            "title": "Link text",
            "url": "https://..."
        }
    ],
    "has_citations": True/False
}
```

---

### `workflows/memory.py`

#### `clear_memory(page)`
Clears all ChatGPT saved memories

**Parameters:**
- `page`: Playwright Page (must be on ChatGPT)

**Returns:** None

**Note:** Navigates through settings UI automatically

---

#### `set_persona(page, persona_text)`
Sets a persona by chatting with ChatGPT

**Parameters:**
- `page`: Playwright Page
- `persona_text`: String describing user (location, preferences, etc.)

**Returns:** None

**What it does:**
1. Sends persona as a chat message
2. Waits for ChatGPT to process and save to memory
3. Starts a new chat to clear conversation context

**Example:**
```python
set_persona(page, "I live in New York City and work in finance")
```

---

## 🔧 Configuration

### Browser Settings

All scripts use these default settings:
```python
browser = playwright.chromium.launch(headless=False)
context = browser.new_context(
    storage_state="storage/auth_state.json",
    viewport={"width": 1280, "height": 720}
)
```

**To run headless (no visible browser):**
```python
browser = playwright.chromium.launch(headless=True)
```

---

### Timeouts

Default timeouts in the code:
- Element wait: 10 seconds
- Response wait: 60 seconds
- Citation load: 2 seconds

**To customize:**
```python
# In workflows/chat.py
response_locator.wait_for(timeout=120000)  # 2 minutes
```

---

## 📁 Project Structure

```
geo-testing/
├── venv/                      # Virtual environment (created by you)
├── scripts/                   # Executable test scripts
│   ├── record_login.py       # Save auth session
│   ├── record_chat.py        # Test chat
│   └── record_memory_clear.py # Test memory clearing
├── workflows/                 # Reusable functions
│   ├── login.py              # Auth management
│   ├── chat.py               # Chat interactions
│   └── memory.py             # Persona/memory management
├── storage/                   # Saved data
│   └── auth_state.json       # Browser session
├── utils/                     # Utilities (empty - for future use)
│   ├── browser.py
│   └── database.py
├── demo_test.py              # Setup verification
├── example_geo_test.py       # Full GEO test example
├── pyproject.toml            # Project config
└── USAGE.md                  # This file
```

---

## 🎯 Common Use Cases

### 1. Test Location Bias
```bash
python example_geo_test.py
```

### 2. Compare Response Quality
Create custom test with different prompts:
```python
prompts = [
    "Explain quantum computing",
    "Recommend a restaurant", 
    "Help me learn Python"
]

for prompt in prompts:
    send_prompt(page, prompt)
    response = extract_response(page)
    analyze(response)
```

### 3. Citation Analysis
```python
response = extract_response(page)

for citation in response['citations']:
    print(f"Source: {citation['url']}")
    # Analyze domain, authority, recency
```

---

## ⚠️ Important Notes

### Authentication
- The saved `auth_state.json` expires after some time
- Re-run `scripts/record_login.py` if you get login errors
- Never commit `auth_state.json` to git (contains tokens)

### Rate Limiting
- ChatGPT may rate limit rapid requests
- Add delays between tests: `time.sleep(5)`
- Consider using ChatGPT Plus for higher limits

### Memory Clearing
- Memory clearing requires specific UI navigation
- If ChatGPT UI changes, the selectors may break
- Update selectors in `workflows/memory.py` if needed

---

## 🐛 Troubleshooting

### "Element not found" errors
**Cause:** ChatGPT UI has changed
**Fix:** Update selectors in workflow files

### Timeout errors
**Cause:** Slow internet or ChatGPT processing time
**Fix:** Increase timeout values in functions

### "Not logged in" errors
**Cause:** Auth session expired
**Fix:** Re-run `scripts/record_login.py`

### Browser crashes
**Cause:** Insufficient memory or conflicts
**Fix:** Close other browsers, restart script

---

## 📚 Additional Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [ChatGPT Memory Settings](https://help.openai.com/en/articles/8590148-memory-in-chatgpt)

---

## 🤝 Contributing

To extend this framework:

1. **Add database storage** (utils/database.py)
   - Store test results in MongoDB
   - Query historical data

2. **Add analysis tools**
   - Statistical comparison of results
   - Visualization of geographic biases

3. **Add more workflows**
   - Image analysis
   - Voice interactions
   - Custom GPT testing

---

**Happy Testing! 🚀**

