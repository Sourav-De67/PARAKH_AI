# ==========================================================
# PARAKH AI - COMPLIANCE ENGINE
# ==========================================================


# ==========================================================
# PRIMARY DECLARATIONS
# These are always checked
# ==========================================================

PRIMARY_FIELDS = [

    "Manufacturer / Packer / Importer",

    "Common / Generic Name",

    "Net Quantity",

    "MRP",

    "Unit Sale Price",

    "Consumer Care Details",

    "Relevant Date Declaration"

]


# ==========================================================
# CONDITIONAL DECLARATIONS
# These depend on the product / situation
# ==========================================================

CONDITIONAL_FIELDS = [

    "Country of Origin",

    "Best Before / Use By",

    "Dimensions"

]


# ==========================================================
# ALL FIELDS
# ==========================================================

ALL_FIELDS = PRIMARY_FIELDS + CONDITIONAL_FIELDS


# ==========================================================
# TEXT MATCHING HELPER
# ==========================================================

def contains_any(text, patterns):

    for pattern in patterns:

        if pattern in text:

            return True

    return False


# ==========================================================
# OCR FALLBACK CHECK
#
# Sometimes detector.py misses a field because OCR writes
# the text differently.
#
# Example:
# "MFD" instead of "Manufacturing Date"
# "MARKETED 8Y" instead of "MARKETED BY"
# ==========================================================

def ocr_detects_field(field, ocr_text):

    text = ocr_text.lower()


    # ======================================================
    # MANUFACTURER / PACKER / IMPORTER
    # ======================================================

    if field == "Manufacturer / Packer / Importer":

        patterns = [

            "manufactured by",
            "manufactured at",
            "manufactured for",

            "manufactured & marketed",
            "manufactured and marketed",

            "marketed by",
            "marketed at",
            "marketed",

            "packed by",
            "packed at",
            "packer",

            "imported by",
            "importer",

            "mfd by",
            "mfg by"

        ]

        return contains_any(text, patterns)


    # ======================================================
    # COMMON / GENERIC NAME
    # ======================================================

    if field == "Common / Generic Name":

        patterns = [

            "ingredients",
            "ingredient",

            "product name",
            "generic name",
            "common name",

            "biscuits",
            "biscuit",
            "chips",
            "snacks",
            "noodles",
            "pasta",
            "rice",
            "flour",
            "atta",
            "sugar",
            "salt",
            "tea",
            "coffee",
            "oil",
            "soap",
            "shampoo",
            "toothpaste"

        ]

        return contains_any(text, patterns)


    # ======================================================
    # NET QUANTITY
    # ======================================================

    if field == "Net Quantity":

        patterns = [

            "net quantity",
            "net qty",
            "net weight",
            "net wt",
            "net volume",

            "quantity:",

            "90 g",
            "100 g",
            "200 g",
            "250 g",
            "500 g",
            "1 kg",

            "50 ml",
            "100 ml",
            "200 ml",
            "500 ml",

            "1 l",
            "1 litre",
            "1 liter"

        ]

        return contains_any(text, patterns)


    # ======================================================
    # MRP
    # ======================================================

    if field == "MRP":

        patterns = [

            "mrp",
            "maximum retail price",
            "retail price"

        ]

        return contains_any(text, patterns)


    # ======================================================
    # UNIT SALE PRICE
    # ======================================================

    if field == "Unit Sale Price":

        patterns = [

            "unit sale price",
            "unit sale",
            "sale price per",
            "price per kg",
            "price per g",
            "price per gram",
            "price per litre",
            "price per liter"

        ]

        return contains_any(text, patterns)


    # ======================================================
    # CONSUMER CARE
    # ======================================================

    if field == "Consumer Care Details":

        patterns = [

            "consumer care",
            "consumer helpline",
            "consumer complaint",

            "customer care",
            "customer service",
            "customer helpline",

            "feedback",
            "complaint",
            "complaints",

            "contact us",
            "contact",

            "toll free",
            "helpline",

            "call us",
            "email:"

        ]

        return contains_any(text, patterns)


    # ======================================================
    # RELEVANT DATE DECLARATION
    # ======================================================

    if field == "Relevant Date Declaration":

        patterns = [

            "manufacturing date",
            "manufacture date",
            "date of manufacture",

            "mfg date",
            "mfg:",
            "mfd",

            "mfd:",
            "mfg",

            "packing date",
            "packed date",
            "date of packing",

            "best before",
            "use by",

            "expiry",
            "expiry date",
            "expires",

            "exp date"

        ]

        return contains_any(text, patterns)


    # ======================================================
    # COUNTRY OF ORIGIN
    # ======================================================

    if field == "Country of Origin":

        patterns = [

            "country of origin",
            "made in",
            "product of india",
            "origin:"

        ]

        return contains_any(text, patterns)


    # ======================================================
    # BEST BEFORE / USE BY
    # ======================================================

    if field == "Best Before / Use By":

        patterns = [

            "best before",
            "use by",
            "expiry",
            "expiry date",
            "expires",
            "exp date"

        ]

        return contains_any(text, patterns)


    # ======================================================
    # DIMENSIONS
    # ======================================================

    if field == "Dimensions":

        patterns = [

            "dimensions",
            "dimension",
            "length:",
            "width:",
            "height:"

        ]

        return contains_any(text, patterns)


    return False


