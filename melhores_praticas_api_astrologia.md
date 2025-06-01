## Pesquisa de Melhores Práticas em APIs Astrológicas

Esta seção documenta as melhores práticas e padrões observados em APIs de astrologia existentes, que servirão de base para o design da nossa API.

### Exemplo Analisado: AstrologyAPI.com (https://www.astrologyapi.com/docs)

**Visão Geral:**
- AstrologyAPI.com se apresenta como uma plataforma "Astrology-as-a-Service".
- Oferece uma gama de cálculos astrológicos, horóscopos, interpretações, etc.
- Suporta tanto astrologia Védica (Indiana) quanto Ocidental.

**Convenções Gerais da API:**
- **URL Base:** `https://api.astrologyapi.com/v1/`
- **HTTPS:** Obrigatório para todas as requisições.
- **Convenções RESTful:** A API segue convenções RESTful sempre que possível.
- **Método HTTP Principal:** A maioria das operações é realizada via requisições `POST` sobre os recursos.
- **Formato de Dados:** Requisições e respostas são codificadas em `JSON`.

**Autenticação:**
- A documentação de referência principal não detalha imediatamente o método de autenticação na primeira página, mas APIs comerciais como esta geralmente usam chaves de API (API Keys) enviadas em cabeçalhos HTTP (ex: `Authorization: Bearer <SUA_CHAVE>` ou um cabeçalho customizado como `X-API-KEY`) ou como parâmetro de query. É comum que a chave seja obtida após registro e assinatura de um plano.
- No caso da AstrologyAPI.com, a autenticação é feita via `userId` e `apiKey` que são obtidos após o registro. Estes são passados no cabeçalho da requisição:
    ```
    Authorization: Basic base64_encode(userId:apiKey)
    ```

**Estrutura de Endpoints (Exemplos Inferidos da Navegação da Documentação):**
- A documentação é categorizada por tipo de astrologia (Indiana, Ocidental) e por funcionalidade (Horóscopos, Tarot, Relatórios PDF).
- **Astrologia Indiana API:**
    - `/western_horoscope` (apesar do nome, parece estar sob Indiana também, ou há sobreposição)
    - `/birth_details`
    - `/astro_details`
    - `/planets` (possivelmente para posições planetárias detalhadas)
    - `/kundli_matching` (para sinastria/compatibilidade)
    - Vários outros endpoints para Dashas, trânsitos (Gochar), relatórios específicos (Mangal Dosha, Kal Sarp, etc.).
- **Astrologia Ocidental API:**
    - `/western_chart_data/tropical` (para mapa tropical)
    - `/western_chart_data/sidereal` (para mapa sideral)
    - `/western_aspects/tropical`
    - `/western_aspects/sidereal`
    - `/houses_report/tropical`
    - `/houses_report/sidereal`
    - `/transit_relation/tropical`
    - `/transit_relation/sidereal`
- **Horóscopos API:**
    - `/daily_horoscope/sun_sign` (diário, semanal, mensal)
- **Tarot API:**
    - `/tarot_predictions`
- **PDF Report API:**
    - `/pdf_report/western`
    - `/pdf_report/vedic`

**Parâmetros Comuns de Requisição (POST body em JSON):**
- Para cálculos de mapa natal/pessoal:
    - `day`, `month`, `year`, `hour`, `min`
    - `lat` (latitude), `lon` (longitude)
    - `tzone` (fuso horário)
- Para trânsitos, geralmente são necessários os dados da pessoa e a data/hora do trânsito.
- Para compatibilidade, dados de duas pessoas.
- `lang` para especificar o idioma da resposta (quando aplicável para interpretações).

**Estrutura de Respostas (JSON):**
- As respostas são em JSON e variam conforme o endpoint.
- **Exemplo (Nascimento):** Pode incluir posições planetárias (signo, grau, casa, se retrógrado), posições das casas, aspectos, etc.
- **Exemplo (Horóscopo):** Texto interpretativo.
- Geralmente bem estruturado com chaves descritivas.

**SDKs e Exemplos de Código:**
- Fornecem exemplos de código em várias linguagens (JavaScript, cURL são visíveis inicialmente).
- Mencionam SDKs de código aberto para facilitar a integração.

**Recursos Adicionais:**
- **Postman Collection:** Disponibilizam uma coleção do Postman para testar a API.
- **Quickstart Guide:** Guia de início rápido.

**Considerações de Design Observadas:**
- **Modularidade:** Endpoints bem definidos para funcionalidades específicas (ex: `/birth_details`, `/western_aspects`).
- **Clareza nos Nomes:** Nomes de endpoints e parâmetros geralmente autoexplicativos.
- **Versionamento:** Uso de `/v1/` na URL base indica versionamento da API, o que é uma boa prática.
- **Suporte a Diferentes Tradições:** Clara separação ou indicação para astrologia Védica e Ocidental.
- **Foco em `POST`:** O uso predominante de `POST` mesmo para buscar dados pode ser uma escolha para lidar com corpos de requisição mais complexos ou para evitar que dados sensíveis (como data de nascimento completa) apareçam em URLs/logs de servidor (comum com `GET`). No entanto, `GET` é mais semanticamente correto para recuperação de dados que não alteram o estado no servidor.
- **Dados de Localização:** Requer latitude, longitude e fuso horário, o que é crucial para a precisão. A API provavelmente não faz a geocodificação (cidade para lat/lon) por si só, esperando esses dados já resolvidos.

**Outras APIs e Práticas Gerais (a serem pesquisadas e adicionadas):**
- [ ] Pesquisar outras APIs de astrologia (ex: Aztro API, JSON-time Astrology API, etc.) para comparar abordagens.
- [ ] Padrões de autenticação comuns (OAuth 2.0, API Keys).
- [ ] Rate limiting e cotas de uso.
- [ ] Formatos de data e hora (ISO 8601 é um padrão comum).
- [ ] Tratamento de erros (códigos de status HTTP e mensagens de erro em JSON).
- [ ] Documentação interativa (Swagger/OpenAPI).

Esta análise inicial da AstrologyAPI.com já fornece insights valiosos. A próxima etapa é complementar com outras APIs e padrões gerais de design de API RESTful.

