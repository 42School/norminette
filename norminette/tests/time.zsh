#!/bin/zsh
time zsh tests/loop.zsh
echo "ran on $(echo $(ls **/*.c | wc -l) "* 100" | bc) files"
