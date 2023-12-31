# -*- coding: utf-8 -*-
"""AI_assign_8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MSnl4NwjPhaUjf21j4mk1C97IKLlMJd7

#Importing Libraries
"""

import numpy as np
import pandas as pd
import nltk
import math
import time
from nltk.corpus import stopwords
nltk.download('stopwords')
from google.colab import files

upload=files.upload()

df = pd.read_csv('/content/smsspam_dataset.csv')

"""#Defining stop words"""

stop_words = set(stopwords.words('english'))

"""#Seperating spam and ham messages"""

def seperate_ham_and_spam_message(X_train,y_train):
    spam_messages_X = []
    ham_messages_X = []
    count = 0

    for lines in X_train:
        if y_train[count]=="spam":
            spam_messages_X.append(lines)
        else:
            ham_messages_X.append(lines)
        count += 1

    spam_message_count  = len(spam_messages_X)
    ham_message_count = len(ham_messages_X)
    total_message_count = spam_message_count + ham_message_count

    return spam_messages_X,spam_message_count,ham_messages_X,ham_message_count,total_message_count

"""#Calculating probability of each classes"""

def probability_of_each_class(spam_message_count,ham_message_count,):
    total_message_count = spam_message_count+ham_message_count
    spam_class_prob = spam_message_count/total_message_count
    ham_class_prob = ham_message_count/total_message_count
    return spam_class_prob,ham_class_prob

"""#calculating spam words and its freq"""

def calculate_spam_word_frequency(spam_messages_X,multivariate_flag):
    spam_words_freq = {}
    if(multivariate_flag):
        for lines in(spam_messages_X):
            for word in set(lines.split(" ")):
                word = word.strip('.,!;()[]"$%@#&/\|\'-_+=*(){}[]:~`').lower()
                if len(word)>0:
                    #print(word)
                    if word not in spam_words_freq.keys():
                        spam_words_freq[word] = 1
                    else:
                        spam_words_freq[word] += 1
    else:
        for lines in(spam_messages_X):
            for word in(lines.split(" ")):
                word = word.strip('.,!;()[]"$%@#&/\|\'-_+=*(){}[]:~`').lower()
                if len(word)>0 and word not in stop_words:
                    #print(word)
                    if word not in spam_words_freq.keys():
                        spam_words_freq[word] = 1
                    else:
                        spam_words_freq[word] += 1
    return spam_words_freq

"""#calculating ham words and its freq"""

def calculate_ham_word_frequency(ham_messages_X,multivariate_flag):
    ham_words_freq = {}
    if(multivariate_flag):
      for lines in(ham_messages_X):
        for word in(lines.split(" ")):
            word = word.strip('.,!;()[]"$%@#&/\|\'-_+=*(){}[]:~`').lower()
            if len(word)>0 and word not in stop_words:
                if word not in ham_words_freq.keys():
                    ham_words_freq[word] = 1
                else:
                    ham_words_freq[word] += 1
    else:
        for lines in(ham_messages_X):
            for word in(lines.split(" ")):
                word = word.strip('.,!;()[]"$%@#&/\|\'-_+=*(){}[]:~`').lower()
                if len(word)>0 and word not in stop_words:
                    if word not in ham_words_freq.keys():
                        ham_words_freq[word] = 1
                    else:
                        ham_words_freq[word] += 1
    return ham_words_freq

"""#calculating all words and its freq"""

def calculate_all_word_frequency(ham_words_freq,spam_words_freq):
    all_words_freq = spam_words_freq.copy()
    for word in(ham_words_freq.keys()):
        if(word not in all_words_freq.keys()):
            all_words_freq[word] = ham_words_freq[word]
        else:
            all_words_freq[word] += ham_words_freq[word]
    return all_words_freq

"""#preprocessing and training"""

def preprocessing_and_training(X_train,y_train,multivariate_flag):
    start_time = time.time()
    spam_messages_X,spam_message_count,ham_messages_X,ham_message_count,total_message_count = seperate_ham_and_spam_message(X_train,y_train)

    ham_words_freq = calculate_ham_word_frequency(ham_messages_X,multivariate_flag)     #return dict
    spam_words_freq = calculate_spam_word_frequency(spam_messages_X,multivariate_flag)  #return dict
    all_words_freq = calculate_all_word_frequency(ham_words_freq,spam_words_freq)

    sum_ham_words_freq = sum(ham_words_freq.values())
    sum_spam_words_freq = sum(spam_words_freq.values())
    sum_all_words_freq = sum(all_words_freq.values())

    spam_class_prob,ham_class_prob = probability_of_each_class(spam_message_count,ham_message_count)
    end_time = time.time()
    print("Time taken for each model to train (time taken for preprocessing and training not for testing) = ",round(end_time-start_time,3),"sec",sep="")
    return spam_message_count,ham_message_count,total_message_count,ham_words_freq,spam_words_freq,all_words_freq,sum_ham_words_freq,sum_spam_words_freq,sum_all_words_freq,spam_class_prob,ham_class_prob

