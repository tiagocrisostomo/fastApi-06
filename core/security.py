from passlib.context import CryptContext


CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(passwd: str, hash_passwd: str) -> bool:    
    """_summary_
    Função que verificar se a senha está correta, comaparando a senha em texto puro, informada pelo usuário,
    e o hash da senha que estará salvo no banco de dados durante a criação da conta.

    Args:
        passwd (str): _description_
        hash_passwd (str): _description_

    Returns:
        bool: _description_
    """
    return CRIPTO.verify(passwd, hash_passwd)

def generate_hash(passwd: str) -> str:
    """_summary_
    Função que gera o retorno o hash da senha.
    
    Args:
        passwd (str): _description_

    Returns:
        str: _description_
    """
    return CRIPTO.hash(passwd)
