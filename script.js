const dice = document.getElementById('dice');
const rollButton = document.getElementById('rollButton');
const result = document.getElementById('result');
const question = document.getElementById('question');

// Lista de questões para cada número
const questions = {
    1: "Qual é a sua cor favorita?",
    2: "Qual foi o último filme que você assistiu?",
    3: "Se pudesse visitar qualquer lugar no mundo, para onde iria?",
    4: "Qual é seu prato favorito?",
    5: "Qual é o seu maior sonho?",
    6: "Se pudesse ter um superpoder, qual seria?"
};

// Função para rolar o dado e exibir o resultado
function rollDice() {
    // Gera um número aleatório entre 1 e 6
    const randomNumber = Math.floor(Math.random() * 6) + 1;

    // Simula o movimento do dado
    dice.textContent = '?';
    dice.style.transition = 'transform 1s';
    dice.style.transform = 'rotate(360deg)';

    // Após 1 segundo, exibe o resultado
    setTimeout(() => {
        dice.style.transform = 'rotate(0deg)';
        dice.textContent = randomNumber;
        result.textContent = `Você rolou o número ${randomNumber}`;
        question.textContent = questions[randomNumber];
    }, 1000);
}

// Adiciona evento ao botão
rollButton.addEventListener('click', rollDice);
