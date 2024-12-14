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
- Support for JPEG and PNG formats
- Adjustable compression quality
- Simple, clean GUI interface

### ⚡ Enhanced Usability
- **Drag & Drop Support**
  - Drag folders directly into the input field
  - Drag files for output PDF location
  - Right-click context menu for quick actions

- **Keyboard Shortcuts**
  - `Ctrl+O`: Browse input folder
  - `Ctrl+S`: Choose PDF save location
  - `Ctrl+Enter`: Start conversion

### 🚀 New Enhanced Features
- Batch processing: Select multiple folders for conversion at once
- Customizable output settings: Set page size, orientation, and margins
- Image editing tools: Crop, rotate, and resize images before conversion
- Support for additional formats: BMP, GIF, and TIFF
- Cloud storage integration: Save output PDF directly to cloud storage services
- Email notifications: Receive notifications upon successful conversion or errors
- Command-line interface: Use terminal commands for advanced users
- Multi-language support: Accessible to a wider audience
- Dark mode: Reduce eye strain with a dark mode option
- Detailed progress tracking: Show detailed information about the current file being processed and estimated time remaining

### 🛡️ On-Device Error Reporting System
- On-device error logs: Collect and store error logs locally on the device
- Automatic error logging: Log error messages to a local file
- Analyze error data: Use the local error logs to analyze error data and identify common issues

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

### Additional Dependencies
5. **tkinterdnd2** 🎯
   - Enables drag & drop functionality
   - Install with:
     ```bash
     pip install tkinterdnd2
     ```

6. **requests** 🌐
   - HTTP library for making API requests
   - Install with:
     ```bash
     pip install requests
     ```

7. **smtplib** 📧
   - Library for sending email notifications
   - Comes with Python, no extra install needed!

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

## 💡 Pro Tips
- Wanna add more image formats? Go for it! 
- Facing dependency issues? That's just a skill issue, my friend! 💪
- Keep calm and convert on! 🚀
- Use drag & drop for faster workflow
- Learn the keyboard shortcuts for maximum efficiency
- Right-click entries for quick actions

## 📚 Usage Instructions

### Basic Usage
1. Open the application.
2. Drag and drop the input folder containing images into the input field or use `Ctrl+O` to browse.
3. Drag and drop the output PDF location into the output field or use `Ctrl+S` to save.
4. Set the compression quality, page size, orientation, and margins as needed.
5. Enter your email address for notifications (optional).
6. Click "Convert" or press `Ctrl+Enter` to start the conversion.

### Batch Processing
1. Select multiple folders for conversion by dragging and dropping them into the input field.
2. Follow the same steps as basic usage for each folder.

### Image Editing Tools
1. Before conversion, use the built-in image editing tools to crop, rotate, and resize images as needed.

### Cloud Storage Integration
1. After conversion, choose to save the output PDF directly to cloud storage services like Google Drive, Dropbox, or OneDrive.

### Command-Line Interface
1. For advanced users, use terminal commands to perform conversions without the GUI.

### Multi-Language Support
1. Select your preferred language from the settings menu to make the application accessible in multiple languages.

### Dark Mode
1. Enable dark mode from the settings menu to reduce eye strain and improve user experience.

### Detailed Progress Tracking
1. Monitor the progress bar to see detailed information about the current file being processed and estimated time remaining.

### On-Device Error Reporting System
1. Configure the error log file path in the `error_reporter.py` file.
2. Error logs will be automatically stored locally on the device for analysis.
3. Use the centralized system to analyze error data and identify common issues.
4. Utilize different logging levels (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL) to categorize the severity of errors and provide more granular information.
5. Include stack traces when logging exceptions to provide more detailed information about where the error occurred.
6. Regularly review the error logs to identify patterns and recurring issues, and take corrective actions to address them.
