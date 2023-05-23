// Function to clear chat history by sending a POST request to the '/clear_history' route
function clearHistory() {
    $.post('/clear_history', {}, function(data) {
        console.log('History cleared');
    });
}

// Clear chat history when the document is ready
$(document).ready(function() {
    clearHistory();
});

// Initialize the Markdown renderer
var renderer = new marked.Renderer();

// Add an event listener to the chat form submission
document.getElementById('chat-form').addEventListener('submit', async event => {
    event.preventDefault();
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();
    if (message) {
        addMessage('user', message);
        chatInput.value = '';
        const botMessageElement = addMessage('bot', '');
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ chat_input: message })
        });
        const data = await response.json();
        updateBotMessage(botMessageElement, data.response);
    }
});

// Function to add a message to the chat window
function addMessage(sender, message) {
    const chatMessages = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    
    const preElement = document.createElement('p');
    preElement.textContent = `${sender}: ${message}`;
    messageElement.appendChild(preElement);
    
    // Add a loading animation for bot messages
    if (sender === 'bot') {
        const loadingElement = document.createElement('div');
        loadingElement.classList.add('loader');
        messageElement.appendChild(loadingElement);
    }

    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return messageElement;
}

// Function to update the bot message with the generated response
function updateBotMessage(botMessageElement, newMessage) {
    const preElement = botMessageElement.querySelector('p');
    newMessage = 'bot: ' + newMessage;
    preElement.innerHTML = marked.parse(newMessage);
    const loadingElement = botMessageElement.querySelector('.loader');
    botMessageElement.removeChild(loadingElement);
}
