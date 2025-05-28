import spacy

nlp = spacy.load("en_core_web_sm")


def extract_merchant_name(text):
    # NPL BASED CHAR RECOGNITIONS
    doc = nlp(text)
    orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    return orgs[0] if orgs else None


def extract_merchant_heuristic(text):
    lines = text.strip().split("\n")
    # PICK FIRST LINE WITH MOSTLY UPPERCASE LETTERS OR LENGTH > 3
    # CHECK FIRST 5 LINES
    for line in lines[:5]:
        if line.isupper() or len(line) > 3:
            return line.strip()
    return None


def extract_merchant(text):
    merchant = extract_merchant_name(text)
    if merchant:
        return merchant
    # FALL BACK OPTION FOR MERCHANT NAME
    return extract_merchant_heuristic(text)
