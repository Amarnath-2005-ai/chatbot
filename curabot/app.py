from flask import Flask, render_template, jsonify, request
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from keras.models import load_model
import json
import random
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'fallback-secret-key-3479373')

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load model and data with error handling
try:
    model = load_model('chatbot_model.h5')
    with open('medical_bot.json', 'r', encoding='utf-8') as f:
        intents = json.load(f)
    words = pickle.load(open('words.pkl', 'rb'))
    classes = pickle.load(open('classes.pkl', 'rb'))
except Exception as e:
    print(f"Error loading model or data: {e}")
    exit(1)

# Helper functions
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for i, w in enumerate(words):
        if w in sentence_words:
            bag[i] = 1
            if show_details:
                print(f"found in bag: {w}")
    return np.array(bag)

def predict_class(sentence, model, threshold=0.15):
    p = bow(sentence, words)
    res = model.predict(np.array([p]), verbose=0)[0]
    
    results = [[i, r] for i, r in enumerate(res) if r > threshold]
    results.sort(key=lambda x: x[1], reverse=True)
    
    return_list = []
    for r in results:
        return_list.append({
            "intent": classes[r[0]], 
            "probability": float(r[1])  # Convert numpy float to Python float
        })
    
    # Fallback to highest probability if none pass threshold
    if not return_list:
        max_idx = np.argmax(res)
        return_list.append({
            "intent": classes[max_idx],
            "probability": float(res[max_idx])
        })
    
    return return_list

def get_response(intents_list, intents_json):
    if not intents_list:
        return "Sorry, I didn't understand that. Could you rephrase?"
    
    tag = intents_list[0]['intent']
    for intent in intents_json['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
    
    return "I'm not sure how to respond to that. Could you ask differently?"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({"response": "Please enter a message."})
    
        
        
    try:
        predicted_intents = predict_class(user_message, model)
        print(f"User message: {user_message}")
        print(f"Predicted intents: {predicted_intents}")
        response = get_response(predicted_intents, intents)
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error processing message: {e}")
        return jsonify({"response": "Sorry, I encountered an error processing your request."})

if __name__ == '__main__':
    # Configure these through environment variables in production
    port = int(os.environ.get('PORT', 8888))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
