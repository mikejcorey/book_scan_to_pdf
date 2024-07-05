import os
import glob
import img2pdf
from multiprocessing.pool import ThreadPool

from utils.folder_ops import locate_raw_images, create_folders
from utils.image_manipulation import rotate_and_crop_image

from dotenv import load_dotenv

load_dotenv()

BOOK_ROOT = os.getenv("BOOK_ROOT")
RAW_SCANS_SUBFOLDER = os.getenv("RAW_SCANS_SUBFOLDER", None)
IMAGE_EXTENSIONS = os.getenv("IMAGE_EXTENSIONS", 'jpg,JPG,jpeg,JPEG').split(',')
NUM_THREADS = os.getenv("NUM_THREADS", 8)

def main():
    pages_to_process = locate_raw_images(BOOK_ROOT, RAW_SCANS_SUBFOLDER, IMAGE_EXTENSIONS)

    print(f"Found {len(pages_to_process)} matching image files.")
    # print(pages_to_process)

    create_folders(BOOK_ROOT)

    # Prepare page list for multithreading because it's complicated to use multiple arguments with the threadpool
    pages_to_process_multi = [{'book_root': BOOK_ROOT, 'page_path': p} for p in pages_to_process]

    pool = ThreadPool(processes=NUM_THREADS)
    pool.map(rotate_and_crop_image, pages_to_process_multi)

    cropped_pages = sorted(glob.glob(os.path.join(BOOK_ROOT, 'cropped_pages', '*.jpg')))

    pdf_filename = f"{BOOK_ROOT.split('/')[-1]}.pdf"
    final_pdf_path = os.path.join(BOOK_ROOT, 'pdf', pdf_filename)
    print(f"Exporting {final_pdf_path}...")

    with open(final_pdf_path,"wb") as f:
        f.write(img2pdf.convert(cropped_pages))

if __name__ == "__main__":
    main()