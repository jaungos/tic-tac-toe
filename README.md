# AI Agent for the Tic-Tac-Toe Game

## About
An application that implements the Min-Max algorithm to create an AI agent that never loses in a tic-tac-toe game against a human player. This AI Agent would never lose; it will always win or get a draw.

<div align = "center">

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
</div>

## Installing Dependencies 
* For Windows, it should be run in a cmd terminal
```bash
py -m venv env # create a new python virtual environment
env/Scripts/activate # Open a new cmd terminal in the same directory

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py # install pip
python get-pip.py

pip install tk
pip install numpy
```

* For linux, open a bash terminal and have sudo privileges
```bash
py -m venv env # create a new python virtual environment
env/Scripts/activate # Open a new terminal in the same directory

sudo apt install pip # install pip

pip install tk
pip install numpy
```

## Running
Open a terminal at the sourcecode folder and run the command: 
### Linux
```bash
python3 main.py
```
### Windows 
* It should be run in the cmd terminal
```bash
py main.py 
```