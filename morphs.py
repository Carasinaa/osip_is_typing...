import json
from pymorphy2 import MorphAnalyzer
from rusyll import rusyll
morph = MorphAnalyzer()
rhymes = {}

with open('verses.json', 'r', encoding='utf-8') as f:
    verses = json.load(f)
    for title in verses:
        for line in verses[title]:
            word = line[0]
            ana = morph.parse(word)[0]
            pos = ana.tag.POS
            syllables = rusyll.word_to_syllables_wd(word)
            rhymes[word] = (pos, syllables)
with open('morphs.json', 'w', encoding='utf-8') as f:
  json.dump(rhymes, f, ensure_ascii = False)