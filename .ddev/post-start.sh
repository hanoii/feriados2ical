#!/bin/bash

[ ! -d .venv ] && python3 -m venv .venv
[ -d .venv ] && python3 -m venv --upgrade .venv
source .venv/bin/activate
pip install -r requirements.txt
