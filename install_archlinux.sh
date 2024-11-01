#!/bin/bash

if (( $(id -u) == 0 )); then
    echo "please do not run install as root or with sudo/doas"
    exit
fi

shell=$(basename "$SHELL")

sudo pacman -S --noconfirm python python-beautifulsoup4 python-requests

str="alias wstatus='python $(pwd)/main.py'"

if grep -q "${str}" ~/.${shell}rc; then
    echo "wstatus alias already exists in ~/.${shell}rc"
    exit
fi

echo "# wstatus alias" >> ~/.${shell}rc
echo "${str}" >> ~/.${shell}rc
echo "Success! restart shell to start using"
