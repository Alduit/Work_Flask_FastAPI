import argparse
from download import download_images,download_images_threaded,download_images_multiprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Cкачивания изображений с URL-адресов.")
    parser.add_argument('urls', metavar='URL', type=str, nargs='*',
                        help='Список URL-адресов изображений для скачивания (опционально)')
    args = parser.parse_args()

    if args.urls:
        urls = args.urls
    else:
        urls = []

    while True:
        url = input("Введите URL-адрес изображения (или 'стоп' для завершения ввода): ").strip()
        if url.lower() == 'стоп':
            break
        urls.append(url)

    if not urls:
        print("Нет URL-адресов для скачивания.")
        sys.exit(0)

    #download_images(urls)
    #download_images_threaded(urls)
    download_images_multiprocess(urls)


if __name__ == "__main__":
    main()