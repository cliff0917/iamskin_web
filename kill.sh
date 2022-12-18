#!/bin/bash

function kill(){
    tmux kill-session -t $1 2> /dev/null
}

kill "web"
kill "linebot"
kill "skin"
kill "nail"
kill "acne"