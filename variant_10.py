import csv
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

WORD_BEFORE_PERIOD = re.compile(r"[^\W\d_]+(?=\.)")
FRACTION_NUMBER = re.compile(r"\d+[.,/]\d+")

PIXEL_VALUE = re.compile(r"(?<![\w.])-?(?:\d+(?:\.\d+)?|\.\d+)px\b")

ID = re.compile(r"\d+")
SURNAME = re.compile(r"[A-Z][a-z]+(?:-[A-Z][a-z]+)?")
EMAIL = re.compile(r"\S+@\S+\.\S+")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
SITE = re.compile(r"https?://[\w-]+(?:\.[\w-]+)+/")

FIELD_PATTERNS = {
    "id": ID,
    "surname": SURNAME,
    "email": EMAIL,
    "date": DATE,
    "site": SITE,
}

HIDDEN_DATE = re.compile(
    r" (\d{1,2}[./-]\d{1,2}[./-]\d{4}|\d{4}[./-]\d{1,2}[./-]\d{1,2})"
)
# В этом учебном файле доменные окончания состоят из 2-3 строчных букв.
# Шум справа может начинаться с буквы, поэтому ru проверяется отдельно.
# Эти выражения извлекают данные из данного файла, а не проверяют любые домены.
HIDDEN_EMAIL = re.compile(
    r" ([\w.%+-]+@[\w-]+(?:\.[\w-]+)*\.(?:ru|[a-z]{2,3}))"
)
HIDDEN_SITE = re.compile(
    r" (https?://[\w-]+(?:\.[\w-]+)*\.(?:ru|[a-z]{2,3}))"
)



def find_task1_values(text):
    words = WORD_BEFORE_PERIOD.findall(text)
    fractions = FRACTION_NUMBER.findall(text)
    return words, fractions


def find_pixel_values(text):
    return PIXEL_VALUE.findall(text)


def parse_task3_records(text):
    tokens = text.split()
    if len(tokens) % 5 != 0:
        raise ValueError("Каждая запись должна содержать 5 полей")

    rows = []
    for start in range(0, len(tokens), 5):
        record = tokens[start : start + 5]
        fields = {}

        for value in record:
            field_names = [
                name for name, pattern in FIELD_PATTERNS.items() if pattern.fullmatch(value)
            ]
            if len(field_names) != 1 or field_names[0] in fields:
                raise ValueError(f"Не удалось распознать запись: {' '.join(record)}")
            fields[field_names[0]] = value

        if len(fields) != 5:
            raise ValueError(f"В записи не хватает полей: {' '.join(record)}")

        rows.append(
            [
                fields["id"],
                fields["surname"],
                fields["email"],
                fields["date"],
                fields["site"],
            ]
        )

    return rows


def write_task3_csv(rows, output_path):
    with Path(output_path).open("w", encoding="utf-8", newline="") as file:
        csv.writer(file, lineterminator="\n", delimiter=";").writerows(rows)


def find_hidden_values(text):
    dates = HIDDEN_DATE.findall(text)
    emails = HIDDEN_EMAIL.findall(text)
    sites = HIDDEN_SITE.findall(text)
    return dates, emails, sites


def main():
    task1_text = (BASE_DIR / "task1-ru.txt").read_text(encoding="utf-8")
    task2_text = (BASE_DIR / "task2.html").read_text(encoding="utf-8")
    task3_text = (BASE_DIR / "task3.txt").read_text(encoding="utf-8")
    extra_text = (BASE_DIR / "task_add.txt").read_text(encoding="utf-8")

    words, fractions = find_task1_values(task1_text)
    pixels = find_pixel_values(task2_text)
    rows = parse_task3_records(task3_text)
    dates, emails, sites = find_hidden_values(extra_text)

    output_path = BASE_DIR / "task3_result.csv"
    write_task3_csv(rows, output_path)

    print(f"Задание 1, слова перед точкой: {len(words)}")
    print(words)
    print()
    print(f"Задание 1, дробные числа: {len(fractions)}")
    print(fractions)
    print()
    print(f"Задание 2, значения в пикселях: {len(pixels)}")
    print(pixels)
    print()
    print(f"Задание 3, записей сохранено: {len(rows)}")
    print(f"CSV: {output_path}")
    print(f"Дополнительное задание, даты: {len(dates)}")
    print(dates)
    print()
    print(f"Дополнительное задание, email: {len(emails)}")
    print(emails)
    print()
    print(f"Дополнительное задание, сайты: {len(sites)}")
    print(sites)


if __name__ == "__main__":
    main()
