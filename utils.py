import fitz  # PyMuPDF
import os
from PIL import Image
import io

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
