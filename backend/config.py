import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

OFFER_DIR = os.path.join(UPLOAD_DIR, "offer_letters")
AADHAAR_DIR = os.path.join(UPLOAD_DIR, "aadhaar")
COLLEGE_DIR = os.path.join(UPLOAD_DIR, "college_id")
RESUME_DIR = os.path.join(UPLOAD_DIR, "resume")
PHOTO_DIR = os.path.join(UPLOAD_DIR, "photos")

REPORT_DIR = os.path.join(BASE_DIR, "reports")
CSV_FILE = os.path.join(REPORT_DIR, "verification_report.csv")

for folder in [
    OFFER_DIR,
    AADHAAR_DIR,
    COLLEGE_DIR,
    RESUME_DIR,
    PHOTO_DIR,
    REPORT_DIR
]:
    os.makedirs(folder, exist_ok=True)