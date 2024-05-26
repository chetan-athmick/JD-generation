import os
import re
from PyPDF2 import PdfReader
from openai import AzureOpenAI

os.environ['AZURE_OPENAI_API_KEY'] = "e3151139857144bb9d56d029fcd44e8f"
os.environ['AZURE_OPENAI_ENDPOINT'] = "https://athmick-openai.openai.azure.com/"
os.environ['OPENAI_API_VERSION'] = "2024-02-15-preview"

client = AzureOpenAI()

def get_pdf_text(file):
    text = ''
    pdf = PdfReader(file)
    for page_number in range(len(pdf.pages)):
        page = pdf.pages[page_number]
        text += page.extract_text()
    return text

def extract_contact_info(text):
    name_pattern = re.compile(r"Name[:\s]+([A-Za-z\s]+)")
    contact_number_pattern = re.compile(r"Contact Number[:\s]+(\+?\d{10,15})")
    email_pattern = re.compile(r"Email[:\s]+([\w\.-]+@[\w\.-]+)")

    name_match = name_pattern.search(text)
    contact_number_match = contact_number_pattern.search(text)
    email_match = email_pattern.search(text)

    name = name_match.group(1) if name_match else None
    contact_number = contact_number_match.group(1) if contact_number_match else None
    email = email_match.group(1) if email_match else None

    return name, contact_number, email

def extract_info_with_openai(text):
    chat_completion = client.chat.completions.create(
        model="GPT35",
        messages=[
            {"role": "system", "content": "You are an AI assistant that extracts contact information from resumes."},
            {"role": "user", "content": f"""Extract the name, contact number, and email from the following text:
                Resume: {text}
                Provide the information in this format:
                Name: [name]
                Contact Number: [contact number]
                Email: [email]
            """}
        ],
        max_tokens=200,
        temperature=0
    )
    result_text = chat_completion.choices[0].message.content

    name = re.search(r"Name: (.*)", result_text).group(1) if re.search(r"Name: (.*)", result_text) else None
    contact_number = re.search(r"Contact Number: (.*)", result_text).group(1) if re.search(r"Contact Number: (.*)", result_text) else None
    email = re.search(r"Email: (.*)", result_text).group(1) if re.search(r"Email: (.*)", result_text) else None

    return name, contact_number, email
