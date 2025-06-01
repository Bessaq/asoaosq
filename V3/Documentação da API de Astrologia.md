# Documentação da API de Astrologia

## 1. Visão Geral

Esta API foi desenvolvida para fornecer funcionalidades astrológicas, incluindo o cálculo de mapas natais, trânsitos planetários e a geração de representações visuais desses mapas em formato SVG. O objetivo inicial também incluía a capacidade de responder a perguntas e gerar interpretações astrológicas com base em uma coleção de livros fornecida, utilizando técnicas de RAG (Retrieval-Augmented Generation). No entanto, devido a limitações de recursos no ambiente de execução durante a criação do índice vetorial (FAISS), essa funcionalidade foi temporariamente pausada e será substituída por uma busca textual mais simples em uma fase posterior.

A API é construída usando FastAPI e utiliza a biblioteca Kerykeion para os cálculos astrológicos e geração de gráficos.

## 2. Processamento de Dados (Livros de Astrologia)

- **Extração:** O conteúdo textual foi extraído de 54 dos 57 arquivos PDF fornecidos usando a ferramenta `pdftotext`. Três arquivos apresentaram problemas na extração (possivelmente PDFs baseados em imagem ou com codificação complexa) e foram pulados: `PrevenirYCurarConLaAstrologiaMedica(HirsigHuguette).pdf`, `[EN]Candleburningmagicaspellbookofritualsforgoodandevil(AnnaRiva).pdf`, `[EN]DarkmoonLilithinAstrology(IvyGoldstein-Jacobson).pdf`.
- **Limpeza:** Os textos extraídos foram limpos (remoção de caracteres estranhos, espaços extras) e normalizados.
- **Armazenamento:** Os textos processados foram salvos em arquivos `.txt` individuais na pasta `/home/ubuntu/processed_texts` (disponibilizada anteriormente como `processed_texts.zip`).
- **Índice Vetorial (Pausado):** A tentativa de criar um índice vetorial FAISS com `sentence-transformers` e `langchain` para busca semântica foi iniciada mas não pôde ser concluída devido a erros de falta de memória (`Killed`). Esta etapa é necessária para a funcionalidade de RAG e será abordada posteriormente, possivelmente com uma abordagem de busca mais simples ou com otimizações na criação do índice.

## 3. Estrutura da API

A API segue uma estrutura modular organizada em diretórios:

- `/home/ubuntu/astrology_api/`: Diretório raiz do projeto.
- `main.py`: Arquivo principal da aplicação FastAPI, onde a app é criada e os routers são incluídos.
- `app/`: Diretório contendo a lógica principal da aplicação.
  - `__init__.py`: Marca o diretório como um pacote Python.
  - `models.py`: Define os modelos Pydantic para as requisições e respostas da API.
  - `security.py`: Implementa a verificação de chave de API (X-API-KEY).
  - `api/`: Diretório contendo os routers para os diferentes endpoints.
    - `__init__.py`: Marca o diretório como um pacote Python.
    - `natal_chart_router.py`: Contém os endpoints relacionados ao cálculo de mapas natais.
    - `transit_router.py`: Contém os endpoints relacionados ao cálculo de trânsitos.
    - `svg_chart_router.py`: Contém os endpoints para a geração de gráficos SVG.

## 4. Endpoints da API

Todos os endpoints estão sob o prefixo `/api/v1` e requerem uma chave de API válida no cabeçalho `X-API-KEY`.

### 4.1. Cálculos Astrológicos (Natal e Trânsito)

*   **`POST /natal_chart`**: Calcula e retorna os dados detalhados de um mapa natal (planetas, casas, aspectos).
*   **`POST /transit_chart`**: Calcula e retorna os dados detalhados de posições planetárias para uma data/hora específica (trânsito).
*   **`POST /transits_to_natal`**: Calcula os aspectos entre planetas em trânsito e planetas natais.

*(Nota: Os detalhes exatos das respostas para estes endpoints podem ser verificados nos respectivos routers e modelos: `natal_chart_router.py`, `transit_router.py`, `models.py`)*

### 4.2. Geração de Gráficos SVG

Utiliza a classe `KerykeionChartSVG` da biblioteca Kerykeion.

