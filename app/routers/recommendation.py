from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.openai import call_openai_api
from app.services.openai import SYSTEM_PROMPT_LIBRARY
from app.services.openai import chat_history_manager


router = APIRouter()

user_recommendations = {}

class RecommendationRequest(BaseModel):
    user_input: str
    user_id: str

@router.post("/recommend")
async def generate_recommendation(request: RecommendationRequest):
    try:
        system_prompt = SYSTEM_PROMPT_LIBRARY["recommend"]
        #call OpenAI API
        recommendation = await call_openai_api(
            user_id=request.user_id,
            user_input = request.user_input,
            system_prompt = system_prompt
        )
        #history
        chat_history_manager.add_message(request.user_id, "user", request.user_input)
        chat_history_manager.add_message(request.user_id, "assistant", recommendation)

        user_recommendations[request.user_id] = recommendation

        return {"user_id": request.user_id,
                "recommendation": recommendation}
    #error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendation: {str(e)}")
