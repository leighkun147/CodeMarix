# 🏗️ CodexMatrix Architecture

## System Overview

CodexMatrix is an AI benchmarking engine that uses a peer-review matrix ($M^2$) to evaluate code-generating AI models. It runs rich, stateful sessions in RAM while also writing aggregate (and optionally detailed) results to Firebase/Firestore for a global leaderboard.

### Core Principle
> **"Temporary Vault for Secrets" Pattern**: API keys and other sensitive secrets live only in Streamlit Session State (RAM) and are cleared when the browser closes, while benchmark outcomes are persisted in Firestore for global analytics.

---

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT UI (app.py)                     │
│                   Session State Manager                      │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Sidebar: Input Collection                              │  │
│  │ ├─ Problems (1-5 coding challenges)                     │  │
│  │ ├─ Models (2+)                                         │  │
│  │ ├─ Languages (1+)                                      │  │
│  │ └─ API Keys (stored in RAM)                            │  │
│  └────────────────────────────────────────────────────────┘  │
│                          │                                    │
│                          ↓                                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ [STEP A] Code Generation (requester.py)                │  │
│  │ ├─ Parallel API calls (ThreadPoolExecutor)             │  │
│  │ ├─ Supports: OpenAI, Anthropic, Google                │  │
│  │ └─ Results → RAM (sanitized)                           │  │
│  └────────────────────────────────────────────────────────┘  │
│                          │                                    │
│                          ↓                                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ [STEP B] Peer Review (judge_matrix.py)                 │  │
│  │ ├─ Each model reviews every other model                │  │
│  │ ├─ LLM-based grading (uses API judge)                 │  │
│  │ ├─ 5-point rubric for 5 criteria                      │  │
│  │ └─ Results → RAM                                       │  │
│  └────────────────────────────────────────────────────────┘  │
│                          │                                    │
│                          ↓                                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ [STEP C] Analysis (src/core/stats_engine.py)           │  │
│  │ ├─ Build M×M peer-review matrix                        │  │
│  │ ├─ Determine session winner                            │  │
│  │ ├─ Generate heatmaps & visualizations                 │  │
│  │ └─ Results → RAM                                       │  │
│  └────────────────────────────────────────────────────────┘  │
│                          │                                    │
│                          ↓                                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ [STEP D] Display & Export                              │  │
│  │ ├─ Interactive Plotly visualizations                  │  │
│  │ ├─ Sortable DataFrames                                │  │
│  │ ├─ Winner announcement                                │  │
│  │ ├─ Per-criterion performance                          │  │
│  │ └─ JSON export for download                           │  │
│  └────────────────────────────────────────────────────────┘  │
│                          │                                    │
└──────────────────────────┼────────────────────────────────────┘
                           │
                           ↓
                    Browser Close
                   RAM is Cleared
                 (100% Privacy)
```

---

## Module Reference

### 1. **app.py** (State Holder & Orchestrator)
**Purpose**: Main Streamlit application that manages the entire workflow

**Responsibilities**:
- Initialize and maintain Streamlit Session State
- Collect user inputs (problems, models, languages, API keys)
- Call other modules in sequence
- Render UI and visualizations
- Handle errors and validation

**Key Functions**:
- `validate_session_inputs()` - Validates all inputs before processing
- Integration with `requester.py`, `judge_matrix.py`, and `stats_engine.py`

**Session State Keys**:
```python
st.session_state = {
    "api_keys": {},              # Model → API Key mapping
    "models": [],                # Selected models
    "languages": [],             # Selected languages
    "problems": [],              # Coding problems
    "generation_results": {},    # Code generation output
    "review_results": {},        # Peer review scores
    "stats_complete": False,     # Analysis flag
    "session_start": datetime    # Session timestamp
}
```

---

### 2. **src/requester.py** (Code Generator)
**Purpose**: Call LLM APIs to generate code solutions

**Architecture**:
```
Input: {problem, language, model, api_key}
           ↓
    [ThreadPoolExecutor] ← Parallel execution (5 workers)
           ↓
    [Get appropriate API caller]
           ↓
    [Call OpenAI/Anthropic/Google API]
           ↓
    [Sanitize response]
           ↓
