import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface CodeGenerationRequest {
  problems: string[]
  languages: string[]
  models: string[]
  api_keys: Record<string, string>
  use_mock?: boolean
}

export interface PeerReviewRequest {
  generation_results: Record<string, any>
  api_keys: Record<string, string>
  use_mock?: boolean
}

export interface AnalysisRequest {
  review_results: Record<string, any>
  problems: string[]
  models: string[]
}

// Health check
export const healthCheck = async () => {
  try {
    const response = await api.get('/health')
    return response.data
  } catch (error) {
    console.error('Health check failed:', error)
    throw error
  }
}

// Get rubric
export const getRubric = async () => {
  try {
    const response = await api.get('/api/rubric')
    return response.data.rubric
  } catch (error) {
    console.error('Failed to fetch rubric:', error)
    throw error
  }
}

// Generate code
export const generateCode = async (request: CodeGenerationRequest) => {
  try {
    const response = await api.post('/api/generate-code', request)
    return response.data
  } catch (error) {
    console.error('Code generation failed:', error)
    throw error
  }
}

// Run peer review
export const runPeerReview = async (request: PeerReviewRequest) => {
  try {
    const response = await api.post('/api/peer-review', request)
    return response.data
  } catch (error) {
    console.error('Peer review failed:', error)
    throw error
  }
}

// Run analysis
export const runAnalysis = async (request: AnalysisRequest) => {
  try {
    const response = await api.post('/api/analyze', request)
    return response.data
  } catch (error) {
    console.error('Analysis failed:', error)
    throw error
  }
}

// Run complete workflow
export const runWorkflow = async (request: CodeGenerationRequest) => {
  try {
    const response = await api.post('/api/workflow', request)
    return response.data
  } catch (error) {
    console.error('Workflow failed:', error)
    throw error
  }
}

export default api
