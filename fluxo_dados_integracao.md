# Planejamento do Fluxo de Dados e Integração com Bibliotecas Externas

Este documento detalha o fluxo de dados dentro da API de Astrologia e a integração com a biblioteca Kerykeion (que utiliza Swiss Ephemeris internamente).

## 1. Visão Geral da Integração com Kerykeion

A biblioteca Kerykeion será o principal motor para os cálculos astrológicos. A API atuará como uma camada de interface, recebendo dados do usuário, passando-os para Kerykeion de forma estruturada, e formatando os resultados de Kerykeion para a resposta JSON da API.

**Principais Objetos Kerykeion a serem utilizados:**
- `AstrologicalSubject`: Para criar um perfil astrológico de uma pessoa ou de um momento (para trânsitos).
- `KerykeionChartSVG`: Para a geração de gráficos SVG (funcionalidade opcional).
- Funções e atributos dos objetos acima para obter posições planetárias, cúspides, aspectos, etc.

## 2. Fluxo de Dados por Endpoint

**2.1. Endpoint: `POST /api/v1/natal_chart`**

1.  **Recebimento da Requisição:** A API recebe uma requisição POST com dados JSON contendo `name`, `year`, `month`, `day`, `hour`, `minute`, `latitude`, `longitude`, `tz_str`, e opcionalmente `house_system`.
2.  **Validação de Entrada:**
    *   Verificar se todos os campos obrigatórios estão presentes.
    *   Validar os tipos de dados (ex: `year` é inteiro, `latitude` é float).
    *   Validar os ranges (ex: `month` entre 1-12, `hour` entre 0-23).
    *   Validar `tz_str` (Kerykeion provavelmente fará isso, mas uma verificação prévia pode ser útil).
    *   Se `house_system` for fornecido, verificar se é um valor suportado por Kerykeion.
3.  **Interação com Kerykeion:**
    *   Instanciar `AstrologicalSubject`:
        ```python
        from kerykeion import AstrologicalSubject
        # ... obter dados da requisição ...
        sujeito_natal = AstrologicalSubject(
            name=dados_req.get("name", "NatalChart"),
            year=dados_req["year"],
            month=dados_req["month"],
            day=dados_req["day"],
            hour=dados_req["hour"],
            minute=dados_req["minute"],
            city="CustomLocation", # Kerykeion permite city como placeholder se lng/lat/tz_str são dados
            nation="",
            lng=dados_req["longitude"],
            lat=dados_req["latitude"],
            tz_str=dados_req["tz_str"],
            house_system=dados_req.get("house_system", "Placidus")
        )
        ```
4.  **Extração de Dados do Objeto Kerykeion:**
    *   **Planetas:** Iterar sobre `sujeito_natal.planets_list` (ou acessar individualmente: `sujeito_natal.sun`, `sujeito_natal.moon`, etc.). Para cada planeta, obter:
        *   `name`
        *   `sign`
        *   `sign_num` (para referência interna, se necessário)
        *   `position` (grau decimal no signo)
        *   `abs_pos` (longitude eclíptica absoluta)
        *   `house_name` (nome da casa)
        *   `speed`
        *   `retrograde` (boolean)
    *   **Cúspides das Casas:** Iterar sobre `sujeito_natal.houses_list_str` ou `sujeito_natal.houses_list_obj`. Para cada casa:
        *   `name` (ex: "First_House")
        *   `sign`
        *   `position` (grau decimal no signo)
    *   **Ascendente (ASC) e Meio do Céu (MC):**
        *   ASC: `sujeito_natal.first_house.sign`, `sujeito_natal.first_house.position`
        *   MC: `sujeito_natal.tenth_house.sign`, `sujeito_natal.tenth_house.position`
    *   **Aspectos:** Utilizar `sujeito_natal.get_all_aspects()` ou métodos similares para obter aspectos. Para cada aspecto:
        *   Planeta 1 (`name`)
        *   Planeta 2 (`name`)
        *   Tipo de aspecto (`name`, ex: "Conjunction")
        *   Orbe (`orbit`)
5.  **Formatação da Resposta JSON:** Construir o objeto JSON de resposta conforme definido na arquitetura, populando-o com os dados extraídos.
6.  **Envio da Resposta:** Retornar a resposta JSON com status 200 OK.

**2.2. Endpoint: `POST /api/v1/current_transits`**

1.  **Recebimento e Validação:** Similar ao `natal_chart`, mas para os dados do momento do trânsito (`year`, `month`, `day`, `hour`, `minute`, `latitude`, `longitude`, `tz_str`).
2.  **Interação com Kerykeion:**
    *   Instanciar `AstrologicalSubject` para o momento do trânsito:
        ```python
        sujeito_transito = AstrologicalSubject(
            name="CurrentTransits",
            year=dados_req["year"],
            # ... restante dos parâmetros ...
            lng=dados_req["longitude"],
            lat=dados_req["latitude"],
            tz_str=dados_req["tz_str"],
            house_system="Placidus" # Sistema de casas pode ser irrelevante aqui se só posições planetárias são desejadas
        )
        ```
3.  **Extração de Dados:** Obter as posições dos planetas (nome, signo, grau, longitude, velocidade, retrogradação) de `sujeito_transito`.
4.  **Formatação e Envio da Resposta:** Construir e enviar a resposta JSON com as posições planetárias.

**2.3. Endpoint: `POST /api/v1/transits_to_natal`**

1.  **Recebimento e Validação:** Receber `natal_data` e `transit_data`. Validar ambos os conjuntos de dados.
2.  **Interação com Kerykeion:**
    *   Criar `AstrologicalSubject` para os dados natais (`sujeito_natal`).
    *   Criar `AstrologicalSubject` para os dados de trânsito (`sujeito_transito`).
    *   Kerykeion tem funcionalidades para calcular aspectos entre dois `AstrologicalSubject` ou entre um `AstrologicalSubject` e um conjunto de posições de trânsito. Se Kerykeion não tiver uma função direta para "aspectos de trânsito para natal", pode ser necessário:
        *   Obter as posições planetárias natais.
        *   Obter as posições planetárias de trânsito.
        *   Implementar uma lógica para calcular aspectos entre esses dois conjuntos de posições (Kerykeion provavelmente tem funções de cálculo de aspecto que podem ser usadas aqui, como `kerykeion.aspects.Aspects`).
        *   Alternativamente, a classe `Synastry` do Kerykeion poderia ser adaptada ou suas lógicas internas de cálculo de aspecto entre dois mapas poderiam ser reutilizadas, tratando o mapa de trânsito como o "segundo" mapa.
        *   **Nota:** A documentação do Kerykeion menciona `TransitChart` na geração de SVG, o que implica que ele tem a lógica para lidar com trânsitos. A classe `KerykeionChartSVG(subject, 
