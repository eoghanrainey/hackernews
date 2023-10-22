from fastapi import APIRouter, HTTPException
from src.services import most_used_words

router = APIRouter()

@router.get("/most_used_words/", summary="10 most used words for first 100 comments")
async def read_top_stories_comments():
    try:
        return await most_used_words.get_top_stories_comments()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))