from fastapi import FastAPI
from src.routers import first_fifty_comments
from src.routers import most_used_words
from src.routers import most_used_words_top10


app = FastAPI()

app.include_router(first_fifty_comments.router)
app.include_router(most_used_words.router)
app.include_router(most_used_words_top10.router)