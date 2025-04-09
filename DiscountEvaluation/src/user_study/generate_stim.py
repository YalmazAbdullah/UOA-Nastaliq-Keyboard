import math
import util
from urduhack import preprocessing
from tqdm import tqdm
from collections import Counter
import pandas as pd
import logging
import os
import subprocess # To run KenLM command-line tools
import sys # To check KenLM availability

# --- Configuration ---

# KenLM Paths (IMPORTANT: Adjust these if KenLM tools are not in your system PATH)
KENLM_LMPLZ_PATH = 'lmplz'  # Path to lmplz executable
KENLM_BUILD_BINARY_PATH = 'build_binary' # Path to build_binary executable

# Data Paths
DATA_DIR = 'interim/transformed/sentences'
DAKSHINA_PATH = os.path.join(DATA_DIR, 'dakshina_dataset')
ROURPARL_PATH = os.path.join(DATA_DIR, 'roUrParl_dataset')
SUBSET_PATH = os.path.join(DATA_DIR, 'combined_subset')

# Output Paths
OUTPUT_DIR = 'kenlm_output'
TRAINING_TEXT_FILE = os.path.join(OUTPUT_DIR, 'urdu_training_corpus.txt')
ARPA_MODEL_FILE = os.path.join(OUTPUT_DIR, 'urdu_model.arpa')
BINARY_MODEL_FILE = os.path.join(OUTPUT_DIR, 'urdu_model.binary')
RESULTS_DIR = 'user_study/results' # Keep previous results dir separate if needed
SCORES_CSV_PATH = os.path.join(RESULTS_DIR, 'stimuli_scores_kenlm.csv')
TOP_100_CSV_PATH = os.path.join(RESULTS_DIR, 'stimuli_scores_kenlm_top100.csv')

# Model & Processing Parameters
N_GRAM_ORDER = 3
VOCAB_THRESHOLD = 2 # Words seen <= this many times become UNK
UNK_TOKEN = "<unk>" # KenLM often uses <unk> by default, match it
KENLM_MEMORY = "8G" # Memory for lmplz (e.g., "8G", "50%")
PRUNING_SETTINGS = "0 0 1" # Example: Prune only singleton trigrams (adjust as needed)

# Scoring Parameters
SENTENCE_MIN_LEN = 9 # Inclusive (tokens after cleaning)
SENTENCE_MAX_LEN = 11 # Inclusive (tokens after cleaning)

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Ensure Output Directories Exist ---
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# --- Helper Functions ---

