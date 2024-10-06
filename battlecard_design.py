import json
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.units import cm

# Premium design templates
TEMPLATES = {
    'modern': {
        'font': 'Helvetica-Bold',
        'font_size': 14,
        'header_color': colors.HexColor('#004080'),  # Dark Blue
        'section_bg_color': colors.HexColor('#E6F0FF'),  # Light Blue Background
        'section_text_color': colors.HexColor('#004080'),  # Dark Blue Text
        'text_color': colors.black,
        'highlight_color': colors.HexColor('#8B0000'),  # Gold for highlights
        'border_color': colors.HexColor('#004080'),  # Dark Blue Borders
        'accent_color': colors.HexColor('#FFD700'),  # Gold for accents
        'footer_color': colors.HexColor('#A9A9A9'),  # Dark Gray footer
    },
    'classic': {
        'font': 'Times-Bold',
        'font_size': 16,
        'header_color': colors.HexColor('#8B0000'),  # Dark Red
        'section_bg_color': colors.HexColor('#FFF8DC'),  # Light Beige Background
        'section_text_color': colors.HexColor('#8B0000'),  # Dark Red Text
        'text_color': colors.HexColor('#333333'),  # Dark Text
        'highlight_color': colors.HexColor('#8B0000'),  # Gold Highlight
        'border_color': colors.HexColor('#8B0000'),  # Dark Red Borders
        'accent_color': colors.HexColor('#FF6347'),  # Tomato for accents
        'footer_color': colors.HexColor('#FFE4C4'),  # Light Biscuit footer
    },
    'professional': {
        'font': 'Courier-Bold',
        'font_size': 12,
        'header_color': colors.HexColor('#333333'),  # Dark Gray
        'section_bg_color': colors.HexColor('#EDEDED'),  # Light Gray Background
        'section_text_color': colors.HexColor('#333333'),  # Dark Gray Text
        'text_color': colors.black,
        'highlight_color': colors.HexColor('#4682B4'),  # Steel Blue for highlights
        'border_color': colors.HexColor('#333333'),  # Dark Gray Borders
        'accent_color': colors.HexColor('#4682B4'),  # Steel Blue for accents
        'footer_color': colors.HexColor('#D3D3D3'),  # Light Gray footer
    }
}

# Function to fetch battlecard content
def fetch_battlecard_content(competitor):
    content = battlecards_data.get(competitor, "Content not found")
    return content

# Function to create structured premium PDFs using ReportLab
def create_battlecard_pdf(competitor, content, output_dir, template_name='classic'):
    template = TEMPLATES.get(template_name, TEMPLATES['classic'])
    
    pdf_path = os.path.join(output_dir, f"{competitor}_battlecard.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Title Style with Premium Highlight
    title_style = ParagraphStyle(
        name='TitleStyle', fontName=template['font'], fontSize=24, textColor=template['highlight_color'], alignment=TA_CENTER, spaceAfter=20,
        leading=30
    )
    
    # Section Header Style with Underline instead of Box
    section_style = ParagraphStyle(
        name='SectionStyle', fontName=template['font'], fontSize=16, textColor=template['section_text_color'], alignment=TA_LEFT, spaceAfter=10, spaceBefore=10,
        underline=True, underlineColor=template['section_text_color'], leading=20
    )
    
    # Body Text Style
    body_style = ParagraphStyle(
        name='BodyStyle', fontName='Helvetica', fontSize=12, textColor=template['text_color'], spaceAfter=8, alignment=TA_JUSTIFY, leading=14,
    )
    
    bullet_style = ParagraphStyle(
        name='BulletStyle', fontName='Helvetica', fontSize=12, textColor=template['text_color'], spaceAfter=8, leftIndent=20, bulletFontSize=12, leading=14
    )

    elements = []

    # Add Title with Premium Styling
    elements.append(Paragraph(f"Competitor Battlecard - {competitor}", title_style))
    elements.append(Spacer(1, 12))

    # Parse and split the content into sections
    sections = content.split("\n\n**")
    if sections[0].startswith("**"):
        sections[0] = sections[0][2:]

    # Add each section to the document
    for section in sections:
        if '**' in section:
            title, body = section.split('**', 1)
            title = title.strip()
            body = body.strip()

            # Remove unnecessary symbols like "**" and "*"
            body = body.replace('•*', '').replace('**', '').replace('*', '')

            # Section Header with Underline
            elements.append(Paragraph(title, section_style))

            # Split the body into lines for further processing
            body_lines = body.split("\n")

            # Handle Introductory Sentence (not part of the bullet list)
            if body_lines[0]:
                intro_line = body_lines.pop(0)
                if "Battlecard" not in intro_line:
                    elements.append(Paragraph(intro_line.strip(), body_style))

            # Handle actual bullet points with bold subheadings
            bullet_items = []
            for line in body_lines:
                if ":" in line:  # Look for subheading (e.g., "Market Share:")
                    subheading, description = line.split(":", 1)
                    bullet_items.append(ListItem(Paragraph(f"<b>{subheading}:</b> {description.strip()}", bullet_style)))
                else:
                    bullet_items.append(ListItem(Paragraph(line.strip(), bullet_style)))

            if bullet_items:
                bullet_list = ListFlowable(bullet_items, bulletType='bullet', bulletFontSize=10)
                elements.append(bullet_list)

            elements.append(Spacer(1, 12))

    # Add Footer with Logo and Light Accent
    footer_style = ParagraphStyle(
        name='FooterStyle', fontName='Helvetica', fontSize=10, textColor=template['footer_color'], alignment=TA_CENTER, spaceBefore=20
    )
    elements.append(Spacer(1, 24))
    elements.append(Paragraph("Generated by Battlecard AI System", footer_style))

    # Build the PDF
    doc.build(elements)

# Function to save content as a .txt file
def save_battlecard_txt(competitor, content, output_dir):
    txt_output_path = os.path.join(output_dir, f"{competitor}_battlecard.txt")
    try:
        with open(txt_output_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except IOError as e:
        print(f"Error writing to file {txt_output_path}: {e}")

# Main function to handle battlecard design
def design_battlecards(template_name='classic'):
    output_dir = 'battlecards'
    os.makedirs(output_dir, exist_ok=True)

    # Load battlecards data
    try:
        with open('battlecards.json', 'r', encoding='utf-8') as file:
            global battlecards_data
            battlecards_data = json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading battlecards data: {e}")
        return
    
    # Process each competitor and create PDFs and text files
    for competitor in battlecards_data:
        content = fetch_battlecard_content(competitor)
        create_battlecard_pdf(competitor, content, output_dir, template_name=template_name)
        save_battlecard_txt(competitor, content, output_dir)

if __name__ == "__main__":
    design_battlecards()