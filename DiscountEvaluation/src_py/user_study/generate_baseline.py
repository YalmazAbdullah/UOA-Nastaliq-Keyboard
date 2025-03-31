import pandas as pd
import re
import random
from tqdm import tqdm

# load in pesudo words
pesudowords = pd.read_csv("./user_study/pesudo_words.csv")
pesudowords = pesudowords[pesudowords['Rationale for Removal'].isna()]
print(len(pesudowords))

# organize pesudo words
pesudoword_dict = {}
for word in pesudowords["Pseudoword"]:
    length = len(word)
    if length not in pesudoword_dict:
        pesudoword_dict[length] = []
    pesudoword_dict[length].append(word)

# load in lorem ipsum
lorem_ipsum = None
with open('./user_study/lorem_ipsum.txt', 'r', encoding='utf-8') as file:
    lorem_ipsum = file.read()

# split sentences
sentences = re.split(r'([.!?])', lorem_ipsum)  # Split by sentence-ending punctuation
sentences = [s.strip() for s in sentences if s.strip()]  # Remove empty elements

# replace lorem ipsum words
pesudo_sentences = []
random.seed(1)
for i in range(0, len(sentences), 2):
    sentence = sentences[i]
    punctuation = sentences[i + 1] if i + 1 < len(sentences) else ""

    words = re.findall(r'\b\w+\b', sentence)  # Extract words without punctuation
    replaced_words = []
    for word in words:
        length = len(word)
        while length>=1:
            if length in pesudoword_dict:
                replacement = random.choice(pesudoword_dict[length])
                replaced_words.append(replacement)
                break
            else:
                length-=1
        else:
            # no suitable replacement found keep word.
            print(word)
            replaced_words.append(word)
    
    new_sentence = sentence
    for original, new in zip(words, replaced_words):
        new_sentence = new_sentence.replace(original, new, 1)
    pesudo_sentences.append(new_sentence + punctuation)

print(len(sentences))
print(len(pesudo_sentences))
print(pesudo_sentences)

df = pd.DataFrame({"Stim":pesudo_sentences})
df.to_csv("./user_study/results/pesudo_sentences.csv")
df = pd.DataFrame({"Stim":random.sample(pesudo_sentences,12)})
df.to_csv("./user_study/results/baseline.csv")


