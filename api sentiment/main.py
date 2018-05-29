import requests
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

counter = 0
output_file = open("results.txt", "w", encoding="utf8")
output_file.write("[")

for doc in documents:
    text = str(doc[1])

    data = [
        ('text', text),
    ]

    response = requests.post('http://text-processing.com/api/sentiment/', data=data)
    json_data = json.loads(response.text)
    print(str(counter) + "/1000")
    counter += 1
    output_file.write(str(json_data))
    output_file.write(",")

output_file.write("]")
output_file.close()