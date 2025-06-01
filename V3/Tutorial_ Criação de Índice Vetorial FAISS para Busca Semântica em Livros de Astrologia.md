# Tutorial: Criação de Índice Vetorial FAISS para Busca Semântica em Livros de Astrologia

## 1. Introdução: O que é e por que usar um Índice Vetorial?

O objetivo de criar um índice vetorial (neste caso, usando FAISS - Facebook AI Similarity Search) era permitir uma **busca semântica** avançada no conteúdo dos seus livros de astrologia. Diferente da busca por palavras-chave, a busca semântica entende o *significado* por trás das palavras.

Isso seria a base para um sistema de **RAG (Retrieval-Augmented Generation)**. Funciona assim:

1.  **Pergunta do Usuário:** Você faz uma pergunta sobre astrologia (ex: "Qual o significado de Saturno na casa 7?").
2.  **Busca (Retrieval):** O sistema converte sua pergunta em um vetor (uma representação numérica do significado) e usa o índice FAISS para encontrar os trechos dos livros que são semanticamente mais *semelhantes* à sua pergunta.
3.  **Geração (Generation):** Um modelo de linguagem (como eu) recebe sua pergunta original *junto* com os trechos relevantes encontrados nos livros.
4.  **Resposta Fundamentada:** O modelo gera uma resposta que combina seu conhecimento geral com as informações específicas encontradas nos seus livros, fornecendo uma interpretação mais precisa e contextualizada.

Sem o índice vetorial, a capacidade de "consultar" os livros de forma inteligente fica comprometida, limitando as respostas a informações genéricas ou exigindo uma busca textual mais simples (e menos precisa).

## 2. O Processo que Tentamos (Pipeline com LangChain)

Utilizamos a biblioteca LangChain para orquestrar o processo, que envolveu as seguintes etapas (conforme o script `build_vector_index.py`):

1.  **Carregamento dos Documentos:**
    *   Usamos `DirectoryLoader` do LangChain para carregar todos os arquivos `.txt` da pasta `/home/ubuntu/processed_texts` (que continham o texto extraído e limpo dos PDFs).
    *   Verificamos se os documentos não estavam vazios.

2.  **Divisão em Chunks (Partes Menores):**
    *   Textos longos são difíceis de processar para embeddings. Usamos `RecursiveCharacterTextSplitter` para dividir cada livro em partes menores (chunks) de 1000 caracteres, com uma sobreposição de 150 caracteres entre eles (para não perder contexto nas quebras).
    *   Isso resultou em aproximadamente 29.389 chunks de texto.

3.  **Criação de Embeddings (Vetores de Significado):**
    *   Esta é a etapa crucial onde o significado do texto é convertido em vetores numéricos.
    *   Utilizamos `SentenceTransformerEmbeddings` do LangChain, configurado para usar o modelo `paraphrase-multilingual-mpnet-base-v2`.
        *   **Por que este modelo?** É um modelo robusto e pré-treinado, otimizado para gerar embeddings de alta qualidade para múltiplos idiomas (incluindo português e inglês, presentes nos seus livros) e bom em capturar a similaridade semântica entre frases/parágrafos.
        *   Configuramos para rodar explicitamente na CPU (`device: "cpu"`).

4.  **Indexação com FAISS:**
    *   Usamos a integração `FAISS.from_documents` do LangChain. Esta função:
        *   Pega todos os chunks de texto.
        *   Usa o modelo de embedding (SentenceTransformer) para calcular o vetor de cada chunk.
        *   Constrói um índice FAISS eficiente que armazena esses vetores e permite buscas rápidas por similaridade.
    *   O plano era salvar este índice localmente na pasta `/home/ubuntu/astrology_faiss_index` para uso posterior pela API.

## 3. Desafios Encontrados: O Erro "Killed"

O processo de criação do índice falhou consistentemente em duas tentativas. O script começava a rodar, carregava os documentos, dividia em chunks, baixava e inicializava o modelo de embedding, e começava a processar os chunks para criar o índice FAISS. No entanto, após algum tempo processando os embeddings e construindo o índice, o processo era abruptamente interrompido pelo sistema operacional, resultando na mensagem `Killed` no terminal.

**Causa Provável:** Falta de Memória RAM.

*   **Alto Consumo de Memória:** O cálculo de embeddings para quase 30.000 chunks de texto e a construção de um índice FAISS para armazenar esses vetores (cada vetor tem centenas de dimensões) são operações que consomem muita memória RAM.
*   **Limitações do Ambiente:** O ambiente de execução (sandbox) onde o processo rodou possui recursos limitados (CPU e, principalmente, RAM). Quando um processo excede a memória disponível, o sistema operacional (Linux) utiliza o "OOM Killer" (Out-of-Memory Killer) para terminá-lo (`kill`) e evitar que o sistema inteiro trave.

## 4. Sugestões para Tentar Novamente (Com Ajustes)

Se você desejar tentar criar o índice FAISS novamente em um ambiente com mais recursos ou com algumas otimizações, considere:

1.  **Ambiente com Mais RAM:** A solução mais direta é executar o script `build_vector_index.py` em um computador ou servidor com significativamente mais memória RAM (ex: 16GB ou mais, dependendo do volume total de texto).

2.  **Processamento em Lotes (Batch Processing):** Modificar o script para processar os documentos e criar embeddings em lotes menores, adicionando-os incrementalmente ao índice FAISS (usando `vectorstore.add_documents()` em vez de `FAISS.from_documents` de uma vez só). Isso pode reduzir o pico de uso de memória.

3.  **Reduzir o Tamanho dos Chunks:** Experimentar chunks menores (ex: 500 caracteres com overlap de 50). Isso gera mais chunks, mas cada um exige menos processamento individualmente. Pode ou não ajudar com a memória, dependendo de como o FAISS e o SentenceTransformer gerenciam os dados.

4.  **Processar Menos Livros Inicialmente:** Começar criando um índice com um subconjunto dos livros (ex: 5 ou 10 livros) para validar o processo e depois adicionar os restantes incrementalmente.

5.  **Usar um Modelo de Embedding Menor:** Modelos como `paraphrase-multilingual-MiniLM-L12-v2` são menores e mais rápidos, consumindo menos recursos, embora possam ter uma ligeira perda na qualidade dos embeddings comparado ao `mpnet-base`.

6.  **Verificar Bibliotecas Otimizadas:** Embora tenhamos usado `faiss-cpu`, garantir que todas as dependências (como PyTorch, que é usado pelo SentenceTransformers) estejam usando versões otimizadas para CPU pode ajudar, mas o gargalo principal provavelmente ainda será a RAM.

7.  **Swap (Menos Ideal):** Configurar espaço de swap no sistema pode dar uma margem extra, mas o desempenho será muito degradado se o sistema depender muito do swap para operações de memória intensiva.

## 5. Alternativa: Busca Simples

Como a criação do índice falhou, a alternativa imediata para permitir alguma forma de consulta aos livros seria implementar uma busca textual simples:

*   **Método:** Ler os arquivos de texto processados (`/home/ubuntu/processed_texts`) e buscar por palavras-chave ou frases exatas da pergunta do usuário.
*   **Vantagens:** Muito mais leve em termos de recursos, não requer indexação prévia.
*   **Desvantagens:** Menos precisa, não entende sinônimos ou contexto (ex: buscar por "casa 7" não encontraria trechos que falam sobre "relacionamentos e parcerias" sem mencionar explicitamente "casa 7").

Esperamos que este tutorial esclareça o processo, os desafios e as opções para habilitar a busca inteligente nos seus livros de astrologia no futuro.
