r"""
HYPOCRITICAL SAINT
Digital Image Steganography Studio
"Innocent on the Outside. Secret on the Inside."
"بريء في الظاهر.. وسرّي في الباطن"

Academic Digital Image Processing Application
Developed by: Um Al-Baneen Awwad (أم البنين عواد)
Department of Computer Engineering, College of Engineering, University of Basrah (2026–2027)
Course: Digital Image Processing (DIP)
Core Engine: Stegano 3.0 (Cédric Bonhomme & contributors) under GNU GPL-3.0.
"""

import base64
import os
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Optional, Tuple

import cv2
import gradio as gr
import numpy as np
from PIL import Image

import stegano
from stegano import lsb, rdh, red
from stegano.lsb import generators
from stegano.steganalysis import parity

# Ensure outputs directory exists
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Sample reference file
SAMPLES_DIR = Path(__file__).resolve().parent / "tests" / "sample-files"
SAMPLE_LENNA = str(SAMPLES_DIR / "Lenna.png") if (SAMPLES_DIR / "Lenna.png").exists() else None


# ==============================================================================
# Centralized Translation Dictionary (Arabic-First & English)
# ==============================================================================

TRANSLATIONS = {
    "ar": {
        "app_title": "HYPOCRITICAL SAINT",
        "app_subtitle": "استوديو إخفاء البيانات في الصور الرقمية",
        "app_tagline": "بريء في الظاهر.. وسرّي في الباطن",
        "arabic_badge": "يدعم إخفاء واستخراج الرسائل باللغة العربية",
        "btn_about": "ℹ️ حول المشروع",
        "btn_close": "✕ إغلاق",
        "about_title": "حول مشروع HYPOCRITICAL SAINT",
        "about_subtitle": "استوديو أكاديمي لإخفاء واسترجاع البيانات في الصور الرقمية",
        "about_dev_title": "إعداد وتطوير",
        "about_dev_val": "أم البنين عواد (Um Al-Baneen Awwad)",
        "about_dev_sub": "المرحلة الرابعة — قسم هندسة الحاسوب (2026–2027)",
        "about_inst_title": "المؤسسة والمادة",
        "about_inst_val": "جامعة البصرة — كلية الهندسة",
        "about_inst_sub": "مادة معالجة الصور الرقمية (Digital Image Processing)",
        "about_lang_title": "دعم اللغة العربية واليونيكود",
        "about_lang_val": "دعم كامل للغة العربية UTF-8 و UTF-32LE في خوارزميات LSB و RDH مع استرجاع كامل 100% بدون أي تشويه.",
        "about_engine_title": "المحرك البرمجي والحقوق",
        "about_engine_val": "مبني استناداً إلى مكتبة Stegano 3.0 المفتوحة المصدر (Cédric Bonhomme ومساهمون)",
        "about_engine_sub": "مرخص تحت رخصة جنو العمومية (GNU General Public License v3.0)",
        
        # Tabs
        "tab_hide": "إخفاء رسالة",
        "tab_reveal": "استخراج الرسالة",
        "tab_adv": "أدوات التحليل",
        
        # Hide Message Tab
        "cover_title": "الصورة الأصلية",
        "cover_upload_label": "اختر أو اسحب صورة الغلاف (PNG, JPG, BMP)",
        "sample_label": "صورة نموذجية مرجعية (Lenna.png)",
        "msg_title": "إخفاء رسالة سرية",
        "msg_input_label": "نص الرسالة السرية",
        "msg_placeholder": "اكتب أو الصق نص الرسالة السرية هنا (يدعم اللغة العربية والأحرف الخاصة)...",
        "payload_len_label": "طول الرسالة:",
        "chars_label": "حرفاً",
        "bytes_label": "بايت",
        "adv_settings": "إعدادات متقدمة",
        "method_label": "خوارزمية الإخفاء",
        "gen_label": "تسلسل توزيع البكسلات",
        "gen_info": "توزيع البكسلات وفق متتاليات رياضية لمقاومة الفحص الإحصائي المتسلسل.",
        "shift_label": "إزاحة نقطة البداية (Shift)",
        "shift_info": "تخطي عدد معين من البكسلات قبل بدء الإخفاء.",
        "btn_calc_rdh": "حساب سعة الاستيعاب (RDH)",
        "red_info": "خوارزمية القناة الحمراء تدعم أحرف ASCII الإنجليزية فقط (بحد أقصى 254 حرفاً).",
        "enc_label": "ترميز المحارف",
        "btn_hide": "إخفاء الرسالة داخل الصورة",
        
        # Hide Results
        "stego_preview_title": "معاينة الصورة الناتجة (الحاملة للرسالة)",
        "stego_preview_label": "الصورة الناتجة",
        "actions_title": "تنزيل الصورة والإجراءات",
        "btn_download_primary": "📥 تنزيل الصورة الناتجة (.PNG)",
        "btn_download_file": "ملف PNG مباشر بدون أي فقدان",
        "btn_forward_reveal": "الانتقال لاستخراج الرسالة ←",
        "btn_hide_another": "إخفاء رسالة جديدة",
        "slider_title": "مقارنة الصورة الأصلية مع الصورة المعدّلة",
        "diff_map_label": "خريطة الاختلافات (توهج وإطار تحديد البكسلات المعدّلة)",
        "tech_metrics_title": "التحليل العلمي وتفاصيل جودة الصورة",
        "zoom_panel_title": "تكبير منطقة التغيّر",
        "zoom_panel_sub": "المربع يحدد مكان البكسلات المتغيرة",
        "zoom_orig_label": "الصورة الأصلية (مكبرة)",
        "zoom_mod_label": "الصورة المعدّلة (مكبرة)",
        "zoom_diff_label": "خريطة الفروق (مكبرة)",
        "select_region_label": "تحديد منطقة التغيّر للمعاينة المجهرية",
        
        # Reveal Message Tab
        "stego_upload_title": "الصورة المخفية",
        "stego_upload_label": "اختر أو اسحب الصورة الحاملة للرسالة",
        "btn_reveal": "استخراج الرسالة",
        "extracted_title": "الرسالة السرية المستخرجة",
        "extracted_placeholder": "ستظهر الرسالة المستخرجة هنا فور انتهاء الفحص...",
        "btn_copy": "📋 نسخ الرسالة",
        "copied_toast": "✓ تم نسخ الرسالة بنجاح!",
        "initial_reveal_hint": "ارفع الصورة واضغط على زر 'استخراج الرسالة' للبدء.",
        "rdh_restore_title": "استرجاع الصورة الأصلية (RDH بدون أي تشويه)",
        "rdh_restore_sub": "الصورة مشفرة بخوارزمية الإخفاء العكسي. يمكنك استرجاع صورة الغلاف الأصلية مطابقة بنسبة 100%.",
        "rdh_ref_label": "الصورة الأصلية للمطابقة (اختياري للتحقق الرياضي)",
        "btn_rdh_restore": "استرجاع الصورة الأصلية",
        "rdh_preview_label": "معاينة الصورة المسترجعة",
        "btn_download_restored": "📥 تنزيل الصورة المسترجعة (.PNG)",
        
        # Advanced Tools Subtabs
        "subtab_compare": "مقارنة الصور",
        "subtab_compare_intro": "تقييم الفروق الإدراكية والرياضية (PSNR و MSE) بين الصورة الأصلية والصورة المعدّلة.",
        "subtab_bit": "تحليل البتات",
        "subtab_bit_intro": "عزل مستوى البت الأقل أهمية (LSB) لاكتشاف الأنماط والتعديلات الخوارزمية في الصورة.",
        "subtab_recovery": "استرجاع الصورة",
        "subtab_recovery_intro": "منصة متخصصة لاسترجاع الصور الأصلية المشفرة بنظام إزاحة المدرج التكراري (Ni et al., 2006).",
        "subtab_about": "حول المشروع",
        
        # Compare tool
        "cmp_orig_label": "الصورة الأصلية",
        "cmp_mod_label": "الصورة المعدّلة",
        "btn_compare": "حساب الفروق وجودة الصورة",
        "cmp_diff_label": "خريطة الاختلافات (توهج وإطار تحديد البكسلات المعدّلة)",
        
        # Bit analysis tool
        "bit_input_label": "الصورة المراد فحصها",
        "btn_bit_exec": "بدء تحليل البتات",
        "bit_output_label": "خريطة بتات LSB المعزولة",
        
        # Recovery tool
        "rec_stego_label": "الصورة المشفرة بخوارزمية RDH",
        "rec_ref_label": "الصورة الأصلية للتحقق الرياضي (اختياري)",
        "btn_rec_exec": "استرجاع الصورة الأصلية واستخراج النص",
        "rec_msg_label": "الرسالة السرية المستخرجة",
        "rec_preview_label": "معاينة الصورة المسترجعة",
        
        # Footer
        "footer_text": "HYPOCRITICAL SAINT • استوديو إخفاء البيانات في الصور الرقمية<br>قسم هندسة الحاسوب • كلية الهندسة • جامعة البصرة (2026–2027)<br>إعداد الطالبة: أم البنين عواد • بإشراف مادة معالجة الصور الرقمية",
    },
    "en": {
        "app_title": "HYPOCRITICAL SAINT",
        "app_subtitle": "Digital Image Steganography Studio",
        "app_tagline": "Innocent on the Outside. Secret on the Inside.",
        "arabic_badge": "Supports Arabic and English hidden messages",
        "btn_about": "ℹ️ About",
        "btn_close": "✕ Close",
        "about_title": "About HYPOCRITICAL SAINT Studio",
        "about_subtitle": "Academic Digital Image Steganography Studio",
        "about_dev_title": "Developer",
        "about_dev_val": "Um Al-Baneen Awwad (أم البنين عواد)",
        "about_dev_sub": "Fourth-Year Computer Engineering (2026–2027)",
        "about_inst_title": "Institution & Course",
        "about_inst_val": "University of Basrah — College of Engineering",
        "about_inst_sub": "Department of Computer Engineering • Digital Image Processing",
        "about_lang_title": "Arabic & Unicode Support",
        "about_lang_val": "Native support for Arabic UTF-8 and UTF-32LE across LSB and RDH algorithms with 100% lossless extraction.",
        "about_engine_title": "Core Engine & License",
        "about_engine_val": "Powered by open-source Stegano 3.0 (Cédric Bonhomme & contributors)",
        "about_engine_sub": "Released under GNU General Public License v3.0 (GPL-3.0)",
        
        # Tabs
        "tab_hide": "Hide Message",
        "tab_reveal": "Reveal Message",
        "tab_adv": "Advanced Tools",
        
        # Hide Message Tab
        "cover_title": "Original Image",
        "cover_upload_label": "Upload Original Image (PNG, JPG, BMP)",
        "sample_label": "Reference Sample Cover (Lenna.png)",
        "msg_title": "Hide a Secret Message",
        "msg_input_label": "Secret Message Payload",
        "msg_placeholder": "Type or paste confidential payload here (Arabic & Unicode supported)...",
        "payload_len_label": "Payload Length:",
        "chars_label": "characters",
        "bytes_label": "bytes",
        "adv_settings": "Advanced Settings",
        "method_label": "Steganography Algorithm",
        "gen_label": "Coordinate Generator Sequence",
        "gen_info": "Traverses pixels non-linearly to resist sequential steganalysis.",
        "shift_label": "Spatial Offset (Shift)",
        "shift_info": "Iterations to skip before embedding starts.",
        "btn_calc_rdh": "Calculate RDH Capacity",
        "red_info": "Red Channel encodes ASCII characters into red components (max 254 chars).",
        "enc_label": "Encoding Format",
        "btn_hide": "Hide Message in Image",
        
        # Hide Results
        "stego_preview_title": "Generated Modified Image Preview",
        "stego_preview_label": "Modified Image Output",
        "actions_title": "Artifact Download & Actions",
        "btn_download_primary": "📥 Download Stego Image (.PNG)",
        "btn_download_file": "Direct Lossless PNG File",
        "btn_forward_reveal": "Forward to Reveal Message →",
        "btn_hide_another": "Conceal Another Message",
        "slider_title": "Original vs. Modified Image Comparison",
        "diff_map_label": "Difference Map (Glow & Highlight Box on Changed Pixels)",
        "tech_metrics_title": "Detailed Image Quality & Technical Metrics",
        "zoom_panel_title": "Zoomed Change Region",
        "zoom_panel_sub": "Box marks the changed pixels",
        "zoom_orig_label": "Original Image (Zoomed)",
        "zoom_mod_label": "Modified Image (Zoomed)",
        "zoom_diff_label": "Difference Map (Zoomed)",
        "select_region_label": "Select Change Region to Inspect",
        
        # Reveal Message Tab
        "stego_upload_title": "Hidden-Message Image",
        "stego_upload_label": "Upload Hidden-Message Image",
        "btn_reveal": "Reveal Message",
        "extracted_title": "Extracted Secret Message",
        "extracted_placeholder": "Extracted confidential message will appear here...",
        "btn_copy": "📋 Copy Message",
        "copied_toast": "✓ Copied to clipboard!",
        "initial_reveal_hint": "Upload a stego image and click Reveal Message to extract payload.",
        "rdh_restore_title": "Restore Original Image (Lossless RDH)",
        "rdh_restore_sub": "This carrier uses Reversible Data Hiding. You can recover the original cover image with zero distortion.",
        "rdh_ref_label": "Original Reference Cover (Optional verification)",
        "btn_rdh_restore": "Restore Original Image",
        "rdh_preview_label": "Restored Cover Preview",
        "btn_download_restored": "📥 Download Restored Cover (.PNG)",
        
        # Advanced Tools Subtabs
        "subtab_compare": "Image Comparison",
        "subtab_compare_intro": "Quantitatively evaluate perceptual and mathematical differences (PSNR & MSE) between original and modified images.",
        "subtab_bit": "Bit Analysis",
        "subtab_bit_intro": "Isolate the least-significant-bit plane to detect visual anomalies and steganographic patterns.",
        "subtab_recovery": "Image Recovery",
        "subtab_recovery_intro": "Dedicated workbench for lossless cover recovery via histogram shifting (Ni et al., 2006).",
        "subtab_about": "About & Theory",
        
        # Compare tool
        "cmp_orig_label": "Original Image",
        "cmp_mod_label": "Modified Image",
        "btn_compare": "Calculate Quality & Differences",
        "cmp_diff_label": "Difference Map (Glow & Highlight Box on Changed Pixels)",
        
        # Bit analysis tool
        "bit_input_label": "Image to Inspect",
        "btn_bit_exec": "Run Bit Analysis",
        "bit_output_label": "Isolated LSB Parity Map",
        
        # Recovery tool
        "rec_stego_label": "RDH Stego Image",
        "rec_ref_label": "Original Reference Image (Optional)",
        "btn_rec_exec": "Restore Cover & Extract Message",
        "rec_msg_label": "Extracted Secret Message",
        "rec_preview_label": "Restored Cover Preview",
        
        # Footer
        "footer_text": "HYPOCRITICAL SAINT • Digital Image Steganography Studio<br>Department of Computer Engineering • College of Engineering • University of Basrah (2026–2027)<br>Developed by: Um Al-Baneen Awwad • Digital Image Processing Course",
    }
}

# Method & Generator choices mapping
METHODS_AR = [
    "LSB (تعديل البت الأقل أهمية)",
    "RDH (الإخفاء العكسي)",
    "القناة الحمراء (ASCII فقط)",
]
METHODS_EN = [
    "LSB (Least Significant Bit)",
    "RDH (Reversible Data Hiding)",
    "Red Channel (ASCII Only)",
]

GENERATORS_AR = [
    "تسلسل خطي منتظم (Sequential)",
    "متتالية فيبوناتشي (Fibonacci)",
    "مصفاة إراتوستينس (Primes)",
    "أعداد ميرسين الأولية (Mersenne)",
    "الأعداد المثلثية (Triangular)",
    "أعداد فيرما (Fermat)",
    "الأعداد المركبة (Composite)",
    "أعداد كارمايكل (Carmichael)",
]
GENERATORS_EN = [
    "Sequential (Identity)",
    "Fibonacci Sequence",
    "Eratosthenes (Primes)",
    "Mersenne Primes",
    "Triangular Numbers",
    "Fermat Numbers",
    "Composite Numbers",
    "Carmichael Numbers",
]

