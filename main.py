from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# اضافه کردن CORS بعد از ساختن app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # برای تست ساده
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello from FastAPI on Render!"}
