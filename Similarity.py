import nltk
import math
nltk.download('stopwords')
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import ExtractDetails
import numpy as np
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine
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
def cleaning_text(data):
    cleaned_data=list()
    for d in data:
        d1=remove_punctuation(d)
        d1=remove_alpha_numeric(d1)
        d1=lower_case(d1)
        cleaned_data.append(d1)
    return cleaned_data

 #creating vocabulary 
def create_vocubulary(data,threshold):
    Bag_of_words=list()
    for d in data.keys():
        if d not in Bag_of_words:
            if float(data[d])<=threshold:
                Bag_of_words.append(d)
    return(Bag_of_words)  

#encoding operations
def freq(docs,word):
    f=0
    for term in docs:
        if term==word:
            f=f+1
    return f

def calculate_freq(document_list,word):
    total_words=0
    fq=0
    frq_doc=0
    for docs in document_list:
        f=freq(docs,word)
        if f>0:
            total_words=total_words+len(docs)
            fq=fq+f
            frq_doc=frq_doc+1
        else:
            pass
        
    return(fq/total_words,frq_doc)  

def TF_IDF(document_list):
    logs=dict()
    for records in document_list: 
        for word in records:
            if word not in logs.keys():
                TF,DFT=calculate_freq(document_list,word)
                IDF=math.log10(len(document_list))-math.log10(DFT)
                W=TF*IDF
                logs[word]=str(W)
    return(logs)

def cal_thr(logs):
	s=0
	for ids in logs.keys():
		s=s+float(logs[ids])
	s=s/len(logs)
	return(s)


def main():
	path="test.json"
	stop_words = set(stopwords.words('english')) 
	helper=ExtractDetails.LoadData(path)
	query=helper.load()
	answers=helper.get_answers(query)
	raw_vocabulary=cleaning_text(answers)
	logs=TF_IDF(raw_vocabulary)
	thr=cal_thr(logs)
	vocabulary=create_vocubulary(logs,thr)
	dataset=list()
	for ans in raw_vocabulary:
		bag_of_zeros=list()
		for words in vocabulary:
			if words in ans:
				bag_of_zeros.append(1)
			else:
				bag_of_zeros.append(0)
		dataset.append(bag_of_zeros)
	dataset_array=np.array(dataset)
	similarity_results= 1-pairwise_distances(dataset_array, metric="cosine")
	print(similarity_results)
	return(similarity_results)
main()

