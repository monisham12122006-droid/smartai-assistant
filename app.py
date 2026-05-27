import os
from flask import Flask, request, render_template, jsonify
import google.generativeai as genai

app = Flask(__name__)
UPLOAD_FOLDER = 'migrated_resumes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ⚠️ உன்னுடைய Gemini API Key-ஐ இங்கே கொடு
genai.configure(api_key="AIzaSyAwK8nZ6xDO1o31BSmLqw0HvYp6yCVk8QY")
model = genai.GenerativeModel('gemini-2.5-flash')

questions_list = [
    "What is the fundamental difference between Artificial Intelligence and Machine Learning?",
    "Explain the three primary ways to include CSS in an HTML webpage.",
    "What are primary keys and foreign keys in a Database?"
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    return jsonify({
        "message": "Resume uploaded successfully!",
        "questions": questions_list,
        "current_question_index": 0,
        "question": questions_list[0]
    })

@app.route('/evaluate', methods=['POST'])
def evaluate_answer():
    data = request.json
    question = data.get('question')
    user_answer = data.get('user_answer')

    if not user_answer or user_answer.strip() == "":
        return jsonify({
            "status": "Incorrect",
            "score": "0/10",
            "explanation": "No answer provided. Please speak or type an answer."
        })

    prompt = f"""
    You are an expert interviewer. Evaluate the candidate's answer strictly based on the question.
    Question: {question}
    Candidate's Answer: {user_answer}

    Provide the evaluation details format EXACTLY like below. Do not use markdown bold tags like ** in the labels:
    STATUS: [Correct, Partially Correct, or Incorrect]
    SCORE: [Score out of 10, e.g., 7/10]
    EXPLANATION: [Write the detailed explanation, areas to improve, and recommended roles here]
    """

    try:
        response = model.generate_content(prompt)
        text = response.text

        # டிஃபால்ட் வேல்யூஸ்
        status = "Evaluated"
        score = "N/A"
        explanation = text

        # AI டெக்ஸ்ட்டை லைன் பை லைனாக பிரித்து வேல்யூஸ் எடுக்கிறோம்
        lines = text.split('\n')
        for line in lines:
            if line.upper().startswith("STATUS:"):
                status = line.split(":", 1)[1].strip()
            elif line.upper().startswith("SCORE:"):
                score = line.split(":", 1)[1].strip()
            elif line.upper().startswith("EXPLANATION:"):
                explanation = line.split(":", 1)[1].strip()

        # ஒருவேளை EXPLANATION லேபிளுக்கு அப்புறம் பெரிய பாராகிராஃப் இருந்தால் முழு டெக்ஸ்ட்டையும் அனுப்புவோம்
        if "EXPLANATION:" in text:
            explanation = text.split("EXPLANATION:", 1)[1].strip()

        return jsonify({
            "status": status,
            "score": score,
            "explanation": explanation
        })

    except Exception as e:
        return jsonify({
            "status": "Error",
            "score": "N/A",
            "explanation": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)