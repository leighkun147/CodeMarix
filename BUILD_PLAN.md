# 🏗️ CodexMatrix Development Plan

## Project Overview
**CodexMatrix** is a decentralized, autonomous AI benchmarking engine that evaluates Codex LLMs using a peer-review matrix ($M^2$) system. This document outlines the complete development roadmap.

---

## 📋 Current Status

### What We Have ✅ (MVP: Session-Only Architecture)
- ✅ Project repository on GitHub (public)
- ✅ Production-ready `app.py` with Streamlit Session State workflow
- ✅ CONTRIBUTING.md guide for team collaboration
- ✅ Enhanced core module structure:
  - `src/requester.py` - Parallel API calls with mock fallback
  - `src/judge_matrix.py` - Actual LLM-based peer-review matrix
  - `src/core/stats_engine.py` - Real-time matrix calculator & heatmaps
  - `src/utils/data_sanitizer.py` - API response cleanup & validation
- ✅ Session-only architecture (no database needed)
- ✅ Privacy-first design (API keys in RAM only)

### What We Need ❌ (Future Phases)
- ❌ Database schema for global leaderboards (Milestone 4)
- ❌ User authentication & profiles
- ❌ Persistent storage for historical benchmarks
- ❌ Comprehensive testing suite
- ❌ Advanced performance monitoring
- ❌ Deployment pipeline (Docker, CI/CD)

---

## 🎯 Phase 1: MVP (Session-Only Architecture) ✅ COMPLETE

### Architecture: The "Temporary Vault" Pattern

```
User Input
    ↓
app.py (Session State Holder)
    ├→ Step A: requester.py (Parallel API Calls)
    ├→ Step B: judge_matrix.py (Peer Review)
    ├→ Step C: stats_engine.py (Real-Time Analysis)
    └→ Output: Beautiful Streamlit Dashboard
    ↓
Browser Close → All cleanup (Zero persistence)
```

### Deliverables ✅

**1.1 - File Reorganization**
- ✅ Created `/src/core/` for analytics modules
- ✅ Created `/src/utils/` for helper functions
- ✅ Moved `stats_engine.py` → `src/core/stats_engine.py`

**1.2 - Core Modules Enhanced**

#### `src/utils/data_sanitizer.py`
- Sanitizes raw API responses → clean Python dicts
- Validates code generation quality
- Sanitizes peer review scores (1-5 range)
- Formats code for display (markdown syntax highlighting)

#### `src/core/stats_engine.py`
- Builds `M x M` peer-review matrix
- Generates real-time heatmaps showing reviewer→reviewee scores
- Calculates overall winner based on average scores
- Compares models by rubric criterion
- Exports session summary stats

#### `src/requester.py` (Enhanced)
- Real API integrations:
  - `call_openai_api()` - GPT-4o, GPT-4 Turbo
  - `call_anthropic_api()` - Claude models
  - `call_google_api()` - Gemini models
- Parallel execution using `ThreadPoolExecutor` (5 workers)
- Mock fallback for testing (no API calls needed)
- Automatic response sanitization

#### `src/judge_matrix.py` (Enhanced)
- Actual LLM-based code grading via API
- Comprehensive rubric with 10 quantitative parameters:
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
- Numeric key JSON format (1-10) for reliable LLM parsing
- Robust JSON extraction with key normalization
- Parallel review execution (5 concurrent reviews)
- Error handling with neutral default scores

**1.3 - Production App (`app.py`)**

Features:
- 🚀 Full workflow orchestration with Streamlit
- 🔐 Session State as "Temporary Vault"
- 📊 Real-time progress tracking (4-step process)
- 📈 Interactive visualizations:
  - Leaderboard table (sortable)
  - Heatmap showing reviewer→reviewee scores
  - Bar charts for each rubric criterion
  - Top models comparison
- 💾 JSON export for session data
- 🎭 Mock mode for testing without API costs
- ✅ Input validation & error handling

### Single-Session Workflow

**Input Collection** (Sidebar)
- Up to 5 coding problems
- 2+ models to benchmark
- 1+ programming languages
- API keys for each model (entered, not saved)

**Processing** (Main)
- Step A: Parallel code generation
- Step B: Peer review matrix (each model reviews others)
- Step C: Real-time statistics & winner determination
- Step D: Interactive result visualization

**Output** (Dashboard)
- Session winner announcement
- Overall leaderboard
- Per-criterion performance comparison
- Peer review heatmap
- Exportable JSON report

**Cleanup**
- Browser close → RAM cleared
- No persistent storage
- Zero privacy concerns

### Rubric Details

