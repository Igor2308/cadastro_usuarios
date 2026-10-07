from fastapi import FastAPI, Depends, Form, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy import Column, Integer, String, text
from sqlalchemy.orm import Session

from backend.database import Base, engine, get_db
from backend.schemas import ClienteCreate, ClienteUpdate


# ==========================================
# CONFIGURAÇÃO DA API
# ==========================================

app = FastAPI(
    title="Cadastro de Clientes"
)

app.add_middleware(
    SessionMiddleware,
    secret_key="chave-secreta-cadastro-clientes"
)

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
    request: Request,
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

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "erro": "Credenciais inválidas."
            }
        )

    request.session["usuario_logado"] = True

    return RedirectResponse(
        url="/cadastro",
        status_code=303
    )

@app.get("/cadastro")
def pagina_cadastro(
    request: Request,
    db: Session = Depends(get_db)
):

    if not request.session.get("usuario_logado"):

        return RedirectResponse(
        url="/",
        status_code=303
    )

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

    db: Session = Depends(get_db)

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
    db: Session = Depends(get_db)
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

    db: Session = Depends(get_db)

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

    db: Session = Depends(get_db)

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

    db: Session = Depends(get_db)

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

