"""
Router para os endpoints de geração de gráficos SVG.

DEPRECIADO: Este módulo está depreciado. Use svg_chart_router_fixed em vez disso.
Este módulo contém os endpoints relacionados à geração de gráficos astrológicos em formato SVG.
"""
# DEPRECIADO: Use svg_chart_router_fixed em vez disso.
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from typing import Dict, Optional, Any
from kerykeion import AstrologicalSubject, KerykeionChartSVG
import tempfile
import os
import base64

from ..schemas.models import SVGChartRequest, SVGChartBase64Response
from ..core.calculations import create_astrological_subject
from ..core.utils import validate_date, validate_timezone, validate_time
from ..security import verify_api_key

router = APIRouter(
    prefix="/api/v1",
    tags=["SVG Chart"],
    dependencies=[Depends(verify_api_key)],
)

def get_svg_content(chart: Any, temp_file: str) -> str:
    """
    Tenta obter o conteúdo SVG do gráfico de várias maneiras possíveis.
    
    Args:
        chart (Any): O objeto do gráfico
        temp_file (str): Caminho para o arquivo temporário
        
    Returns:
        str: Conteúdo SVG
        
    Raises:
        Exception: Se não for possível obter o conteúdo SVG
    """
    # Tentar métodos diretos primeiro
    if hasattr(chart, 'svg_string') and getattr(chart, 'svg_string'):
        return getattr(chart, 'svg_string')
    if hasattr(chart, 'svg') and getattr(chart, 'svg'):
        return getattr(chart, 'svg')
    if hasattr(chart, 'get_svg_string') and callable(getattr(chart, 'get_svg_string')):
        return getattr(chart, 'get_svg_string')()
    if hasattr(chart, 'get_svg') and callable(getattr(chart, 'get_svg')):
        return getattr(chart, 'get_svg')()
    if hasattr(chart, 'makeTemplate') and callable(getattr(chart, 'makeTemplate')):
        return getattr(chart, 'makeTemplate')()
        
    # Se nenhum método direto funcionar, tentar ler o arquivo
    try:
        if os.path.exists(temp_file):
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if content:
                    return content
    except Exception as e:
        raise Exception(f"Erro ao ler arquivo SVG: {str(e)}")
        
    raise Exception("Não foi possível obter o conteúdo SVG por nenhum método disponível")

@router.post("/svg_chart", 
    response_class=Response,
    responses={
        200: {"content": {"image/svg+xml": {}}, "description": "Retorna o gráfico SVG diretamente."},
        422: {"description": "Erro de validação nos dados de entrada."},
        500: {"description": "Erro interno ao gerar o gráfico."}
    })
