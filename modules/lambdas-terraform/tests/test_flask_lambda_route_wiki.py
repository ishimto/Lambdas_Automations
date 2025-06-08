import requests

BASE_URL = "http://localhost:5000/wiki"

def test_missing_title():
    response = requests.post(BASE_URL, data={})
    assert response.status_code == 400
    assert "Missing title" in response.text

def test_page_not_found():
    payload = {"title": "PageThatDoesNotExist1234567890"}
    response = requests.post(BASE_URL, data=payload)
    assert response.status_code == 404
    assert "not found" in response.text.lower()

def test_successful_summary_update():
    payload = {"title": "israel"}
    response = requests.post(BASE_URL, data=payload)
    assert response.status_code == 200
    assert "successfully" in response.text.lower()
