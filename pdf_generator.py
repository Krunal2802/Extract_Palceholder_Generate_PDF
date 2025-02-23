import pdfkit
from exception import customException 
import sys
import os

def create_pdf(data, original_filename):
    try:
        pdf_content = f"""
        <html>
        <head>
            <title>Extracted Placeholders</title>
        </head>
        <body>
            <h1>User Information</h1>
            <p><strong>Name:</strong> {data.get("Name", "")}</p>
            <p><strong>Age:</strong> {data.get("Age", "")}</p>
            <p><strong>Gender:</strong> {data.get("Gender", "")}</p>
            <p><strong>Phone Number:</strong> {data.get("Phone_number", "")}</p>
            <p><strong>Emails:</strong> {data.get("Email", "")}</p>
            <p><strong>Address:</strong> {data.get("Address", "")}</p>
            <p><strong>Nationality:</strong> {data.get("Nationality", "")}</p>
            <p><strong>Organizations:</strong> {data.get("Organizations", "")}</p>
            <p><strong>Languages known:</strong> {data.get("Languages_known", "")}</p>
        </body>
        </html>
        """

        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        pdf_filename = original_filename.replace(".docx", ".pdf")
        pdf_path = os.path.join(output_dir, pdf_filename)

        path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

        # Generate the PDF
        pdfkit.from_string(pdf_content, pdf_path, configuration=config)
        return pdf_path

    except Exception as e:
        raise customException(e, sys)
