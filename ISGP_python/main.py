import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from routers.home import router as login_router
from routers.experiment_data import router as experiment_data_router
from routers.genetic_algorithim import router as genetic_algorithim_router
from routers.algorithim_parameters import router as algorithim_parameters_router
from routers.load_project import router as load_project_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log the incoming request
        logger.info(f"Request: {request.method} {request.url}")
        
        # Process the request
        response = await call_next(request)
        
        # Log the response status
        logger.info(f"Response status: {response.status_code}")
        
        return response
    

app = FastAPI()

#build_dir = "C:/Users/shema/CodingProjects/ISGP/ISGP_UI/ispg-ui/build"

# Determine base directory
if getattr(sys, 'frozen', False):
    # Running as a PyInstaller executable
    base_dir = sys._MEIPASS
else:
    # Running normally (not bundled with PyInstaller)
    base_dir = "C:/Users/shema/CodingProjects/ISGP/ISGP_UI/ispg-ui"

# Path to the React build directory
build_dir = os.path.join(base_dir, "build")

# Serve static files from the /static path
app.mount("/static", StaticFiles(directory=os.path.join(build_dir, "static")), name="static")


# Serve the index.html file at the root path
@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(build_dir, "index.html"))


app.add_middleware(LoggingMiddleware)


app.include_router(login_router)
app.include_router(experiment_data_router)
app.include_router(algorithim_parameters_router)
app.include_router(genetic_algorithim_router)
app.include_router(load_project_router)

origins = [
    "http://localhost:3000",  # If your React app runs on this port
    "http://127.0.0.1:3000",  # Another common localhost address
    "http://localhost:8000",  # If your React app runs on this port
    "http://127.0.0.1:8000",
    "http://localhost:8000/"
    
    # Add any other origins that need access
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


