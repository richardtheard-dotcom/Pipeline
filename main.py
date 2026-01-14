from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
import uuid
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Article(BaseModel):
    id: str
    subject: str
    source: str
    title: str
    author: str
    publish_date: str
    url: str
    full_text: str
    summary: str

def fetch_articles(subject: str, count: int = 5) -> List[Article]:
    articles = []
    for i in range(1, count + 1):
        full_text = f"This is the full text of article {i} about {subject}. It contains detailed information."
        summary = generate_summary(full_text)
        article = Article(
            id=str(uuid.uuid4()),
            subject=subject,
            source=f"Source {i}",
            title=f"Sample Article {i} on {subject}",
            author=f"Author {i}",
            publish_date=f"2026-01-1{i}",
            url=f"https://example.com/article{i}",
            full_text=full_text,
            summary=summary
        )
        articles.append(article)
    return articles

def generate_summary(full_text: str) -> str:
    words = full_text.split()
    return ' '.join(words[:20]) + ('...' if len(words) > 20 else '')

@app.get("/articles", response_model=List[Article])
async def get_articles(subject: str = Query(...)):
    return fetch_articles(subject)

