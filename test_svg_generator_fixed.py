"""
Teste para verificar a geração de gráficos SVG usando nossa implementação fixa.
"""
from kerykeion import AstrologicalSubject
import os
from pathlib import Path

from astrology_api.app.svg.svg_generator_fixed import SVGChartGenerator

def test_svg_generation():
    """Testa a geração de diferentes tipos de gráficos SVG."""
    # Criar sujeito para mapa natal
    natal_subject = AstrologicalSubject(
        name="Teste Natal",
        year=1990,
        month=7,
        day=15,
        hour=12,
        minute=30,
        city="São Paulo",
        nation="BR",
        lng=-46.6333,
        lat=-23.5505,
        tz_str="America/Sao_Paulo"
    )
    
    # Criar sujeito para trânsito
    transit_subject = AstrologicalSubject(
        name="Teste Trânsito",
        year=2023,
        month=5,
        day=10,
        hour=14,
        minute=0,
        city="São Paulo",
        nation="BR",
        lng=-46.6333,
        lat=-23.5505,
        tz_str="America/Sao_Paulo"
    )
    
    # Criar diretório para salvar os SVGs de teste
    output_dir = Path("./test_svg_output")
    output_dir.mkdir(exist_ok=True)
    
    # Testar mapa natal
    print("Gerando mapa natal...")
    natal_generator = SVGChartGenerator(natal_subject)
    try:
        natal_svg = natal_generator.generate_svg(chart_type="natal")
        with open(output_dir / "natal_test.svg", "w", encoding="utf-8") as f:
            f.write(natal_svg)
        print(f"Mapa natal gerado com {len(natal_svg)} caracteres")
    except Exception as e:
        print(f"Erro ao gerar mapa natal: {str(e)}")
    
    # Testar mapa de trânsito
    print("\nGerando mapa de trânsito...")
    transit_generator = SVGChartGenerator(natal_subject, transit_subject)
    try:
        transit_svg = transit_generator.generate_svg(chart_type="transit")
        with open(output_dir / "transit_test.svg", "w", encoding="utf-8") as f:
            f.write(transit_svg)
        print(f"Mapa de trânsito gerado com {len(transit_svg)} caracteres")
    except Exception as e:
        print(f"Erro ao gerar mapa de trânsito: {str(e)}")
    
    # Testar mapa combinado
    print("\nGerando mapa combinado...")
    combined_generator = SVGChartGenerator(natal_subject, transit_subject)
    try:
        combined_svg = combined_generator.generate_svg(chart_type="combined")
        with open(output_dir / "combined_test.svg", "w", encoding="utf-8") as f:
            f.write(combined_svg)
        print(f"Mapa combinado gerado com {len(combined_svg)} caracteres")
    except Exception as e:
        print(f"Erro ao gerar mapa combinado: {str(e)}")
    
    # Testar com tema escuro
    print("\nGerando mapa com tema escuro...")
    dark_generator = SVGChartGenerator(natal_subject)
    try:
        dark_svg = dark_generator.generate_svg(chart_type="natal", theme="dark")
        with open(output_dir / "dark_theme_test.svg", "w", encoding="utf-8") as f:
            f.write(dark_svg)
        print(f"Mapa com tema escuro gerado com {len(dark_svg)} caracteres")
    except Exception as e:
        print(f"Erro ao gerar mapa com tema escuro: {str(e)}")
    
    print("\nTestes concluídos. Verifique os arquivos SVG gerados na pasta:", output_dir.absolute())

if __name__ == "__main__":
    test_svg_generation()
