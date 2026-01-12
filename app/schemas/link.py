from pydantic import BaseModel, HttpUrl, Field


class LinkCreate(BaseModel):
    url: HttpUrl


class LinkOut(BaseModel):
    code: str
    short_url: str
    original_url: str
    clicks: int = 0

    class Config:
        from_attributes = True


class LinkStats(BaseModel):
    code: str
    original_url: str
    clicks: int