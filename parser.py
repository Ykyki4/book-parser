from pathlib import Path, PurePath
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


def parse_book(response):
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        heading_text = soup.find('div', id='content').find('h1').text
    except AttributeError:
        return
    book_title = heading_text.split("::")[0].strip()
    author = heading_text.split("::")[1].strip()
    return book_title


def get_book():
    for id in range(10):
        parse_url = f"https://tululu.org/b{id+1}/"
        response = requests.get(parse_url)
        response.raise_for_status()
        book_name = parse_book(response)
        txt_url = f"https://tululu.org/txt.php?id={id+1}"
        filename = f'{id+1} {book_name}'
        download_txt(txt_url, filename)


if __name__ == "__main__":
    get_book()