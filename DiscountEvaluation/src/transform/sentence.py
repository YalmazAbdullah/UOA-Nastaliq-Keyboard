# STL
from tqdm import tqdm

# Custom
from util import eval
from util import read_tsv,write_tsv


def transform(native,roman):
    '''
    Our inital format of having seperated tokens helps to align the roman and urdu text while
    cleaning. Now that cleaning is complete we want to collapse the tokens back into sentences.
    This function does precisely that.

    Args:
        native (list): list that holds all tokens in native data
        roman (list): list that holds all tokens in roman data
    '''
    # output holders
    native_sentences = []
    roman_sentences = []

    # temporary holders
    n_current_sentence = []
    r_current_sentence = []

    # eval counters
    lost_count = 0
    token_count = 0

    # for each token
    for i in tqdm(range(len(native)), desc="Back to Sentences"):
        # if it is end of sentence
        if native[i] == "</s>":
            # and sentence is more than one token
            if token_count >1:
                # form sentece strings
                native_sentences.append(" ".join(n_current_sentence))
                roman_sentence = " ".join(r_current_sentence)
                roman_sentences.append(roman_sentence.lower())
            else:
                # otherwise drop sentence
                lost_count+=1

            # reset counter
            token_count = 0
            # clean temporary holders
            n_current_sentence = []
            r_current_sentence = []
        else:
            # for native there are sometimes multiple in single token
            if len(native[i].split())>2:
                print (str(i), native[i])
            # otherwise add token to sentence holder
            n_current_sentence.append(native[i])
            r_current_sentence.append(roman[i])
            # increment counter
            token_count+=1
    return native_sentences,roman_sentences,lost_count


def sentence_transform(dataset_name):
    '''
    Simply a wraper to help process multiple datasets easily. Collapses tokens back into sentences.

    Args:
        dataset_name (string): name of the dataset. Must be in cleaned/
    '''
    native,roman = read_tsv("interim/cleaned/"+dataset_name)
    native_sentences,roman_sentences,lost_count = transform(native,roman)
    eval(len(native),len(native)-lost_count)
    write_tsv(native_sentences,roman_sentences,"interim/transformed/sentences/"+dataset_name)


##################
##     MAIN     ##
##################
def main():
    # Dataset: Dakshina
    print("Dataset: Dakshina".center(100, "="))
    sentence_transform("dakshina_dataset")
    # Dataset: Roman Urdu Parl
    print("Dataset: Roman Urdu Parl".center(100, "="))
    sentence_transform("roUrParl_dataset")

if __name__ == "__main__":
    main()