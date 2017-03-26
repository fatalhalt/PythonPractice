#!/usr/bin/env python

def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

# code below will execute only if this .py file is ran directly instead of being imported
if __name__ == "__main__":
    import sys
    if (len(sys.argv) == 2):
        print('fibonacci of ' + str(int(sys.argv[1])) + ' is ' + str(fibonacci(int(sys.argv[1]))));
    else:
        print('usage: fibonacci.py <number>');
