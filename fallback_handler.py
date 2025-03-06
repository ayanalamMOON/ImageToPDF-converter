import os
import json
import time
import hashlib
import logging
from datetime import datetime
import tempfile
from functools import wraps

import requests
from PIL import Image
from fpdf import FPDF

# CloudConvert API key (replace with your actual key)
CLOUDCONVERT_API_KEY = "your_cloudconvert_api_key"

# Configure logging
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(
        LOG_DIR, f'converter_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    ),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Add new global constants
HISTORY_FILE = "conversion_history.json"
CONVERSION_CACHE = ".conversion_cache"

# Add new constants for PDF settings
PAGE_SIZES = {
    'A4': (210, 297),
    'Letter': (216, 279),
    'Legal': (216, 356),
    'Custom': None
}

def get_file_hash(filepath):
    """Generate hash of file content for change detection."""
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def load_conversion_history():
    """Load conversion history from JSON file."""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"Error loading conversion history: {e}")
    return {}

def save_conversion_history(history):
    """Save conversion history to JSON file."""
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        logging.error(f"Error saving conversion history: {e}")

def scan_directory(directory, supported_formats, min_date=None):
    """Recursively scan directory for supported files."""
    files_info = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(supported_formats):
                file_path = os.path.join(root, file)
                mod_time = os.path.getmtime(file_path)
                if min_date is None or mod_time >= min_date:
                    files_info.append({
                        'path': file_path,
                        'modified': mod_time,
                        'hash': get_file_hash(file_path)
                    })
    return files_info

