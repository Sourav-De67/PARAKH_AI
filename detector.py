import re


# ==========================================================
# TEXT NORMALIZATION
# ==========================================================

def normalize_text(text):

    if not text:
        return ""

    text = text.lower()

    # Replace multiple spaces/newlines with one space
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================================
# CHECK WHETHER ANY PATTERN MATCHES
# ==========================================================

def matches_any(text, patterns):

    for pattern in patterns:

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):
            return True

    return False


# ==========================================================
# 1. MANUFACTURER / PACKER / IMPORTER
# ==========================================================

def detect_manufacturer(text):

    patterns = [

        r"manufactured\s+by",
        r"manufactured\s+at",
        r"manufactured\s+for",

        r"marketed\s+by",
        r"marketed\s+at",

        r"packed\s+by",
        r"packed\s+at",

        r"imported\s+by",
        r"importer\s*:"

    ]

    return matches_any(
        text,
        patterns
    )


# ==========================================================
# 2. COMMON / GENERIC NAME
# ==========================================================

def detect_common_name(text):

    patterns = [

        r"ingredients?",
        r"product\s*:",
        r"product\s+name",
        r"generic\s+name",
        r"common\s+name",

        r"atta",
        r"flour",
        r"rice",
        r"sugar",
        r"salt",
        r"spices?",
        r"biscuits?",
        r"cookies?",
        r"noodles?",
        r"pasta",
        r"chips?",
        r"snacks?"

    ]

    return matches_any(
        text,
        patterns
    )


# ==========================================================
# 3. NET QUANTITY
# ==========================================================

def detect_net_quantity(text):

    patterns = [

        r"net\s+(quantity|qty)",
        r"net\s+weight",
        r"net\s+volume",

        r"\b\d+(?:\.\d+)?\s*(?:mg|g|kg|ml|l|cl)\b",

        r"\b\d+(?:\.\d+)?\s*"
        r"(?:milligram|gram|kilogram|"
        r"millilitre|milliliter|litre|liter)\b"

    ]

    return matches_any(
        text,
        patterns
    )


# ==========================================================
# 4. MRP
# ==========================================================

def detect_mrp(text):

    patterns = [

        r"\bmrp\b",

        r"maximum\s+retail\s+price",

        r"retail\s+price",

        r"(?:₹|rs\.?|inr)\s*\.?\s*"
        r"\d+(?:\.\d{1,2})?"

    ]

    return matches_any(
        text,
        patterns
    )


# ==========================================================
# 5. UNIT SALE PRICE
# ==========================================================

def detect_unit_sale_price(text):

    patterns = [

        r"unit\s+sale\s+price",

        r"sale\s+price\s+per",

        r"price\s+per\s+kg",

        r"price\s+per\s+gram",

        r"price\s+per\s+litre",

        r"price\s+per\s+liter",

        r"₹\s*\d+(?:\.\d+)?\s*/\s*(?:kg|g|l|ml)"

    ]

    return matches_any(
        text,
        patterns
    )


# ==========================================================
# 6. CONSUMER CARE DETAILS
# ==========================================================

def detect_consumer_care(text):

    patterns = [

        r"consumer\s+care",

        r"consumer\s+helpline",

        r"consumer\s+complaint",

        r"customer\s+care",

        r"customer\s+helpline",

        r"customer\s+service",

        r"toll\s*free",

        r"helpline",

        r"contact\s+us",

        r"contact\s*:",

        r"care\s*:",

        r"call\s+us"

    ]

    return matches_any(
        text,
        patterns
    )


# ==========================================================
# 7. RELEVANT DATE DECLARATION
# ==========================================================

def detect_relevant_date(text):

    patterns = [

        r"manufacturing\s+date",

        r"manufacture\s+date",

        r"date\s+of\s+manufacture",

        r"mfg\s*\.?\s*date",

        r"mfg\s*:",

        r"packing\s+date",

        r"packed\s+date",

        r"date\s+of\s+packing",

        r"best\s+before",

        r"use\s+by",

        r"expiry",

        r"exp\s*date"

    ]

    return matches_any(
        text,
        patterns
    )


# ==========================================================
# 8. COUNTRY OF ORIGIN
# ==========================================================

def detect_country_of_origin(text):

    patterns = [

        r"country\s+of\s+origin",

        r"country\s+of\s+origin\s*:",

        r"made\s+in",

        r"product\s+of\s+india",

        r"origin\s*:",

        r"india"

    ]

    return matches_any(
        text,
        patterns
    )


# ==========================================================
# 9. BEST BEFORE / USE BY
# ==========================================================

def detect_best_before(text):

    patterns = [

        r"best\s+before",

        r"best\s+before\s+use",

        r"use\s+by",

        r"expiry",

        r"expires",

        r"exp\s*date",

        r"expiry\s+date"

    ]

    return matches_any(
        text,
        patterns
    )


# ==========================================================
# 10. DIMENSIONS
# ==========================================================

def detect_dimensions(text):

    patterns = [

        r"dimensions",

        r"dimension",

        r"length\s*[:\-]",

        r"width\s*[:\-]",

        r"height\s*[:\-]",

        r"\d+\s*[xX×]\s*\d+",

        r"\d+\s*cm\s*[xX×]\s*\d+",

        r"\d+\s*mm\s*[xX×]\s*\d+"

    ]

    return matches_any(
        text,
        patterns
    )


