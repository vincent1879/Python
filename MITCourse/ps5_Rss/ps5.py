# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

# TODO: NewsStory

class NewsStory(object):
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link


#======================
# Part 2
# Triggers
#===    ===================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger
class WorldTigger(Trigger):
    
    def __init__(self, word):
        self.word = word.lower()

    def is_word_in(self, text):
        
        t = text.lower()
        s = string.punctuation
        s += ' '
        i = 0
        while i < len(t):
            j = 0
            while i < len(t) and j < len(self.word) and t[i] == self.word[j]:
                i += 1
                j += 1
            if j == len(self.word):
                if (i == j or t[i-j-1] in s) and (len(t) == len(self.word) or t[i] in s):
                    return True
            else:
                i = i - j
            i += 1
        
        return False









# TODO: TitleTrigger
# TODO: SubjectTrigger
# TODO: SummaryTrigger

class TitleTrigger(WorldTigger):
    def evaluate(self, story):
        return self.is_word_in(story.get_title())

class SubjectTrigger(WorldTigger):
    def evaluate(self, story):
        return self.is_word_in(story.get_subject())

class SummaryTrigger(WorldTigger):
    def evaluate(self, story):
        return self.is_word_in(story.get_summary())




# Composite Triggers
# Problems 6-8

# TODO: NotTrigger
# TODO: AndTrigger
# TODO: OrTrigger

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)


class AndTrigger(Trigger):

    def __init__(self, firstT, secondT):
        self.firstT = firstT
        self.secondT = secondT

    def evaluate(self, story):
        return self.firstT.evaluate(story) and self.secondT.evaluate(story)


class OrTrigger(Trigger):

    def __init__(self, firstT, secondT):
        self.firstT = firstT
        self.secondT = secondT

    def evaluate(self, story):
        return self.firstT.evaluate(story) or self.secondT.evaluate(story)




# Phrase Trigger
# Question 9

# TODO: PhraseTrigger

class PhraseTrigger(Trigger):

    def __init__(self, phrase):
        self.phrase = phrase

    def is_word_in(self, text):
        return self.phrase in text

    def evaluate(self, story):
        return self.is_word_in(story.get_title()) or \
        self.is_word_in(story.get_summary()) or \
        self.is_word_in(story.get_subject())



#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder (we're just returning all the stories, with no filtering) 
    # Feel free to change this line!
    for index in range(len(stories)-1, -1 , -1):
        bNeedRemove = True
        for trigger in triggerlist:
            if trigger.evaluate(stories[index]):
                bNeedRemove = False
        if bNeedRemove:
            stories.pop(index)

    return stories

#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    # TODO: Problem 11
    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones

    triggerDict = {}
    triggerlist = []

    for line in lines:
        indexOne = line.find(' ')
        if indexOne == -1: continue
        firstWord = line[:indexOne]
        if indexOne + 1 >= len(line): continue

        if firstWord != 'ADD':

            indexTwo = line.find(' ', indexOne + 1)
            if indexTwo == -1: continue
            secondWord = line[indexOne + 1:indexTwo]
            if indexTwo + 1 >= len(line): continue
            thirdWord =  line[indexTwo + 1:]

            if secondWord == 'AND' or secondWord == 'OR' or secondWord == 'NOT':
                t1,t2 = thirdWord.split(' ')
                if t1 in triggerDict.keys() and t2 in triggerDict.keys():
                    triggerDict[firstWord] = createNewTrigger(secondWord, None, triggerDict[t1], triggerDict[t2])
            elif secondWord == 'SUBJECT' or secondWord == 'SUMMARY' or secondWord == 'TITLE' or secondWord == 'PHRASE':
                triggerDict[firstWord] = createNewTrigger(secondWord, thirdWord)
        else:
            for t in line[indexOne+1:].split(' '):
                if t in triggerDict.keys():
                    triggerlist.append(triggerDict[t])

    return triggerlist



def createNewTrigger(triggerType, info = None, t1 = None, t2 = None):

    if triggerType == 'SUBJECT':
        newTrigger = SubjectTrigger(info)
    elif triggerType == 'SUMMARY':
        newTrigger = SummaryTrigger(info)
    elif triggerType == 'TITLE':
        newTrigger = TitleTrigger(info)
    elif triggerType == 'PHRASE':
        newTrigger = PhraseTrigger(info)
    elif triggerType == 'AND':
        newTrigger = AndTrigger(t1, t2)
    elif triggerType == 'OR':
        newTrigger = OrTrigger(t1, t2)
    elif triggerType == 'NOT':
        newTrigger = NotTrigger(t1, t2)
    else:
        newTrigger = None

    return newTrigger



    
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    # t1 = TitleTrigger("Republican")
    # t2 = SummaryTrigger("Facebook")
    # t3 = PhraseTrigger("New York Times")
    # t4 = OrTrigger(t2, t3)
    # triggerlist = [t1]
    
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

