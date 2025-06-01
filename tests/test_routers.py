from fastapi.testclient import TestClient
from app.main import app
from app.security import API_KEY_NAME, API_KEY
import pytest
from datetime import datetime
import os

os.environ["API_KEY_KERYKEION"] = "testapikey"

client = TestClient(app)

headers = {API_KEY_NAME: os.getenv("API_KEY_KERYKEION")}

def test_natal_chart_endpoint():
    natal_data = {
        "name": "Test Person",
        "year": 1990,
        "month": 7,
        "day": 15,
        "hour": 14,
        "minute": 30,
        "latitude": -23.5505,
        "longitude": -46.6333,
        "tz_str": "America/Sao_Paulo"
    }
    response = client.post("/api/v1/natal_chart", json=natal_data, headers=headers)
    assert response.status_code == 200, response.text
    assert "input_data" in response.json()
    assert response.json()["input_data"]["name"] == "Test Person"

def test_current_transits_endpoint():
    transit_data = {
        "year": datetime.now().year,
        "month": datetime.now().month,
        "day": datetime.now().day,
        "hour": 12,
        "minute": 0,
        "latitude": -23.5505,
        "longitude": -46.6333,
        "tz_str": "America/Sao_Paulo"
    }
    response = client.post("/api/v1/current_transits", json=transit_data, headers=headers)
    assert response.status_code == 200, response.text
    assert "input_data" in response.json()

def test_transits_to_natal_endpoint():
    natal_data = {
        "name": "Test Person",
        "year": 1990,
        "month": 7,
        "day": 15,
        "hour": 14,
        "minute": 30,
        "latitude": -23.5505,
        "longitude": -46.6333,
        "tz_str": "America/Sao_Paulo"
    }
    transit_data = {
        "year": datetime.now().year,
        "month": datetime.now().month,
        "day": datetime.now().day,
        "hour": 12,
        "minute": 0,
        "latitude": -23.5505,
        "longitude": -46.6333,
        "tz_str": "America/Sao_Paulo"
    }
    data = {
        "natal": natal_data,
        "transit": transit_data
    }
    response = client.post("/api/v1/transits_to_natal", json=data, headers=headers)
    assert response.status_code == 200, response.text
    assert "detail" in response.json()

def test_svg_chart_endpoint():
    natal_data = {
        "name": "Test Person",
        "year": 1990,
        "month": 7,
        "day": 15,
        "hour": 14,
        "minute": 30,
        "latitude": -23.5505,
        "longitude": -46.6333,
        "tz_str": "America/Sao_Paulo",
        "house_system": "Placidus"
    }
    data = {
        "natal_chart": natal_data,
        "chart_type": "natal",
        "show_aspects": True,
        "language": "pt",
        "theme": "light"
    }
    response = client.post("/api/v1/svg_chart", json=data, headers=headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/svg+xml"

def test_api_key_auth():
    natal_data = {
        "name": "Test Person",
        "year": 1990,
        "month": 7,
        "day": 15,
        "hour": 14,
        "minute": 30,
        "latitude": -23.5505,
        "longitude": -46.6333,
        "tz_str": "America/Sao_Paulo"
    }
    response = client.post("/api/v1/natal_chart", json=natal_data)
    assert response.status_code == 403, response.text
    assert response.json()["detail"] == "Could not validate API Key"

def test_resource_not_found_exception():
    response = client.get("/api/v1/nonexistent_route", headers=headers)
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Not Found"

def test_invalid_input_exception():
    invalid_data = {
        "name": "Test Person",
        "year": 1990,
        "month": 15,
        "day": 15,
        "hour": 14,
        "minute": 30,
        "latitude": -23.5505,
        "longitude": -46.6333,
        "tz_str": "America/Sao_Paulo"
    }
    response = client.post("/api/v1/natal_chart", json=invalid_data, headers=headers)
    assert response.status_code == 422, response.text
    assert "detail" in response.json()
