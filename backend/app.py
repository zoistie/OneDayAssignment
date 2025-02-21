
import chat
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

Chatbot = None

#Message handling requests, invokes the model and then sends the response out
@app.route('/api/message', methods=['POST'])
def send_message():
    global Chatbot
    user_input = request.json.get('message')
    response = chat.Chat_Model(Chatbot, user_input)
    return jsonify({'message': response})


#Model Change request, changes the llm to the corresponding model in the frontend
@app.route('/api/change_model', methods=['POST'])
def change_model():
    global Chatbot
    model_change = request.json.get('model')
    service = request.json.get('service')
    user_name = user_settings["name"]
    system_prompt = user_settings["system_prompt"]
    Chatbot = chat.Initialize_Model(service,model_change,user_name,system_prompt)
    return jsonify({'model': model_change})


user_settings = {"name": "", "system_prompt": ""}

@app.route('/api/start', methods=['POST'])
def start_chat():
    global Chatbot
    data = request.json
    name = data.get("name", "")
    user_settings["name"] = name
    sys_prompt = data.get("system_prompt", "")
    user_settings["system_prompt"] = sys_prompt
    Chatbot = chat.Initialize_Model('OpenAI','GPT-4o',name,sys_prompt)
    return jsonify({"message": "User settings saved!", "settings": user_settings})


if __name__ == '__main__':
    app.run(debug=True)


