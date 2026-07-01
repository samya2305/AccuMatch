import fitz
import easyocr
import re
import tempfile

from pathlib import Path
from pdf2image import convert_from_path

# -------------------------------------------------------
# OCR MODEL
# -------------------------------------------------------

reader = easyocr.Reader(
    ['en'],
    gpu=False
)

# -------------------------------------------------------
# CLEAN OCR TEXT
# -------------------------------------------------------

def clean_ocr_text(text):

    if not text:
        return ""

    text = text.replace("|", " ")
    text = text.replace("\r", "")
    text = text.replace("\t", " ")

    text = re.sub(r'[ ]+', ' ', text)
    text = re.sub(r'\n+', '\n', text)

    return text.strip()

# -------------------------------------------------------
# PDF TEXT EXTRACTION
# -------------------------------------------------------

def extract_pdf_text(pdf_path):

    text = ""

    try:

        doc = fitz.open(pdf_path)

        for page in doc:

            page_text = page.get_text("text")

            if page_text:
                text += page_text + "\n"

        doc.close()

    except Exception as e:

        print("PDF Extraction Error :", e)

    return text

# -------------------------------------------------------
# OCR EXTRACTION
# -------------------------------------------------------

def extract_scanned_pdf(pdf_path):

    text = ""

    try:

        pages = convert_from_path(
            pdf_path,
            dpi=250
        )

        for page in pages:

            with tempfile.NamedTemporaryFile(
                suffix=".jpg",
                delete=False
            ) as temp:

                page.save(
                    temp.name,
                    "JPEG"
                )

                result = reader.readtext(
                    temp.name,
                    detail=0,
                    paragraph=True
                )

                text += "\n".join(result)
                text += "\n"

    except Exception as e:

        print("OCR Error :", e)

    return text

# -------------------------------------------------------
# GET TEXT
# -------------------------------------------------------

def get_text(file_path):

    text = extract_pdf_text(file_path)

    print("PDF Text Length :", len(text))

    # PDF-la text irundha OCR run panna koodathu

    if len(text.strip()) > 100:

        print("Using PDF Text")

        return clean_ocr_text(text)

    print("Running OCR...")

    text = extract_scanned_pdf(file_path)

    return clean_ocr_text(text)

# -------------------------------------------------------
# OFFER LETTER
# -------------------------------------------------------

def extract_offer_letter(pdf_path):

    text = get_text(pdf_path)

    print("\n===== OFFER LETTER =====")
    print(text)

    data = {
        "name": "",
        "college": "",
        "reg_no": "",
        "email": "",
        "phone_number": "",
        "shift_timing": ""
    }

    # -------------------------------
    # EMAIL
    # -------------------------------

    match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text,
        re.IGNORECASE
    )

    if match:
        data["email"] = match.group().strip()

    # -------------------------------
    # REGISTER NUMBER (12 digits)
    # -------------------------------

    match = re.search(
        r'\b\d{12}\b',
        text
    )

    if match:
        data["reg_no"] = match.group()

    # -------------------------------
    # PHONE NUMBER
    # -------------------------------

    match = re.search(
        r'(\+91[\s-]*)?[6-9]\d{9}',
        text
    )

    if match:

        phone = re.sub(
            r"\D",
            "",
            match.group()
        )

        data["phone_number"] = phone[-10:]

    # -------------------------------
    # SHIFT TIME
    # -------------------------------

    match = re.search(
        r'Shift\s*Time\s*:?\s*([0-9:\sAPMapmtoTO]+)',
        text,
        re.IGNORECASE
    )

    if match:

        data["shift_timing"] = " ".join(
            match.group(1).split()
        )

    # -------------------------------
    # NAME
    # -------------------------------

    match = re.search(
        r'Dear\s+([A-Za-z ]+)',
        text,
        re.IGNORECASE
    )

    if match:

        name = match.group(1)

        name = re.sub(
            r'\s+',
            ' ',
            name
        )

        data["name"] = name.strip()

    # -------------------------------
    # COLLEGE
    # -------------------------------

    patterns = [

        r'CARE\s+College\s+of\s+Engineering',

        r'[A-Za-z ]+College of Engineering',

        r'[A-Za-z ]+Engineering,?\s*Trichy'

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            data["college"] = " ".join(
                match.group().split()
            )

            break

    return data

# -------------------------------------------------------
# AADHAAR
# -------------------------------------------------------

def extract_aadhaar(pdf_path):

    text = get_text(pdf_path)

    print("\n===== AADHAAR =====")
    print(text)

    data = {
        "name": "",
        "aadhaar_number": "",
        "phone_number": ""
    }

    # -------------------------------
    # Aadhaar Number
    # -------------------------------

    match = re.search(
        r'\d{4}\s\d{4}\s\d{4}',
        text
    )

    if match:

        data["aadhaar_number"] = re.sub(
            r"\D",
            "",
            match.group()
        )

    # -------------------------------
    # Mobile Number
    # -------------------------------

    match = re.search(
        r'[6-9]\d{9}',
        text
    )

    if match:

        data["phone_number"] = match.group()

    # -------------------------------
    # Name
    # -------------------------------

    patterns = [

        r'To\s+([A-Za-z ]+)',

        r'Government of India\s+([A-Za-z ]+)',

        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})'

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            candidate = " ".join(
                match.group(1).split()
            )

            if (
                "government" not in candidate.lower()
                and "india" not in candidate.lower()
                and len(candidate) > 5
            ):

                data["name"] = candidate
                break

    return data


