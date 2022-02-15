import re
from collections import (
    Counter,
    defaultdict,
)
from functools import partial


class State:
    def __init__(self, letters=5):
        self.letters = letters
        self.known = dict()
        self.eliminated = set()
        self.not_in_position = defaultdict(set)

    def __str__(self):
        return f'Eliminated: {self.eliminated}, Known: {self.known}, Not in position: {dict(self.not_in_position)}'


def get_words(n):
    with open("words_alpha.txt") as f:
        for line in f:
            word = line.strip()
            if len(word) == n:
                yield line.strip()


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
    letters = int(input("How many letters?"))
    state = State(letters)
    words = list(get_words(letters))
    while True:
        counts = get_counts(words)
        words.sort(key=partial(score_candidate, counts), reverse=True)
        if len(words) == 1:
            print(f"The word is {words[0].upper()}")
            break
        elif len(state.known) == 4 or len(words) < 10:
            print(f"The word is one of {', '.join(words).upper()}")
        else:
            print(f'Some good guesses would be: {", ".join(words[:5]).upper()} ({len(words)} words remaining)')
        print()
        guess = input("Your guess was: ").lower()
        if not guess.isalpha():
            print("That's not a valid guess...")
            continue
        feedback = input("Feedback was: ")
        parse(guess, feedback, state)
        words = list(filter_words(words, state))
        if len(state.known) == state.letters:
            break


if __name__ == '__main__':
    main()
