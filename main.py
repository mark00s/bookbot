from pathlib import Path

import requests

from stats import count_words

BOOKS = [
    {
        "frankenstein": "https://raw.githubusercontent.com/asweigart/codebreaker/master/frankenstein.txt"
    }
]
BOOKS_PATH = "books"


def main():
    file_paths = []
    try:
        file_paths = save_books()
        for file_path in file_paths:
            book_text = get_book(file_path["path"])
            word_count = count_words(book_text)
            book_chars = count_chars(book_text)

            print_report(file_path["path"], word_count, book_chars)

    except Exception as e:
        print(e)

    return 0


def save_books(books=BOOKS):
    file_paths = []

    for book in books:
        for name, url in book.items():
            file_path = Path(f"{BOOKS_PATH}/{name}.txt")

            if not file_path.is_file():
                book_text = requests.get(url).text
                with open(file_path, "w") as f:
                    f.write(book_text)

            file_paths.append({"name": name, "path": file_path})

    return file_paths


def get_book(file_path):
    text = ""
    # Explicitly close file by adding variable
    with open(file_path) as f:
        text = f.read()
    return text


def count_chars(book_text):
    result = {}
    book_text_lowered = book_text.lower()
    for char in book_text_lowered:
        if not char.isalpha():
            continue

        count = result.get(char, None)
        if not count:
            result[char] = 1
        else:
            result[char] = count + 1

    return dict(sorted(result.items(), key=lambda item: item[1], reverse=True))


def print_report(path, wc, book_chars):
    print(f"--- Begin report of {path} ---")
    print(f"{wc} words found in the document")
    print("")
    for book_char in book_chars:
        count = book_chars[book_char]
        lane = f"The '{book_char}' character was found {count} time"
        if count > 1:
            lane += "s"
        print(lane)
    print("--- End report ---")


main()
