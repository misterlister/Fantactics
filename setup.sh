#! /bin/bash

if ! test -d .venv; then
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    echo "Virtual Environment created and dependencies installed!"
else
    echo "Already set up! Enter './startServer.sh' to start the server or './startGame.sh' to play."
fi
