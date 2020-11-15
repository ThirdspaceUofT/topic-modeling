from nltk.tokenize import sent_tokenize, word_tokenize 
import Stopwords
import string
import re


class tweet:
    
    def __init__(self, dataline, wordMap, uniWordMap):
        self.tweetwords = []
        self.dataline = dataline
        self.wordMap = wordMap
        self.uniWordMap = uniWordMap
        self.time = 0

    def tweet(self):
        number = len(self.wordMap)
        inline = self.dataline
        words = []
        tokens = self.tokenize(inline)
        
        for token in tokens:
            tmpToken = token.lower()
            if ((not Stopwords.isStopword(tmpToken)) and (not self.isNoisy(tmpToken))):
                if (not(tmpToken in self.wordMap)):
                    words.append(number)
                    self.wordMap[tmpToken] = number
                    number += 1
                    self.uniWordMap.append(tmpToken)
                else:
                    words.append(self.wordMap.get(tmpToken))
                    
        
        for w in words:
            self.tweetwords.append(w)
            
        words.clear()
        tokens.clear()
        
        
    def isNoisy(self, token):
        if(("#pb#" in token.lower()) or ("http:" in token.lower())):
            return True
        
        if("@" in token.lower()):
            return True
        
        if(token in string.punctuation):
            return True

        return False

    def tokenize(self, line):
        tokens = word_tokenize(line)    
        return tokens