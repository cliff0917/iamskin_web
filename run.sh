#!/bin/bash

env=iamskin

function run() {
    tmux new -s $2 -d
    tmux send-keys "cd $1" C-m
    tmux send-keys "conda activate $env" C-m
    tmux send-keys 'python app.py' C-m
}

run "." "web"
run "utils/linebot" "linebot"
run "utils/skin-server" "skin"
run "utils/nail-server" "nail"
run "utils/acne-server" "acne"