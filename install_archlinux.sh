#!/bin/sh

if (( $(id -u) == 0 )); then
    echo "please do not run install as root or with sudo/doas"
    exit
fi

sudo pacman -S --noconfirm python python-beautifulsoup4 python-requests

str="alias wstatus='python $(pwd)/main.py'"

echo "# wstatus alias" >> ~/.bashrc
echo "${str}" >> ~/.bashrc
echo "Success! restart shell to start using"
