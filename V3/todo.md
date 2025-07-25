- [X] Analisar o código Python fornecido (`pasted_content.txt`) para entender a estrutura e as funções existentes.
- [X] Extrair o conteúdo textual de todos os arquivos PDF de astrologia fornecidos.
    - [X] Priorizar o uso de `pdftotext` (do `poppler-utils`).
    - [ ] Avaliar a necessidade de OCR para PDFs baseados em imagem ou com layouts complexos (Arquivos problemáticos identificados: `PrevenirYCurarConLaAstrologiaMedica(HirsigHuguette).pdf`, `[EN]Candleburningmagicaspellbookofritualsforgoodandevil(AnnaRiva).pdf`, `[EN]DarkmoonLilithinAstrology(IvyGoldstein-Jacobson).pdf`).
    - [ ] Processar PDFs em diferentes idiomas (Português, Inglês, Espanhol) conforme indicado nos nomes dos arquivos e no código.
- [X] Preparar os dados extraídos para o treinamento do modelo.
    - [X] Limpar e pré-processar o texto (54 arquivos processados, 3 pulados).
    - [X] Aplicar a normalização de símbolos astrológicos conforme a função `process_astrological_symbols`.
    - [X] Estruturar os dados, possivelmente usando as categorias sugeridas no código ou a ontologia/grafo de conhecimento (Dados limpos e prontos na pasta `/home/ubuntu/processed_texts`).
- [X] Definir a arquitetura e o objetivo do modelo de IA (necessário esclarecimento com o usuário sobre o tipo de modelo e funcionalidade desejada no VSCode).
    - Objetivo: Responder perguntas e gerar interpretações astrológicas (mapa natal, trânsitos, médica, psique) com base nos livros, acessível via API. Gerar mapas SVG.
    - Arquitetura: RAG (Retrieval-Augmented Generation) integrado a uma API FastAPI (Pausado devido a limitações de recursos, substituído por busca simples a ser implementada posteriormente).
- [X] Analisar a estrutura do projeto FastAPI existente e os arquivos de API fornecidos (Documentação, main.py, natal_chart_router.py, transit_router.py analisados).
- [X] Integrar geração de SVG e mapas ao pipeline (Implementado `svg_chart_router.py`).
- [X] Expor endpoints via FastAPI (Atualizado `main.py` para incluir `svg_chart_router`).
- [X] Diagnosticar e ajustar integração Kerykeion SVG (Ajustado para usar `KerykeionChartSVG`).
- [X] Testar os endpoints da API localmente (SVG e outros - Teste inicial SVG OK).
- [X] Documentar todo o processo, incluindo a extração de dados, pré-processamento, implementação da API, geração de SVG e instruções de uso/integração.
- [ ] Implementar pipeline de busca simples e gerador de interpretação (Pausado, a ser retomado no final).
- [ ] Criar tutorial sobre a criação do índice vetorial FAISS (Pausado, a ser retomado no final).
- [X] Entregar o código finalizado, a API (se aplicável) e a documentação ao usuário.

## Próximos Passos (Atualizado em 31/05/2025)

- [ ] Unificar estrutura de diretórios conforme o plano de integração.
- [ ] Consolidar modelos Pydantic das três versões.
- [ ] Implementar sistema de tradução para múltiplos idiomas.
- [ ] Aprimorar a geração de SVG com mais opções de personalização.
- [ ] Desenvolver uma abordagem alternativa para interpretações textuais.
- [ ] Implementar testes unitários abrangentes.
- [ ] Atualizar a documentação da API.
