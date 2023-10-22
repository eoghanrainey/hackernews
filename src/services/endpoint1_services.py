import httpx
import asyncio
from src.models.comment import Comment

HACKERNEWS_API = 'https://hacker-news.firebaseio.com/v0'

class HackerNewsService:
    @staticmethod
    async def get_top_stories_comments():
        comments = []

        async with httpx.AsyncClient() as client:
            response = await client.get(f'{HACKERNEWS_API}/topstories.json')
            response.raise_for_status()

            top_stories = response.json()[:100]

            tasks = []
            for story_id in top_stories:
                tasks.append(HackerNewsService.fetch_story_comments(client, story_id))
            all_comments = await asyncio.gather(*tasks)

            for comment_list in all_comments:
                comments.extend(comment_list)
                # Stop once we have collected 50 comments
                if len(comments) >= 50:
                    break

        return comments[:50]

    @staticmethod
    async def fetch_story_comments(client, story_id):
        comments = []

        response = await client.get(f'{HACKERNEWS_API}/item/{story_id}.json')
        response.raise_for_status()

        story = response.json()

        if 'kids' in story:
            tasks = []
            for comment_id in story['kids'][:50]:
                tasks.append(HackerNewsService.fetch_comment(client, comment_id))
            comments = await asyncio.gather(*tasks)

        return comments

    @staticmethod
    async def fetch_comment(client, comment_id):
        response = await client.get(f'{HACKERNEWS_API}/item/{comment_id}.json')
        response.raise_for_status()

        comment_data = response.json()
        comment = Comment(**comment_data)

        # Check if the comment is deleted or dead
        if comment.deleted or comment.dead:
            return None

        return comment