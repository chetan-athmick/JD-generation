from openai import AzureOpenAI
from flask import Flask,request
import os

os.environ['AZURE_OPENAI_API_KEY'] = "e3151139857144bb9d56d029fcd44e8f"
os.environ['AZURE_OPENAI_ENDPOINT'] = "https://athmick-openai.openai.azure.com/"
os.environ['OPENAI_API_VERSION'] = "2024-02-15-preview"

app = Flask(__name__)

def generate(job_title,experience,primary_skills,secondary_skills):
    client = AzureOpenAI()
    
    conversation = [
            {"role": "system", "content": "You are a Resume Assistant."},
            {"role": "user", "content": f"""Your task is generate Job description for this {job_title},{experience},{primary_skills},{secondary_skills}.
                    Job Description Must have
                    1. Job Title
                    2. Job Summary : [200 words]
                    3. Responsibilities : Five Responsibilities in five lines
                    4. Required Skills : Six Skills
                    5. Primary Skills
                    6. Secondary Skills
                    7. Qualifications
                  These topics must have in that Generated Job Description.
                  """}
        ]
                
    # Call OpenAI GPT-3.5-turbo
    chat_completion = client.chat.completions.create(
        model = "GPT35",
        messages = conversation,
        max_tokens=1000,
        temperature=0
    )
    response = chat_completion.choices[0].message.content
    return response

@app.route("/get_job_description", methods=["POST"])
def get_response():
    job_title = request.form['job_title']
    experience = request.form['experience']
    primary_skills = request.form['primary_skills']
    secondary_skills = request.form['secondary_skills']

    if job_title and experience and primary_skills and secondary_skills != "":
        response = generate(job_title,experience,primary_skills,secondary_skills)
        return response
    else:
        return "Please fill out all the inputs"
    
if __name__ == "__main__":
    app.run(debug=True,port=5000)
