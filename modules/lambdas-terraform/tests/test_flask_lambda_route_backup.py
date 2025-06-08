import requests
import pytest

BASE_URL = "http://localhost:5000/backup"

def test_successful_backup():
    payload = {
        "file_name": "output.xlsx",
        "bucket_name": "hdo4bucket",
        "gitlab_user": "main-group",
        "gitlab_repo": "xlsx_files",
        "gitlab_branch": "main"
    }

    response = requests.post(BASE_URL, data=payload)

    print("Success Response:", response.text)
    assert response.status_code == 200
    assert "Successfully uploaded" in response.text


def test_nonexistent_file():
    payload = {
        "file_name": "nonexistent_file.txt",
        "bucket_name": "hdo4bucket",
        "gitlab_user": "main-group",
        "gitlab_repo": "xlsx_files",
        "gitlab_branch": "main"
    }

    response = requests.post(BASE_URL, data=payload)

    assert response.status_code == 500
    assert "Git backup to s3 lambda failed" in response.text


def test_invalid_bucket_name():
    payload = {
        "file_name": "output.xlsx",
        "bucket_name": "non-exist-bucket-name-test-blabla",
        "gitlab_user": "main-group",
        "gitlab_repo": "xlsx_files",
        "gitlab_branch": "main"
    }

    response = requests.post(BASE_URL, data=payload)

    assert response.status_code == 500
    assert "The specified bucket does not exist" in response.text


def test_missing_parameters():
    payload = {
        "gitlab_repo": "myrepo",
        "gitlab_branch": "main"
    }

    response = requests.post(BASE_URL, data=payload)

    assert response.status_code == 500
    assert "Git backup to s3 lambda failed" in response.text

