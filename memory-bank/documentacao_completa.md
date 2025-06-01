# Documentação Completa da API de Astrologia

## Visão Geral

A API de Astrologia é um sistema robusto para cálculos astrológicos, oferecendo funcionalidades para gerar mapas natais, calcular trânsitos planetários, analisar aspectos entre planetas e gerar representações visuais em SVG. O objetivo inicial também incluía a capacidade de responder a perguntas e gerar interpretações astrológicas com base em uma coleção de livros fornecida, utilizando técnicas de RAG (Retrieval-Augmented Generation). No entanto, devido a limitações de recursos no ambiente de execução durante a criação do índice vetorial (FAISS), essa funcionalidade foi temporariamente pausada e será substituída por uma busca textual mais simples em uma fase posterior.

A API é construída usando FastAPI e utiliza a biblioteca Kerykeion para os cálculos astrológicos e geração de gráficos.

## Funcionalidades Principais

1. **Cálculo de Mapas Natais**
   - Posições planetárias precisas
   - Cálculo de casas astrológicas
   - Ascendente e Meio do Céu
   - Nodos lunares e pontos especiais

2. **Cálculo de Trânsitos**
   - Posições planetárias atuais ou para datas específicas
   - Trânsitos em relação a mapas natais
   - Aspectos entre planetas em trânsito e planetas natais
   - Indicação de aspectos aplicativos ou separativos

3. **Personalização de Sistema de Casas**
   - Suporte para 12 sistemas de casas diferentes
   - Placidus, Koch, Equal, Whole Sign, entre outros
   - Configurável por requisição

4. **Geração de Gráficos SVG**
   - Representações visuais de mapas natais
   - Gráficos de trânsitos
   - Gráficos combinados (natal + trânsito)
   - Personalização de tema e idioma

5. **Suporte a Idiomas**
   - Inglês e Português
   - Tradução de nomes de signos, planetas e aspectos
   - Preservação dos termos originais para compatibilidade

6. **Interpretações Textuais**
   - Planetas em signos
   - Planetas em casas
   - Aspectos entre planetas
   - Trânsitos planetários

## Endpoints da API

Todos os endpoints estão sob o prefixo `/api/v1` e requerem uma chave de API válida no cabeçalho `X-API-KEY`.

### Mapas Natais

```
POST /api/v1/natal_chart
```

Calcula um mapa natal completo com posições planetárias, casas, ascendente e meio do céu.

**Parâmetros:**
```json
{
  "name": "Nome da pessoa",
  "year": 1990,
  "month": 1,
  "day": 1,
  "hour": 12,
  "minute": 0,
  "longitude": -46.63,
  "latitude": -23.55,
  "tz_str": "America/Sao_Paulo",
  "house_system": "Placidus",
  "language": "pt",
  "include_interpretations": false
}
```

**Resposta:**
```json
{
  "input_data": { ... },
  "planets": {
    "sun": {
      "name": "Sol",
      "name_original": "Sun",
      "longitude": 280.5,
      "latitude": 0.0,
      "sign": "Capricórnio",
      "sign_original": "Cap",
      "sign_num": 10,
      "house": 5,
      "retrograde": false
    },
    ...
  },
  "houses": {
    "house_1": {
      "number": 1,
      "sign": "Virgem",
      "sign_original": "Vir",
      "sign_num": 6,
      "longitude": 172.5
    },
    ...
  },
  "ascendant": {
    "longitude": 172.5,
    "sign": "Virgem",
    "sign_original": "Vir",
    "sign_num": 6
  },
  "midheaven": {
    "longitude": 98.2,
    "sign": "Câncer",
    "sign_original": "Can",
    "sign_num": 4
  },
  "house_system": "Placidus"
}
```

### Trânsitos Atuais

```
POST /api/v1/current_transits
```

Calcula as posições planetárias para uma data e hora específicas.

**Parâmetros:**
```json
{
  "year": 2025,
  "month": 5,
  "day": 28,
  "hour": 12,
  "minute": 0,
  "longitude": -46.63,
  "latitude": -23.55,
  "tz_str": "America/Sao_Paulo",
  "house_system": "Placidus",
  "language": "pt"
}
```

