# HYPOCRITICAL SAINT
### Digital Image Steganography Studio
### استوديو إخفاء البيانات في الصور الرقمية
> *"بريء في الظاهر.. وسرّي في الباطن"*  
> *"Innocent on the Outside. Secret on the Inside."*

---

## 1. Project Overview | نظرة عامة عن المشروع

**HYPOCRITICAL SAINT** is an academic software application and graphical workstation dedicated to the study, demonstration, and evaluation of **Digital Image Steganography** and information hiding within the spatial domain of digital raster graphics.

The name *Hypocritical Saint* embodies the core philosophy of steganographic communication: an image that outwardly projects complete innocence, serenity, and visual normalcy, while covertly concealing confidential data within its low-order spatial structures. Unlike traditional cryptography—which scrambles plaintext into noticeable, suspicious ciphertext—steganography conceals the very existence of the communication. 

Built as a specialized academic extension of the open-source `Stegano` engine, this studio integrates spatial pixel manipulation, mathematical coordinate scattering, reversible histogram-shifting data hiding, objective perceptual fidelity analysis (MSE, PSNR), and least-significant-bit parity steganalysis into a warm, elegant **Maroon × Soft Ivory × Charcoal** bilingual workstation.

---

## 2. Academic Information | المعلومات الأكاديمية

| Academic Field | Official Specification | المواصفات الأكاديمية |
| :--- | :--- | :--- |
| **Project Name** | **HYPOCRITICAL SAINT** | **HYPOCRITICAL SAINT** |
| **Application Subtitle** | Digital Image Steganography Studio | استوديو إخفاء البيانات في الصور الرقمية |
| **Tagline** | *"Innocent on the Outside. Secret on the Inside."* | *"بريء في الظاهر.. وسرّي في الباطن"* |
| **Project Type** | Digital Image Steganography and Information Hiding | إخفاء وتشفير البيانات في الصور الرقمية |
| **Curricular Course** | **Digital Image Processing (DIP)** | **معالجة الصور الرقمية** |
| **Author / Developer** | **Um Al-Baneen Awwad (أم البنين عواد)** | **أم البنين عواد** |
| **Department** | Department of Computer Engineering | قسم هندسة الحاسوب |
| **College** | College of Engineering | كلية الهندسة |
| **University** | **University of Basrah** | **جامعة البصرة** |
| **Academic Year** | **2026–2027** | **2026–2027** |

### Academic Project Abstract
An academic Digital Image Processing application designed to demonstrate image-based information hiding, message extraction, reversible data hiding, and the evaluation of image quality after steganographic modifications. The system provides students and researchers with hands-on experimentation in spatial-domain bit modulation, mathematical pixel traversal, histogram modification, and objective perceptual quality assessment with complete bilingual (Arabic & English) support.

---

## 3. Quick Start — Windows (One-Command Setup) | البدء السريع بنقرة واحدة

You can set up, install dependencies, and launch **HYPOCRITICAL SAINT** on any Windows 10 or Windows 11 computer using a single PowerShell command.

### 3.1 One-Line PowerShell Installation

Open **PowerShell** (no Administrator privileges required) and run:

```powershell
irm https://raw.githubusercontent.com/xdc7-css/Hypocritical-Saint/main/setup.ps1 | iex
```

