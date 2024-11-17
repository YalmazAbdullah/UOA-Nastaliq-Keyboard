# clean
python ./DiscountEvaluation/src_py/prepare.py > DiscountEvaluation/logs/prepare.txt
python ./DiscountEvaluation/src_py/clean.py > ./DiscountEvaluation/logs/clean.txt

# transform
python ./DiscountEvaluation/src_py/transform_sentence.py > ./DiscountEvaluation/logs/transform_sentence.txt
python ./DiscountEvaluation/src_py/transform_keystroke.py
python ./DiscountEvaluation/src_py/transform_dyad.py