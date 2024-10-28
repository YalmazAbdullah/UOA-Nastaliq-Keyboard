import prepare
import clean
import transform_sentence
import transform_keystroke
import transform_triad
import score

def main():
    # Prepare the Roman Urdu Parl dataset so that it matches Dakshina Format
    print("Step1: Preparing dataset by transforming into Dakshina Format")
    prepare.main(
        "./data/raw/uncompressed/Roman-Urdu-Parl/Urdu.txt",
        "./data/raw/uncompressed/Roman-Urdu-Parl/Roman-Urdu.txt"
    )
    print("==================================================================")
    # Clean both datasets
    print("Step2: Cleaning datasets")
    clean.main()
    print("==================================================================")
    print("Step2: Transform enteries from tokens into sentences")
    transform_sentence.main()
    print("==================================================================")
    print("Step3: Transform charachters in sentences to keystrokes")
    transform_keystroke.main()
    print("==================================================================")
    print("Step4: Generate triad combinations from keystrokes")
    transform_triad.main()
    print("==================================================================")
    print("Step5: Score resulting data")
    score.main()


if __name__ == "__main__":
    main()