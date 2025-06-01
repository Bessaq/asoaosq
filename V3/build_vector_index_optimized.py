#!/usr/bin/env python
# coding: utf-8

import os
import time
import gc
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader

# --- Configurações Otimizadas ---
PROCESSED_TEXTS_DIR = "/home/ubuntu/processed_texts"
FAISS_INDEX_PATH = "/home/ubuntu/astrology_faiss_index_optimized"
# Modelo de embedding mais leve
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
CHUNK_SIZE = 500 # Chunks menores
CHUNK_OVERLAP = 50 # Sobreposição menor
BATCH_SIZE = 500 # Processar N chunks por vez

# --- Funções Auxiliares ---
def load_documents(directory):
    """Carrega documentos de texto de um diretório."""
    print(f"Carregando documentos de: {directory}")
    loader = DirectoryLoader(directory, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"}, show_progress=True, use_multithreading=True)
    documents = loader.load()
    print(f"Total de documentos carregados: {len(documents)}")
    documents = [doc for doc in documents if doc.page_content.strip()]
    print(f"Documentos não vazios: {len(documents)}")
    return documents

def split_documents(documents):
    """Divide os documentos em chunks menores."""
    print(f"Dividindo documentos em chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = text_splitter.split_documents(documents)
    print(f"Total de chunks criados: {len(chunks)}")
    return chunks

def initialize_embeddings():
    """Inicializa o modelo de embedding."""
    print(f"Inicializando modelo de embedding: {EMBEDDING_MODEL}")
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": False} # Normalização pode ser feita pelo FAISS se necessário
    embeddings = SentenceTransformerEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return embeddings

def create_and_save_faiss_index_batched(chunks, embeddings, index_path):
    """Cria embeddings e salva o índice FAISS processando em lotes."""
    if not chunks:
        print("Nenhum chunk para processar.")
        return

    print(f"Criando índice FAISS em lotes de {BATCH_SIZE} chunks...")
    vectorstore = None
    total_chunks = len(chunks)
    start_time_total = time.time()

    for i in range(0, total_chunks, BATCH_SIZE):
        batch_chunks = chunks[i:min(i + BATCH_SIZE, total_chunks)]
        batch_num = (i // BATCH_SIZE) + 1
        print(f"\nProcessando lote {batch_num}/{ (total_chunks + BATCH_SIZE - 1) // BATCH_SIZE } (chunks {i+1}-{min(i + BATCH_SIZE, total_chunks)} de {total_chunks})...")
        start_time_batch = time.time()

        try:
            if vectorstore is None:
                # Cria o índice com o primeiro lote
                print("Inicializando índice FAISS com o primeiro lote...")
                vectorstore = FAISS.from_documents(batch_chunks, embeddings)
                print("Índice inicializado.")
            else:
                # Adiciona os lotes subsequentes ao índice existente
                print("Adicionando lote ao índice FAISS existente...")
                vectorstore.add_documents(batch_chunks)
                print("Lote adicionado.")

            end_time_batch = time.time()
            print(f"Lote {batch_num} processado em {end_time_batch - start_time_batch:.2f} segundos.")

        except Exception as e:
            print(f"Erro ao processar o lote {batch_num}: {e}")
            # Opcional: decidir se quer parar ou continuar com os próximos lotes
            # raise e # Descomente para parar em caso de erro
            print("Pulando para o próximo lote devido ao erro.")
            continue # Continua para o próximo lote
        finally:
             # Limpar memória após cada lote (pode ajudar)
             del batch_chunks
             gc.collect()
             time.sleep(1) # Pequena pausa

    if vectorstore:
        end_time_total = time.time()
        print(f"\nProcessamento de todos os lotes concluído em {end_time_total - start_time_total:.2f} segundos.")
        print(f"Salvando índice FAISS final em: {index_path}")
        vectorstore.save_local(index_path)
        print("Índice FAISS salvo com sucesso.")
    else:
        print("Nenhum índice FAISS foi criado devido a erros ou falta de chunks.")

# --- Execução Principal ---
if __name__ == "__main__":
    print("--- Iniciando criação OTIMIZADA do índice vetorial (lotes, modelo leve) ---")
    
    # 1. Carregar documentos
    docs = load_documents(PROCESSED_TEXTS_DIR)
    
    if not docs:
        print("Nenhum documento encontrado. Abortando.")
    else:
        # 2. Dividir em chunks (menores)
        doc_chunks = split_documents(docs)
        
        if not doc_chunks:
            print("Nenhum chunk foi criado. Abortando.")
        else:
            # 3. Inicializar embeddings (modelo mais leve)
            embeddings_model = initialize_embeddings()
            
            # 4. Criar e salvar índice FAISS em lotes
            create_and_save_faiss_index_batched(doc_chunks, embeddings_model, FAISS_INDEX_PATH)
            
    print("--- Processo de criação do índice OTIMIZADO concluído ---")

