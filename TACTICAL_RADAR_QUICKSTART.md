# 🎯 Tactical Radar Analysis - Quick Start Guide

## What's New?

CodexMatrix now features an advanced **Tactical Radar Analysis System** - a military-themed multi-dimensional visualization dashboard for comparing AI model performance.

---

## 🎬 Getting Started

### 1. Run the Application
```bash
cd /home/leykun/LingoDuel
source venv/bin/activate
streamlit run app.py
```

### 2. Follow the Setup Wizard
- Enter coding problems to benchmark
- Select AI models to compare
- Choose programming languages
- Provide API keys (or use mock data)

### 3. Watch the Benchmark Execute
- **Phase 1**: Code generation across all model/language combinations
- **Phase 2**: Peer review matrix (each model grades others)
- **Phase 3**: Real-time analysis and scoring

### 4. Navigate to Results

Once analysis completes, you'll see:
```
🏆 Session Results & Winner Determination
├─ Winner Announcement (🏆 banner)
├─ Session Statistics (4 metrics)
├─ Overall Leaderboard
└─ Analysis Tabs:
   ├─ 📊 Heatmap (Peer Review Matrix)
   ├─ 📈 Rankings by Criteria
   ├─ 🎯 Top Models Comparison
   ├─ 🎯 TACTICAL RADAR ← NEW! ⭐
   └─ 💾 Raw Data Download
```

---

## ⚡ Using the Tactical Radar Tab

### Select Analysis Mode
Two powerful modes available:

#### Mode 1: 📊 Single Model Analysis
Analyze one model's performance across all 5 tactical dimensions:
- **Correctness** - Algorithmic correctness + edge-case handling
- **Efficiency** - Time complexity + space complexity
- **Readability** - Code clarity + code simplicity
- **Documentation** - Comments and documentation quality
- **Security** - Error handling + security practices + best practices

**How to Use:**
1. Click the "📊 Single Model" radio button
2. Select a model from the dropdown
3. View the radar pentagon showing all dimensions
4. Hover over sections to see exact scores
5. Click "📋 DETAILED METRICS BREAKDOWN" for granular details

**Visual Guide:**
```
         Documentation
              /\
             /  \
        Security  Correctness
           /        \
          /          \
   Efficiency ---- Readability
   
   (5-point scale shown as radius distance)
```

---

#### Mode 2: ⚔️ Model Overlay Comparison
Compare two models head-to-head to identify competitive advantages.

