from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def generate_pdf_report(
    score,
    matching_terms,
    missing_terms,
    resume_skills,
    job_skills,
    missing_skills,
    skill_coverage,
    detected_sections,
    all_sections,
    suggestions
):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=20
    )

    heading_style = styles["Heading2"]

    normal_style = styles["BodyText"]

    story = []

    # Title
    story.append(
        Paragraph("AI Resume Analysis Report", title_style)
    )

    story.append(Spacer(1, 15))

    # Resume Match
    story.append(
        Paragraph("1. Resume Match Analysis", heading_style)
    )

    match_data = [
        ["Metric", "Result"],
        ["Resume Match", f"{score}%"],
        ["Skill Coverage", f"{skill_coverage:.1f}%"]
    ]

    match_table = Table(
        match_data,
        colWidths=[8 * cm, 8 * cm]
    )

    match_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    story.append(match_table)

    story.append(Spacer(1, 15))

    # Keywords
    story.append(
        Paragraph("2. Keyword Analysis", heading_style)
    )

    story.append(
        Paragraph(
            "<b>Matching Keywords:</b> "
            + escape(", ".join(matching_terms) or "None"),
            normal_style
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            "<b>Potentially Missing Keywords:</b> "
            + escape(", ".join(missing_terms) or "None"),
            normal_style
        )
    )

    story.append(Spacer(1, 15))

    # Skills
    story.append(
        Paragraph("3. Skill Analysis", heading_style)
    )

    for category, skills in resume_skills.items():

        if skills:

            story.append(
                Paragraph(
                    f"<b>{escape(category)}:</b> "
                    + escape(", ".join(skills)),
                    normal_style
                )
            )

            story.append(Spacer(1, 5))

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "<b>Required Job Skills:</b> "
            + escape(
                ", ".join(
                    skill
                    for skills in job_skills.values()
                    for skill in skills
                ) or "None detected"
            ),
            normal_style
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            "<b>Missing Skills:</b> "
            + escape(", ".join(missing_skills) or "None"),
            normal_style
        )
    )

    story.append(Spacer(1, 15))

    # Resume Structure
    story.append(
        Paragraph("4. Resume Structure Analysis", heading_style)
    )

    for section in all_sections:

        status = (
            "Detected"
            if section in detected_sections
            else "Missing"
        )

        story.append(
            Paragraph(
                f"<b>{escape(section)}:</b> {status}",
                normal_style
            )
        )

        story.append(Spacer(1, 5))

    story.append(Spacer(1, 15))

    # Suggestions
    story.append(
        Paragraph("5. Improvement Suggestions", heading_style)
    )

    for index, suggestion in enumerate(suggestions, start=1):

        story.append(
            Paragraph(
                f"{index}. {escape(suggestion)}",
                normal_style
            )
        )

        story.append(Spacer(1, 8))

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>Disclaimer:</b> This report uses text similarity "
            "and rule-based analysis. The match percentage is not "
            "an official ATS score or a prediction of hiring success.",
            normal_style
        )
    )

    # Generate PDF
    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()