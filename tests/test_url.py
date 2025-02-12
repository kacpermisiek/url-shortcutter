from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from tests.conftest import get_url_by_original_url
from url_shortcutter.app.settings import settings
from url_shortcutter.models import Url

TEST_URL = "https://example.com/"


@pytest.mark.parametrize("url", ["invalid", 1, True, "exmaple.com"])
def test_url_create_should_raise_unprocessable_entity_if_url_is_not_valid(alice: TestClient, url: str):
    resp = alice.post("/shorten", json={"url": url})
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, resp.text


def test_url_create_should_create_new_url_in_db(alice: TestClient, db_api):
    resp = alice.post("/shorten", json={"url": TEST_URL})
    assert resp.status_code == HTTPStatus.OK, resp.text

    url_row = get_url_by_original_url(TEST_URL, db_api)

    assert url_row is not None
    assert url_row.url == TEST_URL
    assert url_row.short_suffix is not None
    assert len(url_row.short_suffix) == settings.suffix_length
    assert url_row.visits == 0
    assert url_row.created_by_ip == "testclient"
    assert url_row.created_by_user_agent == "testclient"


def test_url_create_should_return_existing_url_and_not_create_row_to_db_if_it_already_exists(alice: TestClient, db_api):
    first_resp = alice.post("/shorten", json={"url": TEST_URL})
    first_resp_url = first_resp.json()["short_url"]

    second_resp = alice.post("/shorten", json={"url": TEST_URL})
    second_resp_url = second_resp.json()["short_url"]

    assert first_resp_url == second_resp_url

    num_of_urls = db_api.query(Url).count()
    assert num_of_urls == 1


def test_url_redirection_should_increase_visits(alice: TestClient, db_api):
    resp = alice.post("/shorten", json={"url": "http://testserver/docs"})
    short_url = resp.json()["short_url"]

    assert short_url.startswith("http://testserver/")
    url_suffix = short_url.strip("http://testserver/")

    for i in range(10):
        redirect_resp = alice.get(url_suffix)
        assert redirect_resp.status_code == HTTPStatus.OK

    stats_resp = alice.get(f"{url_suffix}/stats")
    assert stats_resp.status_code == HTTPStatus.OK
    assert stats_resp.json()["visits"] == 10
