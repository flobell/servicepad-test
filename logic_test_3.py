import re

def words_repetitions(text: str):
    """words repetitions function"""

    # remove symbols
    text_no_symbols = re.sub(r'[^a-zA-Z\s]', '', text)

    # lowercase words
    text_lowercase = text_no_symbols.lower()

    # split in list
    words = text_lowercase.split()

    # count dict
    word_count = {}
    for word in words:
        word_count[word] = words.count(word)

    return word_count


if __name__ == '__main__':
    text = input("Enter a text: ")
    print(words_repetitions(text))