# ==========================================================
# CHECK COMPLIANCE
# ==========================================================

def check_compliance(detected_fields, ocr_text=""):

    results = {}

    ocr_text = ocr_text.lower()


    # ======================================================
    # PRIMARY CHECKS
    # ======================================================

    primary_detected = 0


    for field in PRIMARY_FIELDS:

        # --------------------------------------------------
        # First trust detector.py
        # --------------------------------------------------

        detected = field in detected_fields


        # --------------------------------------------------
        # If detector missed it, use OCR fallback
        # --------------------------------------------------

        if not detected:

            detected = ocr_detects_field(
                field,
                ocr_text
            )


        # --------------------------------------------------
        # Store result
        # --------------------------------------------------

        if detected:

            results[field] = True

            primary_detected += 1

        else:

            results[field] = False


    # ======================================================
    # CONDITIONAL CHECK 1
    # COUNTRY OF ORIGIN
    # ======================================================

    imported_patterns = [

        "imported by",
        "importer",
        "imported",
        "country of origin"

    ]


    imported_product = contains_any(
        ocr_text,
        imported_patterns
    )


    if imported_product:

        country_detected = (

            "Country of Origin" in detected_fields

            or

            ocr_detects_field(
                "Country of Origin",
                ocr_text
            )

        )


        if country_detected:

            results["Country of Origin"] = True

        else:

            results["Country of Origin"] = False

    else:

        results["Country of Origin"] = None


    # ======================================================
    # CONDITIONAL CHECK 2
    # BEST BEFORE / USE BY
    # ======================================================

    best_before_detected = (

        "Best Before / Use By" in detected_fields

        or

        ocr_detects_field(
            "Best Before / Use By",
            ocr_text
        )

    )


    if best_before_detected:

        results["Best Before / Use By"] = True

    else:

        results["Best Before / Use By"] = None


    # ======================================================
    # CONDITIONAL CHECK 3
    # DIMENSIONS
    # ======================================================

    dimensions_detected = (

        "Dimensions" in detected_fields

        or

        ocr_detects_field(
            "Dimensions",
            ocr_text
        )

    )


    if dimensions_detected:

        results["Dimensions"] = True

    else:

        results["Dimensions"] = None


    # ======================================================
    # COMPLIANCE SCORE
    # ======================================================

    applicable_fields = 0

    detected_count = 0


    # ------------------------------------------------------
    # PRIMARY FIELDS
    # ------------------------------------------------------

    applicable_fields += len(
        PRIMARY_FIELDS
    )

    detected_count += primary_detected


    # ------------------------------------------------------
    # COUNTRY OF ORIGIN
    # ------------------------------------------------------

    if imported_product:

        applicable_fields += 1

        if results["Country of Origin"] is True:

            detected_count += 1


    # ------------------------------------------------------
    # BEST BEFORE / USE BY
    #
    # Not counted separately because it is already handled
    # through the relevant date declaration.
    # ------------------------------------------------------

    # No additional score.


    # ------------------------------------------------------
    # DIMENSIONS
    #
    # Not counted unless specifically applicable.
    # ------------------------------------------------------

    # No additional score.


    # ======================================================
    # CALCULATE PERCENTAGE
    # ======================================================

    if applicable_fields > 0:

        percentage = round(

            (
                detected_count
                /
                applicable_fields
            )
            * 100

        )

    else:

        percentage = 0


    # ======================================================
    # DETERMINE STATUS
    # ======================================================

    if primary_detected == len(
        PRIMARY_FIELDS
    ):

        # All primary declarations detected

        if (

            imported_product

            and

            not results["Country of Origin"]

        ):

            status = "Non-Compliant"

        else:

            status = "Compliant"


    else:

        # Some primary declarations are missing

        # --------------------------------------------------
        # Count packaging evidence
        # --------------------------------------------------

        packaging_keywords = [

            "mrp",

            "net",

            "quantity",

            "weight",

            "manufactured",

            "manufacturer",

            "marketed",

            "packed",

            "packer",

            "importer",

            "mfd",

            "mfg",

            "ingredients",

            "fssai",

            "consumer",

            "customer",

            "helpline",

            "complaint",

            "feedback",

            "unit sale",

            "best before",

            "use by",

            "country of origin",

            "made in"

        ]


        evidence_count = 0


        for keyword in packaging_keywords:

            if keyword in ocr_text:

                evidence_count += 1


        if evidence_count < 3:

            status = "Verification Required"

        else:

            status = "Non-Compliant"


    # ======================================================
    # RETURN RESULTS
    # ======================================================

    return (

        results,

        status,

        percentage

    )