import spacy
from docx import Document
import gender_guesser.detector as g
import re
import sys
from exception import customException

# Initialize gender_guesser object
d = g.Detector()

# Regex patterns for phone number and email
phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
age_pattern = r'\b(\d{1,3})\s*(?:years old|yrs old|years)\b'
gender_pattern = r'\b(male|female|man|woman)\b'

# Load SpaCy language model
nlp = spacy.load("en_core_web_trf")

def extract_entities(filepath):
    try:
        doc = Document(filepath)
        full_text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        raise customException(e, sys)
    
    try:
        nlp_doc = nlp(full_text)
    except Exception as e:
        raise customException(e, sys)
    
    extracted_data = {
        "First_name": "",
        "Last_name": "",
        "Age": "",
        "Gender": "",
        "Phone_number": "",
        "Email": "",
        "Address": "",
        "Nationality": "",
        "Organizations": "",
        "Languages_known": ""
    }

    names = []
    organizations = []
    languages = []
    addresses = []
    nationality = []
    
    try:
        for ent in nlp_doc.ents:
            if ent.label_ == "PERSON":
                names.append(ent.text.strip())
            elif ent.label_ == "ORG":
                organizations.append(ent.text.strip())
            elif ent.label_ == "LANGUAGE":
                languages.append(ent.text.strip())
            elif ent.label_ == "GPE":
                addresses.append(ent.text.strip())
            elif ent.label_ == "NORP":
                nationality.append(ent.text.strip())

        if names:
            extracted_data["Name"] = ", ".join(names)
        
        # Extract Age using regex (e.g., "18 years old")
        age_match = re.search(age_pattern, full_text, re.IGNORECASE)
        if age_match:
            extracted_data["Age"] = age_match.group(1)

        # extract gender using regex
        gender_match = re.search(gender_pattern, full_text, re.IGNORECASE)
        if gender_match:
            extracted_data["Gender"] = gender_match.group(1).lower()
        else:
            if not extracted_data.get("Gender") or extracted_data["Gender"].lower() == "not found":
                if extracted_data.get("Name"):
                    first_name = extracted_data["Name"].split()[0] # multiple name then gender of first name
                    extracted_data["Gender"] = d.get_gender(first_name)
                else:
                    extracted_data["Gender"] = "Not found"
        
        # Extract phone number using regex
        phone_match = re.search(phone_pattern, full_text)
        if phone_match:
            extracted_data["Phone_number"] = phone_match.group().strip()
        
        # Extract emails using regex; join multiple matches with a comma
        email_matches = re.findall(email_pattern, full_text)
        if email_matches:
            extracted_data["Email"] = ", ".join(email_matches)
        
        if addresses:
            unique_addresses = list(dict.fromkeys(addresses))
            extracted_data["Address"] = ", ".join(unique_addresses)
        
        if nationality:
            extracted_data["Nationality"] = nationality[0]
        
        if organizations:
            extracted_data["Organizations"] = ", ".join(list(dict.fromkeys(organizations)))
        
        if languages:
            extracted_data["Languages_known"] = ", ".join(list(dict.fromkeys(languages)))

    except Exception as e:
        raise customException(e, sys)
    
    return extracted_data