"""#Multinomial Testing"""

def testing_multinomial_naive_bayes(X_test,spam_words_freq,ham_words_freq,sum_ham_words_freq,sum_spam_words_freq,all_words_freq,spam_class_prob,ham_class_prob):
    smoothingfactor = 1
    predY = []
    for lines in(X_test):
        #for class spam
        prob_s = 1
        for word in(lines.split(" ")):
            word = word.strip('.,!;()[]"$%@#&/\|\'-_+=*(){}[]:~`').lower()
            prob_s = prob_s + math.log((spam_words_freq.get(word,0)+smoothingfactor)/(sum_spam_words_freq+len(all_words_freq)*smoothingfactor))

        prob_s += math.log(spam_class_prob)

        #for class ham
        prob_h = 1
        for word in(lines.split(" ")):
            word = word.strip('.,!;()[]"$%@#&/\|\'-_+=*(){}[]:~`').lower()
            prob_h = prob_h + math.log((ham_words_freq.get(word,0)+smoothingfactor)/(sum_ham_words_freq+len(all_words_freq)*smoothingfactor))

        prob_h += math.log(ham_class_prob)

        #print(prob_h)
        if(prob_s>=prob_h):
            predY.append("spam")
        else:
            predY.append("ham")
    return predY

"""#Multivariate testing"""

def testing_multivariate_naive_bayes(X_test,spam_words_freq,ham_words_freq,sum_ham_words_freq,sum_spam_words_freq,sum_all_words_freq,spam_class_prob,ham_class_prob):
    smoothingfactor = 1
    predY = []
    for lines in(X_test):
        #for class spam
        prob_s = 1
        for word in(lines.split(" ")):
            word = word.strip('.,!;()[]"$%@#&/\|\'-_+=*(){}[]:~`').lower()
            prob_s = prob_s + math.log((spam_words_freq.get(word,0)+smoothingfactor)/(sum_spam_words_freq+2*smoothingfactor))

        prob_s += math.log(spam_class_prob)

        #for class ham
        prob_h = 1
        for word in(lines.split(" ")):
            word = word.strip('.,!;()[]"$%@#&/\|\'-_+=*(){}[]:~`').lower()
            prob_h = prob_h + math.log((ham_words_freq.get(word,0)+smoothingfactor)/(sum_ham_words_freq+2*smoothingfactor))

        prob_h += math.log(ham_class_prob)

        #print(prob_h)
        if(prob_s>=prob_h):
            predY.append("spam")
        else:
            predY.append("ham")
    return predY

"""#Multinomial Naive Bayes"""

def multinomial_Naive_Bayes(X_train,y_train,X_test,y_test,multivariate_flag):

    #preprocessing and training
    spam_message_count,ham_message_count,total_message_count,ham_words_freq,spam_words_freq,all_words_freq,sum_ham_words_freq,sum_spam_words_freq,sum_all_words_freq,spam_class_prob,ham_class_prob = preprocessing_and_training(X_train,y_train,multivariate_flag)

    #testing
    predY = testing_multinomial_naive_bayes(X_test,spam_words_freq,ham_words_freq,sum_ham_words_freq,sum_spam_words_freq,all_words_freq,spam_class_prob,ham_class_prob)

    spamcount = 0
    hamcount = 0
    precision = 0
    recall = 0
    TP = 0
    FP = 0
    FN = 0

    for i in range(len(predY)):
        #print(predY[i])
        if(predY[i]==y_test[i]):
            if(y_test[i]=="spam"):
                spamcount += 1
            else:
                hamcount += 1
                TP +=1  #actual ham pred ham
        else:
            if(y_test[i]=="spam"):  #actual Spam pred ham
              FN +=1
            else: #actual ham pred spam
              FP +=1
    precision  = (TP/(TP+FP))
    recall = (TP/(TP+FN))

    spam_Accuracy = (float(spamcount)/float(spam_message_count))
    ham_Accuracy = (float(hamcount)/float(ham_message_count))
    total_Accuracy = ((float(hamcount)+float(spamcount))/float(total_message_count))

    return spam_Accuracy,ham_Accuracy,total_Accuracy,precision,recall

"""#Multivariate Naive Bayes"""

