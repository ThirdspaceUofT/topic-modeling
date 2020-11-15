from __future__ import absolute_import, division, unicode_literals  # noqa
import logging
import sys
import os
from datetime import datetime
import numpy as np
import random
import math
import string


class Model:
  
    
    def __init__(self, A_all, u, v, niter, alpha_g, beta, beta_b, gamm):
        
        self.alpha_general = []
        self.alpha_general_sum = 0
        self.beta_word = []
        self.beta_word_sum = 0
        self.beta_background = []
        self.beta_background_sum = 0
        self.gamma = []

        
        self.z = [] # all hidden variables
        self.x = []

        self.A = int(A_all)
        self.U = int(u)
        self.V = int(v)
        self.nIter = int(niter)
        
        #############################
        
        for i in range(self.A):
            self.alpha_general.append(alpha_g)
            self.alpha_general_sum += self.alpha_general[i]
        
        self.gamma = []
        for i in range(2):
            self.gamma.append(gamm)
            
        
        for i in range(self.V):
            self.beta_background.append(beta_b)
            self.beta_background_sum += self.beta_background[i]
            self.beta_word.append(beta)
            self.beta_word_sum += self.beta_word[i]
            
            
        #########################
        
        self.C_ua = [ [ 0 for i in range(self.A) ] for j in range(self.U) ] #[[0]*self.A]*self.U 
        self.theta_general = [ [ 0.0 for i in range(self.A) ] for j in range(self.U) ] #[[0.0]*self.A]*self.U
        
        self.C_lv = [0, 0]
        self.rho = [0, 0]
        self.C_word = []

        self.C_word = [ [ 0 for i in range(self.V) ] for j in range(self.A) ] #[[0]*self.V]*self.A
        self.phi_word = [ [ 0.0 for i in range(self.V) ] for j in range(self.A) ] #[[0.0]*self.V]*self.A

        self.C_b = [0]*self.V 
        self.phi_background = [0.0]*self.V
        
        self.countAllWord = [0]*self.A


    
        
    def initialize(self, users):
        print("initializing...")
        
        u, d, w = (0, 0, 0)
        
        for u in range(len(users)):
            buffer_user = users[u]
            
            z_u = []
            x_u = []
            
            for d in range(len(buffer_user.tweets)):
                tw = buffer_user.tweets[d]

                x_u_d = []
                
                randgeneral = random.random()
                thred = 0
                a_general = 0
                
                for a in range(self.A):
                    thred += float(1.0 / self.A)
                    if (thred >= randgeneral):
                        a_general = a
                        break
                
                z_u.append(a_general)
                self.C_ua[u][a_general] += 1
                
                for w in range(len(tw.tweetwords)):
                    word = tw.tweetwords[w]
                    randback = random.random()
                    
                    if (randback > 0.5):
                        buffer_x = True
                    else:
                        buffer_x = False

                    if (buffer_x):
                        self.C_lv[1] += 1
                        self.C_word[a_general][word] += 1
                        self.countAllWord[a_general] += 1
                        x_u_d.append(buffer_x)
                    else:
                        self.C_lv[0] += 1
                        self.C_b[word] += 1
                        x_u_d.append(buffer_x)
                
                x_u.append(x_u_d)
                # x_u_d.clear()
                    
            self.z.append(z_u)
            self.x.append(x_u)
            # x_u.clear()
            # z_u.clear()
        
        print("Intialize Done")
        
    
    def estimate(self, users, nIter):
        niter = 0
        
        while True:
            niter += 1
            print("iteration" + " " + str(niter) + " ...")
            self.sweep(users)
            
            if (niter >= self.nIter):
                self.update_distribution()
                break

    def sweep(self, users):
        for cntuser in range(len(users)):
            buffer_user = users[cntuser]
            for cnttweet in range(buffer_user.tweetCnt):
                tw = buffer_user.tweets[cnttweet]
                self.sample_z(cntuser, cnttweet, buffer_user, tw)
                
                for cntword in range(len(tw.tweetwords)):
                    word = tw.tweetwords[cntword]
                    self.sample_x(cntuser, cnttweet, cntword, word)

    
    def update_distribution(self):
        
        for u in range(self.U):
            c_u_a = 0
            for a in range(self.A):
                c_u_a += self.C_ua[u][a]
                
            for a in range(self.A):
                self.theta_general[u][a] = ((self.C_ua[u][a] + self.alpha_general[a])*1.0) / ((c_u_a + self.alpha_general_sum)*1.0)
                

        for a in range(self.A):
            c_v = 0
            for v in range(self.V):
                c_v += self.C_word[a][v]
                
            for v in range(self.V):
                self.phi_word[a][v] = ((self.C_word[a][v] + self.beta_word[v])*1.0) / ((c_v + self.beta_word_sum)*1.0)

        
        c_b_v = 0
        for v in range(self.V):
            c_b_v += self.C_b[v]
            
        for v in range(self.V):
            self.phi_background[v] = ((self.C_b[v] + self.beta_background[v])*1.0) / ((c_b_v + self.beta_background_sum)*1.0)

        for l in range(2):
            self.rho[0] = ((self.C_lv[0] + self.gamma[0])*1.0) / ((self.C_lv[0] + self.C_lv[1] + self.gamma[0] + self.gamma[1])*1.0)
            self.rho[1] = ((self.C_lv[1] + self.gamma[1])*1.0) / ((self.C_lv[0] + self.C_lv[1] + self.gamma[0] + self.gamma[1])*1.0)

    
    def sample_x(self, u, d, n, word):
        binarylabel = self.x[u][d][n]
        
        if (binarylabel == True):
            binary = 1
        else:
            binary = 0
            

        self.C_lv[binary] -= 1
        if (binary == 0):
            self.C_b[word] -= 1
        else:
            self.C_word[self.z[u][d]][word] -= 1
            self.countAllWord[self.z[u][d]] -= 1
        
        binarylabel = self.draw_x(u, d, n, word)

        self.x[u][d][n] = binarylabel

        if (binarylabel == True):
            binary = 1
        else:
            binary = 0

        self.C_lv[binary] += 1
        
        if (binary == 0):
            self.C_b[word] += 1
        else:
            self.C_word[self.z[u][d]][word] += 1
            self.countAllWord[self.z[u][d]] += 1

    def sample_z(self, u, d, buffer_user, tw):
        
        tweet_topic = self.z[u][d]
        w = 0
        
        self.C_ua[u][tweet_topic] -= 1
        
        for w in range(len(tw.tweetwords)):
            word = tw.tweetwords[w]
            if (self.x[u][d][w] == True):
                self.C_word[tweet_topic][word] -= 1
                self.countAllWord[tweet_topic] -= 1


        buffer_z = self.draw_z(u, d, buffer_user, tw)

        tweet_topic = buffer_z
        self.z[u][d] = tweet_topic

        self.C_ua[u][tweet_topic] += 1
        
        for w in range(len(tw.tweetwords)):
            word = tw.tweetwords[w]
            if (self.x[u][d][w] == True): 
                self.C_word[tweet_topic][word] += 1
                self.countAllWord[tweet_topic] += 1
                
    def draw_x(self, u, d, n, word):
        returnvalue = False

        P_lv = [0.0, 0.0]
        Pb = 1
        Ptopic = 1

        P_lv[0] = ((self.C_lv[0] + self.gamma[0])*1.0) / ((self.C_lv[0] + self.C_lv[1] + self.gamma[0] + self.gamma[1])*1.0) # part 1 from counting C_lv

        P_lv[1] = ((self.C_lv[1] + self.gamma[1])*1.0) / ((self.C_lv[0] + self.C_lv[1] + self.gamma[0] + self.gamma[1])*1.0)

        Pb = ((self.C_b[word] + self.beta_background[word])*1.0) / ((self.C_lv[0] + self.beta_background_sum)*1.0) # word in background part(2)
        Ptopic = ((self.C_word[self.z[u][d]][word] + self.beta_word[word])*1.0) / ((self.countAllWord[self.z[u][d]] + self.beta_word_sum)*1.0)

        p0 = Pb * P_lv[0]
        p1 = Ptopic * P_lv[1]

        sum_p = p0 + p1
        randPick = random.random()

        if (randPick <= (p0 / (sum_p*1.0))):
            returnvalue = False
        else:
            returnvalue = True

        return returnvalue
    
    def draw_z(self, u, d, buffer_user, tw):
        
        P_topic = [0.0]*self.A
        pCount = [0]*self.A
        
        wordcnt = {} # store the topic words with frequency
        
        totalWords = 0 # total number of topic words
        
        for w in range(len(tw.tweetwords)):
            if (self.x[u][d][w] == True):
                totalWords += 1
                word = tw.tweetwords[w]
                if (not(word in wordcnt)):
                    wordcnt[word] = 1
                else:
                    wordcnt[word] += 1
        
        for a in range(self.A):
            P_topic[a] = ((self.C_ua[u][a] + self.alpha_general[a])*1.0) / ((buffer_user.tweetCnt - 1 + self.alpha_general_sum)*1.0)

            buffer_P = 1
            
            i = 0
            
            for entry in wordcnt:
                word = int(entry)
                buffer_cnt = int(wordcnt[entry])
                
                for j in range(buffer_cnt):
                    value = float((self.C_word[a][word] + self.beta_word[word] + j) / ((self.countAllWord[a] + self.beta_word_sum + i)*1.0))
                    i += 1
                    buffer_P *= value
                    buffer_P, pCount = self.isOverFlow(buffer_P, pCount, a)
            
            P_topic[a] *= math.pow(buffer_P, float(1))
            
        P_topic, pCount = self.reComputeProbs(P_topic, pCount)

        randz = random.random()

        sum_temp = 0
        
        for a in range(self.A):
            sum_temp += P_topic[a]

        thred = 0

        chosena = -1

        for a in range(self.A):
            thred += (P_topic[a] / (1.0*sum_temp))
            if (thred >= randz):
                chosena = a
                break

        if (chosena == -1):
            print("chosena equals -1, error!")

        wordcnt.clear()
        return chosena
          
    def isOverFlow(self, buffer_P, pCount, a2):
        if (buffer_P > 1e150):
            pCount[a2] += 1
            return float(buffer_P / 1e150), pCount

        if (buffer_P < 1e-150):
            pCount[a2] -= 1
            return buffer_P * 1e150, pCount
        
        return buffer_P, pCount
    
    def reComputeProbs(self, p_topic, pCount):
        max_temp = pCount[0]
        # print(max_temp + " ")
        for i in range(len(pCount)):
            if (pCount[i] > max_temp):
                max_temp = pCount[i]
            # System.out.print(pCount[i] + " ")
            
        if (max_temp > 0):
            self.print_console(p_topic, "previous: ", " ", "\n")
            
        for i in range(len(pCount)):
            p_topic[i] = p_topic[i] * math.pow(1e150, pCount[i] - max_temp)

        if (max_temp > 0):
            print(pCount[0] + " ", end='')
            for i in range(len(pCount)):
                print(pCount[i] + " ", end='')
                
            print("\n")
            self.print_console(p_topic, "current: ", " ", "\n")
            # System.exit(0);
        return p_topic, pCount

    
    def print_console(self, p_topic, prefix, midd, fedix):
        tstr = prefix
        for i in range(len(p_topic)):
            tstr += str(p_topic[i]) + midd

        print(tstr+fedix, end='')
        
    
    def outputWordsInTopics(self, output, slist, Cnt):
        
        writer = open(output, 'w', encoding='utf-8')
        
        rankList = []

        for a in range(self.A):
            topicline = "Topic " + str(a) + ":"
            writer.write(topicline)
            
            rankList = self.getTop(self.phi_word[a], rankList, Cnt)
            
            for i in range(len(rankList)):
                tmp = "\t" + str(slist[rankList[i]]) + "\t" + str(self.phi_word[a][rankList[i]])
                writer.write(tmp + "\n")
            
            rankList.clear()
            
        writer.close()
        
        
    def getTop(self, array, rankList, i):
        index = 0
        count = 0
        scanned = set()
        max_f = sys.float_info.min
        for m in range(len(array)):
            if (m < i):
                max_f = sys.float_info.min
                for no in range(len(array)):
                    if ((array[no] >= max_f) and (not(no in scanned))):
                        index = no
                        max_f = array[no]
                        
                scanned.add(index)
                rankList.append(index)
                
                #System.out.println(m + "\t" + index)
        return rankList     
    
    def outputTopicDistributionOnUsers(self, outputDir, users):
        
        outputfile = outputDir + "TopicsDistributionOnUsers.txt"
        writer = open(outputfile, 'w', encoding='utf-8')
        
        for u in range(self.U):
            bufferline1 = ""
            name = users[u].userID
            writer.write(name + "\t")
            for a in range(self.A):
                bufferline1 += str(self.theta_general[u][a]) + "\t"
            
            writer.write(bufferline1 + "\n")

        writer.close()


        outputfile = outputDir + "TopicCountsOnUsers.txt"
        writer = open(outputfile, 'w', encoding='utf-8')

        for u in range(self.U):
            bufferline1 = ""
            name = users[u].userID
            writer.write(name + "\t")
            for a in range(self.A):
                bufferline1 += str(self.C_ua[u][a]) + "\t"
                
            writer.write(bufferline1 + "\n")
            
        writer.close()
        
    def outputBackgroundWordsDistribution(self, output, slist, Cnt):
        
        writer = open(output, 'w', encoding='utf-8')
        
        rankList = []

        rankList = self.getTop(self.phi_background, rankList, Cnt)

        for i in range(len(rankList)):
            tmp = "\t" + slist[rankList[i]] + "\t" + str(self.phi_background[rankList[i]])
            writer.write(tmp + "\n")

        rankList.clear()
        writer.close()
        
    def outputTextWithLabel(self, output, users, uniWordMap):
        
        for u in range(len(users)):
            buffer_user = users[u]
            writer = open(output + "/" + str(buffer_user.userID), 'w', encoding='utf-8')
            
            for d in range(buffer_user.tweetCnt):
                buffer_tweet = buffer_user.tweets[d]
                line = "z=" + str(self.z[u][d]) + ":  "
                for n in range(len(buffer_tweet.tweetwords)):
                    word = buffer_tweet.tweetwords[n]
                    if (self.x[u][d][n] == True):
                        line += uniWordMap[word] + "/" + str(self.z[u][d]) + " "
                    else:
                        line += uniWordMap[word] + "/" + "false" + " "

                buffertime = buffer_tweet.time + 1
                if (buffertime <= 30):
                    if (buffertime < 10):
                        line = "2011-09-0" + str(buffertime) + ":\t" + line
                    else:
                        line = "2011-09-" + str(buffertime) + ":\t" + line
                        
                elif ((buffertime <= 61) and (buffertime > 30)):
                    buffer_time = buffertime - 30
                    if ((buffertime - 30) < 10):
                        line = "2011-10-0" + str(buffer_time) + ":\t" + line
                    else:
                        line = "2011-10-" + str(buffer_time) + ":\t" + line
                        
                elif (buffertime > 61):
                    buffer_time = buffertime - 61
                    if ((buffertime - 61) < 10):
                        line = "2011-11-0" + str(buffer_time) + ":\t" + line
                    else:
                        line = "2011-11-" + str(buffer_time) + ":\t" + line

                #outlines.add(line);
                writer.write(line + "\n")

            writer.close()

         #FileUtil.writeLines(output, outlines);
         #outlines.clear();
   