async def generate_svg_chart(data: SVGChartRequest):
    """Gera um gráfico SVG para um mapa natal, trânsito ou combinação."""
    try:
        # Validar dados natais
        natal_req = data.natal_chart
        if not validate_date(natal_req.year, natal_req.month, natal_req.day):
            raise HTTPException(status_code=422, detail="Data natal inválida")
        if not validate_time(natal_req.hour, natal_req.minute):
            raise HTTPException(status_code=422, detail="Hora natal inválida")
        if not validate_timezone(natal_req.tz_str):
            raise HTTPException(status_code=422, detail="Fuso horário natal inválido")
            
        natal_subject = create_astrological_subject(
            name=natal_req.name or "Natal Chart",
            year=natal_req.year,
            month=natal_req.month,
            day=natal_req.day,
            hour=natal_req.hour,
            minute=natal_req.minute,
            longitude=natal_req.longitude,
            latitude=natal_req.latitude,
            tz_str=natal_req.tz_str,
            house_system=natal_req.house_system
        )
        
        # Validar e criar objeto de trânsito se necessário
        transit_subject = None
        if data.transit_chart and data.chart_type in ["transit", "combined"]:
            transit_req = data.transit_chart
            if not validate_date(transit_req.year, transit_req.month, transit_req.day):
                raise HTTPException(status_code=422, detail="Data de trânsito inválida")
            if not validate_time(transit_req.hour, transit_req.minute):
                raise HTTPException(status_code=422, detail="Hora de trânsito inválida")
            if not validate_timezone(transit_req.tz_str):
                raise HTTPException(status_code=422, detail="Fuso horário de trânsito inválido")
                
            transit_subject = create_astrological_subject(
                name="Transit",
                year=transit_req.year,
                month=transit_req.month,
                day=transit_req.day,
                hour=transit_req.hour,
                minute=transit_req.minute,
                longitude=transit_req.longitude,
                latitude=transit_req.latitude,
                tz_str=transit_req.tz_str,
                house_system=transit_req.house_system
            )
        
        # Criar diretório temporário para o SVG
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = os.path.join(temp_dir, "chart.svg")
            
            # Configurar e gerar o gráfico
            chart_params = {
                "new_output_directory": temp_dir,
                "filename": "chart.svg"
            }
            
            # Adicionar configurações de tema
            if data.theme == "dark":
                chart_params["black_bg"] = True
            
            # Criar o gráfico com base no tipo
            if data.chart_type == "natal":
                chart = KerykeionChartSVG(natal_subject, **chart_params)
            elif data.chart_type == "transit" and transit_subject:
                chart = KerykeionChartSVG(transit_subject, **chart_params)
            elif data.chart_type == "combined" and transit_subject:
                chart_params["second_obj"] = transit_subject
                chart = KerykeionChartSVG(natal_subject, **chart_params)
            else:
                raise HTTPException(
                    status_code=422,
                    detail=(f"Dados de trânsito necessários para o tipo de gráfico '{data.chart_type}'"
                           if data.chart_type in ["transit", "combined"]
                           else "Tipo de gráfico inválido")
                )
            
            # Configurar aspectos
            if not data.show_aspects:
                try:
                    if hasattr(chart, 'set_show_aspects'):
                        chart.set_show_aspects(False)
                    elif hasattr(chart, 'aspects_list'):
                        chart.aspects_list = []
                except Exception as e:
                    print(f"Aviso: Não foi possível configurar aspectos: {e}")
            
            # Configurar idioma
            try:
                if hasattr(chart, 'lang'):
                    chart.lang = data.language
                # Substituições manuais podem ser adicionadas aqui se necessário
            except Exception as e:
                print(f"Aviso: Não foi possível configurar idioma: {e}")
            
            # Gerar SVG
            chart.makeSVG()
            
            try:
                svg_content = get_svg_content(chart, temp_file)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erro ao obter conteúdo SVG: {str(e)}")
            
            return Response(
                content=svg_content,
                media_type="image/svg+xml",
                headers={
                    "Content-Disposition": f"inline; filename=chart_{natal_req.name or 'astrology'}.svg"
                }
            )
            
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Erro detalhado ao gerar SVG: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno ao gerar gráfico SVG: {str(e)}")

@router.post("/svg_chart_base64", 
    response_model=Dict[str, str],
    summary="Gera gráfico SVG em Base64",
    description="Gera um gráfico SVG e retorna como string base64, útil para incorporação em aplicações web.")
async def generate_svg_chart_base64(data: SVGChartRequest):
    """
    Gera um gráfico SVG e retorna como string base64.
    """
    try:
        svg_response = await generate_svg_chart(data)
        if svg_response.status_code != 200:
            raise HTTPException(status_code=svg_response.status_code, detail="Falha ao gerar SVG base.")
            
        svg_content_bytes = svg_response.body
        base64_svg = base64.b64encode(svg_content_bytes).decode("utf-8")
        
        return {
            "svg_base64": base64_svg,
            "data_uri": f"data:image/svg+xml;base64,{base64_svg}"
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Erro detalhado ao gerar SVG base64: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao gerar gráfico SVG em base64: {str(e)}"
        )

