from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field, UrlConstraints
from typing import Annotated

class LinkCreate(BaseModel):
    url: HttpUrl
    expires_at: datetime | None = None

class LinkOut(BaseModel):
    slug: str
