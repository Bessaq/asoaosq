# Memory Bank: Projeto API de Astrologia

**Data:** 2025-05-31

**Objetivo deste Documento:** Servir como um resumo estratégico e guia de continuidade para este projeto, destinado a futuras IAs, desenvolvedores ou equipes que possam assumir ou dar seguimento ao trabalho. Ele detalha o escopo, progresso, desafios, decisões técnicas e recomendações, com foco especial em lidar com a base de conhecimento astrológica (livros).

## 1. Meta Principal do Projeto

Criar uma API robusta que forneça:

1.  **Cálculos Astrológicos Precisos:** Geração de dados para mapas natais e trânsitos planetários.
2.  **Visualização:** Geração de gráficos SVG personalizáveis para os mapas calculados.
3.  **Interpretação Fundamentada (Objetivo Original):** Capacidade de responder perguntas e gerar interpretações astrológicas (mapa natal, trânsitos, médica, psique, etc.) com base em uma extensa coleção de livros de astrologia fornecida pelo usuário.

## 2. Escopo e Funcionalidades

*   **Implementado e Funcional:**
    *   API FastAPI com estrutura modular (`/app`, `/app/api`).
    *   Endpoints para cálculo de Mapa Natal (`/api/v1/natal_chart`).
    *   Endpoints para cálculo de Trânsitos (`/api/v1/transit_chart`, `/api/v1/transits_to_natal`).
    *   Endpoints para geração de Gráficos SVG (`/api/v1/svg_chart`, `/api/v1/svg_chart_base64`) com opções de personalização (tipo, tema, idioma, aspectos).
    *   Segurança básica via chave de API (`X-API-KEY`).
    *   Extração e pré-processamento de texto de 54 livros PDF.
*   **Planejado / Parcialmente Implementado / Pausado:**
    *   **Base de Conhecimento Semântica (RAG/FAISS):** Tentativas de criar um índice vetorial FAISS para busca semântica nos livros falharam devido a limitações de memória RAM no ambiente de execução. Esta é a principal funcionalidade pendente para permitir interpretações *baseadas nos livros*.
    *   **Endpoint de Interpretação:** Um endpoint (ex: `/api/v1/interpret`) para receber perguntas ou dados de mapa e retornar interpretações baseadas na base de conhecimento.
    *   **Busca Textual Simples:** Alternativa à busca semântica, ainda não implementada.

## 3. Stack Tecnológico Principal

*   **Backend:** Python, FastAPI
*   **Cálculos Astrológicos & SVG:** Kerykeion (v4.26.2 utilizada)
*   **Processamento de Texto PDF:** `pdftotext` (do `poppler-utils`)
*   **Busca Semântica (Tentativa):** LangChain, FAISS (`faiss-cpu`), SentenceTransformers (`paraphrase-multilingual-MiniLM-L12-v2` e `paraphrase-multilingual-mpnet-base-v2`)
*   **Gerenciamento de Dependências:** pip
*   **Servidor:** Uvicorn
*   **Configuração:** python-dotenv

## 4. Pipeline de Processamento de Dados (Livros)

1.  **Entrada:** Coleção de livros de astrologia em PDF.
2.  **Extração:** Uso de `pdftotext` para converter PDF em texto puro (UTF-8).
    *   *Observação:* Falhou em 3 PDFs, indicando necessidade de OCR ou tratamento especial para PDFs baseados em imagem.
3.  **Limpeza:** Remoção de caracteres inválidos, excesso de espaços/linhas em branco.
4.  **Armazenamento Intermediário:** Textos limpos salvos em arquivos `.txt` individuais (`/home/ubuntu/processed_texts`).
5.  **Chunking:** Divisão dos textos em partes menores (chunks) usando `RecursiveCharacterTextSplitter` (testado com 1000/150 e 500/50 de tamanho/overlap).
6.  **Embedding (Tentativa):** Conversão dos chunks em vetores usando SentenceTransformers.
7.  **Indexação (Tentativa):** Armazenamento dos vetores em um índice FAISS para busca rápida por similaridade.

## 5. Desafio Principal: Criação do Índice Vetorial (FAISS)

*   **Problema:** O processo de criação do índice FAISS (`FAISS.from_documents` ou adição em lotes) consumiu mais memória RAM do que a disponível no ambiente de execução, resultando em interrupção do processo (`Killed` pelo OOM Killer do Linux).
*   **Causa:** Grande volume de texto (54 livros -> ~30k-55k chunks dependendo do tamanho) e a natureza intensiva em memória da vetorização e indexação.
*   **Tentativas Realizadas:**
    1.  **Abordagem Direta:** Usando `FAISS.from_documents` com modelo `mpnet-base` e chunks de 1000/150. Falhou.
    2.  **Abordagem Otimizada:** Usando modelo mais leve (`MiniLM`), chunks menores (500/50) e processamento em lotes (`vectorstore.add_documents()`). Mostrou progresso (processou >50% dos lotes) mas foi interrompida manualmente a pedido do usuário antes da conclusão ou falha.
