# ⚖️ PARAKH AI

**AI-powered Packaged Commodity Compliance Detection System**

PARAKH AI is a Flask-based web application that automatically checks whether packaged commodity labels comply with the **Legal Metrology (Packaged Commodities) Rules (LMPC), India**. It uses OCR to extract label text, verifies mandatory declarations, calculates a compliance score, generates PDF reports, and stores scan history in SQLite.

---

## 🚀 Features

* 📷 Upload packaged commodity images
* 🔍 OCR using Tesseract
* 🖼️ OpenCV image preprocessing
* 📦 Packaged commodity detection
* ✅ LMPC declaration verification
* 📊 Compliance score generation
* ⚠️ Compliant / Verification Required / Non-Compliant status
* 📄 Automatic PDF report generation
* 💾 SQLite database for scan history

---

## 🛠️ Tech Stack

| Technology    | Purpose                   |
| ------------- | ------------------------- |
| Python        | Core programming language |
| Flask         | Web framework             |
| OpenCV        | Image preprocessing       |
| Tesseract OCR | Text extraction           |
| SQLite        | Scan history database     |
| ReportLab     | PDF report generation     |
| HTML/CSS      | User Interface            |

---

## 📂 Project Structure

<escape>SIH-26034/
│
├── app.py                 # Main Flask application
├── detector.py            # Declaration detection logic
├── compliance.py          # LMPC compliance engine
├── database.py            # SQLite operations
├── report.py              # PDF report generation
├── parakh_ai.db           # SQLite database
├── uploads/               # Uploaded images
├── reports/               # Generated PDF reports
├── templates/             # HTML templates
├── static/                # CSS and assets
└── README.md</escape>

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/PARAKH-AI.git
cd PARAKH-AI
```

### 2. Install dependencies

```bash
pip install flask opencv-python pytesseract reportlab
```

### 3. Install Tesseract OCR

Download and install Tesseract OCR for Windows.

Default installation path:

<escape>```
C:\Program Files\Tesseract-OCR\tesseract.exe

````</escape>

Update the path in `app.py` if necessary.

### 4. Run the application

```bash
python app.py
````

Open:

<escape>```
http://127.0.0.1:5000

```</escape>

---

## 📋 How It Works

1. User uploads a packaged commodity image.
2. OpenCV enhances image quality.
3. Tesseract extracts text.
4. The commodity detector verifies whether it is a packaged product.
5. The LMPC compliance engine checks mandatory declarations.
6. A compliance score is calculated.
7. The result is displayed.
8. A PDF report is generated when required.
9. The scan is stored in SQLite.

---

## 📊 Compliance Categories

| Score | Result |
|-------|--------|
| 96–100% | Compliant |
| 86–95% | Verification Required |
| Below 86% | Non-Compliant |

---

## 🔍 Mandatory Declarations Checked

- Manufacturer / Packer / Importer
- Common / Generic Name
- Net Quantity
- MRP
- Unit Sale Price
- Consumer Care Details
- Relevant Date Declaration

### Conditional Declarations

- Country of Origin
- Best Before / Use By
- Dimensions

---

## 📄 PDF Report

The generated report includes:

- Uploaded product image
- Compliance score
- Compliance status
- LMPC declaration checklist
- Inspection disclaimer

---

## 💾 Database

SQLite stores every scan automatically.

Stored information includes:

- Image name
- Compliance status
- Compliance score
- Declaration detection results
- Scan timestamp

---

## 🎯 Future Scope

- Multi-language OCR
- Barcode/QR verification
- Inspector dashboard
- Cloud database support
- Mobile application

---

## 👨‍💻 Developed By

**PARAKH AI Team**

Built as a Smart India Hackathon (SIH) prototype for automated packaged commodity compliance verification.
```
