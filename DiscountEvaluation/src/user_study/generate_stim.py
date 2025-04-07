# for each sentence calculate score prob of word multiplied
# threshold sentence by length
# print unrecognized
# print top 100 csv

import math
import util
from urduhack import preprocessing
from tqdm import tqdm
from collections import Counter
import pandas as pd

import urduhack
urduhack.download()

def build_freq_table(n,data):
    '''
    We do not have an explicity vocab list so we will be generating it from the text.
    Using all the words identified this function creates a list of all possible ngrams.
    A dictionary using these as keys is then constructed. This will later be used to store
    ngram counts
    Returns:
        - dictionary which serves as a freqeuncy table
        - an int which represents the vocabulary size
    '''
    # we use a set for our vocab list to avoid repeats
    # we go over the dataset and add each word to our vocab set.
    tokens = []
    for sentence in tqdm(data, desc="Building histogram"):
        sentence = preprocessing.remove_punctuation(sentence)
        tokens += sentence.split()
    ngrams = list(zip(*[tokens[i:] for i in range(n)]))
    counts = Counter(ngrams)
    return counts

def threshold_frequency(n,freq_table):
    '''
    Threolds the data by combining all tokens below threshold value into a single UNK token
    Returns:
        - dictionary that is a filled frequency table.
    '''
    thresholded = {}
    unk = 0
    for ngram in tqdm(freq_table, desc="Thresholding histogram"):
        if (freq_table[ngram] > 10):
            thresholded[ngram] = freq_table[ngram]
        else:
            unk += freq_table[ngram]      # counting total frequency of UNK tokens
    thresholded[("UNK",) * n] = unk
    return thresholded

def calculate_probability(n_grams:dict,n_minus_1_grams):
    lm = {}
    # for each ngram
    for n_gram in tqdm(n_grams, desc="Building language model"):
        # get the frequency of the ngram
        numer = n_grams[n_gram]
        # get the frequency of the prefix ie:n-1 gram (ex: if we are training trigram then prefix is bigram)
        denom = n_minus_1_grams[n_gram[:-1]]
        # calcualte the probability in log space
        lm[n_gram] = math.log(numer) - math.log(denom)
    return lm

# read corpus sentences.
dakshina,_ = util.read_tsv('interim/transformed/sentences/dakshina_dataset')
roUrParl,_ = util.read_tsv('interim/transformed/sentences/roUrParl_dataset')
dataset,_ = util.read_tsv('interim/transformed/sentences/combined_subset')
training = set(roUrParl)
training = training.union(set(dakshina))
training = training.difference(set(dataset))
training = list(training)

n = 3

n_grams = build_freq_table(n,training)
n_grams = threshold_frequency(n,n_grams)
n_minus_1_grams = build_freq_table(n-1,training)
n_minus_1_grams = threshold_frequency(n-1,n_minus_1_grams)

lm = calculate_probability(n_grams, n_minus_1_grams)

estimates = {}
for sentence in tqdm(dataset):
    cleaned = preprocessing.remove_punctuation(sentence)
    tokens = cleaned.split()
    
    if len(tokens)<=8 or len(tokens)>= 12:
        continue
    
    total_log_prob = 0
    ngram_count = 0
    for i in range(len(tokens) - n + 1):
        ngram = tuple(tokens[i:i + n])
        log_prob = lm.get(ngram,lm[("UNK",)*n])
        total_log_prob += log_prob
        ngram_count += 1
    avg_log_prob = total_log_prob / ngram_count
    estimates[sentence] = avg_log_prob

df = pd.DataFrame.from_dict(estimates, orient="index", columns=["estimate"])
df.to_csv('user_study/results/stimuli_scores.csv')