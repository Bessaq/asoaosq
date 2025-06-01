from fastapi import FastAPI
from app.routers import natal_chart_router, transit_router, svg_chart_router # Ajuste de importação relativo
from app.exceptions import add_exception_handlers
import uvicorn
import os
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
# Isso é útil se você tiver chaves de API ou configurações sensíveis
# Por exemplo, API_KEY_KERYKEION="SUA_CHAVE_AQUI" no .env
load_dotenv()

os.environ["API_KEY_KERYKEION"] = "testapikey"

app = FastAPI(
    title="API de Astrologia",
    description="Uma API para cálculos astrológicos, incluindo mapas natais, trânsitos e geração de gráficos SVG.",
    version="0.1.0",
    #openapi_tags=openapi_tags # Se precisar de metadados de tags
)

add_exception_handlers(app)

# Incluir os routers
app.include_router(natal_chart_router.router)
app.include_router(transit_router.router)
app.include_router(svg_chart_router.router) # Adicionando o router SVG

@app.get("/", tags=["Root"], summary="Endpoint raiz da API")
async def read_root():
    return {"message": "Bem-vindo à API de Astrologia. Acesse /docs para a documentação interativa."}

# Para executar localmente com Uvicorn (opcional, pode ser executado via CLI)
if __name__ == "__main__":
    # Certifique-se de que o Uvicorn está instalado: pip install uvicorn[standard]
    # Para executar: python app/main.py (estando no diretório astrologia_api)
    # Ou, mais comumente: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    
    # Para o ambiente de desenvolvimento, rodar via CLI é geralmente melhor por causa do --reload.
    # Esta seção __main__ é mais para conveniência de teste rápido ou se não quiser usar o CLI.
    # uvicorn.run(app, host="0.0.0.0", port=8000) # Comentado para preferir execução via CLI
    pass