# ==========================================================
# DETECT ALL REQUIRED FIELDS
# ==========================================================

def detect_fields(text):

    clean_text = normalize_text(
        text
    )

    detected = {

        "Manufacturer / Packer / Importer":
            detect_manufacturer(clean_text),

        "Common / Generic Name":
            detect_common_name(clean_text),

        "Net Quantity":
            detect_net_quantity(clean_text),

        "MRP":
            detect_mrp(clean_text),

        "Unit Sale Price":
            detect_unit_sale_price(clean_text),

        "Consumer Care Details":
            detect_consumer_care(clean_text),

        "Relevant Date Declaration":
            detect_relevant_date(clean_text),

        "Country of Origin":
            detect_country_of_origin(clean_text),

        "Best Before / Use By":
            detect_best_before(clean_text),

        "Dimensions":
            detect_dimensions(clean_text)

    }

    return detected


# ==========================================================
# PACKAGED COMMODITY DETECTION
# ==========================================================

def is_packaged_commodity(text):

    clean_text = normalize_text(
        text
    )

    words = clean_text.split()

    # Very short OCR text is unlikely to be a product label
    if len(words) < 3:

        return False


    # ======================================================
    # STRONG PACKAGING INDICATORS
    # ======================================================

    packaging_patterns = [

        # Manufacturer / packaging
        r"manufactured\s+by",
        r"manufactured\s+at",
        r"manufactured\s+for",

        r"marketed\s+by",
        r"marketed\s+at",
        r"marketed\s+and\s+sold",

        r"packed\s+by",
        r"packed\s+at",

        r"imported\s+by",
        r"importer\s*:",

        # Product information
        r"ingredients?",
        r"ingredient\s*:",

        # Food licence / licence information
        r"fssai",
        r"fssai\s*(lic|license|no)",

        r"lic\s*\.?\s*no",
        r"licence\s*no",
        r"license\s*no",

        # Quantity
        r"net\s+(quantity|qty|weight|wt|volume)",

        # Price
        r"\bmrp\b",
        r"maximum\s+retail\s+price",

        # Dates
        r"manufacturing\s+date",
        r"date\s+of\s+manufacture",
        r"packing\s+date",

        r"best\s+before",
        r"use\s+by",

        # Consumer information
        r"consumer\s+care",
        r"consumer\s+helpline",

        r"customer\s+care",
        r"customer\s+helpline",

        # Origin
        r"country\s+of\s+origin",
        r"made\s+in",

        # Storage
        r"store\s+in",
        r"store\s+in\s+a\s+cool",
        r"storage\s+instructions"

    ]


    # ======================================================
    # COUNT PACKAGING INDICATORS
    # ======================================================

    packaging_count = 0

    for pattern in packaging_patterns:

        if re.search(
            pattern,
            clean_text,
            re.IGNORECASE
        ):

            packaging_count += 1


    # ======================================================
    # QUANTITY CHECK
    # ======================================================

    quantity_found = re.search(

        r"\b\d+(?:\.\d+)?\s*"
        r"(?:mg|g|kg|ml|l|cl|"
        r"milligram|gram|kilogram|"
        r"millilitre|milliliter|"
        r"litre|liter)\b",

        clean_text,

        re.IGNORECASE

    )


    # ======================================================
    # PRICE CHECK
    # ======================================================

    price_found = re.search(

        r"(?:₹|rs\.?|inr)\s*\.?\s*"
        r"\d+(?:\.\d{1,2})?",

        clean_text,

        re.IGNORECASE

    )


    # ======================================================
    # COMMON PACKAGED PRODUCT WORDS
    # ======================================================

    product_patterns = [

        r"\batta\b",
        r"\bflour\b",
        r"\brace\b",
        r"\bsugar\b",
        r"\bsalt\b",

        r"\bpulses?\b",
        r"\blentils?\b",
        r"\bspices?\b",

        r"\btea\b",
        r"\bcoffee\b",

        r"\bbiscuits?\b",
        r"\bcookies?\b",

        r"\bnoodles?\b",
        r"\bpasta\b",
        r"\bcereal\b",

        r"\bjuice\b",
        r"\bdrink\b",

        r"\boil\b",

        r"\bsoap\b",
        r"\bdetergent\b",
        r"\bshampoo\b",
        r"\btoothpaste\b",

        r"\bcream\b",
        r"\blotion\b",
        r"\bpowder\b",

        r"\bchips?\b",
        r"\bsnacks?\b"

    ]


    product_found = matches_any(

        clean_text,

        product_patterns

    )


    # ======================================================
    # FINAL DECISION
    # ======================================================

    # A strong packaging indicator is enough.
    #
    # Examples:
    # FSSAI
    # LIC NO
    # INGREDIENTS
    # MARKETED BY
    # PACKED BY
    # MRP
    # BEST BEFORE

    if packaging_count >= 1:

        return True


    # Product name + quantity

    if product_found and quantity_found:

        return True


    # Product name + price

    if product_found and price_found:

        return True


    # Quantity + price

    if quantity_found and price_found:

        return True


    return False