import re
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

# ==========================================
# 1. DEFINIÇÃO DOS TOKENS (Expressões Regulares)
# ==========================================
TOKEN_SPECIFICATION = [
    ('COMENTARIO',   r'#.*'),                    # Comentários de linha única
    ('NUMERO',       r'\d+'),                    # Números inteiros
    ('PALAVRA_RES',  r'\b(se|senao|enquanto|exibir)\b'), # Palavras reservadas
    ('IDENTIFICADOR',r'\b[a-zA-B_][a-zA-Z0-8_]*'), # Identificadores (variáveis)
    ('OP_RELACIONAL',r'==|<=|>=|<|>'),           # Operadores relacionais
    ('OP_ATRIBUICAO',r'='),                      # Operador de atribuição
    ('OP_ARITMETICO',r'[\+\-\*/]'),              # Operadores aritméticos
    ('ABRE_PAR',     r'\('),                     # Abre parênteses
    ('FECHA_PAR',    r'\)'),                     # Fecha parênteses
    ('ABRE_CHAVE',   r'\{'),                     # Abre chaves
    ('FECHA_CHAVE',  r'\}'),                     # Fecha chaves
    ('FIM_LINHA',    r';'),                      # Ponto e vírgula
    ('ESPACO',       r'[ \t\n\r]+'),             # Espaços, tabs e quebras de linha
]

# ==========================================
# 2. FUNÇÃO DE ANÁLISE LÉXICA
# ==========================================
def analisar_codigo_gui():
    # Pega o texto digitado na caixa de entrada
    codigo_fonte = txt_entrada.get("1.0", tk.END)
    
    # Limpa a caixa de saída para o novo resultado
    txt_saida.delete("1.0", tk.END)
    
    regex_combinada = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION)
    
    tokens_encontrados = []
    tabela_simbolos = set()
    
    # Texto que será montado para exibir na tela
    resultado_texto = "=== PASSO A PASSO DA ANÁLISE LÉXICA ===\n"
    
    # Varre o código fonte usando a regex
    for match in re.finditer(regex_combinada, codigo_fonte):
        tipo_token = match.lastgroup
        valor_token = match.group(tipo_token)
        
        if tipo_token == 'ESPACO':
            resultado_texto += f"[Ignorado] Espaço/Quebra de linha.\n"
            continue
        elif tipo_token == 'COMENTARIO':
            resultado_texto += f"[Ignorado] Comentário removido: {valor_token}\n"
            continue
        else:
            resultado_texto += f"[Identificado] Texto: '{valor_token}' -> Token: {tipo_token}\n"
            tokens_encontrados.append((tipo_token, valor_token))
            
            if tipo_token == 'IDENTIFICADOR':
                tabela_simbolos.add(valor_token)
                
    # Monta o relatório final
    resultado_texto += "\n" + "="*40 + "\n"
    resultado_texto += "             RELATÓRIO FINAL\n"
    resultado_texto += "="*40 + "\n\n"
    
    resultado_texto += ">>> LISTA DE TOKENS GERADOS:\n"
    for token in tokens_encontrados:
        resultado_texto += f"  <{token[0]}, \"{token[1]}\">\n"
        
    resultado_texto += "\n>>> TABELA DE SÍMBOLOS:\n"
    if tabela_simbolos:
        for index, simbolo in enumerate(tabela_simbolos, 1):
            resultado_texto += f"  {index}. {simbolo}\n"
    else:
        resultado_texto += "  [Vazia]\n"
        
    # Injeta o texto final na caixa de saída da janela
    txt_saida.insert(tk.END, resultado_texto)

# ==========================================
# 3. CONSTRUÇÃO DA INTERFACE GRÁFICA (GUI)
# ==========================================
# Cria a janela principal
janela = tk.Tk()
janela.title("Case 3 - Analisador Léxico")
janela.geometry("700x600")
janela.configure(bg="#f0f0f0")

# Rótulo de instrução
lbl_entrada = tk.Label(janela, text="Digite ou cole o código fonte aqui:", bg="#f0f0f0", font=("Arial", 10, "bold"))
lbl_entrada.pack(pady=5)

# Caixa de texto para entrada do código (com barra de rolagem)
txt_entrada = scrolledtext.ScrolledText(janela, width=80, height=10, font=("Consolas", 10))
txt_entrada.pack(pady=5)

# Inserir um código de exemplo padrão para facilitar os testes
codigo_exemplo = "# Exemplo de código\nX = 10;\nse (X > 5) {\n    exibir(X);\n}"
txt_entrada.insert(tk.END, codigo_exemplo)

# Botão para acionar a análise
btn_analisar = tk.Button(janela, text="Analisar Código", command=analisar_codigo_gui, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), padx=10, pady=5)
btn_analisar.pack(pady=10)

# Rótulo do resultado
lbl_saida = tk.Label(janela, text="Resultado da Análise Léxica:", bg="#f0f0f0", font=("Arial", 10, "bold"))
lbl_saida.pack(pady=5)

# Caixa de texto para a saída do resultado (com barra de rolagem)
txt_saida = scrolledtext.ScrolledText(janela, width=80, height=18, font=("Consolas", 10), bg="#ffffff")
txt_saida.pack(pady=5)

# Inicia o loop da janela gráfica
janela.mainloop()