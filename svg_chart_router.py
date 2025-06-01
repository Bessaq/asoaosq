from fastapi import APIRouter, HTTPException, Depends
from kerykeion import AstrologicalSubject, KerykeionChartSVG # Removido KerykeionError
from ..models import NatalChartSVGRequest, NatalChartSVGResponse # Reusing NatalChartRequest for SVG
import os

router = APIRouter(
    prefix="/api/v1",
    tags=["SVG Chart"],
)

@router.post("/natal_chart_svg", response_model=NatalChartSVGResponse)
async def create_natal_chart_svg(request: NatalChartSVGRequest):
    try:
        subject = AstrologicalSubject(
            name=request.name if request.name else "NatalChartSVG",
            year=request.year,
            month=request.month,
            day=request.day,
            hour=request.hour,
            minute=request.minute,
            city="CustomLocation",
            nation="",
            lng=request.longitude,
            lat=request.latitude,
            tz_str=request.tz_str,
            house_system=request.house_system if request.house_system else "Placidus"
        )
        
        chart_instance_name = request.name if request.name else "chart"
        safe_name = "".join(c if c.isalnum() else "_" for c in chart_instance_name)
        temp_svg_filename = f"{safe_name}_temp.svg"
        temp_svg_dir = "/home/ubuntu/astrologia_api/app/temp_svgs"
        os.makedirs(temp_svg_dir, exist_ok=True)
        temp_svg_filepath = os.path.join(temp_svg_dir, temp_svg_filename)
        
        chart_svg_generator = KerykeionChartSVG(
            subject,
            chart_type="Natal",
            new_output_directory=temp_svg_dir,
            filename=temp_svg_filename,
        )
        chart_svg_generator.makeSVG()

        svg_string_content = ""
        if hasattr(chart_svg_generator, 'svg_string') and chart_svg_generator.svg_string:
            svg_string_content = chart_svg_generator.svg_string
        else:
            try:
                with open(temp_svg_filepath, 'r', encoding='utf-8') as f:
                    svg_string_content = f.read()
            except FileNotFoundError:
                raise HTTPException(status_code=500, detail="Falha ao gerar ou ler o arquivo SVG.")
        
        try:
            if os.path.exists(temp_svg_filepath):
                os.remove(temp_svg_filepath)
        except OSError as e:
            print(f"Erro ao remover arquivo SVG temporário {temp_svg_filepath}: {e}")

        if not svg_string_content:
             raise HTTPException(status_code=500, detail="Conteúdo SVG não pôde ser gerado.")

        return NatalChartSVGResponse(svg_image=svg_string_content)

    except Exception as e:  # Captura genérica para erros do Kerykeion e outros
        print(f"Erro de cálculo astrológico em natal_chart_svg (Kerykeion ou outro): {type(e).__name__} - {str(e)}")
        raise HTTPException(status_code=400, detail=f"Erro de cálculo astrológico (Kerykeion) para SVG: {str(e)}")
    # except ValueError as e:
    #     raise HTTPException(status_code=400, detail=f"Erro nos dados de entrada para SVG: {str(e)}")
    # except Exception as e:
    #     print(f"Erro inesperado em natal_chart_svg: {type(e).__name__} - {str(e)}")
    #     raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao gerar SVG: {type(e).__name__}")

