import json
from typing import List
from fastapi import HTTPException
import logging
import uuid
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
import httpx
from version import VERSION
from file_managment.file_manager import  get_config_path
from project_context import current_project_name
#from cache.db_connection import initialize_db_connection
from packaging import version
from modules.login_module.login_handler import create_new_project, get_project_names, load_project#, create_project

router = APIRouter()

@router.get("/checkVersion")
async def check_version():
    url = "https://raw.githubusercontent.com/shem221/version-check/refs/heads/main/version"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            latest_version = response.text.strip()
            
            # Compare the versions using version.parse() to handle version strings properly
            current_version_parsed = version.parse(VERSION)
            latest_version_parsed = version.parse(latest_version)

            if current_version_parsed > latest_version_parsed:
                message = f"Please be advised:\nThe version you are working with seems to be newer.\n" \
                          f"The latest version of ISGP is {latest_version}, while your version is {VERSION}."
            elif current_version_parsed < latest_version_parsed:
                message = f"Please be advised:\nThe version you are working with is not up to date.\n" \
                          f"The latest version of ISGP is {latest_version}, while your version is {VERSION}."
            else:
                message = f"Your version is up to date. You are using the latest version ({VERSION})."

            return {
                "updateAvailable": current_version_parsed != latest_version_parsed,
                "currentVersion": VERSION,
                "message": message
            }

    except httpx.RequestError as e:
        # Log the error for debugging purposes (optional)
        print(e)
        print(f"GitHub request failed: {str(e)}")
        raise HTTPException(status_code=502, detail="Failed to connect to GitHub to check the version.")




@router.post("/login")
def login(response: Response):
    
    #user_id = create_project()
    user_id = str(uuid.uuid4())

    content={"message": "Created Project", "user_id": user_id}
    response = JSONResponse(content=content)
    response.set_cookie(key="authToken", value=user_id, httponly=True, samesite="None", secure=True)

    return response


@router.post("/createProject")
def create_project(response: Response,project_name: str):
    # Sanitize project name to prevent invalid directory names
    current_project_name.set(project_name)
    invalid_chars = set('/\\:*?"<>|')
    if not project_name or any(char in project_name for char in invalid_chars):
        raise HTTPException(status_code=400, detail="Invalid project name")
    
    # Create new project (pseudo function)
    status = create_new_project(project_name)

    # Handle project creation status
    if status is False:
        raise HTTPException(status_code=400, detail="Project already exists")
    
    # Prepare response
    content = {"message": f"Project '{project_name}' created successfully", "projectName": project_name}
    response = JSONResponse(content=content)
    response.set_cookie(key="projectName", value=project_name, httponly=True, samesite="None", secure=True)

    return response


@router.get("/getProjects", response_model=List[str])
def getProjects()-> List[str]:
    
    project_names = get_project_names()

    return project_names


@router.post("/loadProject")
def loadProject(response: Response,project_name: str):
    current_project_name.set(project_name)
    project_exists = load_project(project_name)
    
    if project_exists is False:
        raise HTTPException(status_code=400, detail="Project doesn't exist")
    
    content={"message": "Loaded Project", "projectName": project_name}
    response = JSONResponse(content=content)
    response.set_cookie(key="projectName", value=project_name, httponly=True, samesite="None", secure=True)

    return response


    

# @router.get("/checkVersion")
# async def check_version():
#     url = "https://raw.githubusercontent.com/shem221/version-check/refs/heads/main/version"
    
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(url)
#             response.raise_for_status()
#             latest_version = response.text.strip()

#             config_path = get_config_path()
#             print(config_path)
#             # Load your local version (from JSON or other storage)
#             try:
#                 with open(config_path) as f:
#                     config = json.load(f)
#                     current_version = config.get("version", "0.0.0")
#             except FileNotFoundError:
#                 print('Could not find local configuration file.')
#                 raise HTTPException(status_code=500, detail="Local configuration file not found.")
            
#             # Compare the versions using version.parse() to handle version strings properly
#             current_version_parsed = version.parse(current_version)
#             latest_version_parsed = version.parse(latest_version)

#             if current_version_parsed > latest_version_parsed:
#                 message = f"Please be advised:\nThe version you are working with seems to be newer.\n" \
#                           f"The latest version of ISGP is {latest_version}, while your version is {current_version}."
#             elif current_version_parsed < latest_version_parsed:
#                 message = f"Please be advised:\nThe version you are working with is not up to date.\n" \
#                           f"The latest version of ISGP is {latest_version}, while your version is {current_version}."
#             else:
#                 message = f"Your version is up to date. You are using the latest version ({current_version})."

#             return {
#                 "updateAvailable": current_version_parsed != latest_version_parsed,
#                 "currentVersion": current_version,
#                 "message": message
#             }

#     except httpx.RequestError as e:
#         # Log the error for debugging purposes (optional)
#         print(f"GitHub request failed: {str(e)}")
#         raise HTTPException(status_code=502, detail="Failed to connect to GitHub to check the version.")