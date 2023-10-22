from fastapi import APIRouter, HTTPException
from src.services.endpoint1_services import HackerNewsService as hackernews

router = APIRouter()

@router.get("/top_stories_comments/")
async def read_top_stories_comments():
    try:
        return await hackernews.get_top_stories_comments()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))