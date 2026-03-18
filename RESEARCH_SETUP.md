# 🔬 Research-Grade Setup Guide

## For Academic & Research Purposes

CodexMatrix can be used for research papers, benchmarks, and publications **IF AND ONLY IF** you use real, authenticated API keys with actual LLM providers.

---

## ⚠️ Important: Mock Mode is NOT for Research

**❌ Mock Mode:**
- Returns simulated/random scores
- NOT suitable for research papers
- NOT suitable for publications
- NOT suitable for peer review procedures

**✅ Research Mode:**
- Uses real API keys
- Gets ACTUAL grading from LLMs
- Produces authentic peer-review scores
- Suitable for academic use

---

## 🔑 Getting Real API Keys

### Option 1: OpenAI (GPT-4o)

1. **Go to**: https://platform.openai.com/api-keys
2. **Sign up or log in** with your OpenAI account
3. **Create new API key**
4. **Copy the key** (starts with `sk-` or `sk_proj-`)
5. **Paste into CodexMatrix sidebar** under "GPT-4o API Key"

**Cost**: ~$0.03 per benchmark run (depending on code complexity)

**Benefits**: Most capable model, frequently updated

### Option 2: Anthropic (Claude 3.5 Sonnet)

1. **Go to**: https://console.anthropic.com/
2. **Sign up or log in** with your Anthropic account
3. **Create API key** in Account Settings
4. **Copy the key** (typically 40+ characters)
5. **Paste into CodexMatrix sidebar** under "Claude 3.5 Sonnet API Key"

**Cost**: ~$0.02 per benchmark run

**Benefits**: Excellent code understanding, strong on security issues

### Option 3: Google (Gemini 1.5 Pro)

1. **Go to**: https://makersuite.google.com/app/apikey
2. **Create API key**
3. **Copy the key**
4. **Paste into CodexMatrix sidebar** under "Gemini 1.5 Pro API Key"

**Cost**: ~$0.01 per benchmark run

**Benefits**: Fast, efficient, good for algorithmic problems

---

## 🏃 Quick Start (Research Grade)

### Step 1: Get API Keys
Get keys from at least 1 (ideally 3+) providers above

### Step 2: Start CodexMatrix
```bash
streamlit run app.py
```

### Step 3: DON'T Check "Use Mock Data"
Leave the checkbox ☐ **unchecked**

### Step 4: Enter Your Problems
Add coding problems you want to benchmark

### Step 5: Select Models
Choose 3+ models (e.g., GPT-4o, Claude, Gemini)

### Step 6: Enter API Keys
Paste your REAL API keys from Step 1

### Step 7: Start Benchmark
Click "🚀 Start Benchmark"

**Result**: Authentic LLM peer-review scores for your research

---

## ✅ Verification Checklist

Before using results in a research paper, verify:

- [ ] ✅ **Real API Keys**: Using actual keys from official providers
- [ ] ✅ **Mock Mode OFF**: Checkbox is NOT checked
- [ ] ✅ **Valid Keys**: Keys are 40+ characters long
- [ ] ✅ **Sufficient Credits**: Providers have active credits
- [ ] ✅ **Network Connection**: Internet is stable
- [ ] ✅ **Clear Error Messages**: No API error messages appeared

---

## 📊 Reproducibility Tips

### For Academic Research:
1. **Document the setup**:
   - Which models? (GPT-4o, Claude 3.5 Sonnet, etc.)
   - Which rubric? (Default 5 criteria provided)
   - How many runs? (Multiple runs for statistical validity)

2. **Note the date**:
   - Model versions change regularly
   - Document the benchmark date

3. **Save the JSON export**:
   - Export results after each benchmark
   - Include in supplementary materials
   - Allows others to verify results

4. **Run multiple times**:
   - Temperature is set to 0.3 (deterministic but not random)
   - Run 3-5 times to account for variation
   - Report mean and std dev

---

## 🎯 Research Applications

### Benchmark Comparisons
```
Question: "How does GPT-4o compare to Claude on code quality?"
Setup: 
  - 10 coding problems (various difficulty levels)
  - 3 models (GPT-4o, Claude, Gemini)
  - Multiple languages
Result: Peer-reviewed comparison scores
```

### Model Evolution Tracking
```
Question: "Has GPT model quality improved over time?"
Setup:
  - Same 10 problems used quarterly
  - Compare results month-over-month
Result: Trend analysis of model improvements
```

### Rubric Validation
```
Question: "Is this code quality rubric effective?"
Setup:
  - Have models grade same code
  - Analyze score agreement/variance
Result: Rubric reliability analysis
```

---

