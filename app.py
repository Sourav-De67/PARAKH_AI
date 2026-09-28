from flask import Flask, render_template, request, send_from_directory, send_file
import os
import cv2
import pytesseract
import shutil

from detector import detect_fields, is_packaged_commodity
from compliance import check_compliance
from report import generate_report
from database import init_db, save_scan

# ==========================================================
# TESSERACT CONFIGURATION
# ==========================================================

# Windows locally, Linux on Render
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
else:
    pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract") or "tesseract"

# ==========================================================
# FLASK APP
# ==========================================================

app = Flask(__name__)

# ==========================================================
# FOLDERS
# ==========================================================

UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
REPORT_FOLDER = os.path.join(app.root_path, "reports")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

init_db()

# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():
    return render_template("index.html")

# ==========================================================
# SERVE UPLOADED IMAGE
# ==========================================================

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )

# ==========================================================
# DOWNLOAD REPORT
# ==========================================================

@app.route("/download-report/<filename>")
def download_report(filename):

    report_path = os.path.join(
        app.config["REPORT_FOLDER"],
        filename
    )

    if not os.path.exists(report_path):
        return "Report not found!", 404

    return send_file(
        report_path,
        as_attachment=True,
        download_name=filename
    )

# ==========================================================
# SCAN ROUTE
# ==========================================================

@app.route("/scan", methods=["POST"])
def scan():

    image_file = request.files.get("product_image")

    if image_file is None or image_file.filename == "":
        return "No image selected!"

    # ------------------------------------------------------
    # SAVE IMAGE
    # ------------------------------------------------------

    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        image_file.filename
    )

    image_file.save(image_path)

    # ------------------------------------------------------
    # READ IMAGE
    # ------------------------------------------------------

    image = cv2.imread(image_path)

    if image is None:
        return "Error reading uploaded image."

    # ------------------------------------------------------
    # IMAGE PREPROCESSING (RENDER OPTIMIZED)
    # ------------------------------------------------------

    height, width = image.shape[:2]

    max_width = 1400

    if width > max_width:
        scale = max_width / width

        image = cv2.resize(
            image,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_AREA
        )

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    processed = clahe.apply(gray)

    # ------------------------------------------------------
    # OCR (FASTER FOR RENDER)
    # ------------------------------------------------------

    try:
        ocr_text = pytesseract.image_to_string(
            processed,
            config="--oem 3 --psm 6",
            timeout=20
        )
    except RuntimeError:
        return render_template(
            "result.html",
            image_filename=image_file.filename,
            results={},
            status="Verification Required",
            percentage=0,
            commodity_detected=True,
            report_filename=None
        )

    # ------------------------------------------------------
    # COMMODITY CHECK
    # ------------------------------------------------------

    commodity_detected = is_packaged_commodity(ocr_text)

    if not commodity_detected:

        results = {}
        status = "NON-COMPLIANT"
        percentage = 0

        print("➡ Calling save_scan() for NON-COMMODITY", flush=True)

        save_scan(
            image_name=image_file.filename,
            status=status,
            percentage=percentage,
            results=results
        )

        print("⬅ Returned from save_scan()", flush=True)

        return render_template(
            "result.html",
            image_filename=image_file.filename,
            results=results,
            status=status,
            percentage=percentage,
            commodity_detected=False,
            report_filename=None
        )

    # ------------------------------------------------------
    # FIELD DETECTION
    # ------------------------------------------------------

    detected = detect_fields(ocr_text)

    detected_fields = [
        field
        for field, found in detected.items()
        if found
    ]

    # ------------------------------------------------------
    # COMPLIANCE CHECK
    # ------------------------------------------------------

    results, status, percentage = check_compliance(
        detected_fields,
        ocr_text
    )

    # ------------------------------------------------------
    # SAVE TO SQLITE DATABASE
    # ------------------------------------------------------

    print("➡ Calling save_scan()", flush=True)

    save_scan(
        image_name=image_file.filename,
        status=status,
        percentage=percentage,
        results=results
    )

    print("⬅ Returned from save_scan()", flush=True)

    # ------------------------------------------------------
    # GENERATE PDF REPORT
    # ------------------------------------------------------

    report_filename = (
        os.path.splitext(image_file.filename)[0]
        + "_compliance_report.pdf"
    )

    report_path = os.path.join(
        app.config["REPORT_FOLDER"],
        report_filename
    )

    if status in [
        "Verification Required",
        "Non-Compliant",
        "NON-COMPLIANT"
    ]:

        generate_report(
            output_path=report_path,
            status=status,
            percentage=percentage,
            results=results,
            image_path=image_path
        )

    # ------------------------------------------------------
    # RESULT PAGE
    # ------------------------------------------------------

    return render_template(
        "result.html",
        image_filename=image_file.filename,
        results=results,
        status=status,
        percentage=percentage,
        commodity_detected=True,
        report_filename=report_filename
    )

# ==========================================================
# RUN APP
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True)