**How to Use:**
1. Click the "⚔️ Model Overlay" radio button
2. Select **Model 1** (Primary - shown in green #00ff41)
3. Select **Model 2** (Comparison - shown in cyan #00d9ff)
4. View overlaid radar showing both models
5. Click "🎯 TACTICAL COMPARISON SUMMARY" for:
   - Average score comparison with winner announcement
   - Dimension-by-dimension advantage breakdown
   - Tactical strengths & weaknesses analysis

**Color Legend:**
- 🟢 **Green (Solid Line)**: Model 1 - Primary model & assessment
- 🔵 **Cyan (Dashed Line)**: Model 2 - Secondary model & comparison
- Pentagon shape shows relative performance strength
- Larger pentagon area = higher overall performance

---

## 📊 Understanding the Radar Chart

### Scale Interpretation
- **5.0**: Excellent (Gold standard)
- **4.0-4.9**: Very Good (High quality)
- **3.0-3.9**: Good (Satisfactory)
- **2.0-2.9**: Fair (Needs improvement)
- **1.0-1.9**: Poor (Significant issues)
- **0.0**: No data / Not evaluated

### Shape Analysis
- **Balanced/Round Pentagon**: Well-rounded model with consistent performance
- **Pointy/Unbalanced**: Specialized model - strong in some areas, weak in others
- **Large Overlay Gap**: Significant performance difference between models

### Color Meanings
- **Bright Green**: Military alert state - high tactical readiness
- **Cyan**: Targeting state - element of comparison/focus
- **Grid Pattern**: Tactical readiness display

---

## 💡 Practical Examples

### Example 1: Identifying a Specialist Model
```
Model: DeepSeek-Coder

Radar shows:
- Correctness: ⭐⭐⭐⭐⭐ (5.0) - PEAK PERFORMANCE
- Efficiency: ⭐⭐⭐ (3.2) - Average
- Readability: ⭐⭐⭐⭐ (4.1) - Strong
- Documentation: ⭐⭐ (2.0) - Weak
- Security: ⭐⭐⭐⭐⭐ (5.0) - PEAK PERFORMANCE

🎯 Interpretation: 
Use for security-critical and correctness-dependent tasks.
Not ideal when documentation and efficiency matter most.
```

### Example 2: Finding the Balanced Winner
```
Model: Claude-3-Opus

Overlay vs GPT-4:
- Correctness: ✅ Tied (5.0 vs 5.0)
- Efficiency: ✅ Claude Wins (4.5 vs 3.8)
- Readability: ❌ GPT Wins (4.2 vs 4.8)
- Documentation: ✅ Claude Wins (4.6 vs 3.9)
- Security: ✅ Tied (4.7 vs 4.7)

🎯 Verdict: Claude edges out GPT-4 in 3/5 dimensions,
with efficiency being a key differentiator.
```

---

## 🎨 UI Elements Explained

### Military Design Elements

**🟢 Neon Green Highlights**
- Active/focused elements
- Primary action buttons
- Main tactical readiness indicator

**🔵 Cyan Borders**
- Secondary focus points
- Comparison/overlay indicators
- Navigation elements

**📡 Scan Lines & Grid**
- Background atmosphere
- Creates "command center" aesthetic
- Enhances professional appearance

**Glowing Effects**
- Box-shadow hauls emphasizing interactive elements
- Stronger glow on hover
- Indicates system responsiveness

---

## 🔧 Advanced Features

### Data Export
1. Click "💾 Raw Data" tab
2. View formatted session report
3. Click "📥 Download Session Report (JSON)"
4. Use data for:
   - Further analysis
   - Academic research
   - Performance tracking
   - Team presentations

### Accessing Raw Metrics
```json
{
  "session_info": {
    "start_time": "2026-03-21T14:32:00",
    "models": ["Model1", "Model2", "Model3"],
    "languages": ["Python", "JavaScript"],
    "problems_count": 5, 
    "winner": "Model1",
    "winner_score": 4.75
  },
  "leaderboard": { ... },
  "consensus_scores": { ... },
  "summary_stats": { ... }
}
```

---

## 🎯 Best Practices

### When Running Benchmarks
1. ✅ **Test multiple models** (3-5 for meaningful comparison)
2. ✅ **Vary problems** (different algorithmic challenges)
3. ✅ **Try multiple languages** (reveal language-specific patterns)
4. ✅ **Use real API keys** (mock data for testing only)
5. ✅ **Export results** (preserve session data)

### Interpreting Results
1. ✅ **Look for patterns** (does one model consistently excel?)
2. ✅ **Check consistency** (is performance stable across dimensions?)
3. ✅ **Consider specialization** (some models may be specialists)
4. ✅ **Factor context** (some dimensions matter more for your use case)
5. ✅ **Run multiple sessions** (results may vary, so establish trends)

### Using Insights
- **For Production**: Choose model with highest "Correctness" + "Security"
- **For Speed**: Optimize for "Efficiency" scores
- **For Maintenance**: Prioritize "Readability" + "Documentation"
- **For Innovation**: Look for unique patterns in specialists

---

## 🐛 Troubleshooting

### Radar Chart Not Displaying?
**Solution:** 
- Ensure benchmark has completed all phases
- Check that models have scoring data
- Try refreshing the page

### Model Not Appearing in Dropdown?
**Solution:**
- Verify model was selected during setup
- Confirm it successfully generated code
- Check for API errors in generation phase

### Values Seem Incorrect?
**Solution:**
- Values are aggregated averages from peer reviews
- Each model grades every other model
- Review process is shown in "Heatmap" tab
- Raw data is available for verification

### Performance Issues?
**Solution:**
- Reduce number of models (fewer = faster)
- Reduce number of problems (fewer = faster)
- Use fewer languages (reduces complexity)
- Close other browser tabs

---

## 📈 Performance Metrics Formula

Each dimension score is calculated as:
```
Dimension Score = Average(all_rubric_items_in_dimension) / count_of_reviewers

Scale: 1-5 points
Aggregation: Mean across all peer reviews
```

**Example:**
```
Correctness = (Score_Reviewer1 + Score_Reviewer2 + Score_Reviewer3) / 3
            = (5 + 4 + 5) / 3
            = 4.67 / 5
```

---

## 🚀 Next Level: Custom Analysis

### Export for Further Study
1. Download JSON report
2. Use Python/R/Excel for deeper analysis
3. Create custom visualizations
4. Build performance trends over time

### Use Cases
- **Academic Research**: Publish findings on model performance
- **Team Decisions**: Share insights with engineering team
- **Vendor Evaluation**: Compare LLM providers
- **Performance Tracking**: Monitor improvements over time

---

## 📞 Support

### Common Questions

**Q: How accurate are these ratings?**
A: Ratings reflect peer consensus across multiple reviewers (AI models). The peer matrix ensures no single rater bias.

**Q: Can I weight dimensions differently?**
A: Currently all dimensions are equally weighted. Raw data is available for custom weighting.

**Q: How long does a benchmark take?**
A: Depends on models, languages, and number of API calls. Typically 5-15 minutes for full session.

**Q: Why do overlaid models look so different?**
A: Real performance differences! This visualization exposes gaps between models clearly.

---

## 🎯 Command Center Status

**SYSTEM**: 🟢 ONLINE  
**THEME**: Military Command Center v1.0  
**VISUALIZATION**: Tactical Radar Analysis  
**DEPLOYMENT**: Ready for Operations  
**LAST UPDATE**: March 21, 2026  

---

**Ready to launch your tactical AI benchmarking operation? 🚀**

Start the application and explore the radar analysis to discover your model's competitive advantages!
