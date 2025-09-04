import random
from time import sleep
from os import system
from pyfiglet import figlet_format

#defining key attributes of cards
suitTuple=("diamonds","clubs","hearts","spades")
faceTuple=("ace","two","three","four","five","six","seven","eight","nine","ten","jack","queen","king")
cardValues={"ace":11,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,"jack":10,"queen":10,"king":10}


class card: #create a class for cards whereby the attributes are the suit and face/number of the card

    def __init__(self,face,suit):
        self.face=face
        self.suit=suit
        self.value=cardValues[face]

    def __str__(self):
        return self.face + " of " + self.suit

    def obtainValue(self):
        return cardValues[self.face]

class deck: #create a class of a whole deck of 52 cards

    def __init__(self):
        self.deckList=[]
        for suit in suitTuple:
            for face in faceTuple:
                self.deckList.append(card(face,suit))
    
    def shuffleDeck(self):
        random.shuffle(self.deckList)

    def dealOne(self):
        return self.deckList.pop()

def gameStart(): #prints intro text, takes name
    global playerName

    intro=["(lobby music plays in the background)","\nwelcome to keagan's blackjack(SG)","\nthe rules are as follows:"]
    rules=["\nat two cards, ace's value is 11; at 3 cards, its value is 10 or 1; at 4 or 5 cards, its value is 1","cards from 2 to 10 retain their face value and picture cards have a value of 10","you are dealt two cards but can keep drawing up to a maximum of 5 cards","you will go draw cards to your own hand until you are satisfied, and the dealer starts drawing afterwards","try to attain a total value as close to, but not over 21","if your total value falls below 16, you lose by default","at the end, beat the dealer's value to win","if your hand has the same value as the dealer's, there is a stand off and your bet is neither won nor lost"]
    specialRules=["\n\nspecial cases:","\nif your starting hand has a value of 21(i.e. A+10 or A+J), you have a 'ban-luck' and you win by default with 2 to 1 odds","if your starting hand has two aces, you have a 'ban-ban' and you win by default with 3 to 1 odds","if you only have 3 cards in you hand and they are all 7, you have a triple 7 and you win by defaut with 7 to 1 odds","if you draw to 5 cards and still have a total value below 21, you have a 'wu-long' and you win by default with 2 to 1 odds"]

    system('cls')
    for line in intro:
        sleep(1)
        print(line)
    
    for rule in rules:
        sleep(2)
        print(rule)

    for specialRule in specialRules:
        sleep(2)
        print(specialRule)
    sleep(2)
     
    playerName=input("\n\nif you understand the rules, please input your name: ")
    takeBalance()

def takeBalance(): #checks what balance the player wants for this game
    global balance

    while True:
        try:
            balance=int(input("\nhow much money would you like to start with?\namount: $"))
        except:
            print("that's not a valid number!")
        else:
            break

    sleep(1)
    print(f"\nunderstood, player {playerName} starting with an amount of ${balance}\nplease wait...")
    sleep(3)

def checkBetSize(): #check what bet size player wants for this hand
    global betSize

    print(f"\nyour current balance is ${balance}.")
    while True:
        try:
            betSize=int(input("\nhow much money would you like to bet this round?\nbet: $"))
        except:
            print("that's not a valid number!")
        else:
            if betSize>balance:
                print("you cannot bet more money than you have!")
                checkBetSize()
            else:
                break

    sleep(1)
    print(f"\nunderstood, player {playerName} betting an amount of ${betSize} this round\nplease wait...")
    sleep(4)
    system('cls')
    
def dealHands(): #creates deck, deal 2 cards each to player and dealer from back of deck(end of list)

     #set/reset each hand
    global playerHand
    global dealerHand
    playerHand=[]
    dealerHand=[]

    #resets and shuffles deck
    global myDeck
    myDeck=deck()
    myDeck.shuffleDeck()
    
    #add 2 cards to each hand
    playerHand.append(myDeck.dealOne())
    playerHand.append(myDeck.dealOne())
    dealerHand.append(myDeck.dealOne())
    dealerHand.append(myDeck.dealOne()) 
   
def printBoard(dealerTurn=False): #print the current board
    sleep(1)
    system('cls')
    print(f"value of dealer's hand: {dealerValue}")
    
    if dealerTurn==True:
        print(f"card 1: {dealerHand[0]}\n")
        print(f"card 2: {dealerHand[1]}\n")

        for i in range(2,5):
            try:
                print(f"card {i+1}: {dealerHand[i]}\n")
            except:
                pass

    
    result = figlet_format("\nblackjack!\n\n") 
    print(result)

    print(f"your current balance is ${balance}")
    print(f"value of {playerName}'s hand: {playerValue}\n")

    print(f"card 1: {playerHand[0]}\n")
    print(f"card 2: {playerHand[1]}\n")

    for i in range(2,5):
        try:
            print(f"card {i+1}: {playerHand[i]}\n")
        except:
            pass

