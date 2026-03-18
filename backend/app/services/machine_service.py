import uuid

from backend.app.core.constants import (
    DOCES,
    VALORES_PERMITIDOS,
    STATUS_AGUARDANDO_PAGAMENTO,
    STATUS_AGUARDANDO_ESCOLHA,
    STATUS_FINALIZADO,
    MSG_SESSAO_NAO_ENCONTRADA,
    MSG_SESSAO_FINALIZADA,
    MSG_VALOR_INVALIDO,
    MSG_DOCE_INVALIDO,
    MSG_SALDO_INSUFICIENTE,
    MSG_COMPRA_SUCESSO,
    MSG_SESSAO_ENCERRADA,
)


class MachineService:
    def __init__(self):
        self.sessions: dict[str, dict] = {}

    def create_session(self) -> dict:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = self._new_session_data()
        return self._build_state(session_id)

    def get_session(self, session_id: str) -> dict:
        self._get_existing_session(session_id)
        return self._build_state(session_id)

    def insert_money(self, session_id: str, valor: int) -> dict:
        if valor not in VALORES_PERMITIDOS:
            raise ValueError(MSG_VALOR_INVALIDO)

        session = self._get_existing_session(session_id)
        self._ensure_session_not_finished(session)

        session["saldo"] += valor
        session["valores_inseridos"].append(valor)
        session["status"] = self._calculate_status(session["saldo"])

        return self._build_state(session_id)

    def buy_candy(self, session_id: str, doce: str) -> dict:
        session = self._get_existing_session(session_id)
        self._ensure_session_not_finished(session)

        if doce not in DOCES:
            raise ValueError(MSG_DOCE_INVALIDO)

        preco = DOCES[doce]
        saldo_inicial = session["saldo"]

        if saldo_inicial < preco:
            raise ValueError(MSG_SALDO_INSUFICIENTE)

        saldo_final = saldo_inicial - preco
        session["saldo"] = saldo_final
        session["status"] = self._calculate_status(saldo_final)

        return {
            "session_id": session_id,
            "doce": doce,
            "preco": preco,
            "saldo_inicial": saldo_inicial,
            "saldo_final": saldo_final,
            "troco": saldo_final,
            "doces_disponiveis": self._available_candies(saldo_final),
            "status": session["status"],
            "mensagem": MSG_COMPRA_SUCESSO,
        }

    def finish_session(self, session_id: str) -> dict:
        session = self._get_existing_session(session_id)
        self._ensure_session_not_finished(session)

        troco = session["saldo"]
        session["saldo"] = 0
        session["status"] = STATUS_FINALIZADO

        return {
            "session_id": session_id,
            "troco": troco,
            "status": session["status"],
            "mensagem": MSG_SESSAO_ENCERRADA,
        }

    def _new_session_data(self) -> dict:
        return {
            "saldo": 0,
            "valores_inseridos": [],
            "status": STATUS_AGUARDANDO_PAGAMENTO,
        }

    def _get_existing_session(self, session_id: str) -> dict:
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(MSG_SESSAO_NAO_ENCONTRADA)
        return session

    def _ensure_session_not_finished(self, session: dict) -> None:
        if session["status"] == STATUS_FINALIZADO:
            raise ValueError(MSG_SESSAO_FINALIZADA)

    def _available_candies(self, saldo: int) -> list[str]:
        return [nome for nome, preco in DOCES.items() if saldo >= preco]

    def _calculate_status(self, saldo: int) -> str:
        if self._available_candies(saldo):
            return STATUS_AGUARDANDO_ESCOLHA
        return STATUS_AGUARDANDO_PAGAMENTO

    def _build_state(self, session_id: str) -> dict:
        session = self._get_existing_session(session_id)
        return {
            "session_id": session_id,
            "saldo": session["saldo"],
            "valores_inseridos": session["valores_inseridos"],
            "doces_disponiveis": self._available_candies(session["saldo"]),
            "status": session["status"],
        }