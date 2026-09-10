import cv2
import pytesseract

from detector import detect_fields


# Tell Python where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ==========================================
# READ IMAGE
# ==========================================

image = cv2.imread("packet.png")

if image is None:
    print("Error: packet.png not found!")
    exit()


# ==========================================
# METHOD 1
# Upscale + Grayscale
# ==========================================

image_up = cv2.resize(
    image,
    None,
    fx=5,
    fy=5,
    interpolation=cv2.INTER_CUBIC
)

gray = cv2.cvtColor(
    image_up,
    cv2.COLOR_BGR2GRAY
)


# ==========================================
# METHOD 2
# OTSU THRESHOLD
# ==========================================

otsu = cv2.threshold(
    gray,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)[1]


# ==========================================
# METHOD 3
# ADAPTIVE THRESHOLD
# ==========================================

adaptive = cv2.adaptiveThreshold(
    gray,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    31,
    11
)


# ==========================================
# METHOD 4
# CLAHE CONTRAST ENHANCEMENT
# ==========================================

clahe = cv2.createCLAHE(
    clipLimit=2.0,
    tileGridSize=(8, 8)
)

enhanced = clahe.apply(gray)


# ==========================================
# FUNCTION TO TEST OCR
# ==========================================

def test_ocr(name, processed_image):

    print("\n")
    print("=" * 70)
    print(name)
    print("=" * 70)

    text = pytesseract.image_to_string(
        processed_image,
        config="--psm 11"
    )

    print("\nOCR TEXT:")
    print(text)

    detected = detect_fields(text)

    print("\nDETECTED FIELDS:")

    count = 0

    for field, found in detected.items():

        if found:
            print("✓", field)
            count += 1

        else:
            print("✗", field)

    print("\nFIELDS DETECTED:", count, "/ 6")

    return count


# ==========================================
# RUN ALL METHODS
# ==========================================

score1 = test_ocr(
    "METHOD 1 - UPSCALE + GRAYSCALE",
    gray
)

score2 = test_ocr(
    "METHOD 2 - OTSU THRESHOLD",
    otsu
)

score3 = test_ocr(
    "METHOD 3 - ADAPTIVE THRESHOLD",
    adaptive
)

score4 = test_ocr(
    "METHOD 4 - CLAHE ENHANCEMENT",
    enhanced
)


# ==========================================
# FINAL COMPARISON
# ==========================================

print("\n")
print("=" * 70)
print("FINAL COMPARISON")
print("=" * 70)

print("Method 1 - Upscale + Grayscale :", score1, "/ 6")
print("Method 2 - OTSU Threshold      :", score2, "/ 6")
print("Method 3 - Adaptive Threshold  :", score3, "/ 6")
print("Method 4 - CLAHE Enhancement   :", score4, "/ 6")

print("=" * 70)