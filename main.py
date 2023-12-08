from fastapi import FastAPI

from core.configs import settings
from api.v1.api import api_router


app = FastAPI(
    title="Aprendendo FastAPI Segurança e Autenticação !", 
    version="v1",
    description='Uma API para estudo do FastAPI.',
    openapi_url='/apiconf.json',
    docs_url='/api/v1/documentacao',
    redoc_url='/api/v1/redoc'
)
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level='info',
        reload=True        
    )
        