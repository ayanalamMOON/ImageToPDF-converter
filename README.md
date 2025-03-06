# 📱 HEIC, JPEG, PNG to PDF Converter

## My Story 🚀

Hey there! I'm Just your average CS student who was sick and tired of jumping through digital hoops just to convert my iPhone images into PDFs for assignments. 🙄 Every time I needed to submit something, I'd find myself lost in a maze of random apps, sketchy websites, and complicated conversion processes. 

So, what did I do? I built my own solution! 💪 What started as a simple HEIC to PDF converter has now evolved into a multi-format image conversion tool that saves me (and hopefully you) tons of time and headaches. No more downloading random apps, no more suspicious websites, just a clean, straightforward Python script that does exactly what you need.

## Why This Matters 🤔

- 📸 iPhone user? Got tons of HEIC images?
- 📚 Need to submit assignments quickly?
- 🛡️ Want to avoid sketchy online converters?

**This tool is your new best friend!**

## 🌟 Features

### 🎯 Core Features
- Convert HEIC images to PDF
- Support for JPEG, PNG, BMP, and GIF formats
- Adjustable compression quality
- Simple, clean GUI interface

### 📄 PDF Customization
- **Layout Options**
  - Portrait/Landscape orientation
  - Standard page sizes (A4, Letter, Legal)
  - Custom page dimensions
  - Smart image scaling and centering

- **Document Enhancement**
  - Custom watermarks
  - Page numbers
  - PDF compression control
  - Multi-PDF merging
  - Custom fonts
  - Background colors

- **Professional Output**
  - Consistent formatting
  - Proper image alignment
  - Quality preservation
  - Batch PDF processing

### ⚡ Enhanced Usability
- **Drag & Drop Support**
  - Drag folders directly into the input field
  - Drag files for output PDF location
  - Right-click context menu for quick actions

- **Keyboard Shortcuts**
  - `Ctrl+O`: Browse input folder
  - `Ctrl+S`: Choose PDF save location
  - `Ctrl+Enter`: Start conversion

### 🛡️ Error Handling & Diagnostics
- **Smart Error Detection**
  - Pre-conversion image analysis
  - Resolution and file size warnings
  - Color mode compatibility checks
  
- **Comprehensive Logging**
  - Detailed error logs with timestamps
  - Easy-to-access log viewer
  - Automatic error reporting
  
- **Recovery Features**
  - Automatic retry for failed conversions
  - Issue preview before conversion
  - Conversion status tracking

### 📁 File Management
- **Smart Directory Scanning**
  - Recursive folder scanning
  - Date-based file filtering
  - Skip already converted files
  - Source file cleanup option

- **Conversion History**
  - Track converted files
  - View conversion timestamps
  - Monitor output locations
  - Prevent duplicate conversions

- **File Processing**
  - Intelligent file change detection
  - Automatic file organization
  - Batch processing optimization
  - Source cleanup options

## 🛠 Dependencies Installation Guide (aka Skill Acquisition 101) 

### 🐍 Python Libraries You'll Need

1. **Pillow (PIL)** 🖼️
   - The image manipulation wizard
   - Converts images, makes them look pretty
   - Install with the magic spell: 
     ```bash
     pip install pillow
     ```

2. **pyheif** 🍎 
   - Your HEIC decoding ninja
   - Turns those iPhone images into something everyone can read
   - Install with:
     ```bash
     pip install pyheif
     ```
   - Pro tip: You'll also need `libheif` (more on that below) 😉

3. **FPDF** 📄
   - PDF creation guru
   - Transforms your images into a slick PDF
   - Install command:
     ```bash
     pip install fpdf
     ```

4. **tkinter** 🖥️
   - Your GUI building buddy
   - Already comes with Python, so no extra install needed! 
   - Free real estate! 🎊

5. **PyPDF2** 📑
   - PDF manipulation powerhouse
   - Handles PDF merging and more
   - Install with:
     ```bash
     pip install PyPDF2
     ```

6. **tkinterdnd2** 🎯
   - Enables drag & drop functionality
   - Install with:
     ```bash
     pip install tkinterdnd2
     ```

7. **logging** 📝
   - Built-in Python logging system
   - No installation needed
   - Automatically tracks all operations

### 🖥️ System Dependencies

#### libheif (The HEIC Whisperer)
- Required for pyheif to work its magic
- Windows Installation Guide:
  1. Head to [libheif GitHub Releases](https://github.com/strukturag/libheif/releases)
  2. Download the pre-built binaries
  3. Extract those sweet `.dll` files
  4. Do ONE of these:
     - Add to system PATH (tech ninja mode 🥷)
     - Drop files in the same folder as your script (lazy mode activated 😎)
     - If the binaries are not available, compile on you're own (stop complaing and start compiling 🤡)

## 💡 Pro Tips
- Wanna add more image formats? Go for it! 
- Facing dependency issues? That's just a skill issue, my friend! 💪
- Keep calm and convert on! 🚀
- Use drag & drop for faster workflow
- Learn the keyboard shortcuts for maximum efficiency
- Right-click entries for quick actions
- Check error logs for troubleshooting
- Review pre-conversion warnings
- Use the error log viewer for detailed diagnostics
- Use date filters to process recent files
- Enable recursive scanning for nested folders
- Keep track of conversions with history viewer
- Clean up source files automatically after conversion
- Check conversion history before processing
- Use custom page sizes for special documents
- Add watermarks for document protection
- Enable page numbers for long documents
- Merge related PDFs into single documents
- Choose orientation based on image dimensions

