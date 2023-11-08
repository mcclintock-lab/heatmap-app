#!/bin/bash

pyinstaller --path=./.venv/lib/python3.11/site-packages --windowed --icon=heatmap-icon.ico heatmap-app.py
