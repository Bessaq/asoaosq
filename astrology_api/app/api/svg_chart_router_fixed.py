"""
Router para os endpoints de geração de gráficos SVG.

Este módulo contém os endpoints relacionados à geração de gráficos astrológicos em formato SVG.
"""
from fastapi import APIRouter, HTTPException, Depends, Response
from typing import Dict, Optional, Any, Union
from kerykeion import AstrologicalSubject
import tempfile
import os
import base64

from ..schemas.models import SVGChartRequest, SVGChartBase64Response
from ..core.calculations import create_astrological_subject
from ..core.utils import validate_date, validate_timezone, validate_time
from ..security import verify_api_key
from ..svg.svg_generator_fixed import SVGChartGenerator

router = APIRouter(
    prefix="/api/v1",
    tags=["SVG Chart"],
    dependencies=[Depends(verify_api_key)],
)

@router.post("/svg_chart", 
    response_class=Response,
    responses={
        200: {"content": {"image/svg+xml": {}}, "description": "Retorna o gráfico SVG diretamente."},
        422: {"description": "Erro de validação nos dados de entrada."},
        500: {"description": "Erro interno ao gerar o gráfico."}
    })
async def generate_svg_chart(request: SVGChartRequest):
    """
    Gera um gráfico astrológico em formato SVG.
    
    Os tipos de gráficos suportados são:
    - natal: Apenas o mapa natal
    - transit: Apenas o mapa de trânsitos
    - combined: Mapa natal com trânsitos sobrepostos
    """
    try:
        # Validar dados do mapa natal
        natal_req = request.natal_chart
        validate_date(natal_req.year, natal_req.month, natal_req.day)
        validate_time(natal_req.hour, natal_req.minute)
        validate_timezone(natal_req.tz_str)

        # Converter house_system para string
        house_system_str = str(natal_req.house_system) if natal_req.house_system else "Placidus"
        
        # Criar subject para o mapa natal
        natal_subject = create_astrological_subject(
            name=natal_req.name if natal_req.name else "NatalChart",
            year=natal_req.year,
            month=natal_req.month,
            day=natal_req.day,
            hour=natal_req.hour,
            minute=natal_req.minute,
            longitude=natal_req.longitude,
            latitude=natal_req.latitude,
            tz_str=natal_req.tz_str,
            house_system=house_system_str
        )

        # Criar subject para trânsitos se necessário
        transit_subject = None
        if request.transit_chart and request.chart_type in ["transit", "combined"]:
            trans_req = request.transit_chart
            validate_date(trans_req.year, trans_req.month, trans_req.day)
            validate_time(trans_req.hour, trans_req.minute)
            validate_timezone(trans_req.tz_str)

            transit_system_str = str(trans_req.house_system) if trans_req.house_system else "Placidus"
            
            transit_subject = create_astrological_subject(
                name="Transit",
                year=trans_req.year,
                month=trans_req.month,
                day=trans_req.day,
                hour=trans_req.hour,
                minute=trans_req.minute,
                longitude=trans_req.longitude,
                latitude=trans_req.latitude,
                tz_str=trans_req.tz_str,
                house_system=transit_system_str
            )

        # Criar o gerador de SVG
        svg_generator = SVGChartGenerator(natal_subject, transit_subject)

        # Gerar o SVG
        svg_content = svg_generator.generate_svg(
            chart_type=request.chart_type,
            show_aspects=request.show_aspects,
            language=request.language,
            theme=request.theme
        )

        # Retornar o SVG
        return Response(
            content=svg_content,
            media_type="image/svg+xml",
            headers={"Content-Disposition": f"inline; filename=chart_{natal_req.name or 'astrology'}.svg"}
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/svg_chart_base64", 
    response_model=SVGChartBase64Response,
    summary="Gera gráfico SVG em Base64",
    description="Gera um gráfico SVG e retorna como string base64, útil para incorporação em aplicações web.")
async def generate_svg_chart_base64(request: SVGChartRequest):
    """
    Gera um gráfico SVG e retorna como string base64.
    Útil para clientes que precisam incorporar o SVG em páginas web ou outros documentos.
    """
    try:
        # Primeiro gera o SVG normal
        svg_response = await generate_svg_chart(request)
        
        # Verifica se a resposta é do tipo Response
        if not isinstance(svg_response, Response):
            raise HTTPException(status_code=500, detail="Falha ao gerar SVG base.")
            
        # Converter para Base64
        svg_content_bytes = svg_response.body
        base64_svg = base64.b64encode(svg_content_bytes).decode('utf-8')
        
        # Retornar resposta formatada
        return SVGChartBase64Response(
            svg_base64=base64_svg,
            data_uri=f"data:image/svg+xml;base64,{base64_svg}"
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao converter SVG para Base64: {str(e)}")