def t(key: str, lang: str = "ar") -> str:
    """Lookup translation helper."""
    return TRANSLATIONS.get(lang, TRANSLATIONS["ar"]).get(key, key)


def normalize_method(method: str) -> str:
    """Normalize any localized or English method name."""
    if not method:
        return "LSB"
    m = method.lower()
    if "rdh" in m or "عكسي" in m:
        return "RDH"
    elif "red" in m or "حمراء" in m:
        return "RED"
    return "LSB"


def get_generator_by_name(name: str):
    """Normalize generator name across Arabic and English choices."""
    if not name:
        return generators.identity()
    n = name.lower()
    if "fibonacci" in n or "فيبوناتشي" in n:
        return generators.fibonacci()
    elif "eratosthenes" in n or "إراتوستينس" in n or "primes" in n or "أولية" in n:
        return generators.eratosthenes()
    elif "mersenne" in n or "ميرسين" in n:
        return generators.mersenne()
    elif "triangular" in n or "مثلثية" in n:
        return generators.triangular_numbers()
    elif "fermat" in n or "فيرما" in n:
        return generators.fermat()
    elif "composite" in n or "مركبة" in n:
        return generators.composite()
    elif "carmichael" in n or "كارمايكل" in n:
        return generators.carmichael()
    return generators.identity()


# ==============================================================================
# Helper Functions (PIL, Base64, Comparison Slider, Metrics)
# ==============================================================================

def pil_to_base64(img: Image.Image, format="PNG") -> str:
    """Convert a PIL Image to base64 encoded data URI with downscaling for snappy rendering."""
    buf = BytesIO()
    w, h = img.size
    max_dim = 800
    if max(w, h) > max_dim:
        scale = max_dim / max(w, h)
        preview_img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
    else:
        preview_img = img
    preview_img.save(buf, format=format)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def generate_comparison_slider_html(cover_img: Image.Image, stego_img: Image.Image, lang: str = "ar") -> str:
    """Interactive Before/After comparison slider in pure CSS/JS with Maroon x Soft Ivory styling."""
    cover_b64 = pil_to_base64(cover_img)
    stego_b64 = pil_to_base64(stego_img)

    tag_cover = "الصورة الأصلية" if lang == "ar" else "Original Image"
    tag_stego = "الصورة المعدّلة" if lang == "ar" else "Modified Image"
    caption_text = (
        "حرّك المؤشر لمقارنة الصورة الأصلية مع الصورة المعدّلة"
        if lang == "ar"
        else "Slide to compare original cover vs. modified image"
    )
    caption_hint = (
        "تعديل البتات الدنيا يحافظ على جودة الصورة بدون أي تشويه بصري"
        if lang == "ar"
        else "Sub-visual bit modifications maintain complete visual fidelity"
    )

    return f"""
    <div class="hs-slider-container" style="--slider-pos: 50%;">
        <div class="hs-slider-viewport">
            <img src="data:image/png;base64,{cover_b64}" class="hs-layer-cover" alt="{tag_cover}" />
            <div class="hs-layer-stego-wrap">
                <img src="data:image/png;base64,{stego_b64}" class="hs-layer-stego" alt="{tag_stego}" />
            </div>
            <div class="hs-slider-divider"></div>
            <input type="range" min="0" max="100" value="50" class="hs-slider-input" 
                oninput="this.closest('.hs-slider-container').style.setProperty('--slider-pos', this.value + '%')" />
            <div class="hs-tag-cover">{tag_cover}</div>
            <div class="hs-tag-stego">{tag_stego}</div>
        </div>
        <div class="hs-slider-caption">
            <span>{caption_text}</span>
            <span class="hs-slider-hint">{caption_hint}</span>
        </div>
    </div>
    """


