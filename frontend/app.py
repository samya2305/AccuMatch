import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)
import streamlit as st
import requests

from backend.file_handler import save_uploaded_file

from backend.config import (
    OFFER_DIR,
    AADHAAR_DIR,
    COLLEGE_DIR,
    RESUME_DIR,
    PHOTO_DIR
)

st.set_page_config(
    page_title="AccuMatch",
    layout="wide"
)

st.title("AccuMatch")
st.subheader(
    "AI Powered Document Verification System"
)

st.markdown("---")

offer = st.file_uploader(
    "Upload Offer Letter",
    type=["pdf"]
)

aadhaar = st.file_uploader(
    "Upload Aadhaar Card",
    type=["jpg", "jpeg", "png", "pdf"]
)

college = st.file_uploader(
    "Upload College ID",
    type=["jpg", "jpeg", "png", "pdf"]
)

resume = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

photo = st.file_uploader(
    "Upload Passport Size Photo",
    type=["jpg", "jpeg", "png"]
)

st.markdown("---")

if st.button("Verify Documents"):

    if not all([
        offer,
        aadhaar,
        college,
        resume,
        photo
    ]):

        st.error(
            "Please upload all required documents."
        )

    else:

        try:

            # Save uploaded files

            offer_path = save_uploaded_file(
                offer,
                OFFER_DIR
            )

            aadhaar_path = save_uploaded_file(
                aadhaar,
                AADHAAR_DIR
            )

            college_path = save_uploaded_file(
                college,
                COLLEGE_DIR
            )

            resume_path = save_uploaded_file(
                resume,
                RESUME_DIR
            )

            photo_path = save_uploaded_file(
                photo,
                PHOTO_DIR
            )

            st.info(
                "Documents uploaded successfully."
            )

            # Call backend API (use local backend)

            response = requests.get("http://127.0.0.1:8000/verify")

            if response.status_code == 200:

                result = response.json()

                st.success(
                    "Verification Completed Successfully"
                )

                st.markdown("## Verification Result")

                st.json(result)

                if "final_score" in result:

                    st.metric(
                        "Verification Score",
                        round(
                            result["final_score"],
                            2
                        )
                    )

                if "status" in result:

                    status = result["status"]

                    if status == "VERIFIED":

                        st.success(
                            f"Status : {status}"
                        )

                    elif status == "REVIEW_REQUIRED":

                        st.warning(
                            f"Status : {status}"
                        )

                    else:

                        st.error(
                            f"Status : {status}"
                        )

            else:

                st.error(
                    "Backend Verification Failed"
                )

        except Exception as e:

            st.error(
                f"Error : {str(e)}"
            )