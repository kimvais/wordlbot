# Wordlbot

A simple python script to help solve the word game that is all the craze.

Just clone the repository and run `python wordle.py`. Requires python3.x, no need for any libraries or whatnot.

Things worth noting:

1. The corpus is just some random english wordlist, **not** the one used by Worldle, so it suggests words that are not in wordle list.
2. You can use any words, the helper doesn't care but gives you the best guesses based on feedback on your own word.
3. `CARES` is *statistically* the best word to start with, if you are playing the hard mode.
4. This is optimized for the hard mode, so suggestions will always be ones that are valid in it, but it works just as well if you ignore the first 2 suggestions and just go with e.g. "TRAIL - NODES" no matter what the feedback was. Just let the script know the feedback correctly and the 3rd suggestions should be really good.
