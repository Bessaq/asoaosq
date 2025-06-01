"""
Testes para a API de Astrologia.

Este módulo contém testes para os endpoints da API de Astrologia.
"""
import pytest
from fastapi.testclient import TestClient
import os
import sys

# Adicionar o diretório raiz ao path para importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from app.schemas.models import NatalChartRequest, TransitRequest, SVGChartRequest
from dotenv import load_dotenv

load_dotenv()

# Criar cliente de teste
client = TestClient(app)

# Dados de teste
EINSTEIN_DATA = {
    "name": "Albert Einstein",
    "year": 1879,
    "month": 3,
    "day": 14,
    "hour": 11,
    "minute": 30,
    "longitude": 10.0,
    "latitude": 48.4,
    "tz_str": "Europe/Berlin",
    "house_system": "Placidus",
    "language": "pt",
    "include_interpretations": False
}

TRANSIT_DATA = {
    "year": 2025,
    "month": 5,
    "day": 31,
    "hour": 12,
    "minute": 0,
    "longitude": -46.63,
    "latitude": -23.55,
    "tz_str": "America/Sao_Paulo",
    "house_system": "Placidus",
    "language": "pt",
    "include_interpretations": False
}

# Testes para o endpoint de mapa natal
def test_natal_chart():
    """Testa o endpoint de mapa natal."""
    response = client.post(
        "/api/v1/natal_chart",
        json=EINSTEIN_DATA,
        headers={"X-API-KEY": os.getenv("API_KEY_ASTROLOGIA", "dev_key")}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "planets" in data
    assert "houses" in data
    assert "ascendant" in data
    assert "midheaven" in data
    assert "aspects" in data
    
    # Verificar se o Sol está em Peixes para Einstein
    assert data["planets"]["sun"]["sign"] in ["Peixes", "Pisces"]

# Testes para o endpoint de trânsito
def test_transit_chart():
    """Testa o endpoint de trânsito."""
    response = client.post(
        "/api/v1/transit_chart",
        json=TRANSIT_DATA,
        headers={"X-API-KEY": os.getenv("API_KEY_ASTROLOGIA", "dev_key")}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "planets" in data
    assert "house_system" in data

# Testes para o endpoint de trânsitos sobre mapa natal
def test_transits_to_natal():
    """Testa o endpoint de trânsitos sobre mapa natal."""
    response = client.post(
        "/api/v1/transits_to_natal",
        json={
            "natal": EINSTEIN_DATA,
            "transit": TRANSIT_DATA,
            "include_interpretations": False
        },
        headers={"X-API-KEY": os.getenv("API_KEY_ASTROLOGIA", "dev_key")}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "natal_planets" in data
    assert "transit_planets" in data
    assert "aspects" in data

# Testes para o endpoint de geração de SVG
def test_svg_chart():
    """Testa o endpoint de geração de SVG."""
    response = client.post(
        "/api/v1/svg_chart",
        json={
            "natal_chart": EINSTEIN_DATA,
            "chart_type": "natal",
            "show_aspects": True,
            "language": "pt",
            "theme": "light"
        },
        headers={"X-API-KEY": os.getenv("API_KEY_ASTROLOGIA", "dev_key")}
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/svg+xml"
    assert "<svg" in response.text
    assert "</svg>" in response.text

# Testes para o endpoint de geração de SVG em Base64
def test_svg_chart_base64():
    """Testa o endpoint de geração de SVG em Base64."""
    response = client.post(
        "/api/v1/svg_chart_base64",
        json={
            "natal_chart": EINSTEIN_DATA,
            "chart_type": "natal",
            "show_aspects": True,
            "language": "pt",
            "theme": "light"
        },
        headers={"X-API-KEY": os.getenv("API_KEY_ASTROLOGIA", "dev_key")}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "svg_base64" in data
    assert "data_uri" in data
    assert data["data_uri"].startswith("data:image/svg+xml;base64,")

# Testes para o endpoint de sinastria
def test_synastry():
    """Testa o endpoint de sinastria."""
    response = client.post(
        "/api/v1/synastry",
        json={
            "chart1": EINSTEIN_DATA,
            "chart2": TRANSIT_DATA,
            "include_interpretations": False
        },
        headers={"X-API-KEY": os.getenv("API_KEY_ASTROLOGIA", "dev_key")}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "chart1_planets" in data
    assert "chart2_planets" in data
    assert "aspects" in data
    
    # Verificar se há aspectos entre os planetas dos dois mapas
    assert len(data["aspects"]) > 0
    
    # Verificar se os proprietários estão corretos
    for aspect in data["aspects"]:
        assert aspect["p1_owner"] == "chart1"
        assert aspect["p2_owner"] == "chart2"

# Testes para o endpoint de progressões
def test_progressions():
    """Testa o endpoint de progressões secundárias."""
    response = client.post(
        "/api/v1/progressions",
        json={
            "natal_chart": EINSTEIN_DATA,
            "progression_date": {
                "year": 2025,
                "month": 5,
                "day": 31
            },
            "include_natal_comparison": True,
            "include_interpretations": False
        },
        headers={"X-API-KEY": os.getenv("API_KEY_ASTROLOGIA", "dev_key")}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "progressed_planets" in data
    assert "natal_houses" in data
    assert "aspects" in data
    
    # Verificar se os planetas progressados foram calculados
    assert "sun" in data["progressed_planets"]
    assert "moon" in data["progressed_planets"]
    
    # Verificar se as casas natais foram preservadas
    assert "1" in data["natal_houses"]
    assert "10" in data["natal_houses"]

# Testes para o endpoint de retornos solares
def test_solar_return():
    """Testa o endpoint de retorno solar."""
    response = client.post(
        "/api/v1/solar-return",
        json={
            "natal_chart": EINSTEIN_DATA,
            "return_year": 2025,
            "include_natal_comparison": True,
            "include_interpretations": False
        },
        headers={"X-API-KEY": os.getenv("API_KEY_ASTROLOGIA", "dev_key")}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "return_planets" in data
    assert "return_houses" in data
    assert "return_date" in data
    
    # Verificar se os planetas do retorno foram calculados
    assert "sun" in data["return_planets"]
    assert "moon" in data["return_planets"]
    
    # Verificar se o Sol está na mesma posição zodiacal do mapa natal
    natal_sun_sign = EINSTEIN_DATA["day"] < 21 and "Pisces" or "Aries"
    return_sun_sign_original = data["return_planets"]["sun"]["sign_original"]
    assert return_sun_sign_original == natal_sun_sign

# Testes para o endpoint de retornos lunares
def test_lunar_return():
    """Testa o endpoint de retorno lunar."""
    response = client.post(
        "/api/v1/lunar-return",
        json={
            "natal_chart": EINSTEIN_DATA,
            "return_year": 2025,
            "return_month": 5,
            "include_natal_comparison": True,
            "include_interpretations": False
        },
        headers={"X-API-KEY": os.getenv("API_KEY_ASTROLOGIA", "dev_key")}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "return_planets" in data
    assert "return_houses" in data
    assert "return_date" in data
    
    # Verificar se os planetas do retorno foram calculados
    assert "sun" in data["return_planets"]
    assert "moon" in data["return_planets"]

# Testes para o endpoint de direções de arco solar
def test_solar_arc():
    """Testa o endpoint de direções de arco solar."""
    response = client.post(
        "/api/v1/solar-arc",
        json={
            "natal_chart": EINSTEIN_DATA,
            "direction_date": {
                "year": 2025,
                "month": 5,
                "day": 31
            },
            "direction_type": "solar_arc",
            "include_natal_comparison": True,
            "include_interpretations": False
        },
        headers={"X-API-KEY": os.getenv("API_KEY_ASTROLOGIA", "dev_key")}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "directed_planets" in data
    assert "natal_houses" in data
    assert "direction_value" in data
    
    # Verificar se os planetas direcionados foram calculados
    assert "sun" in data["directed_planets"]
    assert "moon" in data["directed_planets"]
    
    # Verificar se o valor da direção é coerente (aproximadamente 146 graus para Einstein em 2025)
    direction_value = data["direction_value"]
    assert 140 < direction_value < 150

# Testes para o endpoint de interpretação de texto
def test_interpret_text():
    """Testa o endpoint de interpretação de texto."""
    response = client.get(
        "/api/v1/interpret?query=Sol em Peixes",
        headers={"X-API-KEY": os.getenv("API_KEY_ASTROLOGIA", "dev_key")}
    )

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    if data:
        assert "source" in data[0]
        assert "matched_terms" in data[0]
        assert "paragraphs" in data[0]