**Resposta:**
```json
{
  "input_data": { ... },
  "planets": {
    "sun": {
      "name": "Sol",
      "name_original": "Sun",
      "longitude": 67.8,
      "latitude": 0.0,
      "sign": "Gêmeos",
      "sign_original": "Gem",
      "sign_num": 3,
      "house": 10,
      "retrograde": false
    },
    ...
  },
  "house_system": "Placidus"
}
```

### Trânsitos em Relação a Mapa Natal

```
POST /api/v1/transits_to_natal
```

Calcula as posições planetárias em trânsito em relação a um mapa natal, incluindo aspectos.

**Parâmetros:**
```json
{
  "natal": {
    "name": "Nome da pessoa",
    "year": 1990,
    "month": 1,
    "day": 1,
    "hour": 12,
    "minute": 0,
    "longitude": -46.63,
    "latitude": -23.55,
    "tz_str": "America/Sao_Paulo",
    "house_system": "Placidus"
  },
  "transit": {
    "year": 2025,
    "month": 5,
    "day": 28,
    "hour": 12,
    "minute": 0,
    "longitude": -46.63,
    "latitude": -23.55,
    "tz_str": "America/Sao_Paulo",
    "house_system": "Placidus"
  },
  "language": "pt",
  "include_interpretations": true
}
```

**Resposta:**
```json
{
  "input_data": { ... },
  "natal_planets": { ... },
  "transit_planets": { ... },
  "aspects": [
    {
      "p1_name": "Sol",
      "p1_name_original": "Sun",
      "p1_owner": "Trânsito",
      "p2_name": "Lua",
      "p2_name_original": "Moon",
      "p2_owner": "Natal",
      "aspect": "Trígono",
      "aspect_original": "Trine",
      "orbit": 1.2,
      "aspect_degrees": 120.0,
      "diff": -1.2,
      "applying": true
    },
    ...
  ],
  "natal_house_system": "Placidus",
  "transit_house_system": "Placidus",
  "interpretations": {
    "transit_aspects": {
      "Sun_Trine_Moon": "Trânsito do Sol em trígono com a Lua natal traz um fluxo harmonioso de energia entre a consciência e as emoções. É um período favorável para expressão pessoal e conexão com a família, com equilíbrio entre razão e sentimento."
    }
  }
}
```

### Geração de Gráfico SVG

```
POST /api/v1/svg_chart
```

Gera um gráfico SVG para um mapa natal, trânsito ou combinação.

**Parâmetros:**
```json
{
  "natal_chart": {
    "name": "Nome da pessoa",
    "year": 1990,
    "month": 1,
    "day": 14,
    "hour": 11,
    "minute": 30,
    "longitude": 10.0,
    "latitude": 48.4,
    "tz_str": "Europe/Berlin",
    "house_system": "Placidus"
  },
  "transit_chart": {
    "year": 2025,
    "month": 5,
    "day": 28,
    "hour": 12,
    "minute": 0,
    "longitude": 10.0,
    "latitude": 48.4,
    "tz_str": "Europe/Berlin",
    "house_system": "Placidus"
  },
  "chart_type": "combined",
  "show_aspects": true,
  "language": "pt",
  "theme": "light"
}
```

**Resposta:**
Retorna o conteúdo SVG diretamente, com cabeçalho `Content-Type: image/svg+xml`.

### Geração de Gráfico SVG em Base64

```
POST /api/v1/svg_chart_base64
```

Gera um gráfico SVG e retorna como string base64, útil para incorporação em aplicações web.

**Parâmetros:**
Mesmos parâmetros do endpoint `/api/v1/svg_chart`.

**Resposta:**
```json
{
  "svg_base64": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI4MDAiIGhlaWdodD0iODAwIj4uLi48L3N2Zz4=",
  "data_uri": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI4MDAiIGhlaWdodD0iODAwIj4uLi48L3N2Zz4="
}
```

### Interpretações Textuais

```
POST /api/v1/interpret_natal_chart
```

Gera interpretações textuais para um mapa natal.

**Parâmetros:**
O objeto de resposta de `/api/v1/natal_chart`.

