from flask import Flask, render_template, request, send_file
import pyttsx3
import pdfplumber
import PyPDF2
from gtts import gTTS
import os

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/welcome", methods=["GET"])
def welcome():
    return render_template("home.html")


@app.route("/success", methods=["POST"])
def success():
    if request.method == "POST":
        fi = request.files["file"]
        fi.save("Uploads/" + fi.filename)
        convertToPdf(fi.filename)
        pathToFile = "AudioBooks/audiobook.mp3"
        return send_file(pathToFile, as_attachment=True)


def convertToPdf(filName):
    file = "Uploads/" + filName
    print(file)
    pdfFileObj = open(file, "rb")
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pages = pdfReader.numPages

    finalfile = ""
    with pdfplumber.open(file) as pdf:
        # Loop through the number of pages
        for i in range(0, pages):
            page = pdf.pages[i]
            text = page.extract_text()
            print(text)
            finalfile += text

    print(finalfile)
    output = gTTS(text=finalfile, lang="en")
    output.save("AudioBooks/audiobook.mp3")


if __name__ == "__main__":
    app.run(port=7000, debug=True)
