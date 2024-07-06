# Book scan to PDF

A library to take sets of images from a DIY bookscanner to a PDF. Note that this process does not OCR the PDF.

Note: requires qpdf (On Mac, installed with Homebrew)

## Replacing/adding pages

### Replacing pages

If you have bad scans you need to replace, place each in the `manual_pages` folder, in the same format as the other pages, except with `_manual` appended. For example:

```
book_root
|
├── raw_scans
|   ├── 0001.jpg
|   ├── 0002.jpg
|   ├── 0003.jpg
|
├── cropped_pages
|   ├── 0001_cropped.jpg
|   ├── 0002_cropped.jpg
|   ├── 0003_cropped.jpg
|
├── manual_pages
    ├── 0002_manual.jpg <-- will replace 002_cropped.jpg
```

### Inserting pages

If you would like to insert pages that you missed, place each in the `manual_pages` folder, with the page number you want to insert the image AFTER, with the `manual_extra` and ordering number after. For example:

```
book_root
|
├── raw_scans
|   ├── 0001.jpg
|   ├── 0002.jpg
|   ├── 0003.jpg
|
├── cropped_pages
|   ├── 0001_cropped.jpg
|   ├── 0002_cropped.jpg
|   ├── 0003_cropped.jpg
|
├── manual_pages
    ├── 0002_manual_extra_01.jpg <-- will be inserted after 002_cropped.jpg
```