#!/bin/bash

pyinstaller --onefile --paths=./.venv/lib/python3.11/site-packages heatmap-app.py
