from __future__ import absolute_import, division, unicode_literals  # noqa
import logging
import sys
import os
from datetime import datetime
import numpy as np

from tweet import tweet

class user:
    
    def __init__(self, Dir, id, wordMap, uniWordMap):
        self.tweets = []
        self.tweetCnt = 0
        self.userID = id
        self.wordMap = wordMap
        self.uniWordMap = uniWordMap
        self.Dir = Dir 
    
    def user(self): 
        datalines = []
        
        with open(self.Dir, 'r', encoding='utf-8') as f:
            datalines = f.read().splitlines()
            
        self.tweetCnt = len(datalines)

        for line in datalines: 
            tw = tweet(line, self.wordMap, self.uniWordMap)
            tw.tweet()
            self.wordMap = tw.wordMap
            self.uniWordMap = tw.uniWordMap
            self.tweets.append(tw)
            
        datalines.clear()
