import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

API_BASE_URL = "http://ujk14cj8.rpcld.net/api/v1"  # HTTPS yerine HTTP kullanıyoruz
API_KEY = os.getenv("API_KEY")

def send_chat_message(message, mode="chat", session_id=None):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "message": message,
        "mode": mode,
        "sessionId": session_id or "default-session"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/workspace/benim_calisma_alanim/chat",
            headers=headers,
            json=payload,
            verify=False,  # Disable SSL verification
            proxies={"http": None, "https": None}  # Disable proxy
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message")
    session_id = data.get("session_id")
    
    if not message:
        return jsonify({"error": "Mesaj boş olamaz"}), 400
    
    response = send_chat_message(message, session_id=session_id)
    return jsonify(response)

@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>Yalıtım Bilgileri Chatbot</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    max-width: 800px; 
                    margin: 0 auto; 
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                #chat-container { 
                    height: 400px; 
                    border: 1px solid #ddd; 
                    border-radius: 8px;
                    overflow-y: auto; 
                    padding: 20px; 
                    margin-bottom: 20px;
                    background-color: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                #message-input { 
                    width: 70%; 
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    margin-right: 10px;
                }
                .action-button {
                    padding: 10px 20px;
                    border: none;
                    border-radius: 4px;
                    background-color: #007bff;
                    color: white;
                    cursor: pointer;
                    margin: 0 5px;
                }
                .action-button:hover {
                    background-color: #0056b3;
                }
                .message {
                    margin: 10px 0;
                    padding: 10px;
                    border-radius: 4px;
                    max-width: 80%;
                }
                .user-message {
                    background-color: #e3f2fd;
                    margin-left: auto;
                    margin-right: 0;
                    font-weight: bold;
                }
                .bot-message {
                    background-color: #f5f5f5;
                    margin-right: auto;
                    margin-left: 0;
                    white-space: pre-line;
                }
                .message-container {
                    display: flex;
                    flex-direction: column;
                    gap: 20px;
                }
                .copy-button {
                    padding: 5px 10px;
                    margin-top: 5px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 12px;
                }
                .copy-button:hover {
                    background-color: #45a049;
                }
                .controls {
                    display: flex;
                    gap: 10px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>Yalıtım bilgileri için doğru adrestesiniz...</h1>
            <div id="chat-container"></div>
            <div class="input-area">
                <input type="text" id="message-input" placeholder="Mesajınızı yazın...">
                <button class="action-button" onclick="sendMessage()">Gönder</button>
            </div>
            <div class="controls">
                <button class="action-button" onclick="clearChat()" style="background-color: #dc3545;">İçeriği Temizle</button>
            </div>
            
            <script>
                const chatContainer = document.getElementById('chat-container');
                const messageInput = document.getElementById('message-input');
                
                function clearChat() {
                    chatContainer.innerHTML = '';
                }
                
                function copyToClipboard(text) {
                    navigator.clipboard.writeText(text).then(() => {
                        alert('Mesaj kopyalandı!');
                    });
                }
                
                async function sendMessage() {
                    const message = messageInput.value;
                    if (!message) return;
                    
                    // Kullanıcı mesajını göster
                    appendMessage(message, true);
                    messageInput.value = '';
                    
                    try {
                        const response = await fetch('/chat', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                message: message,
                                session_id: 'web-session'
                            })
                        });
                        
                        const data = await response.json();
                        if (data.error) {
                            appendMessage('Hata: ' + data.error, false);
                        } else {
                            appendMessage(data.textResponse, false);
                        }
                    } catch (error) {
                        appendMessage('Hata: Bir şeyler yanlış gitti', false);
                    }
                }
                
                function appendMessage(message, isUser) {
                    const messageDiv = document.createElement('div');
                    messageDiv.className = 'message-container';
                    
                    const textDiv = document.createElement('div');
                    textDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
                    textDiv.textContent = isUser ? `Siz: ${message}` : `Bot: ${message}`;
                    messageDiv.appendChild(textDiv);
                    
                    if (!isUser) {
                        const copyButton = document.createElement('button');
                        copyButton.className = 'copy-button';
                        copyButton.textContent = 'Cevabı Kopyala';
                        copyButton.onclick = () => copyToClipboard(message);
                        messageDiv.appendChild(copyButton);
                    }
                    
                    chatContainer.appendChild(messageDiv);
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
                
                messageInput.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                });
            </script>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
