#!/bin/bash

# A helper script to execute the Invoke's tasks from the CI server

if [[ ! -d ".venv" ]]; then
    python3 -m venv .venv
fi

source .venv/bin/activate && \
pip install wheel && \
pip install -r requirements.txt && \
invoke $@
