"""
Módulo para geração de gráficos SVG astrológicos.

Este módulo contém a classe SVGChartGenerator que encapsula toda a lógica
de geração de gráficos SVG usando o Kerykeion.
"""
from kerykeion import AstrologicalSubject, KerykeionChartSVG
from typing import Optional, Dict, Any, Tuple, Union, Literal, cast
import os
import tempfile
import shutil
from pathlib import Path

# Definindo literais para tipos de gráficos Kerykeion
ChartType = Literal["Natal", "Transit", "Synastry", "Combined", "Composite"]

class SVGChartGenerator:
    """
    Gerador de gráficos SVG com suporte a diferentes tipos de mapas e customizações.
    
    Esta classe implementa métodos seguros para lidar com diferentes versões
    do Kerykeion e seus métodos de geração de SVG.
    """

    CHART_TYPES = {
        "natal": "Natal",
        "transit": "Transit", 
        "combined": "Composite"
    }

    def __init__(self, natal_subject: AstrologicalSubject, transit_subject: Optional[AstrologicalSubject] = None) -> None:
        """
        Inicializa o gerador de gráficos SVG.
        
        Args:
            natal_subject: O objeto AstrologicalSubject do mapa natal
            transit_subject: O objeto AstrologicalSubject do trânsito (opcional)
        """
        self.natal_subject = natal_subject
        self.transit_subject = transit_subject    def get_svg_content(self, chart: Any, temp_file: str) -> str:
        """
        Tenta obter o conteúdo SVG do gráfico usando diferentes métodos disponíveis.
        
        Esta função é robusta para lidar com diferentes versões do Kerykeion.
        
        Args:
            chart: Objeto do gráfico Kerykeion
            temp_file: Caminho para o arquivo SVG temporário
            
        Returns:
            Conteúdo SVG como string
            
        Raises:
            Exception: Se não for possível obter o conteúdo SVG
        """
        # Tenta obter diretamente da instância primeiro (atributos)
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

    def is_valid_svg(self, content: str) -> bool:
        """
        Verifica se o conteúdo SVG parece válido.
        
        Args:
            content: Conteúdo SVG como string
            
        Returns:
            bool: True se o conteúdo parece ser um SVG válido
        """
        if not content:
            return False
            
        # Verificações básicas de estrutura SVG
        has_svg_tag = '<svg' in content and '</svg>' in content
        has_xml_declaration = '<?xml' in content or '<svg' in content
        
        # Verificar se há elementos essenciais em um gráfico astrológico
        has_astrological_elements = any(x in content for x in [
            'circle', 'path', 'text', 'zodiac', 'planet', 'house',
            'ascendant', 'midheaven', 'wheel'
        ])
        
        return has_svg_tag and has_xml_declaration and has_astrological_elements

    def generate_svg(
        self,
        chart_type: str = "natal",
        show_aspects: bool = True,
        language: str = "pt",
        theme: str = "light"
    ) -> str:
        """
        Gera um gráfico SVG com as configurações especificadas.
        
        Args:
            chart_type: Tipo de gráfico ("natal", "transit", "combined")
            show_aspects: Se deve mostrar aspectos no gráfico
            language: Idioma do gráfico
            theme: Tema do gráfico ("light", "dark")
            
        Returns:
            Conteúdo SVG como string
            
        Raises:
            ValueError: Se os parâmetros forem inválidos
            Exception: Se ocorrer um erro na geração do gráfico
        """
        # Validar o tipo de gráfico
        if chart_type not in self.CHART_TYPES:
            raise ValueError(f"Tipo de gráfico inválido: {chart_type}")

        # Validar se temos os dados necessários para o tipo de gráfico
        if chart_type in ["transit", "combined"] and not self.transit_subject:
            raise ValueError(f"Dados de trânsito são necessários para gráficos do tipo {chart_type}")

        # Criar um diretório temporário para salvar o SVG
        temp_dir = None
        try:
            temp_dir = tempfile.mkdtemp()
            temp_file = os.path.join(temp_dir, "chart.svg")
            
            # Criar o gerador de gráficos SVG
            kerykeion_chart_type = self.CHART_TYPES[chart_type]
            
            kwargs = {}
            
            # Adicionar segundo objeto apenas se necessário
            if chart_type in ["transit", "combined"] and self.transit_subject:
                kwargs["second_obj"] = self.transit_subject                # Criar instância do gerador de gráficos
                chart_svg_generator = KerykeionChartSVG(
                    self.natal_subject,
                    chart_type=cast(ChartType, kerykeion_chart_type),
                    **kwargs
                )
            
            # Configurar diretório de saída de forma segura
            if hasattr(chart_svg_generator, 'set_output_directory') and callable(getattr(chart_svg_generator, 'set_output_directory')):
                try:
                    # Tentar com Path
                    getattr(chart_svg_generator, 'set_output_directory')(Path(temp_dir))
                except TypeError:
                    # Fallback para string
                    getattr(chart_svg_generator, 'set_output_directory')(temp_dir)
            
            # Configurar tema se suportado
            if theme == "dark" and hasattr(chart_svg_generator, 'set_up_theme') and callable(getattr(chart_svg_generator, 'set_up_theme')):
                getattr(chart_svg_generator, 'set_up_theme')("dark")
            
            # Configurar aspectos se necessário
            if not show_aspects and hasattr(chart_svg_generator, 'set_show_aspects') and callable(getattr(chart_svg_generator, 'set_show_aspects')):
                getattr(chart_svg_generator, 'set_show_aspects')(False)
              # Configurar idioma se suportado
            if hasattr(chart_svg_generator, 'lang'):
                try:
                    setattr(chart_svg_generator, 'lang', language)
                except Exception:
                    pass  # Ignorar erro de configuração de idioma
            
            # Gerar SVG
            if hasattr(chart_svg_generator, 'makeSVG') and callable(getattr(chart_svg_generator, 'makeSVG')):
                getattr(chart_svg_generator, 'makeSVG')()

            # Obter o conteúdo SVG
            svg_content = self.get_svg_content(chart_svg_generator, temp_file)
            
            # Validar o conteúdo SVG gerado
            if not self.is_valid_svg(svg_content):
                raise Exception(f"O SVG gerado para o gráfico '{chart_type}' não é válido. Verifique a configuração do Kerykeion ou forneça informações mais detalhadas.")

            return svg_content

        except Exception as e:
            raise Exception(f"Erro ao gerar gráfico SVG: {str(e)}")
        finally:
            # Garantir que o diretório temporário seja removido
            if temp_dir and os.path.exists(temp_dir):
                try:
                    import shutil
                    shutil.rmtree(temp_dir, ignore_errors=True)
                except Exception:
                    pass  # Melhor esforço para limpar
