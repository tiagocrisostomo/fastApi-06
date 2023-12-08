from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.user_model import UserModel
from schemas.user_schema import UserSchemaBase, UserSchameCreate, UserSchemaArtigos, UserSchemaUp
from core.deps import get_session, get_current_user
from core.security import generate_hash
from core.auth import authenticate, create_access_token


router = APIRouter()


# GET Logado
@router.get('/logado', 
    response_model=UserSchemaBase,
    description='Consulta o usuário logado pelo seu token.', 
    summary='Consulta o usuário logado.', 
    response_description="Consulta efetuada com sucesso.")
def get_logado(user_logged: UserModel = Depends(get_current_user)):
    return user_logged


# POST / Sign up
@router.post('/signup', 
        status_code=status.HTTP_201_CREATED, 
        response_model=UserSchemaBase,
        description='Cadastro de um novo usuário', 
        summary='Cadastra um usuário.', 
        response_description="Cadastro efetuado com sucesso.")
async def post_user(user: UserSchameCreate, db: AsyncSession = Depends(get_session)):
    new_user: UserModel = UserModel(
        nome=user.nome,
        sobrenome=user.sobrenome,
        email=user.email,
        senha=generate_hash(user.senha),
        eh_admin=user.eh_admin
    )
    async with db as session:
        try:            
            session.add(new_user)
            await session.commit()
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Já existe um usuário com este email.')
        
        return new_user
    
    
# GET Usuarios
@router.get('/', 
        response_model=List[UserSchemaBase],
        description='Consulta os usuários, devolvendo seus dados.', 
        summary='Consulta os usuários.', 
        response_description="Consulta efetuada com sucesso.")
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).order_by(UserModel.id)
        result = await session.execute(query)
        usuarios: List[UserSchemaBase] = result.scalars().unique().all()
        
        return usuarios

# GET Usuario
@router.get('/{user_id}', 
        response_model=UserSchemaArtigos, 
        status_code=status.HTTP_200_OK,
        description='Consulta o usuário informado, devolvendo seus dados.', 
        summary='Consulta um usuário.', 
        response_description="Consulta efetuada com sucesso.")
async def get_usuario(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        usuario: UserSchemaArtigos = result.scalars().unique().one_or_none()
        
        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
        

# PUT Usuario
@router.put('/{user_id}', 
            response_model=UserSchemaBase, 
            status_code=status.HTTP_202_ACCEPTED, 
            description='Retorna os dados do usuário atualizado, caso seja um Admin ou ele próprio alterando, caso contrário não terá permissão.', 
            summary='Altera o usuário.', 
            response_description="Alterado com sucesso.")
async def put_usuario(user_id: int,  
                      user: UserSchemaUp,  
                      db: AsyncSession = Depends(get_session), 
                      user_logged: UserModel = Depends(get_current_user)):
    
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        usuario_up: UserSchemaBase = result.scalars().unique().one_or_none()
             
        if usuario_up:
            if user.nome:
                usuario_up.nome = user.nome
            if user.sobrenome:
                usuario_up.sobrenome = user.sobrenome
            if user.email:
                usuario_up.email = user.email
            if user.eh_admin != None:    
                usuario_up.eh_admin = user.eh_admin
            if user.senha:
                usuario_up.senha= generate_hash(user.senha)
            
            try:
                if not user_logged.id == user_id and user_logged.eh_admin == False:
                    raise HTTPException(detail='Sem permissão para alterar usuário.', status_code=status.HTTP_401_UNAUTHORIZED)
                
                await session.commit()
                
                return usuario_up
            except IntegrityError:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Já existe um usuário com este email.')            
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
        

# DELETE Usuario
@router.delete('/{user_id}', 
                status_code=status.HTTP_204_NO_CONTENT,
                description='Deleta o usuário informado.', 
                summary='Deleta o usuário.', 
                response_description="Deletado com sucesso.")
async def delete_usuario(user_id: int, db: AsyncSession = Depends(get_session), user_logged: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id).filter(UserModel.id != user_logged.id).filter(UserModel.eh_admin == False)
        result = await session.execute(query)
        usuario_del: UserSchemaBase = result.scalars().unique().one_or_none()
        
        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()            
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)            
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
        
# POST Login
@router.post('/login',
            description='Efetua o login do usuário e devolve o token de acesso.', 
            summary='Login no sistema.', 
            response_description="Login efetuado com sucesso.")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usario = await authenticate(email=form_data.username, passwd=form_data.password, db=db)
    
    if not usario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Dados de acesso incorretos.')
    
    return JSONResponse(content={"access_token": create_access_token(subject=usario.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)