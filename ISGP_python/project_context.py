from contextvars import ContextVar
from fastapi import HTTPException, Request




current_project_name: ContextVar[str] = ContextVar("current_project_name", default=None)


async def get_current_project_name(request: Request) -> str:

    project_name = request.cookies.get("projectName")  # Assuming "projectName" is the name of the cookie

    if not project_name:
        raise HTTPException(status_code=401, detail="Unauthorized")

    current_project_name.set(project_name)

    return project_name

