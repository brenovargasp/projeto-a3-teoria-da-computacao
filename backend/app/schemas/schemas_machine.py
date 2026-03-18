from typing import List, Literal
from pydantic import BaseModel


class SessionStateResponse(BaseModel):
    session_id: str
    saldo: int
    valores_inseridos: List[int]
    doces_disponiveis: List[str]
    status: str


class CreateSessionResponse(SessionStateResponse):
    pass


class InsertMoneyRequest(BaseModel):
    valor: int


class InsertMoneyResponse(SessionStateResponse):
    pass


class BuyCandyRequest(BaseModel):
    doce: Literal["Sorvete", "Bolo", "Cupcake"]


class BuyCandyResponse(BaseModel):
    session_id: str
    doce: str
    preco: int
    saldo_inicial: int
    saldo_final: int
    troco: int
    doces_disponiveis: List[str]
    status: str
    mensagem: str


class FinishSessionResponse(BaseModel):
    session_id: str
    troco: int
    status: str
    mensagem: str