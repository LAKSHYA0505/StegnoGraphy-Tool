# SecureCover: Advanced Steganography Tool 🔒🖼️

This project is part of my **AICTE IBM Cyber Security Internship**.

---

## 🔍 Project Description

**SecureCover** is an advanced steganography tool that allows embedding any file (text, PDF, image, etc.) inside image files using Least Significant Bit (LSB) technique.

### Key Features:

- Embed secret text or any file into cover images (BMP, PNG).
- Extract embedded secret data from stego images.
- Custom header to reliably identify message size and file extension during extraction.
- Seamless handling of both text-based and binary files.

> ⚠ **Disclaimer:**  
> This project is for educational and learning purposes only. Not intended for illegal use.

---

## 🔧 Technologies Used

- Python 3.x
- Pillow (PIL)
- Struct (for binary data handling)
- OS module (for file operations)

---

## 🚀 Current Features

- ✅ Text embedding into images.
- ✅ File embedding (PDF, image, any file type).
- ✅ File extraction with extension detection.
- ✅ Custom binary header structure.
- ✅ Error handling for image size, file formats, and corrupted data.
- ✅ Works on Windows and Linux (tested on Ubuntu).

---

## 🖼️ Example Flow

1️⃣ **Embed Mode:**
   - Start program → Choose embed
   - Provide cover image → Provide secret data (text or file) → Get stego image saved

2️⃣ **Extract Mode:**
   - Run program → Choose extract
   - Provide stego image → Extracted secret file or message appears

---

## 📈 Project Status

- ✅ Core embedding & extraction fully functional
- 🔜 AES encryption module (coming soon)
- 🔜 Steganalysis (coming soon)
- 🔜 Audio file support (coming soon)
- 🔜 GUI interface (coming soon)

---

## 📚 Learning Outcome

- Learned advanced steganography algorithms
- Worked with binary data encoding
- File I/O handling
- Built robust error-handling logic
- Applied cybersecurity concepts practically

---

## 🔧 Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```
    *(Replace `YOUR_USERNAME` and `YOUR_REPOSITORY_NAME` with your actual GitHub details)*

2. **Install dependencies:**
    ```bash
    pip install Pillow
    ```

---

## 🎮 Usage

Run the main script from your terminal:

```bash
python stegnography_tool.py

Follow on-screen prompts:

Embed Mode:

    Enter path of cover image

    Enter secret text or select a file to hide

    Enter output file name for stego image

Extract Mode:

    Enter path of stego image

    Extracted data will be printed (for text) or saved (for files)

👨‍💻 Author

Lakshya Garg
(Part of AICTE IBM Cyber Security Internship Project)