**Resposta:**
```json
{
  "interpretations": {
    "sun_sign": "O Sol em Capricórnio indica uma personalidade ambiciosa, responsável e disciplinada. Há uma necessidade de realização e reconhecimento social. Pessoas com Sol em Capricórnio tendem a ser perseverantes, práticas e possuem grande capacidade de organização.",
    "moon_sign": "A Lua em Câncer revela emoções profundas, protetoras e nostálgicas. Há uma forte necessidade emocional de segurança familiar e pertencimento. Pessoas com Lua em Câncer tendem a ser muito sensíveis e intuitivas.",
    "ascendant": "O Ascendente em Virgem confere uma aparência discreta, precisa e observadora. A primeira impressão é de uma pessoa analítica, organizada e prestativa. Há uma abordagem meticulosa e prática da vida, com atenção aos detalhes e busca de aperfeiçoamento.",
    "planets_in_houses": {
      "sun": "O Sol na quinta casa confere uma personalidade criativa, expressiva e dramática. Há uma forte necessidade de reconhecimento através da autoexpressão criativa. A pessoa tende a se destacar em atividades artísticas, recreativas ou relacionadas a crianças."
    },
    "aspects": { ... }
  }
}
```

```
POST /api/v1/interpret_transits
```

Gera interpretações textuais para trânsitos.

**Parâmetros:**
O objeto de resposta de `/api/v1/transits_to_natal`.

**Resposta:**
```json
{
  "interpretations": {
    "transit_aspects": {
      "Sun_Trine_Moon": "Trânsito do Sol em trígono com a Lua natal traz um fluxo harmonioso de energia entre a consciência e as emoções. É um período favorável para expressão pessoal e conexão com a família, com equilíbrio entre razão e sentimento."
    }
  }
}
```

```
GET /api/v1/interpretation/{category}/{element}/{position}
```

Retorna uma interpretação específica.

**Parâmetros:**
- `category`: Categoria da interpretação (planet_sign, planet_house, aspect, transit)
- `element`: Elemento astrológico (sun, moon, mercury, etc.)
- `position`: Posição (signo, casa, aspecto)

**Exemplo:**
```
GET /api/v1/interpretation/planet_sign/sun/Áries
```

**Resposta:**
```json
{
  "interpretation": "O Sol em Áries confere uma personalidade dinâmica, corajosa e pioneira. Há uma forte necessidade de autoafirmação e independência. Pessoas com Sol em Áries tendem a ser diretas, entusiasmadas e possuem iniciativa para começar novos projetos."
}
```

## Sistemas de Casas Suportados

A API suporta os seguintes sistemas de casas:

- **Placidus** (padrão): Sistema mais comum, baseado na divisão do tempo que leva para um ponto da eclíptica passar do horizonte ao meio-céu.
- **Koch**: Baseado na divisão do tempo que leva para um ponto da eclíptica passar do horizonte ao meridiano.
- **Porphyrius**: Sistema antigo que divide o espaço entre os quatro ângulos.
- **Regiomontanus**: Baseado na divisão do equador celeste.
- **Campanus**: Baseado na divisão do primeiro vertical.
- **Equal**: Casas de tamanho igual (30°) a partir do Ascendente.
- **Whole Sign**: Cada casa corresponde a um signo inteiro.
- **Alcabitus**: Sistema medieval baseado na divisão do equador celeste.
- **Morinus**: Sistema que ignora a rotação da Terra.
- **Horizontal**: Baseado no horizonte local.
- **Topocentric**: Variação do sistema Placidus.
- **Vehlow**: Variação do sistema Equal com deslocamento de 5°.

## Suporte a Idiomas

A API suporta os seguintes idiomas:

- **Inglês (en)**: Nomes de signos, planetas e aspectos em inglês.
- **Português (pt)** (padrão): Nomes de signos, planetas e aspectos traduzidos para português.

## Instalação e Configuração

### Requisitos

- Python 3.8+
- FastAPI
- Uvicorn
- Kerykeion

### Instalação

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

### Execução

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

A documentação interativa estará disponível em `http://localhost:8000/docs`.

## Exemplos de Uso

### Python

