#!/bin/bash

# Default values for flags (off by default)
clean=false
transform=false
score=false

# Function to display usage
usage() {
    echo "Usage: $0 [-a] [-b] [-c]"
    echo "  -clean      Run cleaning for datasets"
    echo "  -transform  Run transformations for dataset"
    echo "  -score      Run score monad and diad"
    exit 1
}

# Parse options
while getopts "cts" opt; do
    case $opt in
        c)
            clean=true
            ;;
        t)
            transform=true
            ;;
        s)
            score=true
            ;;
        *)
            usage
            ;;
    esac
done

# Shift processed options away
shift $((OPTIND-1))

# If no flags were set, show usage
if ! $clean && ! $transform && ! $score; then
    echo "Error: No tasks specified."
    usage
fi

mkdir ./DiscountEvaluation/logs/$(date +'%Y%m%d_%H%M%S')
LOG_PATH="./DiscountEvaluation/logs/$(date +'%Y%m%d_%H%M%S')"

# Main logic
if $clean; then
    echo "Cleaning..."
    # clean
    python ./DiscountEvaluation/src_py/prepare.py > "$LOG_PATH/1_prepare.log"
    python ./DiscountEvaluation/src_py/clean.py > "$LOG_PATH/2_clean.log"
fi

if $transform; then
    echo "Transforming..."
    # transform
    python ./DiscountEvaluation/src_py/transform_sentence.py > "$LOG_PATH"
    python ./DiscountEvaluation/src_py/transform_keystroke.py
    python ./DiscountEvaluation/src_py/transform_dyad.py
fi

if $score; then
    echo "Scoring..."
    # score
    python ./DiscountEvaluation/src_py/score_monad.py
    python ./DiscountEvaluation/src_py/score_dyad.py
fi
