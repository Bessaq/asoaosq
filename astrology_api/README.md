# AstroAPI

API para cálculos astrológicos, mapas natais, trânsitos, sinastria, progressões, retornos solares/lunares, direções e interpretações.

## Visão Geral

A AstroAPI é uma API RESTful para cálculos astrológicos, oferecendo funcionalidades para gerar mapas natais, calcular trânsitos planetários, analisar aspectos entre planetas, calcular sinastria, progressões secundárias, retornos solares e lunares, direções de arco solar e gerar representações visuais em SVG. Também inclui capacidade de responder a perguntas e gerar interpretações astrológicas com base em uma coleção de livros utilizando busca avançada de texto com TF-IDF.

A API é construída usando FastAPI e utiliza a biblioteca Kerykeion para os cálculos astrológicos e geração de gráficos.

## Funcionalidades Principais

- **Cálculo de Mapas Natais**: Obtenha dados detalhados de um mapa astrológico natal com posições planetárias, casas, e aspectos.
- **Cálculo de Trânsitos**: Calcule posições planetárias para uma data/hora específica.
- **Análise de Trânsitos sobre Mapa Natal**: Analise aspectos entre planetas em trânsito e planetas natais.
- **Sinastria (Comparação de Mapas)**: Compare dois mapas natais e analise a compatibilidade astrológica.
- **Progressões Secundárias**: Calcule progressões secundárias para um mapa natal.
- **Retornos Solares e Lunares**: Calcule retornos solares anuais e retornos lunares mensais.
- **Direções de Arco Solar**: Calcule direções por arco solar.
- **Geração de Gráficos SVG**: Gere representações visuais de mapas astrológicos em formato SVG.
- **Personalização de Sistema de Casas**: Escolha entre diferentes sistemas de casas astrológicas (Placidus, Koch, etc.).
- **Suporte a Múltiplos Idiomas**: Obtenha resultados em diferentes idiomas (suportados: português, inglês, espanhol, francês, italiano e alemão).
- **Interpretações Textuais**: Receba interpretações baseadas em livros de astrologia usando busca avançada com TF-IDF.
- **Cache de Cálculos**: Sistema de cache em dois níveis (memória e disco) para melhorar o desempenho.

## Requisitos

- Python 3.9+
- Bibliotecas: FastAPI, Kerykeion, Uvicorn, Python-dotenv, Pydantic, PyTZ

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/astrology-api.git
   cd astrology-api
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Crie um arquivo .env a partir do .env.example:
   ```bash
   cp .env.example .env
   ```

## Uso da API

### Iniciar o servidor

```bash
uvicorn main:app --reload
```

### Documentação da API

A documentação interativa estará disponível em:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints Principais

#### Mapa Natal
```
POST /api/v1/natal_chart
```
Calcula um mapa natal completo com posições planetárias, casas e aspectos.

#### Trânsitos
```
POST /api/v1/transit_chart
```
Calcula as posições planetárias para uma data específica.

```
POST /api/v1/transits_to_natal
```
Calcula os trânsitos sobre um mapa natal, incluindo aspectos entre planetas em trânsito e natais.

#### Sinastria
```
POST /api/v1/synastry
```
Calcula a sinastria (comparação) entre dois mapas natais, incluindo aspectos entre os planetas.

#### Progressões Secundárias
```
POST /api/v1/progressions
```
Calcula as progressões secundárias para um mapa natal.

#### Retornos Solares
```
POST /api/v1/solar-return
```
Calcula o retorno solar para um ano específico.

#### Retornos Lunares
```
POST /api/v1/lunar-return
```
Calcula o retorno lunar mais próximo para um mês/ano específico.

#### Direções de Arco Solar
```
POST /api/v1/solar-arc
```
Calcula as direções de arco solar para uma data específica.

#### Gráficos SVG
```
POST /api/v1/svg_chart
```
Gera um gráfico SVG para um mapa natal, trânsito ou combinado.

```
POST /api/v1/svg_chart_base64
```
Igual ao endpoint acima, mas retorna o SVG em formato Base64.

### Configuração da API Key

Edite o arquivo .env para adicionar sua chave de API:
```
API_KEY_ASTROLOGIA=sua_chave_secreta_aqui
```

Todos os endpoints requerem uma chave de API válida no cabeçalho `X-API-KEY`.

## Estrutura do Projeto

