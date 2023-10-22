import httpx
import asyncio
from src.models.comment import Comment
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

        top_stories = response.json()[:30]

        tasks = []
        for story_id in top_stories:
            tasks.append(fetch_story_comments(client, story_id))
        all_comments = await asyncio.gather(*tasks)

        for comment_list in all_comments:
            comments.extend(comment_list)
            # Stop once we have collected 100 comments
            if len(comments) >= 100:
                break

    words_counter = Counter()

    for comment in comments[:100]:
        words_counter.update(re.findall(r'\b\w+\b', comment['text'] or ''))

    return words_counter.most_common(10)


async def fetch_story_comments(client, story_id):
    comments = []
    try:
        response = await client.get(f'{HACKERNEWS_API}/item/{story_id}.json')
        response.raise_for_status()
    except:
        raise HTTPException(status_code=500, detail="Failed to fetch story")

    story = response.json()

    if 'kids' in story:
        tasks = []
        for comment_id in story['kids'][:100]:
            tasks.append(fetch_comment(client, comment_id))
        comments = await asyncio.gather(*tasks)

    return comments


async def fetch_comment(client, comment_id):
    try:
        response = await client.get(f'{HACKERNEWS_API}/item/{comment_id}.json')
        response.raise_for_status()
    except:
        raise HTTPException(status_code=500, detail="Failed to fetch comment")

    comment = Comment(**response.json())

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