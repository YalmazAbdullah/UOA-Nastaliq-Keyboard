import math
import util
from urduhack import preprocessing
from tqdm import tqdm
from collections import Counter
import pandas as pd
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

THRESHOLD = 5
UNK_TOKEN = "<UNK>" # Use a distinct token, angle brackets are common convention

def prepare_and_build_vocab(data):
    """
    Preprocesses data, builds vocabulary based on frequency threshold.
    Returns list of lists of tokens (original structure) and vocabulary.
    """
    tokens_nested = [] # Keep sentence structure
    all_tokens_flat = [] # For vocab count

    logging.info("Preprocessing and tokenizing for vocabulary...")
    for sentence in tqdm(data, desc="Preprocessing & Tokenizing"):
        cleaned = preprocessing.remove_punctuation(sentence)
        sentence_tokens = cleaned.split()
        # Skip empty sentences after cleaning
        if not sentence_tokens:
            continue
        tokens_nested.append(sentence_tokens)
        all_tokens_flat.extend(sentence_tokens)

    logging.info(f"Building unigram counts from {len(all_tokens_flat)} tokens...")
    counts = Counter(all_tokens_flat)

    logging.info(f"Building vocabulary with frequency threshold > {THRESHOLD}...")
    vocabulary = {word for word, count in counts.items() if count > THRESHOLD}
    vocabulary.add(UNK_TOKEN) # Add the UNK token itself
    logging.info(f"Vocabulary size: {len(vocabulary)} (including {UNK_TOKEN})")

    # Replace OOV in the nested list structure
    logging.info(f"Replacing OOV words with {UNK_TOKEN} in sentence structures...")
    prepared_nested = []
    for sentence_tokens in tqdm(tokens_nested, desc="Replacing OOV"):
        processed_sentence = [token if token in vocabulary else UNK_TOKEN for token in sentence_tokens]
        prepared_nested.append(processed_sentence)

    return prepared_nested, vocabulary

# Modified build_freq_table to work sentence by sentence
def build_freq_table_sent_aware(n, nested_token_list):
    """
    Builds n-gram frequency table from a list of tokenized sentences,
    respecting sentence boundaries.
    """
    logging.info(f"Building {n}-gram frequency table (sentence aware)...")
    total_ngrams_counter = Counter()
    num_sentences_processed = 0

    for sentence_tokens in tqdm(nested_token_list, desc=f"Generating {n}-grams"):
        if len(sentence_tokens) >= n:
            # Generate n-grams for this sentence
            ngrams_in_sentence = list(zip(*[sentence_tokens[i:] for i in range(n)]))
            total_ngrams_counter.update(ngrams_in_sentence)
            num_sentences_processed +=1
        # else: # Optional: log sentences too short for n-grams
            # if sentence_tokens: # Log only if not empty
                 # logging.debug(f"Sentence too short for {n}-grams: {' '.join(sentence_tokens)}")

    logging.info(f"Processed {num_sentences_processed} sentences for {n}-grams.")
    logging.info(f"Found {len(total_ngrams_counter)} unique {n}-grams.")
    return total_ngrams_counter

