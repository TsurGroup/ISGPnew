import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query, Response , WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, StreamingResponse
from sse_starlette import EventSourceResponse
from project_context import get_current_project_name, set_proj_name
from cache.cache import get_project_status, set_project_status
from models.project_data import ProjectStatus
from modules.genetic_algorithm.genetic_algorithm import run_evolution
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

abort_events: dict[str, asyncio.Event] = {}

@router.websocket("/ws/runEvolution")
async def websocket_run_evolution(websocket: WebSocket, project_name: str = Query(...)):  # <-- get project_name from query param now
    set_proj_name(project_name)
    print("WebSocket connect attempt")
    await websocket.accept()
    print(f"WebSocket accepted for project: {project_name}")
    set_project_status(ProjectStatus.Running)

    cancel_event = asyncio.Event()
    abort_events[project_name] = cancel_event

    async def listen_for_abort():
        try:
            while True:
                message = await websocket.receive_text()
                if message.strip().lower() == "abort":
                    print("Abort signal received from client.")
                    set_project_status(ProjectStatus.Aborted)
                    cancel_event.set()
                    break
        except WebSocketDisconnect:
            print("Client disconnected during abort listen.")
            cancel_event.set()

    listener_task = asyncio.create_task(listen_for_abort())

    try:
        for data in run_evolution():
            if cancel_event.is_set():
                set_project_status(ProjectStatus.Aborted)
                break
            await websocket.send_text(data.json())

        set_project_status(ProjectStatus.Finished)

    except Exception as e:
        print(f"Error during evolution: {e}")
        set_project_status(ProjectStatus.Finished)

    finally:
        listener_task.cancel()
        abort_events.pop(project_name, None)
        await websocket.close()

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
