python ./src_py/prepare.py > ./logs/prepare.txt
python ./src_py/clean.py > ./logs/clean.txt
python ./src_py/transform_sentence.py > ./logs/transform_sentence.txt
python ./src_py/transform_keystroke.py
python ./src_py/transform_triad.py
python ./src_py/score.py