```
astrology_api/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── natal_chart_router.py
│   │   ├── transit_router.py
│   │   ├── svg_chart_router.py
│   │   ├── synastry_router.py
│   │   ├── progression_router.py
│   │   ├── return_router.py
│   │   └── direction_router.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── calculations.py
│   │   ├── cache.py
│   │   └── utils.py
│   ├── interpretations/
│   │   ├── __init__.py
│   │   ├── text_search.py
│   │   └── translations.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── svg/
│   │   ├── __init__.py
│   │   └── generators.py
│   ├── security.py
│   └── __init__.py
├── data/
│   ├── processed_texts/
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── .env.example
├── main.py
└── requirements.txt
```

## Exemplo de Uso

### Exemplo de Cálculo de Sinastria

```bash
curl -X POST "http://localhost:8000/api/v1/synastry" \
-H "Content-Type: application/json" \
-H "X-API-KEY: sua_chave_secreta_aqui" \
-d '{
  "chart1": {
    "name": "Pessoa 1",
    "year": 1990,
    "month": 5,
    "day": 15,
    "hour": 10,
    "minute": 30,
    "longitude": -46.63,
    "latitude": -23.55,
    "tz_str": "America/Sao_Paulo",
    "house_system": "Placidus",
    "language": "pt"
  },
  "chart2": {
    "name": "Pessoa 2",
    "year": 1992,
    "month": 8,
    "day": 22,
    "hour": 15,
    "minute": 45,
    "longitude": -46.63,
    "latitude": -23.55,
    "tz_str": "America/Sao_Paulo",
    "house_system": "Placidus",
    "language": "pt"
  },
  "include_interpretations": true
}'
```

### Exemplo de Cálculo de Progressões

```bash
curl -X POST "http://localhost:8000/api/v1/progressions" \
-H "Content-Type: application/json" \
-H "X-API-KEY: sua_chave_secreta_aqui" \
-d '{
  "natal_chart": {
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
    "language": "pt"
  },
  "progression_date": {
    "year": 2025,
    "month": 5,
    "day": 31
  },
  "include_natal_comparison": true,
  "include_interpretations": true
}'
```

### Exemplo de Geração de SVG

```bash
curl -X POST "http://localhost:8000/api/v1/svg_chart" \
-H "Content-Type: application/json" \
-H "X-API-KEY: sua_chave_secreta_aqui" \
-d '{
  "natal_chart": {
    "name": "Albert Einstein",
    "year": 1879,
    "month": 3,
    "day": 14,
    "hour": 11,
    "minute": 30,
    "longitude": 10.0,
    "latitude": 48.4,
    "tz_str": "Europe/Berlin",
    "house_system": "Placidus",    "language": "pt"
  },
  "chart_type": "natal",
  "show_aspects": true,
  "language": "pt",
  "theme": "light"
}'
```

### Exemplo de Retorno Solar

```bash
curl -X POST "http://localhost:8000/api/v1/solar-return" \
-H "Content-Type: application/json" \
-H "X-API-KEY: sua_chave_secreta_aqui" \
-d '{
  "natal_chart": {
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
    "language": "pt"
  },
  "return_year": 2023,
  "location_longitude": -46.63,
  "location_latitude": -23.55,
  "location_tz_str": "America/Sao_Paulo",
  "include_natal_comparison": true,
  "include_interpretations": true
}'
```

## Sistema de Busca de Interpretações

A API utiliza um sistema avançado de busca de texto baseado em TF-IDF para encontrar interpretações relevantes nos textos astrológicos. Isso permite:

1. Interpretações de planetas em signos e casas
2. Interpretações de aspectos entre planetas
3. Interpretações específicas para configurações astrológicas

As interpretações são obtidas através de busca avançada em textos astrológicos processados. Para usar esta funcionalidade, defina `include_interpretations: true` nas requisições.

## Cache e Otimização de Performance

A API implementa um sistema de cache em dois níveis:
1. Cache em memória para acesso rápido
2. Cache persistente em disco para resultados de longo prazo

Isso melhora significativamente o desempenho para cálculos repetidos, especialmente para retornos solares e lunares que exigem cálculos iterativos.

## Suporte a Múltiplos Idiomas

A API suporta os seguintes idiomas:

- Português (pt)
- Inglês (en)
- Espanhol (es)
- Francês (fr)
- Italiano (it)
- Alemão (de)

## Contribuições

Contribuições são bem-vindas! Por favor, sinta-se à vontade para enviar um Pull Request.

## Licença

Este projeto está licenciado sob a licença MIT.

## Contato

Para dúvidas ou sugestões, entre em contato através do GitHub.
  "theme": "light"
}' -o einstein_natal.svg
```

## Testes

Para executar os testes:

```bash
pytest tests/
```

## Licença

[MIT](LICENSE)

---

*Documentação atualizada em: 31/05/2025*
