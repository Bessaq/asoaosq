"""
Módulo para busca de texto e interpretações astrológicas.
"""
import os
import re
import math
import json
from collections import Counter
from typing import Dict, List, Any, Optional, Tuple
from ..schemas.models import LanguageType

from ..interpretations.translations import translate_astrological_text

# Diretório onde os textos processados estão armazenados
PROCESSED_TEXTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "processed_texts")

# Cache para armazenar documentos já processados
DOCUMENT_CACHE = {}
TF_IDF_INDEX = None
DOCUMENT_PARAGRAPHS = {}

def preprocess_text(text: str) -> List[str]:
    """
    Pré-processa um texto, dividindo-o em tokens.
    
    Args:
        text (str): Texto a ser pré-processado.
        
    Returns:
        List[str]: Lista de tokens.
    """
    # Converter para minúsculas
    text = text.lower()
    
    # Remover caracteres especiais e dividir em tokens
    tokens = re.findall(r'\b\w+\b', text)
    
    # Remover stopwords simples (artigos, preposições, etc.)
    stopwords = {'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas', 'e', 'de', 'do', 'da', 'dos', 'das', 'em', 'no', 'na', 'nos', 'nas', 'por', 'para', 'com', 'que', 'se', 'the', 'and', 'of', 'to', 'in', 'is', 'for', 'with', 'by', 'on', 'at', 'from', 'an', 'this', 'that', 'these', 'those'}
    tokens = [token for token in tokens if token not in stopwords and len(token) > 1]
    
    return tokens

def build_tf_idf_index() -> Tuple[Dict[str, Dict[str, float]], Dict[str, List[str]]]:
    """
    Constrói um índice TF-IDF para os documentos processados.
    
    Returns:
        Tuple[Dict[str, Dict[str, float]], Dict[str, List[str]]]: 
            Índice TF-IDF e dicionário de parágrafos por documento.
    """
    global TF_IDF_INDEX, DOCUMENT_PARAGRAPHS
    
    if TF_IDF_INDEX is not None:
        return TF_IDF_INDEX, DOCUMENT_PARAGRAPHS
    
    # Verificar se o diretório de textos processados existe
    if not os.path.exists(PROCESSED_TEXTS_DIR):
        TF_IDF_INDEX = {}
        DOCUMENT_PARAGRAPHS = {}
        return TF_IDF_INDEX, DOCUMENT_PARAGRAPHS
    
    # Índice invertido: termo -> documento -> frequência
    index = {}
    document_terms = {}
    paragraphs_by_doc = {}
    
    # Processar documentos
    doc_count = 0
    for filename in os.listdir(PROCESSED_TEXTS_DIR):
        if not filename.endswith(".txt"):
            continue
        
        filepath = os.path.join(PROCESSED_TEXTS_DIR, filename)
        doc_id = filename
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Dividir em parágrafos
                paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
                paragraphs_by_doc[doc_id] = paragraphs
                
                # Processar cada parágrafo como um "subdocumento"
                for i, paragraph in enumerate(paragraphs):
                    sub_doc_id = f"{doc_id}:{i}"
                    DOCUMENT_CACHE[sub_doc_id] = paragraph
                    
                    # Pré-processar texto
                    tokens = preprocess_text(paragraph)
                    
                    # Calcular frequência dos termos
                    term_freq = Counter(tokens)
                    document_terms[sub_doc_id] = term_freq
                    
                    # Atualizar índice invertido
                    for term, freq in term_freq.items():
                        if term not in index:
                            index[term] = {}
                        index[term][sub_doc_id] = freq
                
                doc_count += 1
        except Exception as e:
            print(f"Erro ao processar arquivo {filename}: {str(e)}")
    
    # Calcular IDF e TF-IDF
    tf_idf_index = {}
    for term, docs in index.items():
        # IDF = log(N / df)
        idf = math.log(doc_count / len(docs))
        
        for doc_id, freq in docs.items():
            # Normalizar TF
            tf = freq / sum(document_terms[doc_id].values())
            
            # TF-IDF
            tf_idf = tf * idf
            
            if doc_id not in tf_idf_index:
                tf_idf_index[doc_id] = {}
            
            tf_idf_index[doc_id][term] = tf_idf
    
    TF_IDF_INDEX = tf_idf_index
    DOCUMENT_PARAGRAPHS = paragraphs_by_doc
    
    return tf_idf_index, paragraphs_by_doc