Output: Clean code string
```

**Key Functions**:
- `generate_code_parallel()` - Main entry point, calls all models in parallel
- `call_openai_api()` - GPT-4o, GPT-4 Turbo
- `call_anthropic_api()` - Claude 3.5 Sonnet, Claude 3
- `call_google_api()` - Gemini 1.5 Pro
- `get_api_caller()` - Router function

**Output Format**:
```python
{
    problem1: {
        language1: {
            "GPT-4o": {
                "code": "...",
                "model": "GPT-4o",
                "problem": problem1,
                "language": language1,
                "valid": True,
                "timestamp": "2026-03-18T10:30:00",
                "error": None
            },
            "Claude 3.5 Sonnet": {...}
        }
    }
}
```

---

### 3. **src/utils/data_sanitizer.py** (Data Cleaner)
**Purpose**: Clean and validate API responses before processing

**Key Functions**:
- `sanitize_code_generation()` - Converts raw API response → clean dict
- `sanitize_review_scores()` - Ensures scores are 1-5 integers
- `sanitize_session_data()` - Validates entire session state
- `format_code_for_display()` - Adds syntax highlighting for UI

**Usage Pattern**:
```python
from src.utils.data_sanitizer import sanitize_code_generation

raw = '{"code": "print(\'hello\')"}'
clean = sanitize_code_generation(raw, "GPT-4o", problem, language)
```

---

### 4. **src/judge_matrix.py** (Peer Reviewer)
**Purpose**: Grade code using LLM-based peer review

**Architecture**:
```
Input: {generated_code, problem, language, reviewer_model, api_key}
           ↓
    [Build grading prompt with rubric]
           ↓
    [ThreadPoolExecutor] ← Parallel grading (5 workers)
           ↓
    [Call reviewer API]
           ↓
    [Parse JSON scores]
           ↓
    [Validate scores (1-5 range)]
           ↓
Output: {rubric_criterion: score, ...}
```

**Rubric** (10 criteria):
1. **Correctness & Accuracy** - Does the solution produce correct output?
2. **Efficiency (Time)** - Optimal time complexity (O(n), O(log n), O(n²), etc.)?
3. **Efficiency (Space)** - Minimal memory usage without bloat?
4. **Readability & Clear Code** - Easy to understand at first glance?
5. **Documentation & Comments** - Well-commented and documented?
6. **Edge-Case Handling** - Handles all boundary conditions and edge cases?
7. **Error Handling & Robustness** - Graceful error management and input validation?
8. **Security & Safe Practices** - Avoids vulnerabilities and unsafe patterns?
9. **Code Simplicity** - Elegant solution without unnecessary complexity?
10. **Best Practices & Standards** - Follows language conventions and idioms?

**Key Functions**:
- `peer_review_matrix()` - Creates M×M review matrix (each model grades others)
- `grade_code_with_api()` - Single code grading
- `_grade_with_openai()` - OpenAI grader
- `_grade_with_anthropic()` - Anthropic grader

**Grading Logic**:
- Model A's code is graded by: Model A, Model B, Model C, ... (all reviewers)
- Each reviewer uses same rubric
- Scores are averaged to get final judgment on Model A

---

### 5. **src/core/stats_engine.py** (Real-Time Analyzer)
**Purpose**: Compute statistics and generate visualizations

**Key Concepts**:

#### M×M Matrix
```
        GPT-4o  Claude  Gemini
GPT-4o    -      3.5     4.2
Claude   3.8     -       3.9
Gemini   4.1     4.3      -

