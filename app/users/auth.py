from .models import User
import datetime
from jose import jwt, ExpiredSignatureError
from app.config import get_settings
settings = get_settings()

# step 1
def authenticate(email, password):
    try:
        user_obj = User.objects.get(email=email)
    except Exception as e:
        user_obj = None
    if user_obj is not None:
        if not user_obj.verify_password(password):
            return None
    return user_obj

# step 2
def login(user_obj, expires=5):
    raw_data = {
        "user_id": f"{user_obj.user_id}",
        "role": "admin",
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=expires)
    }
    
    return jwt.encode(raw_data, settings.secret_key, algorithm=settings.jwt_algo)

# step 3
def verify_user_id(token):
    data = {}
    try:
        data = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algo])
    except ExpiredSignatureError as e:
        print(e)
    except:
        pass
    if "user_id" not in data:
        return None
    return data