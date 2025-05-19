from fastapi import APIRouter, HTTPException
from app.routers.recommendation import user_recommendations
from app.services.openai import call_openai_with_function
from app.services.openai import project_schema

router = APIRouter()

@router.post("/dataframe/generation")
async def generate_structured_data_from_latest_recommendation(user_id: str):
    if user_id not in user_recommendations:
        raise HTTPException(status_code=404, detail=f"No recommendation found for user_id: {user_id}")

    recommendation = user_recommendations[user_id]

    try:
        structured_result = await call_openai_with_function(
            content=recommendation,
            function_name="parse_project_plan",
            schema=project_schema,
            system_prompt="You are a project planner. Extract structured project details in English JSON format."
        )
        return structured_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing structured data: {str(e)}")


@router.post("/dataframe/download")
async def download_dataframe():
    return {"message": "DataFrame downloaded"}
