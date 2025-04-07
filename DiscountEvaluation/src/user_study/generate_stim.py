# for each sentence calculate score prob of word multiplied
# threshold sentence by length
# print unrecognized
# print top 100 csv

import math
import util
import heapq
import pandas as pd
import unicodedata
import pprint
from urduhack import normalize

# read each word and freq in list
word_freq = {}
with open("./user_study/word_freq.txt", "r", encoding="utf-8") as file:
    for line in file:
        parts = line.strip().split(' ')
        if len(parts) == 2:
            word, frequency = parts
            try:
                frequency = int(frequency)
                word = normalize(word)
                word_freq[word] = frequency
            except:
                pass
pprint.pprint(word_freq)

# threshold word freq to account for unkowns
THRESHOLD = 300
unk = 0
total_tokens = 0
thresolded_word_freq = {}
for word in word_freq:
    if (word_freq[word] > THRESHOLD):
        thresolded_word_freq[word] = word_freq[word]
    else:
        unk += word_freq[word]
    total_tokens += word_freq[word] 
thresolded_word_freq["UNK"] = unk
# pprint.pprint(thresolded_word_freq)

# build model
lm = {word: (math.log(freq/float(total_tokens))) for word, freq in thresolded_word_freq.items()}

# read corpus sentences.
sentences,_ = util.read_tsv('transformed/sentences/combined_subset')

#calculate likelihood for each sentence
estimates = {}
test = 0
bad = {}
for i in range(len(sentences)):
    sentence = normalize(sentences[i])
    tokens = sentence.split()
    estimate = 0
    for token in tokens:
        test+=1
        estimate += lm.get(token,lm["UNK"])
        if(not lm.get(token,None)):
            # bad[token] = bad.get(token, 0)+1
            print(token)
    estimate = math.exp(estimate)/len(tokens)
    estimates[sentences[i]] = estimate
# pprint.pprint(bad)
print(test)

df = pd.DataFrame.from_dict(estimates, orient="index", columns=["estimate"])
df.to_csv('user_study/results/stimuli_scores.csv')

filtered = []
sorted_sentences = sorted(estimates.items(), key=lambda x: x[1], reverse=True)
for sentence in sorted_sentences:
    sentence = sentence[0]
    tokens = sentence.split()
    if 8 <= len(tokens) <= 12:
        filtered.append(sentence)
df = pd.DataFrame({"Stim":filtered})
df.to_csv('user_study/results/stimuli_filtered.csv')
    