```python
RUBRIC = [
    "Correctness & Accuracy",       # Correct output?
    "Efficiency (Time)",             # Time complexity optimal?
    "Efficiency (Space)",            # Memory usage minimal?
    "Readability & Clear Code",      # Easy to understand?
    "Documentation & Comments",      # Well-documented?
    "Edge-Case Handling",            # Boundary conditions?
    "Error Handling & Robustness",   # Error management?
    "Security & Safe Practices",     # Safe code?
    "Code Simplicity",               # Elegant without complexity?
    "Best Practices & Standards"     # Language conventions?
]
```

Each score: **1-5** (1=Poor, 5=Excellent)

---

## 🎯 Phase 2: Testing & Documentation

### 2.1 Comprehensive Testing
**Goal:** Ensure system reliability before scaling

**Tasks:**
- [ ] Unit tests for all modules
- [ ] Integration tests (end-to-end workflows)
- [ ] API tests (mock + real LLM providers)
- [ ] Performance/load testing
- [ ] Security tests (API key handling)

**Test Coverage Target:** >80%

**Deliverables:**
- `tests/` folder with pytest suite
- Test documentation
- Performance benchmarks

---

## 💾 Phase 3: Database Integration (Global Leaderboards)

### 3.1 Persistent Storage Setup
**Goal:** Enable cross-session result storage

**Tasks:**
- [ ] Design PostgreSQL schema:
  - `sessions` table (benchmark runs)
  - `problems` table (coding challenges)
  - `submissions` table (generated code)
  - `reviews` table (peer ratings)
  - `leaderboards` table (aggregated scores)
- [ ] Implement database connector module
- [ ] Create migration scripts
- [ ] Set up connection pooling

**Recommended Stack:**
- PostgreSQL (reliability + JSONB support)
- SQLAlchemy (ORM)
- Alembic (migrations)

**Deliverables:**
- Database schema documentation
- Migration scripts
- Database models

### 3.2 Global Leaderboard Feature
**Goal:** Track model performance across all sessions

**Tasks:**
- [ ] Aggregate scores across sessions
- [ ] Calculate global rankings & trends
- [ ] Implement historical comparison
- [ ] Add leaderboard visualization page
- [ ] Export historical data

---

## 🔐 Phase 4: Authentication & Multi-User Support

### 4.1 User Management
**Goal:** Enable team collaboration and benchmarking

**Tasks:**
- [ ] Implement user authentication (OAuth2/JWT)
- [ ] User profiles & history
- [ ] Shared benchmarks
- [ ] Permissions & access control
- [ ] Audit logs

**Recommended:**
- Firebase Auth (simple)
- Or Auth0 + PostgreSQL (advanced)

---

## 🎨 Phase 5: Advanced Features

### 5.1 UI/UX Enhancements
**Goal:** Professional, scalable interface

**Tasks:**
- [ ] Multi-page Streamlit app:
  - Dashboard (summary)
  - New Benchmark (input)
  - Results (visualization)
  - Leaderboards (global)
  - History (past sessions)
  - Settings (preferences)
- [ ] Real-time progress tracking
- [ ] Result filtering & sorting
- [ ] Advanced visualizations (3D heatmaps)

### 5.2 API Integration Expansion
**Goal:** Support more LLM providers

**Tasks:**
- [ ] Add Hugging Face models support
- [ ] Add Open Source LLM support (via Ollama)
- [ ] Implement rate limiting & quotas
- [ ] Add provider-specific optimizations

---

## 📈 Phase 6: Scaling & Optimization

### 6.1 Performance Improvements
**Goal:** Handle large-scale benchmarks (10+ models, 100+ problems)

**Tasks:**
- [ ] Implement result caching (Redis)
- [ ] Optimize database queries
- [ ] Background task processing (Celery)
- [ ] API call batching & scheduling
- [ ] Cost optimization (cache API responses)

### 6.2 Deployment Infrastructure
**Goal:** Production-ready deployment

**Tasks:**
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Cloud deployment (AWS/GCP/Azure)
- [ ] Monitoring & alerting (DataDog/New Relic)
- [ ] Backup & disaster recovery

---

## 🎯 Phase 7: Community & Ecosystem

### 7.1 Open Source Contributions
- [ ] Community-contributed benchmarks
- [ ] Custom rubrics from users
- [ ] Benchmark result submissions
- [ ] Model provider partnerships
- [ ] Research paper publication

---

### 8.2 Performance Optimization
- [ ] Cache frequent queries
- [ ] Optimize LLM API calls
- [ ] Reduce response times
- [ ] Implement CDN for static assets

### 8.3 Community Features
- [ ] Public leaderboard
- [ ] User contributions
- [ ] Problem library
- [ ] Discussion forum

---

## 📈 Development Timeline

