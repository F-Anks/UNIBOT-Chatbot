const userInput = document.getElementById('userInput');
const chatWindow = document.getElementById('chat-window');

userInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    const messageText = userInput.value.trim();
    if (messageText === '') return;

    appendMessage(messageText, 'user');
    userInput.value = '';

    try {
        const response = await fetch('/api/chat', { // <-- Usaremos esta ruta
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: messageText }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        appendMessage(data.response, 'bot');
    } catch (error) {
        console.error('Error al contactar al bot:', error);
        appendMessage('Lo siento, hubo un error de conexión con la API.', 'bot');
    }
}

function appendMessage(text, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${sender}-message`);
    messageElement.textContent = text;
    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}