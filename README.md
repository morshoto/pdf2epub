# 📖 PDF to EPUB Converter Using Python  

## 📌 Introduction  

This is a **Python-based tool** that converts **PDF files into EPUB format**, ensuring that text formatting, images, and essential elements are preserved for a seamless reading experience. Additionally, the tool **generates a thumbnail** from the first page of the PDF to improve visual representation in e-readers and digital libraries.  

---

## 🎯 Objectives  

- ✅ Convert **PDF files** into **EPUB format** efficiently.  
- ✅ Retain **text formatting, images, and metadata**.  
- ✅ Support **batch conversion** for multiple PDFs.  
- ✅ Provide a **command-line interface (CLI)** and an optional **GUI**.  
- ✅ Ensure compatibility with major **EPUB readers**.  
- ✅ **Generate a cover thumbnail** from the first page of the PDF.  

---

## ✨ Features  

### 📂 Input Handling  
✔ Accepts **single** or **multiple** PDF files.  
✔ Supports **encrypted PDFs** (optional, requiring a password).  
✔ Preserves **metadata** such as **title, author, and publication date**.  

### 🔄 Conversion Process  
✔ Extracts **text, images, and formatting** from the PDF.  
✔ Converts text into **reflowable EPUB format**.  
✔ Handles **tables, footnotes, and hyperlinks**.  
✔ Converts **embedded fonts** where applicable.  
✔ Preserves **chapters and headings** as per the PDF structure.  

### 🖼 Thumbnail Generation  
✔ Automatically generates a **thumbnail image** from the **first page** of the PDF.  
✔ Saves the thumbnail in **JPEG/PNG format**.  
✔ Embeds the **thumbnail as the cover image** in the EPUB metadata.  
✔ Allows the user to **override the default thumbnail** with a custom image.  

### 📤 Output Handling  
✔ Generates an **EPUB file** with a proper content structure (`.epub`).  
✔ Embeds **images and multimedia elements**.  
✔ Supports **metadata editing** for the output EPUB.  
✔ Provides **progress logs** for each conversion.  

### ⚠ Error Handling  
✔ Logs **errors** if a PDF cannot be processed.  
✔ Provides **meaningful error messages and suggestions**.  

---

## 🛠 Technical Requirements  

### 📌 Programming Language & Libraries  
- **Language:** Python (3.x)  
- **Libraries Used:**  
  - `pdfminer.six` – Extracts text from PDFs.  
  - `pymupdf` (fitz) – Parses PDFs and extracts content.  
  - `pypdf` – Handles encrypted PDFs.  
  - `beautifulsoup4` – Generates structured HTML.  
  - `ebooklib` – Creates EPUB files.  
  - **`Pillow` – Generates and processes thumbnails.**  

### 🖥 System Requirements  
✔ Works on **Windows, macOS, and Linux**.  
✔ Requires **Python 3.x installed**.  
✔ Optional **GUI** can be built with `tkinter` or `PyQt`.  

---

## 💻 Command-Line Interface (CLI)  

### 🚀 Usage Example  
```bash
python pdf_to_epub.py input.pdf -o output.epub --thumbnail cover.png
```

### ⚙ Available Options  
| Option            | Description  |
|------------------|-------------|
| `-o`, `--output` | Specify output EPUB filename. |
| `-b`, `--batch`  | Convert multiple PDFs at once. |
| `-m`, `--metadata` | Edit metadata fields (title, author, etc.). |
| `-p`, `--password` | Unlock **encrypted PDFs** with a password. |
| `-t`, `--thumbnail` | Specify a **custom cover image** instead of auto-generated one. |

---

## 🎨 Graphical User Interface (GUI) (Optional)  

🔹 **Drag-and-drop support** for PDFs.  
🔹 **Progress bar** and **logs** for conversion.  
🔹 **Metadata editing** before conversion.  
🔹 Option to **select output folder**.  
🔹 **Thumbnail preview** and customization option.  

---

## 📌 Installation  

### 📥 Install Dependencies  
Make sure you have **Python 3.x** installed, then install the required dependencies:  

```bash
pip install -r requirements.txt
```

### ▶ Run the Converter  
```bash
python pdf_to_epub.py input.pdf
```

For batch conversion:
```bash
python pdf_to_epub.py --batch input1.pdf input2.pdf input3.pdf
```

For encrypted PDFs:
```bash
python pdf_to_epub.py input.pdf --password "mypassword"
```
