import spacy
from collections import Counter
from heapq import nlargest
from flask import Flask, render_template, request, send_file, jsonify, redirect, session
import PyPDF2
import random
import time
import threading
import json
import os

app = Flask(__name__)

# Set a secret key for sessions (Make sure to keep it secure)
app.secret_key = os.urandom(24)  # Generate a random 24-byte secret key for your app

# Function to summarize the text, considering all paragraphs
def summarize_text(text, num_sentences=7):
    nlp = spacy.load('en_core_web_sm')
    paragraphs = text.split('\n\n')  # Split the text into paragraphs

    # Calculate sentences to extract per paragraph
    total_sentences = sum(len(list(nlp(paragraph).sents)) for paragraph in paragraphs)
    sentences_per_paragraph = [
        max(1, round(len(list(nlp(paragraph).sents)) / total_sentences * num_sentences))
        for paragraph in paragraphs
    ]

    summary = []
    for i, paragraph in enumerate(paragraphs):
        if not paragraph.strip():  # Skip empty paragraphs
            continue
        doc = nlp(paragraph)

        # Word frequency analysis for the paragraph
        tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct and token.text != '\n']
        word_freq = Counter(tokens)
        max_freq = max(word_freq.values(), default=1)  # Avoid division by zero
        for word in word_freq.keys():
            word_freq[word] = word_freq[word] / max_freq

        # Score sentences within the paragraph
        sent_token = [sent.text for sent in doc.sents]
        sent_score = {}
        for sent in sent_token:
            for word in sent.split():
                if word.lower() in word_freq.keys():
                    if sent not in sent_score.keys():
                        sent_score[sent] = word_freq[word]
                    else:
                        sent_score[sent] += word_freq[word]

        # Select top sentences for the paragraph
        top_sentences = nlargest(sentences_per_paragraph[i], sent_score, key=sent_score.get)
        summary.extend(top_sentences)

    return " ".join(summary)

# Function to extract and clean text from a PDF
def extract_clean_text_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""

            for page in pdf_reader.pages:
                page_text = page.extract_text()
                filtered_lines = [
                    line for line in page_text.splitlines()
                    if len(line.strip()) > 50 and not line.strip().isdigit()
                ]
                text += "\n".join(filtered_lines) + "\n"
            return text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Function to generate flashcards from extracted text
def generate_flashcards_from_text(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    flashcards = []
    used_entities = set()  # To track used entities
    used_sentences = set()  # To track used sentences
    paragraphs = text.split('\n\n')  # Split the text into paragraphs
    paragraph_indices = list(range(len(paragraphs)))

    random.shuffle(paragraph_indices)  # Randomize paragraph order to ensure diversity

    for paragraph_index in paragraph_indices:
        paragraph = paragraphs[paragraph_index]
        doc = nlp(paragraph)

        for ent in doc.ents:  # Use named entities instead of individual tokens
            if ent.label_ in {"PERSON", "ORG", "GPE", "NORP", "PRODUCT", "EVENT", "WORK_OF_ART", "LOC"}:  # Check for relevant named entity types
                if ent.text not in used_entities:
                    # Check that the entity's sentence hasn't been used before
                    sentence = next(sent for sent in doc.sents if ent.text in sent.text)
                    if sentence.text not in used_sentences:
                        question = ent.text
                        answer = f"{sentence.text.strip()} (Definition: {question})"
                        flashcards.append({
                            "question": question,
                            "answer": answer
                        })
                        used_entities.add(ent.text)
                        used_sentences.add(sentence.text)  # Mark this sentence as used

        if len(flashcards) >= 3:  # Stop after generating 3 flashcards
            break

    return flashcards[:3]

# Function to generate rapid-fire fill-in-the-blank questions from extracted text
def generate_fill_in_the_blank_questions(text, num_questions=3):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    questions = []
    used_entities = set()  # To track used entities

    for sent in doc.sents:
        entity = None

        # Detect named entities for fill-in-the-blank
        for ent in doc.ents:
            if ent.text in sent.text and ent.text not in used_entities:
                entity = ent.text
                used_entities.add(entity)
                break

        if entity:
            question = sent.text.replace(entity, "")
            correct_answer = entity

            options = [correct_answer]
            while len(options) < 4:
                random_entity = random.choice([ent.text for ent in doc.ents if ent.text != correct_answer and ent.text not in used_entities])
                if random_entity not in options:
                    options.append(random_entity)

            random.shuffle(options)

            questions.append({
                "question": question,
                "options": options,
                "correct_answer": correct_answer
            })

    return questions[:num_questions]

# Route to render the upload page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dropdown/summary')
def summary_page():
    return render_template('summary.html')

@app.route('/dropdown/todo')
def todo():
    return render_template('todo.html')

@app.route('/dropdown/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/dropdown/techniques')
def techniques():
    return render_template('techniques.html')

@app.route('/dropdown/notes')
def notes():
    return render_template('notes.html')

@app.route('/planner')
def plan():
    return render_template('planner.html')

@app.route('/dropdown/techniques/pomodoro')
def pomodoro():
    return render_template('pomodoro.html')

@app.route('/dropdown/quiz/soloquiz')
def soloquiz():
    return render_template('soloquiz.html')


@app.route('/dropdown/flashcards')
def flashcards():
    return render_template('flashcards.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/dropdown')
def dropdown():
    return render_template('dropdown.html')

# Route to handle file uploads and generate the JSON file
@app.route('/upload', methods=['POST'])
def handle_upload():
    if 'pdf_file' not in request.files:
        return "No file uploaded", 400

    pdf_file = request.files['pdf_file']
    file_path = os.path.join("uploads", pdf_file.filename)
    pdf_file.save(file_path)

    # Extract text from the uploaded PDF
    extracted_text = extract_clean_text_from_pdf(file_path)

    # Summarize the extracted text
    summary = summarize_text(extracted_text, num_sentences=7)

    # Generate flashcards based on the extracted text
    flashcards = generate_flashcards_from_text(extracted_text)

    # Generate rapid-fire fill-in-the-blank questions from the extracted text
    questions = generate_fill_in_the_blank_questions(extracted_text, num_questions=3)

    # Structure all data
    data = {
        "summary": summary,
        "flashcards": [{"question": fc["question"], "answer": fc["answer"]} for fc in flashcards],
        "rapid_fire_quiz": [{"question": q["question"], "options": q["options"], "correct_answer": q["correct_answer"]} for q in questions]
    }

    # Save the data to a JSON file
    output_filename = f"{pdf_file.filename}_output.json"
    output_filepath = os.path.join("uploads", output_filename)
    with open(output_filepath, "w") as json_file:
        json.dump(data, json_file, indent=4)

    # Store the filename in the session
    session['filename'] = output_filename

    # Redirect to the dropdown page
    return redirect('/dropdown')

if __name__ == '__main__':
    app.run(debug=True)
