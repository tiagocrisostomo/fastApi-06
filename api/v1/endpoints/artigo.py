from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.artigo_model import ArtigoModel
from models.user_model import UserModel
from schemas.artigo_shema import ArtigoSchema
from core.deps import get_session, get_current_user


router = APIRouter()

# POST Artigo
@router.post('/', 
    status_code=status.HTTP_201_CREATED, 
    response_model=ArtigoSchema,
    description='Cadastra um novo artigo.', 
    summary='Cadastra um artigo.', 
    response_description="Cadastro efetuado com sucesso.")
async def post_artigo(artigo: ArtigoSchema, user_logged: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):    
    novo_artigo: ArtigoModel = ArtigoModel(titulo=artigo.titulo, descricao=artigo.descricao, url_fonte=str(artigo.url_fonte), user_id=user_logged.id)
    
    db.add(novo_artigo)
    await db.commit()
    
    return novo_artigo

# GET Artigos
@router.get('/', 
    response_model=List[ArtigoSchema],
    description='Consultas os artigos, devolvendo seus dados.', 
    summary='Consulta os artigos.', 
    response_description="Cadastro efetuado com sucesso.")
async def get_artigos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel).order_by(ArtigoModel.id)
        result = await session.execute(query)
        artigos: List[ArtigoModel] = result.scalars().unique().all()
        
        return artigos
    
# GET Artigo
@router.get('/{artigo_id}', 
    response_model=ArtigoSchema, 
    status_code=status.HTTP_200_OK,
    description='Consulta o artigo informado, devolvendo seus dados.', 
    summary='Consulta um artigo.', 
    response_description="Consulta efetuada com sucesso.")
async def get_artigo(artigo_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().unique().one_or_none()
        
        if artigo:
            return artigo
        else:
            raise HTTPException(detail="Artigo não entrado.", status_code=status.HTTP_404_NOT_FOUND)
        
        
# PUT Artigo
@router.put('/{artigo_id}', 
    response_model=ArtigoSchema, 
    status_code=status.HTTP_202_ACCEPTED,
    description='Retorna os dados do artigo atualizado.', 
    summary='Altera o artigo.', 
    response_description="Alterado com sucesso.")
async def put_artigo(artigo_id: int, artigo: ArtigoSchema,  db: AsyncSession = Depends(get_session), user_logged: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo_up: ArtigoModel = result.scalars().unique().one_or_none()
        
        if artigo_up:            
            if artigo.titulo:
                artigo_up.titulo =  artigo.titulo
            if artigo.descricao:
                artigo_up.descricao = artigo.descricao
            if artigo.url_fonte:
                artigo_up.url_fonte = str(artigo.url_fonte) 
            if user_logged.id != artigo_up.user_id:
                artigo_up.user_id =  user_logged.id
            
            await session.commit()
            
            return artigo_up
        else:
            raise HTTPException(detail="Artigo não entrado.", status_code=status.HTTP_404_NOT_FOUND)    
        
        
# DELETE Artigo        
@router.delete('/{artigo_id}', 
    status_code=status.HTTP_204_NO_CONTENT,
    description='Deleta o artigo informado.', 
    summary='Deleta o artigo.', 
    response_description="Deletado com sucesso.")
async def delete_artigo(artigo_id: int, db: AsyncSession = Depends(get_session), user_logged: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id).filter(ArtigoModel.user_id == user_logged.id)
        result = await session.execute(query)
        artigo_del: ArtigoModel = result.scalars().unique().one_or_none()
        
        if artigo_del:            
            await session.delete(artigo_del)            
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Artigo não entrado.", status_code=status.HTTP_404_NOT_FOUND) 