import os
from config import Config
from utils.resume_generator import generate_resume_html
import pdfkit

def export_to_pdf(resume_data, experience_level, filename):
    """Export resume to PDF format using pdfkit"""
    
    # Generate HTML content
    html_content = generate_resume_html(resume_data, experience_level)
    
    # Create exports directory if not exists
    os.makedirs(Config.EXPORT_DIR, exist_ok=True)
    
    # Save PDF
    pdf_path = os.path.join(Config.EXPORT_DIR, f"{filename}.pdf")
    
    # PDFKit configuration
    # Windows path
    config_windows = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    # Mac/Linux path
    config_unix = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    
    # Try both configurations
    try:
        config = config_windows
        options = {
            'page-size': 'A4',
            'margin-top': '10mm',
            'margin-right': '10mm',
            'margin-bottom': '10mm',
            'margin-left': '10mm',
            'encoding': 'UTF-8',
            'no-outline': None,
            'enable-local-file-access': None
        }
        pdfkit.from_string(html_content, pdf_path, options=options, configuration=config)
    except Exception:
        try:
            config = config_unix
            options = {
                'page-size': 'A4',
                'margin-top': '10mm',
                'margin-right': '10mm',
                'margin-bottom': '10mm',
                'margin-left': '10mm',
                'encoding': 'UTF-8',
                'no-outline': None,
                'enable-local-file-access': None
            }
            pdfkit.from_string(html_content, pdf_path, options=options, configuration=config)
        except Exception as e:
            raise Exception(f"Failed to generate PDF. Make sure wkhtmltopdf is installed. Error: {str(e)}")
    
    return pdf_path
