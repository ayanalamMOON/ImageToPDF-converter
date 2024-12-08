# 📱 HEIC, JPEG, PNG to PDF Converter

## My Story 🚀

Hey there! I'm Just your average CS student who was sick and tired of jumping through digital hoops just to convert my iPhone images into PDFs for assignments. 🙄 Every time I needed to submit something, I'd find myself lost in a maze of random apps, sketchy websites, and complicated conversion processes. 

So, what did I do? I built my own solution! 💪 What started as a simple HEIC to PDF converter has now evolved into a multi-format image conversion tool that saves me (and hopefully you) tons of time and headaches. No more downloading random apps, no more suspicious websites, just a clean, straightforward Python script that does exactly what you need.

## Why This Matters 🤔

- 📸 iPhone user? Got tons of HEIC images?
- 📚 Need to submit assignments quickly?
- 🛡️ Want to avoid sketchy online converters?

**This tool is your new best friend!**

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

