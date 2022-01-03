#!/usr/bin/python3
import os
import sys
import shlex
import subprocess


HOME = os.getenv("HOME")


def runShell(args, out=sys.stdout):
    subprocess.run(args, stdout=out, stderr=out)


def processCommand(line):
    try:
        command = shlex.split(line)

        if len(command) == 0:
            return None

        if command[0] == 'pwd':
            print(os.getcwd())

        elif command[0] == 'cd':
            if len(command) == 1:
                os.chdir(HOME)
            else:
                os.chdir(command[1])
        elif command[0] == 'exit':
            sys.exit(0)

        else:
            if '>' in command:
                if command.count('>') == 1 and command[-2] == '>':
                    with open(command[-1], 'w') as f:
                        runShell(command[:-2], out=f)
                else:
                    print("An error has occurred", file=sys.stderr)
            else:
                runShell(command)

    except Exception:
        print("An error has occurred", file=sys.stderr)


def prompt():
    while True:
        line = input("mysh$ ")
        processCommand(line)


def batch_mode(path):
    with open(path, 'r') as f:
        for line in f:
            print(line.strip())
            processCommand(line)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        batch_mode(sys.argv[1])
    else:
        prompt()