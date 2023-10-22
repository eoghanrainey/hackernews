from fastapi import APIRouter, HTTPException
from src.services.first_fifty_comments import HackerNewsService as hackernews


router = APIRouter()


@router.get("/first_fifty_comments/", summary="First 50 comments", description="Return the first 50 comments "
                                                                               "(only the comment itself, not the ")
async def read_top_stories_comments():
    try:
        return await hackernews.get_top_stories_comments()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))