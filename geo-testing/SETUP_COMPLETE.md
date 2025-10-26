# ✅ GEO Testing Framework - Setup Complete!

## 🎉 Installation Summary

Your GEO testing framework is fully installed and working!

### What Was Installed

1. ✅ **Python 3.13.7** - Already on your system
2. ✅ **Virtual Environment** - Created at `venv/`
3. ✅ **Python Dependencies:**
   - Playwright 1.55.0 (browser automation)
   - PyMongo 4.15.3 (database driver)
   - Python-dotenv 1.2.1 (environment variables)
4. ✅ **Chromium Browser** - Playwright-managed browser
5. ✅ **Authentication State** - Pre-existing (271 KB)

---

## 🚀 Quick Start Commands

### Activate Virtual Environment
```bash
cd /Users/mariagorskikh/sundai_GEO/geo-testing
source venv/bin/activate
```

### Run Demo Scripts

#### 1. Verify Setup
```bash
python demo_test.py
```
**Output:** Confirms all components are working

---

#### 2. Quick Chat Test (⚡ Fastest)
```bash
python quick_chat_test.py
```
**What it does:**
- Sends a single prompt to ChatGPT
- Extracts and displays the response
- Takes ~10-15 seconds

**Output Example:**
```
Response Text: "Boston built America's first subway system in 1897..."
Citations: 0
```

---

#### 3. Full GEO Testing (🌍 Comprehensive)
```bash
python example_geo_test.py
```
**What it does:**
- Tests 3 different geographic personas
- Compares responses for location bias
- Saves results to `geo_test_results.json`
- Takes ~3-5 minutes

**Tests:**
1. Boston user asking for coffee shops
2. Seattle user asking for coffee shops
3. No location set (control group)

---

## 📁 File Structure

```
geo-testing/
├── 📜 Scripts You Can Run
│   ├── demo_test.py              ← Verify setup
│   ├── quick_chat_test.py        ← Quick demo (10 sec)
│   └── example_geo_test.py       ← Full GEO test (3 min)
│
├── 🔧 Original Scripts (from repo)
│   └── scripts/
│       ├── record_login.py       ← Save auth session
│       ├── record_chat.py        ← Test chat
│       └── record_memory_clear.py ← Clear memory
│
├── 📚 Reusable Functions
│   └── workflows/
│       ├── login.py              ← Auth management
│       ├── chat.py               ← Send/receive messages
│       └── memory.py             ← Persona/memory control
│
├── 💾 Data Storage
│   └── storage/
│       └── auth_state.json       ← Your ChatGPT session
│
├── 📖 Documentation
│   ├── USAGE.md                  ← Complete usage guide
│   └── SETUP_COMPLETE.md         ← This file
│
└── 🐍 Python Environment
    ├── venv/                     ← Virtual environment
    ├── requirements.txt          ← Dependencies list
    └── pyproject.toml            ← Project config
```

---

## 🎯 Common Tasks

### Test a Custom Prompt

Edit `quick_chat_test.py` line 13:
```python
test_prompt = "Your custom question here"
```

Then run:
```bash
python quick_chat_test.py
```

---

### Create Your Own Test Script

```python
from playwright.sync_api import sync_playwright
from workflows.login import load_auth_session
from workflows.chat import send_prompt, extract_response

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="storage/auth_state.json")
    page = context.new_page()
    
    load_auth_session(context, page)
    send_prompt(page, "Your prompt here")
    response = extract_response(page)
    
    print(response['text'])
    
    context.close()
    browser.close()
```

---

### Test Geographic Bias

Run the full test:
```bash
python example_geo_test.py
```

Then analyze `geo_test_results.json`:
```bash
cat geo_test_results.json | python -m json.tool
```

---

## 🔍 What We Tested

### ✅ Demo Test Output
```
✅ Browser test successful!
✅ All workflow functions found
✅ Auth state found (271,058 bytes)
```

### ✅ Quick Chat Test Output
```
Prompt: "Tell me a fun fact about Boston in one sentence."
Response: "Boston built America's first subway system in 1897..."
✅ Test complete!
```

---

## 📚 Next Steps

### 1. Learn the System
Read the comprehensive guide:
```bash
cat USAGE.md
# or
open USAGE.md
```

### 2. Run Full GEO Test
```bash
source venv/bin/activate
python example_geo_test.py
```

This will:
- Test multiple geographic personas
- Extract citations and location mentions
- Generate `geo_test_results.json` with analysis

### 3. Customize for Your Research

**Example: Test Restaurant Recommendations**
```python
test_scenarios = [
    {"persona": "I live in Miami", "prompt": "Best Cuban restaurant?"},
    {"persona": "I live in NYC", "prompt": "Best Cuban restaurant?"},
]
```

**Example: Test Language/Cultural Bias**
```python
test_scenarios = [
    {"persona": "I'm from the UK", "prompt": "Explain American football"},
    {"persona": "I'm from the US", "prompt": "Explain American football"},
]
```

---

## 🔐 Security Notes

### Current Auth State
- Pre-existing `auth_state.json` found (from repo)
- Contains ChatGPT session for `cyfox66@gmail.com`
- **May expire after some time**

### To Use Your Own Account

1. **Edit** `scripts/record_login.py`:
   ```python
   page.get_by_role("textbox", name="Email address").fill("YOUR_EMAIL")
   page.get_by_role("textbox", name="Password").fill("YOUR_PASSWORD")
   ```

2. **Run** the login script:
   ```bash
   python scripts/record_login.py
   ```

