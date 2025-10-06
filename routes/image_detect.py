# routes/simple_routes.py
from fastapi import APIRouter, File, UploadFile, Depends,HTTPException
from typing import List, Optional
from pydantic import BaseModel, Extra
from supabase import Client
from core.supabase import get_supabase
from services.image_service import ImageService
from dependencies.auth import authenticate_and_get_user_details
from ai.image_related_ai import ImageAI


class GenericDatum(BaseModel):
    id: str
    user_id: str
    class Config:
        extra = Extra.allow


class SupabaseGenericResponse(BaseModel):
    data: List[GenericDatum]
    count: Optional[int] = None


class ImageResponse(BaseModel):
    plant_name: str
    disease: str
    severity: str
    time: str
    disease_probability: str
    suggestions: List[str]


router = APIRouter(prefix="/image", tags=["Image Detect"])

 # supabase: Client = Depends(get_supabase),user=Depends(authenticate_and_get_user_details)
# response_model=ImageResponse
@router.post("/detect")
async def create_upload_file(file: UploadFile = File(...)):
    # print(user,file)
    # service = ImageService(supabase)
    ai = ImageAI()
    isPlantImage = ai.isPlantImage(await file.read())
    if isPlantImage in ["False",False,'false']:
        return HTTPException(status_code=404,detail="Please insert Image of Plant not of anything")
    # Example mocked recognition
    recognized = {
        "plant_name": "Rice",
        "disease": "Rice Disease",
        "severity": "Medium",
        "time": "2hrs",
        "disease_probability": "85%",
        "suggestions": [
            "Use a good Pesticide",
            "Always take Crop Insurance",
            "You are good to go"
        ]
    }
    try:
        data = {
            # "user_id": user["user_id"],
            "response_result": recognized,
        }
        # service.save_res_to_database(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return recognized


@router.get("/image-history", response_model=SupabaseGenericResponse,)
async def get_history(supabase: Client = Depends(get_supabase),user=Depends(authenticate_and_get_user_details)):
    service = ImageService(supabase)
    return service.get_top_3_responses(user["user_id"])
