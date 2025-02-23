from flask import Flask, render_template, request, send_file, redirect, url_for
from database import insert_data, fetch_data
from nlp_extractor import extract_entities
from pdf_generator import create_pdf
from exception import customException
import sys
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists("output"):
    os.makedirs("output")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_docx():
    try:
        if "file" not in request.files:
            return redirect(url_for("home"))
        file = request.files["file"]
        if file.filename == "":
            return redirect(url_for("home"))
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        extracted_data = extract_entities(filepath)

        insert_data(extracted_data)

        pdf_path = create_pdf(extracted_data, file.filename)

        pdf_filename = os.path.basename(pdf_path)
        return redirect(url_for("download_page", pdf_filename=pdf_filename))
        # return send_file(pdf_path, as_attachment=True, download_name="output.pdf")
    except Exception as e:
        raise customException(e, sys)
    
@app.route("/download_page")
def download_page():
    # Render download.html with the pdf_filename
    pdf_filename = request.args.get("pdf_filename")
    return render_template("download.html", pdf_filename=pdf_filename)

@app.route("/download_pdf/<pdf_filename>", methods=["GET"])
def download_pdf(pdf_filename):
    try:
        pdf_path = os.path.join("output", pdf_filename)
        return send_file(pdf_path, as_attachment=True, download_name=pdf_filename)
    except Exception as e:
        raise customException(e, sys)

if __name__ == "__main__":
    app.run(debug=True)
