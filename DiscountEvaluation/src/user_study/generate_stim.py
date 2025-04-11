import os
import subprocess
import shutil
import pandas as pd # For saving results to CSV
from tqdm import tqdm # For progress bars
import util
import kenlm
import json
import random

MODEL_PATH = "user_study/lm/urdu_3gram.binary"
DATA_PATH = "user_study/results/selected_sentences.json"
OUTPUT_CSV_PATH = "user_study/results/stimuli.csv" 

def tokenize_urdu(sentence):
    return " ".join(sentence.split())

# Shuffle and balance into 3 groups with similar average perplexities
def balance_sets(df, n_sets=3, max_attempts=1000, tolerance=1.0):
    best_split = None
    best_diff = float('inf')

    for _ in range(max_attempts):
        shuffled = df.sample(frac=1, random_state=random.randint(0, 9999)).reset_index(drop=True)
        sets = [shuffled.iloc[i::n_sets].reset_index(drop=True) for i in range(n_sets)]

        avg_perps = [s['perplexity'].mean() for s in sets]
        diff = max(avg_perps) - min(avg_perps)

        if diff < best_diff:
            best_diff = diff
            best_split = sets

        if diff <= tolerance:  # Close enough!
            break

    return best_split, best_diff

def main():
    print(f"Loading binary model from: {MODEL_PATH}")
    model = kenlm.Model(MODEL_PATH)
    print("KenLM model loaded successfully.")


    file = open(DATA_PATH)
    sentences_set = json.load(file)
    file.close()

    results_data = []
    for pos in ["start","middle","end"]:
        for sentence in tqdm(sentences_set[pos], desc="Scoring sentences"):
            tokenized_sentence = tokenize_urdu(sentence)
            num_tokens = len(tokenized_sentence.split())
            log_score = model.score(tokenized_sentence, bos=True, eos=True)/num_tokens
            perp = model.perplexity(tokenized_sentence)
            results_data.append({
                'sentence': sentence,
                'log10_score': log_score,
                'perplexity':perp,
                'position':pos
            })

    results_df = pd.DataFrame(results_data)

    balanced_sets, final_diff = balance_sets(results_df, n_sets=3, tolerance=1.0)

    # Assign new set numbers instead of overwriting original position
    final_df = pd.concat([
        df.assign(set_number=i) for i, df in enumerate(balanced_sets)
    ]).reset_index(drop=True)

    # Optional: sort by set number
    final_df = final_df.sort_values(by='set_number')

    print(f"Final average perplexity difference between sets: {final_diff:.2f}")

    # Save to CSV
    print(f"Saving results to {OUTPUT_CSV_PATH}...")
    final_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
    print("Results saved successfully.")

    avg_perps = final_df.groupby('set_number')['perplexity'].mean()
    
    # Show average perplexity of each set
    print("\n📊 Average Perplexity by Set:")
    for set_num, avg in avg_perps.items():
        print(f"  Set {set_num}: {avg:.2f}")

    max_perp = avg_perps.max()
    min_perp = avg_perps.min()
    mean_perp = avg_perps.mean()
    relative_diff = (max_perp - min_perp) / mean_perp * 100

    print(f"Perplexity range: {min_perp:.2f} - {max_perp:.2f}")
    print(f"Absolute difference: {max_perp - min_perp:.2f}")
    print(f"Relative difference: {relative_diff:.2f}%")

if __name__ == "__main__":
    main()