from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import os
import shutil

from extractor import (
    extract_offer_letter,
    extract_aadhaar,
    extract_college_id,
    extract_resume
)

from verifier import (
    verify_text,
    verify_name
)

from report_generator import save_report

from config import (
    OFFER_DIR,
    AADHAAR_DIR,
    COLLEGE_DIR,
    RESUME_DIR,
    PHOTO_DIR
)

# -------------------------------------------------------
# APP
# -------------------------------------------------------

app = FastAPI(
    title="AccuMatch",
    version="1.0"
)

app.mount(
    "/static",
    StaticFiles(directory="../static"),
    name="static"
)

templates = Jinja2Templates(
    directory="../templates"
)

# -------------------------------------------------------
# HOME
# -------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

# -------------------------------------------------------
# UPLOAD
# -------------------------------------------------------

@app.post("/upload")
async def upload_documents(

    offer: UploadFile = File(...),
    aadhaar: UploadFile = File(...),
    college: UploadFile = File(...),
    resume: UploadFile = File(...),
    photo: UploadFile = File(...)
):

    # -----------------------------
    # Create Paths
    # -----------------------------

    offer_path = os.path.join(
        OFFER_DIR,
        offer.filename
    )

    aadhaar_path = os.path.join(
        AADHAAR_DIR,
        aadhaar.filename
    )

    college_path = os.path.join(
        COLLEGE_DIR,
        college.filename
    )

    resume_path = os.path.join(
        RESUME_DIR,
        resume.filename
    )

    photo_path = os.path.join(
        PHOTO_DIR,
        photo.filename
    )

    # -----------------------------
    # Save Offer
    # -----------------------------

    with open(offer_path, "wb") as f:
        shutil.copyfileobj(
            offer.file,
            f
        )

    # -----------------------------
    # Save Aadhaar
    # -----------------------------

    with open(aadhaar_path, "wb") as f:
        shutil.copyfileobj(
            aadhaar.file,
            f
        )

    # -----------------------------
    # Save College ID
    # -----------------------------

    with open(college_path, "wb") as f:
        shutil.copyfileobj(
            college.file,
            f
        )

    # -----------------------------
    # Save Resume
    # -----------------------------

    with open(resume_path, "wb") as f:
        shutil.copyfileobj(
            resume.file,
            f
        )

    # -----------------------------
    # Save Photo
    # -----------------------------

    with open(photo_path, "wb") as f:
        shutil.copyfileobj(
            photo.file,
            f
        )

    # Continue Verification

    return verify_documents(
        offer_path,
        aadhaar_path,
        college_path,
        resume_path
    )

# -------------------------------------------------------
# VERIFY
# -------------------------------------------------------

def verify_documents(

    offer_path,
    aadhaar_path,
    college_path,
    resume_path

):

    try:

        # -----------------------------------
        # EXTRACT DATA
        # -----------------------------------

        offer = extract_offer_letter(
            offer_path
        )

        aadhaar = extract_aadhaar(
            aadhaar_path
        )

        college = extract_college_id(
            college_path
        )

        resume = extract_resume(
            resume_path
        )

        # -----------------------------------
        # VERIFY NAME
        # -----------------------------------

        name_check = verify_name(

            offer.get("name", ""),

            aadhaar.get("name", ""),

            college.get("name", ""),

            resume.get("name", "")

        )

        # -----------------------------------
        # VERIFY COLLEGE
        # -----------------------------------

        college_check = verify_text(

            "College",

            offer.get("college", ""),

            college.get("college", "")

        )

        # -----------------------------------
        # VERIFY REGISTER NUMBER
        # -----------------------------------

        register_check = verify_text(

            "Register Number",

            offer.get("reg_no", ""),

            college.get("reg_no", "")

        )

        # -----------------------------------
        # VERIFY RESUME NAME
        # -----------------------------------

        resume_check = verify_text(

            "Resume Name",

            offer.get("name", ""),

            resume.get("name", "")

        )

        # -----------------------------------
        # FINAL SCORE
        # -----------------------------------

        final_score = round(

            (
                name_check["score"]
                + college_check["score"]
                + register_check["score"]
                + resume_check["score"]

            ) / 4,

            2

        )

        # -----------------------------------
        # FINAL STATUS
        # -----------------------------------

        if final_score >= 85:

            final_status = "VERIFIED"

        elif final_score >= 75:

            final_status = "REVIEW_REQUIRED"

        else:

            final_status = "REJECTED"

        # -----------------------------------
        # REPORT
        # -----------------------------------

        report = {

            "name": offer.get("name", ""),

            "email": resume.get("email", ""),

            "phone_number": aadhaar.get("phone_number", ""),

            "register_number": offer.get("reg_no", ""),

            "college_name": offer.get("college", ""),

            "aadhaar_number": aadhaar.get("aadhaar_number", ""),

            "shift_timing": offer.get("shift_timing", ""),

            "final_score": final_score,

            "status": final_status

        }

        # -----------------------------------
        # SAVE REPORT
        # -----------------------------------

        save_report(report)

        # -----------------------------------
        # RETURN RESULT
        # -----------------------------------

        return {

            "offer_letter": offer,

            "aadhaar": aadhaar,

            "college_id": college,

            "resume": resume,

            "name_check": name_check,

            "college_check": college_check,

            "register_check": register_check,

            "resume_check": resume_check,

            "final_score": final_score,

            "status": final_status

        }

    except Exception as e:

        import traceback

        traceback.print_exc()

        return {

            "error": str(e)

        }