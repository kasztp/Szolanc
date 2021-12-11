import random
import timeit

# Load Word dictionaries from text files.
EN_FILENAME = './app/static/Scrabble.txt'  # EN word list
HU_FILENAME = './app/static/szavak.txt'  # HU word list

with open(HU_FILENAME, encoding='utf-8') as hu_file, open(EN_FILENAME, encoding='utf-8') as en_file:
    EN_WORDS = set(en_file.read().splitlines())
    HU_WORDS = set(hu_file.read().splitlines())


class Hand:
    def __init__(self, letterset, lettercount):
        self.letterset = letterset
        self.lettercount = lettercount
        self.held_letters = self.draw_letters(lettercount)

    # Draw n number of random letters from the letter set
    def draw_letters(self, lettercount: int) -> list:
        if lettercount >= 2:
            print(self.letterset)
            ownletters = random.sample(self.letterset, k=lettercount)
            print(f'letters drawn: {ownletters}')
            return ownletters
        else:
            print('ERROR: letter number less than 2!')
            return []

    def update_hand(self, letters):
        self.held_letters = letters


class Szolanc:
    def __init__(self, language):
        self.language = language
        if self.language == 'HU':
            self.word_list = HU_WORDS
            self.letter_list = ['a'] * 2 + ['b'] * 2 + ['c'] * 2 + ['d'] * 2 + ['e'] * 2 + ['f'] * 2 + \
                               ['g'] * 2 + ['h'] * 2 + ['i'] * 2 + ['j'] * 2 + ['k'] * 2 + ['l'] * 2 + \
                               ['m'] * 2 + ['n'] * 2 + ['o'] * 2 + ['p'] * 2 + ['á'] * 2 + ['r'] * 2 + \
                               ['s'] * 2 + ['t'] * 2 + ['u'] * 2 + ['v'] * 2 + ['é'] * 2 + ['í'] * 2 + \
                               ['ó'] * 2 + ['z'] * 2 + ['ö'] * 2 + ['ő'] * 2 + ['ú'] * 2 + ['ü'] * 2 + \
                               ['ű'] * 2 + ['sz'] * 2 + ['gy'] * 2 + ['ny'] * 2 + ['cs'] * 2 + \
                               ['ly'] * 2 + ['zs'] * 2 + ['ty'] * 2
        else:
            self.word_list = EN_WORDS
            self.letter_list = ['a'] * 2 + ['b'] * 2 + ['c'] * 2 + ['d'] * 2 + ['e'] * 2 + \
                               ['f'] * 2 + ['g'] * 2 + ['h'] * 2 + ['i'] * 2 + ['j'] * 2 + \
                               ['k'] * 2 + ['l'] * 2 + ['m'] * 2 + ['n'] * 2 + ['o'] * 2 + \
                               ['p'] * 2 + ['q'] * 2 + ['r'] * 2 + ['s'] * 2 + ['t'] * 2 + \
                               ['u'] * 2 + ['v'] * 2 + ['w'] * 2 + ['x'] * 2 + ['y'] * 2 + ['z']
        self.hand = Hand(self.letter_list, 2)

    # Check which words of the dictionary can be used with the given starting & ending letters
    # HU version to be refined:
    def checker(self, ownletters, length):
        valid_words = set()
        for word in self.word_list:
            if len(word) == length:
                word = word.lower()
                if word[0] == ownletters[0] and word[-1] == ownletters[-1]:
                    valid_words.add(word)
        return valid_words

    def word_check(self, ownletters, length):
        textperm = set()
        for wordlength in range(2, (length + 1)):
            start_time = timeit.default_timer()
            results = set(self.checker(ownletters, wordlength))
            print(timeit.default_timer() - start_time)
            print(f'Unique {wordlength} length words generated: {len(results)}')
            textperm |= results
            print(f'Unique words generated so far: {len(textperm)}')
        return textperm

    # Calculate word point values
    def score_calc(self, words: list) -> dict:
        if words != 1:
            scores = {}
            for word in words:
                if word != ():
                    value = len(word)
                    scores[word] = value
            return scores
        else:
            print('ERROR: NO valid words given!')
            return 'NONE'

    def group_by_score(self, scores: dict) -> dict:
        score_groups = sorted(set(val for val in scores.values()), reverse=True)
        grouped_words = {}
        for number in score_groups:
            wordgroup = []
            for i in scores.items():
                if i[1] == number:
                    wordgroup.extend(i[0:1])
            grouped_words[number] = sorted(wordgroup)
        return grouped_words
