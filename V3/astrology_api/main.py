from fastapi import FastAPI
# Import routers from the app.api package
from app.api import natal_chart_router, transit_router, svg_chart_router

app = FastAPI(
    title="API de Astrologia",
    description="""
    API para cálculos astrológicos, incluindo mapas natais, trânsitos, aspectos e geração de gráficos SVG.
    
    Utiliza Kerykeion para cálculos precisos e oferece endpoints para:
    - Calcular Mapas Natais
    - Calcular Trânsitos Planetários
    - Gerar Gráficos SVG (Natal, Trânsito, Combinado)
    
    **Sistemas de Casas Suportados:** Placidus (padrão), Koch, Porphyrius, Regiomontanus, Campanus, Equal, Whole Sign, Alcabitus, Morinus, Horizontal, Topocentric, Vehlow.
    
    **Idiomas Suportados (SVG):** Inglês (en), Português (pt).
    
    **Temas Suportados (SVG):** Light (padrão), Dark.
    """,
    version="1.1.0" # Versão incrementada para refletir adição do SVG
)

# Incluir os routers existentes
app.include_router(natal_chart_router.router, prefix="/api/v1", tags=["Natal Chart"])
app.include_router(transit_router.router, prefix="/api/v1", tags=["Transits"])

# Incluir o novo router para SVG
app.include_router(svg_chart_router.router, prefix="/api/v1", tags=["SVG Charts"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bem-vindo à API de Astrologia! Acesse /docs para a documentação interativa."}

# Adicionar configuração para Uvicorn se for executar diretamente
# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

