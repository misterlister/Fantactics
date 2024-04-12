#! /bin/bash

if ! test -d .venv; then
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    echo "Virtual Environment created and dependencies installed!"
fi

source .venv/bin/activate
python3 main.py