import secrets
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.link import Link


def _gen_code(length: int = 7) -> str:
    # URL-safe base64-ish alphabet, short and readable
    alphabet = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def create_short_link(db: Session, original_url: str, code_len: int = 7) -> Link:
    # Try a few times to avoid collisions
    for _ in range(10):
        code = _gen_code(code_len)
        existing = db.scalar(select(Link).where(Link.code == code))
        if not existing:
            link = Link(code=code, original_url=original_url)
            db.add(link)
            db.commit()
            db.refresh(link)
            return link

    # fallback: longer code if too many collisions
    for _ in range(10):
        code = _gen_code(code_len + 2)
        existing = db.scalar(select(Link).where(Link.code == code))
        if not existing:
            link = Link(code=code, original_url=original_url)
            db.add(link)
            db.commit()
            db.refresh(link)
            return link

    raise RuntimeError("Could not generate unique short code")


def get_by_code(db: Session, code: str) -> Link | None:
    return db.scalar(select(Link).where(Link.code == code))


def increment_click(db: Session, link: Link) -> None:
    link.clicks += 1
    db.add(link)
    db.commit()