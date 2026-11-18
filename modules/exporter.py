"""Markdown compilation and ATS-friendly DOCX export."""
from io import BytesIO
import re


def markdown_to_docx(markdown_text: str) -> BytesIO:
    from docx import Document
    from docx.shared import Inches, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    document = Document()
    section = document.sections[0]
    section.top_margin = Inches(0.55)
    section.bottom_margin = Inches(0.55)
    section.left_margin = Inches(0.65)
    section.right_margin = Inches(0.65)

    styles = document.styles
    normal = styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(10)

    for line in markdown_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("###"):
            p = document.add_paragraph()
            r = p.add_run(re.sub(r"^#+\s*", "", line))
            r.bold = True
            r.font.size = Pt(10)
        elif line.startswith("##"):
            p = document.add_paragraph()
            r = p.add_run(re.sub(r"^#+\s*", "", line).upper())
            r.bold = True
            r.font.size = Pt(11)
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(3)
        elif line.startswith("#"):
            p = document.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(re.sub(r"^#+\s*", "", line))
            r.bold = True
            r.font.size = Pt(16)
            p.paragraph_format.space_after = Pt(5)
        else:
            is_bullet = line.startswith(("- ", "* "))
            clean = re.sub(r"^[-*]\s+", "", line)
            clean = re.sub(r"[*_]{1,2}([^*_]+)[*_]{1,2}", r"\1", clean)
            p = document.add_paragraph(style="List Bullet" if is_bullet else None)
            p.paragraph_format.left_indent = Inches(0.18) if is_bullet else Inches(0)
            p.paragraph_format.first_line_indent = Inches(-0.12) if is_bullet else Inches(0)
            p.paragraph_format.space_after = Pt(2)
            p.add_run(clean)

    output = BytesIO()
    document.save(output)
    output.seek(0)
    return output
