import os
import glob
import pytest

from dotenv import load_dotenv

load_dotenv()

BOOK_ROOT = os.getenv("BOOK_ROOT")
RAW_SCANS_SUBFOLDER = os.getenv("RAW_SCANS_SUBFOLDER", None)
IMAGE_EXTENSIONS = os.getenv("IMAGE_EXTENSIONS", 'jpg,JPG,jpeg,JPEG').split(',')
NUM_THREADS = os.getenv("NUM_THREADS", 8)

def extract_page_num(file_path):
    basename = os.path.basename(file_path)
    return int(basename.split('_')[0])


def test_page_continuity_katznelson():
    pages = glob.glob(os.path.join(BOOK_ROOT, 'cropped_pages', '*.jpg'))
    page_nums = sorted([extract_page_num(page) for page in pages])

    max_page = max(page_nums)

    print(page_nums)

    assert(len(page_nums) == max_page + 1)