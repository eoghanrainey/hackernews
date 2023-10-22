import re
from collections import Counter
from http.client import HTTPException


import httpx
import asyncio

from src.models.comment import Comment_Most_Used

HACKERNEWS_API = 'https://hacker-news.firebaseio.com/v0'

class HackerNewsService:
    @staticmethod
    async def get_top_stories_comments():
        comments = []
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f'{HACKERNEWS_API}/topstories.json')
                response.raise_for_status()
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

            response_json = response.json()
            top_stories = response_json[:10] if response_json else []

            tasks = []
            for story_id in top_stories:
                tasks.append(HackerNewsService.fetch_story_comments(client, story_id))
            all_comments = await asyncio.gather(*tasks)

            for comment_list in all_comments:
                comments.extend(comment_list)

        words_counter = Counter()

        for comment in comments:
            if comment and comment.text:
                words_counter.update(re.findall(r'\b\w+\b', comment.text))

        return words_counter.most_common(10)

    @staticmethod
    async def fetch_story_comments(client, story_id):
        try:
            response = await client.get(f'{HACKERNEWS_API}/item/{story_id}.json')
            response.raise_for_status()
        except:
            raise HTTPException(status_code=500, detail="Failed to fetch story")

        response_json = response.json()
        story = response_json if response_json else {}

        comments = []
        if story and 'kids' in story:
            comments = await HackerNewsService.fetch_all_comments(client, story['kids'])

        return comments

    @staticmethod
    async def fetch_all_comments(client, comment_ids):
        comments = []
        tasks = []
        for comment_id in comment_ids:
            tasks.append(HackerNewsService.fetch_comment(client, comment_id))
        fetched_comments = await asyncio.gather(*tasks)

        for comment in fetched_comments:
            if comment is not None:
                comments.append(comment)
                if 'kids' in comment:
                    comments.extend(await HackerNewsService.fetch_all_comments(client, comment.kids))

        return comments

    @staticmethod
    async def fetch_comment(client, comment_id):
        try:
            response = await client.get(f'{HACKERNEWS_API}/item/{comment_id}.json')
            response.raise_for_status()
        except:
            raise HTTPException(status_code=500, detail="Failed to fetch comment")

        response_json = response.json()
        if response_json is not None:
            comment = Comment_Most_Used(**response_json)
        else:
            return None  # if the response is None, return None

        # Check if the comment is deleted or dead
        if comment.deleted or comment.dead:
            return None

        return comment