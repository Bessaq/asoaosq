"""
Módulo para geração de gráficos SVG astrológicos.

Este módulo contém funções auxiliares para geração de gráficos SVG
utilizando a biblioteca Kerykeion.
"""
from kerykeion import KerykeionChartSVG, AstrologicalSubject
import os
import tempfile
from typing import Optional, Dict, Any, Tuple

def generate_svg_chart(
    natal_subject: AstrologicalSubject,
    transit_subject: Optional[AstrologicalSubject] = None,
    chart_type: str = "Natal",
    show_aspects: bool = True,
    theme: str = "light",
    language: str = "pt"
) -> str:
    """
    Gera um gráfico astrológico em formato SVG.
    
    Args:
        natal_subject (AstrologicalSubject): Objeto AstrologicalSubject para o mapa natal.
        transit_subject (Optional[AstrologicalSubject], opcional): Objeto AstrologicalSubject para o mapa de trânsito.
        chart_type (str, opcional): Tipo de gráfico ("Natal", "Transit", "Combined"). Padrão é "Natal".
        show_aspects (bool, opcional): Se deve mostrar linhas de aspectos. Padrão é True.
        theme (str, opcional): Tema de cores ("light", "dark"). Padrão é "light".
        language (str, opcional): Idioma para os textos ("pt", "en"). Padrão é "pt".
        
    Returns:
        str: Conteúdo SVG do gráfico gerado.
        
    Raises:
        Exception: Se ocorrer um erro durante a geração do gráfico.
    """
    try:
        # Criar um diretório temporário para salvar o SVG
        with tempfile.TemporaryDirectory() as temp_dir:
            # Definir o nome do arquivo temporário
            temp_file = os.path.join(temp_dir, "chart.svg")
            
            # Configurar opções com base no tema
            chart_params = {
                "new_output_directory": temp_dir,
                "filename": "chart.svg",
                "chart_type": chart_type,
                "second_obj": transit_subject
            }
            
            # Adicionar opções específicas de tema e idioma
            # Nota: Essas opções podem variar dependendo da versão do Kerykeion
            if theme == "dark":
                chart_params["black_bg"] = True
            
            # Criar o gerador de gráficos SVG
            chart_svg_generator = KerykeionChartSVG(
                natal_subject,
                **chart_params
            )
            
            # Gerar o SVG
            chart_svg_generator.makeSVG()
            
            # Ler o conteúdo SVG
            svg_content = ""
            if hasattr(chart_svg_generator, 'svg_string') and chart_svg_generator.svg_string:
                svg_content = chart_svg_generator.svg_string
            else:
                try:
                    with open(temp_file, 'r', encoding='utf-8') as f:
                        svg_content = f.read()
                except FileNotFoundError:
                    raise Exception("Erro ao gerar gráfico SVG: arquivo SVG não encontrado")
            
            return svg_content
    
    except Exception as e:
        raise Exception(f"Erro ao gerar gráfico SVG: {str(e)}")

def customize_svg(svg_content: str, options: Dict[str, Any]) -> str:
    """
    Personaliza um gráfico SVG com base nas opções fornecidas.
    
    Args:
        svg_content (str): Conteúdo SVG original.
        options (Dict[str, Any]): Opções de personalização.
        
    Returns:
        str: Conteúdo SVG personalizado.
    """
    # Implementar lógica de personalização do SVG
    # Por exemplo, alterar cores, fontes, etc.
    
    # Por enquanto, apenas retornamos o SVG original
    return svg_content

def get_chart_dimensions(chart_size: str = "medium") -> Tuple[int, int]:
    """
    Obtém as dimensões do gráfico com base no tamanho especificado.
    
    Args:
        chart_size (str, opcional): Tamanho do gráfico ("small", "medium", "large"). Padrão é "medium".
        
    Returns:
        Tuple[int, int]: Dimensões do gráfico (largura, altura).
    """
    sizes = {
        "small": (600, 600),
        "medium": (800, 800),
        "large": (1000, 1000),
        "xlarge": (1200, 1200)
    }
    
    return sizes.get(chart_size, (800, 800))
