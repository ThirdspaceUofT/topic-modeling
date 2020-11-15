from __future__ import absolute_import, division, unicode_literals  # noqa
import logging
import sys
import os
from datetime import datetime
import numpy as np
from user import user
from Model import Model
import Stopwords
 
    
class TwitterLDAmain:
    
    def __init__(self, mon, data_dir = "/data"):
        self.base = os.getcwd() + data_dir
        self.name = "test"
        self.mon = mon
        self.filelist = self.base + "/files/" + self.mon + "_files.txt"
        self.dataDir = self.base + "/Data4Model/" + self.name + "/"
        self.dataDir = self.base + "/Data4Model/" + self.name + "/"+ self.mon +"/"
        self.outputDir = self.base + "/ModelRes/" + self.name + "/"+ self.mon +"/"
        self.modelParas = self.base + "/modelParameters-" + self.name + ".txt"
        self.stopfile = self.base + "/stoplist.txt"
        self.modelSettings = {}


    def getModelPara(self, modelParas, modelSettings): 
        
        modelSettings['topics'] = 40
        modelSettings['alpha_g'] = 1.25
        modelSettings["beta_word"] = 0.01
        modelSettings["beta_b"] = 0.01
        modelSettings["gamma"] = 20
        modelSettings["iteration"] = 20                     

        with open(modelParas, 'r', encoding='utf-8') as f:
            inputlines = f.read().splitlines()

        for item in inputlines:
            x = item.split(":")
            x = [x[0].strip(), x[1].strip()]
            if(x[1] and (x[0] in modelSettings)):
                modelSettings[x[0]] = float(x[1])
                
                
    def errprint(self, *args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)
        
                
    def main(self):
        
        # 1. get model parameters
        
        self.getModelPara(self.modelParas, self.modelSettings)
        A_all = self.modelSettings['topics']
        alpha_g = self.modelSettings['alpha_g']
        beta_word = self.modelSettings['beta_word']
        beta_b = self.modelSettings['beta_b']
        gamma = self.modelSettings['gamma']
        nIter = self.modelSettings['iteration']
        
        self.errprint("Topics:" + str(A_all) + ", alpha_g:" + str(alpha_g) + ", beta_word:" + str(beta_word) + ", beta_b:" + str(beta_b) + ", gamma:" + str(gamma) + ", iteration:" + str(nIter))
        self.modelSettings.clear()
        
        
        Stopwords.Stopwords()
        Stopwords.addStopfile(self.stopfile)
        sw = Stopwords.stopwords_list
        
        outputTopicwordCnt = 30
        outputBackgroundwordCnt = 50

        outputWordsInTopics = self.outputDir + "WordsInTopics.txt"
        outputBackgroundWordsDistribution = self.outputDir + "BackgroundWordsDistribution.txt"
        outputTextWithLabel = self.outputDir + "/TextWithLabel/"

        
        if not os.path.exists(outputTextWithLabel):
            os.makedirs(outputTextWithLabel)
        
        # 2. get documents (users)
        
        
        wordMap = {}
        uniWordMap = []
        users = []

        with open(self.filelist, 'r', encoding='utf-8') as f:
            files = f.read().splitlines()
            
        
            
        for file in files:
            tweetuser = user(self.dataDir + file, file, wordMap, uniWordMap)
            tweetuser.user()
            wordMap = tweetuser.wordMap
            uniWordMap = tweetuser.uniWordMap
            users.append(tweetuser)
            
        if (len(uniWordMap) != len(wordMap)):
            print(len(wordMap))
            print(len(uniWordMap))
            self.errprint("uniqword size is not the same as the hashmap size!")
            sys.exit(0)
            
        # output wordMap and itemMap
        with open(self.outputDir + "wordMap.txt", 'w', encoding='utf-8') as f:
            for k, v in wordMap.items():
                f.write(str(k) + '\t'+ str(v) + '\n')
                
        with open(self.outputDir + "uniWordMap.txt", 'w', encoding='utf-8') as f:
            for k in uniWordMap:
                f.write(str(k)+ '\n')
                
        uniWordMapSize = len(uniWordMap)
        wordMap.clear()
        uniWordMap.clear()

        # 3. run the model
        model = Model(A_all, len(users), uniWordMapSize, nIter, alpha_g, beta_word, beta_b, gamma)
        model.initialize(users)
        model.estimate(users, nIter)
        
        # 4. output model results
        print("Record Topic Distributions/Counts")
        model.outputTopicDistributionOnUsers(self.outputDir, users)
        print("read uniwordmap")
        
        with open(self.outputDir + "uniWordMap.txt", 'r', encoding='utf-8') as f:
            uniWordMap = f.read().splitlines()
        
        try:
            model.outputTextWithLabel(outputTextWithLabel, users, uniWordMap)
        except:
            print("An exception occurred in outputTextWithLabel: ", sys.exc_info()[0])
            
        print("write text with labels done")
        # model.outputTopicCountOnTime(outputTopicsCountOnTime)
        users.clear()

        try:
            model.outputWordsInTopics(outputWordsInTopics, uniWordMap, outputTopicwordCnt)
        except:
            print("An exception occurred in outputWordsInTopics: ", sys.exc_info()[0])

        print("write topics with keywords done")
        
        
        try:
            model.outputBackgroundWordsDistribution(outputBackgroundWordsDistribution, uniWordMap, outputBackgroundwordCnt)
        except:
            print("An exception occurred in outputBackgroundWordsDistribution: ", sys.exc_info()[0])
            
        print("Record Background done")
        print("Final Done")