document.addEventListener("DOMContentLoaded", function () {

    const chatIcon = document.getElementById("chat-icon");
    const chatWindow = document.getElementById("chat-window");
    const closeBtn = document.getElementById("close-chat");

    const sendBtn = document.getElementById("send-btn");
    const userInput = document.getElementById("user-input");
    const chatBody = document.getElementById("chat-body");

    // Open Chat
    chatIcon.onclick = function () {
        chatWindow.style.display = "flex";
        chatIcon.style.display = "none";
    };

    // Close Chat
    closeBtn.onclick = function () {
        chatWindow.style.display = "none";
        chatIcon.style.display = "flex";
    };

    // Send Button
    sendBtn.onclick = sendMessage;

    // Enter Key
    userInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });

    function sendMessage() {

        const message = userInput.value.trim();

        if (message === "")
            return;

        addUserMessage(message);

        userInput.value = "";

        addBotMessage("Thinking...");

        fetch("/chat/", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        })

        .then(response => response.json())

        .then(data => {

            chatBody.lastChild.remove();

            addBotMessage(data.reply);

        })

        .catch(error => {

            chatBody.lastChild.remove();

            addBotMessage("Server Error.");

            console.log(error);

        });

    }

    function addUserMessage(message) {

        const div = document.createElement("div");

        div.className = "user-message";

        div.innerText = message;

        chatBody.appendChild(div);

        chatBody.scrollTop = chatBody.scrollHeight;

    }

    function addBotMessage(message) {

        const div = document.createElement("div");

        div.className = "bot-message";

        div.innerText = message;

        chatBody.appendChild(div);

        chatBody.scrollTop = chatBody.scrollHeight;

    }

});