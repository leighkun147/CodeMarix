"""
FastAPI Backend for CodexMatrix
Exposes Python logic as REST API endpoints
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
import os

# Add parent directory to path to import existing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.requester import generate_code_parallel
from src.judge_matrix import peer_review_matrix, RUBRIC
from src.core.stats_engine import (
    build_review_matrix, 
    get_overall_winner, 
    build_heatmap_data,
    compute_consus_scores
)

# Initialize FastAPI app
app = FastAPI(
    title="CodexMatrix API",
    description="AI Model Benchmarking Engine",
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# PYDANTIC MODELS (Request/Response schemas)
# ============================================================================

class CodeGenerationRequest(BaseModel):
    problems: List[str]
    languages: List[str]
    models: List[str]
    api_keys: Dict[str, str]
    use_mock: bool = False

class CodeGenerationResponse(BaseModel):
    status: str
    generated_count: int
    results: Dict
    errors: Optional[List[str]] = None

class PeerReviewRequest(BaseModel):
    generation_results: Dict
    api_keys: Dict[str, str]
    use_mock: bool = False

class PeerReviewResponse(BaseModel):
    status: str
    review_matrix: Dict
    errors: Optional[List[str]] = None

class AnalysisRequest(BaseModel):
    review_results: Dict
    problems: List[str]
    models: List[str]

class AnalysisResponse(BaseModel):
    status: str
    heatmap_data: Dict
    winner: Dict
    consensus_scores: Dict
    metrics: Dict

class RubricResponse(BaseModel):
    rubric: List[str]
    count: int

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
def health_check():
    """Check if API is running"""
    return {
        "status": "healthy",
        "service": "CodexMatrix API",
        "version": "1.0.0"
    }

# ============================================================================
# RUBRIC ENDPOINT
# ============================================================================

@app.get("/api/rubric")
def get_rubric() -> RubricResponse:
    """Get evaluation rubric"""
    return RubricResponse(
        rubric=RUBRIC,
        count=len(RUBRIC)
    )

# ============================================================================
# CODE GENERATION ENDPOINT
# ============================================================================

@app.post("/api/generate-code")
async def generate_code(request: CodeGenerationRequest) -> CodeGenerationResponse:
    """Generate code from problems using multiple models"""
    try:
        if not request.problems or not request.models or not request.languages:
            raise HTTPException(
                status_code=400,
                detail="Problems, models, and languages are required"
            )
        
        # Call existing code generation logic
        results = generate_code_parallel(
            problems=request.problems,
            languages=request.languages,
            models=request.models,
            api_keys=request.api_keys,
            use_mock=request.use_mock
        )
        
        generated_count = sum(
            1 for problem in results.values()
            for language in problem.values()
            for model_data in language.values()
            if model_data.get("valid")
        )
        
        errors = []
        for problem in results.values():
            for language in problem.values():
                for model_data in language.values():
                    if model_data.get("error"):
                        errors.append(model_data.get("error"))
        
        return CodeGenerationResponse(
            status="success" if generated_count > 0 else "partial",
            generated_count=generated_count,
            results=results,
            errors=errors if errors else None
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# PEER REVIEW ENDPOINT
# ============================================================================

@app.post("/api/peer-review")
async def peer_review(request: PeerReviewRequest) -> PeerReviewResponse:
    """Run peer review matrix on generated code"""
    try:
        if not request.generation_results:
            raise HTTPException(
                status_code=400,
                detail="Generation results required"
            )
        
        # Call existing peer review logic
        review_results = peer_review_matrix(
            generation_results=request.generation_results,
            api_keys=request.api_keys,
            use_mock=request.use_mock
        )
        
        errors = []
        if isinstance(review_results, dict) and "errors" in review_results:
            errors = review_results.get("errors", [])
        
        return PeerReviewResponse(
            status="success" if not errors else "partial",
            review_matrix=review_results,
            errors=errors if errors else None
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ANALYSIS ENDPOINT
# ============================================================================

@app.post("/api/analyze")
async def analyze(request: AnalysisRequest) -> AnalysisResponse:
    """Analyze peer review results and generate insights"""
    try:
        if not request.review_results:
            raise HTTPException(
                status_code=400,
                detail="Review results required"
            )
        
        # Build analysis data
        review_matrix = build_review_matrix(request.review_results)
        heatmap_data = build_heatmap_data(review_matrix, request.problems, request.models)
        winner = get_overall_winner(review_matrix)
        consensus = compute_consus_scores(review_matrix)
        
        return AnalysisResponse(
            status="success",
            heatmap_data={
                "z": heatmap_data[0].tolist() if hasattr(heatmap_data[0], 'tolist') else heatmap_data[0],
                "problems": request.problems,
                "models": request.models
            },
            winner=winner,
            consensus_scores=consensus,
            metrics={
                "total_reviews": len(request.review_results),
                "rubric_items": len(RUBRIC)
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# WORKFLOW ENDPOINT (All-in-one)
# ============================================================================

class WorkflowRequest(BaseModel):
    problems: List[str]
    languages: List[str]
    models: List[str]
    api_keys: Dict[str, str]
    use_mock: bool = False

@app.post("/api/workflow")
async def run_workflow(request: WorkflowRequest):
    """Run complete workflow: generate → review → analyze"""
    try:
        # Step 1: Generate
        generation_results = generate_code_parallel(
            problems=request.problems,
            languages=request.languages,
            models=request.models,
            api_keys=request.api_keys,
            use_mock=request.use_mock
        )
        
        # Step 2: Peer Review
        review_results = peer_review_matrix(
            generation_results=generation_results,
            api_keys=request.api_keys,
            use_mock=request.use_mock
        )
        
        # Step 3: Analysis
        review_matrix = build_review_matrix(review_results)
        heatmap_data = build_heatmap_data(review_matrix, request.problems, request.models)
        winner = get_overall_winner(review_matrix)
        
        return {
            "status": "success",
            "generation": generation_results,
            "review": review_results,
            "analysis": {
                "heatmap": heatmap_data[0].tolist() if hasattr(heatmap_data[0], 'tolist') else heatmap_data[0],
                "winner": winner,
                "problems": request.problems,
                "models": request.models
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ERROR HANDLER
# ============================================================================

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "CodexMatrix API",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
