document.getElementById("openChatBtn").addEventListener("click", function() {
    const chatPopup = document.getElementById("chatPopup");
    chatPopup.style.display = "block";
    setTimeout(() => {
        chatPopup.classList.add("show");
        document.getElementById("chat-body").scrollTop = document.getElementById("chat-body").scrollHeight;
    }, 10);
});

document.getElementById("closeChatBtn").addEventListener("click", function() {
    const chatPopup = document.getElementById("chatPopup");
    chatPopup.classList.remove("show");
    setTimeout(() => {
        chatPopup.style.display = "none";
    }, 300); // Matches the CSS transition duration
});

document.getElementById("sendBtn").addEventListener("click", function() {
    sendMessage1();
});

document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage1();
    }
});

const policyLinks = {
    op1: "/guide#Code-of-Conduct",
    op2: "/guide#Time-Off-Policy",
    op3: "/guide#Remote-Work-Policy",
    op4: "/guide#Performance-Management-Policy",
    op5: "/guide#Intellectual-Property-Policy",
    op6: "/guide#Anti-Discrimination-and-Harassment-Policy",
    op7: "/guide#Health-and-Safety-Policy",
    op8: "/guide#IT-Security-Policy",
    op9: "/guide#Customer-Site-Visit-Policy",
    op10: "/guide#Bring-Your-Own-System-(BYOS)-Computer-Policy",
    op11: "/guide#Daily-Work-Shift-Policy",
    op12: "/guide#Annual-Appraisal-Policy",
    op13: "/guide#Notice-Period"
};

for (let id in policyLinks) {
    document.getElementById(id).addEventListener("click", function() {
        const message = `You can view the ${this.textContent} here: <a href="${policyLinks[id]}" target="_blank">${this.textContent}</a>`;
        appendMessage('bot', message);
    });
}

async function sendMessage1() {
    const userInput = document.getElementById('user-input').value;
    if (!userInput) return;

    // Display user message
    appendMessage('user', userInput);

    // Send request to the backend
    const response = await fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: userInput })
    });

    const data = await response.json();
    if (data.error) {
        appendMessage('bot', 'Error: ' + data.error);
    } else {
        appendMessage('bot', data.result);
    }

    // Clear input field
    document.getElementById('user-input').value = '';
}

function appendMessage(sender, message) {
    const chatBody = document.getElementById('chat-body');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', sender);

    const avatarElement = document.createElement('div');
    avatarElement.classList.add('avatar');
    avatarElement.textContent = sender === 'user' ? 'U' : 'B';

    const textElement = document.createElement('div');
    textElement.classList.add('message');
    textElement.innerHTML = message;

    messageElement.appendChild(avatarElement);
    messageElement.appendChild(textElement);
    chatBody.appendChild(messageElement);

    // Scroll to the bottom
    chatBody.scrollTop = chatBody.scrollHeight;
}
