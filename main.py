#!/usr/bin/env python3
"""
PDF to EPUB Converter
---------------------
Converts PDF files to EPUB format, including generating a thumbnail cover
from the first page of the PDF.
"""

import argparse
import os

import fitz
from bs4 import BeautifulSoup
from ebooklib import epub
from PIL import Image
from pypdf import PdfReader

from src.logging.Logging import logger


def generate_cover_image(pdf_path, output_path="./data/cover.jpg", dpi=150):
    """
    Generates a cover image (thumbnail) from the first page of the PDF using PyMuPDF.
    Saves the cover image as JPEG (default) or you can switch to PNG by changing output_path extension.
    """
    try:
        with fitz.open(pdf_path) as doc:
            # Load the first page
            page = doc.load_page(0)
            # Render page to a pixel map
            pix = page.get_pixmap(dpi=dpi)

            # Convert Pixmap to PIL Image
            mode = "RGBA" if pix.alpha else "RGB"
            img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)

            # Resize or process image if needed (e.g., create a smaller thumbnail)
            img.save(output_path, "JPEG")
        logger.info(f"Cover image generated at: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Failed to generate cover image for '{pdf_path}': {e}")
        logger.exception(e)
        return None


def extract_pdf_text(pdf_path, password=None):
    """
    Extract text (and possibly other elements) from a PDF. This example uses PyPDF (pypdf).
    For more advanced extraction (including images, layout, fonts), consider using pdfminer.six or PyMuPDF in detail.
    """
    try:
        reader = PdfReader(pdf_path)
        if reader.is_encrypted and password:
            reader.decrypt(password)

        extracted_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)

        combined_text = "\n".join(extracted_text)
        logger.info(
            f"Extracted text from '{pdf_path}' (length: {len(combined_text)} chars)."
        )
        return combined_text
    except Exception as e:
        logger.error(f"Failed to extract text from '{pdf_path}': {e}")
        logger.exception(e)
        return ""


def create_epub_from_text(
    text_content, cover_image=None, title="Untitled", author="Unknown", metadata=None
):
    """
    Create an EPUB file from plain text content. Embeds the cover_image if provided.
    """
    # Create an EPUB book
    book = epub.EpubBook()

    # Set metadata
    book.set_identifier("id_123456")
    book.set_title(title)
    book.set_language("en")
    book.add_author(author)

    # If provided, set additional metadata
    if metadata:
        for key, value in metadata.items():
            book.add_metadata("DC", key, value)

    # If text_content is empty, ensure we have at least some placeholder text.
    if not text_content.strip():
        logger.warning("No text content extracted. Adding placeholder paragraph.")
        text_content = "No textual content could be extracted from this PDF."

    # Create a "chapter" from the text_content
    c1 = epub.EpubHtml(title="Content", file_name="content.xhtml", lang="en")

    # Use BeautifulSoup to create a simple HTML structure from the text
    soup = BeautifulSoup("", "html.parser")
    for line in text_content.splitlines():
        p = soup.new_tag("p")
        p.string = line
        soup.append(p)

    c1.content = str(soup)
    book.add_item(c1)

    # Add default NCX and NAV
    book.toc = (epub.Link("content.xhtml", "Content", "content"),)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Optionally set cover image
    if cover_image and os.path.exists(cover_image):
        with open(cover_image, "rb") as img_file:
            book.set_cover(os.path.basename(cover_image), img_file.read())

    # Define CSS style (optional)
    style = """
    body {
        font-family: Arial, sans-serif;
        margin: 10px;
    }
    p {
        text-align: justify;
        margin-bottom: 1em;
    }
    """
    nav_css = epub.EpubItem(
        uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style
    )
    book.add_item(nav_css)

    # Create spine
    book.spine = ["nav", c1]

    return book


def save_epub(book, output_path):
    """
    Saves the EPUB book to the specified output_path.
    """
    logger.debug(f"Attempting to write EPUB file to: {output_path}")
    epub.write_epub(output_path, book, {})
    logger.info(f"EPUB successfully saved: {output_path}")


def convert_pdf_to_epub(
    pdf_path, output_path=None, password=None, custom_cover=None, metadata=None
):
    """
    High-level function that extracts text from PDF, generates a cover image,
    creates an EPUB, and saves it.
    """
    try:
        # Derive output name from PDF name if not specified
        if not output_path:
            base = os.path.splitext(pdf_path)[0]
            output_path = base + ".epub"

        # Generate a cover thumbnail from first page unless a custom cover is provided
        if custom_cover and os.path.exists(custom_cover):
            cover_image = custom_cover
            logger.info(f"Using custom cover image: {cover_image}")
        else:
            cover_image = generate_cover_image(pdf_path)

        # Extract PDF text
        text_content = extract_pdf_text(pdf_path, password=password)

        # Use the PDF filename as the default "title" if none in metadata
        title = (
            metadata.get("title", os.path.basename(pdf_path))
            if metadata
            else os.path.basename(pdf_path)
        )
        author = metadata.get("author", "Unknown") if metadata else "Unknown"

        # Build the EPUB from the extracted text
        book = create_epub_from_text(
            text_content,
            cover_image=cover_image,
            title=title,
            author=author,
            metadata=metadata,
        )

        # Save the EPUB
        save_epub(book, output_path)

    except Exception as e:
        logger.error(f"Failed to convert '{pdf_path}' to EPUB: {e}")
        logger.exception(e)


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF(s) to EPUB format with optional cover thumbnail."
    )
    parser.add_argument(
        "input_files", nargs="+", help="Path to one or more PDF files to convert."
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output EPUB file name (only valid if converting a single PDF).",
    )
    parser.add_argument(
        "-b", "--batch", action="store_true", help="Batch convert multiple PDFs."
    )
    parser.add_argument("-p", "--password", help="Password if PDF is encrypted.")
    parser.add_argument(
        "-t", "--thumbnail", help="Path to a custom thumbnail image to embed as cover."
    )
    parser.add_argument(
        "-m",
        "--metadata",
        nargs="+",
        help="Optional metadata in key=value format (e.g. title=MyBook author=JohnDoe).",
    )

    args = parser.parse_args()

    # Process metadata from CLI
    meta_dict = {}
    if args.metadata:
        for pair in args.metadata:
            if "=" in pair:
                k, v = pair.split("=", 1)
                meta_dict[k.lower()] = v

    # Single or batch conversion
    if args.batch and len(args.input_files) > 1:
        for pdf_file in args.input_files:
            convert_pdf_to_epub(
                pdf_file,
                output_path=None,
                password=args.password,
                custom_cover=args.thumbnail,
                metadata=meta_dict,
            )
    else:
        # Single PDF or multiple files, but not in batch mode
        if len(args.input_files) == 1 and args.output:
            convert_pdf_to_epub(
                args.input_files[0],
                output_path=args.output,
                password=args.password,
                custom_cover=args.thumbnail,
                metadata=meta_dict,
            )
        else:
            for pdf_file in args.input_files:
                convert_pdf_to_epub(
                    pdf_file,
                    output_path=None,
                    password=args.password,
                    custom_cover=args.thumbnail,
                    metadata=meta_dict,
                )


if __name__ == "__main__":
    main()
