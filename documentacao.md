# Documentação da API de Astrologia

## Visão Geral

Esta API de Astrologia é um sistema robusto para cálculos astrológicos, desenvolvido com FastAPI e a biblioteca Kerykeion. A API permite calcular mapas natais, trânsitos planetários e aspectos astrológicos, fornecendo dados precisos para aplicações astrológicas profissionais.

## Instalação

### Requisitos

- Python 3.8+
- pip

### Passos para Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/astrologia-api.git
cd astrologia-api
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Inicie o servidor:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Endpoints da API

### 1. Mapa Natal

**Endpoint:** `/api/v1/natal_chart`

**Método:** POST

**Descrição:** Calcula um mapa natal completo com posições planetárias, casas, ascendente, meio do céu e aspectos.

**Parâmetros de Requisição:**
```json
{
  "name": "Nome da Pessoa",
  "year": 2000,
  "month": 1,
  "day": 1,
  "hour": 12,
  "minute": 0,
  "longitude": 0.0,
  "latitude": 51.5,
  "tz_str": "UTC"
}
```

**Campos:**
- `name`: Nome da pessoa (opcional)
- `year`: Ano de nascimento (obrigatório)
- `month`: Mês de nascimento (1-12) (obrigatório)
- `day`: Dia de nascimento (1-31) (obrigatório)
- `hour`: Hora de nascimento (0-23) (obrigatório)
- `minute`: Minuto de nascimento (0-59) (obrigatório)
- `longitude`: Longitude do local de nascimento em graus decimais (obrigatório)
- `latitude`: Latitude do local de nascimento em graus decimais (obrigatório)
- `tz_str`: String de fuso horário (ex: "UTC", "Europe/Berlin") (obrigatório)

**Exemplo de Resposta:**
```json
{
  "input_data": {
    "name": "Test Modern Date",
    "year": 2000,
    "month": 1,
    "day": 1,
    "hour": 12,
    "minute": 0,
    "latitude": 51.5,
    "longitude": 0.0,
    "tz_str": "UTC",
    "house_system": "Placidus"
  },
  "sun": {
    "name": "Sun",
    "sign": "Cap",
    "sign_num": 9,
    "position": 10.3689,
    "abs_pos": 280.3689,
    "house_name": "N/A",
    "speed": 0.0,
    "retrograde": false
  },
  "moon": {
    "name": "Moon",
    "sign": "Sco",
    "sign_num": 7,
    "position": 13.3238,
    "abs_pos": 223.3238,
    "house_name": "N/A",
    "speed": 0.0,
    "retrograde": false
  },
  // Outros planetas, casas, ascendente, MC e aspectos...
}
```

### 2. Trânsitos Atuais

**Endpoint:** `/api/v1/current_transits`

**Método:** POST

**Descrição:** Calcula as posições planetárias para uma data e hora específicas.

**Parâmetros de Requisição:**
```json
{
  "year": 2023,
  "month": 5,
  "day": 28,
  "hour": 12,
  "minute": 0,
  "longitude": 0.0,
  "latitude": 51.5,
  "tz_str": "UTC"
}
```

**Campos:** Mesmos campos de data, hora e localização do endpoint de mapa natal.

### 3. Trânsitos em Relação ao Mapa Natal

**Endpoint:** `/api/v1/transits_to_natal`

**Método:** POST

**Descrição:** Calcula os trânsitos planetários em relação a um mapa natal, incluindo aspectos entre planetas em trânsito e planetas natais.

**Parâmetros de Requisição:**
```json
{
  "natal_data": {
    "name": "Nome da Pessoa",
    "year": 2000,
    "month": 1,
    "day": 1,
    "hour": 12,
    "minute": 0,
    "longitude": 0.0,
    "latitude": 51.5,
    "tz_str": "UTC"
  },
  "transit_data": {
    "year": 2023,
    "month": 5,
    "day": 28,
    "hour": 12,
    "minute": 0,
    "longitude": 0.0,
    "latitude": 51.5,
    "tz_str": "UTC"
  }
}
```

**Campos:**
- `natal_data`: Dados do mapa natal (mesmos campos do endpoint de mapa natal)
- `transit_data`: Dados para o cálculo dos trânsitos (mesmos campos de data, hora e localização)

## Considerações Importantes

### Fusos Horários