| Phase | Duration | Start | End | Status |
|-------|----------|-------|-----|--------|
| Phase 1: Core Foundation | 2 weeks | Mar 18 | Apr 1 | 🔄 IN PROGRESS |
| Phase 2: Database Setup | 1 week | Apr 1 | Apr 8 | ⏳ PENDING |
| Phase 3: Security | 1 week | Apr 8 | Apr 15 | ⏳ PENDING |
| Phase 4: UI Improvements | 1 week | Apr 15 | Apr 22 | ⏳ PENDING |
| Phase 5: Algorithm Optimization | 1 week | Apr 22 | Apr 29 | ⏳ PENDING |
| Phase 6: Testing | 1 week | Apr 29 | May 6 | ⏳ PENDING |
| Phase 7: Documentation & Deploy | 1 week | May 6 | May 13 | ⏳ PENDING |
| Phase 8: Post-Launch | Ongoing | May 13 | ∞ | ⏳ PENDING |

**Total Estimated Timeline:** 8-10 weeks

---

## 🛠️ Technology Stack

### Backend
- **Language:** Python 3.14+
- **Framework:** Streamlit (UI), FastAPI (optional API)
- **Database:** PostgreSQL or Firebase
- **Key Management:** Environment variables / AWS Secrets Manager

### LLM Providers
- OpenAI (GPT-4o)
- Anthropic (Claude 3.5)
- Google (Gemini 1.5 Pro)
- DeepSeek, Codestral, etc.

### DevOps
- **Hosting:** Streamlit Cloud or AWS/Azure
- **VCS:** GitHub
- **CI/CD:** GitHub Actions
- **Monitoring:** Sentry or DataDog

---

## 📋 Development Checklist

### Pre-Development
- [ ] All team members have GitHub access
- [ ] Understand CONTRIBUTING.md guide
- [ ] Set up local development environment
- [ ] Review README.md and project vision

### Per Phase
- [ ] Create feature branch from `main`
- [ ] Make commits with clear messages
- [ ] Create Pull Request with description
- [ ] Code review by team member
- [ ] Merge to `main` after approval
- [ ] Deploy/test changes

### Code Quality Standards
- [ ] Follows PEP 8 style guide
- [ ] Functions have docstrings
- [ ] Tests written for new features
- [ ] No hardcoded values/secrets
- [ ] Meaningful variable names
- [ ] Code commented where necessary

---

## 🎓 Learning Resources

**For Streamlit:**
- [Streamlit Docs](https://docs.streamlit.io)
- [Streamlit Gallery](https://streamlit.io/gallery)

**For Git/GitHub Workflow:**
- [CONTRIBUTING.md](./CONTRIBUTING.md) (in this repo)

**For API Integration:**
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Anthropic Claude Docs](https://docs.anthropic.com)

**For Database:**
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Firebase Docs](https://firebase.google.com/docs)

---

## 🤝 Team Responsibilities

### Leykun (Project Lead)
- [ ] Architecture decisions
- [ ] Code review & merging
- [ ] GitHub repository management
- [ ] Phase planning & tracking

### Friend (Developer)
- [ ] Implementation of assigned features
- [ ] Testing assigned modules
- [ ] Code quality improvements
- [ ] Documentation writing

### Both
- [ ] Daily standups (optional but recommended)
- [ ] Code reviews of each other's PRs
- [ ] Testing & validation
- [ ] Communication on blockers

---

## ⚠️ Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| LLM API rate limits | HIGH | MEDIUM | Implement caching, request queuing |
| API key exposure | CRITICAL | LOW | Use env vars, never commit secrets |
| Database failures | HIGH | LOW | Automated backups, redundancy |
| Poor code performance | MEDIUM | MEDIUM | Benchmark early, optimize incrementally |
| Team miscommunication | MEDIUM | MEDIUM | Regular standups, clear commits |

---

## 🎯 Success Criteria

✅ **Phase 1 Complete:**
- All modules documented and tested
- Core functionality verified locally

✅ **Phase 4 Complete:**
- Streamlit app is user-friendly
- All features accessible from UI

✅ **Phase 7 Complete:**
- App deployed and accessible online
- Complete documentation
- Others can set it up locally

✅ **Overall Success:**
- >1000 benchmark runs completed
- <5% error rate
- <3s response time for benchmarks
- >90% API uptime

---

## 📞 Questions? Issues?

If you get stuck:
1. Check [CONTRIBUTING.md](./CONTRIBUTING.md) for workflow
2. Create a GitHub issue with detailed description
3. Discuss with your team member
4. Check relevant documentation/API docs

---

## Version History

- **v1.0** (Mar 18, 2026) - Initial development plan created

---

**Last Updated:** March 18, 2026  
**Next Review:** March 25, 2026

