import json
import csv
#import Similarity
#print(Similarity.main())
with open("test.json") as json_file:
    queries=json.loads(json_file.read())

comments=list()
#print(len(queries))
#extract all comments
for i in range(0,len(queries)):
	comments.append(queries[i]["Comment 1"])
	comments.append(queries[i]["Comment 2"])
	comments.append(queries[i]["Comment 3"])
with open('comment_data.csv', 'w+', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["comments","Label"])
    for x in comments:
    	if x=='null':
    		pass
    	else:
        	writer.writerow([x,-1])
        	
