#!/usr/bin/env python3
"""
Script para inspecionar os módulos e classes do Kerykeion.

Este script analisa as classes e métodos disponíveis no Kerykeion,
ajudando a entender as diferenças entre versões e a implementar
compatibilidade.
"""
import sys
import os
import inspect
from pprint import pprint

try:
    import kerykeion
    from kerykeion import AstrologicalSubject, KerykeionChartSVG
except ImportError as e:
    print(f"Erro ao importar Kerykeion: {e}")
    sys.exit(1)

def print_separator():
    print("\n" + "=" * 60 + "\n")

def inspect_module(module):
    """Inspeciona um módulo e mostra informações sobre ele."""
    print(f"Módulo: {module.__name__}")
    print(f"Versão: {getattr(module, '__version__', 'Desconhecida')}")
    print(f"Localização: {getattr(module, '__file__', 'Desconhecida')}")
    print("\nSubmódulos/pacotes:")
    
    # Listar submódulos
    submodules = []
    for name in dir(module):
        obj = getattr(module, name)
        if inspect.ismodule(obj):
            submodules.append(name)
    
    if submodules:
        for submodule in sorted(submodules):
            print(f"  - {submodule}")
    else:
        print("  Nenhum submódulo encontrado")
    
    # Listar classes
    print("\nClasses exportadas:")
    classes = []
    for name in dir(module):
        obj = getattr(module, name)
        if inspect.isclass(obj) and obj.__module__.startswith(module.__name__):
            classes.append(name)
    
    if classes:
        for cls in sorted(classes):
            print(f"  - {cls}")
    else:
        print("  Nenhuma classe encontrada")

def inspect_class(cls):
    """Inspeciona uma classe e mostra suas propriedades e métodos."""
    print(f"Classe: {cls.__name__}")
    print(f"Módulo: {cls.__module__}")
    
    # Listar métodos
    methods = []
    for name, obj in inspect.getmembers(cls):
        if inspect.isfunction(obj) or inspect.ismethod(obj):
            if not name.startswith("_"):  # Ignorar métodos privados
                try:
                    signature = str(inspect.signature(obj))
                    methods.append(f"  - {name}{signature}")
                except ValueError:
                    methods.append(f"  - {name}(...)")
    
    if methods:
        print("\nMétodos públicos:")
        for method in sorted(methods):
            print(method)
    else:
        print("\nNenhum método público encontrado")
    
    # Listar atributos
    attributes = []
    for name in dir(cls):
        if not name.startswith("_") and not callable(getattr(cls, name, None)):
            attributes.append(name)
    
    if attributes:
        print("\nAtributos públicos:")
        for attr in sorted(attributes):
            print(f"  - {attr}")
    else:
        print("\nNenhum atributo público encontrado")

def create_and_inspect_instance(cls, *args, **kwargs):
    """Cria uma instância da classe e inspeciona seus atributos e métodos."""
    try:
        instance = cls(*args, **kwargs)
        print(f"Instância de {cls.__name__} criada com sucesso")
        
        # Listar atributos de instância
        instance_attrs = {}
        for name in dir(instance):
            if not name.startswith("_") and not callable(getattr(instance, name)):
                try:
                    value = getattr(instance, name)
                    if not inspect.isclass(value) and not inspect.isfunction(value) and not inspect.ismethod(value):
                        # Truncar strings longas
                        if isinstance(value, str) and len(value) > 100:
                            value = value[:100] + "..."
                        instance_attrs[name] = value
                except Exception as e:
                    instance_attrs[name] = f"<Erro ao acessar: {e}>"
        
        if instance_attrs:
            print("\nAtributos da instância:")
            for name, value in sorted(instance_attrs.items()):
                print(f"  - {name}: {type(value).__name__} = {value}")
        else:
            print("\nNenhum atributo de instância encontrado")
        
        return instance
    except Exception as e:
        print(f"Erro ao criar instância: {e}")
        return None

def main():
    """Função principal do script."""
    print("===== INSPEÇÃO DE MÓDULOS DO KERYKEION =====")
    
    # Inspecionar módulo principal
    inspect_module(kerykeion)
    print_separator()
    
    # Inspecionar classes principais
    print("===== CLASSES PRINCIPAIS =====")
    inspect_class(AstrologicalSubject)
    print_separator()
    
    inspect_class(KerykeionChartSVG)
    print_separator()
    
    # Criar e inspecionar instâncias
    print("===== INSTÂNCIAS =====")
    
    # Criar subject
    subject = create_and_inspect_instance(
        AstrologicalSubject,
        name="Teste",
        year=1990, month=1, day=1,
        hour=12, minute=0,
        longitude=-46.63, latitude=-23.55,
        tz_str="America/Sao_Paulo"
    )
    print_separator()
    
    # Criar chart
    if subject:
        chart = create_and_inspect_instance(
            KerykeionChartSVG,
            subject
        )
        
        # Testar métodos do chart
        if chart and hasattr(chart, 'makeSVG') and callable(getattr(chart, 'makeSVG')):
            print("\nExecutando chart.makeSVG()...")
            try:
                getattr(chart, 'makeSVG')()
                print("makeSVG() executado com sucesso")
                
                # Verificar onde o SVG foi salvo
                print("\nVerificando atributos após makeSVG:")
                svg_attrs = ['svg', 'svg_string', 'svg_path']
                for attr in svg_attrs:
                    if hasattr(chart, attr):
                        value = getattr(chart, attr)
                        if value:
                            print(f"  - {attr}: {type(value).__name__}")
                            if isinstance(value, str) and len(value) > 100:
                                print(f"    Primeiros 100 caracteres: {value[:100]}...")
                            else:
                                print(f"    Valor: {value}")
                
            except Exception as e:
                print(f"Erro ao executar makeSVG: {e}")

if __name__ == "__main__":
    main()
