document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.getElementById('chat-box');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    
    // Correct WebSocket URL based on the protocol

    const socket = new WebSocket("wss://airvistaj.onrender.com/ws/chat/");

    // Connection status indicators
    const connectionStatus = document.createElement('div');
    connectionStatus.id = 'connection-status';
    chatBox.parentNode.insertBefore(connectionStatus, chatBox);

    function updateStatus(connected) {
        connectionStatus.textContent = connected ? 'Connected' : 'Disconnected';
        connectionStatus.className = connected ? 'connected' : 'disconnected';
        messageInput.disabled = !connected;
        sendButton.disabled = !connected;
    }

    socket.onopen = function() {
        updateStatus(true);
    };

    socket.onclose = function() {
        updateStatus(false);
    };

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.type === 'history') {
            data.messages.reverse().forEach(msg => appendMessage(msg));
        } else if (data.type === 'message') {
            appendMessage(data);
        }
    };

    function appendMessage(data) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message';
        messageDiv.innerHTML = `
            <span class="timestamp">${new Date(data.timestamp).toLocaleString()}</span>
            <span class="username">${data.username}:</span>
            <span class="message-text">${data.message}</span>
        `;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    sendButton.addEventListener('click', function() {
        const message = messageInput.value.trim();
        if (message && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({
                message: message,
                username: window.CHAT_CONFIG.username
            }));
            messageInput.value = '';
        }
    });

    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendButton.click();
        }
    });
});
