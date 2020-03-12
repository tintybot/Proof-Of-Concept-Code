import json
class LoadData:
	def __init__(self,path):
		self.path=path

	def load(self):
		with open (self.path) as json_file:
			answers=json.loads(json_file.read())
		return answers

	def get_answers(self,queries):
		answers=[]
		self.queries=queries
		for i in range(0,len(self.queries)):
			answers.append(self.queries[i]['Answer'])
		return(answers)

	def get_questions(self,queries):
		questions=[]
		self.queries=queries
		for i in range(0,len(self.queries)):
			if self.queries[i]['Question'] in questions:
				pass
			else:
				questions.append(self.queries[i]['Question'])
		return(questions)
	def get_selected_question(self,sel_ques,queries):
		self.sel_ques=sel_ques
		self.queries=queries
		requested_query=dict()
		for q in self.sel_ques:
			answers=list()
			for i in range(0,len(self.queries)):
				if self.queries[i]['Question']==q:
					answers.append(self.queries[i]['Answer'])
				else:
					pass
			requested_query[q]=answers
		return(requested_query)
	def get_links(self,result,queries):
		self.result=result
		answers=list()
		for ques,ans,sc in self.result:
			for i in range(0,len(self.queries)):
				if self.queries[i]['Question']==ques and self.queries[i]['Answer']==ans :
					answers.append([ques,ans,self.queries[i]['Link']])
		return(answers)


#obj=LoadData("test.json")
#a=obj.load()
#b=obj.get_questions(a)
#print(b)

