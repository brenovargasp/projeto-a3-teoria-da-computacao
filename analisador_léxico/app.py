import re
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# ==========================================
# INICIALIZAÇÃO DO FASTAPI
# ==========================================

app = FastAPI(title="Lexical Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# CAMINHOS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

# Configuração do Jinja2
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ==========================================
# EXPRESSÕES REGULARES DOS TOKENS
# ==========================================

TOKEN_REGEX = [
    ('COMMENT', r'//.*|/\*[\s\S]*?\*/'),
    ('WHITESPACE', r'\s+'),
    ('KEYWORD', r'\b(if|else|while|for|return|int|float|void|print)\b'),
    ('NUMBER', r'\b\d+(\.\d+)?\b'),
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('OPERATOR', r'[+\-*/=<>!&|]+'),
    ('SYMBOL', r'[(){}\[\],;]'),
    ('MISMATCH', r'.'),
]

# ==========================================
# FUNÇÃO DE ANÁLISE LÉXICA
# ==========================================

def analyze_code(code: str):
    tokens = []
    symbol_table = {}
    eliminated = []

    pos = 0
    line = 1

    while pos < len(code):
        match = None

        for token_type, regex in TOKEN_REGEX:
            pattern = re.compile(regex)
            match = pattern.match(code, pos)

            if match:
                value = match.group(0)

                if token_type == 'WHITESPACE':
                    line += value.count('\n')

                    eliminated.append({
                        'type': 'Espaço/Quebra de Linha',
                        'value': repr(value)
                    })

                elif token_type == 'COMMENT':
                    line += value.count('\n')

                    eliminated.append({
                        'type': 'Comentário',
                        'value': value
                    })

                elif token_type == 'MISMATCH':
                    tokens.append({
                        'type': 'ERRO_LEXICO',
                        'value': value,
                        'line': line
                    })

                else:
                    tokens.append({
                        'type': token_type,
                        'value': value,
                        'line': line
                    })

                    if token_type == 'IDENTIFIER':
                        if value not in symbol_table:
                            symbol_table[value] = {
                                'type': 'Variável/Função',
                                'lines': [line]
                            }

                        elif line not in symbol_table[value]['lines']:
                            symbol_table[value]['lines'].append(line)

                pos = match.end()
                break

        if not match:
            pos += 1

    return tokens, symbol_table, eliminated

# ==========================================
# MODEL DE ENTRADA
# ==========================================

class CodeRequest(BaseModel):
    code: str

# ==========================================
# ROTA PRINCIPAL
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

# ==========================================
# ROTA DE ANÁLISE
# ==========================================

@app.post("/analyze")
async def analyze(data: CodeRequest):

    tokens, symbol_table, eliminated = analyze_code(data.code)

    return {
        "tokens": tokens,
        "symbol_table": [
            {
                "name": k,
                "details": v
            }
            for k, v in symbol_table.items()
        ],
        "eliminated": eliminated
    }
