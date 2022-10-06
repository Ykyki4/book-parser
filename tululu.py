import os
from pathlib import Path, PurePath
from urllib.parse import urljoin, urlsplit
import argparse
from bs4 import BeautifulSoup
import requests
from requests import HTTPError
from pathvalidate import sanitize_filename
import sys
import time


def check_for_redirect(response):
    if response.url == "https://tululu.org/":
        raise HTTPError


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("start_id", help="С какого идентификатора скачивать книги", type=int)
    parser.add_argument("end_id", help="До какого идентификатора скачивать книги", type=int)
    parser.add_argument(
        "-df", "--dest_folder",
        help="Путь к папке куда всё скачивать",
        default=os.path.dirname(os.path.realpath(__file__))
    )
    args = parser.parse_args()
    return args


def download_txt(url, params, filename, path):
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    filename = sanitize_filename(f"{filename}.txt")
    Path(f'{path}/books').mkdir(parents=True, exist_ok=True)
    path = PurePath(f'{path}/books', filename)
    with open(path, 'wb') as file:
        file.write(response.content)
    return path


def download_book_cover(url, path):
    response = requests.get(url)
    response.raise_for_status()
    Path(f"{path}/images").mkdir(parents=True, exist_ok=True)
    filename = urlsplit(response.url).path.split("/")[2]
    path = PurePath(f"{path}/images", filename)
    with open(path, 'wb') as file:
        file.write(response.content)
    return path


def parse_book(response):
    soup = BeautifulSoup(response.text, 'lxml')
    heading_text_selector = 'table.tabs h1'
    heading_text_result = soup.select_one(heading_text_selector)
    image_selector = 'div.bookimage img'
    image_select_result = soup.select_one(image_selector)
    texts_tags_selector = 'div.texts'
    texts_tags = soup.select(texts_tags_selector)
    tag_selector = 'span.black'
    comments = [tag.select_one(tag_selector).text for tag in texts_tags]
    book_genres_tags_selector = 'span.d_book a'
    book_genres_tags = soup.select(book_genres_tags_selector)
    book_genres = [book_genre.text for book_genre in book_genres_tags]
    image_url = urljoin(response.url, image_select_result['src'])
    title, author = heading_text_result.text.split("::")
    book = {
        "title": title.strip(),
        "author": author.strip(),
        "image": image_url,
        "comments": comments,
        "genres": book_genres
    }

    return book


def get_books():
    args = parse_args()
    download_path = args.dest_folder
    for book_id in range(args.start_id, args.end_id):
        try:
            parse_url = f"https://tululu.org/b{book_id}/"
            response = requests.get(parse_url)
            response.raise_for_status()
            check_for_redirect(response)
            book = parse_book(response)
            book_name = book["title"]
            img_url = book["image"]
            params = {"id": book_id}
            txt_url = f"https://tululu.org/txt.php"
            filename = f'{book_id} {book_name}'
            download_txt(txt_url, params, filename, download_path)
            download_book_cover(img_url, download_path)
            print(f"Название книги: {book_name}")
            print(book['genres'])

        except requests.exceptions.ConnectionError:
            print("Connection lost, next try in 1 minute", file=sys.stderr)
            time.sleep(60)

        except HTTPError:
            print("Книги не существует")
            continue


if __name__ == "__main__":
    get_books()