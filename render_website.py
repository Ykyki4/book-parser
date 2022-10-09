import json
import math
import os
from itertools import count
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from parse_tululu_category import parse_args
from livereload import Server, shell
from more_itertools import chunked

def on_reload():
    args = parse_args()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open(args.json_path, "r", encoding="utf-8") as my_file:
        books_json = my_file.read()

    books = json.loads(books_json)
    for page, books_page_chunks in enumerate(list(chunked(books, 10))):
        rendered_page = template.render(
            books_chunks=list(chunked(books_page_chunks, 2)),
            pages_numb=math.ceil(len(books) / 10),
            current_page=page+1
        )
        Path('pages').mkdir(parents=True, exist_ok=True)
        with open(f'pages/index{page+1}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == "__main__":
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')