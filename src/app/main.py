import secrets
import string

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import URL
from app.schemas import ShortenRequest, ShortenResponse, StatsResponse

app = FastAPI(title="URL Shortener")

CODE_LENGTH = 8
CODE_ALPHABET = string.ascii_letters + string.digits


def generate_code(length: int = CODE_LENGTH) -> str:
    return "".join(secrets.choice(CODE_ALPHABET) for _ in range(length))


@app.post("/shorten", response_model=ShortenResponse, status_code=201)
def shorten_url(body: ShortenRequest, request: Request, db: Session = Depends(get_db)):
    code = generate_code()
    while db.query(URL).filter(URL.code == code).first() is not None:
        code = generate_code()

    url_entry = URL(code=code, original_url=str(body.url))
    db.add(url_entry)
    db.commit()
    db.refresh(url_entry)

    short_url = str(request.base_url) + code
    return ShortenResponse(code=code, short_url=short_url)


@app.get("/stats/{code}", response_model=StatsResponse)
def get_stats(code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.code == code).first()
    if url_entry is None:
        raise HTTPException(status_code=404, detail="Code not found")
    return StatsResponse(code=url_entry.code, redirect_count=url_entry.redirect_count)


@app.get("/{code}")
def redirect_to_url(code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.code == code).first()
    if url_entry is None:
        raise HTTPException(status_code=404, detail="Code not found")
    url_entry.redirect_count += 1
    db.commit()
    return RedirectResponse(url=url_entry.original_url, status_code=302)
