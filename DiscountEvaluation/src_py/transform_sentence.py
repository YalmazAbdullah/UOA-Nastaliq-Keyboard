# Custom
from util import eval
from util import read_tsv,write_tsv

def transform(native,roman):
    native_sentences = []
    roman_sentences = []
    n_current_sentence = []
    r_current_sentence = []
    lost_count = 0
    token_count = 0

    for i in range(len(native)):
        if native[i] == "</s>":
            if token_count >1:
                native_sentences.append(" ".join(n_current_sentence))
                roman_sentences.append(" ".join(r_current_sentence))
            else:
                lost_count+=1
            n_current_sentence = []
            r_current_sentence = []
            token_count = 0
        else:
            n_current_sentence.append(native[i])
            r_current_sentence.append(roman[i])
            token_count+=1
    return native_sentences,roman_sentences,lost_count

def main():
    print("###############################################")
    print("===================TRANSFORM===================")
    print("###############################################")
    print()
    print("=============Dataset: Dakshina=============")
    native,roman = read_tsv("cleaned/dakshina_dataset")
    native_sentences,roman_sentences,lost_count = transform(native,roman)
    eval(len(native),len(native)-lost_count)
    write_tsv(native_sentences,roman_sentences,"transformed/sentences/dakshina_dataset")

    print("=============Dataset: Roman Urdu Parl=============")
    native,roman = read_tsv("cleaned/roUrParl_dataset")
    native_sentences,roman_sentences,lost_count = transform(native,roman)
    eval(len(native),len(native)-lost_count)
    write_tsv(native_sentences,roman_sentences,"transformed/sentences/roUrParl_dataset")

if __name__ == "__main__":
    main()