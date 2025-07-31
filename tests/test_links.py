"""
Tests for the URL Shortener service QuickPath (FastAPI).
Run with:  pytest -q
"""
from __future__ import annotations

import datetime
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel, Session

from app.main import app
from app.database import engine, get_session
from app import crud

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def _prepare_database():
    """Create all tables once per test session, drop them afterwards."""
    SQLModel.metadata.create_all(bind=engine)
    yield
    SQLModel.metadata.drop_all(bind=engine)

@pytest.fixture()
def session():
    """Provide a fresh SQLModel Session for each test function."""
    with Session(engine) as s:
        yield s

@pytest_asyncio.fixture()
async def client(session: Session):  # type: ignore[valid-type]
    """Async HTTP client wired to FastAPI with an overridden DB session."""
    app.dependency_overrides[get_session] = lambda: session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_create_link_success(client: AsyncClient):
    resp = await client.post("/links", json={"url": "https://example.com"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["slug"].isalnum() and 5 < len(body["slug"]) <= 8
    assert body["short_url"].endswith(body["slug"])

@pytest.mark.asyncio
async def test_create_link_invalid_url(client: AsyncClient):
    resp = await client.post("/links", json={"url": "notaurl"})
    assert resp.status_code == 422

@pytest.mark.asyncio
async def test_generate_slug_collision(monkeypatch, client: AsyncClient):
    """Force a collision on slug generation to ensure retry logic works."""

    calls = 0

    def fake_slug(_session: Session, length: int = 6) -> str:  # type: ignore[valid-type]
        nonlocal calls
        calls += 1
        return "ABC123" if calls == 1 else "XYZ999"

    monkeypatch.setattr(crud, "generate_slug", fake_slug)

    # first link → slug "ABC123"
    await client.post("/links", json={"url": "https://foo.com"})
    # second link triggers collision then returns "XYZ999"
    resp = await client.post("/links", json={"url": "https://bar.com"})
    assert resp.status_code == 201
    assert resp.json()["slug"] == "XYZ999"

@pytest.mark.asyncio
async def test_redirect_and_click_counter(client: AsyncClient):
    # create a link
    create = await client.post("/links", json={"url": "https://python.org"})
    slug = create.json()["slug"]

    # redirect
    resp = await client.get(f"/{slug}", follow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers["location"].rstrip("/") == "https://python.org"

    # stats should reflect 1 click
    stats = await client.get(f"/links/{slug}")
    data = stats.json()
    assert data["clicks"] == 1
    assert data["last_accessed"] is not None

@pytest.mark.asyncio
async def test_redirect_unknown_slug(client: AsyncClient):
    resp = await client.get("/doesnotexist", follow_redirects=False)
    assert resp.status_code == 404

@pytest.mark.asyncio
async def test_expired_link_returns_410(client: AsyncClient):
    past_iso = (datetime.datetime.utcnow() - datetime.timedelta(seconds=1)).isoformat() + "Z"
    create = await client.post(
        "/links",
        json={"url": "https://expired.example", "expires_at": past_iso},
    )

    slug = create.json()["slug"]

    resp = await client.get(f"/{slug}", follow_redirects=False)
    assert resp.status_code == 410