## 💰 Cost Estimation

| Models | Problems | Languages | Approx. Cost |
|--------|----------|-----------|------------|
| 2 | 1 | 1 | $0.01 |
| 3 | 2 | 2 | $0.10 |
| 4 | 3 | 3 | $0.30 |
| 5 | 5 | 5 | $1.50 |

*Estimates based on March 2026 API pricing*

---

## ⚠️ Common Mistakes

### ❌ Using Expired Keys
**Issue**: Keys expire or lose credits
**Solution**: Check provider dashboard for active status

### ❌ Mixing Mock and Real Data
**Issue**: Can't tell if scores are real or simulated
**Solution**: Keep mock mode OFF for research; use only for testing UI

### ❌ Insufficient Problems
**Issue**: Small sample size not statistically significant
**Solution**: Use 5+ problems for valid academic benchmarks

### ❌ Single Run
**Issue**: LLM responses vary slightly each run
**Solution**: Run 3-5 times, report statistics

### ❌ Not Documenting Setup
**Issue**: Others can't reproduce your results
**Solution**: Document models, rubric, date, API versions

---

## 📝 Citation Format

If using CodexMatrix for published research:

```bibtex
@software{codexmatrix2026,
  title={CodexMatrix: AI Code Benchmarking Engine},
  author={LingoDuel Team},
  year={2026},
  howpublished={\url{https://github.com/yourusername/LingoDuel}},
  note={Session-Only Peer-Review Architecture}
}
```

---

## 🔬 Academic Validation

### To publish your results:

1. **Describe the methodology**
   - Which models evaluated
   - Which rubric criteria used
   - How many problems tested
   - How many runs performed

2. **Show the code**
   - Include benchmark problems in appendix
   - Document any modifications to rubric
   - Explain any filtering/preprocessing

3. **Report statistics**
   - Mean scores ± standard deviation
   - Inter-rater reliability (if multiple judges)
   - Confidence intervals

4. **Make findings reproducible**
   - Export and share JSON results
   - Document exact API versions used
   - Note any known API changes

---

## 🚨 Important Legal Notes

### API Usage Terms
- ✅ Verify you comply with each API provider's terms
- ✅ OpenAI: https://openai.com/api/policies/
- ✅ Anthropic: https://www.anthropic.com/legal
- ✅ Google: https://ai.google.dev/terms

### Academic Use
- ✅ Most providers allow academic research
- ✅ Be transparent about using paid APIs
- ✅ Don't claim original LLM development
- ✅ Cite the models/papers appropriately

### Data Sharing
- ❌ Don't share raw API responses publicly (may contain sensitive info)
- ✅ Share aggregated results and statistics
- ✅ Share problem statements (if original or permissible)
- ✅ Document your methodology

---

## 💡 Pro Tips

### Efficient Benchmarking
1. Start with 1-2 models (cheaper, faster)
2. Confirm setup works well
3. Expand to more models
4. Run multiple passes for statistics

### Cost Optimization
1. Use fewer, varied problems (quality > quantity)
2. Use faster/cheaper models as judges when appropriate
3. Cache results temporarily to avoid re-running
4. Test with mock mode first

### Statistical Validity
1. 3-5 runs minimum for published results
2. Use problems of varying difficulty
3. Include edge-case problems
4. Test across multiple languages

---

## 📞 Support for Researchers

If you encounter issues:

1. **Check API key validity**
   - Log into provider dashboard
   - Verify active credits/quota

2. **Check network connection**
   - Ensure internet is stable
   - Check firewall/VPN settings

3. **Try with mock mode first**
   - Verify app functionality
   - Then re-test with real keys

4. **Document the error**
   - Screenshot exact error message
   - Note which model failed
   - Include problem details

---

## 🎓 Example Research Setup

### Setup for Publication
```
Title: "Comparative Analysis of LLM Code Quality"

Methodology:
- 5 diverse coding problems (easy, medium, hard)
- 3 models: GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro
- 3 programming languages: Python, JavaScript, Java
- 3 independent runs per configuration
- 5-point rubric on: correctness, efficiency, readability, 
  edge-case handling, security

Cost: ~$1.50 total
Results: 15 peer reviews × 5 problems × 3 languages = 225 data points
Statistical confidence: High (multiple runs)
```

---

## ✅ You're Ready for Research!

With real API keys and this setup, CodexMatrix is suitable for:
- ✅ Academic papers
- ✅ Peer-reviewed journals
- ✅ Conference submissions
- ✅ Technical benchmarks
- ✅ Model comparisons

---

**Last Updated**: March 18, 2026  
**Status**: Ready for Research Use
