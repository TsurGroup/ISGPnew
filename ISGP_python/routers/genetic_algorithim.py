import asyncio
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse, StreamingResponse
from sse_starlette import EventSourceResponse
from project_context import get_current_project_name
from cache.cache import get_project_status, set_project_status
from models.project_data import ProjectStatus
from modules.genetic_algorithm.genetic_algorithim_parallel import run_evolution
#from redis_orm.redis_client import get_project_status, set_project_status
from user_context import get_current_user,current_user_id

router = APIRouter()


async def event_generator():
    try:
        for data in run_evolution():
            yield data.json()
            project_status = get_project_status()
            if project_status == ProjectStatus.Aborted:
                set_project_status(ProjectStatus.Finished)
                break
 
    except asyncio.CancelledError:
        # Handle the cancellation explicitly if needed
        set_project_status(ProjectStatus.Finished)
        print("EventSource connection was cancelled.")

@router.get("/runEvolution")
def runEvolution(project_name: str = Depends(get_current_project_name)):
    try:
        set_project_status(ProjectStatus.Running)
        return EventSourceResponse(event_generator())
    except Exception as e:
        print(f"Error in runEvolution: {e}")
    finally:
        print("runEvolution endpoint finished.")


@router.post("/abortEvolution")
async def abort_evolution( project_name: str = Depends(get_current_project_name)):#user_id: str = Depends(get_current_user)

    try:
       #set_project_status(user_id,ProjectStatus.Aborted)
       #project_status = get_project_status(user_id)
       set_project_status(ProjectStatus.Aborted)
       project_status = get_project_status()
       while(project_status is not ProjectStatus.Finished):
           await asyncio.sleep(1)
          # project_status = get_project_status(user_id)
           project_status = get_project_status()

    except Exception as e:
        print('An exception occurred:', e)
        raise HTTPException(status_code=500, detail="Could not retrieve user ID")
    
    return JSONResponse(content={"message": "Abort signal sent, stopping the evolution process..."})

@router.get("/evolutionStatus")
def evolution_status(project_name: str = Depends(get_current_project_name)):#user_id: str = Depends(get_current_user)

    #project_status = get_project_status(user_id)
    project_status = get_project_status()
    if project_status == ProjectStatus.Aborted:
        return JSONResponse(content={"status": "Aborting"})
    if project_status == ProjectStatus.Finished:
        return JSONResponse(content={"status": "Finished"})
    return JSONResponse(content={"status": "Running"})
