import os
import re
import glob


def locate_raw_images(book_root, raw_scans_subfolder, file_extensions):
    '''Find all matching images.'''
    if raw_scans_subfolder:
        pages_root = os.path.join(book_root, raw_scans_subfolder)
    else:
        pages_root = book_root

    img_list = []
    for ext in file_extensions:
        search_path = os.path.join(pages_root, f'*.{ext}')
        print(search_path)
        img_list.extend(glob.glob(search_path, recursive=False))
    
    return sorted(img_list)


def create_folders(book_root):
    '''Create any needed folders that don't already exist to store processed images'''

    output_dirs = ['cropped_pages', 'temp_images', 'manual_pages', 'pdf']

    for od in output_dirs:
        print(f"Creating {od} directory (if it doesn't already exist)...")
        os.makedirs(os.path.join(book_root, od), exist_ok=True)


def seek_manual_page(page_path, manual_pages):
    manual_test = page_path.replace('cropped_pages', 'manual_pages').replace('_cropped', '_manual')

    if manual_test in manual_pages:
        print(f"Replacing {page_path}...")
        return manual_pages[manual_pages.index(manual_test)]
    return page_path


def replace_manual_pages(book_root, cropped_pages):
    manual_pages = sorted(glob.glob(os.path.join(book_root, 'manual_pages', '*_manual.jpg')))
    if len(manual_pages) > 0:
        print(f"MANUAL PAGES FOUND. Trying to replace {len(manual_pages)} pages...")
        cropped_pages = [seek_manual_page(p, manual_pages)for p in cropped_pages]
    else:
        print(f"No manual pages found.")

    extra_pages = sorted(glob.glob(os.path.join(book_root, 'manual_pages', '*_manual_extra_*.jpg')))
    if len(extra_pages) > 0:
        print(f"EXTRA PAGES FOUND. Adding replace {len(extra_pages)} pages...")
        cropped_pages.extend(extra_pages)
        # Sorting should put properly formatted extra pages after the correct images when re-sorted
        # Sort list only by filename, not including folder
        cropped_pages = sorted(cropped_pages, key=lambda x: os.path.basename(x))
    else:
        print(f"No extra pages found.")
    
    return cropped_pages
