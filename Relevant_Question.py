import ExtractDetails
import nltk
import math
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import numpy as np
#convert a list of charcters to list of sttrings
def remove_punctuation(string):
    punctuations='''!()[,]{\};:'"<>./?@#$%^&*_~'''
    for chars in string:
        if chars in punctuations:
            string=string.replace(chars,"")
    return(string)

#remove alpha numeric
def remove_alpha_numeric(string):
    line=list()
    for words in string.split(" "):
        if words.isalpha() == True:
            line.append(words)
    return(line)

#make into lower case
def lower_case(string):
    S_list=list()
    for s in string:
        S_list.append(s.lower())     
    return(S_list)

#perform basic actions
def cleaning_text_(data):
    cleaned_data=list()
    for d in data:
        d1=remove_punctuation(d)
        d1=remove_alpha_numeric(d1)
        d1=lower_case(d1)
        cleaned_data.append(d1)
    return cleaned_data

#perform basic actions
def cleaning_text(data):
    cleaned_data=list()
    d1=remove_punctuation(data)
    d1=remove_alpha_numeric(d1)
    d1=lower_case(d1)
    return d1 
#get list of words
def get_word_bucket(data):
	stop_words = set(stopwords.words('english'))
	words_bucket=cleaning_text(data)
	for words in stop_words:
		if words in words_bucket:
			words_bucket.remove(words)
	return(words_bucket)
def get_question_score(word_bucket,questions): 
	score=list()
	for question in questions:
		sc=0
		for words in question:
			if words in word_bucket:
				sc=sc+1
		score.append(sc)
	return score
def get_the_questions(ques,score):
	max_=-1
	list_of_questions=[]
	for sc in score:
		if sc > max_:
			max_=sc
	for i in range(0,len(score)):
		if score[i]==max_:
			list_of_questions.append(ques[i])
	return(list_of_questions)
def main():
	query="tensorflow not working in python 3.7"
	fname="test.json"
	helper=ExtractDetails.LoadData(fname)
	queries=helper.load()
	Questions=helper.get_questions(queries)
	questions=cleaning_text_(Questions)
	words_bucket=get_word_bucket(query)
	score=get_question_score(words_bucket,questions)
	relevant_questions=get_the_questions(Questions,score)
	#print(relevant_questions)
	return relevant_questions
main()