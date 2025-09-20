from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Clinio API", description="AI-powered clinical decision support")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Clinio Backend is running", "status": "success"}

@app.get("/api/")
async def api_root():
    return {"message": "Clinio API - Clinical Decision Support", "version": "1.0.0"}

@app.get("/api/stats")
async def get_stats():
    return {
        "total_analyses": 0,
        "clinical_sections": 250,
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
