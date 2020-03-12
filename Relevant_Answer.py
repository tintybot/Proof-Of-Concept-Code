import Relevant_Question
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
#get list of words
def get_word_bucket(data):
	stop_words = set(stopwords.words('english'))
	words_bucket=cleaning_text_(data)
	bucket=list()
	for words in words_bucket:
		for w in words:
			if w not in bucket:
				bucket.append(w)
	for words in stop_words:
		if words in bucket:
			bucket.remove(words)
	return(bucket)
#calculate most relevant answer
def relevant_ans(raw_vocab,q_answer_map):
	word_bucket=get_word_bucket(raw_vocab)
	#print(word_bucket)
	score=list()
	result=list()
	for ids in q_answer_map:
		answers=cleaning_text_(q_answer_map[ids])
		for i in range(0,len(answers)):
			ans=answers[i]
			sc=0
			for words in ans:
				if words in word_bucket:
					sc=sc+1
			score.append([ids,q_answer_map[ids][i],sc])
			result.append(sc)
	max_=-1
	index=list()
	for i in range(0,len(result)):
		if result[i]>max_:
			max_=result[i]
	for i in range(0,len(result)):
		if result[i]==max_:
			index.append(i)
	final_query=list()
	for i in index:
		final_query.append(score[i])
	return(final_query)

def main():
	questions=Relevant_Question.main()
	path="test.json"
	helper=ExtractDetails.LoadData(path)
	queries=helper.load()
	q_a_list=helper.get_selected_question(questions,queries) 
	answer=dict()
	result=relevant_ans(questions,q_a_list)
	final_result=helper.get_links(result,queries)
	return(final_result)
main()