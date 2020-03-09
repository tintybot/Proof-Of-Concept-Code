import requests
from bs4 import BeautifulSoup
import bs4
import pandas as pd
import json

l = []
link = []

def scraper(url):
    global l    
    r1 = requests.get(url)
    c1 = r1.content
    soup1 = BeautifulSoup(c1, 'html.parser')
    qs = soup1.find('div', {'id': 'question-header'}).findChildren('a',{'class':'question-hyperlink'})[0].text
    ans = soup1.find_all('div', {'class': 'answer'})
    for i in range(len(ans)):
        ss = ans[i].findChildren('div', {'class': 'post-text'})
        uvc = ans[i].findChildren('div', {'class': 'js-vote-count'})[0].text
        answers = ""
        for x in ss:
            answers = answers + x.text
        cmts = ans[i].findChildren('div', {'class': 'comment-body'})
        cmnt1 = "null"
        cmnt2 = "null"
        cmnt3 = "null"
        if(len(cmts) >= 3):
            cmnt1 = cmts[0].text
            cmnt2 = cmts[1].text
            cmnt3 = cmts[2].text
        elif (len(cmts) < 3) and (len(cmts) >= 2):
            cmnt1 = cmts[0].text
            cmnt2 = cmts[1].text
        elif (len(cmts) < 2) and (len(cmts) >= 1):
            cmnt1 = cmts[0].text
        tt = ans[i].findChildren('div', {'class': 'user-action-time'})[0].text
        sk = tt.split()
        tt = sk[1]+" "+sk[2]+" "+sk[3]
        mydict = {'Question': qs, 'Answer': answers, 'Time': tt,
                  "Comment 1": cmnt1, "Comment 2": cmnt2, "Comment 3": cmnt3, "Link": url,"UpVotes":uvc}
        l.append(mydict)

def startScaper():
    q = input()
    query = q.split()
    qs = ""
    for i in query:
        qs += '+'+i
    url = 'https://www.google.com/search?q=stackoverflow'+qs+'&oq=stackoverflow'+qs
    output_g = requests.get(url)
    output_g_text = bs4.BeautifulSoup(output_g.text, 'lxml')
    flag = 1
    global link
    for i in output_g_text.findAll('a'):
        for j in i.get_attribute_list('href'):
            if j.find('https://stackoverflow.com/') != -1:
                p = j.find('/&sa')
                link.append(j[len("/url?q="):p])
                flag = 0
                break
        if flag == 0:
            break
    if len(link) != 0:
        getRelatedLinks()

def getRelatedLinks():
    global link
    if len(link) != 0:
        url = link[0]
        r1 = requests.get(url)
        c1 = r1.content
        soup1 = BeautifulSoup(c1, 'html.parser')    
        relatedEle = soup1.find('div',{'class':'module sidebar-related'})
        relatedlinksEle = relatedEle.findChildren('a', {'class': 'question-hyperlink'})
        relatedlinksEleVote = relatedEle.findChildren('div', {'class': 'answer-votes answered-accepted large'})
        relatedLinksHref = []
        relatedLinksVote = []
        for x,y in zip(relatedlinksEle,relatedlinksEleVote):
            relatedLinksHref.append("https://stackoverflow.com/"+x.get_attribute_list('href')[0])
            relatedLinksVote.append(int(y.text))
        Z = [x for _,x in sorted(zip(relatedLinksVote,relatedLinksHref))]
        k=0
        for i in reversed(Z) :
            link.append(i)
            k=k+1
            if k == 1:
               break
        scrapeAndCreateFiles()
    else:
        print('Failed to fetch')

def scrapeAndCreateFiles(): 
    for x in link:
        scraper(x)
    
    df = pd.DataFrame(l)
    df.to_csv("Question&Answers.csv")

    with open('test.json', 'w') as fout:
        json.dump(l, fout)
        
        
startScaper()

#df1 = pd.read_csv("Question&Answers.csv")