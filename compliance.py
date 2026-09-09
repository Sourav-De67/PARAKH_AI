REQUIRED_FIELDS = [
    "Common / Generic Name",
    "Net Quantity",
    "MRP",
    "Manufacturer",
    "Manufacturing Date",
    "Consumer Care"
]


def check_compliance(detected_fields):

    results = {}

    for field in REQUIRED_FIELDS:

        if field in detected_fields:
            results[field] = True
        else:
            results[field] = False


    # =====================================
    # CHECK STATUS
    # =====================================

    # Common / Generic Name needs manual
    # verification because OCR may not
    # reliably identify it.

    if "Common / Generic Name" not in detected_fields:

        status = "Verification Required"

    else:

        missing_fields = [
            field
            for field in REQUIRED_FIELDS
            if field not in detected_fields
        ]

        if len(missing_fields) == 0:
            status = "Compliant"
        else:
            status = "Non-Compliant"


    return results, status


# =====================================
# TEST
# =====================================

if __name__ == "__main__":

    detected_fields = [
        "Net Quantity",
        "MRP",
        "Manufacturer",
        "Manufacturing Date",
        "Consumer Care"
    ]

    results, status = check_compliance(
        detected_fields
    )

    print("Compliance Results:")
    print(results)

    print("Status:", status)