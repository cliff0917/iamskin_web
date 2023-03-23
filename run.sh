#!/bin/bash

env=iamskin

tmux new -s web -d
tmux send-keys "conda activate $env" C-m
tmux send-keys 'python app.py' C-m