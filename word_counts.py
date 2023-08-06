import json

with open("data.json", "r") as f:
    data = json.load(f)


all_words = {}

for category in data:
    for word in data[category]:
        if word in all_words:
            all_words[word] += data[category][word]
        else:
            all_words[word] = data[category][word]
            
words = []
for word in all_words:
    words.append((word, all_words[word]))
    
words.sort(key=lambda word: word[1])

for i, word in enumerate(words):
    print(f"{i + 1}) {word[0]}  -  {word[1]}")
