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
    
    """ tiago
        TOKEN: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzAwNTcyMTU2LCJpYXQiOjE2OTk5NjczNTYsInN1YiI6IjUifQ.ogUBzT_Gb259qYr7bm4elNn6I3E-cFpINfNiwIo1b_Q
        TIPO: bearer
    """
    
    """ helio
        TOKEN: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzAwNTc2MDcxLCJpYXQiOjE2OTk5NzEyNzEsInN1YiI6IjYifQ.nEQDwIMhR4KYBwZohQxlxWjxdqXj8eNDlHztKSO0CEg
        TIPO: bearer
    """
    
    """ michael
        TOKEN: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzAwNzQ4MTQ0LCJpYXQiOjE3MDAxNDMzNDQsInN1YiI6IjgifQ.BcEdgLY-sCRMZzdaIe5YOljC2qBKeo4-XdqXqMbPhII
        TIPO: bearer
    """
    