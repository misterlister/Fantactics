#! /bin/bash

if ! test -d .venv; then
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    echo "Virtual Environment created and dependencies installed!"
else
    echo "   ---------   "
    echo "Already set up!" 
    echo "Start virtual environment with the command 'python3 .venv/bin/activate'"
    echo "If playing across different machines, one player must start the server with the command 'python3 server.py'"
    echo "Start the game with the command 'python3 main.py'"
    echo "   ---------   "
fi
