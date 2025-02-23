#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.md
python3 read_display.py