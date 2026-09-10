from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
import os


# ==========================================================
# GENERATE PDF REPORT
# ==========================================================

def generate_report(
    output_path,
    status,
    percentage,
    results,
    ocr_text="",
    image_path=None
):

    # ------------------------------------------------------
    # PDF DOCUMENT
    # ------------------------------------------------------

    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )


    # ------------------------------------------------------
    # STYLES
    # ------------------------------------------------------

    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=15
    )


    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8
    )


    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14
    )


    # ------------------------------------------------------
    # CONTENT
    # ------------------------------------------------------

    content = []


    # ------------------------------------------------------
    # TITLE
    # ------------------------------------------------------

    content.append(
        Paragraph(
            "PARAKH AI",
            title_style
        )
    )


    content.append(
        Paragraph(
            "Packaged Commodity Compliance Report",
            normal_style
        )
    )


    content.append(
        Spacer(
            1,
            15
        )
    )


    # ------------------------------------------------------
    # PRODUCT IMAGE
    # ------------------------------------------------------

    if image_path and os.path.exists(image_path):

        try:

            product_image = Image(
                image_path,
                width=3.5 * inch,
                height=3.5 * inch
            )

            content.append(
                product_image
            )

            content.append(
                Spacer(
                    1,
                    15
                )
            )

        except Exception:

            pass


    # ------------------------------------------------------
    # OVERALL RESULT
    # ------------------------------------------------------

    content.append(
        Paragraph(
            "Overall Result",
            heading_style
        )
    )


    summary_data = [

        ["Status", status],

        ["Compliance Score", f"{percentage}%"]

    ]


    summary_table = Table(
        summary_data,
        colWidths=[180, 280]
    )


    summary_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.lightgrey
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "Helvetica"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                10
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            )

        ])
    )


    content.append(
        summary_table
    )


    # ------------------------------------------------------
    # DECLARATION CHECK
    # ------------------------------------------------------

    content.append(
        Paragraph(
            "Declaration Check",
            heading_style
        )
    )


    table_data = [

        [
            "Declaration",
            "Result"
        ]

    ]


    for field, value in results.items():

        if value is True:

            result_text = "Detected"

        elif value is False:

            result_text = "Missing"

        else:

            result_text = "Not Applicable"


        table_data.append(

            [
                field,
                result_text
            ]

        )


    declaration_table = Table(
        table_data,
        colWidths=[360, 100],
        repeatRows=1
    )


    declaration_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.black
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "FONTNAME",
                (0, 1),
                (-1, -1),
                "Helvetica"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )

        ])
    )


    content.append(
        declaration_table
    )


    # ------------------------------------------------------
    # DISCLAIMER
    # ------------------------------------------------------

    content.append(
        Spacer(
            1,
            20
        )
    )


    content.append(
        Paragraph(
            "This report is generated by PARAKH AI "
            "based on OCR and automated declaration detection. "
            "It should be used as an assistance tool and may "
            "require verification by an authorized officer.",
            normal_style
        )
    )


    # ------------------------------------------------------
    # BUILD PDF
    # ------------------------------------------------------

    document.build(
        content
    )