> [!NOTE]
> **Repository Source:** Clones and installs the verified release directly from the official GitHub repository:  
> [https://github.com/xdc7-css/Hypocritical-Saint](https://github.com/xdc7-css/Hypocritical-Saint)

#### What this automated script does:
1. **Windows Environment Inspection:** Validates Windows 10/11 compatibility and PowerShell runtime.
2. **Python Detection:** Verifies Python 3.10–3.12 availability (supports Python launcher `py` and standard `python`).
3. **Default Installation Path (`D:\Hypocritical-Saint`):**
   - Automatically detects whether drive `D:` exists.
   - If `D:` is present, installs into `D:\Hypocritical-Saint`.
   - If `D:` is unavailable, smoothly falls back to `C:\Hypocritical-Saint` without failing.
   - Preserves existing files and avoids overwriting without inspection.
4. **Dedicated Virtual Environment:** Creates an isolated `.venv` environment and upgrades `pip`.
5. **Dependency Installation:** Automatically installs `stegano`, `gradio (>=6.0.0)`, `opencv-python`, `pillow`, and `numpy`.
6. **Automated Verification:** Runs diagnostic checks to ensure all cryptographic and UI modules load cleanly.
7. **Global CLI Registration:** Registers the system-wide command `PROJECT RUN` so you can launch the studio from any directory.
8. **Automatic Launch:** Starts the local server and opens your default browser at:
   ```
   http://127.0.0.1:7860
   ```

---

### 3.2 Instant Global Command: `PROJECT RUN`

Once installed, you do **not** need to navigate to the installation directory or manually activate virtual environments. You can launch the studio at any time from **ANY** command prompt or PowerShell window:

```cmd
PROJECT RUN
```

*(Commands are fully case-insensitive: `PROJECT RUN`, `project run`, and `Project Run` are all recognized).*

#### Additional CLI Options:
| Command | Action |
| :--- | :--- |
| `PROJECT RUN` | Starts the server and opens `http://127.0.0.1:7860` (if already active, focuses browser without spawning duplicates) |
| `PROJECT STATUS` | Checks whether the local studio server is actively listening on port 7860 |
| `PROJECT HELP` | Displays command-line syntax and quick reference |

---

## 4. Bilingual Support & Simplified Terminology | الدعم ثنائي اللغة وتبسيط المصطلحات

The studio features a real-time language switcher (**العربية | English**) in the top-right header, enabling instant interface updates without server restarts.

### 4.1 Arabic-First & RTL Typography
- **Typography:** Features Google Fonts **Cairo** for natural Modern Standard Arabic and **Inter** for English.
- **Directionality:** Full native Right-to-Left (RTL) alignment for Arabic navigation and controls, while strictly preserving numerical metrics, binary coordinates, equations, and filenames in Left-to-Right (LTR).
- **Subtle Feature Indicator:** `✦ يدعم إخفاء واستخراج الرسائل باللغة العربية` (`✦ Supports Arabic and English hidden messages`).
- **Unicode Support:** Native encoding support for Arabic Unicode characters across Least Significant Bit (LSB) and Reversible Data Hiding (RDH via automated UTF-32LE fallback).

### 4.2 Terminology Simplification Mapping
| Technical Concept | Simplified English | المصطلح العربي المبسط |
| :--- | :--- | :--- |
| Cover Carrier Image | Original Image | **الصورة الأصلية** |
| Stego Carrier Image | Hidden-Message Image | **الصورة المخفية** |
| Hide Secret Data | Hide Message | **إخفاء رسالة** |
| Reveal Hidden Data | Reveal Message | **استخراج الرسالة** |
| Objective Image Fidelity & Distortion Analysis | Image Quality Comparison | **مقارنة جودة الصور** |
| Baseline Reference Image | Original Image | **الصورة الأصلية** |
| Comparative Image | Modified Image | **الصورة المعدّلة** |
| Spatial Error Map | Difference Map | **خريطة الاختلافات** |
| Modified Pixels | Changed Pixels | **البكسلات المتغيرة** |
| Reversible Data Hiding Studio | Restore Original Image | **استرجاع الصورة الأصلية** |
| LSB Parity Steganalysis | Hidden Bit Analysis | **تحليل البتات المخفية** |
| Extraction Parameters | Advanced Settings | **إعدادات متقدمة** |

---

## 5. Visual Identity & Design System | الهوية البصرية ونظام التصميم

The studio utilizes a warm, luxurious **Maroon × Soft Ivory × Charcoal** design system crafted to minimize visual fatigue and avoid excessive decorative noise:

| Design Token | Hex Code | Visual Application |
| :--- | :--- | :--- |
| **Main Background** | `#141316` | Deep charcoal foundation |
| **Primary Surface** | `#211C20` | Cards, panels, and container surfaces |
| **Elevated Surface** | `#2B2429` | Metric cards, active tabs, secondary buttons |
| **Input Background** | `#19161B` | Form fields, textareas, and image dropzones |
| **Primary Maroon** | `#8B354B` | Primary interactive color, action buttons, active indicator |
| **Maroon Hover** | `#A44861` | Button hover state with subtle glow |
| **Deep Maroon** | `#572334` | Subtle borders and container depths |
| **Soft Ivory** | `#F6F0E8` | High-contrast primary text and headings |
| **Warm Beige** | `#D9C6B0` | Secondary accent, labels, and metadata pills |
| **Secondary Text** | `#B8A9B0` | Muted slate-rose for descriptions and sub-labels |
| **Border Color** | `#40343C` | Razor-thin structural borders (no redundant nested lines) |
| **Success Color** | `#44B99A` | Emerald green for 100% lossless badges and toasts |
| **Error Color** | `#E67C86` | Soft rose-red for validation notices |

---

## 6. Digital Image Processing Concepts | مفاهيم معالجة الصور الرقمية

The architecture of **HYPOCRITICAL SAINT** directly incorporates several foundational concepts from Digital Image Processing:

### 6.1 Digital Image Representation in the Spatial Domain
A continuous image is sampled and quantized into an $M \times N$ matrix of discrete spatial coordinates:
$$f(x, y) = \begin{bmatrix} f(0,0) & f(0,1) & \cdots & f(0, N-1) \\ f(1,0) & f(1,1) & \cdots & f(1, N-1) \\ \vdots & \vdots & \ddots & \vdots \\ f(M-1,0) & f(M-1,1) & \cdots & f(M-1, N-1) \end{bmatrix}$$
In true-color 24-bit imagery, each coordinate $(x, y)$ consists of three color channels:
$$f(x, y) = \{R(x, y), G(x, y), B(x, y)\}, \quad \text{where } R, G, B \in [0, 255]$$

### 6.2 Bit-Plane Decomposition & LSB Substitution
Every 8-bit quantized intensity byte can be decomposed into eight binary planes:
$$P = \sum_{b=0}^{7} a_b \cdot 2^b = a_7 2^7 + a_6 2^6 + \cdots + a_1 2^1 + a_0 2^0$$
- **Most Significant Bits (MSBs, $b_7 - b_5$):** Dominate visual energy, luminance contrast, and scene semantics.
- **Least Significant Bits (LSBs, $b_0$):** Govern microscopic variations. Replacing $b_0$ modifies the pixel intensity by at most $\pm 1$ on an 8-bit scale ($0.39\%$ relative delta), remaining beneath the contrast sensitivity threshold of the Human Visual System ($\text{HVS}$).
- Bitwise substitution function:
$$\text{setlsb}(c, m) = (c \ \& \ \sim 1) \ | \ m, \quad m \in \{0, 1\}$$

### 6.3 Image Histogram Analysis & Histogram Shifting
An image histogram $h(r_k) = n_k$ tabulates the occurrence frequency of each intensity level $r_k \in [0, 255]$. 
- In **Reversible Data Hiding (RDH)**, the histogram is evaluated to locate:
  - **Peak Bin ($p$):** The most frequent intensity value in the payload region.
  - **Zero Bin ($z$):** An unpopulated intensity value closest to $p$.
- Shifting intermediate bins between $p$ and $z$ opens an empty bin adjacent to $p$, allowing payload bits to be embedded losslessly.

### 6.4 Objective Image Distortion Metrics ($\text{MSE}$ and $\text{PSNR}$)
To evaluate spatial degradation caused by data embedding, the studio calculates:
- **Mean Squared Error ($\text{MSE}$):**
$$\text{MSE} = \frac{1}{M \cdot N \cdot C} \sum_{x=0}^{M-1} \sum_{y=0}^{N-1} \sum_{c=0}^{C-1} \left[ I_{\text{cover}}(x, y, c) - I_{\text{stego}}(x, y, c) \right]^2$$
- **Peak Signal-to-Noise Ratio ($\text{PSNR}$):**
$$\text{PSNR} = 10 \cdot \log_{10}\left(\frac{\text{MAX}_I^2}{\text{MSE}}\right) = 20 \cdot \log_{10}\left(\frac{255}{\sqrt{\text{MSE}}}\right) \quad (\text{dB})$$
When images are identical ($\text{MSE} = 0$), $\text{PSNR} = \infty\text{ dB}$. Typical steganographic embeddings maintain $\text{PSNR} > 50\text{ dB}$, confirming high visual fidelity.

---

## 7. Steganography Techniques | تقنيات إخفاء البيانات

The studio integrates three distinct information hiding methodologies:

### 7.1 Least Significant Bit (LSB) Steganography
- **Carrier Compatibility:** Lossless $\text{RGB}$ and $\text{RGBA}$ PNG images.
- **Principle:** Modulates the least significant bit of each color component ($R$, $G$, $B$) sequentially or via mathematical generators.
- **Encoding Structure:** Length prefix $\langle\text{len}\rangle\text{:}$ encoded in ASCII, followed by the payload bits in $\text{UTF-8}$ or $\text{UTF-32LE}$.
- **Generators Available:**
  - `identity()`: Sequential raster traversal ($0, 1, 2, \dots$).
  - `fibonacci()`: Pixel indices chosen from Fibonacci numbers ($1, 2, 3, 5, 8, 13, \dots$).
  - `eratosthenes()`: Prime coordinate dispersion via the Sieve of Eratosthenes ($2, 3, 5, 7, 11, \dots$).
  - `mersenne()`: Mersenne primes ($2^p - 1$).
  - `triangular_numbers()`: Triangular sequence indices ($\frac{n(n+1)}{2}$).
  - `fermat()`: Fermat sequence indices ($2^{2^n} + 1$).
  - `composite()` / `carmichael()`: Higher-order composite and pseudo-prime sequences.

### 7.2 Reversible Data Hiding (RDH via Histogram Shifting)
- **Carrier Compatibility:** $\text{L}$ (Grayscale), $\text{RGB}$, and $\text{RGBA}$ PNG images.
- **Algorithm:** Z. Ni, Y.-Q. Shi, N. Ansari, and W. Su, *"Reversible data hiding,"* IEEE CSVT, 2006.
- **Reversibility Guarantee:** Unlike classical LSB methods, RDH permits the exact pixel-for-pixel recovery of the original cover carrier ($\Delta = 0$, $\text{MSE} = 0.0$, $\text{PSNR} = \infty$).
- **Workflow:** 
  1. Computes the intensity histogram and extracts peak $p$ and zero $z$.
  2. Embeds payload bits into shifted bins.
  3. Extraction reverses the shift, fully reconstructing the cover image.

### 7.3 Red-Channel Steganography
- **Carrier Compatibility:** $\text{RGB}$ 24-bit images.
- **Principle:** Embeds ASCII character byte values directly into the Red channel component of successive pixels.
- **Capacity:** Specialized for compact ASCII messages ($\le 254$ characters). Displays a translated validation warning if Arabic or Unicode text is entered.

---

## 8. Application Navigation & Workspaces | أقسام التطبيق

The application features three streamlined main sections:

### Section 1: Hide Message — إخفاء رسالة
1. **Original Image Upload:** Drag and drop any cover image with real-time resolution and capacity indicators.
2. **Secret Message Input:** Enter Arabic or English payload with a live character/byte counter.
3. **Hide Message Action:** Click the prominent Maroon action button.
4. **Instant Results Workspace:** Reveals upon processing with a green success banner, generated preview, prominent **Download Stego Image (.PNG)** button, interactive Before/After comparison slider, difference map, and compact metrics.

### Section 2: Reveal Message — استخراج الرسالة
1. **Hidden-Message Image Upload:** Ingest the stego image.
2. **Reveal Message Action:** Extract hidden payloads in one click.
3. **Extracted Message Card:** Displays only upon extraction with a one-click **Copy Message** button and toast feedback.
4. **Reversible Cover Recovery (RDH):** Optional one-click pristine cover reconstruction with mathematical zero-error confirmation.

### Section 3: Advanced Tools — أدوات التحليل (4 Compact Sub-Tools)
1. **Image Comparison (مقارنة الصور):** Quantitatively evaluate PSNR, MSE, RMSE, and spatial difference heatmaps between any two images.
2. **Bit Analysis (تحليل البتات):** Isolate the binary LSB bit-plane to inspect visual entropy and detect steganographic tampering.
3. **Image Recovery (استرجاع الصورة):** Dedicated standalone workbench for Ni et al. histogram-shifting cover reconstruction.
4. **About & Theory (حول المشروع):** In-depth academic documentation, DIP theory, mathematical formulas, and open-source attribution.

---

## 9. Installation and Setup Options | خيارات التثبيت والتشغيل

### Option A: One-Command Online Installer (Recommended)
Open PowerShell and run:
```powershell
irm https://raw.githubusercontent.com/xdc7-css/Hypocritical-Saint/main/setup.ps1 | iex
```

### Option B: System-Wide Global Command
If already installed, run from any terminal prompt:
```cmd
PROJECT RUN
```

### Option C: One-Click Local Launcher
Double-click **`RUN.bat`** in the project installation directory (`D:\Hypocritical-Saint\RUN.bat`). It activates the virtual environment, verifies dependencies, and automatically launches the studio in your browser.

### Option D: Manual Command Line Execution
```cmd
cd /d D:\Hypocritical-Saint
call .venv\Scripts\activate.bat
python app.py
```
Open your browser to:
```
http://127.0.0.1:7860
```

### Running the Automated Unit Test Suite
To run the full suite of unit tests:
```cmd
cd /d D:\Hypocritical-Saint
call .venv\Scripts\activate.bat
python -m unittest discover
```
*All 73 unit tests pass with 100% success.*

---

## 10. Project Structure | هيكلية المشروع

```text
Hypocritical-Saint\  (Default: D:\Hypocritical-Saint\)
│
├── setup.ps1                   # One-Command Windows Setup & Automated Installer
├── PROJECT.cmd                 # Global CLI Launcher (PROJECT RUN / STATUS / HELP)
├── RUN.bat                     # Windows Automated One-Click Local Launcher
├── app.py                      # HYPOCRITICAL SAINT - Main Maroon Bilingual Studio
├── pyproject.toml              # Project configuration and dependency definitions
├── requirements.txt            # Pinned requirements for pip installations
├── poetry.lock                 # Poetry dependency lockfile
├── README.md                   # Academic project documentation
├── CHANGELOG.md                # Stegano library version changelog
├── COPYING                     # GNU General Public License v3.0 text
│
├── outputs/                    # Output directory for saved stego and restored PNG files
│   └── .gitkeep
│
├── stegano/                    # Core Stegano 3.0 Python Module
│   ├── __init__.py             # Package exports (lsb, rdh, red, exifHeader, steganalysis)
│   ├── tools.py                # Bitwise manipulations, Hider and Revealer classes
│   ├── lsb/                    # Least Significant Bit implementation
│   ├── rdh/                    # Reversible Data Hiding (Histogram Shifting)
│   ├── red/                    # Red-channel steganography
│   ├── steganalysis/           # Parity and statistical analysis
│   ├── exifHeader/             # EXIF metadata steganography
│   └── wav/                    # PCM audio steganography
│
└── tests/                      # Unit test suite and sample imagery (73 passing tests)
```

---

## 11. Original Open-Source Credits | حقوق الملكية الفكرية

- **Academic Application & Studio Author:**  
  **Um Al-Baneen Awwad (أم البنين عواد)**  
  Department of Computer Engineering, College of Engineering, University of Basrah (2026–2027).  
  *Designed and developed the unified graphical studio, bilingual Arabic/English architecture, DIP integration, PSNR evaluation suite, difference visualizer, academic documentation, and launcher.*

- **Underlying Steganography Library Author:**  
  **Cédric Bonhomme** and contributors ([https://github.com/cedricbonhomme/Stegano](https://github.com/cedricbonhomme/Stegano)).  
  *Original authors and maintainers of the underlying Stegano Python module under GNU GPL-3.0.*

- **RDH Algorithm Reference:**  
  Z. Ni, Y.-Q. Shi, N. Ansari, and W. Su, *"Reversible data hiding,"* IEEE Transactions on Circuits and Systems for Video Technology, vol. 16, no. 3, pp. 354–362, 2006.

---

## 12. License Information | معلومات الترخيص

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)** in compliance with the original Stegano library license.

See the `COPYING` file for full license terms.
