# GEO Testing Platform 🚀

**Generative Engine Optimization (GEO) Testing Suite** - Analyze how well your brand appears in AI-generated responses from ChatGPT.

![Status](https://img.shields.io/badge/status-active-success.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 Overview

The **GEO Testing Platform** helps businesses understand their visibility in generative AI responses. By simulating real user personas and search queries, it measures how often your brand appears when potential customers ask AI assistants for solutions.

### Why GEO Matters

- **80%+ of users** now start their research with AI assistants
- **Brand visibility** in AI responses drives discovery and trust
- **Organic mentions** are more valuable than paid placements
- **Competitive advantage** through AI-optimized content

### What This Tool Does

1. **Analyzes your website** using Perplexity AI with real-time search
2. **Generates realistic personas** representing your target audience
3. **Creates problem-focused queries** users might ask AI assistants
4. **Tests on ChatGPT** with automated browser simulation
5. **Provides AI-powered insights** on your brand visibility with actionable recommendations

---

## ✨ Features

### 🔍 **Intelligent Analysis**
- Real-time website analysis using Perplexity AI with search
- Automatic brand description generation
- AI-powered persona creation based on business context

### 👥 **Persona Generation**
- Creates 1-5 realistic user personas
- Includes demographics, goals, pain points, and behaviors
- Editable before testing

### 💬 **Prompt Engineering**
- Generates problem-focused search queries (not brand-specific)
- Multiple categories: informational, transactional, comparison, navigational
- Tests organic brand discovery

### 🤖 **Automated Testing**
- Headless browser automation with Playwright
- Authentic ChatGPT interaction (not API)
- Memory management between tests
- Persona context injection

### 📊 **Comprehensive Analytics**
- Brand mention rate tracking
- Citation rate analysis
- AI-powered GEO score (0-100)
- Persona and prompt performance breakdown
- Strengths, weaknesses, and recommendations

### 💾 **Data Persistence**
- MongoDB Atlas integration
- Complete response storage
- Historical data tracking
- Export capabilities

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GEO Testing Platform                     │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  React Frontend  │────▶│  Flask Backend   │────▶│  MongoDB Atlas   │
│  (Vite + Tailwind)│     │  (Python 3.x)    │     │  (Cloud DB)      │
└──────────────────┘     └──────────────────┘     └──────────────────┘
         │                        │
         │                        ├──────▶ Perplexity AI (Analysis)
         │                        ├──────▶ OpenAI GPT-4 (Prompts & Insights)
         │                        └──────▶ Playwright (ChatGPT Testing)
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│                   User Workflow                               │
├──────────────────────────────────────────────────────────────┤
│  1. Enter URL                                                 │
│  2. Review AI-generated brand description                     │
│  3. Generate & approve personas                               │
│  4. Generate & approve test prompts                           │
│  5. Run automated ChatGPT testing                             │
│  6. View analytics & AI insights                              │
└──────────────────────────────────────────────────────────────┘
```

### Tech Stack

**Frontend:**
- React 18
- Vite
- Tailwind CSS
- Headless UI

**Backend:**
- Python 3.13
- Flask
- Playwright
- pymongo

**AI Services:**
- Perplexity AI (sonar model with search)
- OpenAI GPT-4o-mini

**Database:**
- MongoDB Atlas

---

## 🚀 Quick Start

### Prerequisites

- Node.js 20.10.0+ (for frontend)
- Python 3.13+ (for backend)
- MongoDB Atlas account
- API Keys:
  - Perplexity AI
  - OpenAI
  - ChatGPT account credentials

### Installation

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd sundai_GEO
```

#### 2. Setup Backend

```bash
# Navigate to backend
cd geo-frontend/server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your API keys
```

**Backend `.env` configuration:**
```env
PERPLEXITY_API_KEY=your_perplexity_key_here
OPENAI_API_KEY=your_openai_key_here
MONGODB_URI=your_mongodb_atlas_connection_string
MONGODB_DATABASE=geo_sundai
PORT=5001
```

#### 3. Setup Frontend

```bash
# Navigate to frontend (from project root)
cd geo-frontend/client

# Install dependencies
npm install

# Frontend uses backend's .env (no separate config needed)
```

#### 4. Setup Testing Environment

```bash
# Navigate to testing directory
cd ../../geo-testing

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Create .env file
cp .env.example .env
# Edit .env with credentials
```

**Testing `.env` configuration:**
```env
CHATGPT_EMAIL=your_chatgpt_email
CHATGPT_PASSWORD=your_chatgpt_password
MONGODB_URI=your_mongodb_atlas_connection_string
MONGODB_DATABASE=geo_sundai
```

### Running the Application

#### Option 1: Use Start Scripts (Recommended)

```bash
# From project root
cd geo-frontend

# Terminal 1 - Start backend
./start-backend.sh

# Terminal 2 - Start frontend
./start-frontend.sh
```

#### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd geo-frontend/server
source venv/bin/activate
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd geo-frontend/client
npm run dev
```

**Access the application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:5001

---

## 🔄 How It Works

### Step-by-Step Workflow

#### **1. Website Analysis**
```
User enters URL → Perplexity AI analyzes with search →
Generates brand summary → User reviews and edits
```

#### **2. Persona Generation**
```
Brand context → Perplexity AI generates 1-5 personas →
Each persona includes:
  • Name, age, occupation, location
  • Goals and pain points
  • Behavior patterns
→ User approves/edits → Saved to MongoDB
```

#### **3. Prompt Generation**
```
Website analysis → OpenAI GPT-4o-mini generates prompts →
Problem-focused queries (not brand-specific):
  • "What are the best tools for..."
  • "How can I solve..."
  • "Compare solutions for..."
→ User approves/edits → Saved to MongoDB
```

#### **4. Automated Testing**
```
For each persona × each prompt:
  1. Launch Playwright browser
  2. Login to ChatGPT
  3. Clear ChatGPT memory
  4. Inject persona context
  5. Send prompt
  6. Extract response + citations
  7. Detect brand mentions
  8. Save to MongoDB
→ Repeat for all combinations (e.g., 3 personas × 3 prompts = 9 tests)
```

#### **5. Analytics & Insights**
```
All test results → Backend calculates stats:
  • Total tests
  • Brand mention rate
  • Citation rate
  • Persona performance
  • Prompt performance
→ OpenAI analyzes all data →
Generates:
  • GEO Performance Score (0-100)
  • Key insights
  • Strengths & weaknesses
  • Actionable recommendations
→ Display in beautiful UI
```

### Brand Detection Algorithm

The platform uses smart brand extraction to accurately detect mentions:

```python
# Example: "MongoDB - Build Better" from "https://mongodb.com"
# Extracts: ["mongodb", "mongodb.com", "mongodb - build better"]

Response: "You should use MongoDB for databases"
Detection: ✅ FOUND (matches "mongodb")

# This prevents false negatives from checking full titles/domains
```

---

## ⚙️ Configuration

### Environment Variables

#### Backend (`geo-frontend/server/.env`)

| Variable | Description | Required |
|----------|-------------|----------|
| `PERPLEXITY_API_KEY` | Perplexity AI API key | ✅ Yes |
| `OPENAI_API_KEY` | OpenAI API key | ✅ Yes |
| `MONGODB_URI` | MongoDB Atlas connection string | ✅ Yes |
| `MONGODB_DATABASE` | Database name (default: geo_sundai) | ✅ Yes |
| `PORT` | Backend port (default: 5001) | ❌ No |

#### Testing (`geo-testing/.env`)

| Variable | Description | Required |
|----------|-------------|----------|
| `CHATGPT_EMAIL` | ChatGPT account email | ✅ Yes |
| `CHATGPT_PASSWORD` | ChatGPT account password | ✅ Yes |
| `MONGODB_URI` | MongoDB Atlas connection string | ✅ Yes |
| `MONGODB_DATABASE` | Database name | ✅ Yes |

### MongoDB Collections

The platform creates these collections automatically:

- **`personas`** - Stores persona sets with website context
- **`prompts`** - Stores prompt sets for testing
- **`test_results`** - Stores all ChatGPT responses and analysis

---

## 📖 Usage Guide

### Running Your First Test

1. **Start the servers** (see Quick Start)

2. **Open the application** at http://localhost:5173

3. **Enter a website URL** (e.g., `https://mongodb.com`)
   - The system analyzes the website using Perplexity AI
   - Review and edit the generated brand description

4. **Generate Personas** (recommended: 3)
   - Click "Generate Personas"
   - Review each persona
   - Edit if needed
   - Click "Approve"

5. **Generate Prompts** (recommended: 3-5)
   - The system generates problem-focused queries
   - Review and edit prompts
   - Delete any irrelevant ones
   - Click "Approve & Start GEO Test"

6. **Watch the Testing**
   - Browser opens automatically
   - Progress updates: "3/9 tests complete..."
   - Takes ~2-3 minutes per test
   - Keep the window open

7. **View Results**
   - After all tests complete, analytics appear
   - View GEO score, insights, and recommendations
   - Filter results by brand mentions or citations
   - Expand individual results to see full responses

### Best Practices

**Persona Generation:**
- Use 3-5 personas for diverse coverage
- Ensure personas represent real target audiences
- Edit to match your customer demographics

**Prompt Creation:**
- Focus on problems, not brand names
- Use varied intent types (informational, transactional, comparison)
- Test realistic queries users would ask

**Testing:**
- Run tests during off-peak hours (fewer rate limits)
- Use a dedicated ChatGPT account for testing
- Monitor console output for debugging

---

## 📡 API Reference

### Backend Endpoints

#### Health Check
```http
GET /api/health
```
Returns API status and configuration.

#### Scrape & Analyze Website
```http
POST /api/scrape
Content-Type: application/json

{
  "url": "https://example.com"
}
```

#### Generate Personas
```http
POST /api/generate-personas
Content-Type: application/json

{
  "content": "Brand description text",
  "title": "Website Title",
  "url": "https://example.com",
  "num_personas": 3
}
```

#### Save Personas
```http
POST /api/personas/save
Content-Type: application/json

{
  "personas": [...],
  "website_url": "https://example.com",
  "website_title": "Website Title",
  "brand_description": "..."
}
```

#### Generate Prompts
```http
POST /api/generate-prompts
Content-Type: application/json

{
  "brand_description": "...",
  "website_analysis": "...",
  "website_title": "Website Title",
  "num_prompts": 5
}
```

#### Save Prompts
```http
POST /api/prompts/save
Content-Type: application/json

{
  "prompts": [...],
  "persona_set_id": "...",
  "website_url": "...",
  "website_title": "..."
}
```

#### Run GEO Test
```http
POST /api/run-geo-test
Content-Type: application/json

{
  "persona_set_id": "...",
  "prompts_id": "..."
}
```

#### Get Test Results
```http
GET /api/test-results/<test_run_id>
```
Returns complete results with AI analysis.

---

## 🐛 Troubleshooting

### Common Issues

#### **"Port 5001 is already in use"**
```bash
# Kill the process using port 5001
lsof -ti:5001 | xargs kill -9

# Restart backend
cd geo-frontend/server
source venv/bin/activate
python app.py
```

#### **"ModuleNotFoundError: No module named 'playwright'"**
```bash
# Activate correct virtual environment
cd geo-testing
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

#### **"ChatGPT login failed"**
- Verify credentials in `geo-testing/.env`
- Check if ChatGPT requires 2FA (disable for testing account)
- Ensure account is not rate-limited

#### **"Brand not detected even though mentioned"**
- Check console output for detected keywords
- Verify brand name extraction is working
- Review `run_from_db.py` line 280-289

#### **"Analytics appear after 1 test, not all tests"**
- This was fixed in latest version
- Ensure you have the latest code
- Check `TestingProgress.jsx` line 37

#### **Database Connection Issues**
```bash
# Verify MongoDB URI
echo $MONGODB_URI

# Test connection
python -c "from pymongo import MongoClient; client = MongoClient('your_uri'); print(client.list_database_names())"
```

### Debug Mode

Enable verbose logging:

**Backend:**
```python
# In app.py
app.config['DEBUG'] = True
```

**Testing:**
```bash
# Run with console output
cd geo-testing
python run_from_db.py <persona_set_id> <prompts_id>
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt  # If available

# Run tests
pytest  # If tests are implemented
```

---

## 📊 Project Status

- ✅ Website analysis with Perplexity AI
- ✅ Persona generation
- ✅ Prompt generation
- ✅ Automated ChatGPT testing
- ✅ Brand detection algorithm
- ✅ Analytics dashboard
- ✅ AI-powered insights
- ✅ MongoDB integration
- ✅ Progress tracking
- ✅ Results export

### Roadmap

- [ ] Support for other AI assistants (Claude, Gemini)
- [ ] Historical trend analysis
- [ ] Competitor comparison
- [ ] A/B testing for content strategies
- [ ] API rate limit optimization
- [ ] Batch testing capabilities
- [ ] Custom reporting templates

---

## 📝 License

This project is proprietary software. All rights reserved.

---

## 📞 Support

For issues, questions, or feature requests:
- Create an issue in the repository
- Contact: maria@citable.xyz

---

## 🙏 Acknowledgments

- **Perplexity AI** for real-time web search and analysis
- **OpenAI** for prompt generation and insights
- **Playwright** for browser automation
- **MongoDB** for data persistence

---

**Built with ❤️ for better GEO**

Last Updated: October 26, 2025
Version: 1.0.0

