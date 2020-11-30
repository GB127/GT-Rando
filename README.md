# Goof Troop Randomizer : Version 1.0
Data structure & Project management by Niamek, 
Randomizer logic and code organization by Charles342


# How to use the script:
First, you must have python 3.8 installed on your computer.

Follow the instructions on this link.
https://realpython.com/installing-python/


Second, you need to have a Goof Troop USA ROM in the script folder and rename it to Vanilla.smc. (note the capital V).


Third, To run the program, you need to learn how to run a script from the command line (cmd). In the future we will make it more user friendly.

In short :
1. Open the terminal window in the Randomizer folder. Here is a link that might help you : https://www.groovypost.com/howto/open-command-window-terminal-window-specific-folder-windows-mac-linux/
2. Type the command. To see the options, use -h
    1. WINDOWS: python main.py -[FLAGS] --seed [SEED] --worldselect
        1. EXAMPLE : python main.py -h
        2. EXAMPLE : python main.py -eiwd
        3. EXAMPLE : python main.py -eiwd --seed 342
    2. MAC : python3 main.py  -[FLAGS] --seed [SEED] --worldselect
        1. EXAMPLE : python3 main.py -h
        2. EXAMPLE : python3 main.py -eiwd
        3. EXAMPLE : python3 main.py -eiwd --seed 342
3. Enjoy!

# Troubleshooting
###  No module named 'matplotlib'
* Try running: 
```
python -m pip install -U pip
python -m pip install -U matplotlib
```

###  No module named 'cv2'
* Try running: 
```
python -m pip install -U pip
pip install opencv-python
```

# Community and links
Github project : https://github.com/GB127/GT-Rando

Goof Troop's Discord server : https://discord.gg/4MJT3Y5tgk