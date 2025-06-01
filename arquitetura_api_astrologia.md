# Definição da Arquitetura do Sistema e Funcionalidades Principais da API de Astrologia

Este documento descreve a arquitetura proposta e as funcionalidades centrais para a API de Astrologia, com base nas análises de bibliotecas e melhores práticas de APIs existentes.

## 1. Visão Geral da Arquitetura

A API será desenvolvida em Python, utilizando uma framework web leve como Flask ou FastAPI para construir os endpoints RESTful. A lógica astrológica principal será implementada utilizando a biblioteca Kerykeion, que por sua vez se baseia no Swiss Ephemeris para cálculos de alta precisão.

**Componentes Principais:**

1.  **Camada de API (Interface RESTful):**
    *   Responsável por receber requisições HTTP, validar entradas, interagir com a Camada de Lógica Astrológica e retornar respostas em formato JSON.
    *   Implementará os endpoints definidos.
    *   Framework: Flask ou FastAPI.

2.  **Camada de Lógica Astrológica (Core Astrológico):**
    *   Contém a lógica de negócios para todos os cálculos astrológicos.
    *   Utilizará a biblioteca Kerykeion para:
        *   Cálculo de posições planetárias e de casas.
        *   Cálculo de aspectos.
        *   Geração de dados para mapas natais, trânsitos, etc.
        *   Opcionalmente, geração de SVGs de mapas.
    *   Abstrai a complexidade do Kerykeion/Swiss Ephemeris da camada da API.

3.  **Camada de Utilitários/Configuração:**
    *   Funções auxiliares, tratamento de datas/horas, conversões, gerenciamento de configurações (se necessário).
    *   Validação de dados de entrada (latitude, longitude, fuso horário).

**Princípios de Design:**

*   **Modularidade:** Separar claramente as responsabilidades entre as camadas.
*   **Stateless:** A API será, idealmente, stateless. Cada requisição conterá toda a informação necessária para ser processada.
*   **Clareza e Consistência:** Nomes de endpoints e estruturas de dados serão intuitivos e consistentes.
*   **Escalabilidade:** A escolha de Python com Flask/FastAPI permite uma boa escalabilidade horizontal.
*   **Manutenibilidade:** Código bem organizado e documentado.

## 2. Especificações da API

*   **Protocolo:** HTTPS
*   **Formato de Dados:** JSON para todas as requisições e respostas.
*   **Versionamento:** A URL base incluirá um número de versão (ex: `/api/v1/`).
*   **Autenticação:** Inicialmente, será implementada autenticação baseada em Chave de API (API Key). A chave deverá ser enviada no cabeçalho HTTP `X-API-KEY`.
*   **Tratamento de Erros:** Serão utilizados códigos de status HTTP padrão (200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Internal Server Error). Respostas de erro incluirão um corpo JSON com uma mensagem clara.
*   **Codificação de Caracteres:** UTF-8.

## 3. Funcionalidades Principais e Endpoints

Os seguintes endpoints principais serão desenvolvidos. Todas as requisições que envolvem dados de nascimento ou de um momento específico exigirão data, hora, latitude, longitude e fuso horário (`tz_str`, ex: "America/Sao_Paulo").

**3.1. Cálculos de Mapa Natal (Natal Chart)**

*   **Endpoint:** `POST /api/v1/natal_chart`
*   **Descrição:** Calcula os detalhes de um mapa astral de nascimento.
*   **Corpo da Requisição (JSON):**
    ```json
    {
        "name": "Exemplo Pessoa", // Opcional
        "year": 1990,
        "month": 7,
        "day": 15,
        "hour": 14,
        "minute": 30,
        "latitude": -23.5505,
        "longitude": -46.6333,
        "tz_str": "America/Sao_Paulo",
        "house_system": "Placidus" // Opcional, default Placidus. Outros: Koch, Regiomontanus, Campanus, etc.
    }
    ```
*   **Resposta (JSON):**
    *   Dados do Solicitante (data, hora, local).
    *   Posições dos Planetas (Sol, Lua, Mercúrio, Vênus, Marte, Júpiter, Saturno, Urano, Netuno, Plutão, Nodo Norte, Nodo Sul, Quíron - opcional):
        *   Nome do planeta
        *   Signo (ex: "Áries")
        *   Grau (ex: 15.25)
        *   Longitude eclíptica absoluta (graus decimais)
        *   Casa astrológica em que se encontra
        *   Velocidade
        *   Se está retrógrado (true/false)
    *   Posições das Cúspides das Casas (1 a 12):
        *   Número da casa
        *   Signo
        *   Grau
    *   Ascendente (ASC) e Meio do Céu (MC):
        *   Signo
        *   Grau
    *   Aspectos Maiores (Conjunção, Oposição, Trígono, Quadratura, Sextil) entre planetas:
        *   Planeta 1
        *   Planeta 2
        *   Tipo de aspecto
        *   Orbe (diferença para o aspecto exato)
    *   (Opcional) Distribuição por elemento e qualidade.

