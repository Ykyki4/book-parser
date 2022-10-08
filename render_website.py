import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from parse_tululu_category import parse_args
from livereload import Server, shell

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

    rendered_page = template.render(
        books=books
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == "__main__":

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')