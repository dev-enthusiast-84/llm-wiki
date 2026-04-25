# PowerPoint/PPTX Presentation Generator

## Quick Start

### Option 1: Generate PowerPoint Locally (Recommended)

```bash
# Install dependencies
pip install python-pptx

# Run the generator
python create_presentation.py

# Output: LLM-Wiki-Presentation.pptx
```

### Option 2: Use the Pre-Generated Files

- **HTML Version**: `llm-wiki-presentation.html` - View in browser, download as PDF
- **Python Generator**: `create_presentation.py` - Customizable, generates PPTX

---

## 📊 Presentation Structure (5 Slides, ~10 minutes)

### Slide 1: Title Slide
- **Theme**: Purple gradient (102, 126, 234 → 118, 75, 162)
- **Content**: 
  - Main title: "🧠 From Concept to Implementation"
  - Subtitle: "Building an LLM Wiki: A Smart Knowledge Architecture"
  - Tagline: "Turning Andrej Karpathy's Vision into Reality"
- **Speaker Notes**: Covered (1.5 min)

### Slide 2: The Problem & Solution
- **Theme**: Pink gradient (240, 147, 251 → 245, 87, 108)
- **Content**:
  - Problem icons: 📚 Knowledge Overload, 🔗 Scattered Sources, 😵 No Structure
  - Karpathy's Insight box with key concept
- **Speaker Notes**: Covered (2 min)

### Slide 3: Three-Step Architecture
- **Theme**: Blue gradient (79, 172, 254 → 0, 242, 254)
- **Content**:
  - 4 step boxes: 1️⃣ Compile, 2️⃣ Sync, 3️⃣ Audit, 🔄 Repeat
  - Key principle box at bottom
- **Speaker Notes**: Covered (2.5 min)

### Slide 4: Real-World Implementation
- **Theme**: Orange gradient (250, 112, 154 → 254, 225, 64)
- **Content**:
  - 3 stat boxes: 3 Copilot Skills, 100+ Pages, Fully Automated
  - 5 feature bullet points
- **Speaker Notes**: Covered (2 min)

### Slide 5: Demo & Call to Action
- **Theme**: Cyan gradient (48, 207, 208 → 51, 8, 103)
- **Content**:
  - Video placeholder (▶️ Live Demo Video)
  - CTA box with repository link
  - Quick start instructions
- **Speaker Notes**: Covered (2 min)

---

## 🎨 Design Features

✅ **Gradient Backgrounds** - Each slide has a unique gradient for visual interest  
✅ **Emoji Icons** - Visual elements for quick comprehension  
✅ **Speaker Notes** - Detailed notes on every slide for delivery guidance  
✅ **Professional Layout** - 16:9 widescreen format (standard for modern presentations)  
✅ **Color-Coded** - Consistent color scheme for visual flow  
✅ **Accessible Fonts** - Segoe UI with sizes optimized for projection  

---

## 📝 Customization

Edit `create_presentation.py` to modify:

```python
# Change colors
colors = {
    1: {'bg': (R, G, B), 'accent': (R, G, B), 'text': (R, G, B)},
}

# Change slide content
title_para.text = "Your custom title"

# Change font sizes
title_para.font.size = Pt(60)
```

---

## 🚀 Generate & Export

### From PowerPoint (after running create_presentation.py):

1. Open `LLM-Wiki-Presentation.pptx` in Microsoft PowerPoint or Google Slides
2. **Export options**:
   - **PDF**: File → Export → PDF
   - **Video**: File → Export → Create Animated GIF/Video
   - **Share**: Upload to Google Drive → Share link

### From Google Slides:

1. Upload PPTX to Google Drive
2. Open with Google Slides
3. File → Download → PowerPoint (.pptx) or PDF

---

## 📊 Slide Timings

| Slide | Topic | Timing |
|-------|-------|--------|
| 1 | Title & Intro | 1.5 min |
| 2 | Problem & Concept | 2 min |
| 3 | Architecture | 2.5 min |
| 4 | Implementation | 2 min |
| 5 | Demo & CTA | 2 min |
| **Total** | | **~10 min** |

---

## 📥 Files Included

- `create_presentation.py` - Python script to generate PPTX
- `llm-wiki-presentation.html` - HTML/web version (browser-viewable)
- `README.md` - This file

---

## 🔗 Links & Resources

- **Repository**: https://github.com/dev-enthusiast-84/llm-wiki
- **Karpathy's Gist**: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- **HTML Version**: View directly in browser, no installation needed

---

## ⚠️ Requirements

- Python 3.7+
- python-pptx library

```bash
pip install python-pptx
```

---

## 📞 Support

For issues or customization needs:
1. Check the `create_presentation.py` script comments
2. Modify colors, text, or layout directly in the script
3. Regenerate the PPTX file

---

**Created**: 2026-04-25  
**Duration**: 10 minutes  
**Slides**: 5  
**Format**: PowerPoint (PPTX) + HTML + Python Generator
