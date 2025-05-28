import re


def extract_total(text):
    total_patterns = [
        # TRANSACTION AMOUNT: 12.90 or TRANSACTION AMOUNT $12.90
        r"\bTRANSACTION AMOUNT\s*\$?\s*(\d+[\.,] ?\d{2})",

        # Total: 123.45 or Total - $99.99 or Total 80.00 or Total 134. 64
        r"\bTotal\s*[:\-]?\s*\$?\s*(\d+[\.,] ?\d{2})",

        # Amount: 45.67 or Amount - $77.20 or Amount 100.00
        r"\bAmount\s*[:\-]?\s*\$?\s*(\d+[\.,] ?\d{2})",

        # Balance Due 134. 64
        r"\bBalance\s+Due\s*\$?\s*(\d+[\.,] ?\d{2})",

        # $123.45 or $ 12.95
        r"\$\s*(\d+[\.,] ?\d{2})\b",
    ]

    for pattern in total_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Clean up number by removing spaces and replacing comma with dot if needed
            cleaned = match.group(1).replace(" ", "").replace(",", ".")
            try:
                return float(cleaned)
            except ValueError:
                continue
    return None
