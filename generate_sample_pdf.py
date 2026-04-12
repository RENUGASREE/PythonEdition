import os
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from datetime import datetime

def generate_sample_pdf():
    # Sample data
    full_name = "RENUGA SREE"
    module_title = "Python Fundamentals"
    issued_date = datetime.now()
    cert_id = f"PY-CERT-PREVIEW-{issued_date.strftime('%Y%m%d')}-001"
    
    # Output path
    output_path = os.path.join(os.getcwd(), "sample_certificate.pdf")
    
    # Set up PDF canvas
    p = canvas.Canvas(output_path, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Define colors
    dark_blue = colors.Color(26/255, 43/255, 75/255)
    gold = colors.Color(197/255, 160/255, 89/255)
    light_gray = colors.Color(248/255, 249/255, 250/255)

    # Background
    p.setFillColor(light_gray)
    p.rect(0, 0, width, height, fill=1)

    # Main Borders
    p.setStrokeColor(dark_blue)
    p.setLineWidth(12)
    p.rect(20, 20, width - 40, height - 40)
    
    p.setStrokeColor(gold)
    p.setLineWidth(2)
    p.rect(32, 32, width - 64, height - 64)

    # Header: Python Edition
    p.setFillColor(dark_blue)
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2.0, height - 80, "Python Edition")

    # AI Badge (Top Right)
    badge_x = width - 150
    badge_y = height - 100
    p.setFillColor(dark_blue)
    p.rect(badge_x, badge_y, 100, 40, fill=1)
    p.setStrokeColor(gold)
    p.setLineWidth(2)
    p.line(badge_x, badge_y, badge_x + 100, badge_y)
    
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 8)
    p.drawCentredString(badge_x + 50, badge_y + 25, "AI VERIFIED LEARNING")
    p.setFillColor(gold)
    p.setFont("Helvetica-Bold", 7)
    p.drawCentredString(badge_x + 50, badge_y + 10, "SKILL LEVEL: PRO")

    # Title: CERTIFICATE OF ACHIEVEMENT
    p.setFillColor(dark_blue)
    p.setFont("Helvetica-Bold", 36)
    p.drawCentredString(width / 2.0, height - 180, "CERTIFICATE OF ACHIEVEMENT")

    # Presentee text
    p.setFillColor(colors.gray)
    p.setFont("Times-Italic", 16)
    p.drawCentredString(width / 2.0, height - 220, "This certification is proudly presented to")

    # Student Name
    p.setFillColor(gold)
    p.setFont("Times-Bold", 48)
    p.drawCentredString(width / 2.0, height - 300, full_name.upper())
    
    # Underline for name
    p.setStrokeColor(gold)
    p.setLineWidth(2)
    p.line(width/2 - 200, height - 310, width/2 + 200, height - 310)

    # Description
    p.setFillColor(colors.gray)
    p.setFont("Times-Roman", 14)
    p.drawCentredString(width / 2.0, height - 360, "For successfully mastering the high-fidelity curriculum of")

    # Module Title
    p.setFillColor(dark_blue)
    p.setFont("Helvetica-Bold", 28)
    p.drawCentredString(width / 2.0, height - 410, module_title)

    # Footer Left: Signature
    p.setFillColor(dark_blue)
    p.setFont("Times-Italic", 20)
    p.drawString(80, 120, "Pythonized AI")
    p.setLineWidth(1)
    p.line(80, 115, 230, 115)
    p.setFont("Helvetica-Bold", 8)
    p.drawString(80, 100, "PLATFORM DIRECTOR, PYTHON EDITION")
    p.setFont("Helvetica", 8)
    p.setFillColor(colors.gray)
    p.drawString(80, 85, f"Issued on: {issued_date.strftime('%B %d, %Y')}")

    # Footer Center: QR Code and ID
    # Create QR Code
    qr_code = qr.QrCodeWidget(f"https://python-edition.app/verify/{cert_id}")
    qr_drawing = Drawing(80, 80)
    qr_drawing.add(qr_code)
    
    # Draw the QR code
    qr_x, qr_y = width / 2.0 - 40, 80
    renderPDF.draw(qr_drawing, p, qr_x, qr_y)

    p.setFillColor(colors.gray)
    p.setFont("Helvetica", 6)
    p.drawCentredString(width / 2.0, 75, "Scan to Verify Certificate")
    p.drawCentredString(width / 2.0, 65, f"ID: {cert_id}")
    p.setFont("Times-Italic", 8)
    p.drawCentredString(width / 2.0, 50, "Python Edition Adaptive Learning Platform")

    # Footer Right: Verified Seal
    seal_x = width - 180
    seal_y = 60
    center_x = seal_x + 50
    center_y = seal_y + 50
    
    # Outer Circle
    p.setStrokeColor(gold)
    p.setLineWidth(1)
    p.circle(center_x, center_y, 52, fill=0)

    # Seal Inner Circle
    p.setFillColor(dark_blue)
    p.circle(center_x, center_y, 36, fill=1)
    p.setStrokeColor(gold)
    p.setLineWidth(3)
    p.circle(center_x, center_y, 36, fill=0)
    
    # "VERIFIED" text
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(center_x, center_y - 5, "VERIFIED")
    
    # Circular Text around seal
    seal_text = "AUTHENTIC • CERTIFIED • PYTHON EDITION • "
    p.setFillColor(gold)
    p.setFont("Helvetica-Bold", 6)
    
    radius = 44
    chars = list(seal_text)
    angle_step = 360 / len(chars)
    
    for i, char in enumerate(chars):
        angle = 90 - (i * angle_step)  # Start from top (90 degrees)
        p.saveState()
        # Move to center, rotate, move to radius
        import math
        p.translate(center_x, center_y)
        p.rotate(angle)
        p.drawString(0, radius, char)
        p.restoreState()

    p.showPage()
    p.save()
    print(f"Sample certificate generated successfully: {output_path}")

if __name__ == "__main__":
    generate_sample_pdf()
