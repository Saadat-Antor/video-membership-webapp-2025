from fastapi import Request, HTTPException
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        if not request.cookies.get("cookies"):
            raise HTTPException(status_code=400)
        return func(request, *args, **kwargs)
    return wrapper