*   **`POST /svg_chart`**: Gera e retorna um gráfico astrológico em formato SVG.
    *   **Requisição (`SVGChartRequest` em `models.py`):**
        *   `natal_chart`: Objeto `NatalChartRequest` com os dados do mapa base.
        *   `transit_chart` (Opcional): Objeto `TransitRequest` para gráficos de trânsito ou combinados.
        *   `chart_type`: Tipo de gráfico (`"natal"`, `"transit"`, `"combined"`). Default: `"natal"`.
        *   `show_aspects`: Booleano para mostrar ou ocultar linhas de aspecto. Default: `true`.
        *   `language`: Idioma para textos no gráfico (`"en"`, `"pt"`). Default: `"pt"`.
        *   `theme`: Tema de cores (`"light"`, `"dark"`). Default: `"light"`.
    *   **Resposta:** Conteúdo SVG (`image/svg+xml`).

*   **`POST /svg_chart_base64`**: Gera um gráfico SVG e retorna a representação em Base64.
    *   **Requisição:** Mesma que `/svg_chart`.
    *   **Resposta:** JSON com `svg_base64` (string) e `data_uri` (string).

### 4.3. Ajuste na Integração Kerykeion

Durante o desenvolvimento, foi identificado que a classe `MakeSvgChart` usada inicialmente não estava disponível na versão instalada do Kerykeion (4.26.2). A implementação foi ajustada para usar `KerykeionChartSVG`, que é a classe correta para geração de SVG nesta versão.

## 5. Como Executar a API Localmente

1.  **Estrutura de Arquivos:** Certifique-se de que os arquivos do projeto estão organizados conforme descrito na Seção 3.
2.  **Dependências:** Instale as dependências necessárias:
    ```bash
    pip install fastapi uvicorn[standard] kerykeion python-dotenv
    ```
3.  **Chave de API:** Crie um arquivo `.env` no diretório raiz (`/home/ubuntu/astrology_api/`) com o seguinte conteúdo, substituindo `sua_chave_secreta` por uma chave de sua escolha:
    ```
    API_KEY_KERYKEION=sua_chave_secreta
    ```
4.  **Executar o Servidor:** Navegue até o diretório raiz (`/home/ubuntu/astrology_api/`) e execute o Uvicorn:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```
    *(O `--reload` é opcional, útil durante o desenvolvimento)*
5.  **Acesso:** A API estará disponível em `http://localhost:8000`. A documentação interativa (Swagger UI) estará em `http://localhost:8000/docs`.

## 6. Como Usar a API (Exemplos com cURL)

Substitua `SUA_CHAVE_API` pela chave definida no arquivo `.env` e `URL_DA_API` pelo endereço onde a API está rodando (ex: `http://localhost:8000` ou a URL pública fornecida).

**Exemplo: Gerar SVG do Mapa Natal de Einstein**

```bash
curl -X POST "URL_DA_API/api/v1/svg_chart" \
-H "Content-Type: application/json" \
-H "X-API-KEY: SUA_CHAVE_API" \
-d 
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
    "house_system": "Placidus"
  },
  "chart_type": "natal",
  "show_aspects": true,
  "language": "pt",
  "theme": "dark"
}
 -o einstein_natal_dark.svg
```

**Exemplo: Gerar SVG Combinado (Natal + Trânsito) em Base64**

```bash
curl -X POST "URL_DA_API/api/v1/svg_chart_base64" \
-H "Content-Type: application/json" \
-H "X-API-KEY: SUA_CHAVE_API" \
-d 
  "natal_chart": {
    "name": "Pessoa Exemplo",
    "year": 1995,
    "month": 8,
    "day": 20,
    "hour": 14,
    "minute": 0,
    "longitude": -46.63,
    "latitude": -23.55,
    "tz_str": "America/Sao_Paulo"
  },
  "transit_chart": {
    "year": 2025,
    "month": 5,
    "day": 31,
    "hour": 17,
    "minute": 30,
    "longitude": -46.63,
    "latitude": -23.55,
    "tz_str": "America/Sao_Paulo"
  },
  "chart_type": "combined",
  "show_aspects": true,
  "language": "en",
  "theme": "light"
}

```
*(A resposta será um JSON contendo `svg_base64` e `data_uri`)*

## 7. Próximos Passos (Funcionalidades Pausadas)

- **Busca nos Livros:** Implementar um sistema de busca (provavelmente baseado em palavras-chave ou busca textual direta nos arquivos processados) para permitir a geração de interpretações baseadas nos livros.
- **Tutorial FAISS:** Criar um tutorial detalhado explicando o processo de criação do índice vetorial FAISS, os desafios encontrados e possíveis abordagens para tentar novamente com sucesso em um ambiente com mais recursos.

---
*Documentação gerada em: 2025-05-31*
