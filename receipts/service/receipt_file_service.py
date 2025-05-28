import os
from uuid import uuid4
import pytesseract
from PyPDF2 import PdfReader
from django.conf import settings
from django.forms import model_to_dict
from django.utils import timezone
from pdf2image import convert_from_path
from automate_accounts.settings import POPPLER_PATH
from receipts.models import (
    ReceiptFile,
    Receipt
)
from resources.common_functions.text_extract_date import extract_date
from resources.common_functions.text_extract_merchant import extract_merchant
from resources.common_functions.text_extract_total import extract_total


def handle_upload(file):
    # GENERATE UNIQUE FILENAME
    original_name = file.name
    extension = os.path.splitext(original_name)[1]

    new_filename = f"{uuid4().hex}{extension}"
    # SAVE THE FILE MANUALLY
    file_path = os.path.join("receipts", new_filename)

    if extension != '.pdf':
        receipt_file = ReceiptFile.objects.create(
            file_name=original_name,
            file_path=file_path,
            is_valid=False,
            invalid_reason="Invalid file type",
            is_processed=False,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        res = model_to_dict(receipt_file, fields=['receipt_file_id', 'file_name'])
        return res

    absolute_path = os.path.join(settings.MEDIA_ROOT, file_path)
    os.makedirs(os.path.dirname(absolute_path), exist_ok=True)

    with open(absolute_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # CREATE A RECEIPTFILE RECORD
    receipt_file = ReceiptFile.objects.create(
        file_name=original_name,
        file_path=file_path,
        is_valid=False,
        invalid_reason=None,
        is_processed=False,
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    res = model_to_dict(receipt_file, fields=['receipt_file_id', 'file_name'])
    return res


def validate_pdf(receipt_file: ReceiptFile):
    try:
        pdf_path = os.path.join(settings.MEDIA_ROOT, str(receipt_file.file_path))
        PdfReader(pdf_path)
        receipt_file.is_valid = True
        receipt_file.invalid_reason = ''

    except Exception as e:
        receipt_file.is_valid = False
        receipt_file.invalid_reason = str(e)

    receipt_file.save()
    return model_to_dict(receipt_file, fields=['receipt_file_id', 'file_name', 'is_valid', 'invalid_reason'])


def validate_receipt(validated_data):
    result = []
    receipt_ids_list = validated_data.get("receipt_file_ids", [])
    found_receipts = ReceiptFile.objects.filter(
        receipt_file_id__in=receipt_ids_list
    )

    for _pdf in found_receipts:
        result.append(validate_pdf(_pdf))

    return result


def extract_text_from_pdf(file_path):
    pdf_path = os.path.join(settings.MEDIA_ROOT, file_path)
    images = convert_from_path(
        str(pdf_path),
        dpi=300,
        poppler_path=POPPLER_PATH
    )
    full_text = ""
    for image in images:
        text = pytesseract.image_to_string(image)
        full_text += text + "\n"
    return full_text

def process_receipt(receipt_file: ReceiptFile):
    if not receipt_file.is_valid:
        raise ValueError("Cannot process invalid receipt")

    text = extract_text_from_pdf(str(receipt_file.file_path))
    purchased_at = extract_date(text)
    merchant_name = extract_merchant(text)
    total_amount = extract_total(text)

    # UPDATE PROCESS FLAG
    receipt_file.is_processed = True
    receipt_file.save()

    receipt, created = Receipt.objects.update_or_create(
        receipt_file=receipt_file,
        defaults={
            'purchased_at': purchased_at,
            'merchant_name': merchant_name,
            'total_amount': total_amount
        }
    )
    receipt_file.is_processed = True
    receipt_file.save()
    return receipt


def fetch_all_un_process_receipt():
    found_receipt = ReceiptFile.objects.filter(
        is_valid=True,
        is_processed=False
    )
    return found_receipt
