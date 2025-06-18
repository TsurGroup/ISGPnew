import os
from fastapi import APIRouter, Depends, Response, UploadFile, File, Form
from fastapi.responses import FileResponse
import httpx
from models.project import FilterDataView
from modules.experiment_data_module.filtered_data_module import  get_filter, set_filter
from file_managment.file_manager import get_example_excel_file_path, get_example_text_file_path
from project_context import get_current_project_name
from modules.experiment_data_module.experiment_data_handler import  new_save_experiment_data#, save_experiment_data
from user_context import get_current_user


router = APIRouter()


@router.post("/SaveExperimentData")
async def save_experiment_data(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    w0: float = Form(...),
    w1: float = Form(...),
    useFilter: bool = Form(...),
    project_name: str = Depends(get_current_project_name)
):
    # Print the received form data for debugging
    print(f"Received form data - w0: {w0}, w1: {w1}, useFilter: {useFilter}")

    # Process files and form data
    kkt_graph1, kkt_graph2 = await new_save_experiment_data(file1, file2)
    
    # Return the processed data
    return kkt_graph1,  kkt_graph2


# @router.get("/getFilter/{w0}/{w1}")
# async def get_filtered_data_graph(w0:float,w1:float,project_name: str = Depends(get_current_project_name)):
    
#     success = set_filter(w0, w1, True)
#     filtered_data = get_filter(w0,w1)
#     return {"filteredData":filtered_data}

@router.post("/setFilter")
async def setFilter(data: FilterDataView, project_name: str = Depends(get_current_project_name)):

    filtered_data = []
    # Access the data from the request body
    w0 = data.w0
    w1 = data.w1
    useFilter = data.useFilter
    print(useFilter)
    # Your existing logic here...
    success = set_filter(w0, w1, useFilter)
    if(useFilter):
       filtered_data = get_filter(w0,w1)
    return {"success": success,"filteredData":filtered_data}


# @router.get("/getExampleTextFile")
# async def get_example_text_file(project_name: str = Depends(get_current_project_name)):
#     # Path to the file to be downloaded
#     file_path = get_example_text_file_path()
#     # If the file exists, return it for download
#     if os.path.exists(file_path):
#         return FileResponse(file_path, media_type='application/octet-stream', filename="downloaded_file.txt")
#     else:
#         return Response(content="File not found", status_code=404)
    
# @router.get("/getExampleExcelFile")
# async def get_example_text_file(project_name: str = Depends(get_current_project_name)):
#     # Path to the file to be downloaded
#     file_path = get_example_excel_file_path()
#     # If the file exists, return it for download
#     if os.path.exists(file_path):
#         return FileResponse(file_path, media_type='application/octet-stream', filename="downloaded_file.txt")
#     else:
#         return Response(content="File not found", status_code=404)

@router.get("/getExampleTextFile")
async def getExampleTextFile(project_name: str = Depends(get_current_project_name)):
    github_url = 'https://raw.githubusercontent.com/shem221/ISGPexampleFiles/refs/heads/main/RCData.txt'
    filename = 'RCData.txt'
    try:
        # Download file from GitHub
        await download_file_from_github(github_url, filename)
        # Return the file as a response
        return FileResponse(filename, media_type='application/octet-stream', headers={"Content-Disposition": f"attachment; filename={filename}"})
    except Exception as e:
        return {"error": str(e)}

@router.get("/getExampleExcelFile")
async def getExampleTextFile(project_name: str = Depends(get_current_project_name)):
    github_url = 'https://raw.githubusercontent.com/shem221/ISGPexampleFiles/refs/heads/main/RCData.xlsx'
    filename = 'RCData.xlsx'
    try:
        # Download file from GitHub
        await download_file_from_github(github_url, filename)
        # Return the file as a response
        return FileResponse(filename, media_type='application/octet-stream', headers={"Content-Disposition": f"attachment; filename={filename}"})
    except Exception as e:
        return {"error": str(e)}

async def download_file_from_github(url: str, filename: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        if response.status_code == 200:
            print("imhere")
            with open(filename, 'wb') as file:
                file.write(response.content)
            return filename
        else:
            raise Exception(f"Failed to download file. Status code: {response.status_code}")