def playerCheckAce(hand): #since ace value is fluid, check what user wants ace to be
    global playerValue
    aceMinus=0

    if len(hand)==2:
        return 0
    
    elif len(hand)==3:
        for card in range(0,3):
            if hand[card].face=="ace":
                while True:
                    try:
                        aceThree=int(input("you have an ace in your hand\nwould you like the ace to be 1 or 10? "))
                    except:
                        print("thats not a valid number!")
                    else:
                        if aceThree==1 or aceThree==10:
                            break
                        else:
                            print("thats not a valid number!")

                if aceThree==1:
                    aceMinus+=10

                elif aceThree==10:
                    aceMinus+=1
    
    elif len(hand)>3:
        playerValue=0
        for card in range(len(hand)-1):
            playerValue+=hand[card].obtainValue()
        for card in range(len(hand)):
            if hand[card].face=="ace":
                aceMinus+=10
        
    return aceMinus

def dealerCheckAce(hand,risk): #since ace value is fluid, check for ace depending on size of hand, higher risk value means more likely to choose ace=1
    global dealerValue
    aceMinus=0

    if len(hand)==2:
        return 0
    
    elif len(hand)==3:
        for card in range(0,3):
            if hand[card].face=="ace":
                if dealerValue>=21:
                    aceMinus+=10
                elif random.randint(1,100)<risk:
                    aceMinus+=10
                elif random.randint(1,100)>risk:
                    aceMinus+=1
    
    elif len(hand)>3:
        dealerValue=0
        for card in range(len(hand)-1):
            dealerValue+=hand[card].obtainValue()
        for card in range(len(hand)):
            if hand[card].face=="ace":
                aceMinus+=10
    
    return aceMinus

def getPlayerHand(): #output player initial hand and check for special win//return 2=double win, 3=triple win, "false"=keep going

    #define hand and obtain total value of hand
    global playerValue
    playerValue=0
    playerValue=playerHand[0].obtainValue()+playerHand[1].obtainValue()

    #check for ban luck and ban ban
    if playerValue==21:
        return 2
    elif playerValue==22:
        return 3
    else:
        return True

def getDealerHand(): #output dealer initial hand and check for special win//return 2=double win, 3=triple win, "false"=keep going

    #define hand and obtain total value of hand
    global dealerValue
    dealerValue=0
    dealerValue=dealerHand[0].obtainValue() + dealerHand[1].obtainValue()

    #check for ban luck and ban ban
    if dealerValue==21:
        return 2
    elif dealerValue==22:
        dealerValue=21
        return 3
    else:
        dealerValue="???"
        return True

def checkPlayerDraw(): #check if player wants to keep drawing
    global playerValue
    global playerHand

    while playerValue<21:
        printBoard()

        if len(playerHand)==3 and playerHand[0].obtainValue()==playerHand[1].obtainValue()==playerHand[2].obtainValue()==7:
            return 7
        if len(playerHand)<5:
            try:
                option=input("would you like to hit or stand? ")
            except:
                print("thats not a valid input")

            else:
                if option.lower()=="hit":
                    playerHand.append(myDeck.dealOne())
                    printBoard()
                    aceThree=playerCheckAce(playerHand)

                    playerValue-=aceThree
                    playerValue+=playerHand[-1].obtainValue()
                    printBoard()

                elif option.lower()=="stand":
                    print("dealer's turn")
                    return False
                
                else:
                    print("that's not a valid input")
                
        elif len(playerHand)==5:
            print("you have 5 cards!\n")
            return 5
    else:
        if len(playerHand)==5:
            print("you have 5 cards!\n")
            return 5
        print("you cannot draw any more cards!\n\ndealer's turn\n")
        return 4

def checkDealerDraw(risk): #uses logic to check if dealer keeps going
    global dealerValue
    global dealerHand

    dealerValue=dealerHand[0].obtainValue() + dealerHand[1].obtainValue()
    while True:
        printBoard(True)
        if len(dealerHand)==3 and dealerHand[0].obtainValue()==7 and dealerHand[1].obtainValue()==7 and dealerHand[2].obtainValue()==7:
            return 7
        elif len(dealerHand)==5:
            return 5
        elif dealerValue<16:
                dealerHand.append(myDeck.dealOne())
                aceThree=dealerCheckAce(dealerHand,risk)
                dealerValue-=aceThree
                dealerValue+=dealerHand[-1].obtainValue()
                printBoard(True)
        elif 16<=dealerValue<19:
            if random.randint(1,100)<risk:
                dealerHand.append(myDeck.dealOne())
                aceThree=dealerCheckAce(dealerHand,risk)
                dealerValue-=aceThree
                dealerValue+=dealerHand[-1].obtainValue()
                printBoard(True)
                if dealerValue>21:
                    print("dealer has bust\n")
                    return 4
                elif 16<=dealerValue<=21:
                    print("end of dealer's turn\n")
                    return False
                else:
                    continue
                
            elif random.randint(1,100)>risk:
                print("end of dealer's turn\n")
                return False
        elif 19<=dealerValue<=21:
            print("end of dealer's turn\n")
            return False
            
        elif dealerValue>21:
            print("dealer has bust\n")
            return 4

