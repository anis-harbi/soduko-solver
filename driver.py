from sys import argv
from copy import deepcopy
import time

R = "ABCDEFGHI"
C = "123456789"
# generates list for a cell based on its row, column and block
# organizes input data accordingly 
def Generate(row, column):
    for i in range(9):
        if row!=i:
            sudokuDict[R[row]+C[column]].append(str(R[i])+str(C[column]))
    for i in range(9):
        if column!=i:
            sudokuDict[R[row]+C[column]].append(str(R[row])+str(C[i]))

    if (row == 0 or row == 1 or row == 2) and (column==0 or column == 1 or column == 2):
        for r in range(0,3):
            for c in range(0,3):
                if (row!=r) and (column!=c):
                    sudokuDict[R[row]+C[column]].append(str(R[r])+str(C[c]))
    elif (row == 0 or row == 1 or row == 2) and (column==3 or column == 4 or column == 5):
        for r in range(0,3):
            for c in range(3,6):
                if (row!=r) and (column!=c):
                    sudokuDict[R[row]+C[column]].append(str(R[r])+str(C[c]))
    elif (row == 0 or row == 1 or row == 2) and (column==6 or column == 7 or column == 8):
        for r in range(0,3):
            for c in range(6,9):
                if (row!=r) and (column!=c):
                    sudokuDict[R[row]+C[column]].append(str(R[r])+str(C[c]))        
    elif (row == 3 or row == 4 or row == 5) and (column==0 or column == 1 or column == 2):
        for r in range(3,6):
            for c in range(0,3):
                if (row!=r) and (column!=c):
                    sudokuDict[R[row]+C[column]].append(str(R[r])+str(C[c]))
    elif (row == 3 or row == 4 or row == 5) and (column==3 or column == 4 or column == 5):
        for r in range(3,6):
            for c in range(3,6):
                if (row!=r) and (column!=c):
                    sudokuDict[R[row]+C[column]].append(str(R[r])+str(C[c]))
    elif (row == 3 or row == 4 or row == 5) and (column==6 or column == 7 or column == 8):
        for r in range(3,6):
            for c in range(6,9):
                if (row!=r) and (column!=c):
                    sudokuDict[R[row]+C[column]].append(str(R[r])+str(C[c]))
    elif (row == 6 or row == 7 or row == 8) and (column==0 or column == 1 or column == 2):
        for r in range(6,9):
            for c in range(0,3):
                if (row!=r) and (column!=c):
                    sudokuDict[R[row]+C[column]].append(str(R[r])+str(C[c]))
    elif (row == 6 or row == 7 or row == 8) and (column==3 or column == 4 or column == 5):
        for r in range(6,9):
            for c in range(3,6):
                if (row!=r) and (column!=c):
                    sudokuDict[R[row]+C[column]].append(str(R[r])+str(C[c]))
    elif (row == 6 or row == 7 or row == 8) and (column==6 or column == 7 or column == 8):
        for r in range(6,9):
            for c in range(6,9):
                if (row!=r) and (column!=c):
                    sudokuDict[R[row]+C[column]].append(str(R[r])+str(C[c]))

# if a sudoku board i given as argument
# this write solution to output.txt
# this can also be used with a file such as start_sudoku.txt
# and prints solution in output.txt line by line
target = open('output.txt', 'w+')
def sudokuToOutput(sudoku):
    for i in R:
        for j in C:
            sdk = str(sudoku[i + j][0])
            target.write(sdk)
    #target.write('\n')
        
