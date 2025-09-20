from fastapi import FastAPI

# Create FastAPI app
app = FastAPI(title="Clinio API")

@app.get("/")
def read_root():
    return {"message": "Clinio Backend is running", "status": "success"}

@app.get("/api")
def api_root():
    return {"message": "Clinio API - Clinical Decision Support", "version": "1.0.0"}

@app.get("/api/")
def api_root_slash():
    return {"message": "Clinio API - Clinical Decision Support", "version": "1.0.0"}

@app.get("/api/stats")
def get_stats():
    return {
        "total_analyses": 0,
        "clinical_sections": 250,
        "status": "operational"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "clinio-backend"}
