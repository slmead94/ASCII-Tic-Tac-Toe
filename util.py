"""
//*************************************//

Assignment 11
Tic Tac Toe Utility Module

Spencer M.
Started: Apr 8th, 2016, 10:30 am

//*************************************//
"""
import time


def is_int(num, ls):
    try:
        int(num)
        if int(num) in ls:
            return True
        else:
            return False
    except ValueError:
        return False


def is_yes(string):
    try:
        str(string)
        if string.upper() == "YES":
            return True
    except ValueError:
        print "That's not a yes or a no...\n"
        return False


def is_x_o(string):
    if string.upper() == "X" or string.upper() == "O":
        return True
    else:
        return False


def loading():
    print ".",
    time.sleep(0.33)
    print ".",
    time.sleep(0.33)
    print ".",
    time.sleep(0.33)
    print