def advanced_text_search(query: str, limit: int = 5, min_score: float = 0.1) -> List[Dict[str, Any]]:
    """
    Realiza uma busca avançada de texto nos livros processados usando TF-IDF.
    
    Args:
        query (str): Consulta de busca.
        limit (int, opcional): Número máximo de resultados. Padrão é 5.
        min_score (float, opcional): Pontuação mínima para incluir um resultado. Padrão é 0.1.
        
    Returns:
        List[Dict[str, Any]]: Lista de resultados da busca.
    """
    # Construir índice TF-IDF (ou recuperar do cache)
    tf_idf_index, paragraphs_by_doc = build_tf_idf_index()
    
    if not tf_idf_index:
        return []
    
    # Pré-processar a consulta
    query_tokens = preprocess_text(query)
    
    if not query_tokens:
        return []
    
    # Pontuar documentos
    scores = {}
    for doc_id, terms in tf_idf_index.items():
        score = 0
        for token in query_tokens:
            if token in terms:
                score += terms[token]
        
        if score > min_score:
            scores[doc_id] = score
    
    # Ordenar por pontuação
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Preparar resultados
    results = []
    for doc_id, score in sorted_docs[:limit]:
        # Extrair informações do doc_id (formato: "filename:paragraph_index")
        parts = doc_id.split(":")
        filename = parts[0]
        paragraph_index = int(parts[1])
        
        # Recuperar parágrafo
        paragraph = DOCUMENT_CACHE.get(doc_id, "")
        
        # Destacar termos da consulta no parágrafo
        highlighted = paragraph
        for token in query_tokens:
            pattern = re.compile(r'\b' + re.escape(token) + r'\b', re.IGNORECASE)
            highlighted = pattern.sub(f"**{token.upper()}**", highlighted)
        
        # Adicionar resultado
        results.append({
            "source": filename,
            "score": score,
            "paragraph": paragraph,
            "highlighted": highlighted,
            "matched_terms": [token for token in query_tokens if token.lower() in paragraph.lower()]
        })
    
    return results