def retry_on_failure(max_retries=3, delay=1):
    """Decorator to retry failed operations."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logging.warning(
                        f"Attempt {attempt + 1} failed: {str(e)}"
                    )
                    time.sleep(delay * (attempt + 1))
            logging.error(
                f"All {max_retries} attempts failed: {str(last_exception)}"
            )
            raise last_exception
        return wrapper
    return decorator

@retry_on_failure(max_retries=3)
def convert_heic_to_jpeg_with_cloudconvert(input_path, output_path):
    """Convert a HEIC file to JPEG using CloudConvert API with retry."""
    logging.info(f"Starting CloudConvert conversion for {input_path}")
    try:
        url = "https://api.cloudconvert.com/v2/jobs"
        headers = {
            "Authorization": f"Bearer {CLOUDCONVERT_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "tasks": {
                "import-my-file": {"operation": "import/upload"},
                "convert-my-file": {
                    "operation": "convert",
                    "input": "import-my-file",
                    "output_format": "jpg"
                },
                "export-my-file": {
                    "operation": "export/url",
                    "input": "convert-my-file"
                }
            }
        }

        # Create a conversion job
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        job = response.json()

        # Upload the HEIC file
        upload_url = job["data"]["tasks"]["import-my-file"]["result"]["form"]["url"]
        with open(input_path, "rb") as file:
            upload_response = requests.post(upload_url, files={"file": file})
        upload_response.raise_for_status()

        # Wait for conversion and download the result
        job_id = job["data"]["id"]
        result_url = f"https://api.cloudconvert.com/v2/jobs/{job_id}"
        while True:
            result_response = requests.get(result_url, headers=headers)
            result_response.raise_for_status()
            result_data = result_response.json()
            status = result_data["data"]["status"]
            if status == "finished":
                files = result_data["data"]["tasks"]["export-my-file"]["result"]["files"]
                download_url = files[0]["url"]
                download_response = requests.get(download_url)
                with open(output_path, "wb") as f:
                    f.write(download_response.content)
                break
            elif status in {"error", "failed"}:
                raise RuntimeError("CloudConvert job failed.")
            time.sleep(2)
    except Exception as e:
        raise RuntimeError(f"CloudConvert API error: {e}")

def check_image_issues(image_path):
    """Check for potential issues in the image."""
    issues = []
    try:
        with Image.open(image_path) as img:
            # Check resolution
            if any(dim > 5000 for dim in img.size):
                issues.append("High resolution might cause memory issues")
            elif any(dim < 100 for dim in img.size):
                issues.append("Low resolution might affect quality")
            
            # Check color mode
            if img.mode not in ['RGB', 'RGBA']:
                issues.append(f"Unusual color mode: {img.mode}")
            
            # Check file size
            file_size = os.path.getsize(image_path) / (1024 * 1024)  # MB
            if file_size > 10:
                issues.append(f"Large file size: {file_size:.1f}MB")
    except Exception as e:
        issues.append(f"Error analyzing image: {str(e)}")
    return issues

class CustomPDF(FPDF):
    """Extended FPDF class with watermark and page numbers."""
    def __init__(
        self, orientation='P', unit='mm', format='A4',
        watermark_text=None, font=None, background_color=None
    ):
        super().__init__(orientation=orientation, unit=unit, format=format)
        self.watermark_text = watermark_text
        self.font = font
        self.background_color = background_color

    def header(self):
        if self.watermark_text:
            self.set_font('Arial', 'I', 30)
            self.set_text_color(200, 200, 200)  # Light gray
            self.rotate(45)
            self.text(40, 80, self.watermark_text)
            self.rotate(0)

    def footer(self):
        if self.page_numbers:
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_page(self, orientation='', size='', rotation=0):
        super().add_page(orientation, size, rotation)
        if self.background_color:
            self.set_fill_color(*self.background_color)
            self.rect(0, 0, self.w, self.h, 'F')
        if self.font:
            self.set_font(self.font)

def merge_pdfs(pdf_files, output_path):
    """Merge multiple PDF files into one."""
    from PyPDF2 import PdfMerger
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()

def heic_to_pdf_with_fallback(input_folder, output_pdf, compression_quality, supported_formats, 
                            progress_bar, status_label, pdf_options=None, recursive=True, min_date=None, 
                            skip_converted=True, delete_source=False):
    """Enhanced conversion function with new features."""
    conversion_issues = {}
    try:
        # Load conversion history
        history = load_conversion_history()
        
        # Scan for files
        files_info = scan_directory(input_folder, supported_formats, min_date)
        if not files_info:
            messagebox.showwarning("No Files", "No matching files found!")
            return

        # Filter already converted files
        if skip_converted:
            files_info = [f for f in files_info 
                        if f['hash'] not in history or 
                        history[f['hash']]['timestamp'] < f['modified']] 

        if not files_info:
            messagebox.showinfo("Info", "All files are up to date!")
            return

        # Sort files by modification date
        files_info.sort(key=lambda x: x['modified'])

        # Pre-scan for potential issues
        for file_info in files_info:
            file_path = file_info['path']
            issues = check_image_issues(file_path)
            if issues:
                conversion_issues[file_info['path']] = issues
                logging.warning(f"Issues detected in {file_info['path']}: {issues}")

        # Show preview of issues if any
        if conversion_issues:
            issues_text = "\n".join(
                f"{fname}: {', '.join(issues)}"
                for fname, issues in conversion_issues.items()
            )
            if not messagebox.askyesno("Potential Issues", 
                f"The following issues were detected:\n\n{issues_text}\n\nContinue anyway?"):
                return

        images = []
        progress_bar["maximum"] = len(files_info)
        progress_bar["value"] = 0

        for i, file_info in enumerate(files_info):
            file_path = file_info['path']
            output_image_path = os.path.join(input_folder, f"converted_{os.path.splitext(os.path.basename(file_path))[0]}.jpg")

            # Handle HEIC files
            if file_path.lower().endswith(".heic"):
                try:
                    # Attempt to convert HEIC locally
                    import pyheif
                    heif_file = pyheif.read(file_path)
                    image = Image.frombytes(
                        heif_file.mode, heif_file.size, heif_file.data,
                        "raw", heif_file.mode, heif_file.stride
                    )
                    if image.mode != "RGB":
                        image = image.convert("RGB")
                    image.save(output_image_path, "JPEG", quality=compression_quality)
                except ImportError:
                    # Fallback to CloudConvert
                    status_label.config(text=f"Falling back to CloudConvert for {os.path.basename(file_path)}")
                    convert_heic_to_jpeg_with_cloudconvert(file_path, output_image_path)
            else:
                # Handle JPEG, PNG, BMP, and GIF directly
                image = Image.open(file_path)
                if image.mode != "RGB":
                    image = image.convert("RGB")
                image.save(output_image_path, "JPEG", quality=compression_quality)

            images.append(Image.open(output_image_path))
            progress_bar["value"] += 1
            status_label.config(text=f"Processed: {os.path.basename(file_path)} ({i + 1}/{len(files_info)})")
            progress_bar.update_idletasks()

        # Create PDF with custom options
        pdf_options = pdf_options or {}
        orientation = pdf_options.get('orientation', 'P')
        page_size = pdf_options.get('page_size', 'A4')
        custom_size = pdf_options.get('custom_size', None)
        watermark = pdf_options.get('watermark', None)
        page_numbers = pdf_options.get('page_numbers', False)
        font = pdf_options.get('font', None)
        background_color = pdf_options.get('background_color', None)
        
        if page_size == 'Custom' and custom_size:
            pdf = CustomPDF(orientation=orientation, format=custom_size, watermark_text=watermark, font=font, background_color=background_color)
        else:
            pdf = CustomPDF(orientation=orientation, format=page_size, watermark_text=watermark, font=font, background_color=background_color)
        
        pdf.page_numbers = page_numbers
        
        # Process images
        for img in images:
            pdf.add_page()
            
            # Calculate image placement
            if orientation == 'P':
                max_w = pdf.w - 20
                max_h = pdf.h - 30
            else:
                max_w = pdf.w - 30
                max_h = pdf.h - 20
                
            # Scale image
            img_w, img_h = img.size
            ratio = min(max_w/img_w, max_h/img_h)
            new_w = img_w * ratio
            new_h = img_h * ratio
            
            # Center image
            x = (pdf.w - new_w) / 2
            y = (pdf.h - new_h) / 2
            
            temp_image_path = "temp_image.jpg"
            img.save(temp_image_path, "JPEG", quality=compression_quality)
            pdf.image(temp_image_path, x, y, new_w, new_h)
            os.remove(temp_image_path)

        pdf.output(output_pdf)
        
        # Handle PDF merging if requested
        if pdf_options.get('merge_files'):
            merge_files = pdf_options['merge_files']
            if merge_files:
                temp_output = output_pdf
                final_output = os.path.splitext(output_pdf)[0] + "_merged.pdf"
                merge_pdfs([temp_output] + merge_files, final_output)
                os.remove(temp_output)  # Remove temporary PDF
                output_pdf = final_output

        messagebox.showinfo("Success", f"PDF created successfully: {output_pdf}")
        logging.info(f"Successfully created PDF: {output_pdf}")

        # Update conversion history
        for file_info in files_info:
            history[file_info['hash']] = {
                'path': file_info['path'],
                'timestamp': datetime.now().timestamp(),
                'output': output_pdf
            }
        
        # Delete source files if requested
        if delete_source:
            for file_info in files_info:
                try:
                    os.remove(file_info['path'])
                    logging.info(f"Deleted source file: {file_info['path']}")
                except Exception as e:
                    logging.error(f"Failed to delete {file_info['path']}: {e}")
        
        # Save updated history
        save_conversion_history(history)

    except Exception as e:
        error_msg = f"Error during conversion: {str(e)}"
        logging.error(error_msg, exc_info=True)
        messagebox.showerror("Error", error_msg)
        
        # Generate error report
        report_path = os.path.join(LOG_DIR, f"error_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(report_path, 'w') as f:
            f.write(f"Error Report\n\nTimestamp: {datetime.now()}\n")
            f.write(f"Error: {str(e)}\n\n")
            f.write("Conversion Issues:\n")
            for fname, issues in conversion_issues.items():
                f.write(f"{fname}: {', '.join(issues)}\n")
        
        messagebox.showinfo("Error Report", 
            f"An error report has been generated at:\n{report_path}")
    finally:
        progress_bar["value"] = 0
        status_label.config(text="Ready")
