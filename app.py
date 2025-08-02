from flask import Flask, request, render_template
import pdfplumber
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_info(text):
    doc = nlp(text)
    name = ""
    skills = []
    edu_keywords = ['btech', 'mtech', 'bsc', 'msc', 'graduation']

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    for token in doc:
        if token.pos_ == "NOUN":
            skills.append(token.text.lower())

    education = [word for word in edu_keywords if word in text.lower()]
    return name, list(set(skills)), education

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["resume"]
        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(file)
            name, skills, education = extract_info(text)
            return render_template("result.html", name=name, skills=skills, education=education)
        else:
            return "Only PDF files are allowed!"
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
