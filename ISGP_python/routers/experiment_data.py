import os
from fastapi import APIRouter, Depends, Response, UploadFile, File, Form
from fastapi.responses import FileResponse
from modules.experiment_data_module.filtered_data_module import get_filtered_data
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

@router.get("/getFilteredData/{w0}/{w1}")
async def get_filtered_data_graph(w0:float,w1:float,project_name: str = Depends(get_current_project_name)):

    filtered_data = get_filtered_data(w0,w1)
    return {"filteredData":filtered_data}

@router.get("/getExampleTextFile")
async def get_example_text_file(project_name: str = Depends(get_current_project_name)):
    # Path to the file to be downloaded
    file_path = get_example_text_file_path()
    # If the file exists, return it for download
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/octet-stream', filename="downloaded_file.txt")
    else:
        return Response(content="File not found", status_code=404)
    
@router.get("/getExampleExcelFile")
async def get_example_text_file(project_name: str = Depends(get_current_project_name)):
    # Path to the file to be downloaded
    file_path = get_example_excel_file_path()
    # If the file exists, return it for download
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/octet-stream', filename="downloaded_file.txt")
    else:
        return Response(content="File not found", status_code=404)
