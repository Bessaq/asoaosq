# Checklist do Projeto de API de Astrologia

Este checklist resume o status das tarefas realizadas e pendentes no projeto.

**Fase 1: Configuração e Análise Inicial**

*   [X] Analisar código Python inicial fornecido (`pasted_content.txt`).
*   [X] Analisar arquivos PDF de astrologia fornecidos (anexos e link do Drive - link não acessível).
*   [X] Definir objetivo principal com o usuário: API para cálculos astrológicos (natal, trânsito), geração de SVG e interpretações baseadas nos livros.
*   [X] Definir arquitetura inicial: API FastAPI + Kerykeion + RAG (LangChain/FAISS) para interpretações.

**Fase 2: Processamento de Dados (Livros)**

*   [X] Extrair conteúdo textual dos PDFs usando `pdftotext`.
    *   Sucesso: 54 de 57 arquivos.
    *   Falha/Pulados: 3 arquivos (provavelmente imagem/OCR necessário).
*   [X] Limpar e pré-processar textos extraídos (remoção de ruídos, normalização básica).
*   [X] Salvar textos processados em `/home/ubuntu/processed_texts`.
*   [ ] **(Falhou/Pausado)** Criar índice vetorial FAISS para busca semântica (RAG).
    *   Tentativa 1: Falhou (Erro `Killed` - falta de memória RAM).
    *   Tentativa 2 (Otimizada - modelo menor, chunks menores, lotes): Interrompida manualmente a pedido do usuário para criar resumo. Mostrou progresso (processou >50% dos lotes) mas não concluída.

**Fase 3: Desenvolvimento da API FastAPI**

*   [X] Analisar estrutura do projeto FastAPI existente fornecido pelo usuário.
*   [X] Organizar estrutura do projeto (`/app`, `/app/api`, `models.py`, `security.py`, `main.py`).
*   [X] Implementar/Integrar router para cálculos de Mapa Natal (`natal_chart_router.py`).
*   [X] Implementar/Integrar router para cálculos de Trânsitos (`transit_router.py`).
*   [X] Implementar router para geração de Gráficos SVG (`svg_chart_router.py`).
    *   [X] Diagnosticar e corrigir problema de importação (`MakeSvgChart` vs `KerykeionChartSVG`).
    *   [X] Implementar endpoints `/svg_chart` e `/svg_chart_base64`.
*   [X] Implementar segurança básica com chave de API (`security.py`, `Depends(verify_api_key)`).
*   [X] Configurar `main.py` para incluir todos os routers e documentação OpenAPI.
*   [X] Instalar dependências (`fastapi`, `uvicorn`, `kerykeion`, `python-dotenv`, `langchain`, `faiss-cpu`, `sentence-transformers`, etc.).

**Fase 4: Testes e Validação**

*   [X] Testar inicialização do servidor FastAPI.
*   [X] Testar endpoint de geração de SVG (`/api/v1/svg_chart`) com dados de exemplo (Einstein) - Sucesso.
*   [ ] Testar endpoints de cálculo Natal (`/api/v1/natal_chart`) - *Não realizado explicitamente nesta sessão.*
*   [ ] Testar endpoints de cálculo Trânsito (`/api/v1/transit_chart`, `/api/v1/transits_to_natal`) - *Não realizado explicitamente nesta sessão.*
*   [ ] Testar endpoint de SVG Base64 (`/api/v1/svg_chart_base64`) - *Não realizado explicitamente nesta sessão.*

**Fase 5: Documentação e Entrega**

*   [X] Criar documentação da API (`astrology_api_documentation.md`).
*   [X] Criar tutorial sobre a criação do índice FAISS (`tutorial_faiss_index.md`).
*   [X] Compactar código da API (`astrology_api_code.zip`).
*   [X] Entregar código, documentação, textos processados e exemplos ao usuário.
*   [X] Criar este checklist (`project_checklist.md`).
*   [X] Criar Memory Bank do projeto (`project_memory_bank.md`).

**Fase 6: Próximos Passos / Tarefas Pendentes**

*   [ ] **Implementar Busca/Interpretação:**
    *   Opção A: Tentar novamente a criação do índice FAISS (requer ambiente com mais RAM ou otimizações adicionais).
    *   Opção B: Implementar busca textual simples nos arquivos processados como alternativa.
    *   Integrar a busca escolhida a um novo endpoint na API (ex: `/api/v1/interpret`).
*   [ ] **Testes Abrangentes:** Realizar testes mais completos em todos os endpoints da API (cálculos e SVG) com diferentes dados de entrada e casos de borda.
*   [ ] **Refinamento:** Melhorar tratamento de erros, logs, traduções no SVG, etc.
*   [ ] **Deployment (Opcional):** Se necessário, fazer deploy da API em um ambiente de produção.

