import loader
from mvideo_parser import work

key_words = [
    'xbox series x / s - консоли',
    'sony ps5',
]

black_list = [
]

work.start(key_words, black_list)