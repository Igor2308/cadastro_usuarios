from fastapi import FastAPI, Depends, Form, Request, Header, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy import Column, Integer, String, text
from sqlalchemy.orm import Session
import secrets
from backend.database import Base, engine, get_db
from backend.schemas import ClienteCreate, ClienteUpdate


# ==========================================
# CONFIGURAÇÃO DA API
# ==========================================

app = FastAPI(
    title="Cadastro de Clientes"
)

tokens_sessoes = set()

# Verifica se o token existe e ainda é válido
def validar_token(
    authorization: str | None = Header(default=None)
):
    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail="Sessão não informada."
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Token inválido."
        )

    token = authorization.replace(
        "Bearer ",
        "",
        1
    )

    if token not in tokens_sessoes:
        raise HTTPException(
            status_code=401,
            detail="Sessão inválida ou expirada."
        )

    return token

# ==========================================
# ARQUIVOS DO FRONTEND
# ==========================================

# Libera acesso aos arquivos CSS
app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)


# Local onde estão os arquivos HTML
templates = Jinja2Templates(
    directory="frontend/html"
)


# ==========================================
# MODELO DO CLIENTE
# ==========================================

class Cliente(Base):

    __tablename__ = "clientes"


    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )


    nome = Column(
        String(100),
        nullable=False
    )


    email = Column(
        String(100),
        nullable=False,
        unique=True
    )


    telefone = Column(
        String(20),
        nullable=True
    )


    cidade = Column(
        String(100),
        nullable=True
    )


# Cria as tabelas caso elas ainda não existam
Base.metadata.create_all(
    bind=engine
)


# ==========================================
# PÁGINA PRINCIPAL
# ==========================================

@app.get("/")
def pagina_login(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.post("/login")
def fazer_login(
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    usuario = db.execute(
        text(
            "SELECT * FROM usuarios "
            "WHERE email = :email AND senha = :senha"
        ),
        {
            "email": email,
            "senha": senha
        }
    ).fetchone()

    if usuario is None:
        return {
            "sucesso": False,
            "erro": "Credenciais inválidas."
        }

    # Gera um token exclusivo para esta sessão
    token = secrets.token_urlsafe(32)

    # Guarda o token como sessão válida
    tokens_sessoes.add(token)

    return {
        "sucesso": True,
        "token": token
    }

# ==========================================
# VALIDAR SESSÃO
# ==========================================

@app.get("/validar-sessao")
def validar_sessao(
    token: str = Depends(validar_token)
):
    return {
        "sucesso": True
    }

@app.get("/cadastro")
def pagina_cadastro(
    request: Request,
    db: Session = Depends(get_db)
):
    clientes = db.query(Cliente).all()

    return templates.TemplateResponse(
        request=request,
        name="cadastro.html",
        context={
            "clientes": clientes
        }
    )

# ==========================================
# CADASTRAR CLIENTE
# ==========================================

@app.post("/clientes")
def cadastrar_cliente(

    nome: str = Form(...),

    email: str = Form(...),

    telefone: str = Form(...),

    cidade: str = Form(...),

    db: Session = Depends(get_db),

    token: str = Depends(validar_token)

):

    # Cria o cliente
    cliente = Cliente(

        nome=nome,

        email=email,

        telefone=telefone,

        cidade=cidade

    )


    # Adiciona o cliente ao banco
    db.add(cliente)

    db.commit()

    db.refresh(cliente)


    # Volta para a página principal
    return RedirectResponse(
        url="/cadastro",
        status_code=303
    )


# ==========================================
# LISTAR CLIENTES
# ==========================================

@app.get("/clientes")
def listar_clientes(
    db: Session = Depends(get_db),
    token: str = Depends(validar_token)
):

    return db.query(
        Cliente
    ).all()


# ==========================================
# BUSCAR CLIENTE
# ==========================================

@app.get("/clientes/{cliente_id}")
def buscar_cliente(

    cliente_id: int,

    db: Session = Depends(get_db),

    token: str = Depends(validar_token)

):

    cliente = db.query(
        Cliente
    ).filter(
        Cliente.id == cliente_id
    ).first()


    if cliente is None:

        return {
            "erro": "Cliente não encontrado"
        }


    return cliente


# ==========================================
# ATUALIZAR CLIENTE
# ==========================================

@app.put("/clientes/{cliente_id}")
def atualizar_cliente(

    cliente_id: int,

    cliente_data: ClienteUpdate,

    db: Session = Depends(get_db),

    token: str = Depends(validar_token)

):

    cliente = db.query(
        Cliente
    ).filter(
        Cliente.id == cliente_id
    ).first()


    if cliente is None:

        return {
            "erro": "Cliente não encontrado"
        }


    cliente.nome = cliente_data.nome

    cliente.email = cliente_data.email

    cliente.telefone = cliente_data.telefone

    cliente.cidade = cliente_data.cidade


    db.commit()

    db.refresh(cliente)


    return cliente


# ==========================================
# EXCLUIR CLIENTE
# ==========================================

@app.delete("/clientes/{cliente_id}")
def excluir_cliente(

    cliente_id: int,

    db: Session = Depends(get_db),

    token: str = Depends(validar_token)

):

    cliente = db.query(
        Cliente
    ).filter(
        Cliente.id == cliente_id
    ).first()


    if cliente is None:

        return {
            "erro": "Cliente não encontrado"
        }


    db.delete(cliente)

    db.commit()


    return {
        "mensagem": "Cliente excluído com sucesso"
    }

