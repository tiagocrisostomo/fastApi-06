from fastapi import APIRouter

from api.v1.endpoints import artigo
from api.v1.endpoints import user

api_router = APIRouter()

api_router.include_router(user.router, prefix='/usuarios', tags=['Usuários'])
api_router.include_router(artigo.router, prefix='/artigos', tags=['Artigos'])
