// Função para rolar o dado
function rolarDado() {
    const dado = document.getElementById("dado");
    const numero = Math.floor(Math.random() * 6) + 1; // Gera um número entre 1 e 6

    // Limpa o dado antes de gerar as bolinhas
    dado.innerHTML = "";

    // Adiciona as bolinhas conforme o número
    const bolinhasPosicoes = {
        1: [[50, 50]],
        2: [[25, 25], [75, 75]],
        3: [[25, 25], [50, 50], [75, 75]],
        4: [[25, 25], [25, 75], [75, 25], [75, 75]],
        5: [[25, 25], [25, 75], [50, 50], [75, 25], [75, 75]],
        6: [[25, 25], [25, 50], [25, 75], [75, 25], [75, 50], [75, 75]]
    };

    bolinhasPosicoes[numero].forEach(([top, left]) => {
        const bolinha = document.createElement("div");
        bolinha.className = "bolinha";
        bolinha.style.top = `${top}%`;
        bolinha.style.left = `${left}%`;
        dado.appendChild(bolinha);
    });
}

// Lista de perguntas
const listaPerguntas = [];

// Função para adicionar perguntas
function adicionarPergunta() {
    const pergunta = document.getElementById("nova-pergunta").value;
    if (pergunta.trim()) {
        listaPerguntas.push(pergunta.trim());
        atualizarListaPerguntas();
        document.getElementById("nova-pergunta").value = ""; // Limpa o campo
    }
}

// Função para atualizar a lista de perguntas
function atualizarListaPerguntas() {
    const lista = document.getElementById("lista-perguntas");
    lista.innerHTML = ""; // Limpa a lista
    listaPerguntas.forEach((pergunta, index) => {
        const li = document.createElement("li");
        li.textContent = `${index + 1}. ${pergunta}`;
        lista.appendChild(li);
    });
}