*   **Status:** Funcionalidade de busca semântica (RAG) **não está operacional**. O índice FAISS não foi criado com sucesso.

## 6. Recomendações para Lidar com Grandes Volumes (Base de Conhecimento)

Para implementar com sucesso a busca semântica (RAG) com a coleção completa de livros (ou ainda maior):

1.  **Recursos Computacionais:**
    *   **RAM:** Prioridade máxima. É essencial executar o processo de indexação em um ambiente com memória RAM substancial (16GB, 32GB ou mais, dependendo do volume final). Monitorar o uso de memória durante o processo é crucial.
    *   **CPU:** Múltiplos cores aceleram o processamento de embeddings.
    *   **GPU (Opcional):** Usar uma GPU acelera *drasticamente* o cálculo de embeddings (requer `faiss-gpu` e instalação correta de CUDA/PyTorch com suporte a GPU).
2.  **Otimização do Processo de Indexação:**
    *   **Processamento em Lotes (Obrigatório):** Sempre processe e adicione documentos ao índice em lotes gerenciáveis (ex: 100-1000 chunks por vez). Ajuste o tamanho do lote conforme a memória disponível.
    *   **Limpeza de Memória:** Forçar a coleta de lixo (`gc.collect()`) após cada lote pode ajudar.
    *   **Modelos de Embedding:** Balancear qualidade e recursos. Modelos menores (`MiniLM`) são mais rápidos e usam menos RAM, mas podem ser ligeiramente menos precisos que modelos `base`.
    *   **Chunking Estratégico:** O tamanho e a sobreposição dos chunks afetam a qualidade da busca e o número de vetores. Testar diferentes estratégias pode ser necessário.
    *   **Bibliotecas Otimizadas:** Usar versões mais recentes e otimizadas das bibliotecas (FAISS, PyTorch, SentenceTransformers, LangChain).
3.  **Arquiteturas Alternativas de Banco de Vetores:**
    *   **Bancos de Vetores Dedicados:** Para volumes muito grandes ou necessidade de escalabilidade/gerenciamento, considerar bancos de dados vetoriais como Pinecone, Weaviate, Milvus, Qdrant. Eles oferecem soluções gerenciadas ou auto-hospedadas otimizadas para busca vetorial.
    *   **FAISS Persistido:** O FAISS pode ser salvo em disco e carregado posteriormente, mas a criação inicial ainda exige memória.
4.  **Pré-processamento e Filtragem:**
    *   Remover conteúdo irrelevante (índices, prefácios genéricos, bibliografias extensas) *antes* do chunking e embedding pode reduzir significativamente o tamanho do índice.
    *   Identificar e tratar PDFs problemáticos (OCR, extração manual de tabelas/imagens se necessário).

## 7. Guia para Continuidade (Próximos Passos Sugeridos)

1.  **Decidir sobre a Busca/Interpretação:**
    *   **Opção 1 (RAG Completo):** Tentar criar o índice FAISS novamente em um ambiente com mais RAM, aplicando as otimizações (lotes, modelo leve, etc.).
    *   **Opção 2 (Busca Simples):** Implementar uma busca textual (palavras-chave) nos arquivos `.txt` processados. Será mais rápido de implementar mas menos preciso.
2.  **Implementar a Busca Escolhida:** Criar a lógica de busca e um novo endpoint na API (ex: `/api/v1/interpret`) que use essa lógica para encontrar trechos relevantes dos livros.
3.  **Integração com LLM (se RAG):** Se o índice FAISS for criado, integrar a busca com um modelo de linguagem (como Gemini, GPT, etc.) para gerar as respostas finais fundamentadas.
4.  **Testes Abrangentes:** Testar *todos* os endpoints da API (cálculos, SVG, interpretação) com diversos cenários.
5.  **Refinamento:** Melhorar logs, tratamento de erros, adicionar mais opções de personalização (SVG, interpretações), etc.
6.  **Deployment:** Se necessário, preparar a API para deploy.

## 8. Considerações Finais

O projeto estabeleceu uma base sólida com a API FastAPI funcional para cálculos e geração de SVG. O principal obstáculo reside na implementação da base de conhecimento semântica devido a limitações de recursos. Superar esse desafio exigirá um ambiente mais robusto ou uma abordagem alternativa para a busca nos livros. A estrutura modular da API facilita a adição de novas funcionalidades ou a substituição de componentes (como o mecanismo de busca).

---
