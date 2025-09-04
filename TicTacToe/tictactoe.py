import os 
from time import sleep

def startScreen(): #clear screen and define p1 and p2
    os.system('cls')
    sleep(2)
    print("(lobby music plays in the background)")
    sleep(2)
    print("\nwelcome to keagan's tic tac toe")
    sleep(2)
    print("\nplayer 1(X) will go first")
    sleep(2)
    print("\nplayer 2(O) will go second")
    sleep(2)
    print("\nplease wait...")
    sleep(5)

def checkTurn(): #return number for whose turn it is
    if turn%2==1:
        print("player 1(X)'s turn")
        return 1
    elif turn%2==0:
        print("player 2(O)'s turn")
        return 2

def board(r1,r2,r3): #printing game board
    print("\n    1    2    3")
    print(f"A {r1}")
    print(f"\nB {r2}")
    print(f"\nC {r3}\n\n")

def choice(): #OLD take input for grid position
    row="z"
    column=0
    while True:
        if row.lower()!="a" and row.lower()!="b" and row.lower()!="c":
            row=input("pick a row: A, B or C?   ")
        else:
            row=row.lower()
            break
    while True:
        if  column!="1" and column!="2" and column!="3":
            column=input("pick a column: 1, 2 or 3?   ")
        else:
            column=int(column)   
            break  

    #print and return the selected grid
    print("player {}'s selected grid is {}{}".format(currentPlayer,row.upper(),column))
    return [row,column]

def choiceNew(): #take input for grid position
    while True:
        userI=input("select a grid:   ")
        print(f"selected grid is {userI}")
        userInput=list(userI.lower())
        if len(userInput)==2:
            if userInput[0]=="a" or userInput[0]=="b" or userInput[0]=="c":
                if userInput[-1]=="1" or userInput[-1]=="2" or userInput[-1]=="3":
                    userInput[1]=int(userInput[1])
                    break
                else:
                    print(f'"{userI}" is not a valid grid\nplease input a valid grid(i.e. A1, B2, C3)')
            else:
                print(f'"{userI}" is not a valid grid\nplease input a valid grid(i.e. A1, B2, C3)')
        elif len(userInput)<2:
            print(f'"{userI}" is too short!')
        else: 
            print(f'"{userI}" is too long!')
    return userInput    

def outr1(grid): #determine which index to replace and the string to replace it with("X" or "O")
    if grid[0]=="a":
        if currentPlayer==1:
            new="X"
        elif currentPlayer==2:
            new="O"
        return [grid[1]-1,new]
    else:
        return 0

def outr2(grid):
    if grid[0]=="b":
        if currentPlayer==1:
            new="X"
        elif currentPlayer==2:
            new="O"
        return [grid[1]-1,new]
    else:
        return 0

def outr3(grid):
    if grid[0]=="c":
        if currentPlayer==1:
            new="X"
        elif currentPlayer==2:
            new="O"
        return [grid[1]-1,new]
    else:
        return 0

def updateRow1(r): #update row by replacing with "X" or "O" and preventing it from rerunning again
    global rerun 
    if r!=0:
        rIndex=r[0]
        rString=r[1]
        if row1[rIndex]==" ":
            row1[rIndex]=rString
            rerun=False
        else:
            print("\ngrid is taken\nchoose another grid\n")
    return row1

def updateRow2(r):
    global rerun 
    #r=[index to replace,replacement string]
    if r!=0:
        rIndex=r[0]
        rString=r[1]
        if row2[rIndex]==" ":
            row2[rIndex]=rString
            rerun=False
        else:
            print("\nchoose another grid\n")
    return row2

def updateRow3(r):
    global rerun
    #r=[index to replace,replacement string]
    if r!=0:
        rIndex=r[0]
        rString=r[1]
        if row3[rIndex]==" ":
            row3[rIndex]=rString
            rerun=False
        else:
            print("\nchoose another grid\n")
    return row3

def winCheck(): #check is there is a winner and return false or True and "X" or "O" depending on who winner is

    #horizontal
    if len(set(row1))==1 and set(row1)!={" "}:
        return [True,set(row1)]
    elif len(set(row2))==1 and set(row2)!={" "}:
        return [True,set(row2)]
    elif len(set(row3))==1 and set(row3)!={" "}:
        return [True,set(row3)]

    #vertical
    if row1[0]==row2[0] and row2[0]==row3[0] and row1[0]!=" ":
        return [True, set(row1[0])]
    elif row1[1]==row2[1] and row2[1]==row3[1] and row1[1]!=" ":
        return [True, set(row1[1])]
    elif row1[2]==row2[2] and row2[2]==row3[2] and row1[2]!=" ":
        return [True, set(row1[2])]

    #diagonal
    if row1[0]==row2[1] and row2[1]==row3[2] and row1[0]!=" ":
        return [True, set(row1[0])]
    elif row1[2]==row2[1] and row2[1]==row3[0] and row1[2]!=" ":
        return [True, set(row1[2])]
    
    #stalemate
    x=[i for i in row1 if i==" "]
    y=[i for i in row2 if i==" "]
    z=[i for i in row3 if i==" "]
    if x==[] and y==[] and z==[]:
        return [True,0]

    
    return [False]

def winner(): #print result of the match
    x=gameComplete[1]
    if x=={"X"}:
        print("the winner is player one!!")
    elif x=={"O"}:
        print("the winner is player two!!")
    elif x==0:
        print("no winners")
    

def main(): #main tic tac toe program
    global row1
    global row2
    global row3
    global gameComplete
    global turn
    global currentPlayer
    global rerun

    #define the lists that are each row
    row1=[" "," "," "]
    row2=[" "," "," "]
    row3=[" "," "," "]

    gameComplete=[False] 
    turn=1
    currentPlayer=0
    rerun=True

    while gameComplete[0]==False:
        os.system('cls')
        currentPlayer=checkTurn()
        board(row1,row2,row3)
        while rerun==True:
            chosenGrid=choiceNew()
            newr1=outr1(chosenGrid)
            newr2=outr2(chosenGrid)
            newr3=outr3(chosenGrid)
            updatedr1=updateRow1(newr1)
            updatedr2=updateRow2(newr2)
            updatedr3=updateRow3(newr3)
        row1=updatedr1
        row2=updatedr2
        row3=updatedr3
        rerun=True
        turn+=1
        gameComplete=winCheck()
    os.system('cls')
    winner()
    board(row1,row2,row3)
    print("\ngame over!\n\n")

def checkRestart(): #check if play wants to restart
    res=input("restart? Y or N   ").lower()
    while res!="y" and res!="n":
        print("please type either Y or N")
        res=input("proceed to game? Y or N   ")
    if res=="n":
        sleep(1)
        print("\ngoodbye!")
        sleep(5)
        return False
    elif res=="y":
        print("\nrestarting.")
        sleep(2)
        print(".")
        sleep(2)
        print(".")
        sleep(3)
        return True
        
restart=True
startScreen()
while restart:
    main()
    restart=checkRestart()