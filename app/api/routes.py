from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.link import LinkCreate, LinkOut, LinkStats
from app.crud.link import create_short_link, get_by_code, increment_click
from app.core.config import settings

router = APIRouter()


@router.post("/shorten", response_model=LinkOut, status_code=201)
def shorten(payload: LinkCreate, db: Session = Depends(get_db)):
    link = create_short_link(db, original_url=str(payload.url))
    return LinkOut(
        code=link.code,
        short_url=f"{settings.BASE_URL.rstrip('/')}/{link.code}",
        original_url=link.original_url,
        clicks=link.clicks,
    )


@router.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    link = get_by_code(db, code)
    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")

    increment_click(db, link)
    return RedirectResponse(url=link.original_url, status_code=307)


@router.get("/stats/{code}", response_model=LinkStats)
def stats(code: str, db: Session = Depends(get_db)):
    link = get_by_code(db, code)
    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")
    return LinkStats(code=link.code, original_url=link.original_url, clicks=link.clicks)