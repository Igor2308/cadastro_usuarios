from pydantic import BaseModel, EmailStr, Field


# Dados utilizados para cadastrar um cliente
class ClienteCreate(BaseModel):

    nome: str = Field(
        min_length=1,
        max_length=100
    )

    email: EmailStr

    telefone: str | None = Field(
        default=None,
        max_length=20
    )

    cidade: str | None = Field(
        default=None,
        max_length=100
    )


# Dados utilizados para atualizar um cliente
class ClienteUpdate(BaseModel):

    nome: str = Field(
        min_length=1,
        max_length=100
    )

    email: EmailStr

    telefone: str | None = Field(
        default=None,
        max_length=20
    )

    cidade: str | None = Field(
        default=None,
        max_length=100
    )


# Dados devolvidos pela API
class ClienteResponse(BaseModel):

    id: int
    nome: str
    email: str
    telefone: str | None
    cidade: str | None

    class Config:
        from_attributes = True