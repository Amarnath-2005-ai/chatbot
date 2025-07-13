# Cura Medical Chatbot

Cura is an AI-powered medical chatbot built with Flask, Keras, and NLTK. It can answer health-related questions, provide first aid tips, and offer general medical advice. The model is trained on intents defined in `job_intents.json`.

## Features
- Natural language understanding for medical queries
- Friendly, conversational responses
- Covers symptoms, first aid, medicine advice, mental health, nutrition, and more
- Day/night mode UI

## Setup

1. **Clone the repository or copy the files to your project folder.**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Download NLTK data:**
   The first run will download required NLTK data automatically. If not, run:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('wordnet')
   ```
4. **Train the model:**
   ```bash
   python chatbot.py
   ```
   This will create `chatbot_model.h5`, `words.pkl`, and `classes.pkl`.
5. **Run the Flask app:**
   ```bash
   python app.py
   ```
6. **Open your browser and go to:**
   [http://localhost:8888](http://localhost:8888)

## File Structure
- `app.py` - Flask web server
- `chatbot.py` - Model training script
- `job_intents.json` - Intents and responses
- `static/` - CSS and JS files
- `templates/` - HTML templates

## Notes
- This chatbot is for informational purposes only and does not replace professional medical advice.
- For urgent or serious health issues, always consult a healthcare professional.

---

Made with ❤️ by Amaranth
