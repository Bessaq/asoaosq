from fastapi import APIRouter, Query
from typing import List, Dict, Any
from ..interpretations.text_search import simple_text_search

# Criar o router
router = APIRouter(
    prefix="/api/v1",
    tags=["Interpretations"],
)

@router.get("/interpret", response_model=List[Dict[str, Any]])
async def interpret_text(query: str = Query(..., title="Search Query", description="Text to search in interpretations")):
    """
    Realiza uma busca textual simples nos arquivos de interpretação e retorna os trechos encontrados.
    """
    results = simple_text_search(query)
    return results