# -------------------------------------------------------
# COLLEGE ID
# -------------------------------------------------------

def extract_college_id(pdf_path):

    text = get_text(pdf_path)

    print("\n===== COLLEGE ID =====")
    print(text)

    data = {
        "name": "",
        "college": "",
        "reg_no": ""
    }

    # -------------------------------
    # Register Number
    # -------------------------------

    match = re.search(
        r'\b\d{12}\b',
        text
    )

    if match:

        data["reg_no"] = match.group()

    # -------------------------------
    # College Name
    # -------------------------------

    patterns = [

        r'CARE\s+COLLEGE\s+OF\s+ENGINEERING',

        r'[A-Za-z ]+College of Engineering'

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            data["college"] = " ".join(
                match.group().split()
            )

            break

    # -------------------------------
    # Student Name
    # -------------------------------

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if any(ch.isdigit() for ch in line):
            continue

        if (
            "college" in line.lower()
            or "engineering" in line.lower()
            or "principal" in line.lower()
            or "autonomous" in line.lower()
        ):
            continue

        words = line.split()

        if 2 <= len(words) <= 5:

            data["name"] = " ".join(words)
            break

    return data

# -------------------------------------------------------
# RESUME
# -------------------------------------------------------

def extract_resume(pdf_path):

    text = get_text(pdf_path)

    print("\n===== RESUME =====")
    print(text)

    data = {
        "name": "",
        "college": "",
        "email": "",
        "phone_number": ""
    }

    # -------------------------------
    # EMAIL
    # -------------------------------

    match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text,
        re.IGNORECASE
    )

    if match:
        data["email"] = match.group()

    # -------------------------------
    # PHONE
    # -------------------------------

    match = re.search(
        r'[6-9]\d{9}',
        text
    )

    if match:
        data["phone_number"] = match.group()

    # -------------------------------
    # NAME
    # -------------------------------

    lines = text.split("\n")

    for line in lines:

        line = " ".join(line.split())

        if len(line) == 0:
            continue

        if any(ch.isdigit() for ch in line):
            continue

        lower = line.lower()

        if (
            "contact" in lower
            or "summary" in lower
            or "education" in lower
            or "skills" in lower
            or "projects" in lower
            or "activities" in lower
            or "github" in lower
        ):
            continue

        words = line.split()

        if 2 <= len(words) <= 6:

            data["name"] = line.title()
            break

    # -------------------------------
    # COLLEGE
    # -------------------------------

    patterns = [

        r'CARE\s+College\s+of\s+Engineering',

        r'CARE\s+college\s+of\s+engineering',

        r'[A-Za-z ]+College of Engineering',

        r'[A-Za-z ]+College'

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            data["college"] = " ".join(
                match.group().split()
            )

            break

    return data


# -------------------------------------------------------
# FILE EXISTS
# -------------------------------------------------------

def file_exists(file_path):

    return Path(file_path).exists()