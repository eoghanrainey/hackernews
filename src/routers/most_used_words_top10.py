from fastapi import APIRouter, HTTPException
from src.services.most_used_words_top10 import HackerNewsService


router = APIRouter()

@router.get("/most_used_words_top10/", summary="return the most used words in all comments, "
                                               "including nested comments, of the first 10 stories.")
async def read_top_stories_comments():
    try:
        return await HackerNewsService.get_top_stories_comments()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))