# py-scrabble

py-scrabble is an implementation of Scrabble for Windows that runs in the command line. 

## Preview

![Preview](https://media.giphy.com/media/PvjLbMySMx1sjOVU4G/giphy.gif)

## Installation
To install py-scrabble, make sure you have the latest version of [Python 3](https://www.python.org/) and [pip](https://pypi.org/project/pip/). Simply clone the repository to your local computer and install the project dependencies with 
```
pip install -r requirements.txt
```
and run the program (from the root directory) with 
```
python scrabble/main.py
```

## Tests
This project features pytests as part of its test driven development. The recommended way to run all the tests is to `cd` into the project's root directory and run the tests with
```
pytest --verbose --capture=no
```
The tests should all pass, like this: ![this](https://i.imgur.com/8DPzLcd.png)
