import pygame
import sys
from time import sleep
from generate import generateBoard
from draw import *

WIDTH=600
HEIGHT=800
white = (255,255,255)
black = (0,0,0)

board = [[0, 8, 4, 1, 0, 0, 0, 0, 0], 
            [3, 0, 0, 0, 0, 0, 0, 2, 0], 
            [7, 0, 0, 9, 0, 0, 0, 0, 0], 
            [0, 2, 0, 8, 0, 3, 0, 1, 6], 
            [0, 0, 0, 0, 0, 7, 9, 0, 3], 
            [6, 0, 0, 0, 0, 9, 5, 0, 0], 
            [0, 1, 0, 0, 6, 0, 0, 0, 5], 
            [2, 0, 0, 0, 0, 0, 0, 6, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 7]]
originalBoard = []
interactiveBoard = []
for row in board:
    originalBoard.append(row.copy())
    interactiveBoard.append(row.copy())

def loadNewBoard(newBoard):
    board.clear()
    originalBoard.clear()
    interactiveBoard.clear()
    for row in newBoard:
        board.append(row.copy())
        originalBoard.append(row.copy())
        interactiveBoard.append(row.copy())

def calcBox():
    mouse = pygame.mouse.get_pos()
    return ((mouse[1]-3)//((WIDTH-6)/9),(mouse[0]-3)//((WIDTH-6)/9))

#def printBoard():
#    print('\n'.join([''.join(['{:4}'.format(col) for col in row]) 
#            for row in board]))

def isSafe(row,col,num):
    for i in range(0,9):
        if i!=row and board[i][col]==num:
            return False
    for j in range(0,9):
        if j!=col and board[row][j]==num:
            return False
    startingRow = 3*(row//3)
    startingCol = 3*(col//3)
    for a in range(startingRow,startingRow+3):
        for b in range(startingCol,startingCol+3):
            if (a!=row or b!=col) and board[a][b]==num:
                return False
    return True
        
def getUnassigned(row,col):
    for a in range(row,9):
        for b in range(0,9):
            if board[a][b]==0:
                return (a,b)
    return (-1,-1)

def solve(gameDisplay,row,col,startTime,checkWork):
    if not checkWork:
        drawTimer(gameDisplay,startTime)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
    unassigned = getUnassigned(row,col)
    if unassigned[0]==-1:
        return True
    for i in range(1,10):
        if isSafe(unassigned[0],unassigned[1],i):
            if not checkWork:
                removeInvalid(gameDisplay,unassigned[0],unassigned[1])
                addValid(gameDisplay,unassigned[0],unassigned[1],i)
            board[unassigned[0]][unassigned[1]] = i
            if unassigned[0]==8 and unassigned[1]==8:
                return True
            elif unassigned[1]==8:
                if solve(gameDisplay, unassigned[0]+1,0, startTime, checkWork):
                    return True
            else:
                if solve(gameDisplay, unassigned[0],unassigned[1]+1, startTime, checkWork):
                    return True
    board[unassigned[0]][unassigned[1]] = 0
    if not checkWork:
        removeInvalid(gameDisplay,unassigned[0],unassigned[1])
    return False

def executeSolve(gameDisplay, startTime, checkWork):
    solve(gameDisplay,0,0,startTime,checkWork)

def resetBoard(gameDisplay):
    gameDisplay.fill(white)
    drawBoard(gameDisplay)
    for a in range(9):
        for b in range(9):
            board[a][b] = originalBoard[a][b]
            interactiveBoard[a][b] = originalBoard[a][b]
            if originalBoard[a][b]!=0:
                addValid(gameDisplay,a,b,originalBoard[a][b])
    pygame.display.update()

def handleUserInput(gameDisplay, row,col):
    box_width = (WIDTH-6)/9
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4 or event.key == pygame.K_5 or event.key == pygame.K_6 or event.key == pygame.K_7 or event.key == pygame.K_8 or event.key == pygame.K_9:
                    interactiveBoard[int(row)][int(col)] = event.key-48
                    removeInvalid(gameDisplay,row,col)
                    addValid(gameDisplay,row,col,event.key-48)
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    interactiveBoard[int(row)][int(col)] = 0
                    removeInvalid(gameDisplay,row,col)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drawInnerBox(gameDisplay,white,row,col,2)
                pygame.display.update()
                handleClick(gameDisplay)
                return
        drawInnerBox(gameDisplay,black,row,col,2)
        pygame.display.update()
        
def checkWork(gameDisplay):
    executeSolve(gameDisplay, 0, True)
    complete = True
    for a in range(9):
        for b in range(9):
            if originalBoard[a][b]==0 and interactiveBoard[a][b]!=0:
                if interactiveBoard[a][b] == board[a][b]:
                    drawInnerBox(gameDisplay,green,a,b,2)
                else:
                    complete = False
                    drawInnerBox(gameDisplay,dark_red,a,b,2)
            elif interactiveBoard[a][b]==0:
                complete = False
    if complete:
        drawComplete(gameDisplay)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for a in range(9):
                    for b in range(9):
                        drawInnerBox(gameDisplay,white,a,b,2)
                removeComplete(gameDisplay)
                handleClick(gameDisplay)
                return

def handleClick(gameDisplay):
    mouse = pygame.mouse.get_pos()
    if WIDTH/10 <= mouse[0] <= 3*WIDTH/10 and WIDTH+(HEIGHT-WIDTH)/6 <= mouse[1] <= WIDTH+(HEIGHT-WIDTH)/2: # solve
        resetBoard(gameDisplay)
        startTime = pygame.time.get_ticks()
        drawButtons(gameDisplay)
        drawTimer(gameDisplay,startTime)
        executeSolve(gameDisplay, startTime, False)
        drawTimer(gameDisplay,startTime)
    elif 4*WIDTH/10 <= mouse[0] <= 6*WIDTH/10 and WIDTH+(HEIGHT-WIDTH)/6 <= mouse[1] <= WIDTH+(HEIGHT-WIDTH)/2: # check
        checkWork(gameDisplay)
    elif 7*WIDTH/10 <= mouse[0] <= 9*WIDTH/10 and WIDTH+(HEIGHT-WIDTH)/6 <= mouse[1] <= WIDTH+(HEIGHT-WIDTH)/2: # new board
        newBoard = generateBoard()
        loadNewBoard(newBoard)
        resetBoard(gameDisplay)
    elif 7*WIDTH/10 <= mouse[0] <= 9*WIDTH/10 and WIDTH+4*(HEIGHT-WIDTH)/6 <= mouse[1] <= WIDTH+5*(HEIGHT-WIDTH)/6: # reset
        resetBoard(gameDisplay)
    elif 3 <= mouse[0] <= WIDTH-3 and 3 <= mouse[1] <= WIDTH-3:
        box = calcBox()
        if originalBoard[int(box[0])][int(box[1])]==0:
            handleUserInput(gameDisplay,box[0],box[1])

def playGame():
    pygame.init()
    gameDisplay = pygame.display.set_mode([WIDTH,HEIGHT])
    pygame.display.set_caption('Sodoku Solver')
    resetBoard(gameDisplay)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handleClick(gameDisplay)
        drawButtons(gameDisplay)
        pygame.display.update()
    pygame.quit()

playGame()
