from fastapi import FastAPI
from src.routers import first_fifty_comments
from src.routers import most_used_words
from src.routers import most_used_words_top10


app = FastAPI(
    title="Ecorus HackNews Api",
    description="Eoghan Rainey's Application to retrieve some data from the Hackernews API, transform it and return "
                "it via an API",
    version="1.0.0",
)

app.include_router(first_fifty_comments.router)
app.include_router(most_used_words.router)
app.include_router(most_used_words_top10.router)