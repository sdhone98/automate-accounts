# 📖 Full API Documentation

---

## 1. Upload Raw Receipts

- **POST** `/upload`
- **Description:** Upload one or more PDF receipts for OCR processing.

### Request

- **Content-Type:** `multipart/form-data`
- **Field:** `file` (repeatable for multiple PDFs)

### Example cURL

```bash
curl --location 'http://127.0.0.1:8000/upload/' \
--form 'file=@"/path/to/receipt1.pdf"' \
--form 'file=@"/path/to/receipt2.pdf"'
```

### Example cURL
```
{
    "data": {
        "data": [
            {
                "receipt_file_id": "REF17483742305827",
                "file_name": "beerhouse_20231209_005.pdf"
            }
        ],
        "ids": [
            "REF17483742305827"
        ]
    },
    "message": "Receipt uploaded successfully.",
    "status_code": 201,
    "type": "Success",
    "time_stamp": "2025-05-27T19:30:30.169420Z"
}
```

---

## 2. Validate Uploaded PDFs

- **POST** `/validate`
- **Description:** Validates one or more uploaded PDF receipts. Checks if each file is a valid PDF and stores the validation result.

### Request

- **Content-Type:** `application/json`
- **Body Parameters:** `receipt_file_ids` (List of receipt file IDs that get from upload api)

### Example cURL

```bash
curl --location 'http://127.0.0.1:8000/validate' \
--header 'Content-Type: application/json' \
--data '{
    "receipt_file_ids": [
            "REF17483742305827"
        ]
}'
```

### Response Example
```
{
    "data": [
        {
            "receipt_file_id": "REF17483742305827",
            "file_name": "beerhouse_20231209_005.pdf",
            "is_valid": true,
            "invalid_reason": ""
        }
    ],
    "message": "Receipts validated successfully.",
    "status_code": 200,
    "type": "Success",
    "time_stamp": "2025-05-27T20:46:06.674519Z"
}
```

---

## 3. Process Validated PDFs

- **POST** `/process`
- **Description:** Processes one or more validated receipt files by extracting details like purchase date, merchant name, and total amount. Marks receipts as processed in the system.

### Request

- **Content-Type:** `application/json`
- **Body Parameters:** `receipt_file_ids` (List of receipt file IDs to be processed)

### Example cURL

```bash
curl --location 'http://127.0.0.1:8000/process' \
--header 'Content-Type: application/json' \
--data '{
    "receipt_file_ids": [
            "REF17483742305827"
        ]
}'
```

### Response Example
```
{
    "data": [],
    "message": "All Receipts Processed",
    "status_code": 200,
    "type": "Success",
    "time_stamp": "2025-05-27T19:39:32.195651Z"
}
```

---

## 4. Get List of Un-Process PDFs Details 

- **GET** `/un-process`
- **Description:** Returns a list of all uploaded receipts that are valid but have not yet been processed.

### Request

- **Content-Type:** `application/json`

### Example cURL

```bash
curl --location --request GET 'http://127.0.0.1:8000/un-process' \
--form 'file=@"/C:/Users/sdhon/Desktop/Sagar Dhone.pdf"'
```

### Response Example
```
{
    "data": [
        {
            "receipt_file_id": "REF17483792619932",
            "file_name": "cvs_20231209_006.pdf",
            "file_path": "/media/receipts/d6600701938441379a5b016296f9031f.pdf",
            "is_valid": true,
            "invalid_reason": "",
            "is_processed": false,
            "created_at": "2025-05-28T02:24:21.566967",
            "updated_at": "2025-05-28T02:24:36.786462"
        }
    ],
    "message": "Fetch Un-Process Receipt successfully.",
    "status_code": 200,
    "type": "Success",
    "time_stamp": "2025-05-27T20:54:39.289988Z"
}
```

---

## 5. Get all Processed Receipts Data

- **GET** `/receipts`
- **Description:** Retrieves receipts that have been successfully processed, including extracted data like merchant name, total amount, and purchase date.

### Request

- **Content-Type:** `application/json`

### Example cURL

```bash
curl --location 'http://127.0.0.1:8000/receipts'
```

### Response Example
```
{
    "data": [
        {
            "receipt_id": "RCP17483746179454",
            "purchased_at": "2023-11-28T00:00:00",
            "merchant_name": "Firestone",
            "total_amount": "38.50",
            "created_at": "2025-05-28T01:06:57.576936",
            "updated_at": "2025-05-28T01:09:32.182649",
            "file_path": "REF17483742305827"
        },
        {
            "receipt_id": "RCP17483794820169",
            "purchased_at": null,
            "merchant_name": "MASTERCARD",
            "total_amount": null,
            "created_at": "2025-05-28T02:28:02.223190",
            "updated_at": "2025-05-28T02:28:02.223190",
            "file_path": "REF17483792619932"
        }
    ],
    "message": "All Receipt Fetch successfully.",
    "status_code": 200,
    "type": "Success",
    "time_stamp": "2025-05-27T20:58:04.200838Z"
}
```

---

## 6. Get Specific Processed Receipt Data by ID

- **GET** `/receipts/{receipt_id}`
- **Description:** Fetches a single processed receipt using the provided receipt_id. Returns the merchant name, purchase date, total amount, and associated file.

### Request

- **Content-Type:** `application/json`
- **Path Parameters:** `receipt_id` (The unique identifier of the receipt)

### Example cURL

```bash
curl --location 'http://127.0.0.1:8000/receipts/RCP17483746179454'
```

### Response Example
```
{
    "data": {
        "receipt_id": "RCP17483746179454",
        "purchased_at": "2023-11-28T00:00:00",
        "merchant_name": "Firestone",
        "total_amount": "38.50",
        "created_at": "2025-05-28T01:06:57.576936",
        "updated_at": "2025-05-28T01:09:32.182649",
        "file_path": "REF17483742305827"
    },
    "message": "Receipt fetched successfully.",
    "status_code": 200,
    "type": "Success",
    "time_stamp": "2025-05-27T21:01:37.044562Z"
}
```




