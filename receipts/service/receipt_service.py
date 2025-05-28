from receipts.models import Receipt


def fetch_all_process_receipts(filter_para):
    q_filter = {}
    if filter_para:
        query_keys = filter_para.keys()
        model_fields = {field.name for field in Receipt._meta.get_fields()}
        valid_filter_keys = set(query_keys).intersection(model_fields)
        q_filter = {key: filter_para[key] for key in valid_filter_keys}
    result = Receipt.objects.filter(**q_filter).all()
    return result

def fetch_process_receipt_by_id(receipt_id, filter_para):
    if not receipt_id:
        raise ValueError("receipt_id cannot be None")

    found_receipt = Receipt.objects.filter(
        receipt_id=receipt_id
    )

    if not found_receipt:
        raise ValueError("receipt_id does not exist")
    return found_receipt.first()