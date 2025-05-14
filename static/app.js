// changegayani7/5/2025
class Chatbox {
    constructor() {
        this.args = {
            openButton: document.getElementById('chat-toggle'),
            chatBox: document.getElementById('chatbot-box'),
            sendButton: document.getElementById('send-button'),
            userInput: document.getElementById('user-input'),
            messageContainer: document.getElementById('chatbot-messages'),
            closeButton: document.getElementById('chatbot-close')
        };

        this.state = false;
        this.messages = [];
    }

    display() {
        const { openButton, chatBox, sendButton, userInput, closeButton } = this.args;

        openButton.addEventListener('click', () => this.toggleState());
        closeButton.addEventListener('click', () => this.toggleState(false));

        sendButton.addEventListener('click', () => this.onSendMessage());
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.onSendMessage();
        });
    }

    toggleState(forceClose = null) {
        const chatBox = this.args.chatBox;

        if (forceClose === true) {
            this.state = false;
        } else if (forceClose === false) {
            this.state = true;
        } else {
            this.state = !this.state;
        }

        chatBox.classList.toggle('active', this.state);
    }

    // onSendMessage() {
    //     const { userInput, messageContainer } = this.args;
    //     const text = userInput.value.trim();
    //     if (text === "") return;

    onSendButton(chatBox) {
        var textField = chatbox.querySelector('input');
        let text = textField.value
        if (text === "") {
            return;
        }

        this.addMessage('User', text);

        const typingDiv = document.createElement("div");
        typingDiv.classList.add("bot-message", "typing-indicator");
        typingDiv.innerHTML = `<p>Typing...</p>`;
        messageContainer.appendChild(typingDiv);
        this.scrollToBottom();

        fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text }),
        })
        .then(res => res.json())
        .then(data => {
            const typingDivs = document.querySelectorAll('.typing-indicator');
            typingDivs.forEach(div => messageContainer.removeChild(div));
            this.addMessage('TechTara', data.answer);
        })
        .catch(err => {
            console.error("Error:", err);
            const typingDivs = document.querySelectorAll('.typing-indicator');
            typingDivs.forEach(div => messageContainer.removeChild(div));
            this.addMessage('TechTara', "Oops! Something went wrong. Please try again.");
        });

        userInput.value = "";
    }

    addMessage(sender, message) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add(sender === 'User' ? 'user-message' : 'bot-message');
        msgDiv.innerHTML = `<p>${message}</p>`;
        this.args.messageContainer.appendChild(msgDiv);
        this.scrollToBottom();
    }

    scrollToBottom() {
        const msgBox = this.args.messageContainer;
        msgBox.scrollTop = msgBox.scrollHeight;
    }
}

const chatbox = new Chatbox();
chatbox.display();
