import unittest
import numpy as np
from PIL import Image
from pathlib import Path
import app

class TestDifferenceVisualization(unittest.TestCase):
    """Unit tests for the Difference Map visibility improvements, cluster detection, and zoomed views."""

    def setUp(self):
        sample_path = Path("tests/sample-files/Lenna.png")
        if not sample_path.exists():
            self.skipTest(f"Sample file {sample_path} not found")
        self.orig_img = Image.open(sample_path).convert("RGB")
        self.arr_orig = np.array(self.orig_img, dtype=np.uint8)

    def test_subtle_change_detection_and_metrics(self):
        """Test with an image where only 25 pixels changed."""
        arr_mod = self.arr_orig.copy()
        for dy in range(5):
            for dx in range(5):
                y = 100 + dy
                x = 100 + dx
                arr_mod[y, x, 0] = (int(arr_mod[y, x, 0]) + 1) % 256

        mod_img = Image.fromarray(arr_mod)
        metrics = app.calculate_metrics(self.orig_img, mod_img, lang="ar")

        # Scientific metrics must be exact and unaltered
        self.assertEqual(metrics["changed_count"], 25)
        self.assertEqual(metrics["max_delta"], 1)
        self.assertGreater(metrics["psnr_val"], 70.0)

        # Cluster detection
        clusters = metrics["clusters"]
        self.assertGreaterEqual(len(clusters), 1)
        self.assertEqual(clusters[0]["pixel_count"], 25)

        # Zoomed views
        self.assertIsNotNone(metrics["zoom_orig"])
        self.assertIsNotNone(metrics["zoom_mod"])
        self.assertIsNotNone(metrics["zoom_diff"])
        self.assertIsNotNone(metrics["zoom_info"])
        self.assertEqual(metrics["zoom_info"]["pixel_count"], 25)

    def test_compare_workflow_outputs(self):
        """Verify compare_images_workflow returns all 10 components with proper translations."""
        arr_mod = self.arr_orig.copy()
        arr_mod[50:55, 50:55, 1] = (int(arr_mod[50, 50, 1]) + 1) % 256
        mod_img = Image.fromarray(arr_mod)

        # Arabic
        res_ar = app.compare_images_workflow(self.orig_img, mod_img, "العربية")
        self.assertEqual(len(res_ar), 10)
        self.assertIn("تكبير منطقة التغيّر", res_ar[4])
        self.assertIn("المربع الذهبي", res_ar[3])

        # English
        res_en = app.compare_images_workflow(self.orig_img, mod_img, "English")
        self.assertEqual(len(res_en), 10)
        self.assertIn("Zoomed Change Region", res_en[4])
        self.assertIn("Highlight Box", res_en[3])

    def test_switch_zoom_region(self):
        """Verify dynamic cluster switching via dropdown choice."""
        arr_mod = self.arr_orig.copy()
        for dy in range(5):
            for dx in range(5):
                y = 80 + dy
                x = 80 + dx
                arr_mod[y, x, 2] = (int(arr_mod[y, x, 2]) + 1) % 256
        mod_img = Image.fromarray(arr_mod)

        choice = "Region #1 — Pos (80, 80) — [25 pixels]"
        res = app.switch_zoom_region_workflow(self.orig_img, mod_img, choice, "English")
        self.assertEqual(len(res), 4)
        self.assertIsNotNone(res[0])
        self.assertIsNotNone(res[1])
        self.assertIsNotNone(res[2])
        self.assertIn("25", res[3])

    def test_identical_images_zero_difference(self):
        """Verify handling of completely identical images without errors."""
        metrics = app.calculate_metrics(self.orig_img, self.orig_img, lang="ar")
        self.assertEqual(metrics["changed_count"], 0)
        self.assertEqual(metrics["mse"], 0.0)
        self.assertEqual(metrics["psnr_str"], "∞ dB")
        self.assertEqual(len(metrics["clusters"]), 0)

        res = app.compare_images_workflow(self.orig_img, self.orig_img, "العربية")
        self.assertEqual(len(res), 10)
        self.assertIn("الصورتان متطابقتان تماماً", res[9])


if __name__ == "__main__":
    unittest.main()
