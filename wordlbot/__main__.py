import json
import lzma
import os
import pathlib
import random
import re
from collections import (
    Counter,
    defaultdict,
)
from functools import partial

OFFICIAL_WORDLIST_FN = "official_wordlist.json.xz"
ROOTPATH = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
WORDS_FN = "words.txt.xz"


class State:
    def __init__(self, letters=5):
        self.letters = letters
        self.known = dict()
        self.eliminated = set()
        self.not_in_position = defaultdict(set)

    def __str__(self):
        return f'Eliminated: {self.eliminated}, Known: {self.known}, Not in position: {dict(self.not_in_position)}'


def get_words(n):
    with lzma.open(ROOTPATH / WORDS_FN) as f:
        for line in f:
            word = line.decode('utf-8').strip()
            if len(word) == n:
                yield word


def make_pattern(state):
    yield '^'
    for idx in range(state.letters):
        if c := state.known.get(idx):
            yield f'{c}'
        else:
            exclude = f'{"".join(state.not_in_position.get(idx, set()) | state.eliminated)}'
            yield f'[^{exclude}]'
    yield '$'


def get_filter_fn(regex, state):
    if state.not_in_position.values():
        must_be_in_word = set.union(*state.not_in_position.values())
    else:
        must_be_in_word = None

    def _filter_word(word):
        m = regex.match(word)
        if must_be_in_word:
            return m is not None and all(c in word for c in must_be_in_word)
        return m is not None

    return _filter_word


def filter_words(words, state):
    pattern = re.compile(''.join(make_pattern(state)))
    return filter(get_filter_fn(pattern, state), words)


def get_counts(corpus):
    letters = len(corpus[0])
    counters = [Counter() for _ in range(letters)]
    for word in corpus:
        for i, c in enumerate(word):
            counters[i][c] += 1
    return counters


def parse(guess, feedback, state):
    for i, (g, f) in enumerate(zip(guess, feedback)):
        if f.isupper():
            state.known[i] = g
        elif f.islower():
            state.not_in_position[i].add(g)
        else:
            state.eliminated.add(g)


def score_candidate(counts, word):
    def _inner():
        for i, c in enumerate(word):
            yield counts[i][c]

    return len(set(word)), sum(_inner())


def main():
    print(
        "When prompted for feedback, give an uppercase character for character in correct position (\U0001f7e9), lowercase in incorrect position (\U0001f7e8), and a non-letter for eliminated ones (\u2588)."
    )
    try:
        letters = int(input("How many letters? (4-11) [5]:"))
    except Exception:
        letters = 5
    state = State(letters)
    if letters == 5:
        with lzma.open(ROOTPATH / OFFICIAL_WORDLIST_FN, "r") as f:
            words = json.load(f)
    else:
        words = list(get_words(letters))
    full_corpus = words.copy()
    while True:
        counts = get_counts(words)
        words.sort(key=partial(score_candidate, counts), reverse=True)
        if len(words) == 1:
            print(f"The word is {words[0].upper()}")
            break
        if len(state.known) == 4 or len(words) < 10:
            letters_to_eliminate = set.union(*(set(x) for x in words)) - (
                    set(state.known.values()) | set.union(*state.not_in_position.values()))
            best_for_elimination = \
                sorted(full_corpus, key=lambda x: len(set(x).intersection(letters_to_eliminate)), reverse=True)[
                    0].upper()
            print(f"The word is one of {', '.join(words).upper()}")
            if len(words) > 2:
                print(f"You should guess {best_for_elimination} to eliminate most options.")
        elif len(words) > 100:
            ideas = ", ".join(random.sample(words[1:20], 5)).upper()
            print(
                f'{len(words)} possible words remaining, best guess is {words[0].upper()}, other good ones are: {ideas}'
            )
        else:
            print(
                f'Your best guess would be {words[0].upper()}, but {", ".join(words[1:6]).upper()} are fine too. ({len(words)} words remaining)'
            )
        print()
        guess = input("Your guess was: ").lower()
        if len(guess) != state.letters or not guess.isalpha():
            print("That's not a valid guess...")
            continue
        feedback = input("Feedback was  : ")
        if len(feedback) != state.letters:
            print("Invalid feedback length")
            continue
        parse(guess, feedback, state)
        words = list(filter_words(words, state))
        if len(state.known) == state.letters:
            break


if __name__ == '__main__':
    main()
