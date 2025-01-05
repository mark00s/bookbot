import requests
from pathlib import Path

BOOKS = [{"frankenstein": "https://raw.githubusercontent.com/asweigart/codebreaker/master/frankenstein.txt"}]
BOOKS_PATH = "books"

def main():
    try:
        save_books()
    except Exception as e:
        print(e)



    return 0

def save_books(books=BOOKS):
    for book in books:
        for name, url in book.items():
            file_path = Path(f'{BOOKS_PATH}/{name}.txt')
            if file_path.is_file():
                continue
            
            book_text = requests.get(url).text
            with open(file_path, "w") as f:
                f.write(book_text)

main()