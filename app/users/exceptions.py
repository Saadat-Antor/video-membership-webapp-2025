from fastapi import HTTPException

class LoginRequiredException(HTTPException):
    pass

# class LoginRequiredException(Exception):
#     pass

class InvalidUserIdException(HTTPException):
    pass

class InvalidEmailException(Exception):
    """
        If the user is not validated thus invalid, this exception will occur.
    """

class UserAlreadyHasAccountException(Exception):
    """
    If the email has already been registered, this exception will be called.
        
    """