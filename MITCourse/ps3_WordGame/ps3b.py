from ps3a import *
import time
from perm import *


#
#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    # TO DO...
    MaxScore = 0
    KeyWord = None
    probList = []
    for i in range(1, HAND_SIZE + 1):
        probList.extend(get_perms(hand, i))
    for i in reversed([i for i,x in enumerate(probList) if x not in word_list]):
        del probList[i]
    for s in probList:
        CurrentScore = get_word_score(s, HAND_SIZE)
        if CurrentScore > MaxScore:
            MaxScore = CurrentScore
            KeyWord = s
    # print KeyWord, str(MaxScore)
    return KeyWord


#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    # TO DO ...    

    TotalPoints = 0
    while True:
        print "Current Hand:"
        display_hand(hand)
        tryWord = comp_choose_word(hand, word_list)
        print tryWord
        if tryWord is None:
            break
        if is_valid_word(tryWord, hand, word_list) == False:
            print "Invalid word, please try again."
            continue
        SinglePoints = get_word_score(tryWord, HAND_SIZE)
        TotalPoints += SinglePoints
        print "'%s' earned %d points. Total: %d points." %(tryWord, SinglePoints, TotalPoints)
        hand = update_hand(hand, tryWord)
        if calculate_handlen(hand) == 0:
            break

    print "Total score: %d points" %TotalPoints
    
#
# Problem #6C: Playing a game
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    # TO DO...
    hand = {}
    inputList = ['n', 'r', 'e']
    while True:
        KeyWord = str(raw_input("1.New Game: (n) \n2.Restart Last Game: (r) \n3.Exit: (e) \n:")).lower()
        if KeyWord == 'e':
            print "Bye Bye!"
            break
        elif KeyWord == 'n' or KeyWord == 'r':
            if KeyWord == 'n':
                hand = deal_hand(HAND_SIZE)
            elif len(hand) == 0:
                print "You haven't played before!"
                continue
            while True:
                player = str(raw_input("Enter player: User(u) , AI(a) :")).lower()
                if player == 'u':
                    play_hand(hand, word_list)
                    break
                elif player == 'a':
                    comp_play_hand(hand, word_list)
                    break
                else:
                    print "Wrong command , please try again!"
        else:
            print "Wrong command , please try again!"




        
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    # play_game(word_list)
    hand = {'a':1, 'q':1, 'l':2, 'm':1, 'u':1, 'i':1}
    comp_play_hand(hand, word_list)
    
