import os
import subprocess
import tempfile
import shutil
import pandas as pd # For saving results to CSV
from tqdm import tqdm # For progress bars
import util

DATA_DIR = 'interim/transformed/sentences'
DAKSHINA_PATH = os.path.join(DATA_DIR, 'dakshina_dataset')
ROURPARL_PATH = os.path.join(DATA_DIR, 'roUrParl_dataset')
SUBSET_PATH = os.path.join(DATA_DIR, 'combined_subset') # Sentences to score
OUTPUT_CSV_PATH = "results/scored_sentences.csv" # Where to save the results

N_GRAM_ORDER = 3
KENLM_BUILD_BIN_RAW = "~/Temp/kenlm/build/bin"
KENLM_BUILD_BIN = os.path.expanduser(KENLM_BUILD_BIN_RAW)
KENLM_MEMORY = "2G"

def tokenize_urdu(sentence):
    return " ".join(sentence.split())

def find_kenlm_tool(tool_name, build_bin_path):
    """Finds KenLM tools, checking PATH first, then the specified build path."""
    tool_path = shutil.which(tool_name) # Check system PATH
    if tool_path:
        return tool_path
    # If not in PATH, check the specified build directory
    potential_path = os.path.join(build_bin_path, tool_name)
    if os.path.exists(potential_path) and os.access(potential_path, os.X_OK):
         return potential_path
    # If not found anywhere
    return None

def run_subprocess(command, step_name="Command"):
    """Runs a subprocess command, checks for errors, and prints output."""
    try:
        print(f"Running: {' '.join(command)}")
        process = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
        print(f"{step_name} completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during {step_name} (Return Code: {e.returncode}):")
        print("Command:", " ".join(e.cmd))
        print("stdout:", e.stdout)
        print("stderr:", e.stderr)
        return False
    except FileNotFoundError:
        print(f"Error: Command '{command[0]}' not found. Check KenLM installation and PATH settings.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during {step_name}: {e}")
        return False

if __name__ == "__main__":
    print("Loading data...")
    try:
        dakshina, _ = util.read_tsv(DAKSHINA_PATH)
        roUrParl, _ = util.read_tsv(ROURPARL_PATH)
        sentences_to_score, _ = util.read_tsv(SUBSET_PATH) # These are the sentences we want to score
    except FileNotFoundError as e:
        print(f"Error loading data file: {e}")
        print("Please ensure the TSV files exist at the specified paths.")
        exit(1)
    except Exception as e:
        print(f"An error occurred during data loading: {e}")
        exit(1)
    training_set = set(map(str, roUrParl)).union(set(map(str, dakshina)))
    scoring_set = set(map(str, sentences_to_score))
    training_set = training_set - scoring_set 

    print(f"Total unique sentences for training: {len(training_set)}")
    print(f"Total sentences to score: {len(sentences_to_score)}")

    temp_dir = None # Initialize to None
    try:
        temp_dir = tempfile.mkdtemp()
        print(f"Created temporary directory: {temp_dir}")

        training_data_path = os.path.join(temp_dir, "urdu_train.txt")
        arpa_model_path = os.path.join(temp_dir, f"urdu_{N_GRAM_ORDER}gram.arpa")
        binary_model_path = os.path.join(temp_dir, f"urdu_{N_GRAM_ORDER}gram.binary")

        lmplz_path = find_kenlm_tool("lmplz", KENLM_BUILD_BIN)
        build_binary_path = find_kenlm_tool("build_binary", KENLM_BUILD_BIN)

        if not lmplz_path:
            print(f"Error: Cannot find 'lmplz'. Ensure KenLM is installed correctly,")
            print(f"in your PATH, or KENLM_BUILD_BIN ('{KENLM_BUILD_BIN_RAW}') is set correctly.")
            raise RuntimeError("lmplz not found") # Raise error to trigger finally block

        if not build_binary_path:
            print(f"Error: Cannot find 'build_binary'. Ensure KenLM is installed correctly,")
            print(f"in your PATH, or KENLM_BUILD_BIN ('{KENLM_BUILD_BIN_RAW}') is set correctly.")
            raise RuntimeError("build_binary not found") # Raise error to trigger finally block

        print(f"Preparing training data file: {training_data_path}")
        with open(training_data_path, "w", encoding="utf-8") as f:
            for sentence in tqdm(training_set, desc="Writing training data"):
                if isinstance(sentence, str) and sentence.strip(): # Basic check for valid string
                    tokenized = tokenize_urdu(sentence)
                    f.write(tokenized + "\n")
        print("Training data preparation complete.")

        print(f"Training {N_GRAM_ORDER}-gram model using '{lmplz_path}'...")
        lmplz_command = [
            lmplz_path,
            "-o", str(N_GRAM_ORDER),
            "--discount_fallback",
            "-S", KENLM_MEMORY,
            "--text", training_data_path,
            "--arpa", arpa_model_path
        ]
        if not run_subprocess(lmplz_command, "KenLM Training (lmplz)"):
            raise RuntimeError("lmplz execution failed")

        print(f"Converting ARPA to binary format using '{build_binary_path}'...")
        build_binary_command = [
            build_binary_path,
            arpa_model_path,
            binary_model_path
        ]
        if not run_subprocess(build_binary_command, "Binary Conversion (build_binary)"):
             raise RuntimeError("build_binary execution failed")

        print(f"Loading binary model from: {binary_model_path}")
        try:
            import kenlm
        except ImportError:
            print("Error: The 'kenlm' Python package is not installed.")
            print("Please install it, e.g., using 'pip install kenlm'")
            raise RuntimeError("kenlm package not found")

        model = kenlm.Model(binary_model_path)
        print("KenLM model loaded successfully.")

        print(f"Scoring {len(sentences_to_score)} sentences...")
        results_data = []
        for sentence in tqdm(sentences_to_score, desc="Scoring sentences"):
            tokenized_sentence = tokenize_urdu(sentence)
            num_tokens = len(tokenized_sentence.split())

            if num_tokens < 8 or num_tokens > 11:
                continue 
            
            if any(char.isdigit() for char in sentence):
                continue

            # Handle cases where tokenization might result in an empty string
            if not tokenized_sentence:
                print(f"Warning: Skipping sentence that became empty after tokenization: '{sentence}'")
                continue
            else:
                log_score = model.score(tokenized_sentence, bos=True, eos=True)/num_tokens

            results_data.append({
                'sentence': sentence,
                'log10_score': log_score
            })

        print(f"Saving results to {OUTPUT_CSV_PATH}...")
        results_df = pd.DataFrame(results_data)
        results_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
        print("Results saved successfully.")

    except Exception as e:
        print(f"\nAn error occurred during the process: {e}")

    finally:
        if temp_dir and os.path.exists(temp_dir):
            print(f"Cleaning up temporary directory: {temp_dir}")
            try:
                shutil.rmtree(temp_dir)
                print("Cleanup successful.")
            except Exception as e:
                print(f"Warning: Could not completely clean up temporary directory {temp_dir}. Error: {e}")
        else:
            print("No temporary directory to clean up.")