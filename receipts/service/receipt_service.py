from receipts.models import Receipt


def fetch_all_process_receipts():
    return Receipt.objects.all()

def fetch_process_receipt_by_id(receipt_id):
    if not receipt_id:
        raise ValueError("receipt_id cannot be None")

    found_receipt = Receipt.objects.filter(
        receipt_id=receipt_id
    )

    if not found_receipt:
        raise ValueError("receipt_id does not exist")
    return found_receipt.first()