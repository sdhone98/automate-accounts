# 🧾 Automate Accounts Assignment

This is a Django-based web application that allows users to upload scanned PDF receipts, extract relevant data using OCR, and store the extracted information in a SQLite database. It also exposes RESTful APIs for upload, validation, processing, and retrieval of receipts.

---

## 🚀 Features

- Upload scanned receipt PDFs
- OCR-based text extraction
- Extract key data like date, merchant name, and total amount
- Validate and process receipts
- Store and retrieve receipt data via REST APIs

---

## 🧰 Prerequisites
- Python 3.9+
- pip
- virtualenv (recommended)
- Poppler (for PDF OCR)
- Tesseract

 ---

## ⚙️ Environment Variables

Create a `.env` file in your root directory and add:

```
DJANGO_SECRET_KEY=**APP KEY**
DEBUG_MODE=true
POPPLER_PATH=**ENTER YOUR SYSTEM LOCATED POPPLER PATH**
TESSERACT_CMD=**ADD TESSERACT ON SYSTEM ENV VARIBALES
```

- Make sure `poppler` is installed. You can download poppler for Windows [here](https://github.com/oschwartz10612/poppler-windows/releases/)
- also Make sure `tesseract` is installed. You can download tesseract for Windows [here](https://tesseract-ocr.github.io/)

---

## 🔧 Installation
### 1. Clone the repository
git clone https://github.com/your-username/automate-accounts-assignment.git
cd automate-accounts-assignment

### 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Create Test DB or Connect/Enter with DB 
create `db.sqlite3` file in main root dir.

### 5. Install NLP Model for Receipt Processing
python -m spacy download en_core_web_sm

### 6. Apply migrations
python manage.py migrate

### 7. Run the server
python manage.py runserver

---

## 🧪 Running the App
### Once the server is running, you can:

## 📚 API Endpoints Overview

| Method | Endpoint                      | Description                               |
|--------|-------------------------------|-------------------------------------------|
| POST   | `/upload`                     | Upload one or more PDF receipts           |
| POST   | `/validate`                   | Validate uploaded PDFs                    |
| POST   | `/process`                    | Process validated PDFs                    |
| GET    | `/un-process`                 | Get list of un-process PDFs details       |
| GET | `/receipts`                   | Get all processed receipts data           |
| GET | `/receipts/{receipt_id}` | Get specific processed receipt data by id |

➡️ Full API reference: [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