# Added safety for zero denominator
def calculate_probability(n_grams: dict, n_minus_1_grams: dict, n: int):
    """Calculates log probabilities P(w_n | w_1, ..., w_{n-1})"""
    lm = {}
    num_zero_denom = 0
    num_greater_numer = 0
    unk_ngram = (UNK_TOKEN,) * n

    logging.info("Building language model probabilities...")
    for n_gram, numer in tqdm(n_grams.items(), desc="Calculating probabilities"):
        prefix = n_gram[:-1]
        denom = n_minus_1_grams.get(prefix)

        if denom is None or denom == 0:
            num_zero_denom += 1
            lm[n_gram] = -float('inf') # Assign -inf for zero probability
        elif numer > denom:
            # This indicates a serious issue in counting if it happens now
            num_greater_numer += 1
            logging.error(f"CRITICAL COUNTING ERROR: N-gram {n_gram} count ({numer}) > Prefix {prefix} count ({denom})")
            lm[n_gram] = 0.0 # Assign log(1) = 0, but this is wrong
        else:
            lm[n_gram] = math.log(numer) - math.log(denom)

    if num_zero_denom > 0:
         logging.warning(f"Encountered {num_zero_denom} n-grams with zero-count prefixes (assigned -inf log_prob).")
    if num_greater_numer > 0:
         logging.error(f"CRITICAL: Encountered {num_greater_numer} n-grams with counts > prefix counts.")

    # Determine a fallback probability. Use the calculated UNK prob if possible, else default.
    default_fallback_log_prob = -100.0 # Default large negative value
    calculated_unk_prob = lm.get(unk_ngram)

    if calculated_unk_prob is not None and calculated_unk_prob != -float('inf'):
        final_default_unk_log_prob = calculated_unk_prob
        logging.info(f"Using calculated log_prob for {unk_ngram} as default fallback: {final_default_unk_log_prob}")
    else:
        # Add the default UNK probability to the model if it wasn't calculated or was -inf
        lm[unk_ngram] = default_fallback_log_prob
        final_default_unk_log_prob = default_fallback_log_prob
        logging.warning(f"{unk_ngram} log_prob was not validly calculated or missing. Added/using default fallback: {final_default_unk_log_prob}")

    return lm, final_default_unk_log_prob # Return LM and the determined default prob

def save_lm_to_csv(lm, n, filename):
    """Saves the language model dictionary to a CSV file."""
    logging.info(f"Saving language model probabilities to {filename}...")

    # Prepare data for DataFrame
    lm_data = []
    # Dynamically create column names based on n
    ngram_cols = [f"word_{i+1}" for i in range(n)]
    columns = ngram_cols + ["log_prob"]

    for ngram_tuple, log_prob in tqdm(lm.items(), desc="Preparing LM for CSV"):
        # Combine ngram components and log_prob into a list for the row
        # Ensure components are strings, handle potential non-string items if any
        row_data = [str(item) for item in ngram_tuple] + [log_prob]
        lm_data.append(row_data)

    if lm_data: # Check if there's data to save
        lm_df = pd.DataFrame(lm_data, columns=columns)
        # Optional: Sort the language model, e.g., by probability or n-gram components
        # lm_df = lm_df.sort_values(by="log_prob", ascending=False) # Sort by probability
        try:
            lm_df.to_csv(filename, index=False, encoding='utf-8') # Specify encoding
            logging.info(f"Language model successfully saved to {filename}")
        except Exception as e:
            logging.error(f"Failed to save language model CSV to {filename}: {e}")
    else:
        logging.warning("Language model dictionary 'lm' was empty. No CSV saved.")

# --- Main Script ---

logging.info("Reading datasets...")
dakshina, _ = util.read_tsv('interim/transformed/sentences/dakshina_dataset')
roUrParl, _ = util.read_tsv('interim/transformed/sentences/roUrParl_dataset')
dataset, _ = util.read_tsv('interim/transformed/sentences/combined_subset')

logging.info("Preparing training data...")
training_set = set(roUrParl)
training_set = training_set.union(set(dakshina))
training_set = training_set.difference(set(dataset))
training_list = list(training_set)
logging.info(f"Training set size: {len(training_list)} sentences")
logging.info(f"Test dataset size: {len(dataset)} sentences")

# Prepare training data (returns list of lists with <UNK> and vocab)
prepared_nested_sentences, vocab = prepare_and_build_vocab(training_list)

n = 2

# Build N-grams and N-1 grams sentence-aware
n_grams = build_freq_table_sent_aware(n, prepared_nested_sentences)
n_minus_1_grams = build_freq_table_sent_aware(n - 1, prepared_nested_sentences)

# Calculate LM probabilities and get the default UNK prob
lm, default_unk_log_prob = calculate_probability(n_grams, n_minus_1_grams, n)
logging.info(f"Default log probability for unknown n-grams set to: {default_unk_log_prob}")

save_lm_to_csv(lm, n, 'language_model_probabilities.csv')

