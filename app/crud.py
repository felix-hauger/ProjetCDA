import secrets, string, datetime
from sqlmodel import select, Session
from .models import Link

ALPHABET = string.ascii_letters + string.digits

def generate_slug(session: Session, length: int = 6) -> str:
    while True:
        slug = ''.join(secrets.choice(ALPHABET) for _ in range(length))
        if not session.exec(select(Link).where(Link.slug == slug)).first():
            return slug

def create_link(session: Session, original_url: str, expires_at=None) -> Link:
    slug = generate_slug(session)
    link = Link(slug=slug, original_url=original_url, expires_at=expires_at)
    session.add(link)
    session.commit()
    session.refresh(link)
    return link
