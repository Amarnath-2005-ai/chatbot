import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random

# Initialize variables
words = []
classes = []
documents = []
ignore_words = ['?', '!']

# Load the intents file
try:
    with open('medical_bot.json', 'r', encoding='utf-8') as file:
        intents = json.load(file)
except FileNotFoundError:
    print("Error: File 'medical_bot.json' not found.")
    exit()
except json.JSONDecodeError:
    print("Error: Invalid JSON format in the intents file.")
    exit()

# Process patterns and create documents
for intent in intents['intents']:
    if not intent['patterns']:
        continue  # Skip intents with no patterns
        
    for pattern in intent['patterns']:
        # Tokenize each word
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        # Add documents to the corpus
        documents.append((w, intent['tag']))
        # Add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize and lowercase each word and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

# Save words and classes to files
try:
    pickle.dump(words, open('words.pkl', 'wb'))
    pickle.dump(classes, open('classes.pkl', 'wb'))
except Exception as e:
    print(f"Error saving pickle files: {e}")
    exit()

print(f"{len(documents)} documents")
print(f"{len(classes)} classes: {classes}")
print(f"{len(words)} unique lemmatized words")

# Create training data
training = []
output_empty = [0] * len(classes)

for doc in documents:
    # Initialize bag of words
    bag = []
    # List of tokenized words for the pattern
    pattern_words = doc[0]
    # Lemmatize each word
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    # Create bag of words array
    bag = [1 if w in pattern_words else 0 for w in words]
    
    # Output is '1' for current tag and '0' for others
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    
    training.append([bag, output_row])

# Shuffle features and convert to numpy array
random.shuffle(training)
training = np.array(training, dtype=object)

# Create train and test lists
train_x = np.array([x[0] for x in training])
train_y = np.array([x[1] for x in training])

print("Training data created")

# Validate training data
if len(train_x) == 0:
    print("Error: No training data created. Check your intents file.")
    exit()

print(f"Training samples: {len(train_x)}")
print(f"Features per sample: {len(train_x[0])}")
print(f"Output classes: {len(train_y[0])}")

# Build neural network model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile model with SGD optimizer
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train the model
print("Training model...")
hist = model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)

# Save the model
try:
    model.save('chatbot_model.h5')
    print("Model saved to chatbot_model.h5")
except Exception as e:
    print(f"Error saving model: {e}")

print("Training complete!")
