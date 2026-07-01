import os
import pandas as pd

REPORT_FOLDER = "../reports"

EXCEL_FILE = os.path.join(
    REPORT_FOLDER,
    "verification_report.xlsx"
)


def save_report(data):
    # Create reports directory if it doesn't exist
    os.makedirs(
        REPORT_FOLDER,
        exist_ok=True
    )

    new_row = {
        "Name": data.get("name", ""),
        "Email": data.get("email", ""),
        "Phone Number": data.get("phone_number", ""),
        "Register Number": data.get("register_number", ""),
        "College Name": data.get("college_name", ""),
        "Aadhaar Number": data.get("aadhaar_number", ""),
        "Shift Timing": data.get("shift_timing", ""),
        "Final Score": data.get("final_score", ""),
        "Status": data.get("status", "")
    }

    # Read existing Excel file safely
    if os.path.exists(EXCEL_FILE):
        try:
            df = pd.read_excel(
                EXCEL_FILE,
                engine="openpyxl"
            )
        except Exception:
            # If the file is empty or corrupted, create a new DataFrame
            df = pd.DataFrame()
    else:
        df = pd.DataFrame()

    # Append the new row
    df = pd.concat(
        [df, pd.DataFrame([new_row])],
        ignore_index=True
    )

    # Save back to Excel
    df.to_excel(
        EXCEL_FILE,
        index=False,
        engine="openpyxl"
    )

    CSV_FILE = os.path.join(
    REPORT_FOLDER,
    "verification_report.csv"
    )

    df.to_csv(
    CSV_FILE,
    index=False
    )

    return True
