from contextvars import ContextVar
from fastapi import HTTPException, Request, WebSocket
from http.cookies import SimpleCookie

from config.env import get_env
from tests.test_data import test_project_name

current_project_name: ContextVar[str] = ContextVar("current_project_name", default=None)


async def get_current_project_name(request: Request = None, websocket: WebSocket = None) -> str:
    project_name = None
    #if request:
        # HTTP request: get project name from cookie
    project_name = request.cookies.get("projectName")

    # elif websocket:
    #     # WebSocket request: get project name from query params (or headers if you prefer)
    #     print("im a web socket")
    #     cookie_header = websocket.headers.get("cookie")
    #     print(cookie_header)
    #     project_name = get_cookie_value(cookie_header, "projectName")
       
    #     print(project_name)
    #     #project_name = websocket.query_params.get("project_name")

    if not project_name:
        # if websocket:
        #     # Close WebSocket connection with unauthorized code
        #     await websocket.close(code=1008)
        raise HTTPException(status_code=401, detail="Unauthorized")

    current_project_name.set(project_name)

    return project_name

def set_proj_name(project_name):
    current_project_name.set(project_name)
    return project_name

def get_cookie_value(cookie_header: str, cookie_name: str) -> str | None:
    if not cookie_header:
        return None
    cookie = SimpleCookie()
    cookie.load(cookie_header)
    morsel = cookie.get(cookie_name)
    if morsel:
        return morsel.value
    return None