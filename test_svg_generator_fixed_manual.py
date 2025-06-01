#!/usr/bin/env python3
"""
Script de teste para validar a implementação corrigida do gerador de SVG.

Este script testa a funcionalidade SVGChartGenerator com diferentes tipos de gráficos
e configurações para garantir que as correções funcionem em todos os casos.
"""
import sys
import os
import tempfile
from pathlib import Path
from datetime import datetime

# Adicionar o diretório raiz ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from astrology_api.app.svg.svg_generator_fixed import SVGChartGenerator
    from kerykeion import AstrologicalSubject
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("Verifique se o ambiente está configurado corretamente.")
    sys.exit(1)

def test_natal_chart():
    """Testa a geração de gráficos natais."""
    print("\n--- Testando gráfico natal ---")
    
    # Criar subject natal
    natal_subject = AstrologicalSubject(
        name="Teste Natal",
        year=1990,
        month=1,
        day=1,
        hour=12,
        minute=0,
        longitude=-46.63,
        latitude=-23.55,
        tz_str="America/Sao_Paulo"
    )
    
    # Criar gerador
    svg_generator = SVGChartGenerator(natal_subject)
    
    # Testar geração de SVG
    try:
        svg_content = svg_generator.generate_svg(
            chart_type="natal",
            show_aspects=True,
            language="pt",
            theme="light"
        )
        
        # Verificar se o conteúdo SVG parece válido
        if svg_generator.is_valid_svg(svg_content):
            print("✅ Geração de gráfico natal bem-sucedida")
            save_svg_to_file(svg_content, "natal_test.svg")
        else:
            print("❌ O conteúdo SVG gerado não parece válido")
    
    except Exception as e:
        print(f"❌ Erro ao gerar gráfico natal: {e}")

def test_transit_chart():
    """Testa a geração de gráficos de trânsito."""
    print("\n--- Testando gráfico de trânsito ---")
    
    # Criar subject natal
    natal_subject = AstrologicalSubject(
        name="Teste Natal",
        year=1990,
        month=1,
        day=1,
        hour=12,
        minute=0,
        longitude=-46.63,
        latitude=-23.55,
        tz_str="America/Sao_Paulo"
    )
    
    # Criar subject de trânsito (hoje)
    now = datetime.now()
    transit_subject = AstrologicalSubject(
        name="Trânsito",
        year=now.year,
        month=now.month,
        day=now.day,
        hour=now.hour,
        minute=now.minute,
        longitude=-46.63,
        latitude=-23.55,
        tz_str="America/Sao_Paulo"
    )
    
    # Criar gerador
    svg_generator = SVGChartGenerator(transit_subject)
    
    # Testar geração de SVG
    try:
        svg_content = svg_generator.generate_svg(
            chart_type="transit",
            show_aspects=True,
            language="pt",
            theme="light"
        )
        
        # Verificar se o conteúdo SVG parece válido
        if svg_generator.is_valid_svg(svg_content):
            print("✅ Geração de gráfico de trânsito bem-sucedida")
            save_svg_to_file(svg_content, "transit_test.svg")
        else:
            print("❌ O conteúdo SVG gerado não parece válido")
    
    except Exception as e:
        print(f"❌ Erro ao gerar gráfico de trânsito: {e}")

def test_combined_chart():
    """Testa a geração de gráficos combinados (natal + trânsito)."""
    print("\n--- Testando gráfico combinado ---")
    
    # Criar subject natal
    natal_subject = AstrologicalSubject(
        name="Teste Natal",
        year=1990,
        month=1,
        day=1,
        hour=12,
        minute=0,
        longitude=-46.63,
        latitude=-23.55,
        tz_str="America/Sao_Paulo"
    )
    
    # Criar subject de trânsito (hoje)
    now = datetime.now()
    transit_subject = AstrologicalSubject(
        name="Trânsito",
        year=now.year,
        month=now.month,
        day=now.day,
        hour=now.hour,
        minute=now.minute,
        longitude=-46.63,
        latitude=-23.55,
        tz_str="America/Sao_Paulo"
    )
    
    # Criar gerador
    svg_generator = SVGChartGenerator(natal_subject, transit_subject)
    
    # Testar geração de SVG
    try:
        svg_content = svg_generator.generate_svg(
            chart_type="combined",
            show_aspects=True,
            language="pt",
            theme="light"
        )
        
        # Verificar se o conteúdo SVG parece válido
        if svg_generator.is_valid_svg(svg_content):
            print("✅ Geração de gráfico combinado bem-sucedida")
            save_svg_to_file(svg_content, "combined_test.svg")
        else:
            print("❌ O conteúdo SVG gerado não parece válido")
    
    except Exception as e:
        print(f"❌ Erro ao gerar gráfico combinado: {e}")

def test_theme_variations():
    """Testa diferentes temas."""
    print("\n--- Testando variações de tema ---")
    
    # Criar subject natal
    natal_subject = AstrologicalSubject(
        name="Teste Natal",
        year=1990,
        month=1,
        day=1,
        hour=12,
        minute=0,
        longitude=-46.63,
        latitude=-23.55,
        tz_str="America/Sao_Paulo"
    )
    
    # Criar gerador
    svg_generator = SVGChartGenerator(natal_subject)
    
    # Testar tema escuro
    try:
        svg_content = svg_generator.generate_svg(
            chart_type="natal",
            theme="dark"
        )
        
        # Verificar se o conteúdo SVG parece válido
        if svg_generator.is_valid_svg(svg_content):
            print("✅ Geração com tema escuro bem-sucedida")
            save_svg_to_file(svg_content, "dark_theme_test.svg")
        else:
            print("❌ O conteúdo SVG com tema escuro não parece válido")
    
    except Exception as e:
        print(f"❌ Erro ao gerar gráfico com tema escuro: {e}")

def save_svg_to_file(svg_content, filename):
    """Salva o conteúdo SVG em um arquivo."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"  Arquivo salvo: {filename}")
    except Exception as e:
        print(f"  Erro ao salvar arquivo: {e}")

def run_all_tests():
    """Executa todos os testes."""
    print("===== INICIANDO TESTES DO GERADOR SVG FIXADO =====")
    print(f"Data e hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_natal_chart()
    test_transit_chart()
    test_combined_chart()
    test_theme_variations()
    
    print("\n===== TESTES CONCLUÍDOS =====")

if __name__ == "__main__":
    run_all_tests()
