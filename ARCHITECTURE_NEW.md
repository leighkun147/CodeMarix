# CodexMatrix - Modernized Architecture

## 📋 Project Structure

```
LingoDuel/
├── backend/           # FastAPI Python backend
│   ├── main.py       # REST API endpoints
│   └── requirements.txt
├── frontend/          # Next.js React frontend
│   ├── app/          # Next.js app directory
│   ├── lib/          # API client services
│   ├── components/   # React components (to be created)
│   ├── package.json
│   └── tailwind.config.js
├── src/              # Original Python modules (code generation, peer review, etc.)
└── README.md
```

## 🚀 Quick Start

### 1. Install Backend Dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start FastAPI Backend

```bash
cd backend
source venv/bin/activate
python main.py
```

The API will be available at: **http://localhost:8000**
API docs: **http://localhost:8000/docs**

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 4. Start Next.js Frontend

```bash
cd frontend
npm run dev
```

The frontend will be available at: **http://localhost:3000**

---

## 🏗️ Architecture

### Backend (FastAPI)
- **Location**: `/backend/main.py`
- **Port**: 8000
- **Technology**: FastAPI + Python

**Endpoints**:
- `GET /health` - Health check
- `GET /api/rubric` - Get evaluation rubric
- `POST /api/generate-code` - Generate code from problems
- `POST /api/peer-review` - Run peer review matrix
- `POST /api/analyze` - Analyze results
- `POST /api/workflow` - Run complete workflow (all-in-one)

### Frontend (Next.js + React)
- **Location**: `/frontend`
- **Port**: 3000
- **Technology**: Next.js 14, React 18, TypeScript, Tailwind CSS, daisyUI

**Features**:
- Modern animated forms with Framer Motion
- Beautiful dashboard with daisyUI components
- Real-time API communication
- Dark mode military theme
- Responsive design

---

## 🔧 Environment Variables

### Frontend (`.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend
No additional env vars needed for local development.

---

## 📦 What's Kept from Original

✅ **All Core Functionality**:
- Code generation (requester.py)
- Peer review matrix (judge_matrix.py)
- Stats engine & analysis (stats_engine.py)
- 10-criterion rubric
- All LLM integrations (OpenAI, Anthropic, Google, DeepSeek, Groq)
- Mock data support for testing

✅ **No Functionality Lost**:
- Same peer-review algorithm
- Same heatmap generation
- Same winner calculation
- Same API key handling

---

## 🎨 Frontend Components (To Be Created)

**Main Pages**:
- `/` - Landing page (done)
- `/benchmark` - Main UI for data input & workflow
- `/results` - Results dashboard with heatmaps
- `/guide` - Documentation

**Components to Build**:
- ProblemForm - Multi-input for coding problems
- ModelSelector - Checkbox/multi-select for models
- LanguageSelector - Programming language selection
- ApiKeyInput - Secure API key input fields
- ProgressTracker - Show generation/review/analysis progress
- HeatmapVisualization - Plotly heatmap display
- LeaderboardCard - Show winner & rankings

---

## 📡 API Communication Flow

```
Frontend (Next.js)
    ↓
  axios → HTTP requests
    ↓
Backend (FastAPI)
    ↓
Python modules (src/*.py)
    ↓
Returns JSON data
    ↓
Frontend parses & displays
```

---

## 🔐 Session Handling

- **Frontend**: Session state + localStorage for forms
- **Backend**: Stateless (each API call is independent)
- **API Keys**: Still safe - only in RAM during API calls, never persisted

---

## 🐳 Next Steps

1. ✅ Create backend FastAPI app
2. ✅ Create frontend Next.js project
3. 🔲 Build benchmark page with forms
4. 🔲 Build results dashboard
5. 🔲 Add loading/progress states
6. 🔲 Error handling & validation
7. 🔲 Deploy to production

---

## 💡 Development Tips

**Hot Reload**:
- Frontend: Uses Next.js hot reload automatically
- Backend: Use `--reload` flag with uvicorn

**Full Workflow Command**:
```bash
# Terminal 1 - Backend
cd backend && source venv/bin/activate && python main.py

# Terminal 2 - Frontend
cd frontend && npm run dev
```

**Testing API Endpoints**:
Visit `http://localhost:8000/docs` for interactive Swagger UI

**Building for Production**:

Frontend:
```bash
cd frontend
npm run build
npm start
```

Backend:
```bash
cd backend
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

---

## 📊 Performance

- **Frontend**: Optimized with Next.js bundle splitting, lazy loading
- **Backend**: FastAPI async/await for concurrent requests
- **Graphs**: Plotly heatmaps rendered client-side
- **CSS**: Tailwind CSS tree-shaking removes unused styles

---

## ✨ Military Theme Features

- ✅ Dark navy background (#0a0e1a)
- ✅ Neon green (#00ff41) & cyan (#00d9ff) accents
- ✅ Pulsing glow effects
- ✅ Smooth animations with Framer Motion
- ✅ Monospace fonts (JetBrains Mono)
- ✅ Terminal-like aesthetic

---

**Status**: 🟢 Architecture Ready | Ready for Component Development
