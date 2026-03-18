# ⚔️ CodexMatrix: The $M^2$ Autonomous AI Benchmarking Engine

**Author:** Leykun Hailemichael Hagos  
**Major:** Software Engineering, Samsun University  
**Academic Year:** 2025-2026 (First Year Research)  
**Hardware:** ASUS ExpertBook P5405CSA

---

## 🚀 1. Project Vision
**CodexMatrix** is a high-performance, decentralized evaluation framework designed to scientifically rank the world's leading "Codex" LLMs (models optimized for programming). By implementing a **"Bring Your Own Key" (BYOK)** architecture, CodexMatrix removes the financial and privacy barriers to large-scale AI benchmarking, allowing the community to generate an objective, real-time leaderboard.

---

## 🕹️ 2. The $M^2$ Autonomous Workflow
The core of CodexMatrix is the **Autonomous Peer-Review Matrix**. Unlike static benchmarks (like HumanEval), this system is dynamic and adversarial.

### 2.1 The Execution Matrix
The system scales exponentially based on the user's input:
$$Total\_Ops = (P \times L \times M) + (P \times L \times M^2)$$
* **$P$ (Problems):** Users can input up to **5 specific coding challenges** per session.
* **$L$ (Languages):** Support for 15+ languages (C, C++, Rust, Python, Go, etc.).
* **$M$ (Models):** A selection of at least 2 (up to 10) specialized Codex models.
* **$M^2$ (Judge Matrix):** Every AI model acts as a "Senior Reviewer" for the output of every participant, creating a cross-verified consensus score.

### 2.2 The "Peer-to-Peer" Logic
- **Step A (Generation):** Model A, B, and C generate code for Problem 1 in Python.
- **Step B (Review):** - Model A reviews B and C.
    - Model B reviews A and C.
    - Model C reviews A and B.
    - (Optional) Each model reviews its own code for consistency.

---

## 📊 3. The 5-Point Engineering Rubric
CodexMatrix does not just check if code "works." It evaluates the **Software Engineering Quality** using these 5 quantitative parameters:

1.  **Syntactic Correctness:** Logic flow, syntax validity, and compilability in the target environment.
2.  **Algorithmic Efficiency:** Analysis of Time and Space complexity ($O(n)$, $O(log n)$, etc.).
3.  **Readability & Documentation:** Evaluation of variable naming, modularity, and comment quality.
4.  **Edge-Case Handling:** Detection of potential failures under null inputs, overflows, or boundary conditions.
5.  **Security Vulnerabilities:** Identification of insecure memory management (in C/C++) or injection risks.

---

## 🛠️ 4. The Codex Competitors (Target List)
The platform is built to interface with the world's most powerful coding brains:
1.  **GPT-4o** (OpenAI)
2.  **Claude 3.5 Sonnet** (Anthropic)
3.  **Gemini 1.5 Pro** (Google)
4.  **DeepSeek-Coder-V2** (State-of-the-Art Open Source)
5.  **Codestral** (Mistral AI)
6.  **Llama 3 / CodeLlama** (Meta)
7.  **Qwen-Coder** (Alibaba)
8.  **StarCoder2** (Hugging Face)
9.  **Grok-1** (xAI)
10. **GitHub Copilot API** (Technical Integration)

---

## 🔒 5. Data Strategy & Privacy Protocol
To maintain a 100% privacy-first environment on the **ASUS ExpertBook**, CodexMatrix utilizes a **Decentralized Data Flow**:

- **Volatile Key Management:** All API keys are stored exclusively in **RAM** (Streamlit Session State). They never touch the hard drive or the database.
- **The Metadata Bridge:** Only "Cold Data" is sent to the central Leaderboard.
    - **UPLOADED:** Model Name, Language, Latency (ms), and the 5 Rubric Scores.
    - **NOT UPLOADED:** User Prompts, Generated Code, or API Credentials.

---

## 📂 6. Project Directory Structure
```text
CodexMatrix/
├── venv/                # Isolated Python Environment
├── app.py               # Streamlit Web Application (UI)
├── database/            # Metadata Storage (CSV/JSON)
└── src/
    ├── requester.py     # Milestone 1: Parallel Generation Logic
    ├── judge_matrix.py  # Milestone 2: M^2 Peer-Review Logic
    └── stats_engine.py  # Milestone 3: Consensus Math & Visuals# CodeMarix