def simple_text_search(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Realiza uma busca simples de texto nos livros processados.
    Mantida por compatibilidade, internamente usa advanced_text_search.
    
    Args:
        query (str): Consulta de busca.
        limit (int, opcional): Número máximo de resultados. Padrão é 5.
        
    Returns:
        List[Dict[str, Any]]: Lista de resultados da busca.
    """
    results = advanced_text_search(query, limit)
    
    # Converter para o formato antigo
    simple_results = []
    for result in results:
        simple_results.append({
            "source": result["source"],
            "matched_terms": result["matched_terms"],
            "paragraphs": [result["paragraph"]]
        })
    
    return simple_results

def get_planet_interpretation(planet_name: str, sign: str, house: int, language: LanguageType = "pt") -> Optional[str]:
    """
    Busca a interpretação para um planeta em um signo e casa.
    
    Args:
        planet_name (str): Nome do planeta
        sign (str): Nome do signo
        house (int): Número da casa
        language (LanguageType): Idioma da interpretação. Defaults to "pt".
    
    Returns:
        Optional[str]: Interpretação encontrada ou None se não houver
    """
    # Formar a consulta
    query = f"{planet_name} in {sign} in house {house}"
    
    # Buscar documentos relevantes
    results = search_documents(query)
    if not results:
        return None
        
    # Pegar o resultado mais relevante
    best_match = results[0]
    
    # Traduzir se necessário
    if language != "en":
        best_match = translate_astrological_text(best_match, language)
    
    return best_match

def get_sign_interpretation(sign: str, language: str = "pt") -> Optional[Dict[str, Any]]:
    """
    Busca interpretações para um signo específico.
    
    Args:
        sign (str): Nome do signo.
        language (str, opcional): Idioma para os textos. Padrão é "pt".
        
    Returns:
        Optional[Dict[str, Any]]: Interpretação encontrada ou None.
    """
    # Construir a consulta
    query = f"signo de {sign} características"
    if language != "pt":
        sign_en = {
            "Áries": "Aries", "Touro": "Taurus", "Gêmeos": "Gemini", "Câncer": "Cancer",
            "Leão": "Leo", "Virgem": "Virgo", "Libra": "Libra", "Escorpião": "Scorpio",
            "Sagitário": "Sagittarius", "Capricórnio": "Capricorn", "Aquário": "Aquarius", "Peixes": "Pisces"
        }.get(sign, sign)
        
        query = f"{sign_en} sign characteristics"
    
    # Realizar a busca
    results = advanced_text_search(query, limit=1)
    
    if not results:
        return None
    
    result = results[0]
    
    # Traduzir para o idioma solicitado, se necessário
    if language != "pt" and language != "en":
        result["paragraph"] = translate_astrological_text(result["paragraph"], "en", language)
    
    return {
        "source": result["source"],
        "text": result["paragraph"],
        "relevance": result["score"]
    }

def get_house_interpretation(house: int, language: str = "pt") -> Optional[Dict[str, Any]]:
    """
    Busca interpretações para uma casa específica.
    
    Args:
        house (int): Número da casa.
        language (str, opcional): Idioma para os textos. Padrão é "pt".
        
    Returns:
        Optional[Dict[str, Any]]: Interpretação encontrada ou None.
    """
    # Construir a consulta
    query = f"casa {house} astrologia"
    if language != "pt":
        query = f"house {house} astrology"
    
    # Realizar a busca
    results = advanced_text_search(query, limit=1)
    
    if not results:
        return None
    
    result = results[0]
    
    # Traduzir para o idioma solicitado, se necessário
    if language != "pt" and language != "en":
        result["paragraph"] = translate_astrological_text(result["paragraph"], "en", language)
    
    return {
        "source": result["source"],
        "text": result["paragraph"],
        "relevance": result["score"]
    }

def get_aspect_interpretation(planet1: str, planet2: str, aspect: str, language: LanguageType = "pt") -> Optional[str]:
    """
    Busca a interpretação para um aspecto entre dois planetas.
    
    Args:
        planet1 (str): Nome do primeiro planeta
        planet2 (str): Nome do segundo planeta
        aspect (str): Nome do aspecto
        language (LanguageType): Idioma da interpretação. Defaults to "pt".
    
    Returns:
        Optional[str]: Interpretação encontrada ou None se não houver
    """
    # Formar a consulta
    query = f"{planet1} {aspect} {planet2}"
    
    # Buscar documentos relevantes
    results = search_documents(query)
    if not results:
        return None
        
    # Pegar o resultado mais relevante
    best_match = results[0]
    
    # Traduzir se necessário
    if language != "en":
        best_match = translate_astrological_text(best_match, language)
    
    return best_match

def get_transit_interpretation(transit_planet: str, natal_planet: str, aspect: str, language: str = "pt") -> Optional[Dict[str, Any]]:
    """
    Busca interpretações para um aspecto de trânsito.
    
    Args:
        transit_planet (str): Nome do planeta em trânsito.
        natal_planet (str): Nome do planeta natal.
        aspect (str): Nome do aspecto.
        language (str, opcional): Idioma para os textos. Padrão é "pt".
        
    Returns:
        Optional[Dict[str, Any]]: Interpretação encontrada ou None.
    """
    # Construir a consulta
    query = f"trânsito {transit_planet} {aspect} {natal_planet}"
    if language != "pt":
        # Traduzir para inglês
        transit_planet_en = {
            "Sol": "Sun", "Lua": "Moon", "Mercúrio": "Mercury", "Vênus": "Venus",
            "Marte": "Mars", "Júpiter": "Jupiter", "Saturno": "Saturn",
            "Urano": "Uranus", "Netuno": "Neptune", "Plutão": "Pluto",
            "Quíron": "Chiron", "Lilith": "Lilith"
        }.get(transit_planet, transit_planet)
        
        natal_planet_en = {
            "Sol": "Sun", "Lua": "Moon", "Mercúrio": "Mercury", "Vênus": "Venus",
            "Marte": "Mars", "Júpiter": "Jupiter", "Saturno": "Saturn",
            "Urano": "Uranus", "Netuno": "Neptune", "Plutão": "Pluto",
            "Quíron": "Chiron", "Lilith": "Lilith"
        }.get(natal_planet, natal_planet)
        
        aspect_en = {
            "Conjunção": "Conjunction", "Oposição": "Opposition",
            "Trígono": "Trine", "Quadratura": "Square", "Sextil": "Sextile"
        }.get(aspect, aspect)
        
        query = f"transit {transit_planet_en} {aspect_en} {natal_planet_en}"
    
    # Realizar a busca
    results = advanced_text_search(query, limit=1)
    
    if not results:
        return None
    
    result = results[0]
    
    # Traduzir para o idioma solicitado, se necessário
    if language != "pt" and language != "en":
        result["paragraph"] = translate_astrological_text(result["paragraph"], "en", language)
    
    return {
        "source": result["source"],
        "text": result["paragraph"],
        "relevance": result["score"]
    }

def get_natal_chart_interpretations(natal_data: Dict[str, Any], language: str = "pt") -> Dict[str, Any]:
    """
    Obtém interpretações para um mapa natal completo.
    
    Args:
        natal_data (Dict[str, Any]): Dados do mapa natal.
        language (str, opcional): Idioma para os textos. Padrão é "pt".
        
    Returns:
        Dict[str, Any]: Interpretações do mapa natal.
    """
    interpretations = {
        "planets": {},
        "houses": {},
        "aspects": []
    }
    
    # Interpretações dos planetas
    for planet_key, planet_data in natal_data["planets"].items():
        planet_name = planet_data["name"]
        sign = planet_data["sign"]
        house = planet_data["house"]
        
        interp = get_planet_interpretation(planet_name, sign, house, language)
        if interp:
            interpretations["planets"][planet_key] = interp
    
    # Interpretações das casas
    for house_key, house_data in natal_data["houses"].items():
        house_num = int(house_key)
        
        interp = get_house_interpretation(house_num, language)
        if interp:
            interpretations["houses"][house_key] = interp
    
    # Interpretações dos aspectos
    for aspect_data in natal_data["aspects"]:
        p1_name = aspect_data["p1_name"]
        p2_name = aspect_data["p2_name"]
        aspect = aspect_data["aspect"]
        
        interp = get_aspect_interpretation(p1_name, p2_name, aspect, language)
        if interp:
            interpretations["aspects"].append({
                "p1": p1_name,
                "p2": p2_name,
                                "aspect": aspect,
                "interpretation": interp
            })
    
    return interpretations
