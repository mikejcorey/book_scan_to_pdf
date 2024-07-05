import os
import glob
# import shutil
# from local_settings import EDITIONS_ROOT, SECTIONS_TO_SCAN


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

    output_dirs = ['cropped_pages', 'temp_images', 'pdf']

    for od in output_dirs:
        print(f"Creating {od} directory (if it doesn't already exist)...")
        os.makedirs(os.path.join(book_root, od), exist_ok=True)
    


# def locate_raw_images(book_root, book_title, section_folder=None):
#     '''Find raw images given a pattern to match. Defaults to scanning all JPEGs in the edition directory, but can be set to handle individual folders.'''
#     if section_folder:
#         pages = glob.glob(os.path.join(editions_root, edition_title, 'raw_scans', section_folder, '*.jpg'))
#     else:
#         pages = glob.glob(os.path.join(editions_root, edition_title, 'raw_scans', '*.jpg'))
#     return {
#         'edition_title': edition_title,
#         'section': section_folder,
#         'pages': pages
#     }

# def create_folders(edition_folder, section_folder=None):
#     '''Create any needed folders that don't already exist to store OCR output'''

#     output_dirs = ['ocr_text', 'processed_scans']

#     for od in output_dirs:

#         try:
#             os.mkdir(os.path.join(edition_folder, od))
#             print('Created {} directory.'.format(od))
#         except FileExistsError:
#             print('{} directory already exists.'.format(od))

#         if section_folder:
#             final_dir = os.path.join(od, section_folder)

#             try:
#                 os.mkdir(os.path.join(edition_folder, final_dir))
#                 print('Created {} section directory.'.format(final_dir))
#             except FileExistsError:
#                 print('{} section directory already exists.'.format(final_dir))


#Loops through directories to get to the book title directories

# def path_tokey_directories():
#
#     dirs = os.listdir(EDITIONS_ROOT)
#     edition_dirs = []
#     pages = []
#
#     for i in dirs:
#         if i in ['necrology', 'miscellaneous']:
#             continue
#         newdir = os.path.join(EDITIONS_ROOT, i)
#         if os.path.isdir(newdir):
#             inner_dirs = os.listdir(newdir)
#
#             for id in inner_dirs:
#                 edition_path = os.path.join(newdir, id)
#                 if os.path.isdir(edition_path):
#                     edition_dirs.append(edition_path)
#                     process_dirs = os.listdir(edition_path)
#
#                     for ix in process_dirs:
#                         ix_dirs = os.path.join(edition_path, ix)
#                         pages.append(ix_dirs)
#
#     return edition_dirs, pages

#checks for necessary directories, creates them if they don't exist

# def create_folders():
#
#     necessary_dirs = ['ocr_text', 'processed_scans', 'raw_scans']
#
#     for a in necessary_dirs:
#         edition_dirs, pages = path_tokey_directories()
#
#         for c in edition_dirs:
#             try:
#                 final_path = os.path.join(c, a)
#                 if not os.path.exists(final_path):
#                     os.mkdir(final_path)
#                     print("Directory created")
#
#             except FileExistsError:
#                 print("Directory already exists")


#finds all instances where a file ends in '.jpg' and moves them to 'raw_scans' directory

# def check_jpg():
#
#     edition_dirs, pages = path_tokey_directories()
#
#     for b in pages:
#         if b[-4:] == '.jpg':
#             base_dir = b.rsplit('/', 1)
#             shutil.move(b, os.path.join(base_dir[0], 'raw_scans'))
#             print('Moving ' + base_dir[1] + ' to raw_scans directory')


# def setup():
#     print(locate_raw_images(EDITIONS_ROOT, '1990', 'alpha_list'))
#     # print(path_tokey_directories())
#     # create_folders()
#     # check_jpg()
#
# if __name__ == "__main__":
#     setup()
