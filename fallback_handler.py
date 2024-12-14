import os
from PIL import Image
from fpdf import FPDF
import requests
import time
from error_handling.error_logger import log_error
from error_handling.error_reporter import report_error
from error_handling.retry_mechanism import retry
from error_handling.preview_issues import preview_issues
from error_reporter import log_error

# CloudConvert API key (replace with your actual key)
CLOUDCONVERT_API_KEY = "your_cloudconvert_api_key"

def convert_heic_to_jpeg_with_cloudconvert(input_path, output_path):
    """Converts a HEIC file to JPEG using CloudConvert API."""
    try:
        url = "https://api.cloudconvert.com/v2/jobs"
        headers = {
            "Authorization": f"Bearer {CLOUDCONVERT_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "tasks": {
                "import-my-file": {"operation": "import/upload"},
                "convert-my-file": {"operation": "convert", "input": "import-my-file", "output_format": "jpg"},
                "export-my-file": {"operation": "export/url", "input": "convert-my-file"}
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
            if result_data["data"]["status"] == "finished":
                download_url = result_data["data"]["tasks"]["export-my-file"]["result"]["files"][0]["url"]
                download_response = requests.get(download_url)
                with open(output_path, "wb") as f:
                    f.write(download_response.content)
                break
            elif result_data["data"]["status"] in {"error", "failed"}:
                raise RuntimeError("CloudConvert job failed.")
            time.sleep(2)
    except Exception as e:
        log_error(str(e))
        raise RuntimeError(f"CloudConvert API error: {e}")


def heic_to_pdf_with_fallback(input_folder, output_pdf, compression_quality, supported_formats, progress_bar, status_label):
    """Converts HEIC, JPEG, PNG, BMP, GIF, and TIFF images to PDF with fallback for HEIC."""
    try:
        files = [f for f in os.listdir(input_folder) if f.lower().endswith(supported_formats)]
        if not files:
            messagebox.showwarning("No Supported Files", "No supported files (HEIC, JPEG, PNG, BMP, GIF, TIFF) found in the selected folder!")
            return

        images = []
        progress_bar["maximum"] = len(files)
        progress_bar["value"] = 0

        for i, filename in enumerate(files):
            file_path = os.path.join(input_folder, filename)
            output_image_path = os.path.join(input_folder, f"converted_{os.path.splitext(filename)[0]}.jpg")

            # Handle HEIC files
            if filename.lower().endswith(".heic"):
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
                    status_label.config(text=f"Falling back to CloudConvert for {filename}")
                    convert_heic_to_jpeg_with_cloudconvert(file_path, output_image_path)
            else:
                # Handle JPEG, PNG, BMP, GIF, and TIFF directly
                image = Image.open(file_path)
                if image.mode != "RGB":
                    image = image.convert("RGB")
                image.save(output_image_path, "JPEG", quality=compression_quality)

            images.append(Image.open(output_image_path))
            progress_bar["value"] += 1
            status_label.config(text=f"Processed: {filename} ({i + 1}/{len(files)})")
            progress_bar.update_idletasks()

        # Create PDF
        pdf = FPDF(unit="pt", format=[images[0].width, images[0].height])
        for img in images:
            pdf.add_page()
            temp_image_path = "temp_image.jpg"
            img.save(temp_image_path, "JPEG", quality=compression_quality)
            pdf.image(temp_image_path, 0, 0, img.width, img.height)
            os.remove(temp_image_path)

        pdf.output(output_pdf)
        messagebox.showinfo("Success", f"PDF created successfully: {output_pdf}")
    except Exception as e:
        log_error(str(e))
        report_error(str(e), "recipient@example.com")
        preview_issues([str(e)])
        log_error(str(e))
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        progress_bar["value"] = 0
        status_label.config(text="Ready")
