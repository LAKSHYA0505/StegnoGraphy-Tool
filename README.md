# SecureCover: Advanced Steganography Tool 🔒🖼️

This project is part of my AICTE IBM Cyber Security Internship.

---

## 🔍 Project Description

**SecureCover** is an advanced steganography tool that allows embedding any file (text, PDF, image, etc.) inside image files using Least Significant Bit (LSB) technique. The project currently supports:

- Embedding secret text or any file into cover images (BMP, PNG).
- Extracting embedded secret data from stego images.
- Using a custom header to reliably identify message size and file extension during extraction.
- Seamless handling of both text-based and binary files.

The project is being actively developed and will soon include:

- 🔐 AES encryption for added security.
- 🎯 Steganalysis module to detect hidden data.
- 🎵 Audio-based steganography support.
- 🖥️ Graphical User Interface (GUI) for ease of use.

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

## 📦 Installation Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME

2️⃣ Install Dependencies
pip install pillow

🎯 Usage
  Run the Tool:
  python steganography_tool.py

  Follow on-screen prompts:

    Embed Mode:

        Enter path of cover image.

        Enter secret text or select a file to hide.

        Enter output file name for stego image.

    Extract Mode:

        Enter path of stego image.

        Extracted data will be printed (for text) or saved (for files).

🖼️ Example Flow

1️⃣ Start program → Choose embed
2️⃣ Provide image → Provide secret data (text or file) → Get stego image saved.

3️⃣ Later run → Choose extract
4️⃣ Provide stego image → Extracted secret file or message appears.

📈 Project Status

    ✅ Core embedding & extraction fully functional.

    🔜 AES encryption module (coming soon).

    🔜 Steganalysis (coming soon).

    🔜 Audio file support (coming soon).

    🔜 GUI interface (coming soon).

📚 Learning Outcome

    Learned advanced steganography algorithms.

    Worked with binary data encoding.

    File I/O handling.

    Built robust error-handling logic.

    Applied cybersecurity concepts practically.


⚠️ Disclaimer

This project is for educational and learning purposes only. Not intended for illegal use.
