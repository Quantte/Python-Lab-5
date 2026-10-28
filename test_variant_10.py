import csv
import tempfile
import unittest
from pathlib import Path

import variant_10


LAB_DIR = Path(__file__).resolve().parent


class Variant10Tests(unittest.TestCase):
    def test_task1_finds_words_before_period_and_fractional_numbers(self):
        text = "Alpha. beta, gamma. 0.5 10,25 17/18 and 9178-81."

        words, fractions = variant_10.find_task1_values(text)

        self.assertEqual(words, ["Alpha", "gamma"])
        self.assertEqual(fractions, ["0.5", "10,25", "17/18"])

    def test_task1_real_russian_text_contains_expected_fragments(self):
        text = (LAB_DIR / "task1-ru.txt").read_text(encoding="utf-8")

        words, fractions = variant_10.find_task1_values(text)

        self.assertEqual(len(words), 72)
        self.assertEqual(len(fractions), 21)
        self.assertIn("Введение", words)
        self.assertIn("скоростях", words)
        self.assertIn("0,3", fractions)
        self.assertIn("0,5", fractions)
        self.assertIn("0,8", fractions)
        self.assertEqual(fractions.count("17/18"), 3)

    def test_task2_finds_integer_decimal_and_negative_pixel_values(self):
        text = "width: 10px; margin: -2px; height: 1.5px; ratio: 2; name: x10px"

        self.assertEqual(
            variant_10.find_pixel_values(text),
            ["10px", "-2px", "1.5px"],
        )

    def test_task2_real_html_finds_all_pixel_values(self):
        text = (LAB_DIR / "task2.html").read_text(encoding="utf-8")

        values = variant_10.find_pixel_values(text)

        self.assertEqual(len(values), 70)
        self.assertIn("320px", values)
        self.assertIn("-9999px", values)

    def test_task3_parses_each_five_field_record_without_mixing_site_and_email(self):
        text = (
            "user@example.com Smith 2024-01-02 https://example.com/ 2 "
            "1 http://site.org/ 2023-12-31 Jones other@site.org"
        )

        rows = variant_10.parse_task3_records(text)

        self.assertEqual(
            rows,
            [
                ["2", "Smith", "user@example.com", "2024-01-02", "https://example.com/"],
                ["1", "Jones", "other@site.org", "2023-12-31", "http://site.org/"],
            ],
        )

    def test_task3_real_file_parses_all_250_records(self):
        text = (LAB_DIR / "task3.txt").read_text(encoding="utf-8")

        rows = variant_10.parse_task3_records(text)

        self.assertEqual(len(rows), 250)
        self.assertEqual(
            rows[0],
            [
                "1",
                "Callahan",
                "urangel@espinoza-francis.net",
                "2020-08-26",
                "http://www.escobar.org/",
            ],
        )
        self.assertEqual(
            rows[-1],
            [
                "250",
                "Shea",
                "burnettrebecca@brewer.info",
                "2021-02-01",
                "http://www.tyler-sosa.biz/",
            ],
        )

    def test_task3_writes_csv_in_required_column_order(self):
        rows = [["1", "Smith", "user@example.com", "2024-01-02", "https://example.com/"]]

        with tempfile.TemporaryDirectory() as directory:
            output_path = Path(directory) / "result.csv"
            variant_10.write_task3_csv(rows, output_path)
            with output_path.open(encoding="utf-8", newline="") as file:
                saved_rows = list(csv.reader(file))
            saved_bytes = output_path.read_bytes()

        self.assertEqual(saved_rows, rows)
        self.assertNotIn(b"\r", saved_bytes)

    def test_extra_task_finds_the_real_five_dates_emails_and_sites(self):
        text = (LAB_DIR / "task_add.txt").read_text(encoding="utf-8")

        dates, emails, sites = variant_10.find_hidden_values(text)

        self.assertEqual(
            dates,
            ["2015-06-11", "07.22.1996", "18.03.2001", "2011/01/08", "24-02-2021"],
        )
        self.assertEqual(
            emails,
            [
                "sampleName@inbox.ru",
                "alkatraz69@samp.le",
                "thAnk_U@mas.ter",
                "find@me.now",
                "hidden@mail.ru",
            ],
        )
        self.assertEqual(
            sites,
            [
                "https://ilovedra.mas",
                "http://dumbsi.tee",
                "https://imtir.ed",
                "http://boulevard.com",
                "https://notscumreal.ly",
            ],
        )


if __name__ == "__main__":
    unittest.main()
