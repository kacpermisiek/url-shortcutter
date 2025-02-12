from typing import Optional

import shortuuid
import sqlalchemy.exc
from fastapi import HTTPException
from pydantic import HttpUrl
from sqlalchemy.orm import Session
from starlette.requests import Request
from tenacity import retry, retry_if_exception_type, stop_after_attempt

from url_shortcutter.app.schemas.url import (
    CreatedBySchema,
    UrlCreateReturnSchema,
    UrlStatsSchema,
)
from url_shortcutter.app.settings import settings
from url_shortcutter.models import Url

ALPHABET = "".join([chr(i) for i in range(33, 127)])


@retry(
    retry=retry_if_exception_type(ValueError),
    stop=stop_after_attempt(10),
)
def generate_suffix(db: Session) -> str:
    length = settings.suffix_length
    shortuuid.set_alphabet(ALPHABET)
    suffix = shortuuid.ShortUUID().random(length)

    if db.query(Url).filter(Url.short_suffix == suffix).first():
        raise ValueError("Suffix already exists")

    return suffix


def add_url_to_db(original_url: HttpUrl, request: Request, db: Session) -> Url:
    try:
        product = Url(
            short_suffix=generate_suffix(db),
            url=str(original_url),
            created_by_ip=request.client.host,
            created_by_user_agent=request.headers.get("User-Agent"),
        )
        db.add(product)
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        # In case when the URL already exists, we return the existing URL
        db.rollback()
        product = db.query(Url).filter(Url.url == str(original_url)).first()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not create URL")

    return product


def add_url_to_db_and_return_create_schema(
    original_url: HttpUrl, request: Request, db: Session
) -> UrlCreateReturnSchema:

    product = add_url_to_db(original_url, request, db)

    return UrlCreateReturnSchema(
        short_url=HttpUrl(str(request.base_url) + product.short_suffix),
        original_url=HttpUrl(product.url),
    )


def get_url_by_suffix(suffix: str, db: Session) -> Url:
    url: Optional[Url] = db.query(Url).filter(Url.short_suffix == suffix).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return url


def get_url_stats(suffix: str, db: Session, request: Request) -> UrlStatsSchema:
    url = get_url_by_suffix(suffix, db)
    return UrlStatsSchema(
        short_url=HttpUrl(str(request.base_url) + url.short_suffix),
        original_url=HttpUrl(url.url),
        visits=url.visits,
        created_by=CreatedBySchema(ip=url.created_by_ip, user_agent=url.created_by_user_agent),
    )


def update_url_stats(suffix: str, db: Session) -> None:
    url = get_url_by_suffix(suffix, db)
    url.visits += 1
    db.commit()


def get_redirect_url(short_suffix: str, db: Session) -> str:
    update_url_stats(short_suffix, db)
    url = get_url_by_suffix(short_suffix, db)
    return url.url
