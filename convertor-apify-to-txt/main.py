import json

# variables


k = 0
ratings=[]
texts=[]


# reading a json
with open("data.json", encoding="utf8") as json_file:
    json_data = json.load(json_file)

    #print(json.dumps(json_data, sort_keys=True, indent = 4, separators = (',', ': ')))

    for j in json_data:
        for i in range(min(len(j['rating']),len(j['text']))):
            ratings.append(j['rating'][i])
            texts.append(j['text'][i])
            k += 1

# making a output file

output_file = open("output_file.txt", "w", encoding="utf8")

for line in range(len(ratings)):
    output_file.write(ratings[line] + " " + texts[line].replace("\n", "") + "\n")

output_file.close()
