import requests

from conftest import json_response


def test_canned_response_round_trips_through_a_mounted_session(fake_shop):
    fake_shop.add("GET", "/health", json_response(200, {"status": "ok"}))
    session = requests.Session()
    session.mount("http://", fake_shop)

    response = session.get("http://shop.test/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert [request.url for request in fake_shop.requests] == ["http://shop.test/health"]
