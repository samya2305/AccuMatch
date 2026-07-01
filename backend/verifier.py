import re
from rapidfuzz import fuzz


def clean_text(text):

    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text.replace(" ", "").strip()


def verify_text(field, value1, value2):

    value1 = clean_text(value1)
    value2 = clean_text(value2)

    if not value1 or not value2:
        return {
            "field": field,
            "offer_value": value1,
            "document_value": value2,
            "score": 0,
            "status": "MISSING_DATA"
        }

    score = fuzz.ratio(value1, value2)

    if score >= 90:
        status = "MATCH"

    elif score >= 75:
        status = "PARTIAL_MATCH"

    else:
        status = "MISMATCH"

    return {
        "field": field,
        "offer_value": value1,
        "document_value": value2,
        "score": round(score, 2),
        "status": status
    }


def verify_name(offer_name, aadhaar_name,
                college_name, resume_name):

    candidates = [
        aadhaar_name,
        college_name,
        resume_name
    ]

    best_score = 0
    best_name = ""

    offer = clean_text(offer_name)

    for name in candidates:

        candidate = clean_text(name)

        if not candidate:
            continue

        score = fuzz.ratio(
            offer,
            candidate
        )

        if score > best_score:
            best_score = score
            best_name = candidate

    if best_score >= 90:
        status = "MATCH"

    elif best_score >= 75:
        status = "PARTIAL_MATCH"

    else:
        status = "MISMATCH"

    return {
        "field": "Name",
        "offer_value": offer,
        "document_value": best_name,
        "score": round(best_score, 2),
        "status": status
    }