```python
import requests
import json

# Calcular mapa natal
natal_data = {
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
    "include_interpretations": True
}

response = requests.post("http://localhost:8000/api/v1/natal_chart", json=natal_data)
natal_chart = response.json()

# Salvar o resultado em um arquivo
with open("einstein_natal_chart.json", "w", encoding="utf-8") as f:
    json.dump(natal_chart, f, ensure_ascii=False, indent=2)

print(f"Sol em {natal_chart['planets']['sun']['sign']}")
print(f"Ascendente em {natal_chart['ascendant']['sign']}")

# Gerar gráfico SVG
svg_data = {
    "natal_chart": natal_data,
    "chart_type": "natal",
    "language": "pt",
    "theme": "light"
}

response = requests.post(
    "http://localhost:8000/api/v1/svg_chart",
    json=svg_data,
    headers={"Accept": "image/svg+xml"}
)

# Salvar o SVG em um arquivo
with open("einstein_chart.svg", "wb") as f:
    f.write(response.content)

print("Gráfico SVG salvo em einstein_chart.svg")
```

### JavaScript

```javascript
// Calcular mapa natal
const natalData = {
  name": "Albert Einstein",
  year": 1879,
  month": 3,
  day": 14,
  hour": 11,
  minute": 30,
  longitude": 10.0,
  latitude": 48.4,
  tz_str": "Europe/Berlin",
  house_system": "Placidus",
  language": "pt",
  include_interpretations": true
};

fetch("http://localhost:8000/api/v1/natal_chart", {
  method": "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body": JSON.stringify(natalData)
})
.then(response => response.json())
.then(data => {
  console.log(`Sol em ${data.planets.sun.sign}`);
  console.log(`Ascendente em ${data.ascendant.sign}`);
  
  // Exibir interpretação
  if (data.interpretations && data.interpretations.sun_sign) {
    console.log(`Interpretação do Sol: ${data.interpretations.sun_sign}`);
  }
})
.catch(error => console.error("Erro:", error));

// Gerar gráfico SVG em base64
const svgData = {
  natal_chart": natalData,
  chart_type": "natal",
  language": "pt",
  theme": "light"
};

fetch("http://localhost:8000/api/v1/svg_chart_base64", {
  method": "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body": JSON.stringify(svgData)
})
.then(response => response.json())
.then(data => {
  // Incorporar o SVG em uma página HTML
  const img = document.createElement("img");
  img.src = data.data_uri;
  document.body.appendChild(img);
})
.catch(error => console.error("Erro:", error));
```

## Considerações Técnicas

### Precisão dos Cálculos

A API utiliza a biblioteca Kerykeion, que por sua vez é baseada no Swiss Ephemeris, garantindo alta precisão nos cálculos astrológicos. As posições planetárias são calculadas com precisão de segundos de arco, e os pontos angulares (Ascendente, Meio do Céu) com precisão de minutos de arco.

### Limitações

- A API não suporta cálculos para datas muito antigas (anteriores a 1800) ou muito futuras (posteriores a 2400) com a mesma precisão.
- Algumas interpretações textuais podem ser genéricas e devem ser complementadas com análise astrológica profissional.
- A geração de SVG pode variar ligeiramente dependendo do navegador ou visualizador utilizado.

### Desempenho

- Os cálculos astrológicos são relativamente rápidos, mas a geração de SVG pode ser mais intensiva em recursos.
- Considere implementar cache para requisições frequentes, especialmente para gráficos SVG.

## Próximos Passos e Melhorias Futuras

1. **Expansão das Interpretações**
   - Adicionar interpretações mais detalhadas e específicas
   - Incluir interpretações para padrões planetários (T-quadrados, Yods, etc.)
   - Suporte para interpretações em mais idiomas

2. **Funcionalidades Adicionais**
   - Cálculo de progressões secundárias
   - Cálculo de revoluções solares
   - Análise de compatibilidade (sinastria)
   - Previsões astrológicas baseadas em ciclos planetários

3. **Melhorias Técnicas**
   - Implementação de cache para melhorar desempenho
   - Suporte para exportação em mais formatos (PDF, PNG)
   - API GraphQL para consultas mais flexíveis

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias, correções ou novas funcionalidades.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

---

Desenvolvido com ❤️ pela equipe de Astrologia API.