def detect_change_clusters(diff_mask: np.ndarray, max_clusters: int = 6) -> list:
    """
    Detect spatial clusters of modified pixels and return their bounding boxes.
    Returns list of dicts: [{'id': 1, 'x': x, 'y': y, 'w': w, 'h': h, 'pixel_count': n, 'center': (cx, cy)}, ...]
    """
    if not np.any(diff_mask):
        return []
    
    H, W = diff_mask.shape
    # Dilation kernel to bridge nearby modified pixels into cohesive clusters
    bridge_k = max(7, int(min(H, W) * 0.02) | 1)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (bridge_k, bridge_k))
    dilated = cv2.dilate(diff_mask.astype(np.uint8), kernel, iterations=1)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    clusters = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        sub_mask = diff_mask[y:y+h, x:x+w]
        count = int(np.sum(sub_mask))
        if count > 0:
            clusters.append({
                "x": int(x),
                "y": int(y),
                "w": int(w),
                "h": int(h),
                "pixel_count": count,
                "center": (int(x + w // 2), int(y + h // 2))
            })
            
    # Sort clusters by pixel count in descending order
    clusters.sort(key=lambda c: c["pixel_count"], reverse=True)
    for i, c in enumerate(clusters[:max_clusters]):
        c["id"] = i + 1
        
    return clusters[:max_clusters]


def draw_bounding_boxes(
    canvas_rgb: np.ndarray,
    clusters: list,
    box_color: tuple = (255, 215, 65),  # Vivid Amber Gold
    thickness: int = 2
) -> np.ndarray:
    """Draw high-contrast multi-stroke bounding boxes and corner reticles around change clusters."""
    out = canvas_rgb.copy()
    H, W, _ = out.shape
    
    for c in clusters:
        x, y, w, h = c["x"], c["y"], c["w"], c["h"]
        pad = max(6, int(min(H, W) * 0.012))
        x0 = max(0, x - pad)
        y0 = max(0, y - pad)
        x1 = min(W - 1, x + w + pad)
        y1 = min(H - 1, y + h + pad)
        
        # 1. Outer 1px black outline for contrast against bright scenes
        cv2.rectangle(out, (max(0, x0 - 1), max(0, y0 - 1)), (min(W - 1, x1 + 1), min(H - 1, y1 + 1)), (0, 0, 0), 1)
        # 2. Middle vivid color stroke
        cv2.rectangle(out, (x0, y0), (x1, y1), box_color, thickness)
        # 3. Inner 1px black outline for contrast against dark scenes
        if (x1 - x0) > 4 and (y1 - y0) > 4:
            cv2.rectangle(out, (x0 + thickness, y0 + thickness), (x1 - thickness, y1 - thickness), (0, 0, 0), 1)
            
        # 4. Corner reticles (viewfinder crosshair brackets)
        reticle_len = max(6, min(16, int(min(w, h) * 0.35)))
        cv2.line(out, (max(0, x0 - 3), y0), (x0 + reticle_len, y0), (255, 255, 255), 1)
        cv2.line(out, (x0, max(0, y0 - 3)), (x0, y0 + reticle_len), (255, 255, 255), 1)
        cv2.line(out, (x1 - reticle_len, y0), (min(W - 1, x1 + 3), y0), (255, 255, 255), 1)
        cv2.line(out, (x1, max(0, y0 - 3)), (x1, y0 + reticle_len), (255, 255, 255), 1)
        cv2.line(out, (max(0, x0 - 3), y1), (x0 + reticle_len, y1), (255, 255, 255), 1)
        cv2.line(out, (x0, y1 - reticle_len), (x0, min(H - 1, y1 + 3)), (255, 255, 255), 1)
        cv2.line(out, (x1 - reticle_len, y1), (min(W - 1, x1 + 3), y1), (255, 255, 255), 1)
        cv2.line(out, (x1, y1 - reticle_len), (x1, min(H - 1, y1 + 3)), (255, 255, 255), 1)
        
        # 5. Region identification label pill
        label_text = f"Region {c['id']}" if len(clusters) > 1 else "Modified Area"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.36
        (tw, th), _ = cv2.getTextSize(label_text, font, font_scale, 1)
        tag_y0 = max(0, y0 - th - 6)
        tag_y1 = y0
        tag_x0 = x0
        tag_x1 = min(W - 1, x0 + tw + 8)
        
        cv2.rectangle(out, (tag_x0, tag_y0), (tag_x1, tag_y1), (20, 18, 22), -1)
        cv2.rectangle(out, (tag_x0, tag_y0), (tag_x1, tag_y1), box_color, 1)
        cv2.putText(out, label_text, (tag_x0 + 4, tag_y1 - 4), font, font_scale, (255, 245, 230), 1, cv2.LINE_AA)
        
    return out


def generate_enhanced_diff_map(
    rgb1: np.ndarray,
    diff_mask: np.ndarray,
    clusters: list,
    lang: str = "ar"
) -> Image.Image:
    """Generate high-contrast amplified difference map with glowing pixels and highlight boxes."""
    H, W, _ = rgb1.shape
    
    # Dark monochrome silhouette of cover image for spatial orientation
    gray = np.mean(rgb1[:, :, :3], axis=-1, keepdims=True) * 0.15
    vis = np.clip(gray, 10, 235).astype(np.uint8)
    vis = np.repeat(vis, 3, axis=-1)
    
    if np.any(diff_mask):
        # Visual dilation to create a luminous glowing aura around tiny 1-pixel changes
        glow_k_size = max(3, min(7, int(min(H, W) * 0.008) * 2 + 1))
        glow_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (glow_k_size, glow_k_size))
        glow_mask = cv2.dilate(diff_mask.astype(np.uint8), glow_kernel, iterations=1)
        
        # Outer halo glow: Warm Crimson Maroon
        vis[glow_mask > 0] = [215, 65, 95]
        # Core modified pixels: Vivid Neon Gold / Amber
        vis[diff_mask] = [255, 235, 75]
        
        # Draw high-contrast bounding boxes around detected clusters
        vis = draw_bounding_boxes(vis, clusters, box_color=(255, 215, 65), thickness=2)
        
    return Image.fromarray(vis)


def generate_zoomed_views(
    rgb1: np.ndarray,
    rgb2: np.ndarray,
    diff_mask: np.ndarray,
    cluster: Optional[dict],
    target_dim: int = 360
):
    """
    Generate enlarged, magnified crops of original, modified, and difference regions.
    Uses Nearest-Neighbor interpolation with pixel gridlines so individual modified pixels are obvious.
    """
    if cluster is None or not np.any(diff_mask):
        return None, None, None, None
        
    H, W, _ = rgb1.shape
    x, y, w, h = cluster["x"], cluster["y"], cluster["w"], cluster["h"]
    cx, cy = cluster["center"]
    
    # Calculate square crop window to provide surrounding context
    crop_dim = max(w + 16, h + 16, 24)
    crop_dim = min(crop_dim, 120, H, W)
    half = crop_dim // 2
    
    x0 = max(0, min(W - crop_dim, cx - half))
    y0 = max(0, min(H - crop_dim, cy - half))
    x1 = min(W, x0 + crop_dim)
    y1 = min(H, y0 + crop_dim)
    
    # Ensure uint8 image arrays for PIL conversion
    u8_1 = np.asarray(rgb1, dtype=np.uint8)
    u8_2 = np.asarray(rgb2, dtype=np.uint8)
    crop_orig = u8_1[y0:y1, x0:x1]
    crop_mod = u8_2[y0:y1, x0:x1]
    
    # Crop difference
    local_diff = diff_mask[y0:y1, x0:x1]
    crop_diff_base = np.zeros_like(crop_orig)
    gray_local = np.mean(crop_orig[:, :, :3], axis=-1, keepdims=True) * 0.16
    crop_diff_base[:, :] = np.clip(gray_local, 8, 230).astype(np.uint8)
    
    if np.any(local_diff):
        local_k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        local_glow = cv2.dilate(local_diff.astype(np.uint8), local_k, iterations=1)
        crop_diff_base[local_glow > 0] = [215, 65, 95]
        crop_diff_base[local_diff] = [255, 235, 75]
        
    # Nearest-Neighbor Magnification (preserves crisp square pixel blocks)
    zoom_orig = cv2.resize(crop_orig, (target_dim, target_dim), interpolation=cv2.INTER_NEAREST)
    zoom_mod = cv2.resize(crop_mod, (target_dim, target_dim), interpolation=cv2.INTER_NEAREST)
    zoom_diff = cv2.resize(crop_diff_base, (target_dim, target_dim), interpolation=cv2.INTER_NEAREST)
    
    # Overlay subtle pixel grid if magnification factor is >= 6
    scale_factor = target_dim / crop_dim
    if scale_factor >= 6.0:
        step = int(scale_factor)
        grid_color = (35, 30, 38)
        for i in range(step, target_dim, step):
            cv2.line(zoom_orig, (i, 0), (i, target_dim), grid_color, 1)
            cv2.line(zoom_orig, (0, i), (target_dim, i), grid_color, 1)
            cv2.line(zoom_mod, (i, 0), (i, target_dim), grid_color, 1)
            cv2.line(zoom_mod, (0, i), (target_dim, i), grid_color, 1)
            cv2.line(zoom_diff, (i, 0), (i, target_dim), (50, 45, 55), 1)
            cv2.line(zoom_diff, (0, i), (target_dim, i), (50, 45, 55), 1)
            
    info = {
        "x_range": (x0, x1),
        "y_range": (y0, y1),
        "crop_size": (x1 - x0, y1 - y0),
        "scale_factor": round(scale_factor, 1),
        "pixel_count": cluster["pixel_count"]
    }
    
    return Image.fromarray(zoom_orig), Image.fromarray(zoom_mod), Image.fromarray(zoom_diff), info


def format_diff_legend_html(lang: str = "ar") -> str:
    """Render a clean, bilingual visual legend for the difference map and zoom views."""
    if lang == "ar":
        return """
        <div class="diff-legend-card">
            <div class="legend-header">دليل خريطة الاختلافات والملاحظات البصرية:</div>
            <div class="legend-items">
                <div class="legend-item">
                    <span class="legend-indicator box-indicator"></span>
                    <span class="legend-title">المربع الذهبي:</span>
                    <span class="legend-desc">إطار يحدد مكان وتجمع البكسلات المتغيرة</span>
                </div>
                <div class="legend-item">
                    <span class="legend-indicator glow-indicator"></span>
                    <span class="legend-title">البكسلات المضيئة:</span>
                    <span class="legend-desc">بكسلات طرأ عليها تعديل فعلي في البتات</span>
                </div>
                <div class="legend-item">
                    <span class="legend-indicator zoom-indicator">🔍</span>
                    <span class="legend-title">المعاينة المكبرة:</span>
                    <span class="legend-desc">تكبير مجهري للمنطقة لمشاهدة البكسل الواحد بوضوح</span>
                </div>
            </div>
            <div class="legend-scientific-note">
                ℹ️ <b>ملاحظة علمية:</b> التوهج والمربعات تستخدم لأغراض الإيضاح البصري فقط ولا تؤثر على الحسابات الدقيقة لعدد البكسلات ومقاييس PSNR و MSE.
            </div>
        </div>
        """
    else:
        return """
        <div class="diff-legend-card">
            <div class="legend-header">Difference Map Legend & Visual Guide:</div>
            <div class="legend-items">
                <div class="legend-item">
                    <span class="legend-indicator box-indicator"></span>
                    <span class="legend-title">Highlight Box:</span>
                    <span class="legend-desc">Region enclosing modified pixel clusters</span>
                </div>
                <div class="legend-item">
                    <span class="legend-indicator glow-indicator"></span>
                    <span class="legend-title">Bright Pixels:</span>
                    <span class="legend-desc">Modified pixels encoding secret payload</span>
                </div>
                <div class="legend-item">
                    <span class="legend-indicator zoom-indicator">🔍</span>
                    <span class="legend-title">Enlarged Preview:</span>
                    <span class="legend-desc">Microscopic magnification revealing individual pixels</span>
                </div>
            </div>
            <div class="legend-scientific-note">
                ℹ️ <b>Scientific Note:</b> Visual halos and highlight boxes are for visual clarity only and do not alter exact PSNR, MSE, or pixel count calculations.
            </div>
        </div>
        """


def format_zoom_header_html(lang: str = "ar") -> str:
    """Render title and subtitle for the Zoomed Change Region panel."""
    title = "تكبير منطقة التغيّر" if lang == "ar" else "Zoomed Change Region"
    sub = "المربع يحدد مكان البكسلات المتغيرة • تكبير مجهري بدقة البكسل الواحد" if lang == "ar" else "Box marks the changed pixels • Microscopic single-pixel magnification"
    return f"""
    <div class="zoom-panel-header">
        <div class="zoom-panel-title"><span>🔍</span> {title}</div>
        <div class="zoom-panel-sub">{sub}</div>
    </div>
    """


def format_zoom_info_html(cluster_info: Optional[dict], total_clusters: int = 1, current_idx: int = 1, lang: str = "ar") -> str:
    """Render informative metadata card describing the magnified crop."""
    if not cluster_info:
        if lang == "ar":
            return """
            <div class="zoom-info-card zoom-info-identical">
                ✓ <b>الصورتان متطابقتان تماماً:</b> لا توجد أي بكسلات متغيرة لتكبيرها (نسبة التشويه = 0 و PSNR = ∞ dB).
            </div>
            """
        else:
            return """
            <div class="zoom-info-card zoom-info-identical">
                ✓ <b>Identical Images:</b> No modified pixels detected to magnify (Distortion = 0, PSNR = ∞ dB).
            </div>
            """
            
    x0, x1 = cluster_info["x_range"]
    y0, y1 = cluster_info["y_range"]
    w, h = cluster_info["crop_size"]
    scale = cluster_info["scale_factor"]
    count = cluster_info["pixel_count"]
    
    if lang == "ar":
        multi_badge = f"<span class='zoom-badge'>منطقة {current_idx} من {total_clusters}</span> " if total_clusters > 1 else ""
        return f"""
        <div class="zoom-info-card">
            <div class="zoom-meta-row">
                {multi_badge}
                <span class="zoom-stat">📍 <b>الإحداثيات:</b> X: [{x0} .. {x1}], Y: [{y0} .. {y1}]</span>
                <span class="zoom-stat">📐 <b>أبعاد الإطار:</b> {w} × {h} بكسل</span>
                <span class="zoom-stat">🔍 <b>معامل التكبير:</b> {scale}× (كل بكسل = {int(scale)}×{int(scale)} نقطة)</span>
                <span class="zoom-stat">✨ <b>البكسلات المعدلة هنا:</b> {count:,} بكسل</span>
            </div>
        </div>
        """
    else:
        multi_badge = f"<span class='zoom-badge'>Region {current_idx} of {total_clusters}</span> " if total_clusters > 1 else ""
        return f"""
        <div class="zoom-info-card">
            <div class="zoom-meta-row">
                {multi_badge}
                <span class="zoom-stat">📍 <b>Coordinates:</b> X: [{x0} .. {x1}], Y: [{y0} .. {y1}]</span>
                <span class="zoom-stat">📐 <b>Frame:</b> {w} × {h} px</span>
                <span class="zoom-stat">🔍 <b>Magnification:</b> {scale}× (each pixel = {int(scale)}×{int(scale)} dots)</span>
                <span class="zoom-stat">✨ <b>Modified Pixels:</b> {count:,} px</span>
            </div>
        </div>
        """


def calculate_metrics(img1: Image.Image, img2: Image.Image, lang: str = "ar") -> dict:
    """Compute objective DIP metrics: PSNR, MSE, RMSE, and spatial altered pixel map."""
    rgb1 = np.array(img1.convert("RGB"), dtype=np.int16)
    rgb2 = np.array(img2.convert("RGB"), dtype=np.int16)

    if rgb1.shape != rgb2.shape:
        raise ValueError(
            f"Image dimensions mismatch: {rgb1.shape} vs {rgb2.shape}"
        )

    diff = rgb1 - rgb2
    mse = float(np.mean(diff.astype(np.float64) ** 2))
    rmse = float(np.sqrt(mse))

    if mse == 0.0:
        psnr_val = float("inf")
        psnr_str = "∞ dB"
        quality_tag = "مطابقة تامة" if lang == "ar" else "Lossless"
        quality_assessment = (
            "تطابق تام على مستوى البكسل (نسبة التشويه = 0)"
            if lang == "ar"
            else "Exact pixel-for-pixel mathematical identity (Distortion = 0)"
        )
    else:
        psnr_val = float(10.0 * np.log10((255.0 ** 2) / mse))
        psnr_str = f"{psnr_val:.2f} dB"
        if psnr_val >= 60.0:
            quality_tag = "ممتازة جداً" if lang == "ar" else "Pristine"
            quality_assessment = (
                "تعديل طفيف جداً غير مدرك بالعين البشرية"
                if lang == "ar"
                else "Imperceptible modification well above Human Visual System (HVS) threshold"
            )
        elif psnr_val >= 40.0:
            quality_tag = "عالية" if lang == "ar" else "High"
            quality_assessment = (
                "تطابق عالٍ مع تغيرات طفيفة في البتات الدنيا"
                if lang == "ar"
                else "High fidelity with localized LSB variations"
            )
        elif psnr_val >= 30.0:
            quality_tag = "متوسطة" if lang == "ar" else "Moderate"
            quality_assessment = (
                "تغيرات قد تظهر تحت التكبير المجهري"
                if lang == "ar"
                else "Noticeable variations under magnification"
            )
        else:
            quality_tag = "منخفضة" if lang == "ar" else "Distorted"
            quality_assessment = (
                "تشويه بصري ملحوظ"
                if lang == "ar"
                else "Significant visual degradation"
            )

    diff_pixels = np.any(diff != 0, axis=-1)
    changed_count = int(np.sum(diff_pixels))
    total_pixels = int(rgb1.shape[0] * rgb1.shape[1])
    changed_pct = (changed_count / total_pixels) * 100.0 if total_pixels > 0 else 0.0
    max_delta = int(np.max(np.abs(diff))) if changed_count > 0 else 0

    # Detect spatial clusters and bounding boxes of modified pixels
    clusters = detect_change_clusters(diff_pixels)

    # Generate enhanced difference map with glowing pixels & high-contrast bounding boxes
    u8_1 = np.array(img1.convert("RGB"), dtype=np.uint8)
    u8_2 = np.array(img2.convert("RGB"), dtype=np.uint8)
    diff_image = generate_enhanced_diff_map(u8_1, diff_pixels, clusters, lang=lang)

    # Generate zoomed views for the primary change cluster
    if clusters:
        z_orig, z_mod, z_diff, z_info = generate_zoomed_views(u8_1, u8_2, diff_pixels, clusters[0])
    else:
        z_orig, z_mod, z_diff, z_info = None, None, None, None

    return {
        "psnr_val": psnr_val,
        "psnr_str": psnr_str,
        "mse": mse,
        "rmse": rmse,
        "changed_count": changed_count,
        "total_pixels": total_pixels,
        "changed_pct": changed_pct,
        "max_delta": max_delta,
        "quality_assessment": quality_assessment,
        "quality_tag": quality_tag,
        "diff_image": diff_image,
        "clusters": clusters,
        "zoom_orig": z_orig,
        "zoom_mod": z_mod,
        "zoom_diff": z_diff,
        "zoom_info": z_info,
    }


def format_metric_cards_html(metrics: dict, lang: str = "ar") -> str:
    """Render 4 clean, prominent summary metric cards with plain scientific tooltips."""
    if lang == "ar":
        l_psnr = "PSNR — جودة الصورة"
        t_psnr = "مقياس لوغاريتمي لجودة الصورة بدلالة الديسيبل (dB). القيم الأعلى من 40 dB تعني جودة عالية جداً يصعب تمييز أي فرق فيها بالعين المجردة."
        l_mse = "MSE — متوسط فرق البكسل"
        t_mse = "متوسط مربع الاختلاف بين بكسلات الصورتين عبر قنوات الألوان. كلما اقتربت القيمة من 0.0000 كانت الدقة أعلى."
        l_chg = "البكسلات المتغيرة"
        t_chg = "عدد ونسبة البكسلات التي طرأ عليها تعديل في البت الأقل أهمية لحمل بيانات الرسالة السرية."
        l_max = "أقصى تغير للبكسل"
        t_max = "أكبر فارق عددي طرأ على أي بكسل في المدى [0, 255]. في تقنية LSB يكون الفارق محصوراً في ±1 فقط."
        sub_total = f"من إجمالي <span class='numeric-val'>{metrics['total_pixels']:,}</span> بكسل"
        sub_domain = "في المدى الثماني [0, 255]"
    else:
        l_psnr = "PSNR — Image Quality"
        t_psnr = "Logarithmic measure of peak signal-to-noise ratio in decibels (dB). Values above 40 dB indicate high fidelity that is imperceptible to the human eye."
        l_mse = "MSE — Pixel Difference"
        t_mse = "Mean squared difference per pixel color channel across all spatial coordinates. Closer to 0.0000 indicates higher fidelity."
        l_chg = "Changed Pixels"
        t_chg = "Total count and percentage of pixels whose least-significant bits were modified to encode payload."
        l_max = "Maximum Pixel Change"
        t_max = "The largest numerical level alteration introduced to any pixel channel in [0, 255]. In LSB, change is strictly ±1."
        sub_total = f"Out of <span class='numeric-val'>{metrics['total_pixels']:,}</span> total pixels"
        sub_domain = "8-bit Quantized Domain [0, 255]"

    return f"""
    <div class="metrics-grid">
        <div class="metric-card" title="{t_psnr}">
            <div class="metric-label">{l_psnr}</div>
            <div class="metric-val"><span class="numeric-val">{metrics['psnr_str']}</span> <span class="metric-badge">{metrics['quality_tag']}</span></div>
            <div class="metric-sub">{metrics['quality_assessment']}</div>
        </div>
        <div class="metric-card" title="{t_mse}">
            <div class="metric-label">{l_mse}</div>
            <div class="metric-val"><span class="numeric-val">{metrics['mse']:.6f}</span></div>
            <div class="metric-sub"><span class="numeric-val">RMSE: {metrics['rmse']:.6f}</span></div>
        </div>
        <div class="metric-card" title="{t_chg}">
            <div class="metric-label">{l_chg}</div>
            <div class="metric-val"><span class="numeric-val">{metrics['changed_count']:,}</span> <span class="metric-pct">(<span class="numeric-val">{metrics['changed_pct']:.4f}%</span>)</span></div>
            <div class="metric-sub">{sub_total}</div>
        </div>
        <div class="metric-card" title="{t_max}">
            <div class="metric-label">{l_max}</div>
            <div class="metric-val"><span class="numeric-val">±{metrics['max_delta']}</span></div>
            <div class="metric-sub">{sub_domain}</div>
        </div>
    </div>
    """


def format_quick_metrics_html(metrics: dict, lang: str = "ar") -> str:
    """Render a compact 1-row summary for placement beside the download button."""
    if lang == "ar":
        l_psnr = "جودة الصورة (PSNR):"
        l_mse = "متوسط الفارق (MSE):"
        l_chg = "البكسلات المتغيرة:"
    else:
        l_psnr = "PSNR Quality:"
        l_mse = "MSE Difference:"
        l_chg = "Changed Pixels:"

    return f"""
    <div class="quick-metrics-bar">
        <div class="quick-metric-item">
            <span class="quick-metric-label">{l_psnr}</span>
            <span class="quick-metric-val"><span class="numeric-val">{metrics['psnr_str']}</span></span>
            <span class="quick-metric-tag">{metrics['quality_tag']}</span>
        </div>
        <div class="quick-metric-item">
            <span class="quick-metric-label">{l_mse}</span>
            <span class="quick-metric-val"><span class="numeric-val">{metrics['mse']:.6f}</span></span>
        </div>
        <div class="quick-metric-item">
            <span class="quick-metric-label">{l_chg}</span>
            <span class="quick-metric-val"><span class="numeric-val">{metrics['changed_count']:,} ({metrics['changed_pct']:.3f}%)</span></span>
        </div>
    </div>
    """


def get_image_metadata_html(img: Optional[Image.Image], lang: str = "ar") -> str:
    """Return sleek metadata badge row when an image is selected."""
    if img is None:
        return ""
    w, h = img.size
    mode = img.mode
    est_lsb_bytes = (w * h * 3) // 8

    if lang == "ar":
        res_text = f"الدقة: <b class='numeric-val'>{w} × {h}</b> بكسل"
        mode_text = f"نمط الألوان: <b>{mode}</b>"
        cap_text = f"السعة التقديرية (LSB): <b class='numeric-val'>~{est_lsb_bytes:,}</b> بايت"
    else:
        res_text = f"Resolution: <b class='numeric-val'>{w} × {h}</b> px"
        mode_text = f"Color Mode: <b>{mode}</b>"
        cap_text = f"Estimated LSB Capacity: <b class='numeric-val'>~{est_lsb_bytes:,}</b> bytes"

    return f"""
    <div class="meta-strip">
        <span class="meta-pill">{res_text}</span>
        <span class="meta-pill">{mode_text}</span>
        <span class="meta-pill-maroon">{cap_text}</span>
    </div>
    """


def update_message_counter(msg: str, lang: str = "ar") -> str:
    """Return live payload character and byte counter indicator."""
    char_count = len(msg) if msg else 0
    byte_count = len(msg.encode("utf-8", errors="replace")) if msg else 0

    if lang == "ar":
        lbl = "طول الرسالة:"
        chars_str = f"<span class='numeric-val'>{char_count:,}</span> حرفاً"
        bytes_str = f"(<span class='numeric-val'>{byte_count:,}</span> بايت UTF-8)"
    else:
        lbl = "Payload:"
        chars_str = f"<span class='numeric-val'>{char_count:,}</span> characters"
        bytes_str = f"(<span class='numeric-val'>{byte_count:,}</span> UTF-8 bytes)"

    val_class = "counter-val-active" if char_count > 0 else "counter-val"

    return f"""
    <div class="capacity-counter-bar">
        <span class="counter-label">{lbl}</span>
        <span class="{val_class}">{chars_str}</span>
        <span class="counter-sub">{bytes_str}</span>
    </div>
    """


# ==============================================================================
# Core Action Handlers
# ==============================================================================

def hide_message_workflow(
    image: Optional[Image.Image],
    message: str,
    method_choice: str,
    generator_choice: str,
    shift_val: int,
    encoding: str,
    lang_choice: str,
):
    """Execute steganographic embedding and return refined result workspace."""
    lang = "ar" if (lang_choice == "العربية" or lang_choice == "ar") else "en"

    if image is None:
        err = "⚠️ يرجى رفع صورة الغلاف أولاً." if lang == "ar" else "⚠️ Please upload a cover image first."
        return (
            f"<div class='notice-box notice-error'>{err}</div>",
            gr.update(visible=False),
            "",
            None,
            gr.update(visible=False, value=None),
            gr.update(visible=False, value=None),
            "",
            "",
            "",
            None,
            "",
            gr.update(visible=False),
        )

    if not message or not message.strip():
        err = "⚠️ يرجى كتابة نص الرسالة السرية المراد إخفاؤها." if lang == "ar" else "⚠️ Please enter a secret message to embed."
        return (
            f"<div class='notice-box notice-error'>{err}</div>",
            gr.update(visible=False),
            "",
            None,
            gr.update(visible=False, value=None),
            gr.update(visible=False, value=None),
            "",
            "",
            "",
            None,
            "",
            gr.update(visible=False),
        )

    t0 = time.time()
    cover_copy = image.copy()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Character set checks for Unicode/Arabic support
    is_unicode = any(ord(c) > 255 for c in message)
    is_non_ascii = any(ord(c) > 127 for c in message)
    norm_method = normalize_method(method_choice)

    try:
        if norm_method == "LSB":
            gen = get_generator_by_name(generator_choice)
            stego_img = lsb.hide(
                image=cover_copy,
                message=message,
                generator=gen,
                shift=int(shift_val),
                encoding=encoding,
                auto_convert_rgb=True,
            )
            technique_tag = "lsb"

        elif norm_method == "RDH":
            # If Unicode/Arabic characters exist and user left UTF-8, automatically use UTF-32LE as required by RDH
            actual_encoding = encoding
            if is_unicode and encoding == "UTF-8":
                actual_encoding = "UTF-32LE"

            stego_img = rdh.hide(
                image=cover_copy,
                message=message,
                encoding=actual_encoding,
            )
            technique_tag = "rdh"

        elif norm_method == "RED":
            if is_non_ascii:
                msg_err = (
                    "⚠️ <b>خوارزمية القناة الحمراء تدعم أحرف ASCII الإنجليزية فقط (0–127).</b><br>للرسائل باللغة العربية، يرجى اختيار خوارزمية <b>LSB (تعديل البت الأقل أهمية)</b> أو <b>RDH (الإخفاء العكسي)</b>."
                    if lang == "ar"
                    else "⚠️ <b>Red Channel algorithm only supports standard ASCII characters (0–127).</b><br>For Arabic or Unicode text, please switch to <b>LSB</b> or <b>RDH</b>."
                )
                return (
                    f"<div class='notice-box notice-error'>{msg_err}</div>",
                    gr.update(visible=False),
                    "",
                    None,
                    gr.update(visible=False, value=None),
                    gr.update(visible=False, value=None),
                    "",
                    "",
                    "",
                    None,
                    "",
                    gr.update(visible=False),
                )
            if len(message) >= 255:
                msg_err = (
                    f"⚠️ خوارزمية القناة الحمراء محدودة بـ 254 حرفاً (الحالي: {len(message)}). يرجى تقصير الرسالة أو استخدام LSB / RDH."
                    if lang == "ar"
                    else f"⚠️ Red Channel is limited to 254 characters (current: {len(message)}). Shorten your message or switch to LSB / RDH."
                )
                return (
                    f"<div class='notice-box notice-error'>{msg_err}</div>",
                    gr.update(visible=False),
                    "",
                    None,
                    gr.update(visible=False, value=None),
                    gr.update(visible=False, value=None),
                    "",
                    "",
                    "",
                    None,
                    "",
                    gr.update(visible=False),
                )
            stego_img = red.hide(
                input_image=cover_copy,
                message=message,
            )
            technique_tag = "red"
        else:
            return (
                f"<div class='notice-box notice-error'>⚠️ خوارزمية غير معروفة: {method_choice}</div>",
                gr.update(visible=False),
                "",
                None,
                gr.update(visible=False, value=None),
                gr.update(visible=False, value=None),
                "",
                "",
                "",
                None,
                "",
                gr.update(visible=False),
            )

        elapsed = time.time() - t0

        # Save authentic, uncompressed lossless PNG artifact to disk
        out_filename = f"hypocritical_saint_{technique_tag}_{timestamp}.png"
        out_filepath = str(OUTPUT_DIR / out_filename)
        stego_img.save(out_filepath, format="PNG")

        assert os.path.exists(out_filepath), f"Generated file was not saved at {out_filepath}"
        file_size_bytes = os.path.getsize(out_filepath)
        file_size_mb = file_size_bytes / (1024 * 1024)

        metrics = calculate_metrics(image, stego_img, lang=lang)
        metrics_html = format_metric_cards_html(metrics, lang=lang)
        quick_metrics_html = format_quick_metrics_html(metrics, lang=lang)
        slider_html = generate_comparison_slider_html(image, stego_img, lang=lang)

        msg_bytes = len(message.encode("utf-8", errors="replace"))

        if lang == "ar":
            banner_title = f"تم إخفاء الرسالة السرية بنجاح داخل الصورة في <span class='numeric-val'>{elapsed:.3f}</span> ثانية!"
            banner_sub = f"الخوارزمية: <b>{method_choice}</b> • الحمولة: <b class='numeric-val'>{len(message)}</b> حرفاً (<span class='numeric-val'>{msg_bytes}</span> بايت) • حجم الصورة: <span class='numeric-val'>{file_size_mb:.2f} MB</span>"
            file_badge_text = f"💾 <b>الملف المباشر:</b> <code class='numeric-val'>{out_filename}</code> (<span class='numeric-val'>{file_size_mb:.2f} MB</span>) • <i>صيغة PNG غير مضغوطة جاهزة للتنزيل</i>"
        else:
            banner_title = f"Secret message successfully concealed in <span class='numeric-val'>{elapsed:.3f}s</span>!"
            banner_sub = f"Algorithm: <b>{method_choice}</b> • Payload: <b class='numeric-val'>{len(message)}</b> characters (<span class='numeric-val'>{msg_bytes}</span> bytes) • Output Size: <span class='numeric-val'>{file_size_mb:.2f} MB</span>"
            file_badge_text = f"💾 <b>Direct Artifact:</b> <code class='numeric-val'>{out_filename}</code> (<span class='numeric-val'>{file_size_mb:.2f} MB</span>) • <i>Lossless PNG format</i>"

        success_banner = f"""
        <div class="result-success-banner">
            <div class="banner-icon">✓</div>
            <div class="banner-content">
                <div class="banner-title">{banner_title}</div>
                <div class="banner-sub">{banner_sub}</div>
            </div>
        </div>
        """

        file_path_info = f"""
        <div class="file-path-badge">
            {file_badge_text}
        </div>
        """

        return (
            "",                                                              # 1. hide_status_box (clear error)
            gr.update(visible=True),                                        # 2. results_workspace (reveal results)
            success_banner,                                                 # 3. hide_success_banner
            stego_img,                                                      # 4. hide_stego_preview
            gr.update(value=out_filepath, visible=True),                    # 5. btn_download_primary (DownloadButton)
            gr.update(value=out_filepath, visible=True),                    # 6. btn_download_file (File)
            file_path_info,                                                 # 7. hide_file_path_info
            quick_metrics_html,                                             # 8. hide_quick_metrics
            slider_html,                                                    # 9. hide_slider_display
            metrics["diff_image"],                                          # 10. hide_diff_preview
            metrics_html,                                                   # 11. hide_metrics_detailed
            gr.update(visible=True),                                        # 12. btn_forward_reveal
        )

    except Exception as e:
        err_msg = str(e)
        if "out of range" in err_msg.lower():
            err_msg = (
                "حجم الرسالة يتجاوز سعة المتتالية المختارة لحجم هذه الصورة. يرجى اختيار 'تسلسل خطي منتظم' أو استخدام صورة ذات دقة أكبر."
                if lang == "ar"
                else "Payload exceeds the capacity of the selected sequence. Switch to 'Sequential (Identity)' or choose a larger cover image."
            )
        prefix = "❌ <b>فشلت عملية الإخفاء:</b>" if lang == "ar" else "❌ <b>Embedding Failed:</b>"
        return (
            f"<div class='notice-box notice-error'>{prefix} {err_msg}</div>",
            gr.update(visible=False),
            "",
            None,
            gr.update(visible=False, value=None),
            gr.update(visible=False, value=None),
            "",
            "",
            "",
            None,
            "",
            gr.update(visible=False),
        )


def reveal_message_workflow(
    stego_image: Optional[Image.Image],
    method_choice: str,
    generator_choice: str,
    shift_val: int,
    encoding: str,
    lang_choice: str,
):
    """Extract hidden payload from stego carrier with automatic Unicode/encoding recovery."""
    lang = "ar" if (lang_choice == "العربية" or lang_choice == "ar") else "en"

    if stego_image is None:
        err = "⚠️ يرجى رفع الصورة الحاملة للرسالة أولاً." if lang == "ar" else "⚠️ Please upload a stego carrier image first."
        return (
            f"<div class='notice-box notice-error'>{err}</div>",
            "",
            "",
            gr.update(visible=False),
            None,
            "",
            gr.update(visible=False),
        )

    t0 = time.time()
    norm_method = normalize_method(method_choice)

    try:
        extracted = None

        if norm_method == "LSB":
            gen = get_generator_by_name(generator_choice)
            extracted = lsb.reveal(
                encoded_image=stego_image.copy(),
                generator=gen,
                shift=int(shift_val),
                encoding=encoding,
            )
        elif norm_method == "RDH":
            extracted = rdh.reveal(
                image=stego_image.copy(),
                encoding=encoding,
            )
            if "\x00" in extracted:
                alt_encoding = "UTF-32LE" if encoding == "UTF-8" else "UTF-8"
                try:
                    alt_extracted = rdh.reveal(
                        image=stego_image.copy(),
                        encoding=alt_encoding,
                    )
                    if "\x00" not in alt_extracted:
                        extracted = alt_extracted
                except Exception:
                    pass
        elif norm_method == "RED":
            extracted = red.reveal(
                input_image=stego_image.copy(),
            )
        else:
            err = f"⚠️ خوارزمية غير معروفة: {method_choice}" if lang == "ar" else f"⚠️ Unrecognized method: {method_choice}"
            return (
                f"<div class='notice-box notice-error'>{err}</div>",
                "",
                "",
                gr.update(visible=False),
                None,
                "",
                gr.update(visible=False),
            )

        elapsed = time.time() - t0

        if extracted is None or extracted == "":
            err = (
                "⚠️ لم يتم العثور على أي رسالة مخفية. يرجى التأكد من تطابق الخوارزمية، المتتالية الرياضية، وقيمة الإزاحة المستخدمة أثناء الإخفاء."
                if lang == "ar"
                else "⚠️ No secret message detected. Verify that matching algorithm, generator sequence, shift, and encoding were used."
            )
            return (
                f"<div class='notice-box notice-error'>{err}</div>",
                "",
                "",
                gr.update(visible=False),
                None,
                "",
                gr.update(visible=False),
            )

        msg_bytes = len(extracted.encode("utf-8", errors="replace"))

        if lang == "ar":
            banner_title = f"تم استخراج الرسالة السرية بنجاح في <span class='numeric-val'>{elapsed:.3f}</span> ثانية!"
            banner_sub = f"الخوارزمية: <b>{method_choice}</b> • طول الرسالة المستخرجة: <b class='numeric-val'>{len(extracted)}</b> حرفاً (<span class='numeric-val'>{msg_bytes}</span> بايت)"
            meta_len = f"طول النص: <b class='numeric-val'>{len(extracted):,}</b> حرفاً"
            meta_bytes = f"الحجم: <b class='numeric-val'>{msg_bytes:,}</b> بايت"
            meta_algo = f"الخوارزمية: <b>{method_choice}</b>"
        else:
            banner_title = f"Secret payload successfully extracted in <span class='numeric-val'>{elapsed:.3f}s</span>!"
            banner_sub = f"Method: <b>{method_choice}</b> • Extracted Length: <b class='numeric-val'>{len(extracted)}</b> characters (<span class='numeric-val'>{msg_bytes}</span> bytes)"
            meta_len = f"Length: <b class='numeric-val'>{len(extracted):,}</b> characters"
            meta_bytes = f"Bytes: <b class='numeric-val'>{msg_bytes:,}</b>"
            meta_algo = f"Algorithm: <b>{method_choice}</b>"

        success_html = f"""
        <div class="result-success-banner">
            <div class="banner-icon">✓</div>
            <div class="banner-content">
                <div class="banner-title">{banner_title}</div>
                <div class="banner-sub">{banner_sub}</div>
            </div>
        </div>
        """

        meta_info = f"""
        <div class="meta-strip" style="margin-top: 8px;">
            <span class="meta-pill">{meta_len}</span>
            <span class="meta-pill">{meta_bytes}</span>
            <span class="meta-pill-maroon">{meta_algo}</span>
        </div>
        """

        is_rdh = (norm_method == "RDH")

        return (
            success_html,
            extracted,
            meta_info,
            gr.update(visible=is_rdh),
            None,
            "",
            gr.update(visible=True),  # extracted_result_card visible
        )

    except Exception as e:
        err_msg = (
            f"❌ <b>خطأ أثناء الاستخراج:</b> {str(e)}<br><small>تأكد من اختيار نفس الخوارزمية، المتتالية، ونوع الترميز المستخدم أثناء الإخفاء.</small>"
            if lang == "ar"
            else f"❌ <b>Extraction Error:</b> {str(e)}<br><small>Ensure matching algorithm, sequence generator, and character encoding are selected.</small>"
        )
        return (
            f"<div class='notice-box notice-error'>{err_msg}</div>",
            "",
            "",
            gr.update(visible=False),
            None,
            "",
            gr.update(visible=False),
        )


def execute_rdh_cover_restoration(
    stego_image: Optional[Image.Image],
    orig_reference: Optional[Image.Image],
    encoding: str,
    lang_choice: str,
):
    """Restore cover image pixel-for-pixel using Ni et al. Histogram Shifting."""
    lang = "ar" if (lang_choice == "العربية" or lang_choice == "ar") else "en"

    if stego_image is None:
        err = "⚠️ يرجى رفع صورة مشفرة بخوارزمية RDH أولاً." if lang == "ar" else "⚠️ Please upload an RDH stego image first."
        return (
            f"<div class='notice-box notice-error'>{err}</div>",
            "",
            None,
            gr.update(visible=False, value=None),
            gr.update(visible=False, value=None),
            "",
        )

    t0 = time.time()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        extracted = rdh.reveal(image=stego_image.copy(), encoding=encoding)
        if "\x00" in extracted:
            alt_encoding = "UTF-32LE" if encoding == "UTF-8" else "UTF-8"
            try:
                alt_extracted = rdh.reveal(image=stego_image.copy(), encoding=alt_encoding)
                if "\x00" not in alt_extracted:
                    extracted = alt_extracted
            except Exception:
                pass

        recovered_img = rdh.recover(image=stego_image.copy())
        elapsed = time.time() - t0

        out_filename = f"recovered_cover_{timestamp}.png"
        out_filepath = str(OUTPUT_DIR / out_filename)
        recovered_img.save(out_filepath, format="PNG")

        verif_html = ""
        if orig_reference is not None:
            metrics = calculate_metrics(orig_reference, recovered_img, lang=lang)
            cards = format_metric_cards_html(metrics, lang=lang)
            if metrics["mse"] == 0.0:
                v_title = "تأكيد التطابق التام 100% رياضياً وبصرياً (Lossless)" if lang == "ar" else "Mathematical 100% Lossless Restoration Confirmed"
                v_sub = "الصورة المسترجعة تطابق الصورة الأصلية بكسلاً ببكسل (MSE = 0.000, PSNR = ∞)." if lang == "ar" else "The recovered carrier exactly matches original cover reference (MSE = 0.000, PSNR = ∞)."
                verif_html = f"""
                <div class="result-success-banner" style="margin-top: 10px;">
                    <div class="banner-icon">★</div>
                    <div class="banner-content">
                        <div class="banner-title">{v_title}</div>
                        <div class="banner-sub">{v_sub}</div>
                    </div>
                </div>
                {cards}
                """
            else:
                discrep = "تم رصد فارق بين الصورة المسترجعة والصورة المرجعية المزودة." if lang == "ar" else "Discrepancy detected with supplied reference image."
                verif_html = f"""
                <div class="notice-box notice-error">{discrep}</div>
                {cards}
                """

        s_title = f"تم استرجاع صورة الغلاف الأصلية واستخراج النص بنجاح ({elapsed:.3f} ثانية)" if lang == "ar" else f"Carrier Reconstructed & Message Extracted ({elapsed:.3f}s)"
        s_sub = f"طول النص: <b class='numeric-val'>{len(extracted)}</b> حرفاً • اسم الملف: <code class='numeric-val'>{out_filename}</code>" if lang == "ar" else f"Extracted: <b class='numeric-val'>{len(extracted)} chars</b> • Restored File: <code class='numeric-val'>{out_filename}</code>"

        status_html = f"""
        <div class="result-success-banner">
            <div class="banner-icon">✓</div>
            <div class="banner-content">
                <div class="banner-title">{s_title}</div>
                <div class="banner-sub">{s_sub}</div>
            </div>
        </div>
        """

        return (
            status_html,
            extracted,
            recovered_img,
            gr.update(value=out_filepath, visible=True),
            gr.update(value=out_filepath, visible=True),
            verif_html,
        )

    except Exception as e:
        err_msg = (
            f"❌ <b>خطأ أثناء استرجاع الصورة:</b> {str(e)}<br><small>تأكد من أن الصورة مشفرة بالفعل بتقنية RDH ومحفوظة بصيغة PNG بدون فقدان.</small>"
            if lang == "ar"
            else f"❌ <b>Restoration Error:</b> {str(e)}<br><small>Ensure carrier was encoded with RDH and preserved in a lossless format (PNG).</small>"
        )
        return (
            f"<div class='notice-box notice-error'>{err_msg}</div>",
            "",
            None,
            gr.update(visible=False, value=None),
            gr.update(visible=False, value=None),
            "",
        )


def check_rdh_capacity_action(image: Optional[Image.Image], lang_choice: str):
    """Calculate and return RDH usable capacity."""
    lang = "ar" if (lang_choice == "العربية" or lang_choice == "ar") else "en"
    if image is None:
        err = "يرجى رفع صورة أولاً لحساب سعتها." if lang == "ar" else "Upload an image first to evaluate capacity."
        return f"<div class='notice-box notice-error'>{err}</div>"
    try:
        cap_bytes = rdh.capacity(image.copy())
        if lang == "ar":
            return f"<div class='capacity-badge'>📊 <b>السعة القصوى للاستيعاب (RDH):</b> <code class='numeric-val'>{cap_bytes:,} بايت</code> (حوالي <code class='numeric-val'>{cap_bytes:,}</code> حرفاً)</div>"
        else:
            return f"<div class='capacity-badge'>📊 <b>RDH Payload Capacity:</b> <code class='numeric-val'>{cap_bytes:,} bytes</code> (~<code class='numeric-val'>{cap_bytes:,}</code> characters)</div>"
    except Exception as e:
        return f"<div class='notice-box notice-error'>تنبيه السعة: {str(e)}</div>"


def compare_images_workflow(img1: Optional[Image.Image], img2: Optional[Image.Image], lang_choice: str):
    """Standalone quantitative image quality comparison with bounding boxes, dilation glow, and zoomed crops."""
    lang = "ar" if (lang_choice == "العربية" or lang_choice == "ar") else "en"
    if img1 is None or img2 is None:
        err = "⚠️ يرجى رفع الصورتين (الأصلية والمعدّلة) لبدء المقارنة." if lang == "ar" else "⚠️ Please upload both original and modified images."
        return (
            f"<div class='notice-box notice-error'>{err}</div>",
            None,
            "",
            format_diff_legend_html(lang),
            format_zoom_header_html(lang),
            gr.update(choices=[], value=None),
            None,
            None,
            None,
            format_zoom_info_html(None, lang=lang),
        )
    try:
        metrics = calculate_metrics(img1, img2, lang=lang)
        cards = format_metric_cards_html(metrics, lang=lang)
        if lang == "ar":
            title = "اكتملت المقارنة وحساب الفروق بدقة"
            sub = f"جودة الصورة: <b>{metrics['psnr_str']}</b> • البكسلات المتغيرة: <b class='numeric-val'>{metrics['changed_pct']:.4f}%</b> • أقصى فارق: <b class='numeric-val'>±{metrics['max_delta']}</b>"
        else:
            title = "Quantitative Distortion Evaluation Complete"
            sub = f"PSNR: <b>{metrics['psnr_str']}</b> • Altered Pixels: <b class='numeric-val'>{metrics['changed_pct']:.4f}%</b> • Max Delta: <b class='numeric-val'>±{metrics['max_delta']}</b>"

        status_html = f"""
        <div class="result-success-banner">
            <div class="banner-icon">✓</div>
            <div class="banner-content">
                <div class="banner-title">{title}</div>
                <div class="banner-sub">{sub}</div>
            </div>
        </div>
        """

        clusters = metrics["clusters"]
        if clusters:
            if lang == "ar":
                choices = [f"المنطقة #{c['id']} — إحداثيات ({c['x']}, {c['y']}) — [{c['pixel_count']} بكسل]" for c in clusters]
            else:
                choices = [f"Region #{c['id']} — Pos ({c['x']}, {c['y']}) — [{c['pixel_count']} pixels]" for c in clusters]
            sel_val = choices[0]
        else:
            choices = ["✓ لا توجد بكسلات متغيرة (تطابق تام)" if lang == "ar" else "✓ Identical Images (0 changed pixels)"]
            sel_val = choices[0]

        legend_html = format_diff_legend_html(lang)
        zoom_header_html = format_zoom_header_html(lang)
        region_dropdown_update = gr.update(choices=choices, value=sel_val)
        zoom_info_html = format_zoom_info_html(metrics["zoom_info"], total_clusters=len(clusters), current_idx=1, lang=lang)

        return (
            status_html,
            metrics["diff_image"],
            cards,
            legend_html,
            zoom_header_html,
            region_dropdown_update,
            metrics["zoom_orig"],
            metrics["zoom_mod"],
            metrics["zoom_diff"],
            zoom_info_html,
        )
    except Exception as e:
        return (
            f"<div class='notice-box notice-error'>❌ <b>خطأ في المقارنة:</b> {str(e)}</div>",
            None,
            "",
            format_diff_legend_html(lang),
            format_zoom_header_html(lang),
            gr.update(choices=[], value=None),
            None,
            None,
            None,
            f"<div class='notice-box notice-error'>{str(e)}</div>",
        )


def switch_zoom_region_workflow(img1: Optional[Image.Image], img2: Optional[Image.Image], selected_choice: str, lang_choice: str):
    """Dynamically switch between detected change clusters in the Zoom preview."""
    lang = "ar" if (lang_choice == "العربية" or lang_choice == "ar") else "en"
    if img1 is None or img2 is None or not selected_choice:
        return None, None, None, format_zoom_info_html(None, lang=lang)

    try:
        rgb1 = np.array(img1.convert("RGB"), dtype=np.int16)
        rgb2 = np.array(img2.convert("RGB"), dtype=np.int16)
        if rgb1.shape != rgb2.shape:
            return None, None, None, ""

        diff = rgb1 - rgb2
        diff_mask = np.any(diff != 0, axis=-1)
        if not np.any(diff_mask):
            return None, None, None, format_zoom_info_html(None, lang=lang)

        clusters = detect_change_clusters(diff_mask, max_clusters=6)
        if not clusters:
            return None, None, None, format_zoom_info_html(None, lang=lang)

        import re
        m = re.search(r"#(\d+)", selected_choice)
        target_id = int(m.group(1)) if m else 1

        selected_cluster = clusters[0]
        for c in clusters:
            if c["id"] == target_id:
                selected_cluster = c
                break

        u8_1 = np.array(img1.convert("RGB"), dtype=np.uint8)
        u8_2 = np.array(img2.convert("RGB"), dtype=np.uint8)
        z_orig, z_mod, z_diff, z_info = generate_zoomed_views(u8_1, u8_2, diff_mask, selected_cluster)
        info_html = format_zoom_info_html(z_info, total_clusters=len(clusters), current_idx=selected_cluster["id"], lang=lang)
        return z_orig, z_mod, z_diff, info_html
    except Exception as e:
        return None, None, None, f"<div class='notice-box notice-error'>{str(e)}</div>"


def parity_analysis_workflow(img: Optional[Image.Image], lang_choice: str):
    """Extract LSB bit-plane parity map."""
    lang = "ar" if (lang_choice == "العربية" or lang_choice == "ar") else "en"
    if img is None:
        err = "⚠️ يرجى رفع صورة لفحص بتاتها." if lang == "ar" else "⚠️ Please supply an image to inspect."
        return f"<div class='notice-box notice-error'>{err}</div>", None
    try:
        t0 = time.time()
        analyzed = parity.steganalyse(img.copy())
        elapsed = time.time() - t0
        if lang == "ar":
            title = f"تم عزل مستوى البت الأقل أهمية (LSB) في <span class='numeric-val'>{elapsed:.3f}</span> ثانية"
            sub = "التحليل البصري لمستوى البت الأدنى: تُظهر الصور الطبيعية عشوائية متجانسة في هذا المستوى، بينما يُظهر الإخفاء الخوارزمي أنماطاً أو حدوداً هندسية منتظمة."
        else:
            title = f"LSB Parity Bit-Plane Isolated in <span class='numeric-val'>{elapsed:.3f}s</span>"
            sub = "Visual analysis of the least-significant-bit plane. Natural continuous imagery exhibits uniform stochastic entropy; algorithmic steganography exhibits structural patterns."

        status_html = f"""
        <div class="result-success-banner">
            <div class="banner-icon">✓</div>
            <div class="banner-content">
                <div class="banner-title">{title}</div>
                <div class="banner-sub">{sub}</div>
            </div>
        </div>
        """
        return status_html, analyzed
    except Exception as e:
        return f"<div class='notice-box notice-error'>❌ <b>خطأ التحليل:</b> {str(e)}</div>", None


# ==============================================================================
# HTML Component Renderers (Header, About, Footer)
# ==============================================================================

def get_header_html(lang: str = "ar") -> str:
    """Generate localized slim application header."""
    badge = t("arabic_badge", lang)
    subtitle = t("app_subtitle", lang)
    tagline = t("app_tagline", lang)

    return f"""
    <div class="header-brand-line">
        <div class="brand-monogram">
            <svg width="34" height="34" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="32" height="32" rx="8" fill="#211C20" stroke="#40343C"/>
                <path d="M9 10V22M15 10V22M9 16H15" stroke="#8B354B" stroke-width="2" stroke-linecap="round"/>
                <path d="M23 10.5C23 10.5 22 9.5 20 9.5C18.5 9.5 17.5 10.5 17.5 12C17.5 14.5 23 14 23 17.5C23 19.5 21.5 20.5 19.5 20.5C17.5 20.5 16.5 19.5 16.5 19.5" stroke="#D9C6B0" stroke-width="2" stroke-linecap="round"/>
                <circle cx="24" cy="8" r="2" fill="#8B354B"/>
            </svg>
        </div>
        <div class="brand-text-col">
            <div class="brand-title">HYPOCRITICAL <span class="maroon-text">SAINT</span></div>
            <div class="brand-subtitle">{subtitle}</div>
        </div>
        <div class="brand-feature-pill">
            <span>✦ {badge}</span>
        </div>
        <div class="brand-tagline-box">
            <span class="brand-tagline">“{tagline}”</span>
        </div>
    </div>
    """


def get_about_drawer_html(lang: str = "ar") -> str:
    """Generate localized content for the About Drawer."""
    return f"""
    <div class="about-grid">
        <div class="about-item">
            <div class="about-item-label">{t('about_title', lang)}</div>
            <div class="about-item-val">{t('app_title', lang)} — {t('app_subtitle', lang)}</div>
            <div class="about-item-sub">“{t('app_tagline', lang)}”</div>
        </div>
        <div class="about-item">
            <div class="about-item-label">{t('about_dev_title', lang)}</div>
            <div class="about-item-val">{t('about_dev_val', lang)}</div>
            <div class="about-item-sub">{t('about_dev_sub', lang)}</div>
        </div>
        <div class="about-item">
            <div class="about-item-label">{t('about_inst_title', lang)}</div>
            <div class="about-item-val">{t('about_inst_val', lang)}</div>
            <div class="about-item-sub">{t('about_inst_sub', lang)}</div>
        </div>
        <div class="about-item">
            <div class="about-item-label">{t('about_lang_title', lang)}</div>
            <div class="about-item-val">{t('about_lang_val', lang)}</div>
        </div>
        <div class="about-item" style="grid-column: 1 / -1;">
            <div class="about-item-label">{t('about_engine_title', lang)}</div>
            <div class="about-item-val">{t('about_engine_val', lang)}</div>
            <div class="about-item-sub">{t('about_engine_sub', lang)}</div>
        </div>
    </div>
    """


def get_footer_html(lang: str = "ar") -> str:
    """Generate localized studio footer."""
    return f"""
    <div class="studio-footer">
        {t('footer_text', lang)}
    </div>
    """


# ==============================================================================
# Custom CSS: Maroon × Soft Ivory × Charcoal Design System (Cairo / Inter Fonts)
# ==============================================================================

MAROON_DESIGN_SYSTEM_CSS = r"""
/* HYPOCRITICAL SAINT — Maroon × Soft Ivory × Charcoal Design System */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg-base: #141316;
    --bg-surface: #211C20;
    --bg-elevated: #2B2429;
    --bg-input: #19161B;
    --color-maroon: #8B354B;
    --color-maroon-hover: #A44861;
    --color-maroon-deep: #572334;
    --color-maroon-subtle: rgba(139, 53, 75, 0.18);
    --color-maroon-border: rgba(139, 53, 75, 0.45);
    --color-ivory: #F6F0E8;
    --color-beige: #D9C6B0;
    --color-beige-subtle: rgba(217, 198, 176, 0.12);
    --text-primary: #F6F0E8;
    --text-secondary: #B8A9B0;
    --text-muted: #83757C;
    --border-color: #40343C;
    --border-hover: #8B354B;
    --color-success: #44B99A;
    --color-error: #E67C86;
}

body, .gradio-container {
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
    -webkit-font-smoothing: antialiased;
    letter-spacing: -0.01em;
}

/* RTL Arabic First Alignment */
html[dir="rtl"] body, html[dir="rtl"] .gradio-container, .hs-lang-ar {
    font-family: 'Cairo', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}

/* LTR English Alignment */
html[dir="ltr"] body, html[dir="ltr"] .gradio-container, .hs-lang-en {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    direction: ltr !important;
    text-align: left !important;
}

/* Numbers, Equations, Filenames, Code strictly LTR */
.numeric-val, .ltr-text, code, .metric-val, .file-path-badge code, .equation-block, pre {
    direction: ltr !important;
    display: inline-block !important;
    unicode-bidi: isolate !important;
}

/* Master Layout (~1200px max width) */
.hs-app-wrapper {
    max-width: 1200px !important;
    margin: 0 auto !important;
    padding: 16px 20px 40px 20px !important;
}

/* Slim Premium Header */
.app-header-slim {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 14px 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

.header-brand-line {
    display: flex;
    align-items: center;
    gap: 14px;
    flex-wrap: wrap;
}

.brand-monogram {
    display: flex;
    align-items: center;
    justify-content: center;
}

.brand-text-col {
    display: flex;
    flex-direction: column;
}

.brand-title {
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: var(--color-ivory);
    text-transform: uppercase;
    line-height: 1.1;
}

.maroon-text {
    color: var(--color-maroon) !important;
}

.brand-subtitle {
    font-size: 0.84rem;
    font-weight: 600;
    color: var(--color-beige);
    margin-top: 2px;
}

.brand-feature-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.76rem;
    font-weight: 600;
    color: var(--color-beige);
    background: var(--color-maroon-subtle);
    border: 1px solid var(--color-maroon-border);
    padding: 3px 12px;
    border-radius: 20px;
}

.brand-tagline-box {
    display: none;
}
@media (min-width: 900px) {
    .brand-tagline-box {
        display: block;
        font-style: italic;
        color: var(--text-secondary);
        font-size: 0.80rem;
        padding: 4px 12px;
        background: var(--bg-elevated);
        border-radius: 6px;
        border: 1px solid var(--border-color);
    }
}

/* Language Switcher Component */
.hs-lang-switch {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    padding: 2px !important;
    display: inline-flex !important;
}

.hs-lang-switch label {
    border-radius: 6px !important;
    padding: 4px 12px !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    color: var(--text-secondary) !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

.hs-lang-switch label:hover {
    color: var(--color-ivory) !important;
}

.hs-lang-switch label.selected, .hs-lang-switch label:has(input:checked) {
    background: var(--color-maroon) !important;
    color: var(--color-ivory) !important;
    box-shadow: 0 2px 8px rgba(139, 53, 75, 0.4) !important;
}

/* About Drawer */
#about-drawer-panel {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
    animation: fadeIn 0.2s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-6px); }
    to { opacity: 1; transform: translateY(0); }
}

.about-header-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 12px;
    margin-bottom: 16px;
}

.about-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--color-beige);
}

.about-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
    font-size: 0.88rem;
    color: var(--text-secondary);
}

.about-item {
    background: var(--bg-elevated);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 12px 14px;
}

.about-item-label {
    font-size: 0.74rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--color-beige);
    font-weight: 700;
    margin-bottom: 4px;
}

.about-item-val {
    color: var(--text-primary);
    font-weight: 600;
    line-height: 1.4;
}

.about-item-sub {
    font-size: 0.78rem;
    color: var(--text-secondary);
    margin-top: 4px;
}

/* Horizontal Segmented Navigation Tabs */
.tab-nav {
    border-bottom: 1px solid var(--border-color) !important;
    background: transparent !important;
    gap: 8px !important;
    margin-bottom: 20px !important;
}

.tab-nav button {
    background: var(--bg-surface) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-bottom: none !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 11px 22px !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.tab-nav button.selected {
    background: var(--bg-elevated) !important;
    color: var(--color-beige) !important;
    border-color: var(--border-color) !important;
    border-top: 2px solid var(--color-maroon) !important;
    font-weight: 700 !important;
}

.tab-nav button:hover:not(.selected) {
    color: var(--color-ivory) !important;
    background: rgba(139, 53, 75, 0.08) !important;
}

/* Sub-Tabs in Advanced Tools */
.subtabs .tab-nav button {
    font-size: 0.86rem !important;
    padding: 8px 16px !important;
    border-radius: 6px !important;
    border-bottom: 1px solid var(--border-color) !important;
}

.subtabs .tab-nav button.selected {
    border-top: 2px solid var(--color-maroon) !important;
    color: var(--color-beige) !important;
}

/* Containers & Cards */
.gr-box, .gr-panel, .gr-group, .block, .panel {
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
}

/* Input Fields */
input, textarea, select {
    background-color: var(--bg-input) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 6px !important;
    font-size: 0.92rem !important;
    padding: 8px 12px !important;
}

input:focus, textarea:focus, select:focus {
    border-color: var(--color-maroon) !important;
    box-shadow: 0 0 0 1px var(--color-maroon) !important;
    outline: none !important;
}

label span {
    color: var(--color-beige) !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
}

/* Primary Button (Maroon) */
button.primary, button[variant="primary"] {
    background-color: var(--color-maroon) !important;
    color: var(--color-ivory) !important;
    border: 1px solid rgba(217, 198, 176, 0.2) !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    font-size: 0.94rem !important;
    padding: 10px 22px !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

button.primary:hover, button[variant="primary"]:hover {
    background-color: var(--color-maroon-hover) !important;
    box-shadow: 0 4px 16px rgba(139, 53, 75, 0.45) !important;
    transform: translateY(-1px) !important;
}

button.primary:active, button[variant="primary"]:active {
    transform: translateY(0) !important;
}

/* Secondary Button */
button.secondary, button[variant="secondary"] {
    background-color: var(--bg-elevated) !important;
    color: var(--color-ivory) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 8px 16px !important;
    transition: all 0.2s ease !important;
}

button.secondary:hover, button[variant="secondary"]:hover {
    border-color: var(--color-beige) !important;
    color: var(--color-beige) !important;
}

/* Prominent Stego Download Button */
.download-btn-prominent {
    background: linear-gradient(135deg, #8B354B 0%, #A44861 100%) !important;
    color: #F6F0E8 !important;
    border: 1.5px solid #D9C6B0 !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    padding: 14px 24px !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 18px rgba(139, 53, 75, 0.45) !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 10px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}

.download-btn-prominent:hover {
    background: linear-gradient(135deg, #A44861 0%, #B8536E 100%) !important;
    box-shadow: 0 6px 22px rgba(217, 198, 176, 0.3) !important;
    transform: translateY(-2px) !important;
}

/* Results Workspace Styling */
#results-section {
    margin-top: 24px !important;
    padding-top: 16px !important;
    border-top: 1px solid var(--border-color) !important;
}

.file-path-badge {
    background: var(--bg-input);
    border: 1px solid var(--border-color);
    padding: 10px 14px;
    border-radius: 6px;
    font-size: 0.82rem;
    color: var(--text-secondary);
    word-break: break-all;
    margin: 8px 0;
}

.file-path-badge code {
    color: var(--color-beige);
}

/* Quick Metrics Bar */
.quick-metrics-bar {
    display: flex;
    flex-direction: column;
    gap: 8px;
    background: var(--bg-input);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 12px 14px;
    margin: 10px 0;
}

.quick-metric-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.84rem;
}

.quick-metric-label {
    color: var(--text-secondary);
    font-weight: 500;
}

.quick-metric-val {
    color: var(--color-ivory);
    font-weight: 700;
}

.quick-metric-tag {
    font-size: 0.72rem;
    background: var(--color-maroon-subtle);
    color: var(--color-beige);
    border: 1px solid var(--color-maroon-border);
    padding: 1px 6px;
    border-radius: 3px;
    font-weight: 600;
    margin-inline-start: 6px;
}

/* Image Previews: Uniform, contained, no distortion */
.image-preview-container img {
    max-height: 320px !important;
    object-fit: contain !important;
    border-radius: 6px !important;
    background: var(--bg-input) !important;
}

/* Accordions */
.gr-accordion {
    border: 1px solid var(--border-color) !important;
    background: var(--bg-surface) !important;
    border-radius: 8px !important;
    margin-top: 10px !important;
}

.gr-accordion > .label-wrap {
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    padding: 8px 14px !important;
}

/* Notice & Success Banners */
.notice-box {
    padding: 12px 16px;
    border-radius: 6px;
    font-size: 0.88rem;
    margin: 10px 0;
    line-height: 1.4;
}

.notice-error {
    background: rgba(230, 124, 134, 0.12);
    border: 1px solid rgba(230, 124, 134, 0.4);
    color: #F8B4B8;
}

.result-success-banner {
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(68, 185, 154, 0.12);
    border: 1px solid rgba(68, 185, 154, 0.45);
    border-radius: 8px;
    padding: 14px 20px;
    margin: 12px 0 18px 0;
}

.banner-icon {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    background: var(--color-success);
    color: #141316;
    font-weight: 800;
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.banner-title {
    font-size: 0.98rem;
    font-weight: 700;
    color: var(--color-ivory);
}

.banner-sub {
    font-size: 0.84rem;
    color: var(--text-secondary);
    margin-top: 2px;
}

/* Capacity Indicator Bar */
.capacity-counter-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.82rem;
    color: var(--text-secondary);
    margin-top: 4px;
    margin-bottom: 8px;
}

.counter-label {
    font-weight: 600;
    color: var(--text-muted);
}

.counter-val {
    color: var(--text-secondary);
    font-weight: 600;
}

.counter-val-active {
    color: var(--color-beige);
    font-weight: 700;
}

.counter-sub {
    color: var(--text-muted);
    font-size: 0.78rem;
}

.capacity-badge {
    background: var(--bg-elevated);
    border: 1px solid var(--border-color);
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 0.84rem;
    color: var(--color-beige);
    margin-top: 6px;
}

/* Metadata Strip */
.meta-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 8px;
}

.meta-pill {
    font-size: 0.76rem;
    color: var(--text-secondary);
    background: var(--bg-elevated);
    padding: 3px 10px;
    border-radius: 4px;
    border: 1px solid var(--border-color);
    font-weight: 500;
}

.meta-pill-maroon {
    font-size: 0.76rem;
    color: var(--color-beige);
    background: var(--color-maroon-subtle);
    border: 1px solid var(--color-maroon-border);
    padding: 3px 10px;
    border-radius: 4px;
    font-weight: 600;
}

/* Copy Toast */
.copy-toast {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(68, 185, 154, 0.15);
    color: var(--color-success);
    border: 1px solid rgba(68, 185, 154, 0.4);
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.82rem;
    font-weight: 600;
    margin-inline-start: 10px;
    animation: fadeIn 0.15s ease-out;
}

/* Metrics Cards Grid */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
    margin: 14px 0;
}

.metric-card {
    background: var(--bg-elevated);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    transition: border-color 0.2s ease, transform 0.2s ease;
}

.metric-card:hover {
    border-color: var(--color-beige);
}

.metric-label {
    font-size: 0.76rem;
    color: var(--color-beige);
    font-weight: 700;
}

.metric-val {
    font-size: 1.45rem;
    font-weight: 800;
    color: var(--color-ivory);
    letter-spacing: -0.02em;
    display: flex;
    align-items: baseline;
    gap: 6px;
}

.metric-badge {
    font-size: 0.72rem;
    background: var(--color-maroon-subtle);
    color: var(--color-beige);
    border: 1px solid var(--color-maroon-border);
    padding: 1px 6px;
    border-radius: 3px;
    font-weight: 600;
}

.metric-pct {
    font-size: 0.85rem;
    color: var(--color-beige);
    font-weight: 600;
}

.metric-sub {
    font-size: 0.74rem;
    color: var(--text-secondary);
    line-height: 1.35;
}

/* Interactive Before/After Comparison Slider */
.hs-slider-container {
    --slider-pos: 50%;
    position: relative;
    width: 100%;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 8px;
    box-sizing: border-box;
    margin: 12px 0;
}

.hs-slider-viewport {
    position: relative;
    width: 100%;
    height: 380px;
    overflow: hidden;
    border-radius: 6px;
    background: var(--bg-input);
}

.hs-layer-cover {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: contain;
    user-select: none;
    pointer-events: none;
}

.hs-layer-stego-wrap {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    clip-path: inset(0 calc(100% - var(--slider-pos, 50%)) 0 0);
    overflow: hidden;
    pointer-events: none;
}

.hs-layer-stego {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: contain;
    user-select: none;
}

.hs-slider-divider {
    position: absolute;
    top: 0;
    bottom: 0;
    left: var(--slider-pos, 50%);
    width: 2px;
    background: var(--color-maroon);
    transform: translateX(-50%);
    pointer-events: none;
    box-shadow: 0 0 12px rgba(139, 53, 75, 0.75);
}

.hs-slider-divider::after {
    content: "↔";
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: var(--bg-elevated);
    border: 2px solid var(--color-maroon);
    color: var(--color-ivory);
    font-size: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.hs-slider-input {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: ew-resize;
    margin: 0;
    padding: 0;
    z-index: 10;
}

.hs-tag-cover, .hs-tag-stego {
    position: absolute;
    top: 10px;
    padding: 3px 8px;
    font-size: 0.72rem;
    font-weight: 600;
    border-radius: 4px;
    pointer-events: none;
    letter-spacing: 0.02em;
}

.hs-tag-cover {
    right: 12px;
    background: rgba(20, 19, 22, 0.85);
    border: 1px solid var(--border-color);
    color: var(--color-beige);
}

.hs-tag-stego {
    left: 12px;
    background: rgba(139, 53, 75, 0.45);
    border: 1px solid var(--color-maroon);
    color: var(--color-ivory);
}

.hs-slider-caption {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    color: var(--text-secondary);
    padding: 6px 4px 2px 4px;
    font-weight: 500;
}

.hs-slider-hint {
    color: var(--color-beige);
    font-size: 0.74rem;
}

/* Tool Explanatory Sentence Banner */
.tool-intro-banner {
    background: var(--bg-elevated);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 10px 16px;
    margin-bottom: 14px;
    font-size: 0.88rem;
    color: var(--color-beige);
    font-weight: 500;
}

/* Academic Card in Advanced Tools */
.academic-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
}

.academic-card h3 {
    color: var(--color-beige);
    margin-top: 0;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 8px;
    font-size: 1.05rem;
    letter-spacing: 0.02em;
}

.academic-card p, .academic-card li {
    font-size: 0.88rem;
    color: #D3C9D0;
    line-height: 1.6;
}

/* Studio Footer */
.studio-footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.8rem;
    margin-top: 28px;
    padding: 16px 0 6px 0;
    border-top: 1px solid var(--border-color);
    line-height: 1.5;
}

/* Difference Map Legend & Visual Guidance */
.diff-legend-card {
    background: rgba(33, 28, 32, 0.9);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 12px 16px;
    margin-top: 10px;
}
.legend-header {
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--color-warm-beige);
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.legend-items {
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.82rem;
    line-height: 1.4;
}
.legend-indicator {
    width: 14px;
    height: 14px;
    border-radius: 3px;
    flex-shrink: 0;
    display: inline-block;
}
.box-indicator {
    border: 2px solid #FFD166;
    background: rgba(255, 209, 102, 0.18);
    box-shadow: 0 0 4px rgba(0, 0, 0, 0.8);
}
.glow-indicator {
    background: #FFD166;
    border-radius: 50%;
    box-shadow: 0 0 6px rgba(255, 59, 92, 0.95), 0 0 10px rgba(255, 209, 102, 0.85);
}
.zoom-indicator {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
}
.legend-title {
    font-weight: 700;
    color: var(--color-soft-ivory);
    flex-shrink: 0;
}
.legend-desc {
    color: var(--text-secondary);
}
.legend-scientific-note {
    margin-top: 10px;
    padding-top: 8px;
    border-top: 1px solid rgba(64, 52, 60, 0.6);
    font-size: 0.77rem;
    color: var(--text-muted);
    line-height: 1.45;
}

/* Zoomed Change Region Card & Inspection Panel */
.comparison-view-container {
    gap: 16px;
    margin-top: 12px;
}
.zoom-panel-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    height: 100%;
}
.zoom-panel-header {
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(64, 52, 60, 0.8);
}
.zoom-panel-title {
    font-size: 1.02rem;
    font-weight: 700;
    color: var(--color-soft-ivory);
    display: flex;
    align-items: center;
    gap: 6px;
}
.zoom-panel-sub {
    font-size: 0.79rem;
    color: var(--color-warm-beige);
    margin-top: 3px;
    line-height: 1.35;
}
.zoom-region-dropdown {
    margin: 4px 0;
}
.zoom-previews-row {
    gap: 8px;
}
.zoom-thumb-img {
    border: 1px solid #40343C;
    border-radius: 8px;
    background: #141316;
}
.zoom-info-card {
    background: rgba(43, 36, 41, 0.9);
    border: 1px solid #572334;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 0.8rem;
    color: var(--color-soft-ivory);
    margin-top: 4px;
}
.zoom-info-identical {
    border-color: rgba(68, 185, 154, 0.4);
    background: rgba(68, 185, 154, 0.08);
    color: #44B99A;
}
.zoom-meta-row {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px;
}
.zoom-badge {
    background: var(--color-maroon);
    color: #FFF;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 4px;
    border: 1px solid var(--color-maroon-hover);
}
.zoom-stat {
    color: var(--color-soft-ivory);
}
.zoom-stat b {
    color: var(--color-warm-beige);
}
"""


# ==============================================================================
# Dynamic Language Switching Logic
# ==============================================================================

def switch_language_action(selected_lang):
    """Update all UI elements dynamically between Arabic and English."""
    is_ar = (selected_lang == "العربية" or selected_lang == "ar")
    lang = "ar" if is_ar else "en"

    methods = METHODS_AR if is_ar else METHODS_EN
    gens = GENERATORS_AR if is_ar else GENERATORS_EN

    return (
        # 1. Header & Badges
        get_header_html(lang),
        t("btn_about", lang),
        f"<div class='about-title'>{t('about_title', lang)}</div>",
        t("btn_close", lang),
        get_about_drawer_html(lang),
        # 2. Main Navigation Tabs
        gr.update(label=t("tab_hide", lang)),
        gr.update(label=t("tab_reveal", lang)),
        gr.update(label=t("tab_adv", lang)),
        # 3. Hide Message Section
        f"### {t('cover_title', lang)}",
        gr.update(label=t("cover_upload_label", lang)),
        f"### {t('msg_title', lang)}",
        gr.update(label=t("msg_input_label", lang), placeholder=t("msg_placeholder", lang)),
        gr.update(label=t("adv_settings", lang)),
        gr.update(label=t("method_label", lang), choices=methods, value=methods[0]),
        gr.update(label=t("gen_label", lang), choices=gens, value=gens[0], info=t("gen_info", lang)),
        gr.update(label=t("shift_label", lang), info=t("shift_info", lang)),
        gr.update(value=t("btn_calc_rdh", lang)),
        f"<small style='color:#B8A9B0;'>{t('red_info', lang)}</small>",
        gr.update(label=t("enc_label", lang)),
        gr.update(value=t("btn_hide", lang)),
        # Hide Results
        f"#### 🖼️ {t('stego_preview_title', lang)}",
        gr.update(label=t("stego_preview_label", lang)),
        f"#### 💾 {t('actions_title', lang)}",
        gr.update(label=t("btn_download_primary", lang)),
        gr.update(label=t("btn_download_file", lang)),
        gr.update(value=t("btn_forward_reveal", lang)),
        gr.update(value=t("btn_hide_another", lang)),
        f"#### 🔍 {t('slider_title', lang)}",
        gr.update(label=t("diff_map_label", lang)),
        format_diff_legend_html(lang),
        gr.update(label=t("tech_metrics_title", lang)),
        # 4. Reveal Message Section
        f"### {t('stego_upload_title', lang)}",
        gr.update(label=t("stego_upload_label", lang)),
        gr.update(label=t("adv_settings", lang)),
        gr.update(label=t("method_label", lang), choices=methods, value=methods[0]),
        gr.update(label=t("gen_label", lang), choices=gens, value=gens[0]),
        gr.update(label=t("shift_label", lang)),
        gr.update(label=t("enc_label", lang)),
        gr.update(value=t("btn_reveal", lang)),
        f"### {t('extracted_title', lang)}",
        gr.update(label=t("extracted_title", lang), placeholder=t("extracted_placeholder", lang)),
        gr.update(value=t("btn_copy", lang)),
        f"#### 🔄 {t('rdh_restore_title', lang)}",
        f"<small style='color:#B8A9B0;'>{t('rdh_restore_sub', lang)}</small>",
        gr.update(label=t("rdh_ref_label", lang)),
        gr.update(value=t("btn_rdh_restore", lang)),
        gr.update(label=t("rdh_preview_label", lang)),
        gr.update(label=t("btn_download_restored", lang)),
        # 5. Advanced Tools Subtabs & Components
        gr.update(label=t("subtab_compare", lang)),
        f"<div class='tool-intro-banner'>📈 {t('subtab_compare_intro', lang)}</div>",
        gr.update(label=t("cmp_orig_label", lang)),
        gr.update(label=t("cmp_mod_label", lang)),
        gr.update(value=t("btn_compare", lang)),
        gr.update(label=t("cmp_diff_label", lang)),
        format_diff_legend_html(lang),
        format_zoom_header_html(lang),
        gr.update(label=t("select_region_label", lang)),
        gr.update(label=t("zoom_orig_label", lang)),
        gr.update(label=t("zoom_mod_label", lang)),
        gr.update(label=t("zoom_diff_label", lang)),
        gr.update(label=t("subtab_bit", lang)),
        f"<div class='tool-intro-banner'>🔬 {t('subtab_bit_intro', lang)}</div>",
        gr.update(label=t("bit_input_label", lang)),
        gr.update(value=t("btn_bit_exec", lang)),
        gr.update(label=t("bit_output_label", lang)),
        gr.update(label=t("subtab_recovery", lang)),
        f"<div class='tool-intro-banner'>🔄 {t('subtab_recovery_intro', lang)}</div>",
        gr.update(label=t("rec_stego_label", lang)),
        gr.update(label=t("rec_ref_label", lang)),
        gr.update(label=t("enc_label", lang)),
        gr.update(value=t("btn_rec_exec", lang)),
        gr.update(label=t("rec_msg_label", lang)),
        gr.update(label=t("rec_preview_label", lang)),
        gr.update(label=t("btn_download_restored", lang)),
        gr.update(label=t("subtab_about", lang)),
        # 6. Footer
        get_footer_html(lang),
    )


# ==============================================================================
# Application Builder
# ==============================================================================

def build_app():
    """Build the bilingual Arabic/English HYPOCRITICAL SAINT application."""
    initial_lang = "ar"

    with gr.Blocks(title="HYPOCRITICAL SAINT | استوديو إخفاء البيانات في الصور الرقمية") as demo:
        with gr.Column(elem_classes=["hs-app-wrapper", "hs-lang-ar"], elem_id="hs-app-root"):

            # ---------------- Slim Header & Controls ----------------
            with gr.Row(elem_classes=["app-header-slim"]):
                with gr.Column(scale=8, min_width=320):
                    header_display = gr.HTML(get_header_html(initial_lang))

                with gr.Column(scale=4, min_width=240, elem_classes=["header-right-actions"]):
                    with gr.Row():
                        # Language Switcher
                        lang_selector = gr.Radio(
                            choices=["العربية", "English"],
                            value="العربية",
                            label="",
                            show_label=False,
                            container=False,
                            elem_classes=["hs-lang-switch"],
                        )
                        btn_about_toggle = gr.Button(t("btn_about", initial_lang), variant="secondary", size="sm")

            # ---------------- Collapsible About Drawer ----------------
            about_state = gr.State(False)
            with gr.Group(visible=False, elem_id="about-drawer-panel") as about_drawer:
                with gr.Row(elem_classes=["about-header-row"]):
                    about_header_title = gr.HTML(f"<div class='about-title'>{t('about_title', initial_lang)}</div>")
                    btn_about_close = gr.Button(t("btn_close", initial_lang), variant="secondary", size="sm")

                about_drawer_content = gr.HTML(get_about_drawer_html(initial_lang))

            btn_about_toggle.click(
                fn=lambda curr: (not curr, gr.update(visible=not curr)),
                inputs=[about_state],
                outputs=[about_state, about_drawer],
            )

            btn_about_close.click(
                fn=lambda: (False, gr.update(visible=False)),
                inputs=[],
                outputs=[about_state, about_drawer],
            )

            # ---------------- 3 Main Navigation Sections ----------------
            with gr.Tabs() as main_nav:

                # ==============================================================
                # 1. HIDE MESSAGE (إخفاء رسالة)
                # ==============================================================
                with gr.Tab(t("tab_hide", initial_lang), id="tab_hide_msg") as tab_hide_msg:

                    # Initial Input State (2-column balanced layout)
                    with gr.Row():
                        # Column 1: Original Image
                        with gr.Column(scale=5):
                            hide_cover_title = gr.Markdown(f"### {t('cover_title', initial_lang)}")
                            hide_input_image = gr.Image(
                                label=t("cover_upload_label", initial_lang),
                                type="pil",
                                sources=["upload", "clipboard"],
                                elem_classes=["image-preview-container"],
                            )
                            hide_meta_display = gr.HTML()

                            if SAMPLE_LENNA:
                                gr.Examples(
                                    examples=[[SAMPLE_LENNA]],
                                    inputs=[hide_input_image],
                                    label=t("sample_label", initial_lang),
                                )

                        # Column 2: Secret Message & Primary Action
                        with gr.Column(scale=5):
                            hide_msg_title = gr.Markdown(f"### {t('msg_title', initial_lang)}")
                            hide_message = gr.Textbox(
                                label=t("msg_input_label", initial_lang),
                                placeholder=t("msg_placeholder", initial_lang),
                                lines=4,
                            )
                            hide_capacity_display = gr.HTML(update_message_counter("", initial_lang))

                            # Live character & byte counter
                            hide_message.change(
                                fn=lambda m, l: update_message_counter(m, l),
                                inputs=[hide_message, lang_selector],
                                outputs=[hide_capacity_display],
                            )

                            # Collapsible Advanced Settings
                            with gr.Accordion(t("adv_settings", initial_lang), open=False) as hide_accordion:
                                hide_method = gr.Dropdown(
                                    label=t("method_label", initial_lang),
                                    choices=METHODS_AR,
                                    value=METHODS_AR[0],
                                )

                                # LSB Group
                                with gr.Group() as lsb_settings_group:
                                    hide_generator = gr.Dropdown(
                                        label=t("gen_label", initial_lang),
                                        choices=GENERATORS_AR,
                                        value=GENERATORS_AR[0],
                                        info=t("gen_info", initial_lang),
                                    )
                                    hide_shift = gr.Slider(
                                        label=t("shift_label", initial_lang),
                                        minimum=0,
                                        maximum=500,
                                        step=1,
                                        value=0,
                                        info=t("shift_info", initial_lang),
                                    )

                                # RDH Group
                                with gr.Group(visible=False) as rdh_settings_group:
                                    rdh_cap_output = gr.HTML()
                                    btn_check_rdh_cap = gr.Button(t("btn_calc_rdh", initial_lang), size="sm", variant="secondary")

                                # Red Channel Info
                                with gr.Group(visible=False) as red_settings_group:
                                    red_info_display = gr.Markdown(f"<small style='color:#B8A9B0;'>{t('red_info', initial_lang)}</small>")

                                hide_encoding = gr.Radio(
                                    label=t("enc_label", initial_lang),
                                    choices=["UTF-8", "UTF-32LE"],
                                    value="UTF-8",
                                )

                            btn_hide_exec = gr.Button(
                                t("btn_hide", initial_lang),
                                variant="primary",
                                size="lg",
                            )

                            # Instant Status / Error Notice
                            hide_status_box = gr.HTML()

                    # Dynamic update of metadata when image is uploaded
                    hide_input_image.change(
                        fn=lambda img, l: get_image_metadata_html(img, l),
                        inputs=[hide_input_image, lang_selector],
                        outputs=[hide_meta_display],
                    )

                    # Dynamic visibility of advanced settings
                    def toggle_hide_settings(selected_method):
                        norm = normalize_method(selected_method)
                        return (
                            gr.update(visible=(norm == "LSB")),
                            gr.update(visible=(norm == "RDH")),
                            gr.update(visible=(norm == "RED")),
                        )

                    hide_method.change(
                        fn=toggle_hide_settings,
                        inputs=[hide_method],
                        outputs=[lsb_settings_group, rdh_settings_group, red_settings_group],
                    )

                    btn_check_rdh_cap.click(
                        fn=check_rdh_capacity_action,
                        inputs=[hide_input_image, lang_selector],
                        outputs=[rdh_cap_output],
                    )

                    # ==========================================================
                    # Results Workspace (Revealed only after successful hiding)
                    # ==========================================================
                    with gr.Group(visible=False, elem_id="results-section") as results_workspace:
                        gr.HTML("<hr style='border-color: #40343C; margin: 24px 0 16px 0;' />")

                        # Success Banner
                        hide_success_banner = gr.HTML()

                        # Primary 2-Column Result Dashboard
                        with gr.Row():
                            # Column 1: Generated Image Preview
                            with gr.Column(scale=5):
                                hide_res_preview_title = gr.Markdown(f"#### 🖼️ {t('stego_preview_title', initial_lang)}")
                                hide_stego_preview = gr.Image(
                                    label=t("stego_preview_label", initial_lang),
                                    type="pil",
                                    interactive=False,
                                    elem_classes=["image-preview-container"],
                                )

                            # Column 2: Download Center & Fast Actions
                            with gr.Column(scale=5):
                                hide_res_actions_title = gr.Markdown(f"#### 💾 {t('actions_title', initial_lang)}")

                                # Prominent Download Button
                                btn_download_primary = gr.DownloadButton(
                                    label=t("btn_download_primary", initial_lang),
                                    variant="primary",
                                    size="lg",
                                    elem_classes=["download-btn-prominent"],
                                )

                                # Direct File Component
                                btn_download_file = gr.File(
                                    label=t("btn_download_file", initial_lang),
                                    interactive=False,
                                )

                                # Local Disk Path display
                                hide_file_path_info = gr.HTML()

                                # Compact Key Metrics Bar (PSNR, MSE, Changed Pixels)
                                hide_quick_metrics = gr.HTML()

                                with gr.Row():
                                    btn_forward_reveal = gr.Button(
                                        t("btn_forward_reveal", initial_lang),
                                        variant="secondary",
                                        scale=1,
                                    )
                                    btn_hide_another = gr.Button(
                                        t("btn_hide_another", initial_lang),
                                        variant="secondary",
                                        scale=1,
                                    )

                        # Before/After Comparison
                        hide_slider_title = gr.Markdown(f"#### 🔍 {t('slider_title', initial_lang)}")
                        hide_slider_display = gr.HTML()

                        with gr.Row():
                            with gr.Column(scale=1):
                                hide_diff_preview = gr.Image(
                                    label=t("diff_map_label", initial_lang),
                                    type="pil",
                                    interactive=False,
                                    elem_classes=["image-preview-container"],
                                )
                                hide_diff_legend = gr.HTML(format_diff_legend_html(initial_lang))

                        # Collapsible Detailed Analysis
                        with gr.Accordion(t("tech_metrics_title", initial_lang), open=False) as hide_tech_accordion:
                            hide_metrics_detailed = gr.HTML()

                    # Embedding Execution Trigger
                    btn_hide_exec.click(
                        fn=hide_message_workflow,
                        inputs=[
                            hide_input_image,
                            hide_message,
                            hide_method,
                            hide_generator,
                            hide_shift,
                            hide_encoding,
                            lang_selector,
                        ],
                        outputs=[
                            hide_status_box,
                            results_workspace,
                            hide_success_banner,
                            hide_stego_preview,
                            btn_download_primary,
                            btn_download_file,
                            hide_file_path_info,
                            hide_quick_metrics,
                            hide_slider_display,
                            hide_diff_preview,
                            hide_metrics_detailed,
                            btn_forward_reveal,
                        ],
                    ).then(
                        fn=None,
                        js="() => { const el = document.getElementById('results-section'); if(el) { el.scrollIntoView({ behavior: 'smooth', block: 'start' }); } }",
                    )

                    # Reset Action
                    btn_hide_another.click(
                        fn=lambda: (gr.update(visible=False), "", None, ""),
                        inputs=[],
                        outputs=[results_workspace, hide_status_box, hide_input_image, hide_message],
                    ).then(
                        fn=None,
                        js="() => window.scrollTo({ top: 0, behavior: 'smooth' })",
                    )

                # ==============================================================
                # 2. REVEAL MESSAGE (استخراج الرسالة)
                # ==============================================================
                with gr.Tab(t("tab_reveal", initial_lang), id="tab_reveal_msg") as tab_reveal_msg:
                    with gr.Row():
                        with gr.Column(scale=5):
                            reveal_cover_title = gr.Markdown(f"### {t('stego_upload_title', initial_lang)}")
                            reveal_input_image = gr.Image(
                                label=t("stego_upload_label", initial_lang),
                                type="pil",
                                sources=["upload", "clipboard"],
                                elem_classes=["image-preview-container"],
                            )

                            with gr.Accordion(t("adv_settings", initial_lang), open=False) as reveal_accordion:
                                reveal_method = gr.Dropdown(
                                    label=t("method_label", initial_lang),
                                    choices=METHODS_AR,
                                    value=METHODS_AR[0],
                                )
                                with gr.Group() as reveal_lsb_group:
                                    reveal_generator = gr.Dropdown(
                                        label=t("gen_label", initial_lang),
                                        choices=GENERATORS_AR,
                                        value=GENERATORS_AR[0],
                                    )
                                    reveal_shift = gr.Slider(
                                        label=t("shift_label", initial_lang),
                                        minimum=0,
                                        maximum=500,
                                        step=1,
                                        value=0,
                                    )
                                reveal_encoding = gr.Radio(
                                    label=t("enc_label", initial_lang),
                                    choices=["UTF-8", "UTF-32LE"],
                                    value="UTF-8",
                                )

                            btn_reveal_exec = gr.Button(
                                t("btn_reveal", initial_lang),
                                variant="primary",
                                size="lg",
                            )

                        with gr.Column(scale=5):
                            reveal_ext_title = gr.Markdown(f"### {t('extracted_title', initial_lang)}")
                            reveal_status_box = gr.HTML(
                                f"<div class='notice-box' style='background: #19161B; border: 1px solid #40343C; color: #B8A9B0;'>{t('initial_reveal_hint', initial_lang)}</div>"
                            )

                            # Result card (appears only on extraction)
                            with gr.Group(visible=False) as extracted_result_card:
                                reveal_output_text = gr.Textbox(
                                    label=t("extracted_title", initial_lang),
                                    placeholder=t("extracted_placeholder", initial_lang),
                                    lines=8,
                                )

                                with gr.Row():
                                    btn_copy_extracted = gr.Button(t("btn_copy", initial_lang), variant="secondary", size="sm")
                                    gr.HTML(f"<span id='hs-copy-toast' class='copy-toast' style='display:none;'>{t('copied_toast', initial_lang)}</span>")

                                reveal_meta_info = gr.HTML()

                            # Dedicated RDH Reversible Recovery Option
                            with gr.Group(visible=False) as rdh_restore_box:
                                rdh_card_title = gr.Markdown(f"#### 🔄 {t('rdh_restore_title', initial_lang)}")
                                rdh_card_sub = gr.Markdown(f"<small style='color:#B8A9B0;'>{t('rdh_restore_sub', initial_lang)}</small>")
                                rdh_cover_ref_opt = gr.Image(
                                    label=t("rdh_ref_label", initial_lang),
                                    type="pil",
                                    sources=["upload", "clipboard"],
                                    elem_classes=["image-preview-container"],
                                )
                                btn_rdh_restore_exec = gr.Button(
                                    t("btn_rdh_restore", initial_lang),
                                    variant="secondary",
                                )
                                rdh_restore_status = gr.HTML()
                                with gr.Row():
                                    rdh_restored_preview = gr.Image(
                                        label=t("rdh_preview_label", initial_lang),
                                        type="pil",
                                        elem_classes=["image-preview-container"],
                                    )
                                    with gr.Column():
                                        btn_download_restored = gr.DownloadButton(
                                            label=t("btn_download_restored", initial_lang),
                                            variant="primary",
                                        )
                                        rdh_restored_file = gr.File(label="PNG Lossless")
                                rdh_verif_display = gr.HTML()

                    reveal_method.change(
                        fn=lambda m: gr.update(visible=(normalize_method(m) == "LSB")),
                        inputs=[reveal_method],
                        outputs=[reveal_lsb_group],
                    )

                    btn_reveal_exec.click(
                        fn=reveal_message_workflow,
                        inputs=[
                            reveal_input_image,
                            reveal_method,
                            reveal_generator,
                            reveal_shift,
                            reveal_encoding,
                            lang_selector,
                        ],
                        outputs=[
                            reveal_status_box,
                            reveal_output_text,
                            reveal_meta_info,
                            rdh_restore_box,
                            rdh_restored_preview,
                            rdh_verif_display,
                            extracted_result_card,
                        ],
                    )

                    # Copy to clipboard via pure browser JavaScript
                    btn_copy_extracted.click(
                        fn=None,
                        inputs=[reveal_output_text],
                        js="""(text) => {
                            if (!text) return;
                            navigator.clipboard.writeText(text).then(() => {
                                const toast = document.getElementById('hs-copy-toast');
                                if (toast) {
                                    toast.style.display = 'inline-flex';
                                    setTimeout(() => { toast.style.display = 'none'; }, 2400);
                                }
                            });
                        }""",
                    )

                    btn_rdh_restore_exec.click(
                        fn=execute_rdh_cover_restoration,
                        inputs=[reveal_input_image, rdh_cover_ref_opt, reveal_encoding, lang_selector],
                        outputs=[
                            rdh_restore_status,
                            reveal_output_text,
                            rdh_restored_preview,
                            btn_download_restored,
                            rdh_restored_file,
                            rdh_verif_display,
                        ],
                    )

                    # Forwarding from Hide -> Reveal Tab
                    btn_forward_reveal.click(
                        fn=lambda img: (img, gr.Tabs(selected="tab_reveal_msg")),
                        inputs=[hide_stego_preview],
                        outputs=[reveal_input_image, main_nav],
                    )

                # ==============================================================
                # 3. ADVANCED TOOLS (أدوات التحليل) — 4 Compact Options
                # ==============================================================
                with gr.Tab(t("tab_adv", initial_lang), id="tab_adv_tools") as tab_adv_tools:
                    with gr.Tabs(elem_classes=["subtabs"]) as adv_subtabs:

                        # --- Sub-Tool 1: Image Comparison ---
                        with gr.Tab(t("subtab_compare", initial_lang)) as subtab_compare:
                            cmp_intro_html = gr.HTML(f"<div class='tool-intro-banner'>📈 {t('subtab_compare_intro', initial_lang)}</div>")
                            with gr.Row():
                                with gr.Column(scale=5):
                                    adv_cmp_img1 = gr.Image(
                                        label=t("cmp_orig_label", initial_lang),
                                        type="pil",
                                        sources=["upload", "clipboard"],
                                        elem_classes=["image-preview-container"],
                                    )
                                with gr.Column(scale=5):
                                    adv_cmp_img2 = gr.Image(
                                        label=t("cmp_mod_label", initial_lang),
                                        type="pil",
                                        sources=["upload", "clipboard"],
                                        elem_classes=["image-preview-container"],
                                    )

                            btn_adv_compare = gr.Button(
                                t("btn_compare", initial_lang),
                                variant="primary",
                            )

                            adv_cmp_status = gr.HTML()
                            adv_cmp_cards = gr.HTML()

                            with gr.Row(elem_classes=["comparison-view-container"]):
                                # Left Column: Full Difference Map & Legend
                                with gr.Column(scale=5):
                                    adv_cmp_diff = gr.Image(
                                        label=t("cmp_diff_label", initial_lang),
                                        type="pil",
                                        elem_classes=["image-preview-container"],
                                    )
                                    adv_cmp_legend = gr.HTML(format_diff_legend_html(initial_lang))

                                # Right Column: Zoomed Change Region
                                with gr.Column(scale=7):
                                    with gr.Column(elem_classes=["zoom-panel-card"]):
                                        adv_cmp_zoom_header = gr.HTML(format_zoom_header_html(initial_lang))
                                        adv_cmp_region_selector = gr.Dropdown(
                                            label=t("select_region_label", initial_lang),
                                            choices=[],
                                            value=None,
                                            interactive=True,
                                            elem_classes=["zoom-region-dropdown"],
                                        )
                                        with gr.Row(elem_classes=["zoom-previews-row"]):
                                            with gr.Column(scale=1):
                                                adv_cmp_zoom_orig = gr.Image(
                                                    label=t("zoom_orig_label", initial_lang),
                                                    type="pil",
                                                    interactive=False,
                                                    elem_classes=["zoom-thumb-img"],
                                                )
                                            with gr.Column(scale=1):
                                                adv_cmp_zoom_mod = gr.Image(
                                                    label=t("zoom_mod_label", initial_lang),
                                                    type="pil",
                                                    interactive=False,
                                                    elem_classes=["zoom-thumb-img"],
                                                )
                                            with gr.Column(scale=1):
                                                adv_cmp_zoom_diff = gr.Image(
                                                    label=t("zoom_diff_label", initial_lang),
                                                    type="pil",
                                                    interactive=False,
                                                    elem_classes=["zoom-thumb-img"],
                                                )
                                        adv_cmp_zoom_info = gr.HTML()

                            btn_adv_compare.click(
                                fn=compare_images_workflow,
                                inputs=[adv_cmp_img1, adv_cmp_img2, lang_selector],
                                outputs=[
                                    adv_cmp_status,
                                    adv_cmp_diff,
                                    adv_cmp_cards,
                                    adv_cmp_legend,
                                    adv_cmp_zoom_header,
                                    adv_cmp_region_selector,
                                    adv_cmp_zoom_orig,
                                    adv_cmp_zoom_mod,
                                    adv_cmp_zoom_diff,
                                    adv_cmp_zoom_info,
                                ],
                            )

                            adv_cmp_region_selector.change(
                                fn=switch_zoom_region_workflow,
                                inputs=[adv_cmp_img1, adv_cmp_img2, adv_cmp_region_selector, lang_selector],
                                outputs=[
                                    adv_cmp_zoom_orig,
                                    adv_cmp_zoom_mod,
                                    adv_cmp_zoom_diff,
                                    adv_cmp_zoom_info,
                                ],
                            )

                        # --- Sub-Tool 2: Bit Analysis ---
                        with gr.Tab(t("subtab_bit", initial_lang)) as subtab_bit:
                            bit_intro_html = gr.HTML(f"<div class='tool-intro-banner'>🔬 {t('subtab_bit_intro', initial_lang)}</div>")
                            with gr.Row():
                                with gr.Column(scale=5):
                                    adv_steg_input = gr.Image(
                                        label=t("bit_input_label", initial_lang),
                                        type="pil",
                                        sources=["upload", "clipboard"],
                                        elem_classes=["image-preview-container"],
                                    )
                                    btn_adv_steg = gr.Button(
                                        t("btn_bit_exec", initial_lang),
                                        variant="primary",
                                    )
                                with gr.Column(scale=5):
                                    adv_steg_status = gr.HTML()
                                    adv_steg_output = gr.Image(
                                        label=t("bit_output_label", initial_lang),
                                        type="pil",
                                        elem_classes=["image-preview-container"],
                                    )

                            btn_adv_steg.click(
                                fn=parity_analysis_workflow,
                                inputs=[adv_steg_input, lang_selector],
                                outputs=[adv_steg_status, adv_steg_output],
                            )

                        # --- Sub-Tool 3: Image Recovery (RDH) ---
                        with gr.Tab(t("subtab_recovery", initial_lang)) as subtab_recovery:
                            rec_intro_html = gr.HTML(f"<div class='tool-intro-banner'>🔄 {t('subtab_recovery_intro', initial_lang)}</div>")
                            with gr.Row():
                                with gr.Column(scale=5):
                                    rdh_std_stego = gr.Image(
                                        label=t("rec_stego_label", initial_lang),
                                        type="pil",
                                        sources=["upload", "clipboard"],
                                        elem_classes=["image-preview-container"],
                                    )
                                    rdh_std_ref = gr.Image(
                                        label=t("rec_ref_label", initial_lang),
                                        type="pil",
                                        sources=["upload", "clipboard"],
                                        elem_classes=["image-preview-container"],
                                    )
                                    rdh_std_enc = gr.Radio(
                                        label=t("enc_label", initial_lang),
                                        choices=["UTF-8", "UTF-32LE"],
                                        value="UTF-8",
                                    )
                                    btn_rdh_std_exec = gr.Button(
                                        t("btn_rec_exec", initial_lang),
                                        variant="primary",
                                    )
                                with gr.Column(scale=5):
                                    rdh_std_status = gr.HTML()
                                    rdh_std_msg = gr.Textbox(
                                        label=t("rec_msg_label", initial_lang),
                                        lines=4,
                                    )
                                    with gr.Row():
                                        rdh_std_preview = gr.Image(
                                            label=t("rec_preview_label", initial_lang),
                                            type="pil",
                                            elem_classes=["image-preview-container"],
                                        )
                                        with gr.Column():
                                            btn_download_std_rec = gr.DownloadButton(
                                                label=t("btn_download_restored", initial_lang),
                                                variant="primary",
                                            )
                                            rdh_std_file = gr.File(label="PNG Lossless")
                                    rdh_std_verif = gr.HTML()

                            btn_rdh_std_exec.click(
                                fn=execute_rdh_cover_restoration,
                                inputs=[rdh_std_stego, rdh_std_ref, rdh_std_enc, lang_selector],
                                outputs=[
                                    rdh_std_status,
                                    rdh_std_msg,
                                    rdh_std_preview,
                                    btn_download_std_rec,
                                    rdh_std_file,
                                    rdh_std_verif,
                                ],
                            )

                        # --- Sub-Tool 4: About & Theory ---
                        with gr.Tab(t("subtab_about", initial_lang)) as subtab_about:
                            about_theory_html = gr.HTML(
                                r"""
                                <div class="academic-card">
                                    <h3>🏛️ البيانات الأكاديمية والتوثيق الرسمي | Academic Information</h3>
                                    <p><b>اسم المشروع:</b> HYPOCRITICAL SAINT</p>
                                    <p><b>الوصف:</b> استوديو إخفاء البيانات في الصور الرقمية (Digital Image Steganography Studio)</p>
                                    <p><b>الشعار:</b> <i>“بريء في الظاهر.. وسرّي في الباطن — Innocent on the Outside. Secret on the Inside.”</i></p>
                                    <p><b>المادة الأكاديمية:</b> معالجة الصور الرقمية (Digital Image Processing - DIP)</p>
                                    <p><b>المطوّر:</b> <b>أم البنين عواد (Um Al-Baneen Awwad)</b></p>
                                    <p><b>القسم:</b> قسم هندسة الحاسوب (Department of Computer Engineering)</p>
                                    <p><b>الكلية والجامعة:</b> كلية الهندسة — جامعة البصرة (University of Basrah)</p>
                                    <p><b>العام الدراسي:</b> 2026–2027</p>
                                </div>

                                <div class="academic-card">
                                    <h3>🔬 مفاهيم معالجة الصور الرقمية المطبقة | Digital Image Processing Concepts</h3>
                                    <ul>
                                        <li><b>تمثيل الصورة في المجال المكاني (Spatial Domain):</b> تُمثّل الصورة الرقمية كمصفوفة ثنائية الأبعاد $f(x, y)$ ذات مستويات إضاءة مكممة $[0, 255]$ موزعة على قنوات الألوان الثلاث (الأحمر، الأخضر، الأزرق).</li>
                                        <li><b>تعديل البت الأقل أهمية (LSB Substitution):</b> إخفاء بتات الرسالة السرية داخل البت $b_0$ لقيم البكسلات يغير شدة الإضاءة بمقدار $\pm 1$ فقط (أقل من $0.39\%$ فرق نسبي)، وهو ما يقع تماماً تحت عتبة التمييز للنظام البصري البشري (HVS).</li>
                                        <li><b>التوزيع الرياضي للبكسلات (Coordinate Traversal):</b> تشتيت مسار تضمين الرسالة عبر متتاليات رياضية (فيبوناتشي، أعداد أولية، ميرسين، فيرما) يمنع التكتل البصري ويقاوم الفحص الإحصائي المتسلسل.</li>
                                        <li><b>الإخفاء العكسي التام (Reversible Data Hiding - RDH):</b> تقنية قائمة على إزاحة المدرج التكراري (Ni et al., 2006) تسمح باستخراج الرسالة واسترجاع صورة الغلاف الأصلية بدقة $100\%$ ($\text{MSE} = 0$, $\text{PSNR} = \infty$).</li>
                                        <li><b>التقييم الرياضي لجودة الصورة:</b> حساب دقيق لمعياري متوسط مربع الخطأ (MSE) ونسبة ذروة الإشارة إلى الضوضاء (PSNR بدلالة dB).</li>
                                    </ul>
                                </div>

                                <div class="academic-card">
                                    <h3>📜 الحقوق والبرمجيات مفتوحة المصدر | Attribution & Credits</h3>
                                    <p>تم تصميم وبرمجة وتطوير هذا الاستوديو الأكاديمي بواسطة <b>أم البنين عواد</b> ضمن متطلبات مادة معالجة الصور الرقمية.</p>
                                    <p>تعتمد خوارزميات الإخفاء الأساسية على مكتبة <b>Stegano</b> مفتوحة المصدر من تطوير <b>Cédric Bonhomme</b> والمساهمين تحت رخصة <b>GNU General Public License v3.0 (GPL-3.0)</b>.</p>
                                </div>
                                """
                            )

            # ---------------- Studio Footer ----------------
            footer_display = gr.HTML(get_footer_html(initial_lang))

        # Dynamic Language Switching Event Binding
        lang_selector.change(
            fn=switch_language_action,
            inputs=[lang_selector],
            outputs=[
                header_display,
                btn_about_toggle,
                about_header_title,
                btn_about_close,
                about_drawer_content,
                tab_hide_msg,
                tab_reveal_msg,
                tab_adv_tools,
                hide_cover_title,
                hide_input_image,
                hide_msg_title,
                hide_message,
                hide_accordion,
                hide_method,
                hide_generator,
                hide_shift,
                btn_check_rdh_cap,
                red_info_display,
                hide_encoding,
                btn_hide_exec,
                hide_res_preview_title,
                hide_stego_preview,
                hide_res_actions_title,
                btn_download_primary,
                btn_download_file,
                btn_forward_reveal,
                btn_hide_another,
                hide_slider_title,
                hide_diff_preview,
                hide_diff_legend,
                hide_tech_accordion,
                reveal_cover_title,
                reveal_input_image,
                reveal_accordion,
                reveal_method,
                reveal_generator,
                reveal_shift,
                reveal_encoding,
                btn_reveal_exec,
                reveal_ext_title,
                reveal_output_text,
                btn_copy_extracted,
                rdh_card_title,
                rdh_card_sub,
                rdh_cover_ref_opt,
                btn_rdh_restore_exec,
                rdh_restored_preview,
                btn_download_restored,
                subtab_compare,
                cmp_intro_html,
                adv_cmp_img1,
                adv_cmp_img2,
                btn_adv_compare,
                adv_cmp_diff,
                adv_cmp_legend,
                adv_cmp_zoom_header,
                adv_cmp_region_selector,
                adv_cmp_zoom_orig,
                adv_cmp_zoom_mod,
                adv_cmp_zoom_diff,
                subtab_bit,
                bit_intro_html,
                adv_steg_input,
                btn_adv_steg,
                adv_steg_output,
                subtab_recovery,
                rec_intro_html,
                rdh_std_stego,
                rdh_std_ref,
                rdh_std_enc,
                btn_rdh_std_exec,
                rdh_std_msg,
                rdh_std_preview,
                btn_download_std_rec,
                subtab_about,
                footer_display,
            ],
        ).then(
            fn=None,
            js="""(lang) => {
                const isAr = (lang === 'العربية' || lang === 'ar');
                document.documentElement.dir = isAr ? 'rtl' : 'ltr';
                document.documentElement.lang = isAr ? 'ar' : 'en';
                const root = document.getElementById('hs-app-root');
                if (root) {
                    if (isAr) {
                        root.classList.add('hs-lang-ar');
                        root.classList.remove('hs-lang-en');
                    } else {
                        root.classList.add('hs-lang-en');
                        root.classList.remove('hs-lang-ar');
                    }
                }
            }""",
            inputs=[lang_selector],
        )

    return demo


if __name__ == "__main__":
    app = build_app()
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=False,
        share=False,
        css=MAROON_DESIGN_SYSTEM_CSS,
        head="<script>document.documentElement.dir = 'rtl'; document.documentElement.lang = 'ar';</script>",
    )
