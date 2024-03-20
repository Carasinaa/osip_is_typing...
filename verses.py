import pandas as pd
import string
import json

verses_final = {}
titles = []
verses = []
df = pd.read_csv('output.csv')
for d in df['title']:
    titles.append(d)
for d in df['verse']:
    verses.append(d)

for i in range(len(titles)):
    title = titles[i]
    verse = verses[i]
    verse = verse.strip().split('\n')
    lines = []
    for v in verse:
        if not v.isdigit():
            v = v.rstrip(string.punctuation).replace('—', '').replace('…', '')
            if not v == '':
                w = v.replace(string.punctuation, '').split()
                rhyme = w[-1]

                lines.append((rhyme, v))
    verses_final[title] = lines

with open('verses.json', 'w', encoding='utf-8') as f:
    json.dump(verses_final, f, ensure_ascii = False)
