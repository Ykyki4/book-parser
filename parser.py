from pathlib import Path, PurePath
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup
import requests
from requests import HTTPError
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.url == "https://tululu.org/":
        raise HTTPError


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    try:
        check_for_redirect(response)
    except HTTPError:
        print("Книги не существует")
        return
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
    comments = []
    soup = BeautifulSoup(response.text, 'lxml')
    heading_text = soup.find('div', id='content').find('h1').text
    image = soup.find('div', class_='bookimage').find('img')['src']
    texts_tags = soup.find_all('div', class_='texts')
    for tag in texts_tags:
        comments.append(tag.find('span', class_='black').text)
    book_title = heading_text.split("::")[0].strip()
    author = heading_text.split("::")[1].strip()
    image_url = urljoin('https://tululu.org', image)
    book = {
        "title": book_title,
        "author": author,
        "image": image_url,
        "comments": comments
    }
    return book


def get_book():
    for id in range(10):
        parse_url = f"https://tululu.org/b{id+1}/"
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
        txt_url = f"https://tululu.org/txt.php?id={id+1}"
        filename = f'{id+1} {book_name}'
        download_txt(txt_url, filename)
        download_book_cover(img_url)


if __name__ == "__main__":
    get_book()