import os
import requests
from utils import ensure_dir_exists
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from urllib.parse import urlparse
import time


# Указываем полный путь к папке img
IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'img')


def download_image(url):
    try:
        print(f"Начало загрузки изображения {url}")
        start_time = time.time()
        response = requests.get(url)
        if response.status_code == 200:
            content_type = response.headers.get('content-type')
            extension = content_type.split('/')[-1] if content_type else 'jpg'

            # Извлекаем имя файла из URL
            url_path = urlparse(url).path
            image_name = os.path.basename(url_path)

            save_path = os.path.join(IMAGES_DIR, image_name)
            ensure_dir_exists(IMAGES_DIR)

            with open(save_path, 'wb') as f:
                f.write(response.content)

            end_time = time.time()
            download_time = end_time - start_time
            print(f"Изображение {url} успешно сохранено как {image_name} за {download_time:.2f} секунд")
        else:
            print(f"Не удалось скачать изображение {url}. Статус код: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")


def download_images(urls):
    ensure_dir_exists(IMAGES_DIR)
    start_time = time.time()

    for url in urls:
        download_image(url)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Общее время скачивания последовательно: {total_time:.2f} секунд")


def download_images_threaded(urls):
    ensure_dir_exists(IMAGES_DIR)
    start_time = time.time()

    with ThreadPoolExecutor() as executor:
        executor.map(download_image, urls)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Общее время скачивания с использованием многопоточности: {total_time:.2f} секунд")


def download_images_multiprocess(urls):
    ensure_dir_exists(IMAGES_DIR)
    start_time = time.time()

    with ProcessPoolExecutor() as executor:
        executor.map(download_image, urls)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Общее время скачивания с использованием многопроцессорности: {total_time:.2f} секунд")

    
