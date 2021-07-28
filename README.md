
# Introduction

This project build a program enables people to use hand in front of a camera to control a computer's mouse with the help of OpenCV and mediapipe libs.

## How to control mouse

### Move

Use only index finger to move.

### Left Click

Use only index and middle fingers. Put the two fingers close, the middle should be higher than the index finger to left-click.

### Right Click

Use only index and middle fingers. Put the two fingers closer than left click, the middle should be lower than the index finger to left-click.

### Double Left Click

Use only index and middle fingers. Put the two fingers far to double-click. 

### Scroll Up

Use thumb and index fingers. Other fingers need to be closed.

### Scroll Down

Use thumb, index and middle fingers. Other fingers need to be closed.

# Installation

### Virtual Environment

At the location of this program folder, open a terminal and type in  
`virtualenv venv`

### Dependencies

In the opened terminal, type in  
`venv/Scripts/activate`  
After this command line, (venv) should appear at the begin of the prompt. Then type in  
`pip3 install -r requirments.txt`

## Run Program

In the opened terminal, type in  
`python3 main.py`