def multivariate_Naive_Bayes(X_train,y_train,X_test,y_test,multivariate_flag):
    #preprocessing and training
    spam_message_count,ham_message_count,total_message_count,ham_words_freq,spam_words_freq,all_words_freq,sum_ham_words_freq,sum_spam_words_freq,sum_all_words_freq,spam_class_prob,ham_class_prob = preprocessing_and_training(X_train,y_train,multivariate_flag)
    predY = testing_multivariate_naive_bayes(X_test,spam_words_freq,ham_words_freq,sum_ham_words_freq,sum_spam_words_freq,sum_all_words_freq,spam_class_prob,ham_class_prob)

    spamcount = 0
    hamcount = 0
    precision = 0
    recall = 0
    TP = 0
    FP = 0
    FN = 0

    for i in range(len(predY)):
        #print(predY[i])
        if(predY[i]==y_test[i]):
            if(y_test[i]=="spam"):
                spamcount += 1
            else:
                hamcount += 1
                TP +=1  #actual ham pred ham
        else:
            if(y_test[i]=="spam"):  #actual Spam pred ham
              FN +=1
            else: #actual ham pred spam
              FP +=1

    precision  = (TP/(TP+FP))
    recall = (TP/(TP+FN))
    spam_Accuracy = (float(spamcount)/float(spam_message_count))
    ham_Accuracy = (float(hamcount)/float(ham_message_count))
    total_Accuracy = ((float(hamcount)+float(spamcount))/float(total_message_count))

    return spam_Accuracy,ham_Accuracy,total_Accuracy,precision,recall

"""#Evaluating Classifier"""

#splitting dataset into training and testing
split_ratio = 0.5
X_train = df.iloc[:round(len(df)*split_ratio),-1].values
y_train = df.iloc[:round(len(df)*split_ratio),0].values
X_test = df.iloc[round(len(df)*split_ratio):,-1].values
y_test = df.iloc[round(len(df)*split_ratio):,0].values

print("Enter 1 to run multivariate Naive Bayes and 0 for multinomial Naive Bayes")
multivariate_flag=int(input())
if(multivariate_flag):
    spam_Accuracy,ham_Accuracy,total_Accuracy,precision,recall = multivariate_Naive_Bayes(X_train,y_train,X_test,y_test,multivariate_flag)
else:
    spam_Accuracy,ham_Accuracy,total_Accuracy,precision,recall = multinomial_Naive_Bayes(X_train,y_train,X_test,y_test,multivariate_flag)

print("Spam Accuracy  = ",round(spam_Accuracy*100,2),"%",sep="")
print("Ham Accuracy   = ",round(ham_Accuracy*100,2),"%",sep="")
print("Total Accuracy = ",round(total_Accuracy*100,2),'%',sep="")

"""#5-fold cross-validation"""

total_count = len(df)
fold = 5
split_ratio = round(1/fold)
avg_accuracy = 0
print("Enter 1 to run multivariate Naive Bayes and 0 for multinomial Naive Bayes")
multivariate_flag=int(input())
for i in range(fold):
    start = round(total_count/fold)*(i)
    end = round(total_count/fold)*(i+1)

    X_train = df.iloc[np.r_[0:start,end:],-1].values
    X_test = df.iloc[start:end,-1].values
    y_train = df.iloc[np.r_[0:start,end:],0].values
    y_test = df.iloc[start:end,0].values

    if(multivariate_flag):
        spam_Accuracy,ham_Accuracy,total_Accuracy,precision,recall = multivariate_Naive_Bayes(X_train,y_train,X_test,y_test,multivariate_flag)
    else:
        spam_Accuracy,ham_Accuracy,total_Accuracy,precision,recall = multinomial_Naive_Bayes(X_train,y_train,X_test,y_test,multivariate_flag)

    #print("Fold Iteration",i+1,"Spam Accuracy = ",spam_Accuracy,"Ham Accuracy = ",ham_Accuracy,"Total Accuracy = ",total_Accuracy)
    avg_accuracy += total_Accuracy

avg_accuracy *= (1/fold)
print("Average_accuracy = ",round(avg_accuracy*100,2),'%',sep="")

"""#10-fold cross-validation"""

prec = float(0)
rec = float(0)
total_count = len(df)
fold = 10
split_ratio = round(1/fold)
avg_accuracy = 0
print("Enter 1 to run multivariate Naive Bayes and 0 for multinomial Naive Bayes")
multivariate_flag=int(input())
for i in range(fold):
    start = round(total_count/fold)*(i)
    end = round(total_count/fold)*(i+1)

    X_train = df.iloc[np.r_[0:start,end:],-1].values
    X_test = df.iloc[start:end,-1].values
    y_train = df.iloc[np.r_[0:start,end:],0].values
    y_test = df.iloc[start:end,0].values

    if(multivariate_flag):
        spam_Accuracy,ham_Accuracy,total_Accuracy,precision,recall = multivariate_Naive_Bayes(X_train,y_train,X_test,y_test,multivariate_flag)
    else:
        spam_Accuracy,ham_Accuracy,total_Accuracy,precision,recall = multinomial_Naive_Bayes(X_train,y_train,X_test,y_test,multivariate_flag)

    #print("Fold Iteration",i+1,"Spam Accuracy = ",spam_Accuracy,"Ham Accuracy = ",ham_Accuracy,"Total Accuracy = ",total_Accuracy)
    avg_accuracy += total_Accuracy
    prec += precision
    rec += recall


avg_accuracy *= (1/fold)
fscore = (2*prec*rec)/(prec+rec)
print("Precision = ",prec)
print("Recall    = ",rec)
print("F-Score   = ",fscore)
print("Average_accuracy = ",round(avg_accuracy*100,2),"%",sep="")