# Wordlbot


A simple python script to help solve the word game that is all the craze.

## TL;DR:
1. `pip install wordlbot`
2. `wordlbot`

## Development etc.

Just clone the repository and run `python wordle.py`. Requires python3.x, no need for any libraries or whatnot.

## Things worth noting

1. You can use any words, the helper doesn't care but gives you the best guesses based on feedback on your own word.
2. `CARES` is *statistically* the best word to start with, if you are playing the hard mode.
3. This is optimized for the hard mode, so suggestions will always be ones that are valid in it, but it works just as well if you ignore the first 2 suggestions and just go with e.g. "TRAIL - NODES" no matter what the feedback was. Just let the script know the feedback correctly and the 3rd suggestions should be really good.
4. This completely breaks all the "harder" wordle clones with longer words, especially all the 9+ letter variants can almost always be solved in 3 tries, quite often on second ...

## Todo

Something something [Selenium](https://www.selenium.dev/) actual automagic.
