from typing import Dict
from .extractors import extract_video_id
from .models import Video
from app.users.exceptions import InvalidUserIdException
from .exceptions import (
    VideoAlreadyAddedException,
    InvalidYoutubeVideoUrlException
)
from pydantic import (
    BaseModel,
    model_validator,
    field_validator,
)

class VideoCreateSchema(BaseModel):
    url: str
    user_id: str
    title: str
    youtube_id: Dict

    # @field_validator('url')
    # def validate_youtube_url(cls, v, values, **kwargs):
    #     url = v
    #     video_id = extract_video_id(url)
    #     if video_id is None:
    #         raise ValueError(f"{url} is not a valid YouTube URL.")
    #     return url
    
    @model_validator(mode="before")
    @classmethod
    def validate_data(cls, values):
        url = values.get("url")
        user_id = values.get("user_id")
        title = values.get("title")
        video_obj = None
        extra_data = {}
        if title is not None:
            extra_data["title"] = title
        try:
            video_obj = Video.add_video(url=url, user_id=user_id, **extra_data)
        except VideoAlreadyAddedException:
            raise ValueError(f"{url} has already been added to your account.")
        except InvalidYoutubeVideoUrlException:
            raise ValueError(f"{url} is not a valid YouTube URL.")
        except InvalidUserIdException:
            raise ValueError("The user doesn't exist.")
        except:
            raise ValueError("There's a problem with your account, please try again.")
        if video_obj is None:
            raise ValueError("There's a problem with your account, please try again.")
        values["youtube_id"] = video_obj.as_data() # dict -> {"youtube_id": fRt65Bvgft}
        return values