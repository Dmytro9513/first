import os
import shutil
import re


# Транслітерація кириличних символів на латиницю
def normalize(text, translit_dict):
    normalized_text = ""
    for char in text:
        if char.isalpha() and char.isascii():
            normalized_text += char
        elif char in translit_dict:
            normalized_text += translit_dict[char]
        else:
            normalized_text += "_"


    invalid_chars = r'[^\w.]' # Заміна неприпустимих символів на символ '_'
    normalized_text = re.sub(invalid_chars, '_', normalized_text)

    return normalized_text


def process_folder(folder):
    image_extensions = ('JPEG', 'PNG', 'JPG', 'SVG')
    video_extensions = ('AVI', 'MP4', 'MOV', 'MKV')
    document_extensions = ('DOC', 'DOCX', 'PAGES', 'TXT', 'PDF', 'XLSX', 'PPTX')
    audio_extensions = ('MP3', 'OGG', 'WAV', 'AMR')
    archive_extensions = ('ZIP', 'GZ', 'TAR')

    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g',
        'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
        'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
        'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ь': '', 'ў': 'u', 'ы': 'y', 'э': 'e', 'ю': 'iu',
        'я': 'ia', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H',
        'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'Ye', 'Ж': 'Zh',
        'З': 'Z', 'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y',
        'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O',
        'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh',
        'Щ': 'Shch', 'Ь': '', 'Ў': 'U', 'Ы': 'Y', 'Э': 'E',
        'Ю': 'Yu', 'Я': 'Ya', 
        '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '0': '0',
    }

    known_extensions = set() #список відомих (розпізнаних) розширень файлів
    unknown_extensions = set() #список невідомих (нерозпізнаних) розширень файлів

    for root, dirs, files in os.walk(folder):
        for file in files:
            file_extension = file.split(".")[-1].upper() #розширення файлу
            file_path = os.path.join(root, file) #повний шлях до файлу
            normalized_file_name = normalize(file.split(".")[0], translit_dict) + "." + file_extension #нормалізоване ім'я файлу

            #розсортування файлів
            if file_extension in image_extensions:
                known_extensions.add(file_extension)
                destination_folder = os.path.join(folder, "images")
                os.makedirs(destination_folder, exist_ok=True)
                destination_path = os.path.join(destination_folder, normalized_file_name)
                shutil.move(file_path, destination_path)
            elif file_extension in video_extensions:
                known_extensions.add(file_extension)
                destination_folder = os.path.join(folder, "video")
                os.makedirs(destination_folder, exist_ok=True)
                destination_path = os.path.join(destination_folder, normalized_file_name)
                shutil.move(file_path, destination_path)
            elif file_extension in document_extensions:
                known_extensions.add(file_extension)
                destination_folder = os.path.join(folder, "documents")
                os.makedirs(destination_folder, exist_ok=True)
                destination_path = os.path.join(destination_folder, normalized_file_name)
                shutil.move(file_path, destination_path)
            elif file_extension in audio_extensions:
                known_extensions.add(file_extension)
                destination_folder = os.path.join(folder, "audio")
                os.makedirs(destination_folder, exist_ok=True)
                destination_path = os.path.join(destination_folder, normalized_file_name)
                shutil.move(file_path, destination_path)
            elif file_extension in archive_extensions:
                known_extensions.add(file_extension)
                destination_folder = os.path.join(folder, "archives")
                os.makedirs(destination_folder, exist_ok=True)
                destination_subfolder = os.path.join(destination_folder, normalize(file.split(".")[0], translit_dict))
                os.makedirs(destination_subfolder, exist_ok=True)
                shutil.unpack_archive(file_path, destination_subfolder, format=file_extension.lower())
                os.remove(file_path)
            else:
                unknown_extensions.add(file_extension) #файли, розширення яких невідомі, залищаються без змін 

    # Видалення порожніх папок, крім 'archives', 'video', 'audio', 'documents', 'images'
    for root, dirs, files in os.walk(folder, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if dir_name not in ['archives', 'video', 'audio', 'documents', 'images'] and not os.listdir(dir_path):
                os.rmdir(dir_path)

    # Видалення порожніх папок
    """for root, dirs, files in os.walk(folder, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)"""

    return known_extensions, unknown_extensions


"""if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python3 4.py <Потрібно вказати шлях до папки.>")
        sys.exit(1)

    target_folder = sys.argv[1]
    known_extensions, unknown_extensions = process_folder(target_folder)

    print("Known Extensions:")
    print(known_extensions)
    print("Unknown Extensions:")
    print(unknown_extensions)

def main():
    # Код, що викликається, коли запускаєте скрипт з консолі.

    if __name__ == "__main__":
        main() """ 

def main():
    import sys
    # Код, що викликається, коли запускаєте скрипт з консолі.

    if len(sys.argv) != 2:
        print("Usage: python3 clean.py <Потрібно вказати шлях до папки.>")
        sys.exit(1)

    target_folder = sys.argv[1]
    known_extensions, unknown_extensions = process_folder(target_folder)

    print("Known Extensions:")
    print(known_extensions)
    print("Unknown Extensions:")
    print(unknown_extensions)

if __name__ == "__main__":
    main()
    