Rows = Reviewers (who graded)
Cols = Reviewees (whose code was graded)
Values = Average score given
```

**Key Functions**:

1. **`build_review_matrix(review_results)`**
   - Aggregates all scores into M×M matrix
   - Returns pandas DataFrame
   
2. **`get_overall_winner(leaderboard_df)`**
   - Determines the winner
   - Winner = model with highest average score across all criteria
   - Returns: (model_name, score)

3. **`build_heatmap_data(review_results, metric)`**
   - Builds M×M matrix for specific rubric criterion
   - Returns: (numpy_array, model_names_list)
   - Used for visualization

4. **`build_rubric_comparison(leaderboard_df, top_n)`**
   - Extracts top N models with their per-criterion scores
   - Used for comparison charts

5. **`compute_consus_scores(review_results)`**
   - Flattens all scores into summary dict
   - Format: {model: {criterion: score, ...}}

6. **`generate_summary_stats(session_data, review_results)`**
   - Generates session-level statistics
   - Returns: {total_problems, total_models, total_reviews, ...}

**Output Examples**:

```python
# Leaderboard
{
    "GPT-4o": {
        "Correctness & Accuracy": 4.8,
        "Efficiency (Time)": 4.2,
        "Efficiency (Space)": 4.1,
        "Readability & Clear Code": 4.5,
        "Documentation & Comments": 4.3,
        "Edge-Case Handling": 4.2,
        "Error Handling & Robustness": 4.1,
        "Security & Safe Practices": 4.4,
        "Code Simplicity": 4.3,
        "Best Practices & Standards": 4.2
    },
    "Claude 3.5 Sonnet": {...}
}

# Summary Stats
{
    "total_problems": 3,
    "total_models": 4,
    "total_languages": 2,
    "total_reviews": 96,  # M² * problems * languages
    "rubric_size": 5
}
```

---

## Data Flow

### 1. **Generation Phase**
```
User Input
  ├─ Problems: ["Sort array", "Reverse string"]
  ├─ Models: ["GPT-4o", "Claude"]
  ├─ Languages: ["Python", "JavaScript"]
  └─ API Keys: {GPT-4o: xxx, Claude: yyy}
       ↓
  requester.generate_code_parallel()
       ↓
  Generated Code (2 problems × 2 models × 2 languages = 8 samples)
       ├─ generated_code[problem][language][model]
       └─ Each entry is sanitized (code, model, problem, language, valid, error)
```

### 2. **Review Phase**
```
For each generated code:
  judge_matrix.peer_review_matrix()
       ↓
  Each model reviews all others (M² = 4 reviews per problem/language)
       ├─ GPT-4o reviews GPT-4o code
  ├─ GPT-4o reviews Claude code
       ├─ Claude reviews GPT-4o code
       └─ Claude reviews Claude code
       ↓
  Scores for each review (5 scores per review × rubric criteria)
```

### 3. **Analysis Phase**
```
All review results
       ↓
  stats_engine.build_review_matrix()
       ↓
  Aggregate scores by model
       ├─ GPT-4o average: 4.3/5
       └─ Claude average: 4.2/5
       ↓
  Winner: GPT-4o (4.3 > 4.2)
       ↓
  Generate visualizations
       ├─ Heatmap (M×M matrix)
       ├─ Bar charts (per criterion)
       ├─ Leaderboard table
       └─ Comparison charts
```

### 4. **Display Phase**
```
Interactive Streamlit Dashboard
  ├─ Winner announcement
  ├─ Leaderboard table
  ├─ Real-time heatmap (Plotly)
  ├─ Performance charts
  ├─ Top models comparison
  └─ Export button (JSON)
