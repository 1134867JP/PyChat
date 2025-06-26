document.addEventListener("DOMContentLoaded", () => {
    const messageList = document.getElementById('message-list');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');

    let userName = "";

    function promptForUserName() {
        userName = prompt("Por favor, digite seu nome para entrar no chat:");
        if (!userName || userName.trim() === "") {
            userName = "Anônimo";
        }
    }

    promptForUserName();

    const socket = new WebSocket('ws://localhost:8765');

    function addMessageToUI({ type, user, text, timestamp }) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        
        let messageContent = '';
        
        if (type === 'join') {
            messageElement.classList.add('system');
            messageContent = `<div><strong>${user}</strong> entrou na sala.</div>`;
        } else {
            if (user === userName) {
                messageElement.classList.add('sent');
                messageContent = `
                    <div class="text">${text}</div>
                    <div class="meta">
                        <span class="timestamp">${timestamp}</span>
                    </div>
                `;
            } else {
                messageElement.classList.add('received');
                messageContent = `
                    <div class="user-name">${user}</div>
                    <div class="text">${text}</div>
                    <div class="meta">
                        <span class="timestamp">${timestamp}</span>
                    </div>
                `;
            }
        }
        
        messageElement.innerHTML = messageContent;
        messageList.appendChild(messageElement);

        messageList.scrollTop = messageList.scrollHeight;
    }

    socket.onopen = () => {
        console.log("Conectado ao servidor de chat!");
        const joinMessage = {
            type: 'join',
            user: userName
        };
        socket.send(JSON.stringify(joinMessage));
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        addMessageToUI(data);
    };

    socket.onclose = () => {
        console.log("Desconectado do servidor de chat.");
        addMessageToUI({ type: 'system', text: 'Você foi desconectado.' });
    };

    socket.onerror = (error) => {
        console.error("Erro no WebSocket:", error);
        addMessageToUI({ type: 'system', text: 'Erro de conexão com o servidor.' });
    };

    messageForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const messageText = messageInput.value.trim();

        if (messageText && socket.readyState === WebSocket.OPEN) {
            const messageData = {
                type: 'message',
                user: userName,
                text: messageText
            };
            socket.send(JSON.stringify(messageData));
            messageInput.value = '';
        }
    });
});