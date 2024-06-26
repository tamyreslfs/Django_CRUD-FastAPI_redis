document.addEventListener('DOMContentLoaded', function() {
    // Aqui você pode adicionar mais lógica conforme necessário para interagir com o WebSocket e manipular o DOM do chat.
    const socket = new WebSocket('ws://localhost:8001/ws');

    socket.onmessage = function(event) {
        const messages = document.getElementById('messages');
        const message = document.createElement('li');
        const content = document.createTextNode(event.data);
        message.appendChild(content);
        message.classList.add('message', 'received'); // Adiciona classes para mensagens recebidas
        messages.appendChild(message);
    };

    function sendMessage(event) {
        const input = document.getElementById("messageText");
        if (input.value.trim() !== "") {
            socket.send(input.value);

            const messages = document.getElementById('messages');
            const message = document.createElement('li');
            const content = document.createTextNode(input.value);
            message.appendChild(content);
            message.classList.add('message', 'sent'); // Adiciona classes para mensagens enviadas
            messages.appendChild(message);

            input.value = '';
        }
        event.preventDefault();
    }

    // Liga a função sendMessage ao evento submit do formulário
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', sendMessage);
    } else {
        console.error('Formulário não encontrado!');
    }
});

const element = document.getElementById('seuElemento');
if (element) {
    element.classList.add('suaClasse');
} else {
    console.error('Elemento não encontrado!');
}
