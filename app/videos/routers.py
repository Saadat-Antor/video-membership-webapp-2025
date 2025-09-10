from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from .models import Video
from app.shortcuts import render

router = APIRouter(
    prefix='/videos'
)

@router.get("/", response_class=HTMLResponse)
def video_list_view(request: Request):
    print(request.user)
    q = Video.objects.all().limit(100)
    context = {
        "object_list": q
    }
    return render(request, "videos/list.html", context)


@router.get("/detail", response_class=HTMLResponse)
def video_detail_view(request: Request):
    context = {}
    return render(request, "videos/detail.html", context)