import json
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
import nltk
import re
import random
nltk.download('stopwords')
stops = set(stopwords.words('russian') + ['и', 'как', 'в', 'а', 'на', 'что', 'нам', 'это',
                                          'тебе', 'твой'])

with open('morphs.json', 'r', encoding='utf-8') as f:
    morphs = json.load(f)

with open('verses.json', 'r', encoding='utf-8') as f:
    verses = json.load(f)

# считаем количество строчек и количество стихов
lines = len(morphs)
titles = len(verses)

# считаем части речи и сохраняем круговую диаграмку с ними
data = []
for morph in morphs:
    pos = morphs[morph][0]
    word = morph
    data.append([pos, word])
df = pd.DataFrame(data)
plot = df[0].value_counts().head(10).plot.pie()
plt.savefig('poses.png')

# сплитим строки на слова
# чистим от стоп слов, строим вордклауд, сохраняем его в файл
random.seed = 23
words = []
for title in verses:
    for line in verses[title]:
        text = line[1]
        text_new = (re.sub(r'[^\w\s]', '', text.lower())).split(' ')
        for t in text_new:
            words.append(t)
cloud = ' '.join([word for word in words if word not in stops])
wordcloud = WordCloud(
    background_color='white',
    width=800,
    height=800,
).generate(cloud)

plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.title('Облако слов')
plt.savefig('wordcloud.png')
