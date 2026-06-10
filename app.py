from flask import Flask, render_template, request, jsonify
import requests

# Khởi tạo Flask app
app = Flask(__name__)

# Đường dẫn đến endpoint của Rasa server
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

# Trang chủ của website
@app.route('/')
def home():
    return render_template('index.html')

# API để gửi tin nhắn đến Rasa bot và nhận phản hồi
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Gửi yêu cầu đến Rasa server
    try:
        response = requests.post(RASA_SERVER_URL, json={"sender": "user", "message": user_message})
        response_data = response.json()

        # Lấy phản hồi từ Rasa bot
        bot_messages = [resp.get('text', '') for resp in response_data]
        return jsonify({"messages": bot_messages})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to connect to Rasa server", "details": str(e)}), 500

# Chạy Flask server
if __name__ == '__main__':
    app.run(debug=True)