**3.2. Trânsitos Planetários Atuais (Current Transits)**

*   **Endpoint:** `POST /api/v1/current_transits`
*   **Descrição:** Retorna as posições planetárias para um dado momento e local.
*   **Corpo da Requisição (JSON):**
    ```json
    {
        "year": 2025, // Ano atual/desejado
        "month": 5,   // Mês atual/desejado
        "day": 28,    // Dia atual/desejado
        "hour": 12,   // Hora atual/desejada
        "minute": 0,  // Minuto atual/desejado
        "latitude": -23.5505,
        "longitude": -46.6333,
        "tz_str": "America/Sao_Paulo"
    }
    ```
*   **Resposta (JSON):**
    *   Lista de planetas com suas posições (signo, grau, longitude, velocidade, retrogradação), similar às posições planetárias do mapa natal.

**3.3. Trânsitos sobre o Mapa Natal (Transits to Natal Chart)**

*   **Endpoint:** `POST /api/v1/transits_to_natal`
*   **Descrição:** Calcula as posições dos planetas em trânsito e os aspectos que formam com os planetas do mapa natal.
*   **Corpo da Requisição (JSON):**
    ```json
    {
        "natal_data": {
            "year": 1990,
            "month": 7,
            "day": 15,
            "hour": 14,
            "minute": 30,
            "latitude": -23.5505,
            "longitude": -46.6333,
            "tz_str": "America/Sao_Paulo",
            "house_system": "Placidus"
        },
        "transit_data": {
            "year": 2025,
            "month": 6,
            "day": 10,
            "hour": 10,
            "minute": 0,
            "latitude": -23.5505, // Pode ser o mesmo local do natal ou diferente
            "longitude": -46.6333,
            "tz_str": "America/Sao_Paulo"
        }
    }
    ```
*   **Resposta (JSON):**
    *   Posições dos planetas em trânsito.
    *   Lista de aspectos entre planetas em trânsito e planetas natais (incluindo ASC e MC natais).
        *   Planeta em trânsito
        *   Planeta/Ponto natal
        *   Tipo de aspecto
        *   Orbe

**3.4. (Opcional) Geração de SVG do Mapa Natal**

*   **Endpoint:** `POST /api/v1/natal_chart_svg`
*   **Descrição:** Gera uma representação SVG de um mapa natal.
*   **Corpo da Requisição (JSON):** Idêntico ao de `/api/v1/natal_chart`.
*   **Resposta (JSON):**
    ```json
    {
        "svg_image": "<svg>...</svg>" // String contendo o código SVG do mapa
    }
    ```
    Ou, alternativamente, a API pode retornar a imagem SVG diretamente com o `Content-Type: image/svg+xml`.

## 4. Considerações Futuras (Fora do Escopo Inicial)

*   Cálculos de Progressões e Direções.
*   Sinastria detalhada (mapa composto, aspectos entre dois mapas).
*   Retornos Solares e Lunares.
*   Interpretações textuais (requereria um banco de dados de interpretações ou integração com LLM).
*   Suporte a diferentes Ayanamsas para astrologia sideral de forma mais explícita.
*   Endpoints para consulta de efemérides de um planeta específico ao longo do tempo.

## 5. Tecnologias Propostas

*   **Linguagem de Programação:** Python 3.9+
*   **Framework Web API:** FastAPI (preferido pela performance e auto-documentação com OpenAPI) ou Flask.
*   **Biblioteca Astrológica Principal:** Kerykeion (que utiliza `pyswisseph`).
*   **Tratamento de Datas/Horas:** Biblioteca `datetime` padrão do Python, `pytz` para fusos horários (Kerykeion já lida com isso internamente ao receber `tz_str`).
*   **Servidor de Aplicação:** Uvicorn (para FastAPI) ou Gunicorn (para Flask/FastAPI).

Este plano de arquitetura servirá como guia para as próximas fases de desenvolvimento.
