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
    args = parser.parse_args()
    return args


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
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


def parse_book(response):

    soup = BeautifulSoup(response.text, 'lxml')
    heading_text = soup.find('div', id='content').find('h1').text
    image = soup.find('div', class_='bookimage').find('img')['src']
    texts_tags = soup.find_all('div', class_='texts')
    comments = [tag.find('span', class_='black').text for tag in texts_tags]
    book_genres_tags = soup.find('span', class_='d_book').find_all("a")
    book_genres = [book_genre.text for book_genre in book_genres_tags]
    image_url = urljoin('https://tululu.org', image)
    title, author = heading_text.split("::")
    book = {
        "title": title,
        "author": author,
        "image": image_url,
        "comments": comments,
        "genre": book_genres
    }

        # book["title"] = title.strip()
        # book["author"] = author.strip()
    return book


def get_books():
    args = parse_args()
    for book_id in range(args.start_id, args.end_id):
        try:
            parse_url = f"https://tululu.org/b{book_id}/"
            response = requests.get(parse_url)
            response.raise_for_status()
            try:
                check_for_redirect(response)
            except HTTPError:
                print("Книги не существует")
                continue
            book = parse_book(response)
            book_name = book["title"]
            img_url = book["image"]
            txt_url = f"https://tululu.org/txt.php?id={book_id}"
            filename = f'{book_id} {book_name}'
            try:
                download_txt(txt_url, filename)
            except HTTPError:
                print("Книги не существует")
                continue
            download_book_cover(img_url)
            print(f"Название книги: {book_name}")
            print(book['genre'])
        except requests.exceptions.ConnectionError:
            print("Connection lost, next try in 1 minute", file=sys.stderr)
            time.sleep(60)


if __name__ == "__main__":
    get_books()