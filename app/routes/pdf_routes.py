from flask import Blueprint, make_response, request, jsonify
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO

from app import db
businesses_collection = db.businesses
pdf_routes_bp = Blueprint('pdf_routes_bp', __name__)

@pdf_routes_bp.route('/print_business_info', methods=['GET'])
def print_business_info():
    business_name = request.args.get('name')
    business_info = businesses_collection.find_one({"business_name": business_name})

    if business_info:
        # Generate PDF logic here
        pdf = create_business_pdf(business_info)  # Replace with your PDF generation logic
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename={}.pdf'.format(business_name)
        return response
    else:
        return jsonify({"error": "Business not found"}), 404

def create_business_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Initialize table data with headers
    table_data = []

    if isinstance(data, dict):
        address = data.get('address', {})
        formatted_address = ', '.join([str(address[key]) for key in address if address[key]])
    
        table_data.append(['Business ID', data.get('business_id', '')])
        table_data.append(['Business Name', data.get('business_name', '')])
        table_data.append(['Address', formatted_address])
        table_data.append(['Organization Type', data.get('organization_type', '')])
        table_data.append(['Resources Available', data.get('resources_available', '')])
        table_data.append(['Has Available Resources', 'Yes' if data.get('has_available_resources') else 'No'])
        table_data.append(['Contact Info', data.get('contact_info', '')])
    else:
        print("Invalid data format: Expected a dictionary")
        return None

    # Define column widths
    colWidths = [doc.width/3.0, doc.width/3.0 * 2]

    # Create the table with style
    table = Table(table_data, colWidths=colWidths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    # Build the PDF
    doc.build([table])
    pdf = buffer.getvalue()
    buffer.close()
    return pdf