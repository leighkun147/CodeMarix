# 🚀 CodexMatrix MVP - Quick Start Guide

## Overview

**CodexMatrix** is an AI code benchmarking engine that combines rich per-session analysis with a Firebase-backed global leaderboard. It evaluates code-generating AI models using a peer-review matrix ($M^2$) system.

### Key Features
- 🎯 **Session + Global** - In-depth per-session runs plus persistent aggregate stats in Firestore
- 🔐 **Privacy First** - API keys never saved to disk or Firestore
- ⚡ **Real-Time** - Live progress tracking & visualization
- 📊 **Peer Review** - Each model reviews every other model's code
- 📈 **Global Dashboards** - Interactive heatmaps, rankings, and comparisons across sessions

---

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- pip or conda

### 1. Clone & Navigate
```bash
cd /home/leykun/LingoDuel
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Key Requirements:**
- `streamlit` - UI framework
- `pandas` - Data handling
- `plotly` - Interactive charts
- `requests` - API calls
- `anthropic` (optional) - Claude API
- `openai` (optional) - GPT API
- `google-generativeai` (optional) - Gemini API

---

## 🎬 Running the App

### Start the Streamlit Server
```bash
streamlit run app.py
```

This will:
1. Open your browser at `http://localhost:8501`
2. Display the CodexMatrix MVP interface
3. Show the session setup sidebar

---

## 🎮 Using the App

### Step 1: Enter Coding Problems
In the **Sidebar**, write 1-5 coding challenges:
- Example: *"Implement a function to calculate Fibonacci numbers"*
- Use the text areas to provide detailed problem descriptions

### Step 2: Select Models
Choose 2+ AI models to benchmark:
- GPT-4o
- Claude 3.5 Sonnet
- Gemini 1.5 Pro
- (and others)

### Step 3: Select Programming Languages
Pick 1+ languages for code generation:
- Python, JavaScript, Java, C++, Rust, Go, etc.

### Step 4: Enter API Keys
Paste API keys for each selected model:
- **Important**: Keys are stored in RAM only (this session)
- Keys are automatically cleared when you close the browser
- Never committed to GitHub

### Step 5: Start Benchmark
Click **"🚀 Start Benchmark"** button

---

## 📊 Workflow Overview

The app executes 4 steps automatically:

### Step A: Code Generation
- Calls APIs for each model, language, and problem in parallel
- Handles timeouts and failures gracefully
- Returns cleaned code responses

### Step B: Peer Review Matrix
- Each model grades every other model's code
- Uses the model itself as the judge (LLM-based grading)
- 10 comprehensive rubric criteria:
  1. Correctness & Accuracy
  2. Efficiency (Time)
  3. Efficiency (Space)
  4. Readability & Clear Code
  5. Documentation & Comments
  6. Edge-Case Handling
  7. Error Handling & Robustness
  8. Security & Safe Practices
  9. Code Simplicity
  10. Best Practices & Standards
- Scores: 1-5 (1=Poor, 5=Excellent)

### Step C: Real-Time Analysis
- Aggregates all scores
- Determines session winner (highest average score)
- Builds interactive visualizations

### Step D: Display Results
Interactive dashboard with:
- **🏆 Winner Announcement** - Best performing model
- **📋 Leaderboard** - All models ranked by overall score
- **📊 Heatmap** - Shows who scored whom on each criterion
- **📈 Rankings** - Performance breakdown by rubric item
- **🎯 Top Model Comparison** - Side-by-side comparison
- **💾 Data Export** - Download session report (JSON)

---

## 🎭 Test Mode (No API Costs)

Want to test without real API calls?

1. **Enable Mock Mode**: Check ✅ "Use Mock Data" in sidebar
2. Run the benchmark normally
3. The app will generate fake code and scores for testing

Perfect for:
- Learning how the app works
- Testing the UI
- Debugging issues

---

## 📁 Project Structure

