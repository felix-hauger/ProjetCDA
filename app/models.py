from datetime import datetime, timedelta
from sqlmodel import Field, SQLModel

class Link(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True, max_length=8)
    original_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    clicks: int = 0
    last_accessed: datetime | None = None
    expires_at: datetime | None = None
