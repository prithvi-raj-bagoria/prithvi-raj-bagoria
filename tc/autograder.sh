#!/bin/bash

index=0

for folder in ../submissions/*; do
    python3 autograder.py "$index"
    echo "Autograded $index"
    ((index++))
done

python3 autograder.py -1