def check_kenlm_tools():
    """Checks if KenLM command-line tools seem accessible."""
    logging.info("Checking for KenLM command-line tools...")
    try:
        subprocess.run([KENLM_LMPLZ_PATH, "-h"], capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
        logging.info(f"'{KENLM_LMPLZ_PATH}' found.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logging.error(f"KenLM tool '{KENLM_LMPLZ_PATH}' not found or failed. Error: {e}")
        logging.error("Please install KenLM and ensure 'lmplz' is in your PATH or update KENLM_LMPLZ_PATH in the script.")
        return False
    try:
        # build_binary doesn't have a simple help flag that exits cleanly, just try running it
         subprocess.run([KENLM_BUILD_BINARY_PATH], capture_output=True, text=True, check=False, encoding='utf-8', errors='ignore') # check=False
         logging.info(f"'{KENLM_BUILD_BINARY_PATH}' command exists.") # Check might be basic
    except FileNotFoundError as e:
        logging.error(f"KenLM tool '{KENLM_BUILD_BINARY_PATH}' not found. Error: {e}")
        logging.error("Please ensure 'build_binary' is in your PATH or update KENLM_BUILD_BINARY_PATH in the script.")
        return False
    return True

def prepare_and_build_vocab(data):
    """
    Preprocesses data, builds vocabulary based on frequency threshold.
    Returns list of lists of tokens (original structure) and vocabulary.
    """
    tokens_nested = []
    all_tokens_flat = []

    logging.info("Preprocessing and tokenizing for vocabulary...")
    for sentence in tqdm(data, desc="Preprocessing & Tokenizing"):
        cleaned = preprocessing.remove_punctuation(sentence)
        sentence_tokens = cleaned.split()
        if not sentence_tokens: continue
        tokens_nested.append(sentence_tokens)
        all_tokens_flat.extend(sentence_tokens)

    logging.info(f"Building unigram counts from {len(all_tokens_flat)} tokens...")
    counts = Counter(all_tokens_flat)

    logging.info(f"Building vocabulary with frequency threshold > {VOCAB_THRESHOLD}...")
    vocabulary = {word for word, count in counts.items() if count > VOCAB_THRESHOLD}
    # NOTE: We don't explicitly add UNK_TOKEN here, KenLM handles unknown words
    # internally mapping them to its <unk> token. We'll rely on that.
    logging.info(f"Vocabulary size (known words): {len(vocabulary)}")

    # Replace OOV in the nested list structure - IMPORTANT for training file consistency
    # KenLM can map OOV to <unk> itself, but pre-replacing ensures the counts
    # used by lmplz match exactly what we expect if we were doing it manually.
    logging.info(f"Replacing OOV words with '{UNK_TOKEN}' in sentence structures...")
    prepared_nested = []
    oov_count = 0
    total_tokens_count = 0
    for sentence_tokens in tqdm(tokens_nested, desc="Replacing OOV"):
        processed_sentence = []
        for token in sentence_tokens:
            total_tokens_count +=1
            if token in vocabulary:
                processed_sentence.append(token)
            else:
                processed_sentence.append(UNK_TOKEN)
                oov_count += 1
        prepared_nested.append(processed_sentence)

    if total_tokens_count > 0:
        logging.info(f"Replaced {oov_count} OOV tokens ({oov_count/total_tokens_count:.2%}).")
    else:
        logging.info("No tokens found to process for OOV replacement.")

    return prepared_nested, vocabulary # Return vocab for potential use during scoring if needed

def write_training_file(nested_token_list, filename):
    """Writes prepared sentences to a text file for KenLM, adding <s> and </s>."""
    logging.info(f"Writing prepared training data to {filename}...")
    count = 0
    with open(filename, 'w', encoding='utf-8') as f:
        for sentence_tokens in tqdm(nested_token_list, desc="Writing training file"):
             # KenLM typically expects sentences wrapped in <s> </s>
             # Ensure UNK_TOKEN is correctly written
            f.write(f"<s> {' '.join(sentence_tokens)} </s>\n")
            count += 1
    logging.info(f"Wrote {count} sentences to {filename}.")

def train_kenlm_model(order, memory, text_file, arpa_file, prune_settings):
    """Runs the KenLM lmplz command to train the model."""
    logging.info(f"Training KenLM {order}-gram model...")
    command = [
        KENLM_LMPLZ_PATH,
        '-o', str(order),
        '-S', memory,
        '--text', text_file,
        '--arpa', arpa_file,
        '--prune', *prune_settings.split() # Split prune settings string
        # Add other lmplz options if needed (e.g., --discount_fallback)
    ]
    logging.info(f"Running command: {' '.join(command)}")
    try:
        process = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        logging.info("KenLM training completed successfully.")
        logging.debug(f"lmplz stdout:\n{process.stdout}")
        logging.debug(f"lmplz stderr:\n{process.stderr}")
    except subprocess.CalledProcessError as e:
        logging.error(f"KenLM training failed with exit code {e.returncode}.")
        logging.error(f"Command: {' '.join(e.cmd)}")
        logging.error(f"stdout:\n{e.stdout}")
        logging.error(f"stderr:\n{e.stderr}")
        raise # Re-raise the exception to stop the script
    except FileNotFoundError:
        logging.error(f"Error: '{KENLM_LMPLZ_PATH}' command not found. Check installation and path.")
        raise

def build_kenlm_binary(arpa_file, binary_file):
    """Runs the KenLM build_binary command."""
    logging.info(f"Converting ARPA model {arpa_file} to binary format {binary_file}...")
    command = [
        KENLM_BUILD_BINARY_PATH,
        arpa_file,
        binary_file
    ]
    logging.info(f"Running command: {' '.join(command)}")
    try:
        process = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        logging.info("KenLM binary conversion completed successfully.")
        logging.debug(f"build_binary stdout:\n{process.stdout}")
        logging.debug(f"build_binary stderr:\n{process.stderr}")
    except subprocess.CalledProcessError as e:
        logging.error(f"KenLM binary conversion failed with exit code {e.returncode}.")
        logging.error(f"Command: {' '.join(e.cmd)}")
        logging.error(f"stdout:\n{e.stdout}")
        logging.error(f"stderr:\n{e.stderr}")
        raise
    except FileNotFoundError:
        logging.error(f"Error: '{KENLM_BUILD_BINARY_PATH}' command not found. Check installation and path.")
        raise

# --- Main Execution ---
if __name__ == "__main__":

    # --- Check Dependencies ---
    if not check_kenlm_tools():
        sys.exit(1) # Exit if tools are not found
    try:
        import kenlm
        logging.info(f"KenLM Python bindings version: {kenlm.__version__}")
    except ImportError:
        logging.error("KenLM Python bindings not found. Please install them, e.g.,")
        logging.error("pip install https://github.com/kpu/kenlm/archive/master.zip")
        sys.exit(1)
    try:
        import urduhack
        urduhack.download(verbose=False) # Attempt download quietly
    except ImportError:
         logging.error("UrduHack library not found. Please install it ('pip install urduhack').")
         sys.exit(1)
    except Exception as e:
         logging.warning(f"Could not automatically download UrduHack models (may already exist or offline): {e}")


    # --- Load Data ---
    logging.info("Reading datasets...")
    try:
        dakshina, _ = util.read_tsv(DAKSHINA_PATH)
        roUrParl, _ = util.read_tsv(ROURPARL_PATH)
        dataset, _ = util.read_tsv(SUBSET_PATH) # This is the test/scoring set
    except FileNotFoundError as e:
        logging.error(f"Error reading dataset file: {e}. Please ensure paths are correct.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred while reading datasets: {e}")
        sys.exit(1)

    # --- Prepare Training Data ---
    logging.info("Preparing training data...")
    training_set = set(roUrParl)
    training_set = training_set.union(set(dakshina))
    training_set = training_set.difference(set(dataset)) # Exclude test set sentences
    training_list = list(training_set)
    logging.info(f"Training set size: {len(training_list)} sentences")
    logging.info(f"Test dataset size: {len(dataset)} sentences")

    # Build vocab and replace OOV in training data structure
    prepared_nested_sentences, training_vocab = prepare_and_build_vocab(training_list)

    # Write training data to file for KenLM tools
    write_training_file(prepared_nested_sentences, TRAINING_TEXT_FILE)

    # --- Train KenLM Model ---
    try:
        train_kenlm_model(N_GRAM_ORDER, KENLM_MEMORY, TRAINING_TEXT_FILE, ARPA_MODEL_FILE, PRUNING_SETTINGS)
        build_kenlm_binary(ARPA_MODEL_FILE, BINARY_MODEL_FILE)
    except Exception as e:
        logging.error(f"Stopping script due to error during KenLM model building: {e}")
        sys.exit(1)


    # --- Load KenLM Model ---
    try:
        logging.info(f"Loading KenLM model from binary file: {BINARY_MODEL_FILE}...")
        model = kenlm.Model(BINARY_MODEL_FILE)
        logging.info(f"KenLM model loaded. Order: {model.order}")
    except Exception as e:
        logging.error(f"Failed to load KenLM model from {BINARY_MODEL_FILE}: {e}")
        logging.error("Ensure the binary model file was created successfully.")
        sys.exit(1)

    # --- Scoring ---
    logging.info("Scoring dataset sentences using KenLM...")
    estimates = {}
    scored_sentence_count = 0
    skipped_length_count = 0
    skipped_short_count = 0
    total_tokens_scored = 0
    error_scoring_count = 0

    for sentence in tqdm(dataset, desc="Scoring Sentences"):
        cleaned = preprocessing.remove_punctuation(sentence)
        tokens = cleaned.split()

        if not tokens: continue

        # Filter by length AFTER tokenization
        if len(tokens) < SENTENCE_MIN_LEN or len(tokens) > SENTENCE_MAX_LEN:
            skipped_length_count += 1
            continue

        # Prepare sentence string for KenLM (with <s>, </s> and OOV handling)
        # We pre-replaced with UNK_TOKEN during training file prep,
        # so we do the *same* here for consistency. KenLM should map UNK_TOKEN
        # to its internal <unk> state if UNK_TOKEN appeared in training data.
        tokens_with_unk = [token if token in training_vocab else UNK_TOKEN for token in tokens]
        sentence_for_scoring = f"<s> {' '.join(tokens_with_unk)} </s>"

        try:
             # Get log10 probability from KenLM. bos=False, eos=False as we added markers.
             log10_prob = model.score(sentence_for_scoring, bos=False, eos=False)

             # Convert to natural log (ln)
             log_prob = log10_prob / math.log10(math.e)

             # Normalize by number of tokens + 2 (for <s> and </s>)
             # This normalization helps compare sentences of slightly different lengths
             # within the allowed range.
             num_elements_for_norm = len(tokens_with_unk) + 2
             total_tokens_scored += (len(tokens_with_unk) + 2) # Count tokens including markers

             if num_elements_for_norm > 0:
                 avg_log_prob = log_prob / num_elements_for_norm
                 estimates[sentence] = avg_log_prob # Store original sentence as key
                 scored_sentence_count += 1
             # else: pass # Should not happen if len(tokens)>0

        except RuntimeError as e:
             logging.warning(f"KenLM Runtime Error scoring sentence: '{sentence}'. Error: {e}. Skipping.")
             error_scoring_count += 1
        except Exception as e:
             logging.warning(f"Unexpected error scoring sentence: '{sentence}'. Error: {e}. Skipping.")
             error_scoring_count += 1


    # --- Logging Summary ---
    logging.info(f"Finished scoring.")
    logging.info(f"Successfully scored {scored_sentence_count} sentences.")
    logging.info(f"Skipped {skipped_length_count} sentences due to length constraints (<{SENTENCE_MIN_LEN} or >{SENTENCE_MAX_LEN} tokens).")
    # logging.info(f"Skipped {skipped_short_count} sentences shorter than n={N_GRAM_ORDER} tokens (This check is implicitly handled by length filter).")
    logging.info(f"Encountered errors scoring {error_scoring_count} sentences.")
    # Perplexity is another common metric: PP = exp(-Sum(log_prob) / N_tokens)
    # total_log_prob_sum = sum(est * (len(preprocessing.remove_punctuation(s).split()) + 2) for s, est in estimates.items()) # Approximate total log prob
    # if total_tokens_scored > 0:
    #     avg_log_prob_overall = total_log_prob_sum / total_tokens_scored
    #     perplexity = math.exp(-avg_log_prob_overall)
    #     logging.info(f"Approximate Average Log Probability: {avg_log_prob_overall:.4f}")
    #     logging.info(f"Approximate Perplexity: {perplexity:.4f}")


    # --- Output ---
    logging.info("Saving scoring results to CSV...")
    if estimates:
        df = pd.DataFrame.from_dict(estimates, orient="index", columns=["avg_log_prob_kenlm"])
        df = df.sort_values(by="avg_log_prob_kenlm", ascending=False) # Higher score (closer to 0) is better/more common
        try:
            df.to_csv(SCORES_CSV_PATH, index_label="sentence", encoding='utf-8')
            logging.info(f"Full results saved to {SCORES_CSV_PATH}")

            df.head(100).to_csv(TOP_100_CSV_PATH, index_label="sentence", encoding='utf-8')
            logging.info(f"Top 100 sentences saved to {TOP_100_CSV_PATH}")
        except Exception as e:
            logging.error(f"Failed to save scores CSV: {e}")
    else:
        logging.warning("No sentences were successfully scored. Output score CSV files will not be generated.")

    logging.info("Script finished.")