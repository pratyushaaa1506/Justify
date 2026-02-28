import os
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime

def generate_pdf(summary_data: dict) -> str:
    # Ensure generated/ directory exists
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'generated')
    os.makedirs(output_dir, exist_ok=True)

    # Create a unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"JusticeLens_Report_{timestamp}.pdf"
    file_path = os.path.join(output_dir, filename)

    # Start PDF generation
    c = canvas.Canvas(file_path, pagesize=LETTER)
    width, height = LETTER
    y = height - inch

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(inch, y, "JusticeLens Legal Report")
    y -= 0.5 * inch

    # Issue description
    c.setFont("Helvetica", 12)
    c.drawString(inch, y, f"Issue: {summary_data.get('issue', '')}")
    y -= 0.3 * inch

    # Legal category
    c.drawString(inch, y, f"Category: {summary_data.get('category', '')}")
    y -= 0.3 * inch

    # Applicable laws
    c.setFont("Helvetica-Bold", 12)
    c.drawString(inch, y, "Applicable Laws:")
    y -= 0.3 * inch
    c.setFont("Helvetica", 12)
    for law in summary_data.get('applicable_laws', []):
        c.drawString(inch + 0.2 * inch, y, f"• {law}")
        y -= 0.25 * inch
        if y < inch:
            c.showPage()
            y = height - inch
            c.setFont("Helvetica", 12)

    # Guidance / next steps
    y -= 0.1 * inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(inch, y, "Guidance / Next Steps:")
    y -= 0.3 * inch
    c.setFont("Helvetica", 12)
    guidance = summary_data.get('guidance', '')
    for line in guidance.split('\n'):
        c.drawString(inch, y, line)
        y -= 0.25 * inch
        if y < inch:
            c.showPage()
            y = height - inch
            c.setFont("Helvetica", 12)

    c.save()
    return file_path
