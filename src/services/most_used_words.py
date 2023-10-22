from fastapi import HTTPException
import httpx
import asyncio
from src.models.comment import Comment_Most_Used
from collections import Counter
import re

HACKERNEWS_API = 'https://hacker-news.firebaseio.com/v0'

async def get_top_stories_comments():
    comments = []
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f'{HACKERNEWS_API}/topstories.json')
            response.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        response_json = response.json()
        top_stories = response_json[:30] if response_json else []

        tasks = []
        for story_id in top_stories:
            tasks.append(fetch_story_comments(client, story_id))
        all_comments = await asyncio.gather(*tasks)

        for comment_list in all_comments:
            if comment_list is not None:
                comments.extend(comment_list)
            # Stop once we have collected 100 comments
            if len(comments) >= 100:
                break

    words_counter = Counter()

    for comment in comments[:100]:
        if comment and comment['text']:
            words_counter.update(re.findall(r'\b\w+\b', comment['text']))

    return words_counter.most_common(10)


async def fetch_story_comments(client, story_id):
    comments = []
    try:
        response = await client.get(f'{HACKERNEWS_API}/item/{story_id}.json')
        response.raise_for_status()
    except:
        raise HTTPException(status_code=500, detail="Failed to fetch story")

    response_json = response.json() if response and response.json() else {}
    story = response_json if response_json else {}

    if story and 'kids' in story:
        tasks = []
        comment_ids = story['kids'][:100] if story and 'kids' in story else []
        for comment_id in comment_ids:
            tasks.append(fetch_comment(client, comment_id))
        comments = await asyncio.gather(*tasks)

    return comments


async def fetch_comment(client, comment_id):
    try:
        response = await client.get(f'{HACKERNEWS_API}/item/{comment_id}.json')
        response.raise_for_status()
    except:
        raise HTTPException(status_code=500, detail="Failed to fetch comment")

    response_json = response.json() if response else None
    if response_json is not None:
        comment = Comment_Most_Used(**response_json)
    else:
        return None  # if the response is None, return None

    # Check if the comment is deleted or dead
    if comment.deleted or comment.dead:
        return None

    return {
        'id': comment.id,
        'text': comment.text,
        'by': comment.by,
        'parent': comment.parent,
        'time': comment.time,
    }