# back tracking algorithm implementation 
# with minimum value heureustic and forward checking
def backTrackingAlgorithm(localsudokuDomain):
    minValHeureustic = 12
    isSolved = True
    for i in range(9):
        for j in range(9):
            if len(localsudokuDomain[R[i]+C[j]])==0:
                return 0
            if minValHeureustic>len(localsudokuDomain[R[i]+C[j]]) and len(localsudokuDomain[R[i]+C[j]])>1:
                minValHeureustic = len(localsudokuDomain[R[i]+C[j]])
                var = R[i]+C[j]
                isSolved = False
    if isSolved == True:
        result = 1
        sudokuToOutput(localsudokuDomain)
        return result
    for value in localsudokuDomain[var]:
        isSolved = True
        sudokuDictArray = []
        count2 = 0
        sudokuDictArray = sudokuDict[var]
        while isSolved == True and count2<len(sudokuDictArray):
            for element in localsudokuDomain[sudokuDictArray[count2]]:
                if value == element and len(localsudokuDomain[sudokuDictArray[count2]])==1:
                    isSolved = False
                    break
            count2 = count2+1
        if isSolved == True:
            booleanVal = True
        else:
            booleanVal = False
        if booleanVal:
            localsudokuDomain2 = deepcopy(localsudokuDomain)
            localsudokuDomain2[var]=[value]
            # AC-3
            queue1 = []
            queue2 = []
            for Xi in sudokuDict:
                t = sudokuDict[Xi]
                for Xj in t:
                    queue1.append(Xi)
                    queue2.append(Xj)
            while queue1 !=[]:
                Xi = queue1.pop(0)
                Xj = queue2.pop(0)
                removed = 0
                sp = 0
                for di in localsudokuDomain2[Xi]:
                    for dj in localsudokuDomain2[Xj]:
                        if (di == dj and len(localsudokuDomain2[Xj])==1):
                            localsudokuDomain2[Xi].pop(sp)
                            sp = sp-1
                            removed = 1
                            break
                    sp = sp+1
                if removed == 1:
                    t = sudokuDict[Xi]
                    for Xk in t:
                        queue1.append(Xk)
                        queue2.append(Xi)
            result = backTrackingAlgorithm(localsudokuDomain2)         
            if result == 1:
                return result         
    return 0

# reads sudoku boards from command line argument
# handls two cases
# a file containing sudoku boards or a string of 81 integers fed directly
# to argv[1]
sudokuSource = argv[1]
if "txt" in sudokuSource:
    f = open(sudokuSource)
    sudokuList = f.read()
else:
    sudokuList = sudokuSource
# try solving the board with AC-3 and counts those that were solved
counter = 1
ac3SolvedCount = 0
backTrackingSolvedCount = 0
for line in sudokuList.split("\n"):
    sudokuBoard = {R[i] + C[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}
    sudokuDomain = {R[i] + C[j]: [] for i in range(9) for j in range(9)}
    sudokuDict = {R[i] + C[j]: [] for i in range(9) for j in range(9)}
    for row in range(9):
        for column in range(9):
            if sudokuBoard[R[row]+C[column]] != 0:
                sudokuDomain[R[row]+C[column]].append(sudokuBoard[R[row]+C[column]])
                Generate(row, column)
            if sudokuBoard[R[row]+C[column]] == 0:
                for i in range(1,10):
                    sudokuDomain[R[row]+C[column]].append(i)
                Generate(row, column)
    queue1 = []
    queue2 = []
    for Xi in sudokuDict:
        t = sudokuDict[Xi]
        for Xj in t:
            queue1.append(Xi)
            queue2.append(Xj)
    while queue1 !=[]:
        Xi = queue1.pop(0)
        Xj = queue2.pop(0)
        removed = False
        sp = 0
        for di in sudokuDomain[Xi]:
            for dj in sudokuDomain[Xj]:
                if (di == dj and len(sudokuDomain[Xj])==1):
                    sudokuDomain[Xi].pop(sp)
                    sp = sp-1
                    removed = True
                    break
            sp = sp+1
        if removed:
            t = sudokuDict[Xi]
            for Xk in t:
                queue1.append(Xk)
                queue2.append(Xi)   
    isSolved = True
    for i in sudokuDomain:
        if len(sudokuDomain[i]) != 1:
            isSolved = False
            break
    if isSolved == True:
        ac3SolvedCount = ac3SolvedCount+1
        sudokuToOutput(sudokuDomain)
    # the case AC-3 not working
    # we run backtracking and forward search 
    # on each sudoko board 
    if isSolved ==False :
        localsudokuDomain = deepcopy(sudokuDomain)
        result = backTrackingAlgorithm(localsudokuDomain)
        if result == 1:
            backTrackingSolvedCount = backTrackingSolvedCount+1
    isSolved = True
    counter = counter + 1