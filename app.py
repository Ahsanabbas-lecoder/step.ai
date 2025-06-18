from flask import Flask, request, jsonify, render_template
import joblib
import random
from token_counter import SimpleTokenCounter

app = Flask(__name__)

# Load model
model_data = joblib.load('model/chatbot_model.pkl')
model = model_data['model']
responses = model_data['responses']
token_counter = model_data['token_counter']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()
    user_tokens = token_counter.count_tokens(user_message)
    
    # Special cases
    if any(q in user_message for q in ['your name', 'who are you']):
        response = random.choice(responses['identity'])['text']
    elif 'flask' in user_message:
        response = random.choice(responses['flask'])['text']
    else:
        try:
            intent = model.predict([user_message])[0]
            response = random.choice(responses.get(intent, responses['greeting']))['text']
        except:
            response = "I'm not sure how to answer that."
    
    return jsonify({
        'response': response,
        'tokens': user_tokens + token_counter.count_tokens(response)
    })

@app.route('/tokens', methods=['POST'])
def count_tokens():
    text = request.json.get('text', '')
    return jsonify({'tokens': token_counter.count_tokens(text)})

if __name__ == '__main__':
    app.run(debug=True)