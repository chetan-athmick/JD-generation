from flask import Flask, request, jsonify
import uuid
from utils import get_pdf_text, extract_contact_info, extract_info_with_openai

app = Flask(__name__)

@app.route('/')
def home():
    return "HR Resume Screening Assistance API"

@app.route('/candidate_info', methods=['POST'])
def analyze():
    resumes = request.files.getlist('resumes')

    if not resumes:
        return jsonify({"error": "Resumes are required."}), 400

    data = []

    for resume in resumes:
        resume_txt = get_pdf_text(resume)
        name, contact_number, email = extract_contact_info(resume_txt)

        if not (name and contact_number and email):
            name, contact_number, email = extract_info_with_openai(resume_txt)

        data.append({
            "File": resume.filename,
            "Name": name,
            "Contact Number": contact_number,
            "Email": email
        })

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5051)
