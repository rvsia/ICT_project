import requests
from watson_developer_cloud import ToneAnalyzerV3
import json


# LOADING A DOCUMENTS
input_file = open("output.txt", "r", encoding="utf8")

c = input_file.readlines()

documents = []
counter = 0

for line in c:
    l = line[2:]
    l = l.replace("\n", "")
    classa = line.split(' ')[0]
    documents.append([])
    documents[counter].append(classa)
    documents[counter].append(l)
    counter += 1

input_file.close()


# TEST

'''
for doc in documents:
    print(str(doc[0]) + " " + str(doc[1]))
    print(len(documents))
'''



tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    username='',
    password=''
)

tone_analyzer.set_url('https://gateway.watsonplatform.net/tone-analyzer/api')
content_type = 'application/json'


print(documents[0][1])
counter = 0
output_file = open("results.txt", "w", encoding="utf8")
output_file.write("[")

for doc in documents:
    text = str(doc[1])
    tone = tone_analyzer.tone({"text": text}, content_type, False)
    print(str(counter) + "/1000")
    counter += 1
    output_file.write(json.dumps(tone, indent=2))
    output_file.write(",")

output_file.write("]")
output_file.close()







