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

import sys,os

if len(sys.argv)==2 :
    file_input=str(sys.argv[1])
else :
    print "This program takes a .ll or .c file in input,"
    print "it should be used like:"
    print "python redundant-conditionals.py example.ll"
    exit(1)

'''We check the input file'''
if file_input[-3:]==".ll":
    fname=file_input
    isll=True
elif file_input[-2:]==".c":
    command = "clang -c -emit-llvm -S "+file_input + " -o lol_1664.ll"
    os.system(command)
    fname = "lol_1664.ll"
    isll=False
else :
    print "The input must be a .ll or a .c file"
    exit(1)

'''Opening the file and getting the content'''
with open(fname) as f:
    content = f.readlines()
content = [x.strip("\n") for x in content]

'''Delete the .ll file created in the process if the input is a c file'''
if not(isll) :
    os.system("rm lol_1664.ll")

'''Finding identical if/then branches'''
nbOfIdenticalLines=0
actionsIfThen=[]
actionsIfElse=[]
nbLine=0
while nbLine < len(content) :
    #We look for the lines starting with "if.then"
    if content[nbLine][0:7] == "if.then":
        #we then store all the actions executed in this block of instructions
        nbLine+=1
        lineFirstActionThen=nbLine
        currentAction=[]
        #We stop as soon as we hit the last line of the block
        while content[nbLine+1]!="":
            currentAction+=[content[nbLine]]
            nbLine+=1
        actionsIfThen+=[currentAction]
        nbLine=nbLine+2
        #If after the instruction block "if.then" there is an "if.else" block
        #We also store the actions executed in this block
        if content[nbLine][0:7] == "if.else":
            nbLine += 1
            lineFirstActionElse = nbLine
            currentAction = []
            while content[nbLine+1] != "":
                currentAction += [content[nbLine]]
                nbLine += 1
            actionsIfElse += [currentAction]
            nbLine = nbLine+2
            #We check if we don't have the same actions if both blocks
            for indexThen, instruction in enumerate(actionsIfThen[-1]):
                #If it is the case we simply print the line
                if (instruction in actionsIfElse[-1]):
                    indexElse = actionsIfElse[-1].index(instruction)
                    errorLineThen = lineFirstActionThen + indexThen
                    errorLineElse = lineFirstActionElse + indexElse
                    print "The instruction"
                    print instruction
                    print "is in both the if line",errorLineThen,"and the else line",errorLineElse,"in the LLVM IR file\n"
                    nbOfIdenticalLines += 1
        else :
            actionsIfElse+=[]
    else:
        nbLine+=1

if nbOfIdenticalLines == 0 :
    print "There is no identical lines in the if/else structure"
else :
    print "There is a total of",nbOfIdenticalLines,"identical lines"

'''Debuggig functions'''

#To print the actions with if.then
def printActionsThen():
    for i in range(len(actionsIfThen)):
        for x in actionsIfThen[i]:
            print x
        print ""
    return

#To print the actions with if.else
def printActionsElse():
    for i in range(len(actionsIfElse)):
        for x in actionsIfElse[i]:
            print x
        print ""
    return

'''Useless code ... for now'''

"""
#Writting back into the file
txt='\n'.join(content)
txt+="\n"
f=open(fname,"w")
f.write(txt)
"""