# 6.00 Problem Set 3
# 
# Hangman
#


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    worldList = []
    wordString = random.choice(wordlist)
    for c in wordString:
        worldList.append(c)
    return worldList


def InitGuess(length):
    guess = []
    for i in range(length):
        guess.append('_')

    return guess


def FillInGuess(c, guess, word):
    for i in range(len(word)):
        if word[i] == c:
            guess[i] = c
    return guess

def Hangman():
    wordlist = load_words()
    availableList = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split()
    word = choose_word(wordlist)
    guess = InitGuess(len(word))
    life = 8

    print "Welcome to the game, Hangman!"
    print "I am thinking of  a word that is %d letters long" %len(word)

    while True:
        print "--------------------"
        print "You have %d guesses left" %life
        print "Available letters: %s" %"".join(availableList)
        c = str(raw_input("Please guess a letter:"))
        if c not in availableList:
            print "Please enter a reasonable letter"
            continue
        c = c.lower()
        availableList.remove(c)
        if c in word:
            guess = FillInGuess(c, guess, word)
            print "Good guess:" + "".join(guess)
        else:
            life -= 1
            print "Oops! That letter is not in my word:" + "".join(guess)

        if life <= 0 :
            print "You Lost, the word is %s Want try again?" %"".join(word)
            break
        if guess == word:
            print "Congratulations, You Win!"
            break


# End of Hangman









# end of helper code
# -----------------------------------

# actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program

# your code begins here!

if __name__ == "__main__":
    Hangman()
