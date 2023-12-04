from typing import Optional
from typing import List
from pydantic import BaseModel as SCBaseModel
from pydantic import EmailStr
from schemas.artigo_shema import ArtigoSchema



class UserSchemaBase(SCBaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    eh_admin: bool = False
    
    class Config:
        from_attributes = True
  
        
class UserSchameCreate(UserSchemaBase):
    senha: str
    

class UserSchemaArtigos(UserSchemaBase):
    artigos: Optional[List[ArtigoSchema]]
    


class UserSchemaUp(UserSchemaBase):
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    eh_admin: Optional[bool] = False
        