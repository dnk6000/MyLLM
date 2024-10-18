from PIL import Image, ImageDraw, ImageFont
import re

import config

def add_title_to_image(fname: str, title: str, fname_modified: str) -> None:

    # Текст, который нужно добавить
    text = title #"Have some FUN Have some FUN Have some FUN Have some FUN Have some FUN Have some FUN"

    # Открываем изображение
    img = Image.open(fname).convert('RGBA')

    # Создаем объект для рисования на изображении
    draw = ImageDraw.Draw(img)

    # Задаем шрифт и размер шрифта
    font = ImageFont.truetype(f'{config.PROJECT_FOLDER}\\fonts\\FreeMono.ttf', 50)

    # Получаем размеры изображения
    img_width, img_height = img.size

    # Задаем начальную позицию для текста
    x, y = 10, 10

    # Разбиваем текст на строки по переносу
    lines = []
    line = ""
    for word in text.split():
        # if draw.textlength(line + word, font) <= img_width - 200:
        if draw.textlength(line + word, font) <= img_width:
            line += word + " "
        else:
            lines.append(line.strip())
            line = word + " "
    lines.append(line.strip())

    # Получаем высоту строки
    ascent, descent = font.getmetrics()
    line_height = ascent + descent

    # Получаем размеры текста
    text_width = max(draw.textlength(line, font) for line in lines)
    text_height = line_height * len(lines)

    # Создаем новый слой с темно-синим цветом и прозрачностью 70%
    overlay = Image.new('RGBA', (int(text_width), int(text_height)), (0, 0, 128, 180))

    # Объединяем изображение и слой с помощью наложения
    img.paste(overlay, (int(x), int(y)), mask=overlay)

    # Добавляем текст на изображение, перенося на новую строку при необходимости
    for line in lines:
        draw.text((x, y), line, font=font, fill=(255, 0, 0))
        y += line_height

    # Удаляем альфа-канал
    img = img.convert("RGB")

    # Сохраняем изображение в формате JPEG
    img.save(fname_modified)

def add_title_to_image_with_format(fname: str, title: str, fname_modified: str) -> None:
    # Текст, который нужно добавить
    text = title

    # Настройки текста
    text_color = "red"
    text_bg_color = "navy"
    text_bg_opacity = 70  # Прозрачность фона текста (0-100)
    text_size = 50  # Размер шрифта
    text_font_style = "normal"  # Стиль шрифта: normal, bold, italic, bold_italic

    # Настройки стикера
    sticker_number = 10  # Номер стикера
    sticker_format = "png"  # Формат изображения стикера (png, webp, etc.)
    sticker_size = 50  # Размер стикера
    sticker_folder = "downloads/donutthedog/png"  # Путь к папке с файлами стикеров

    # Открываем изображение
    img = Image.open(fname).convert('RGBA')

    # Создаем объект для рисования на изображении
    draw = ImageDraw.Draw(img)

    # Задаем шрифт, стиль шрифта и размер шрифта
    font_styles = {
        "normal": ImageFont.truetype(f'{config.PROJECT_FOLDER}\\fonts\\FreeMono.ttf', text_size),
        "bold": ImageFont.truetype(f'{config.PROJECT_FOLDER}\\fonts\\FreeMonoBold.ttf', text_size),
        "italic": ImageFont.truetype(f'{config.PROJECT_FOLDER}\\fonts\\FreeMonoOblique.ttf', text_size),
        "bold_italic": ImageFont.truetype(f'{config.PROJECT_FOLDER}\\fonts\\FreeMonoBoldOblique.ttf', text_size)
    }
    font = font_styles["normal"]
    bold_font = font_styles["bold"]
    italic_font = font_styles["italic"]
    bold_italic_font = font_styles["bold_italic"]

    # Получаем размеры изображения
    img_width, img_height = img.size

    # Задаем начальную позицию для текста
    x, y = 10, 10

    # Обрабатываем текст с учетом разметки
    lines = []
    for line in text.split("\n"):
        formatted_line = []
        current_font = font
        parts = re.split(r'(\*{1,2}(?:(?!\*{1,2}).)*?\*{1,2}|_{1,2}(?:(?!_{1,2}).)*?_{1,2}|#{1,6}\s?.+)', line)
        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                current_font = bold_font
                part = part[2:-2]
            elif part.startswith("*") and part.endswith("*"):
                current_font = italic_font
                part = part[1:-1]
            elif part.startswith("_") and part.endswith("_"):
                current_font = italic_font
                part = part[1:-1]
            elif part.startswith("#"):
                current_font = bold_font
                part = part.lstrip("# ")
            else:
                current_font = font
            formatted_line.append((current_font, part))
        lines.append(formatted_line)

    # Получаем высоту строки
    line_height = max(font.getmetrics()[0], bold_font.getmetrics()[0], italic_font.getmetrics()[0])
    # Добавляем текст на изображение, перенося на новую строку при необходимости
    text_color_rgb = {"red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255)}[text_color]
    for line in lines:
        line_width = 0
        for font, part in line:
            if part.strip():  # Проверяем, что часть строки не пустая и не состоит только из пробелов
                draw.text((x + line_width, y), part, font=font, fill=text_color_rgb)
                line_width += draw.textlength(part, font)
        y += line_height

    # Создаем новый слой с цветом фона текста и прозрачностью
    text_bg_color_rgb = {"red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255), "navy": (0, 0, 128)}[
        text_bg_color]
    text_width = max(line_width for line in lines)
    text_height = y + 10
    overlay = Image.new('RGBA', (int(text_width), int(text_height)),
                        text_bg_color_rgb + (int(255 * (100 - text_bg_opacity) / 100),))

    # Объединяем изображение и слой с помощью наложения
    img.paste(overlay, (int(x), int(10)), mask=overlay)

    # Рисуем стикер в правом нижнем углу
    # sticker_files = [f for f in os.listdir(sticker_folder) if f.endswith(f".{sticker_format}")]
    # sticker_name = [f for f in sticker_files if str(sticker_number) in f.split("+")[0]][0]
    # sticker_path = f"{sticker_folder}/{sticker_name}"
    # sticker_image = Image.open(sticker_path)
    # if sticker_image:
    #    sticker_image = sticker_image.resize((sticker_size, sticker_size))
    #    img.paste(sticker_image, (img_width - sticker_size - 10, img_height - sticker_size - 10), mask=sticker_image)

    # Сохраняем изображение в формате PNG
    img.save(fname_modified,format='png')

if __name__ == "__main__":
    # add_title_to_image(fname=f"{config.DATA_FOLDER}\\story.jpg",
    #                    title="Echoes of the Digital Future",
    #                    fname_modified=f"{config.DATA_FOLDER}\\story_title.jpg")
    add_title_to_image_with_format(fname=f"{config.DATA_FOLDER}\\story.jpg",
                                   title="*Echoes* of the **Digital Future**",
                                   fname_modified=f"{config.DATA_FOLDER}\\story_title2.png")

