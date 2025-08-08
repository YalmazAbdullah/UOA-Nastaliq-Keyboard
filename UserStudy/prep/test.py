import kenlm

MODEL_PATH = "lm/urdu_3gram.binary"
print(f"Loading binary model from: {MODEL_PATH}")
model = kenlm.Model(MODEL_PATH)
print("KenLM model loaded successfully.")

tokenized_sentence = " ".join("خود شہزادی سکینہ علیہ السلام کا فیصلہ کافی ہے۔".split())
num_tokens = len(tokenized_sentence.split())
log_score = model.score(tokenized_sentence, bos=True, eos=True)/num_tokens
log_score2 = model.score(tokenized_sentence)/num_tokens
perp = model.perplexity(tokenized_sentence)

result = {
    'token count': num_tokens,
    'log10_score': log_score,
    'log10_score2': log_score2,
    'perplexity':perp,
}

print(result)
print()