3. **Verify** new auth state created:
   ```bash
   ls -lh storage/auth_state.json
   ```

---

## ⚙️ Configuration Options

### Run Headless (No Browser Window)

Edit any script and change:
```python
browser = playwright.chromium.launch(headless=False)
```
to:
```python
browser = playwright.chromium.launch(headless=True)
```

### Adjust Timeouts

In `workflows/chat.py`:
```python
response_locator.wait_for(timeout=60000)  # 60 seconds
```

Change to:
```python
response_locator.wait_for(timeout=120000)  # 120 seconds
```

### Change Viewport Size

```python
context = browser.new_context(viewport={"width": 1920, "height": 1080})
```

---

## 🐛 Troubleshooting

### "Module not found" Error
**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Browser not found" Error
**Solution:**
```bash
source venv/bin/activate
playwright install chromium
```

### "Not logged in" Error
**Solution:**
```bash
python scripts/record_login.py  # With your credentials
```

### Timeout Errors
**Causes:**
- Slow internet connection
- ChatGPT is processing a complex query
- Server is busy

**Solution:**
- Increase timeout values
- Wait and try again
- Check internet connection

---

## 📊 Understanding Results

### Response Structure
```python
{
    "text": "Full response text from ChatGPT",
    "citations": [
        {
            "position": 1,
            "title": "Link text",
            "url": "https://example.com"
        }
    ],
    "has_citations": True,
}
```

### Citation Analysis
- **Position:** Order in response (1st, 2nd, 3rd link)
- **Title:** Display text of the link
- **URL:** Actual destination

### Geographic Bias Indicators
Look for:
- Local business names
- City/state mentions
- Regional terminology
- Area codes/zip codes
- Local landmarks

---

## 🔄 Workflow Recap

```
┌─────────────────────────────────────┐
│ 1. ONE-TIME SETUP (Already Done!)  │
│    ✅ Install dependencies          │
│    ✅ Install browser               │
│    ✅ Auth state exists             │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ 2. RUN TESTS                        │
│    • Activate venv                  │
│    • Run test scripts               │
│    • Analyze results                │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ 3. CUSTOMIZE                        │
│    • Modify test scenarios          │
│    • Add new workflows              │
│    • Store results in database      │
└─────────────────────────────────────┘
```

---

## 💡 Pro Tips

### 1. Use Screen Recording
```bash
# Record your tests
brew install screen-capture-recorder
# Then use QuickTime to record the browser automation
```

### 2. Batch Testing
Create a loop:
```python
prompts = ["prompt1", "prompt2", "prompt3"]
for prompt in prompts:
    send_prompt(page, prompt)
    response = extract_response(page)
    save_to_file(response)
    time.sleep(5)  # Rate limiting
```

### 3. Response Comparison
```python
import difflib

diff = difflib.unified_diff(
    response1['text'].splitlines(),
    response2['text'].splitlines()
)
print('\n'.join(diff))
```

### 4. Citation Domain Analysis
```python
from urllib.parse import urlparse

for citation in response['citations']:
    domain = urlparse(citation['url']).netloc
    print(f"Source: {domain}")
```

---

## 🎓 Learning Resources

### Playwright Documentation
- **Python API:** https://playwright.dev/python/
- **Selectors:** https://playwright.dev/python/docs/selectors
- **Auto-wait:** https://playwright.dev/python/docs/actionability

### ChatGPT Memory
- **Help Article:** https://help.openai.com/en/articles/8590148
- **Privacy:** https://openai.com/policies/privacy-policy

### Python Best Practices
- **Virtual Environments:** https://docs.python.org/3/tutorial/venv.html
- **JSON Handling:** https://docs.python.org/3/library/json.html

---

## 📈 Future Enhancements

### Potential Additions

1. **Database Integration** (utils/database.py)
   - Store all test results in MongoDB
   - Query historical trends
   - Compare results over time

2. **Statistical Analysis**
   - Response similarity metrics
   - Citation frequency analysis
   - Geographic bias scoring

3. **Visualization**
   - Charts of location mentions
   - Citation network graphs
   - Response length comparisons

4. **Advanced Testing**
   - Multi-turn conversations
   - Image-based prompts
   - Voice interactions

---

## 🤝 Support

### Check Logs
```bash
# If something fails, check Python traceback
python quick_chat_test.py 2>&1 | tee test_log.txt
```

### Verify Components
```bash
python demo_test.py
```

### Test Individual Functions
```python
from workflows.chat import send_prompt, extract_response
# Test imports work

from playwright.sync_api import sync_playwright
# Test Playwright works
```

---

## ✅ Summary

### What Works Right Now
- ✅ Browser automation with Playwright
- ✅ ChatGPT authentication (pre-loaded)
- ✅ Send prompts and extract responses
- ✅ Extract citations from responses
- ✅ Clear and set ChatGPT memory/personas
- ✅ Multiple test scenarios
- ✅ JSON result storage

### What You Can Do
1. Run quick chat tests (`quick_chat_test.py`)
2. Run full GEO tests (`example_geo_test.py`)
3. Create custom test scripts
4. Analyze geographic biases in responses
5. Compare citation patterns

### Your First Test (Right Now!)
```bash
cd /Users/mariagorskikh/sundai_GEO/geo-testing
source venv/bin/activate
python quick_chat_test.py
```

---

**🎉 You're all set! Happy testing!**

For detailed usage instructions, see `USAGE.md`
For questions about the code logic, see the original explanation above.

---

**Created:** October 26, 2025
**Framework Version:** 0.1.0
**Python Version:** 3.13.7
**Playwright Version:** 1.55.0

