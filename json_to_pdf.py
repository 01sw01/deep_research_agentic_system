from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import json

def text_to_pdf(text, output_filename):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    paragraphs = text.split('\n\n')
    for item in paragraphs:
        para = Paragraph(f"{item}", styles['Normal'])
        story.append(para)
    #story.append(text)
    doc.build(story)
    
    


    
def json_to_pdf_reportlab(json_data, output_filename):
    # Create PDF document
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], 
                                fontSize=16, spaceAfter=30)
    
    def add_json_to_story(data, level=0):
        if isinstance(data, dict):
            for key, value in data.items():
                # Add key as heading
                heading = Paragraph(f"{'  ' * level}{key}", styles['Heading2'])
                story.append(heading)
                story.append(Spacer(1, 12))
                
                # Add value
                if isinstance(value, (dict, list)):
                    add_json_to_story(value, level + 1)
                else:
                    para = Paragraph(f"{'  ' * (level + 1)}{str(value)}", styles['Normal'])
                    story.append(para)
                    story.append(Spacer(1, 6))
                    
        elif isinstance(data, list):
            for i, item in enumerate(data):
                story.append(Paragraph(f"{'  ' * level}Item {i + 1}:", styles['Heading3']))
                add_json_to_story(item, level + 1)
    
    # Add title
    story.append(Paragraph("JSON Data Report", title_style))
    story.append(Spacer(1, 20))
    
    # Add JSON content
    add_json_to_story(json_data)
    
    # Build PDF
    doc.build(story)
