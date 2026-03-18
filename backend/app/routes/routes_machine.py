from fastapi import APIRouter, HTTPException

from backend.app.schemas.schemas_machine import (
    BuyCandyRequest,
    BuyCandyResponse,
    CreateSessionResponse,
    FinishSessionResponse,
    InsertMoneyRequest,
    InsertMoneyResponse,
    SessionStateResponse,
)
from backend.app.services.machine_service import MachineService

router = APIRouter(prefix="/machine", tags=["Machine"])
service = MachineService()


@router.post("/session", response_model=CreateSessionResponse)
def create_session():
    return service.create_session()


@router.get("/session/{session_id}", response_model=SessionStateResponse)
def get_session(session_id: str):
    try:
        return service.get_session(session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/session/{session_id}/insert", response_model=InsertMoneyResponse)
def insert_money(session_id: str, body: InsertMoneyRequest):
    try:
        return service.insert_money(session_id, body.valor)
    except ValueError as e:
        detail = str(e)
        status_code = 404 if detail == "Sessão não encontrada." else 400
        raise HTTPException(status_code=status_code, detail=detail)


@router.post("/session/{session_id}/buy", response_model=BuyCandyResponse)
def buy_candy(session_id: str, body: BuyCandyRequest):
    try:
        return service.buy_candy(session_id, body.doce)
    except ValueError as e:
        detail = str(e)
        status_code = 404 if detail == "Sessão não encontrada." else 400
        raise HTTPException(status_code=status_code, detail=detail)


@router.post("/session/{session_id}/finish", response_model=FinishSessionResponse)
def finish_session(session_id: str):
    try:
        return service.finish_session(session_id)
    except ValueError as e:
        detail = str(e)
        status_code = 404 if detail == "Sessão não encontrada." else 400
        raise HTTPException(status_code=status_code, detail=detail)