from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import random
import traceback

app = Flask(__name__)
CORS(app)

# Load the sample questions and answers
try:
    with open('Sample Question Answers.json', 'r', encoding='utf-8') as f:
        qa_data = json.load(f)
    print("Successfully loaded Sample Question Answers.json")
except Exception as e:
    print(f"Error loading Sample Question Answers.json: {str(e)}")
    qa_data = {}

# Load the corpus
try:
    with open('corpus.txt', 'r', encoding='utf-8') as f:
        corpus = f.read().lower().split('.')
    print("Successfully loaded corpus.txt")
except Exception as e:
    print(f"Error loading corpus.txt: {str(e)}")
    corpus = []

# Simple keyword-based response function
def get_response_from_corpus(user_input):
    user_words = set(user_input.lower().split())
    best_sentence = ""
    max_overlap = 0
    
    for sentence in corpus:
        sentence_words = set(sentence.split())
        overlap = len(user_words.intersection(sentence_words))
        if overlap > max_overlap:
            max_overlap = overlap
            best_sentence = sentence
    
    return best_sentence.strip().capitalize() + "." if best_sentence else random.choice(default_responses)

# Default responses for when no match is found
default_responses = [
    "I'm not sure about that. Can you ask me something else?",
    "That's an interesting question! I don't have a specific answer for it.",
    "I don't have information about that. Is there something else I can help you with?",
    "I'm still learning and don't have an answer for that yet. Can you try asking in a different way?",
]

@app.route('/chat', methods=['POST'])
def chat():
    print("Received chat request")
    try:
        user_input = request.json.get('message')
        print(f"User input: {user_input}")

        if not user_input:
            print("No message provided")
            return jsonify({'error': 'No message provided'}), 400

        # Check if the question is in the sample questions
        if user_input.lower() in qa_data:
            response_text = qa_data[user_input.lower()]
        else:
            # If not found, use the corpus to generate a response
            response_text = get_response_from_corpus(user_input)

        print(f"Sending response: {response_text}")
        response = jsonify({'response': response_text})
        print(f"JSON response: {response.get_data(as_text=True)}")
        return response

    except Exception as e:
        error_msg = f"An error occurred: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'This is a test response'})

@app.route('/test_json', methods=['GET'])
def test_json():
    return jsonify({'message': 'This is a test JSON response'})

if __name__ == '__main__':
    app.run(debug=True)