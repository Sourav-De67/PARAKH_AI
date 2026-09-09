
import re
from difflib import SequenceMatcher


def fuzzy_match(text, words, threshold=0.65):

    text_words = re.findall(r"[a-zA-Z]+", text.lower())

    for word in text_words:

        for target in words:

            similarity = SequenceMatcher(
                None,
                word,
                target
            ).ratio()

            if similarity >= threshold:
                return True

    return False


def detect_fields(text):

    text = text.lower()

    results = {}


    # =====================================
    # COMMON / GENERIC NAME
    # =====================================

    results["Common / Generic Name"] = bool(

        re.search(
            r"product\s*name|common\s*name|generic\s*name|"
            r"name\s*of\s*(the\s*)?commodity",
            text
        )

    )


    # =====================================
    # NET QUANTITY
    # =====================================

    results["Net Quantity"] = bool(

        re.search(
            r"net\s*(qty|quantity|wt|weight)",
            text
        )

        or

        re.search(
            r"\b\d+(\.\d+)?\s*(g|kg|ml|l)\b",
            text
        )

        or

        re.search(
            r"\b\d+\s*(gram|grams|kg|kilogram|ml|liter|litre)\b",
            text
        )

    )


    # =====================================
    # MRP
    # =====================================

    results["MRP"] = bool(

        re.search(
            r"\bmrp\b|m\.r\.p|maximum\s*retail\s*price|₹|rs\.?",
            text
        )

        or

        fuzzy_match(
            text,
            ["mrp"],
            0.60
        )

    )


    # =====================================
    # MANUFACTURER
    # =====================================

    results["Manufacturer"] = bool(

        re.search(
            r"manufactured\s*by|manufactured\s*at|manufactured\s*for|"
            r"marketed\s*by|manufacturer|mfg\s*by|mfd\s*by|"
            r"packed\s*by|packer|brand\s*owner",
            text
        )

        or

        fuzzy_match(
            text,
            [
                "manufactured",
                "manufacturer",
                "marketed",
                "manufacture",
                "packer"
            ],
            0.60
        )

    )


    # =====================================
    # MANUFACTURING DATE
    # =====================================

    results["Manufacturing Date"] = bool(

        re.search(
            r"\bmfd\b|\bmfg\b|manufacturing\s*date|"
            r"date\s*of\s*manufacture|manufactured\s*on",
            text
        )

        or

        fuzzy_match(
            text,
            [
                "mfd",
                "mfg",
                "manufacturing",
                "manufactured"
            ],
            0.60
        )

    )


    # =====================================
    # CONSUMER CARE
    # =====================================

    results["Consumer Care"] = bool(

        re.search(
            r"consumer\s*care|customer\s*care|"
            r"helpline|toll\s*free|contact\s*us",
            text
        )

        or

        fuzzy_match(
            text,
            [
                "consumer",
                "customer",
                "helpline",
                "contact"
            ],
            0.60
        )

    )


    return results


# =====================================
# TEST
# =====================================

if __name__ == "__main__":

    sample_text = """
    Common Name: Biscuits
    MRP Rs. 50
    Net Qty 100g
    Marketed by ITC LTD.
    MFD 05/2026
    Consumer Care 1800 123 456
    """

    detected = detect_fields(sample_text)

    print("Detected Fields:")

    for field, found in detected.items():

        if found:
            print("✓", field)
        else:
            print("✗", field)