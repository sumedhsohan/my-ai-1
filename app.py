from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

MISTRAL_API_KEY = "NnB7VXmrwPIDnj8jyCjLBes761ihWNfZ"  # Replace with your Mistral API key
MISTRAL_API_URL = "https://console.mistral.ai/api-keys/"  # OpenRouter for Mistral API

HEADERS = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}

# Function to generate resume
@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    data = request.json
    name = data.get("name")
    skills = data.get("skills")
    experience = data.get("experience")

    prompt = f"""
    Generate a professional resume for {name}.
    Skills: {skills}
    Experience: {experience}
    Format it professionally.
    """

    payload = {
        "model": "mistral-7b",  # Use Mixtral if available
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500
    }

    response = requests.post(MISTRAL_API_URL, headers=HEADERS, json=payload)
    resume = response.json().get("choices", [{}])[0].get("message", {}).get("content", "Error generating resume")

    return jsonify({"resume": resume})


# Function to generate interview questions
@app.route('/interview_questions', methods=['POST'])
def interview_questions():
    data = request.json
    job_role = data.get("job_role")

    prompt = f"""
    Generate 5 mock interview questions for a {job_role} position.
    Include both technical and behavioral questions.
    """

    payload = {
        "model": "mistral-7b",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500
    }

    response = requests.post(MISTRAL_API_URL, headers=HEADERS, json=payload)
    questions = response.json().get("choices", [{}])[0].get("message", {}).get("content", "Error generating questions")

    return jsonify({"questions": questions})


if __name__ == '__main__':
    app.run(debug=True)
