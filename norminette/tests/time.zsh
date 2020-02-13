#!/bin/zsh
time zsh loop.zsh
echo "ran on $(echo $(ls **/*.c | wc -l) "* 100" | bc) files"
