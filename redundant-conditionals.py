# -*- coding: utf-8 -*-

########################################################
#   CS4239       NUS School of Computing        2017   #
#                     Assignment 2:                    #
#      Detecting redundant conditionals in C code      #
#                                                      #
#                 By:   Loïc PERACHE                   #
#                       perache@comp.nus.edu           #
#                       A0174362E                      #
########################################################

# This program should be used with a .ll file like this:
# python redundant-conditionals.py example.ll

import sys
import os

'''Defining the different variables'''
########################################################

# Number of identical line we have detected so far
nbOfIdenticalLines = 0
# The table of tuples of block of instructions executed in the different if.then branches and their point of entry
actionsIfThen = []
# Same thing for the if.else branches
actionsIfElse = []
# The line we are currently looking at
nbLine = 0
# Table with all the redundant conditionals we found so far
redundancyFound = []  # (str instruction, int line in if.then, int line in if.else)

'''Defining a few functions'''
########################################################

'''This function test if we have the same instruction in the 2 branches'''


# actionsThen is a table of the instruction executed in the then branch
# actionsElse is the same for the else branch
# and we have the lines of the start of each block
def testIdentical(actionsThen, actionsElse, lineFirstActionThen, lineFirstActionElse, entryThen, entryElse):
    for indexThen, instruction in enumerate(actionsThen):
        # If we have the same line we simply add it to our found lines
        if instruction in actionsElse and entryThen == entryElse:
            indexElse = actionsElse.index(instruction)
            errorLineThen = lineFirstActionThen + indexThen
            errorLineElse = lineFirstActionElse + indexElse
            global redundancyFound
            redundancyFound += [(instruction, errorLineThen, errorLineElse, entryThen, entryElse)]
            global nbOfIdenticalLines
            nbOfIdenticalLines += 1


'''This function rename the variables with the same name if it has the same assignment'''


def renameVariables(actionsThen, actionsElse):
    for indexThen, instruction in enumerate(actionsThen):
        # We first find the assignment instruction in the if.then block
        if "=" in instruction:
            [variable1, assignment1] = instruction.split(" = ")
            for indexElse, instruction2 in enumerate(actionsElse):
                # We look for an assignment in the if.else block
                if "=" in instruction2:
                    [variable2, assignment2] = instruction2.split(" = ")
                    # If we have the same assignment then we rename the variables
                    if assignment1 == assignment2:
                        variable1 = variable1.replace(" ", "")
                        variable2 = variable2.replace(" ", "")
                        for i in range(len(actionsElse)):
                            actionsElse[i] = actionsElse[i].replace(variable2, variable1)
    # We return the instruction blocks after the renaming process is done
    return actionsThen, actionsElse


'''Debugging functions'''
########################################################


# To print the actions with if.then
def printActionsThen():
    for i in range(len(actionsIfThen)):
        for action in actionsIfThen[i]:
            print(action)
        print("")
    return


# To print the actions with if.else
def printActionsElse():
    for i in range(len(actionsIfElse)):
        for action in actionsIfElse[i]:
            print(action)
        print("")
    return


'''Beginning of the program'''
########################################################

# Checking the number of arguments
if len(sys.argv) == 2:
    file_input = str(sys.argv[1])
else:
    print("This program takes a .ll or .c file in input,")
    print("it should be used like:")
    print("python redundant-conditionals.py example.ll")
    exit(1)

'''We check the input file'''
if file_input[-3:] == ".ll":
    fname = file_input
    isll = True
elif file_input[-2:] == ".c":
    if os.path.isfile(file_input):
        command = "clang -c -emit-llvm -S " + file_input + " -o lol_1664.ll"
        os.system(command)
        fname = "lol_1664.ll"
        isll = False
    else:
        print("Error: No such .c file")
        exit(1)
else:
    print("The input must be a .ll or a .c file")
    exit(1)

'''Opening the file and getting the content'''
try:
    with open(fname) as f:
        # We want to have the file line by line
        content = f.readlines()
# Handling the possible errors when opening a file
except IOError as e:
    print("Error: No such .ll file")
    exit(1)
except ValueError:
    print("Could not convert data to an integer.")
    exit(1)
except:
    print("Unexpected error:", sys.exc_info()[0])
    exit(1)
content = [x.strip("\n") for x in content]

'''Delete the .ll file created in the process if the input is a c file'''
if not isll:
    os.system("rm lol_1664.ll")

'''Finding all the if/then branches'''
while nbLine < len(content):
    # We look for the lines starting with "if.then"
    if content[nbLine][0:7] == "if.then":
        # We store the point of entry
        [useless, pointOfEntry] = content[nbLine].split(" = ")
        # We then store all the actions executed in this block of instructions
        nbLine += 1
        lineFirstActionThen = nbLine
        currentAction = []
        # We stop as soon as we hit the last line of the block
        while content[nbLine + 1] != "":
            currentAction += [content[nbLine]]
            nbLine += 1
        actionsIfThen += [[currentAction, pointOfEntry, lineFirstActionThen]]
        nbLine = nbLine + 2
        # If after the instruction block "if.then" there is an "if.else" block
        # We also store the actions executed in this block
    elif content[nbLine][0:7] == "if.else":
        # We store the point of entry
        [useless, pointOfEntry] = content[nbLine].split(" = ")
        nbLine += 1
        lineFirstActionElse = nbLine
        currentAction = []
        while content[nbLine + 1] != "":
            currentAction += [content[nbLine]]
            nbLine += 1
        actionsIfElse += [[currentAction, pointOfEntry, lineFirstActionElse]]
        nbLine = nbLine + 2
    else:
        nbLine += 1

'''Reordering the corresponding if.then and if.else branches'''
for indexThenBranch, thenBranch in enumerate(actionsIfThen):
    found = False
    for indexElseBranch, elseBranch in enumerate(actionsIfElse):
        if elseBranch != [] and thenBranch[1] == elseBranch[1]:
            if indexThenBranch >= len(actionsIfElse):
                actionsIfElse += [[]]
            buf = actionsIfElse[indexThenBranch]
            actionsIfElse[indexThenBranch] = elseBranch
            actionsIfElse[indexElseBranch] = buf
            found = True
    if not found:
        actionsIfElse.insert(indexThenBranch, [])

'''Detecting the identical branches'''
for i in range(len(actionsIfThen)):
    # If there is no if.else branch there can't be identical branches
    if actionsIfElse[i] != []:
        # Rename variable with the same value with the same name
        actionsIfThen[i][0], actionsIfElse[i][0] = renameVariables(actionsIfThen[i][0], actionsIfElse[i][0])
        # We check if we don't have the same actions if both blocks
        testIdentical(actionsIfThen[i][0], actionsIfElse[i][0], actionsIfThen[i][2], actionsIfElse[i][2], actionsIfThen[i][1], actionsIfElse[i][1])

'''Printing the results'''
if nbOfIdenticalLines == 0:
    print("There are no identical lines in the if/else structure")
elif nbOfIdenticalLines == 1:
    print("There is only one identical line")
    x = redundancyFound[0]
    print("Line {} & {} in {}: {}".format(x[1]+1, x[2]+1, x[3], x[0]))
else:
    print("There is a total of {} identical lines\n".format(nbOfIdenticalLines))
    for x in redundancyFound:
        print("Line {} & {} in {}: {}".format(x[1] + 1, x[2] + 1, x[3], x[0]))
exit(0)
