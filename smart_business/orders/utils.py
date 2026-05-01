from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generate_invoice_pdf(order):
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("INVOICE", styles['Title']))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"Customer: {order.customer.name}", styles['Normal']))
    elements.append(Paragraph(f"Product: {order.product.name}", styles['Normal']))
    elements.append(Paragraph(f"Quantity: {order.quantity}", styles['Normal']))
    elements.append(Paragraph(f"Total Price: ₹{order.total_price}", styles['Normal']))

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf