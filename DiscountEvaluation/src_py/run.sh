#!/bin/bash

# Default values for flags (off by default)
clean=false
transform=false
score=false

# Function to display usage
usage() {
    echo "Usage: $0 [-c] [-t] [-s]"
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

mkdir ../logs/$(date +'%Y%m%d_%H%M%S')
LOG_PATH="../logs/$(date +'%Y%m%d_%H%M%S')"

# Main logic
if $clean; then
    echo "Cleaning..."
    # clean
    python -m pre-process.prepare > "$LOG_PATH/1_prepare.log"
    python -m pre-process.clean > "$LOG_PATH/2_clean.log"
fi

if $transform; then
    echo "Transforming..."
    # transform
    python -m transform.sentence > "$LOG_PATH/3_sentence.log"
    python -m transform.subset
    python -m transform.keystroke
    python -m transform.dyad
fi

if $score; then
    echo "Scoring..."
    # score
    python -m score.monad
    python -m score.dyad
    python -m score.sentence
fi

echo "Analysis..."
python -m analysis.stats_corpus > "$LOG_PATH/4_stats.log"
# python -m analysis.distance