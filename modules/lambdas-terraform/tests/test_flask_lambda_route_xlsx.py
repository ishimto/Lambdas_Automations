import requests
import pytest

BASE_URL = "http://localhost:5000/xlsx"

def test_missing_csv_data():
    response = requests.post(BASE_URL, data={})
    assert response.status_code == 400
    assert "Missing csv_data" in response.text

def test_success_minimal_case():
    payload = {
        "csv_data": "Name;Age\nGeorge;30\nAlisonBurger;25",
        "output_file_name": "test.xlsx",
        "commit_message": "Test upload"
    }
    response = requests.post(BASE_URL, data=payload)
    assert response.status_code == 200
    assert "test.xlsx" in response.text or "successfully" in response.text

def test_missing_commit_message():
    payload = {
        "csv_data": "A;B\n1;2",
        "output_file_name": "no_commit.xlsx"
    }
    response = requests.post(BASE_URL, data=payload)
    assert response.status_code == 200

def test_missing_output_filename():
    payload = {
        "csv_data": "A;B\n1;2",
        "commit_message": "no output"
    }
    response = requests.post(BASE_URL, data=payload)
    assert response.status_code == 200