# --- Scoring ---
logging.info("Scoring dataset sentences...")
estimates = {}
unrecognized_ngram_count = 0
total_ngram_count_scoring = 0
scored_sentence_count = 0
skipped_length_count = 0
skipped_short_count = 0

for sentence in tqdm(dataset, desc="Scoring"):
    cleaned = preprocessing.remove_punctuation(sentence)
    tokens = cleaned.split()

    if not tokens: # Skip empty sentences after cleaning
        continue

    if len(tokens) <= 8 or len(tokens) >= 12:
        skipped_length_count += 1
        continue

    if len(tokens) < n:
        skipped_short_count += 1
        continue

    # Replace OOV using the vocabulary from training
    tokens_with_unk = [token if token in vocab else UNK_TOKEN for token in tokens]

    total_log_prob = 0
    ngram_count_in_sentence = 0
    sentence_has_valid_ngram = False
    for i in range(len(tokens_with_unk) - n + 1):
        ngram = tuple(tokens_with_unk[i:i + n])
        total_ngram_count_scoring += 1
        ngram_count_in_sentence += 1

        log_prob = lm.get(ngram, None) # Check if ngram exists in LM

        if log_prob is None:
            # Ngram was not seen in training (or its prefix had 0 count -> -inf was overwritten maybe)
            log_prob = default_unk_log_prob
            unrecognized_ngram_count += 1
        elif log_prob == -float('inf'):
            # Prefix had zero count -> impossible transition based on training data
            # Use the default fallback, as this ngram essentially wasn't seen usefully
            log_prob = default_unk_log_prob
            # You might want to track these specific -inf cases separately if needed
            # logging.debug(f"Ngram {ngram} had -inf probability, using default.")


        total_log_prob += log_prob
        if log_prob != -float('inf'): # Check if at least one ngram was validly scored
             sentence_has_valid_ngram = True


    # Calculate average only if ngrams were generated
    # Avoid division by zero if ngram_count_in_sentence is 0 (shouldn't happen with length checks)
    if ngram_count_in_sentence > 0 and sentence_has_valid_ngram:
        avg_log_prob = total_log_prob / ngram_count_in_sentence
        estimates[sentence] = math.exp(avg_log_prob)
        scored_sentence_count += 1
    # else: # Optional: Log sentences that ended up with no score (e.g., all ngrams were -inf)
        # logging.warning(f"Sentence not scored (no valid ngrams or count was 0): {' '.join(tokens)}")


# (Rest of the logging and output code remains the same)
# --- Logging Summary ---
logging.info(f"Finished scoring.")
logging.info(f"Scored {scored_sentence_count} sentences.")
logging.info(f"Skipped {skipped_length_count} sentences due to length constraints (<=8 or >=12 tokens).")
logging.info(f"Skipped {skipped_short_count} sentences shorter than n={n} tokens.")
if total_ngram_count_scoring > 0:
    percentage_unrecognized = (unrecognized_ngram_count / total_ngram_count_scoring) * 100
    logging.info(f"Total n-grams processed during scoring: {total_ngram_count_scoring}")
    logging.info(f"Unrecognized n-grams encountered (used default probability): {unrecognized_ngram_count} ({percentage_unrecognized:.2f}%)")
else:
    logging.info("No n-grams were processed during scoring.")


# --- Output ---
logging.info("Saving results to CSV...")
# (Output code is the same as the previous good version)
if estimates:
    df = pd.DataFrame.from_dict(estimates, orient="index", columns=["estimate"])
    df = df.sort_values(by="estimate", ascending=False)
    output_path = 'user_study/results/stimuli_scores.csv'
    df.to_csv(output_path, index_label="sentence")
    logging.info(f"Full results saved to {output_path}")

    top_100_path = 'user_study/results/stimuli_scores_top100.csv'
    df.head(100).to_csv(top_100_path, index_label="sentence")
    logging.info(f"Top 100 sentences saved to {top_100_path}")
else:
    logging.warning("No sentences were scored. Output CSV files will not be generated.")

logging.info("Script finished.")