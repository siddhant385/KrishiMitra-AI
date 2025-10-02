from dotenv import load_dotenv
from fastapi import FastAPI,APIRouter
from routes import simple_routes,chatbot,image_detect
from middlewares.cors import setup_cors_middleware

load_dotenv()
# main.py


app = FastAPI(title="Crop AI Backend")


#Middlewares are imported here
setup_cors_middleware(app)


# Include routes
api_router = APIRouter()


#Routes are created and groupted here
api_router.include_router(simple_routes.router)
api_router.include_router(chatbot.router)
api_router.include_router(image_detect.router)






app.include_router(api_router, prefix="/api/v1")
@app.get("/", tags=["Root"])
def read_root():
    """
    🏠 Welcome endpoint with comprehensive API information
    
    Returns:
    - Welcome message with app details
    - Available API endpoints
    - Quick start guide
    - System status
    """
    from datetime import datetime
    from zoneinfo import ZoneInfo
    
    current_time = datetime.now(ZoneInfo("Asia/Kolkata"))
    
    return {
    	"time": current_time
        }

# Run with: uvicorn main:app --reload