def checkWinner(player,dealer): #check who is the winner of this hand and bet size won/lost
    
    if player==2:#player ban luck
        if dealer==2:
            print(f"both {playerName} dealer and hit ban luck, it's a stand!")
            sleep(2)
            return 0
        elif dealer==3:#dealer hit ban ban
            print("dealer hit ban ban, you lose triple! :(")
            sleep(2)
            return -3            
        else: #dealer also ban luck
            print(f"{playerName} hit ban luck, you win double!!!")
            sleep(2)
            return 2
            
        
    elif player==3: #player ban ban
        if dealer==3:
            print(f"both {playerName} dealer and hit ban ban, it's a stand!")
            sleep(2)
            return 0
        else: #dealer also ban ban
            print(f"{playerName} hit ban ban, you win triple!!!")
            sleep(2)
            return 3
    
    elif dealer==2:#dealer ban luck
        print("dealer hit ban luck, you lose double! :(")
        sleep(2)
        return -2
    elif dealer==3: #dealer ban ban
        print("dealer hit ban ban, you lose triple! :(")
        sleep(2)
        return -3
    
    elif player==7: #dealer trip seven
        print(f"{playerName} hit triple seven, you win 7x!!!")
        sleep(2)
        return 7
    elif dealer==7: #dealer trip seven
        print("dealer hit triple seven, you lose 7x! :(")
        sleep(2)
        return -7
    
    elif player==5:#player wu long
        if playerValue<=21:
            print(f"{playerName} hit wu long, you win double!!!")
            sleep(2)
            return 2
        elif playerValue>21:
            print(f"{playerName} tried for wu long but bust, you lose double! :(")
            sleep(2)
            return -2
        
    elif dealer==5:#dealer wu long
        if dealerValue<=21:
            print("dealer hit wu long, you lose double! :(")
            sleep(2)
            return -2
        elif dealerValue>21:
            print("dealer tried for wu long but bust, you win double!!")
            sleep(2)
            return 2

    elif player==4:#player bust
        if dealer==4:
            print("you both bust, it's a stand off!")
            sleep(2)
            return 0
        else:
            print("you bust, you lose! :(")
            sleep(2)
            return -1
    elif dealer==4: #dealer bust
        print("the dealer busts! you win!!!")
        sleep(2)
        return 1
    
    elif player==False and dealer==False: #no special case or bust, check who has higher value
        if playerValue<16:
            print(f"{playerName}'s hand value is less than 16, you lose by default!")
            return -1
        elif playerValue>dealerValue:
            print(f"{playerName}'s cards are better than the dealer's, you win!!!")
            sleep(2)
            return 1
        elif dealerValue>playerValue:
            print("dealer's cards are better than yours, you lose! :(")
            sleep(2)
            return -1
        elif playerValue==dealerValue:
            print("you have the same value, it's a stand off!")
            sleep(2)
            return 0
    
def checkRestart(): #check if player wants to try again, output True or False

    print("oh no! you have lost all your money!\n")
    while True:
        try:
            restart=input("would you like to start over? Y or N ")
        except:
            print("please type Y or N")
        else:
            if restart.lower()=="y":
                return True
            elif restart.lower()=="n":
                return False
            else:
                print("please type Y or N")

def sub(): #main game program
    global balance
    dealerRisk=random.randint(30,80)
    #checks how risky the dealer plays for this game, with smaller number being less risk and higher being more risk

    dealHands()
    checkBetSize()
    playerContinue=getPlayerHand()
    dealerContinue=getDealerHand()
    printBoard()

    if playerContinue==dealerContinue==True:
        while playerContinue==True:
            playerContinue=checkPlayerDraw()
        sleep(2)

        if playerContinue==False or playerContinue==4:
            if dealerContinue==True:
                dealerContinue=checkDealerDraw(dealerRisk)
    
    balanceChange=checkWinner(playerContinue,dealerContinue)
    balance+=(balanceChange)*betSize

    if balance>0:
        sleep(5)
        sub()

def main(): #check if game still goes on based on balance, if player wants restart

    sub()
    
    restart=checkRestart()
    if restart:
        takeBalance()
        main()

def gameEnd(): #end game screen

    system('cls')
    sleep(2)
    print(f"you have come to the end of the game!\nthank you for playing, {playerName}")
    result = figlet_format("\nblackjack!") 
    print(result)
    sleep(5)



#########################################################################

gameStart()
main()
gameEnd()
