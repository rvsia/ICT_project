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

with open("resultstone.txt", "r", encoding="utf8") as f:
    data = json.load(f)

results = []

output_file = open("niceresults.txt","w", encoding="utf8")

for i in range(len(documents)):
    output_file.write(str(documents[i][0]) + ';' + str(data[i]["probability"]["neg"]) + ';' + str(data[i]["probability"]["neutral"]) + ';' + str(data[i]["probability"]["pos"]) + ';' + data[i]["label"])
    output_file.write("\n")

output_file.close()

print(data)