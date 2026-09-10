from flask import Flask, render_template, request, send_from_directory, send_file
import os
import pytesseract
import cv2

from compliance import check_compliance
from detector import detect_fields, is_packaged_commodity
from report import generate_report


# ==========================================================
# TESSERACT CONFIGURATION
# ==========================================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ==========================================================
# FLASK APP
# ==========================================================

app = Flask(__name__)


# ==========================================================
# UPLOAD FOLDER
# ==========================================================

UPLOAD_FOLDER = os.path.join(
    app.root_path,
    "uploads"
)

REPORT_FOLDER = os.path.join(
    app.root_path,
    "reports"
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)


# ==========================================================
# HOME PAGE
# ==========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


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
# DOWNLOAD PDF REPORT
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
# SCAN PRODUCT
# ==========================================================

@app.route("/scan", methods=["POST"])
def scan():

    # ------------------------------------------------------
    # GET IMAGE
    # ------------------------------------------------------

    image_file = request.files.get(
        "product_image"
    )

    if image_file is None or image_file.filename == "":

        return "No image selected!"


    # ------------------------------------------------------
    # SAVE IMAGE
    # ------------------------------------------------------

    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        image_file.filename
    )

    image_file.save(
        image_path
    )


    # ------------------------------------------------------
    # READ IMAGE
    # ------------------------------------------------------

    image = cv2.imread(
        image_path
    )

    if image is None:

        return "Error: Could not read the uploaded image."


    # ------------------------------------------------------
    # RESIZE IMAGE FOR BETTER OCR
    # ------------------------------------------------------

    image = cv2.resize(
        image,
        None,
        fx=5,
        fy=5,
        interpolation=cv2.INTER_CUBIC
    )


    # ------------------------------------------------------
    # CONVERT TO GRAYSCALE
    # ------------------------------------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


    # ------------------------------------------------------
    # IMPROVE CONTRAST
    # ------------------------------------------------------

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    threshold = clahe.apply(
        gray
    )


    # ------------------------------------------------------
    # OCR
    # ------------------------------------------------------

    ocr_text = pytesseract.image_to_string(
        threshold,
        config="--psm 11"
    )


    # ======================================================
    # COMMODITY CHECK
    # ======================================================

    commodity_detected = is_packaged_commodity(
        ocr_text
    )


    # ------------------------------------------------------
    # NOT A PACKAGED COMMODITY
    # ------------------------------------------------------

    if not commodity_detected:

        results = {}

        status = "NON-COMPLIANT"

        percentage = 0

        return render_template(

            "result.html",

            image_filename=image_file.filename,

            results=results,

            status=status,

            percentage=percentage,

            ocr_text=ocr_text,

            commodity_detected=False

        )


    # ======================================================
    # PACKAGED COMMODITY DETECTED
    # ======================================================

    detected = detect_fields(
        ocr_text
    )


    # ------------------------------------------------------
    # GET DETECTED FIELDS
    # ------------------------------------------------------

    detected_fields = [

        field

        for field, found in detected.items()

        if found

    ]


    # ------------------------------------------------------
    # CHECK COMPLIANCE
    # ------------------------------------------------------

    results, status, percentage = check_compliance(

        detected_fields,

        ocr_text

    )


    # ======================================================
    # GENERATE PDF REPORT
    # ======================================================

    report_filename = (

        os.path.splitext(
            image_file.filename
        )[0]

        + "_compliance_report.pdf"

    )


    report_path = os.path.join(

        app.config["REPORT_FOLDER"],

        report_filename

    )


    # ------------------------------------------------------
    # ONLY GENERATE REPORT FOR:
    #
    # NON-COMPLIANT
    # VERIFICATION REQUIRED
    # ------------------------------------------------------

    if status in [

        "Non-Compliant",
        "Verification Required",
        "NON-COMPLIANT"

    ]:

        generate_report(

            output_path=report_path,

            status=status,

            percentage=percentage,

            results=results,

            ocr_text=ocr_text,

            image_path=image_path

        )


    # ------------------------------------------------------
    # SHOW RESULT PAGE
    # ------------------------------------------------------

    return render_template(

        "result.html",

        image_filename=image_file.filename,

        results=results,

        status=status,

        percentage=percentage,

        ocr_text=ocr_text,

        commodity_detected=True,

        report_filename=report_filename

    )


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )