import re
from datetime import datetime

def extract_date(text):
    date_patterns = [
        # MM/DD/YYYY or M/D/YYYY
        (r"\b\d{1,2}/\d{1,2}/\d{4}\b", "%m/%d/%Y"),

        # MM-DD-YYYY or M-D-YYYY
        (r"\b\d{1,2}-\d{1,2}-\d{4}\b", "%m-%d-%Y"),

        # DD/MM/YYYY or D/M/YYYY
        (r"\b\d{1,2}/\d{1,2}/\d{4}\b", "%d/%m/%Y"),

        # DD-MM-YYYY or D-M-YYYY
        (r"\b\d{1,2}-\d{1,2}-\d{4}\b", "%d-%m-%Y"),

        # YYYY/MM/DD
        (r"\b\d{4}/\d{1,2}/\d{1,2}\b", "%Y/%m/%d"),

        # YYYY-MM-DD
        (r"\b\d{4}-\d{1,2}-\d{1,2}\b", "%Y-%m-%d"),

        # MM/DD/YY or M/D/YY
        (r"\b\d{1,2}/\d{1,2}/\d{2}\b", "%m/%d/%y"),

        # MM-DD-YY or M-D-YY
        (r"\b\d{1,2}-\d{1,2}-\d{2}\b", "%m-%d-%y"),

        # DD/MM/YY or D/M/YY
        (r"\b\d{1,2}/\d{1,2}/\d{2}\b", "%d/%m/%y"),

        # DD-MM-YY or D-M-YY
        (r"\b\d{1,2}-\d{1,2}-\d{2}\b", "%d-%m-%y"),

        # DD/M/YYYY
        (r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "%m/%d/%Y"),

        # DD/M/YYYY 00:00 AM
        (r"\b\d{1,2}/\d{1,2}/\d{2,4}\s\d{1,2}:\d{1,2}\s*(AM|PM|am|pm)\b", "%m/%d/%Y"),

        # Month DD, YYYY (November 27, 2023)
        (r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER|january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},\s+\d{4}\b",
         "%B %d, %Y"),

    ]

    for pattern, date_format in date_patterns:
        match = re.search(pattern, text)
        if match:
            try:
                return datetime.strptime(match.group(), date_format)
            except ValueError:
                continue

    return None