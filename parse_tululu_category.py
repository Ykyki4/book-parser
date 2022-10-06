import json
import sys
import time
from pathlib import Path, PurePath
from urllib.parse import urljoin, urlsplit
import re
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests import HTTPError


def check_for_redirect(response):
    if response.url == "https://tululu.org/":
        raise HTTPError


def download_txt(url, params, filename, folder='books/'):
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    filename = sanitize_filename(f"{filename}.txt")
    Path(folder).mkdir(parents=True, exist_ok=True)
    path = PurePath(folder, filename)
    with open(path, 'wb') as file:
        file.write(response.content)
    return path


def download_book_cover(url):
    response = requests.get(url)
    response.raise_for_status()
    Path("images").mkdir(parents=True, exist_ok=True)
    filename = urlsplit(response.url).path.split("/")[2]
    path = PurePath("images", filename)
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


def get_book():
    books = []
    for page in range(1, 5):
        print("Страница", page)
        url = f"https://tululu.org/l55/{page}/"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        book_cards = soup.find_all('table', class_='d_book')
        for numb, book_card in enumerate(book_cards):
            try:
                book_url = urljoin(response.url, book_card.find("a")["href"])
                response = requests.get(book_url)
                response.raise_for_status()
                book = parse_book(response)
                book_name = book["title"]
                img_url = book["image"]
                book_id_unpacked = re.findall(r'\d+', urlsplit(response.url).path)
                for book_id in book_id_unpacked:
                    params = {"id": book_id}
                txt_url = f"https://tululu.org/txt.php"
                filename = f'{book_name}'
                #book["book_path"] = str(download_txt(txt_url, params, filename))
                #book["img_src"] = str(download_book_cover(img_url))
                books.append(book)
            except requests.exceptions.ConnectionError:
                print("Connection lost, next try in 1 minute", file=sys.stderr)
                time.sleep(60)

            except HTTPError:
                print("Книги не существует")
                continue
    with open("book_info.json", "w", encoding='utf8') as file:
        json.dump(books, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    get_book()
