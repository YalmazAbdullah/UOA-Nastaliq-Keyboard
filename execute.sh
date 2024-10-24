python ./src/prepare.py > ./logs/prepare.txt
python ./src/clean.py > ./logs/clean.txt
python ./src/transform_sentence.py > ./logs/transform_sentence.txt
python ./src/transform_keystroke.py
python ./src/transform_triad.py
python ./src/score.py