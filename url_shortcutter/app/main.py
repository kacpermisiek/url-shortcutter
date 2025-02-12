from fastapi import Depends, FastAPI, Request
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from url_shortcutter.app.schemas.url import (
    UrlCreateReturnSchema,
    UrlCreateSchema,
    UrlStatsSchema,
)
from url_shortcutter.app.utils import (
    add_url_to_db_and_return_create_schema,
    get_redirect_url,
    get_url_stats,
)
from url_shortcutter.db import get_db

app = FastAPI()


@app.post("/shorten", response_model=UrlCreateReturnSchema, description="Shorten a URL")
def shorten_url(
    url_create: UrlCreateSchema, request: Request, db: Session = Depends(get_db())
) -> UrlCreateReturnSchema:
    return add_url_to_db_and_return_create_schema(url_create.url, request, db)


@app.get("/{short_suffix}", description="Redirect to the original URL")
def redirect_to_original_url(short_suffix: str, db: Session = Depends(get_db())):
    redirect_url = get_redirect_url(short_suffix, db)
    return RedirectResponse(redirect_url)


@app.get(
    "/{short_suffix}/stats",
    response_model=UrlStatsSchema,
    description="Get the stats of the shortened URL",
)
def get_stats(short_suffix: str, request: Request, db: Session = Depends(get_db())):
    return get_url_stats(short_suffix, db, request)