- Para datas modernas, use strings de fuso horário padrão como "UTC", "Europe/Berlin", "America/New_York", etc.
- Para datas históricas (antes de 1893), considere usar UTC com ajuste manual para o LMT (Local Mean Time).
- Exemplo para Ulm, Alemanha (10°E): Use "UTC" com hora ajustada para LMT (hora local - 40 minutos).

### Precisão dos Cálculos

- Posições planetárias: Precisão excelente, com diferenças mínimas em relação a fontes profissionais.
- Pontos angulares (Ascendente, MC): Podem apresentar variações de até 2-3 graus para datas históricas devido a diferenças no tratamento de fusos horários e algoritmos de cálculo.
- Para máxima precisão em datas históricas, considere validar resultados com múltiplas fontes.

### Limitações Conhecidas

- O sistema de casas padrão é Placidus, conforme implementado pelo Kerykeion.
- Cálculos para datas muito antigas (antes de 1800) podem ter precisão reduzida.
- Lilith (Lua Negra) pode não estar disponível em todos os cálculos.

## Exemplos de Uso

### Exemplo 1: Calcular Mapa Natal

```python
import requests
import json

url = "http://localhost:8000/api/v1/natal_chart"
data = {
    "name": "Albert Einstein",
    "year": 1879,
    "month": 3,
    "day": 14,
    "hour": 11,
    "minute": 30,
    "longitude": 10.0,
    "latitude": 48.40,
    "tz_str": "Europe/Berlin"
}

response = requests.post(url, json=data)
natal_chart = response.json()

# Acessar posição do Sol
sun_sign = natal_chart["sun"]["sign"]
sun_position = natal_chart["sun"]["position"]
print(f"Sol em {sun_sign} a {sun_position}°")

# Acessar Ascendente
asc_sign = natal_chart["ascendant"]["sign"]
asc_position = natal_chart["ascendant"]["position"]
print(f"Ascendente em {asc_sign} a {asc_position}°")
```

### Exemplo 2: Calcular Trânsitos Atuais

```python
import requests
import json
from datetime import datetime

now = datetime.now()

url = "http://localhost:8000/api/v1/current_transits"
data = {
    "year": now.year,
    "month": now.month,
    "day": now.day,
    "hour": now.hour,
    "minute": now.minute,
    "longitude": -46.63,  # São Paulo
    "latitude": -23.55,
    "tz_str": "America/Sao_Paulo"
}

response = requests.post(url, json=data)
transits = response.json()

# Listar posições planetárias atuais
for planet in transits["planets"]:
    print(f"{planet['name']} em {planet['sign']} a {planet['position']}°")
```

### Exemplo 3: Calcular Trânsitos em Relação ao Mapa Natal

```python
import requests
import json
from datetime import datetime

now = datetime.now()

url = "http://localhost:8000/api/v1/transits_to_natal"
data = {
    "natal_data": {
        "name": "Albert Einstein",
        "year": 1879,
        "month": 3,
        "day": 14,
        "hour": 11,
        "minute": 30,
        "longitude": 10.0,
        "latitude": 48.40,
        "tz_str": "Europe/Berlin"
    },
    "transit_data": {
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "hour": now.hour,
        "minute": now.minute,
        "longitude": 10.0,
        "latitude": 48.40,
        "tz_str": "Europe/Berlin"
    }
}

response = requests.post(url, json=data)
transit_data = response.json()

# Listar aspectos entre trânsitos e mapa natal
for aspect in transit_data["aspects_to_natal"]:
    print(f"{aspect['transit_planet']} em trânsito faz {aspect['aspect_name']} com {aspect['natal_planet_or_point']} natal (orbe: {aspect['orbit']}°)")
```

## Recursos Adicionais

### Bibliotecas Utilizadas

- **Kerykeion**: Biblioteca Python para cálculos astrológicos
- **FastAPI**: Framework web para APIs em Python
- **Swiss Ephemeris**: Efemérides astronômicas de alta precisão (via Kerykeion)

### Referências

- [Kerykeion GitHub](https://github.com/g-battaglia/kerykeion)
- [Swiss Ephemeris](https://www.astro.com/swisseph/)
- [Astro.com](https://www.astro.com/)
- [AstroDraw](https://astrodraw.github.io/)

## Suporte e Contribuições

Para suporte ou contribuições, entre em contato através do repositório GitHub ou abra uma issue.

---

© 2025 API de Astrologia - Todos os direitos reservados
