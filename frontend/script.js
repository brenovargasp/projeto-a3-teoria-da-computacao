const API_BASE = "/machine";

let sessionId = null;
let credito = 0;
let preco = null;
let doceSelecionado = null;

async function criarSessao() {
  const response = await fetch(`${API_BASE}/session`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Não foi possível criar a sessão.");
  }

  const data = await response.json();
  sessionId = data.session_id;
  credito = data.saldo;
  atualizarTela();
}

async function garantirSessao() {
  if (!sessionId) {
    await criarSessao();
  }
}

function selecionarDoce(btn, nome, valor) {
  document
    .querySelectorAll(".doces button")
    .forEach((b) => b.classList.remove("selecionado"));

  btn.classList.add("selecionado");

  doceSelecionado = nome;
  preco = valor;

  atualizarTela();
}

async function inserir(btn, valor) {
  try {
    if (preco === null) {
      mostrarModal("Escolha um doce primeiro 🍫");
      return;
    }

    await garantirSessao();

    btn.classList.add("ativo");
    setTimeout(() => btn.classList.remove("ativo"), 150);

    const response = await fetch(`${API_BASE}/session/${sessionId}/insert`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ valor }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Erro ao inserir moeda.");
    }

    credito = data.saldo;
    atualizarTela();
  } catch (error) {
    mostrarModal(error.message || "Erro ao inserir moeda.");
  }
}

async function comprar() {
  try {
    if (preco === null || !doceSelecionado) {
      mostrarModal("Selecione um doce");
      return;
    }

    await garantirSessao();

    const response = await fetch(`${API_BASE}/session/${sessionId}/buy`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ doce: doceSelecionado }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Erro ao comprar o doce.");
    }

    credito = data.saldo_final;

    let msg = `🍫 Doce ${data.doce} liberado!`;

    if (data.troco > 0) {
      msg += `\nTroco: R$ ${data.troco}`;
    }

    mostrarModal(msg);
    reset();
  } catch (error) {
    mostrarModal(error.message || "Erro ao comprar o doce.");
  }
}

async function remover() {
  try {
    if (!sessionId) {
      limparEstadoLocal();
      atualizarTela();
      return;
    }

    const response = await fetch(`${API_BASE}/session/${sessionId}/finish`, {
      method: "POST",
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Erro ao cancelar a sessão.");
    }

    let msg = "Sessão cancelada.";

    if (data.troco > 0) {
      msg += `\nTroco devolvido: R$ ${data.troco}`;
    }

    mostrarModal(msg);
    limparEstadoLocal();
    atualizarTela();
  } catch (error) {
    mostrarModal(error.message || "Erro ao cancelar a sessão.");
  }
}

function atualizarTela() {
  document.getElementById("credito").innerText = credito;

  const max = preco || 8;
  const porcentagem = (credito / max) * 100;

  document.getElementById("progresso").style.width =
    Math.min(porcentagem, 100) + "%";

  const btnComprar = document.getElementById("comprarBtn");

  if (preco !== null && credito >= preco) {
    btnComprar.disabled = false;
    btnComprar.classList.add("ativo");
  } else {
    btnComprar.disabled = true;
    btnComprar.classList.remove("ativo");
  }
}

function limparEstadoLocal() {
  sessionId = null;
  credito = 0;
  preco = null;
  doceSelecionado = null;

  document
    .querySelectorAll(".doces button")
    .forEach((b) => b.classList.remove("selecionado"));

  document.getElementById("progresso").style.width = "0%";
}

function reset() {
  setTimeout(() => {
    limparEstadoLocal();
    atualizarTela();
  }, 500);
}

function mostrarModal(texto) {
  document.getElementById("modal-text").innerText = texto;
  document.getElementById("modal").classList.remove("hidden");
}

function fecharModal() {
  document.getElementById("modal").classList.add("hidden");
}

window.addEventListener("load", () => {
  atualizarTela();
});