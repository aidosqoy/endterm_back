import os
import re
import uuid
from flask import current_app
from werkzeug.utils import secure_filename
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
from app.models import Student
from app.utils.ner_utils import extract_person_names


def process_pdf_file(file, user_id):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)

    images = convert_from_bytes(file.read(), dpi=300)
    if not images:
        raise ValueError("PDF файл пуст или не может быть конвертирован в изображение")
    image = images[0]

    text = pytesseract.image_to_string(image, lang='kaz+eng')
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    person_names = extract_person_names(text)
    full_name_raw = " ".join(person_names)
    full_name_clean = clean_name(full_name_raw)

    last_name, first_name, patronymic = split_kazakh_fullname(full_name_clean.split())

    profession = ""
    for line in lines:
        match = re.search(r'В[А-ЯA-Z]*\d{2,3}\s+(.+)', line)
        if match:
            profession = match.group(1).strip()
            break

    course = ""
    for line in lines:
        match = re.search(r'(\d).*\d{2}\.\d{2}\.\d{4}', line)
        if match:
            course = match.group(1)
            break

    avatar_crop = image.crop((450, 913, 981, 1611))
    avatar_filename = secure_filename(f"avatar_{uuid.uuid4().hex}.jpg")
    avatar_path = os.path.join(upload_folder, avatar_filename)
    avatar_crop.save(avatar_path)

    student = Student(
        first_name=first_name,
        last_name=last_name,
        patronymic=patronymic,
        course=course,
        profession=profession,
        image=avatar_filename,
        user_id=user_id,
    )

    return student, {
        "first_name": first_name,
        "last_name": last_name,
        "patronymic": patronymic,
        "course": course,
        "profession": profession,
        "image": avatar_filename,
    }


def clean_name(name: str) -> str:
    name = re.sub(r"[^А-Яа-яA-Za-zӘәӨөҰұҮүІіҢңҚқҒғЁё\- ]", "", name)
    name = re.sub(r"\bЖЖОКБ[А-ЯӘӨҰҮІҢҚҒ]+\b", "", name, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", name).strip()


def split_kazakh_fullname(words):
    last, first, patronymic = "", "", ""
    if len(words) == 3:
        last, first, patronymic = words
    elif len(words) == 2:
        first_word, second_word = words
        if any(suffix in second_word.lower() for suffix in ['ұлы', 'қызы','вич', 'овна']):
            first = first_word
            patronymic = second_word
        else:
            last = first_word
            first = second_word
    elif len(words) == 1:
        first = words[0]
    return last, first, patronymic
