from contextvars import ContextVar
from fastapi import Cookie, HTTPException, Request




current_user_id: ContextVar[str] = ContextVar("current_user_id", default=None)


async def get_current_user(request: Request) -> str:
    # Access the cookies from the request object
    #print(request.__dict__)
    cookies = request.cookies
    #print(cookies)
    user_id = cookies.get("authToken")  # Assuming "authToken" is the name of the cookie
    
    #print("Received user_id from cookie:", user_id)  # Print the user ID extracted from the cookie
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    current_user_id.set(user_id)
    #print("Current user ID set to:", current_user_id.get())  # Print the value of current_user_id after setting
    return user_id