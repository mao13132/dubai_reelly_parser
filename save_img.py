from datetime import datetime

import requests

import os


def check_dirs(dir_name):
    dir = f'{os.getcwd()}\\files\\'
    dir2 = f'{os.getcwd()}\\files\\{dir_name}\\'

    if not os.path.exists(dir):
        os.mkdir(dir)

    if not os.path.exists(dir2):
        os.mkdir(dir2)


def downloads_image(url, file_name):
    try:
        r = requests.get(url, stream=True)
    except:
        return ''
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            for chunk in r:
                f.write(chunk)

        return True


def save_images(images_list):
    dir_name = datetime.now().strftime("%H%M%S")

    check_dirs(dir_name)

    good_files = []

    if images_list != []:
        print(f'Начинаю скачку {len(images_list)} картинок в {os.getcwd()}\\files')

    for count, image in enumerate(images_list):

        file_name = f"{os.getcwd()}\\files\\{dir_name}\\{count}.jpg"

        name_img = downloads_image(image, file_name)

        if name_img is None:
            continue

        if name_img:
            good_files.append(file_name)

    return good_files
