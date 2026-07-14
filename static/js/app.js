let currentChat = null;

const chatList = document.getElementById("chatList");
const messages = document.getElementById("messages");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const newChatBtn = document.getElementById("newChatBtn");

// Load all chats
async function loadChats() {
    const response = await fetch("/api/chats");
    const chats = await response.json();

    chatList.innerHTML = "";

    chats.forEach(chat => {
        const item = document.createElement("div");
        item.className = "chat-item";

        if (chat._id === currentChat) {
            item.classList.add("active");
        }

        item.textContent = chat.title;

        item.onclick = () => {
            openChat(chat._id);
        };

        chatList.appendChild(item);
    });

    if (!currentChat && chats.length > 0) {
        openChat(chats[0]._id);
    }
}

// Create a new chat
async function newChat() {
    const response = await fetch("/api/chat/new", {
        method: "POST"
    });

    const chat = await response.json();

    currentChat = chat._id;
    messages.innerHTML = "";

    loadChats();
}

// Open an existing chat
async function openChat(chatId) {
    currentChat = chatId;

    const response = await fetch(`/api/chat/${chatId}`);
    const chat = await response.json();

    renderMessages(chat.messages || []);

    loadChats();
}

// Render all messages
function renderMessages(chatMessages) {
    messages.innerHTML = "";

    chatMessages.forEach(msg => {
        addMessage(msg.role, msg.content);
    });

    scrollBottom();
}

// Add one message
function addMessage(role, text) {

    const div = document.createElement("div");
    div.className = `message ${role}`;

    div.innerHTML = marked.parse(text);

    div.querySelectorAll("pre code").forEach((block) => {
        hljs.highlightElement(block);
    });

    messages.appendChild(div);

    scrollBottom();
}

// Send message
async function sendMessage() {

    if (!currentChat) {
        await newChat();
    }

    const text = messageInput.value.trim();

    if (text === "") return;

    addMessage("user", text);

    messageInput.value = "";

    const typing = document.createElement("div");
    typing.className = "typing";
    typing.textContent = "Thinking...";

    messages.appendChild(typing);

    scrollBottom();

    const response = await fetch(`/api/chat/${currentChat}/message`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: text
        })
    });

    const data = await response.json();

    typing.remove();

    if (data.reply) {
        addMessage("assistant", data.reply);
    } else {
        addMessage("assistant", "An error occurred.");
    }

    loadChats();
}

// Scroll to bottom
function scrollBottom() {
    messages.scrollTop = messages.scrollHeight;
}

// Events
sendBtn.addEventListener("click", sendMessage);

newChatBtn.addEventListener("click", newChat);

messageInput.addEventListener("keydown", function (event) {

    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }

});

// Initial load
loadChats();
typing.className="typing";
typing.textContent="Thinking";
messageInput.addEventListener("input",()=>{

messageInput.style.height="auto";
messageInput.style.height=messageInput.scrollHeight+"px";

});
const themeBtn = document.getElementById("themeToggle");

// Restore saved theme
const savedTheme = localStorage.getItem("theme");

if(savedTheme==="light"){
    document.body.classList.add("light");
    themeBtn.textContent="☀️";
}

themeBtn.addEventListener("click",()=>{

    document.body.classList.toggle("light");

    if(document.body.classList.contains("light")){

        themeBtn.textContent="☀️";
        localStorage.setItem("theme","light");

    }else{

        themeBtn.textContent="🌙";
        localStorage.setItem("theme","dark");

    }

});	

