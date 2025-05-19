from fastapi import FastAPI
from app.routers import recommendation, structured_data
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Include routers
app.include_router(recommendation.router, prefix="/recommendation", tags=["Recommendation"])
app.include_router(structured_data.router, prefix="/structured_data", tags=["Structured Data"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Mach-AI Gen-AI API"}