```

---

## Mathematica Formulas

### Total Operations
$$M^2\_Ops = (P \times L \times M) + (P \times L \times M^2)$$

Where:
- $P$ = Number of problems
- $L$ = Number of languages
- $M$ = Number of models

**Breakdown**:
- **Code Generation**: $P \times L \times M$ (generate code for each combo)
- **Code Reviews**: $P \times L \times M^2$ (each model reviews all others)

**Example**: 2 problems, 2 languages, 4 models
- Generation: 2 × 2 × 4 = 16 code samples
- Reviews: 2 × 2 × 4² = 64 reviews
- **Total**: 80 API calls

### Winner Determination
$$\text{Winner} = \arg\max_m \left(\frac{1}{5} \sum_{c=1}^{5} \text{Score}_{m,c}\right)$$

Where:
- $m$ = model index
- $c$ = rubric criterion
- $\text{Score}_{m,c}$ = average score for model $m$ on criterion $c$

---

## API Integration Points

### OpenAI (GPT-4o)
```python
POST https://api.openai.com/v1/chat/completions
{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.7,
    "max_tokens": 1000
}
```

### Anthropic (Claude)
```python
POST https://api.anthropic.com/v1/messages
{
    "model": "claude-3-5-sonnet",
    "max_tokens": 1000,
    "messages": [{"role": "user", "content": prompt}]
}
```

### Google (Gemini)
```python
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent
{
    "contents": [{"parts": [{"text": prompt}]}]
}
```

---

## Error Handling Strategy

### Code Generation Failures
- **No Code**: Mark as `valid=False`, skip from review
- **API Error**: Store error message, use neutral placeholder
- **Timeout**: Catch exception, log, continue with next task

### Grading Failures
- **Bad JSON**: Use regex to extract JSON, fallback to defaults
- **API Error**: Return neutral scores (3/5)
- **Timeout**: Skip review, use average of other reviews

### Validation Failures
- **Missing API Key**: Show error, block benchmark start
- **Invalid Input**: Show specific error message
- **Empty Problems**: Show error, suggest examples

---

## Security Architecture

### API Key Management
```
User Input (Sidebar)
        ↓
Streamlit Session State (RAM only)
        ↓
Pass to API call functions
        ↓
Browser close → Garbage collected
```

**Guarantees**:
- ✅ Keys never written to disk
- ✅ Keys never logged
- ✅ Keys never transmitted outside of API calls
- ✅ Keys automatically cleared on session end

### Data Privacy
- No user tracking
- No telemetry
- No persistent storage
- No cloud uploads (except API calls)

---

## Performance Considerations

### Parallel Execution
```python
ThreadPoolExecutor(max_workers=5)  # Limit concurrency
```

**Why 5 workers?**
- Balances parallelism with rate limiting
- Prevents overwhelming API providers
- Keeps memory usage reasonable

### Timeouts
```python
requests.post(..., timeout=30)  # 30 second timeout per call
```

**Prevents**:
- Hanging requests
- Wasted resources
- Poor user experience

### Caching (Future)
- Cache generated code to avoid regeneration
- Cache grading results (same code, same rubric)
- Would reduce API calls by 50-70% on reruns

---

## Scalability Road Map

### Current (MVP)
- Single session (browser instance)
- Up to 5 problems
- Up to 10 models
- RAM-based storage

### Phase 2
- Add Redis caching
- Implement background tasks (Celery)
- Support 50+ models

### Phase 3
- Add PostgreSQL database
- Global leaderboards
- Multi-user support
- Historical comparisons

### Phase 4+
- Distributed processing
- Kubernetes orchestration
- 1000+ models
- Real-time rankings

---

## Testing Strategy

### Unit Tests
- Test each module independently
- Mock API responses
- Verify data transformations

### Integration Tests
- Test full workflow end-to-end
- Use mock mode (no API costs)
- Verify data flows correctly

### Load Tests
- Test with max inputs (5 problems, 10 models, 5 languages)
- Measure execution time
- Monitor memory usage

---

## Future Enhancements

### Short Term
- [ ] WebSocket support for real-time updates
- [ ] Better error recovery
- [ ] Code caching
- [ ] Rate limiting per model

### Medium Term
- [ ] Database integration (Phase 3)
- [ ] User authentication
- [ ] Benchmark history
- [ ] Global leaderboards

### Long Term
- [ ] GraphQL API
- [ ] Mobile app
- [ ] Custom rubrics
- [ ] Community extensions

---

**Last Updated**: March 18, 2026
**Version**: 1.0 (MVP)
