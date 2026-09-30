#!/usr/bin/env bash
set -e
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/download_models.py
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
