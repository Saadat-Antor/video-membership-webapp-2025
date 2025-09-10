from .extractors import extract_video_id
from .models import Video
from pydantic import (
    BaseModel,
    model_validator,
    field_validator
)

class VideoCreateSchema(BaseModel):
    url: str
    user_id: str

    @field_validator('url')
    def validate_youtube_url(cls, v, values, **kwargs):
        url = v
        video_id = extract_video_id(url)
        if video_id is None:
            raise ValueError(f"{url} is not a valid YouTube URL.")
        return url
    
    @model_validator(mode="before")
    @classmethod
    def validate_data(cls, values):
        url = values.get("url")
        user_id = values.get("user_id")
        video_obj = None
        try:
            video_obj = Video.add_video(url=url, user_id=user_id)
        except:
            raise ValueError("There's a problem with your account, please try again.")
        if video_obj is None:
            raise ValueError("There's a problem with your account, please try again.")
        return video_obj.dict()