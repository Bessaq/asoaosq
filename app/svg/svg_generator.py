"""
Módulo para geração de gráficos SVG astrológicos.

Este módulo contém a classe SVGChartGenerator que encapsula toda a lógica
de geração de gráficos SVG usando o Kerykeion.
"""
from kerykeion import AstrologicalSubject, KerykeionChartSVG
from typing import Optional, Dict, Any, Tuple, Union
import os
import tempfile
from pathlib import Path

class SVGChartGenerator:
    """
    Gerador de gráficos SVG com suporte a diferentes tipos de mapas e customizações.
    """

    CHART_TYPES = {
        "natal": "Natal",
        "transit": "Transit",
        "combined": "Composite"  # ou "Combined", dependendo da versão do Kerykeion
    }

    def __init__(self, natal_subject: AstrologicalSubject, transit_subject: Optional[AstrologicalSubject] = None) -> None:
        self.natal_subject = natal_subject
        self.transit_subject = transit_subject

    def get_svg_content(self, chart: Any, temp_file: str) -> str:
        """
        Tenta obter o conteúdo SVG do gráfico usando diferentes métodos disponíveis.
        """
        # Tenta obter diretamente da instância primeiro
        if hasattr(chart, 'svg_string') and getattr(chart, 'svg_string'):
            return getattr(chart, 'svg_string')
        if hasattr(chart, 'svg') and getattr(chart, 'svg'):
            return getattr(chart, 'svg')

        # Tenta métodos específicos para obter o SVG
        if hasattr(chart, 'makeTemplate') and callable(getattr(chart, 'makeTemplate')):
            return getattr(chart, 'makeTemplate')()
        if hasattr(chart, 'get_svg_string') and callable(getattr(chart, 'get_svg_string')):
            return getattr(chart, 'get_svg_string')()
        if hasattr(chart, 'get_svg') and callable(getattr(chart, 'get_svg')):
            return getattr(chart, 'get_svg')()

        # Tenta ler do arquivo temporário como último recurso
        try:
            if os.path.exists(temp_file):
                with open(temp_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content:
                        return content
        except Exception as e:
            raise Exception(f"Erro ao ler arquivo SVG: {str(e)}")
            
        raise Exception("Não foi possível obter o conteúdo SVG por nenhum método disponível")

    def generate_svg(
        self,
        chart_type: str = "natal",
        show_aspects: bool = True,
        language: str = "pt",
        theme: str = "light"
    ) -> str:
        """
        Gera um gráfico SVG com as configurações especificadas.
        """
        # Validar o tipo de gráfico
        if chart_type not in self.CHART_TYPES:
            raise ValueError(f"Tipo de gráfico inválido: {chart_type}")

        # Validar se temos os dados necessários para o tipo de gráfico
        if chart_type in ["transit", "combined"] and not self.transit_subject:
            raise ValueError(f"Dados de trânsito são necessários para gráficos do tipo {chart_type}")

        # Criar um diretório temporário para salvar o SVG
        with tempfile.TemporaryDirectory() as temp_dir:
            # Definir o nome do arquivo temporário
            temp_file = os.path.join(temp_dir, "chart.svg")

            # Definir parâmetros do gráfico
            chart_params = {}
            if chart_type in ["transit", "combined"] and self.transit_subject:
                chart_params["second_obj"] = self.transit_subject

            # Criar o gerador de gráficos SVG
            chart_svg_generator = KerykeionChartSVG(
                self.natal_subject,
                chart_type=self.CHART_TYPES[chart_type],
                **chart_params
            )

            # Configurar diretório de saída
            if hasattr(chart_svg_generator, 'set_output_directory') and callable(getattr(chart_svg_generator, 'set_output_directory')):
                getattr(chart_svg_generator, 'set_output_directory')(Path(temp_dir))

            # Configurar tema se suportado
            if hasattr(chart_svg_generator, 'set_up_theme') and callable(getattr(chart_svg_generator, 'set_up_theme')) and theme == "dark":
                getattr(chart_svg_generator, 'set_up_theme')("dark")

            # Gerar SVG
            try:
                if hasattr(chart_svg_generator, 'makeSVG') and callable(getattr(chart_svg_generator, 'makeSVG')):
                    getattr(chart_svg_generator, 'makeSVG')()

                # Obter o conteúdo SVG
                svg_content = self.get_svg_content(chart_svg_generator, temp_file)
                return svg_content

            except Exception as e:
                raise Exception(f"Erro ao gerar gráfico SVG: {str(e)}")