```
LingoDuel/
├── app.py                    # Main Streamlit application
├── src/
│   ├── requester.py         # API calls for code generation
│   ├── judge_matrix.py      # Peer review grading logic
│   ├── core/
│   │   └── stats_engine.py  # Real-time analysis & visualization
│   └── utils/
│       └── data_sanitizer.py # API response cleanup
├── database/                 # (Empty for now, Milestone 4)
├── requirements.txt          # Python dependencies
└── BUILD_PLAN.md            # Development roadmap

```

---

## 🔌 API Setup

### For OpenAI (GPT-4o)
1. Get key from https://platform.openai.com/api-keys
2. Paste into "GPT-4o API Key" field

### For Anthropic (Claude)
1. Get key from https://console.anthropic.com/
2. Paste into "Claude 3.5 Sonnet API Key" field

### For Google (Gemini)
1. Get key from https://makersuite.google.com/app/apikey
2. Paste into "Gemini 1.5 Pro API Key" field

---

## 🐛 Troubleshooting

### Issue: "Missing API keys"
**Solution**: Make sure you entered an API key for every selected model

### Issue: "Module not found" error
**Solution**: Ensure you're in the virtual environment and ran `pip install -r requirements.txt`

### Issue: API call timeouts
**Solution**: Try with fewer models, languages, or problems to reduce load

### Issue: Slow performance
**Solution**: 
- Use mock mode to test UI
- Reduce number of problems/languages
- Use faster models

### Issue: "Permission denied" when running streamlit
**Solution**: 
```bash
chmod +x app.py
streamlit run app.py
```

---

## 📚 Understanding the Output

### Leaderboard Table
Shows average scores for each model across all rubrics:
- **Model** - Model name
- **Correctness & Accuracy** - Does solution produce correct output?
- **Efficiency (Time)** - Optimal time complexity?
- **Efficiency (Space)** - Minimal memory usage?
- **Readability & Clear Code** - Easy to understand?
- **Documentation & Comments** - Well-documented?
- **Edge-Case Handling** - Handles boundaries?
- **Error Handling & Robustness** - Graceful error management?
- **Security & Safe Practices** - Any security issues?
- **Code Simplicity** - Elegant without unnecessary complexity?
- **Best Practices & Standards** - Follows language conventions?

### Heatmap
Matrix showing how each model scored others:
- **Rows** = Reviewers (who graded)
- **Columns** = Code Authors (whose code was graded)
- **Color intensity** = Score (darker=lower, brighter=higher)

### Top Models Comparison
Bar chart comparing top performers across all rubrics

---

## 🔐 Privacy & Security

✅ **What's Protected:**
- API keys stored in RAM only
- No persistent storage
- No user tracking
- No telemetry

✅ **What Happens on Browser Close:**
- All session data cleared from memory
- API keys erased
- Code samples deleted
- Review results deleted

---

## 🚀 Next Steps

### To Test the MVP:
```bash
# Make sure you're in the project directory
cd /home/leykun/LingoDuel

# Activate the environment
source venv/bin/activate

# Run the app
streamlit run app.py

# Go to http://localhost:8501 in your browser
```

### To Contribute:
- See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines
- Check [BUILD_PLAN.md](BUILD_PLAN.md) for upcoming features

### To Use With Real APIs:
1. Get API keys from your chosen providers
2. Paste them in the "API Keys" section
3. The app will make real calls (costs will apply!)

---

## 📞 Support

For issues or questions:
1. Check [BUILD_PLAN.md](BUILD_PLAN.md) for roadmap
2. Review [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines
3. Create an issue on GitHub

---

## 📄 License

See LICENSE file in the repository

---

## 🎉 Features Roadmap

**Phase 1 (Current MVP) ✅**
- Session-only architecture
- Peer review matrix
- Real-time visualization
- No database

**Phase 2 (Coming Soon)**
- Comprehensive testing suite
- Performance optimization
- Advanced debugging

**Phase 3 (Database Integration)**
- PostgreSQL backend
- Global leaderboards
- Cross-session comparisons
- User authentication

**Phase 4+ (Scaling & Ecosystem)**
- More LLM providers
- Custom rubrics
- Community benchmarks
- API endpoints
- Research partnerships

---

**Happy Benchmarking! 🚀**
