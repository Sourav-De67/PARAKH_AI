from flask import Flask, render_template, request, send_from_directory
import os
import pytesseract
import cv2

from compliance import check_compliance
from detector import detect_fields


# Tell Python where Tesscd p    eract is installed
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


app = Flask(__name__)


# Folder where uploaded product images are stored
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Make sure uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==============================
# HOME PAGE
# ==============================

@app.route("/")
def home():
    return render_template("index.html")


# ==============================
# DISPLAY UPLOADED IMAGE
# ==============================

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# ==============================
# SCAN PRODUCT
# ==============================

@app.route("/scan", methods=["POST"])
def scan():

    # Get uploaded image
    image_file = request.files.get("product_image")

    if image_file is None or image_file.filename == "":
        return "No image selected!"


    # Save image
    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        image_file.filename
    )

    image_file.save(image_path)


    # ==============================
    # STEP 1: READ IMAGE
    # ==============================

    image = cv2.imread(image_path)

    if image is None:
        return "Error: Could not read the uploaded image."


    # ==============================
    # STEP 2: UPSCALE IMAGE
    # ==============================

    image = cv2.resize(
        image,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )


    # ==============================
    # STEP 3: GRAYSCALE
    # ==============================

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


    # ==============================
    # STEP 4: IMPROVE TEXT VISIBILITY
    # ==============================

    threshold = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]


    # ==============================
    # STEP 5: OCR
    # ==============================

    ocr_text = pytesseract.image_to_string(
        threshold,
        config="--psm 11"
    )


    # ==============================
    # STEP 6: DETECT DECLARATIONS
    # ==============================

    detected = detect_fields(ocr_text)


    # Convert detected dictionary
    # into list of detected fields

    detected_fields = [
        field
        for field, found in detected.items()
        if found
    ]


    # ==============================
    # STEP 7: COMPLIANCE CHECK
    # ==============================

    results, status = check_compliance(
        detected_fields
    )


    # ==============================
    # STEP 8: SHOW RESULT
    # ==============================

    return render_template(
        "result.html",
        image_filename=image_file.filename,
        results=results,
        status=status,
        ocr_text=ocr_text
    )


# ==============================
# START FLASK SERVER
# ==============================

if __name__ == "__main__":
    app.run(debug=True)