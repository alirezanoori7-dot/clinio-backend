[from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from bson import ObjectId
import httpx

# Environment variables
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', 'sk-emergent-eDeEdF8Cb2070E3Dc5')
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'clinio_production')

# MongoDB connection
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Create the main app
app = FastAPI(title="Clinio API", description="AI-powered clinical decision support")

# Create API router
api_router = APIRouter(prefix="/api")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ClinicalAnalysisRequest(BaseModel):
    symptoms: str
    patient_context: Optional[str] = ""

class DifferentialDiagnosis(BaseModel):
    condition: str
    likelihood: str
    reasoning: str

class ClinicalAnalysisResponse(BaseModel):
    id: str
    symptoms: str
    patient_context: str
    differential_diagnoses: Dict[str, List[DifferentialDiagnosis]]
    summary: str
    timestamp: datetime
    is_favorite: bool = False

# Helper function
def convert_objectid(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

# AI Analysis function (simplified for now)
async def analyze_with_ai(symptoms: str, patient_context: str = "") -> Dict[str, Any]:
    # Simplified response for testing - you can enhance this later
    return {
        "summary": f"Clinical analysis completed for: {symptoms[:50]}...",
        "differential_diagnoses": {
            "common": [
                {
                    "condition": "Common condition based on symptoms",
                    "likelihood": "Medium",
                    "reasoning": "Clinical reasoning based on presented symptoms"
                }
            ],
            "life_threatening": [
                {
                    "condition": "Serious condition to rule out",
                    "likelihood": "Low",
                    "reasoning": "Important to exclude based on symptoms"
                }
            ],
            "rare": [
                {
                    "condition": "Rare condition",
                    "likelihood": "Low",
                    "reasoning": "Less likely but worth considering"
                }
            ]
        }
    }

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Clinio API - Clinical Decision Support", "version": "1.0.0"}

@api_router.post("/analyze")
async def analyze_symptoms(request: ClinicalAnalysisRequest):
    """Analyze clinical symptoms and return structured differential diagnosis"""
    
    # Get AI analysis
    ai_result = await analyze_with_ai(request.symptoms, request.patient_context)
    
    # Create analysis object
    analysis_id = str(uuid.uuid4())
    analysis_data = {
        "id": analysis_id,
        "symptoms": request.symptoms,
        "patient_context": request.patient_context,
        "differential_diagnoses": ai_result.get("differential_diagnoses", {}),
        "summary": ai_result.get("summary", "Analysis completed"),
        "timestamp": datetime.utcnow(),
        "is_favorite": False
    }
    
    # Save to database
    await db.clinical_analyses.insert_one(analysis_data.copy())
    
    return analysis_data

@api_router.get("/history")
async def get_analysis_history():
    """Get all clinical analysis history"""
    analyses = await db.clinical_analyses.find().sort("timestamp", -1).to_list(100)
    
    for analysis in analyses:
        convert_objectid(analysis)
    
    return analyses

@api_router.get("/stats")
async def get_stats():
    """Get app statistics"""
    total_analyses = await db.clinical_analyses.count_documents({})
    
    return {
        "total_analyses": total_analyses,
        "clinical_sections": 250
    }

# Include the router in the main app
app.include_router(api_router)

# Root endpoint
@app.get("/")
async def main_root():
    return {"message": "Clinio Backend is running", "api_docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
