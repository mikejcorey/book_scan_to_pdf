import os
import glob
import pytest

from dotenv import load_dotenv

from utils.folder_ops import seek_manual_page, replace_manual_pages

load_dotenv()

BOOK_ROOT = os.getenv("BOOK_ROOT")
RAW_SCANS_SUBFOLDER = os.getenv("RAW_SCANS_SUBFOLDER", None)
IMAGE_EXTENSIONS = os.getenv("IMAGE_EXTENSIONS", 'jpg,JPG,jpeg,JPEG').split(',')
NUM_THREADS = os.getenv("NUM_THREADS", 8)

def extract_page_num(file_path):
    basename = os.path.basename(file_path)
    return int(basename.split('_')[0])


# def test_page_continuity_katznelson():
#     pages = glob.glob(os.path.join(BOOK_ROOT, 'cropped_pages', '*.jpg'))
#     page_nums = sorted([extract_page_num(page) for page in pages])

#     max_page = max(page_nums)

#     print(page_nums)

#     assert(len(page_nums) == max_page + 1)

def test_extra_page_sorting():
    ''' More of a conceptual test'''
    start_pages = [
        "thing_001_cropped.jpg",
        "thing_002_cropped.jpg",
        "thing_003_cropped.jpg",
        "thing_004_cropped.jpg"
    ]

    extra_pages = [
        "thing_002_manual_extra_01.jpg",
        "thing_002_manual_extra_02.jpg"
    ]

    manual_pages = [
        "thing_002_manual.jpg",
        "thing_002_manual.jpg"
    ]

    start_pages.extend(extra_pages)
    start_pages.extend(manual_pages)
    combined_sorted = sorted(start_pages)

    for c in combined_sorted:
        print(c)

    assert combined_sorted == [
        'thing_001_cropped.jpg',
        'thing_002_cropped.jpg',
        'thing_002_manual.jpg',
        'thing_002_manual.jpg',
        'thing_002_manual_extra_01.jpg',
        'thing_002_manual_extra_02.jpg',
        'thing_003_cropped.jpg',
        'thing_004_cropped.jpg',
    ]

def test_page_sorting():
    book_root = 'tests/test_images/book1'
    cropped_pages = glob.glob(os.path.join(book_root, 'cropped_pages', '*.jpg'))

    sort_result = replace_manual_pages(book_root, cropped_pages)

    print(sort_result)

    assert len(cropped_pages) > 0
    assert len(sort_result) > 0
    assert sort_result == [
        'tests/test_images/book1/cropped_pages/0001_cropped.jpg',
        'tests/test_images/book1/cropped_pages/0002_cropped.jpg',
        'tests/test_images/book1/manual_pages/0002_manual_extra_01.jpg',
        'tests/test_images/book1/manual_pages/0002_manual_extra_02.jpg',
        'tests/test_images/book1/cropped_pages/0003_cropped.jpg',
        'tests/test_images/book1/manual_pages/0004_manual.jpg',
        'tests/test_images/book1/manual_pages/0005_manual.jpg',
    ]