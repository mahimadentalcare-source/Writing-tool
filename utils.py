import fitz  # PyMuPDF
import os
from PIL import Image
import io
import re

def extract_text_and_images(pdf_paths, output_dir):
    """
    Extracts text and images from a list of PDF files.
    """
    full_text = ""
    images = []

    for pdf_path in pdf_paths:
        try:
            doc = fitz.open(pdf_path)
            
            # Extract Text
            for page_num, page in enumerate(doc):
                full_text += page.get_text() + "\n"
                
                # Extract Images
                image_list = page.get_images(full=True)
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    image_filename = f"{os.path.basename(pdf_path)}_p{page_num}_i{img_index}.{image_ext}"
                    image_filepath = os.path.join(output_dir, image_filename)
                    
                    with open(image_filepath, "wb") as img_file:
                        img_file.write(image_bytes)
                    
                    # Verify if it's a valid image and large enough to be useful (skip icons/lines)
                    try:
                        with Image.open(image_filepath) as pil_img:
                            width, height = pil_img.size
                            if width > 100 and height > 100:  # Simple filter for small icons
                                images.append({
                                    "path": image_filepath,
                                    "page": page_num,
                                    "source": os.path.basename(pdf_path)
                                })
                    except:
                        pass # Skip invalid images

            doc.close()
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")

    return {"text": full_text, "images": images}

def add_markdown_table_to_docx(doc, table_text):
    """
    Parses a Markdown table and adds it to the python-docx Document.
    """
    # Simple parser for standard markdown tables
    lines = df_lines = table_text.strip().split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    
    if len(lines) < 2: return # Not enough content
    
    # Extract headers
    # Assumes format: | Col 1 | Col 2 | ...
    headers = [c.strip() for c in lines[0].strip('|').split('|')]
    
    # Check if second line is separator
    start_row = 1
    if '---' in lines[1]:
        start_row = 2
        
    # Create Table
    try:
        table = doc.add_table(rows=1, cols=len(headers))
        table.style = 'Table Grid'
        
        # Populate Header
        hdr_cells = table.rows[0].cells
        for i, header in enumerate(headers):
            if i < len(hdr_cells):
                hdr_cells[i].text = header
                # Bold Header
                for paragraph in hdr_cells[i].paragraphs:
                    for run in paragraph.runs:
                        run.font.bold = True
        
        # Populate Rows
        for line in lines[start_row:]:
            if not line.strip('|'): continue
            
            row_cells = table.add_row().cells
            cells = [c.strip() for c in line.strip('|').split('|')]
            
            for i, cell in enumerate(cells):
                if i < len(row_cells):
                    row_cells[i].text = cell
                    
    except Exception as e:
        doc.add_paragraph(f"[Error rendering table: {e}]")
        doc.add_paragraph(table_text) # Fallback to text

def add_markdown_content(doc, text):
    """
    Parses markdown text (headings, bullets, bold) and adds to docx.
    """
    lines = text.splitlines()
    for line in lines:
        stripped = line.strip()
        if not stripped: continue
        
        # Headings
        if stripped.startswith('#'):
            # Count hashes
            hashes = len(stripped.split(' ')[0])
            content = stripped.lstrip('#').strip()
            # Clean ** from headings if present
            content = content.replace('**', '') 
            try:
                doc.add_heading(content, level=min(hashes, 3))
            except:
                doc.add_heading(content, level=1)
            continue
            
        # Bullets
        style = None # Default style
        if stripped.startswith('* ') or stripped.startswith('- '):
            style = 'List Bullet'
            stripped = stripped[2:] # Remove '* '
        
        p = doc.add_paragraph(style=style)
        
        # Parse Bold: **text**
        # Split by **
        parts = re.split(r'(\*\*.*?\*\*)', stripped)
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                run = p.add_run(part[2:-2])
                run.bold = True
            else:
                p.add_run(part)
