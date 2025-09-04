import math,random,pickle,csv
from time import sleep
from os import system
from pyfiglet import figlet_format

EXPcaps={1:40,2:70,3:110,4:150}
resourceLevel={1:60,2:70,3:95,4:120,5:150}
statLevel={1:15,2:25,3:40,4:55,5:75}
kuya=0

class skill:
    def __init__(self,name,ele,power,cost,description):
        self.name=name
        self.ele=ele
        self.power=power
        self.cost=cost
        self.description=description

    def __str__(self):
        return self.name 
    
    def use(self):
        return [self.ele,self.power,self.cost]
    
    def display(self):
        return f"({self.ele}) {self.name}: {self.description}\nPower: {abs(self.power)}\tCost: {self.cost}\n"

punch=skill("Punch","PHYSICAL",5,0,"Punch the enemy, inflicting light damage without consuming any mana.")

class avatar:

    def __init__(self):
        self.progress=0

        self.earthLvl=0
        self.earthEXP=0
        self.currentHP=50
        self.maxHP=50

        self.fireLvl=0
        self.fireEXP=0
        self.strength=10

        self.airLvl=0
        self.airEXP=0
        self.evasiveness=10

        self.waterLvl=0
        self.waterEXP=0
        self.currentMana=50
        self.maxMana=50

        self.numEquipped=3
        self.equippedSkills=[punch]
        self.unlockedSkills=[]

    def displayStats(self):
        print("Current levels:\n")
        if self.earthLvl==5:print(f"Earth: Lv5\nEXP: Max\nHealth: {self.maxHP}\n")
        else:print(f"Earth: Lv{self.earthLvl}\n{self.earthEXP}/{EXPcaps[self.earthLvl]}\nHealth: {self.maxHP}\n")
        if self.fireLvl==5:print(f"Fire: Lv5\nEXP: Max\nStrength: {self.strength}\n")
        else:print(f"Fire: Lv{self.fireLvl}\n{self.fireEXP}/{EXPcaps[self.fireLvl]}\nStrength: {self.strength}\n")
        if self.airLvl==5:print(f"Air: Lv5\nEXP: Max\nEvasiveness: {self.evasiveness}\n")
        else:print(f"Air: Lv{self.airLvl}\n{self.airEXP}/{EXPcaps[self.airLvl]}\nEvasiveness: {self.evasiveness}\n")
        if self.waterLvl==5:print(f"Water: Lv5\nEXP: Max\nMana: {self.maxMana}\n\n")
        else:print(f"Water: Lv{self.waterLvl}\n{self.waterEXP}/{EXPcaps[self.waterLvl]}\nMana: {self.maxMana}\n\n")
        print("Equipped skills:\n")
        for num in range(len(self.equippedSkills)):
            print(f"{num+1}. {self.equippedSkills[num].display()}")

    def resetStats(self):
        self.earthLvl=1
        self.maxHP=resourceLevel[1]
        self.currentHP=self.maxHP

        self.fireLvl=1
        self.strength=statLevel[1]

        self.airLvl=1
        self.evasiveness=statLevel[1]

        self.waterLvl=1
        self.maxMana=resourceLevel[1]
        self.currentMana=self.maxMana

    def clearSkillPool(self):
        self.unlockedSkills=[]
        self.equippedSkills=[punch]

    def setNumEquipped(self,num):
        self.numEquipped=num

    def addSkillPool(self,*skills):
        for skill in skills:
            self.unlockedSkills.append(skill)

    def setSkills(self,*skills):
        self.equippedSkills=[punch]
        for skill in skills:
            self.equippedSkills.append(skill)

    def pickSkills(self):
        self.equippedSkills=[punch]

        while len(self.equippedSkills)<self.numEquipped:
            system("cls")
            print(f"Total number of skills you can equip: {self.numEquipped}")
            print("Currently equipped skills:")
            for number in range(len(self.equippedSkills)):
                print(f"{number+1}. {self.equippedSkills[number]}")
            print("\n")
            for num in range(len(self.unlockedSkills)):
                currSkill=self.unlockedSkills[num]
                print(f"{num+1}. {currSkill.display()}")
                
            while True:
                try:
                    skillNum=int(input("Pick a skill to equip: "))
                except:
                    print("Choose a valid number!\n")
                    sleep(2)
                else:
                    if skillNum<=len(self.unlockedSkills):
                        if self.unlockedSkills[skillNum-1] in self.equippedSkills:
                            print("Choose a valid number!\n")
                        else:
                            self.equippedSkills.append(self.unlockedSkills[skillNum-1])
                            break
                    else:
                        print("Choose a valid number!\n")
                        sleep(2)
        system("cls")
        sleep(3)

    def useMove(self):
        print("Available skills:")
        for num in range(len(self.equippedSkills)):
            print(f"{num+1}. {self.equippedSkills[num]}")
        
        while True:
            try:
                usedSkill=int(input("\nPick a skill to use: "))
            except:
                print("Please pick a skill number!\n")
            else:
                if usedSkill<=len(self.equippedSkills):
                    usedSkillStats=self.equippedSkills[usedSkill-1].use()
                    if usedSkillStats[2]<=self.currentMana:
                        manaUsage=usedSkillStats[-1]
                        self.currentMana-=manaUsage
                        if usedSkillStats[1]>0:
                            usedSkillStats[1]=round(usedSkillStats[1]*self.strength/10)
                            print(f"You used {self.equippedSkills[usedSkill-1]}.")
                            sleep(2)
                            return usedSkillStats
                        elif usedSkillStats[1]<0:
                            usedSkillStats[1]=round(usedSkillStats[1]*1.1*self.strength/10)
                            print(f"You used {self.equippedSkills[usedSkill-1]}.")
                            sleep(2)
                            return usedSkillStats
                    else:
                        print("You don't have enough mana for that!\n")
                        sleep(2)
                else:
                    print("Please pick a skill number!\n")
                    sleep(2)

    def avgLvl(self):
        return int((self.earthLvl+self.fireLvl+self.airLvl+self.waterLvl)/4)

    def addEXP(self,manaUseList):
        sleep(2)
        for move in manaUseList:
            if move[0]=="EARTH" and self.earthLvl<5:
                self.earthEXP+=move[2]
            elif move[0]=="FIRE" and self.fireLvl<5:
                self.fireEXP+=move[2]
            elif move[0]=="AIR" and self.airLvl<5:
                self.airEXP+=move[2]
            elif move[0]=="WATER" and self.waterLvl<5:
                self.waterEXP+=move[2]

        if self.earthLvl<5:
            if self.earthEXP>=EXPcaps[self.earthLvl]:
                self.earthEXP=self.earthEXP%EXPcaps[self.earthLvl]
                self.earthLvl+=1
                self.maxHP=resourceLevel[self.earthLvl]
                self.currentHP=self.maxHP
                if self.earthLvl==5:
                    rockArmor=skill("Rock Armor","EARTH",-999,100,"Form a suit of armor out of rocks to completely nullify one attack.")
                    self.earthEXP=0
                    self.numEquipped+=1
                    self.unlockedSkills.append(rockArmor)
                    print("Earth ultimate skill added to skill pool, number of skills that can be equipped increased by 1.")
        
        if self.fireLvl<5:
            if self.fireEXP>=EXPcaps[self.fireLvl]:
                self.fireEXP=self.fireEXP%EXPcaps[self.fireLvl]
                self.fireLvl+=1
                self.power=resourceLevel[self.fireLvl]
                if self.fireLvl==5:
                    infernoVortex=skill("Inferno Vortex","FIRE",120,85,"Trap your enemy in a vortex of flames, dealing lethal damage to them.")
                    self.fireEXP=0
                    self.numEquipped+=1
                    self.unlockedSkills.append(infernoVortex)
                    print("Fire ultimate skill added to skill pool, number of skills that can be equipped increased by 1.")
        
        if self.airLvl<5:
            if self.airEXP>=EXPcaps[self.airLvl]:
                self.airEXP=self.airEXP%EXPcaps[self.airLvl]
                self.airLvl+=1
                self.evasiveness=resourceLevel[self.airLvl]
                if self.airLvl==5:
                    suffocate=skill("Asphyxiate","AIR",999,150,"Spend a large amount of mana to airbend out of your enemy's lungs, instantly killing them.")
                    self.airEXP=0
                    self.numEquipped+=1
                    self.unlockedSkills.append(suffocate)
                    print("Air ultimate skill added to skill pool, number of skills that can be equipped increased by 1.")
        
        if self.waterLvl<5:
            if self.waterEXP>=EXPcaps[self.waterLvl]:
                self.waterEXP=self.waterEXP%EXPcaps[self.waterLvl]
                self.waterLvl+=1
                self.maxMana=resourceLevel[self.waterLvl]
                self.currentMana=self.maxMana
                if self.waterLvl==5:
                    iceBarrier=skill("Ice Barrier","WATER",-120,60,"Form a huge ice barrier that's brittle yet strong, negating a large amount of damage to yourself.")
                    self.waterEXP=0
                    self.numEquipped+=1
                    self.unlockedSkills.append(iceBarrier)
                    print("Water ultimate skill added to skill pool, number of skills that can be equipped increased by 1.")
        
        sleep(2)
        print("EXP gained!\n")
        if self.earthLvl==5:print("Earth: Lv5\nEXP: Max\n")
        else:print(f"Earth: Lv{self.earthLvl}\n{self.earthEXP}/{EXPcaps[self.earthLvl]}\n")
        if self.fireLvl==5:print("Fire: Lv5\nEXP: Max\n")
        else:print(f"Fire: Lv{self.fireLvl}\n{self.fireEXP}/{EXPcaps[self.fireLvl]}\n")
        if self.airLvl==5:print("Air: Lv5\nEXP: Max\n")
        else:print(f"Air: Lv{self.airLvl}\n{self.airEXP}/{EXPcaps[self.airLvl]}\n")
        if self.waterLvl==5:print("Water: Lv5\nEXP: Max\n")
        else:print(f"Water: Lv{self.waterLvl}\n{self.waterEXP}/{EXPcaps[self.waterLvl]}\n")
        sleep(2)

    def heal(self):
        self.currentHP=self.maxHP
        self.currentMana=self.maxMana
        sleep(2)
        print(f"You are rejuvenated!\nYour HP is now at {self.currentHP}/{self.maxHP}.\nYour mana is now at {self.currentMana}/{self.maxMana}.")
        sleep(2)
    
    def setProgress(self,num):
        self.progress=num

class grunt:

    def __init__(self,name,level,offSkill,defSkill):
        self.name=name
        self.offSkill=offSkill
        self.defSkill=defSkill
        self.strength=statLevel[level]-5
        self.maxHP=resourceLevel[level]-5
        self.currentHP=self.maxHP

    def useMove(self):
        moveNum=random.randint(1,10)
        if moveNum<=8:
            sleep(1)
            print(f"{self.name} used {self.offSkill}")
            sleep(1)
            return round(self.offSkill.use()[1]*self.strength/10)
        elif moveNum>8:
            sleep(1)
            print(f"{self.name} used {self.defSkill}")
            sleep(1)
            return round(self.defSkill.use()[1]*1.1*self.strength/10)
        
class master:

    def __init__(self,name,level,*skills):
        self.name=name
        self.strength=statLevel[level]
        self.maxHP=resourceLevel[level]
        self.currentHP=self.maxHP
        self.skillList=[]
        for skill in skills:
            self.skillList.append(skill)
    
    def useMove(self):
        moveNum=random.randint(0,len(self.skillList)-1)
        sleep(1)
        print(f"{self.name} used {self.skillList[moveNum]}.")
        sleep(1)
        return round(self.skillList[moveNum].use()[1]*1.2*self.strength/10)


def printScreen(enemy,name="Avatar Kuya"):
    system("cls")
    if enemy.currentHP<0: enemyHP=0
    else: enemyHP=enemy.currentHP
    if kuya.currentHP<0: kuyaHP=0
    else: kuyaHP=kuya.currentHP
    print(f"{enemy.name}\nHealth: {enemyHP}/{enemy.maxHP}\n\n")
    print(figlet_format("AVATAR\n"))
    print(f"{name}\nHealth: {kuyaHP}/{kuya.maxHP}\nMana: {kuya.currentMana}/{kuya.maxMana}\n")
    sleep(2)

def saveProgress():
    sleep(2)
    print("Saving progress now...")
    sleep(1)
    with open("avatar.pickle","wb") as outfile:
        pickle.dump(kuya,outfile,protocol=pickle.HIGHEST_PROTOCOL)
    print("Progress has been saved!")
    sleep(2)

def checkLoad():
    global kuya
    saveStatus=False
    system("cls")
    sleep(2)
    print("(Lobby music plays in the background...)")
    sleep(2)
    print("Welcome to Keagan's Text-based RPG set in the world of Avatar: The Last Airbender")
    sleep(2)
    print(figlet_format("\nAVATAR"))
    sleep(2)
    print("\tThe Redemption of Kuya\n")
    sleep(2)

    try:
        with open("avatar.pickle","rb") as infile:
            kuya=pickle.load(infile)
    except:
        pass
    else:
        if isinstance(kuya,avatar):
            saveStatus=True

    sleep(2)
    startNew=0
    
    if saveStatus==False:
        print("No valid save file detected, starting new game now...")
        kuya=avatar()
        print("... (Hit ENTER to continue any time you see '...')")
        input()
    else:
        print("It seems you already have a save file!")
        while True:
            try:
                startNew=int(input("Would you like to continue from your last save or start a new save?\n1. Continue\n2. Start new game\n"))
            except:
                print("Please input a valid number!")
            else:
                if startNew==1 or startNew==2:
                    break
                else:
                    print("Please input a valid number!")
    
    sleep(2)

    if startNew==1:
        print("\nContinuing from last save...")
        sleep(2)
    elif startNew==2:
        while True:
            try:
                confirmWipe=int(input("\nYou are about to start a new save that will overwrite any previous save file when you do save your game. Proceed?\n1. Yes\n2. No\n"))
            except:
                print("Please input a valid number!")
            else:
                if confirmWipe==1:
                    kuya=avatar()
                    print("\nStarting new game.")
                    sleep(1)
                    print("... (Hit ENTER to continue any time you see '...')")
                    input()
                    sleep(1)
                    break
                elif confirmWipe==2:
                    checkLoad()
                else:
                    print("Please input a valid number!")
    system("cls")

def battle(enemy):
    moveCounter=[]

    while True:

        printScreen(enemy)
        enemyMoveReduction=0
        avatarMoveReduction=0

        avatarMove=kuya.useMove()
        if avatarMove[1]<0:
            enemyMoveReduction=avatarMove[1]
        moveCounter.append(avatarMove)

        enemyMove=enemy.useMove()
        if enemyMove<0:
            avatarMoveReduction=enemyMove

        enemyDamageReceived=avatarMove[1]+avatarMoveReduction
        if enemyDamageReceived<0:
            enemyDamageReceived=0
        enemy.currentHP-=enemyDamageReceived
        sleep(2)
        printScreen(enemy)
        if enemy.currentHP<=0:
            break
        
        if enemyMove>0:
            if random.randint(1,100)>kuya.evasiveness:
                avatarDamageReceived=enemyMove+enemyMoveReduction
                if avatarDamageReceived<0:
                    avatarDamageReceived=0
                kuya.currentHP-=avatarDamageReceived
            else:
                avatarDamageReceived=0
                print("You dodged the attack!")
        sleep(1)
        printScreen(enemy)
        if kuya.currentHP<=0:
            sleep(2)
            print("You have died!\n\nRelaunch game to restart at last save point.")
            sleep(5)
            quit()
    
    sleep(2)
    print(f"{enemy.name} has been defeated!")
    sleep(2)
    kuya.addEXP(moveCounter)
    print("...")
    input()
    system("cls")
    
def checkGoTown(location="Republic City"):
    sleep(2)
    while True:
        try:
            go=int(input(f"Would you like to head back to {location}?\n1. Yes\n2. No\n"))
        except:
            print("Please input a valid number!")
            sleep(2)
            system("cls")
        else:
            sleep(2)
            system("cls")
            if go==1:
                goTown(location)
                break

            elif go==2:
                print("Understood, good luck!")
                break
            else:
                print("Please input a valid number!")
                sleep(2)
                system("cls")

def goTown(location="Republic City"):
    sleep(1)

    
    if location=="Republic City":
        mainArea="City Hall"
        healing="Fan's Dumplings"
        train="Air Temple Island Pavillion"
        destination="journey"
    else:
        mainArea="the recreation room"
        healing="the canteen"
        train="the dojo"
        destination="training"
    print("You head over to " + location)
    system("cls")
    while True:
        print(f"You arrive at {mainArea}.\nWhere would you like to go?\n1. {healing.capitalize()} to fill your stomach and heal up\n2. {train.capitalize()} to check your stats and change your equipped skills\n3. Leave {location} and continue your {destination}\n4. The arena to duel other benders\n5. Save and quit the game\n")
        try:
            place=int(input())
            
        except:
            print("Please enter a valid input!")
            sleep(2)
            system("cls")

        else:
            sleep(2)
            if place==1:
                sleep(2)
                system("cls")
                print(f"Heading to {healing}...")
                sleep(2)
                kuya.heal()
                print("You eat your fill and feel refreshed and ready for battle again.")
                sleep(2)
                system("cls")
            elif place==2:
                sleep(2)
                system("cls")
                print(f"Heading to {train}...")
                sleep(1)
                while True:
                    sleep(1)
                    print("What would you like to do?\n1. Check current stats\n2. Change your current equipped skills")
                    try:
                        dojoChoose=int(input())
                    except:
                        print("Please enter a valid input!")
                        sleep(2)
                        system("cls")
                    else:
                        if dojoChoose==1:
                            sleep(2)
                            system("cls")
                            kuya.displayStats()
                            print("...")
                            input()
                            system("cls")
                            break
                        
                        elif dojoChoose==2:
                            sleep(2)
                            system("cls")
                            kuya.pickSkills()
                            sleep(2)
                            system("cls")
                            break

            elif place==3:
                sleep(2)
                system("cls")
                print(f"Heading off to continue your {destination}.")
                sleep(2)
                system("cls")
                break
            elif place==4:
                sleep(2)
                system("cls")
                boulderToss=skill("Boulder Toss","EARTH",30,25,"Pick up a boulder and toss it at your enemy.")
                pebbleWall=skill("Pebble Wall","EARTH",-50,30,"Quickly gather small pebbles nearby to create a small yet reliable wall, reducing incoming damage.")
                fireball=skill("Fireball","FIRE",50,30,"Hurl a flaming ball at the enemy.")
                fireWall=skill("Fire Wall","FIRE",-30,25,"Raise a wall of flames, reducing enemy line of sight and the power of an enemy skill.")
                breathBlast=skill("Breath Blast","AIR",40,25,"Airbend the breath coming out of your mouth to great a blast of air that is both lethal and hard to dodge.")
                redirect=skill("Redirect","AIR",-30,15,"Airbend to redirect an enemy attack headed your way, nullifying damage from weak attacks and reducing damage from stronger ones.")
                waterScythe=skill("Water Scythe","WATER",60,40,"Form a razor sharp scythe to slash your enemy, dealing large amounts of damage.")
                waterSphere=skill("Water Sphere","WATER",-60,40,"Form a full sphere of water around yourself, strong enough to nullify some attacks.")
                earthGrunt=grunt("Unnamed Earthbender",2,boulderToss,pebbleWall)
                fireGrunt=grunt("Unnamed Firebender",2,fireWall,fireball)
                airGrunt=grunt("Unnamed Airbender",2,breathBlast,redirect)
                waterGrunt=grunt("Unnamed Waterbender",2,waterScythe,waterSphere)
                opponentList=[earthGrunt,fireGrunt,airGrunt,waterGrunt]
                opp=random.randint(0,3)
                battle(opponentList[opp])

            elif place==5:
                saveProgress()
                sleep(2)
                system("cls")
                while True:
                    try: checkQuit=int(input("Would you like to quit the game?\n1. Yes\n2. No\n"))
                    except:
                        print("\nPlease select a valid input!")
                        sleep(2)
                        system("cls")
                    else:
                        if checkQuit==1:
                            print("Quitting the game now.")
                            sleep(2)
                            quit()
                        elif checkQuit==2:
                            sleep(2)
                            system("cls")
                            break
                        else:
                            print("\nPlease select a valid input!")
                            sleep(2)
                            system("cls")
            else:
                print("Please enter a valid input!")
                sleep(2)
                system("cls")

def checkTrain(toDo="Continue your journey"):
    while True:
        try:
            print(f"What would you like to do now?\n1. Keep training\n2. {toDo}")
            checkDo=int(input())
            sleep(2)
        except:
            print("\nPlease enter a valid input!")
            sleep(2)
            system("cls")
        else:
            if checkDo==1:
                sleep(2)
                system("cls")
                return True
            elif checkDo==2:
                sleep(2)
                system("cls")
                return False
            else:
                print("\nPlease enter a valid input!")
                sleep(2)
                system("cls")                

def checkHealBoss(name):
    while True:
        try:
            sleep(1)
            print(f"Would you like to heal up before you take on {name}?\n1. Yes\n2. No")
            inp=int(input())
            sleep(1)
        except:
            print("Please type a valid input!")
            sleep(2)
            system("cls")
        else:
            if inp==1:
                kuya.heal()
                sleep(2)
                print(f"{name.capitalize()} attacks!")
                sleep(2)
                system("cls")
                break
            elif inp==2:
                print(f"{name.capitalize()} attacks!")
                sleep(2)
                system("cls")
                break
            else:
                print("Please type a valid input!")
                sleep(2)
                system("cls")

def readText(filename):
    with open(f"text\\{filename}.txt","r") as text:
        toRead=text.readlines()
    for i in toRead:
        sleep(2)
        print(i)
    input()
    system("cls")

def readConvo(filename):
    with open(f"text\\{filename}.csv","r",encoding="utf-8") as text:
        toRead=list(csv.reader(text))
    for i in toRead:
        print(figlet_format(i[0]))
        sleep(.5)
        print(f"{i[1]}")
        sleep(2)
        print(f"\n\n{i[2]}")
        sleep(2)
        print("...")
        input()
        system("cls")

def chap0():

    readText(0.01)
    readText(0.02)
    readConvo(0.03)
    readText(0.04)
    readConvo(0.05)
    readText(0.06)
    readConvo(0.07)
    readText(0.08)
    fireball=skill("Fireball","FIRE",50,30,"Hurl a flaming ball at the enemy.")
    fireCrook=grunt("Firebender crook",1,fireball,fireball)

    printScreen(fireCrook,"Earthbender Kuya")
    avatarMove=kuya.useMove()
    fireCrook.currentHP-=avatarMove[1]
    sleep(2)
    printScreen(fireCrook)
    enemyMove=fireCrook.useMove()
    kuya.currentHP-=enemyMove
    sleep(2)
    printScreen(fireCrook)
    sleep(3)
    system("cls")

    readText(0.09)
    kuya.resetStats()

    print(figlet_format("ONE YEAR LATER"))
    sleep(2)
    print("In the city of Ba Sing Se...")
    sleep(3)
    system("cls")
    readConvo("0.10")
    kuya.setProgress(1)

def chap1():
    if kuya.progress==1:
        kuya.clearSkillPool()
        boulderTossTraining=skill("Boulder Toss","EARTH",10,5,"Pick up a boulder and toss it at your enemy.")
        pebbleWallTraining=skill("Pebble Wall","EARTH",-10,5,"Quickly gather small pebbles nearby to create a small yet reliable wall, reducing incoming damage.")
        kuya.addSkillPool(boulderTossTraining,pebbleWallTraining)
        goTown("the recreation room")
        while len(kuya.equippedSkills)<3:
            readConvo(0.11)
            goTown("the recreation room")

        readText(1.01)
        readConvo(1.02)
        while True:
            earthTrainingEnemy=grunt("White Lotus Earthbender",1,boulderTossTraining,pebbleWallTraining)
            battle(earthTrainingEnemy)
            if kuya.earthLvl>=2:
                break
            checkGoTown("the White Lotus' Inn")

        boulderToss=skill("Boulder Toss","EARTH",30,25,"Pick up a boulder and toss it at your enemy.")
        pebbleWall=skill("Pebble Wall","EARTH",-50,30,"Quickly gather small pebbles nearby to create a small yet reliable wall, reducing incoming damage.")
        kuya.clearSkillPool()
        kuya.addSkillPool(boulderToss,pebbleWall)
        kuya.setSkills(boulderToss,pebbleWall)
        kuya.setProgress(1.1)
        readText(1.03)
        checkGoTown("the White Lotus' Inn")
    
    if kuya.progress==1.1:
        toTrain=checkTrain("Challenge Master Khoshah")
        while toTrain==True:
            boulderTossTraining=skill("Boulder Toss","EARTH",10,5,"Pick up a boulder and toss it at your enemy.")
            pebbleWallTraining=skill("Pebble Wall","EARTH",-10,5,"Quickly gather small pebbles nearby to create a small yet reliable wall, reducing incoming damage.")
            earthTrainingEnemy=grunt("White Lotus Earthbender",1,boulderTossTraining,pebbleWallTraining)
            battle(earthTrainingEnemy)
            checkGoTown("the White Lotus' Inn")
            toTrain=checkTrain("Challenge Master Khoshah")

        readConvo(1.04)
        boulderToss=skill("Boulder Toss","EARTH",30,25,"Pick up a boulder and toss it at your enemy.")
        pebbleWall=skill("Pebble Wall","EARTH",-50,30,"Quickly gather small pebbles nearby to create a small yet reliable wall, reducing incoming damage.")
        earthMaster=master("Earthbending Master Khoshah",2,boulderToss,boulderToss,boulderToss,boulderToss,boulderToss,pebbleWall)
        battle(earthMaster)
        readConvo(1.05)
        readText(1.06)
        kuya.setProgress(1.2)

    if kuya.progress==1.2:
        kuya.clearSkillPool()
        fireballTraining=skill("Fireball","FIRE",10,5,"Hurl a flaming ball at the enemy.")
        fireWallTraining=skill("Fire Wall","FIRE",-10,5,"Raise a wall of flames, reducing enemy line of sight and the power of an enemy skill.")
        kuya.addSkillPool(fireballTraining,fireWallTraining)
        checkGoTown("the White Lotus' Inn")
        while len(kuya.equippedSkills)<3:
            readConvo(1.07)
            goTown("the White Lotus' Inn")

        readConvo(1.08)
        while True:
            fireTrainingEnemy=grunt("White Lotus Firebender",1,fireballTraining,fireWallTraining)
            battle(fireTrainingEnemy)
            if kuya.fireLvl>=2:
                readText(1.09)
                break
            checkGoTown("the White Lotus' Inn")

        fireball=skill("Fireball","FIRE",50,30,"Hurl a flaming ball at the enemy.")
        fireWall=skill("Fire Wall","FIRE",-30,25,"Raise a wall of flames, reducing enemy line of sight and the power of an enemy skill.")
        kuya.clearSkillPool()
        kuya.addSkillPool(fireball,fireWall)
        kuya.setSkills(fireball,fireWall)
        kuya.setProgress(1.3)
        checkGoTown("the White Lotus' Inn")
    
    if kuya.progress==1.3:
        toTrain=checkTrain("Challenge Master Mou")
        while toTrain==True:
            fireballTraining=skill("Fireball","FIRE",10,5,"Hurl a flaming ball at the enemy.")
            fireWallTraining=skill("Fire Wall","FIRE",-10,5,"Raise a wall of flames, reducing enemy line of sight and the power of an enemy skill.")
            fireTrainingEnemy=grunt("White Lotus Firebender",1,fireballTraining,fireWallTraining)
            battle(fireTrainingEnemy)
            checkGoTown("the White Lotus' Inn")
            toTrain=checkTrain("Challenge Master Mou")

        readConvo("1.10")
        fireball=skill("Fireball","FIRE",50,30,"Hurl a flaming ball at the enemy.")
        fireWall=skill("Fire Wall","FIRE",-30,25,"Raise a wall of flames, reducing enemy line of sight and the power of an enemy skill.")
        fireMaster=master("Firebending Master Mou",2,fireball,fireball,fireball,fireball,fireWall)
        battle(fireMaster)
        readConvo(1.11)
        readText(1.12)
        kuya.setProgress(1.4)
    
    if kuya.progress==1.4:
        kuya.clearSkillPool()
        breathBlastTraining=skill("Breath Blast","AIR",10,5,"Airbend the breath coming out of your mouth to great a blast of air that is both lethal and hard to dodge.")
        redirectTraining=skill("Redirect","AIR",-10,5,"Airbend to redirect an enemy attack headed your way, nullifying damage from weak attacks and reducing damage from stronger ones.")
        kuya.addSkillPool(breathBlastTraining,redirectTraining)
        checkGoTown("the White Lotus' Inn")
        while len(kuya.equippedSkills)<3:
            readConvo(1.13)
            goTown("the White Lotus' Inn")

        readConvo(1.14)
        while True:
            airTrainingEnemy=grunt("White Lotus Airbender",1,breathBlastTraining,redirectTraining)
            battle(airTrainingEnemy)
            if kuya.airLvl>=2:
                readText(1.15)
                break
            checkGoTown("the White Lotus' Inn")

        breathBlast=skill("Breath Blast","AIR",40,25,"Airbend the breath coming out of your mouth to great a blast of air that is both lethal and hard to dodge.")
        redirect=skill("Redirect","AIR",-30,15,"Airbend to redirect an enemy attack headed your way, nullifying damage from weak attacks and reducing damage from stronger ones.")
        kuya.clearSkillPool()
        kuya.addSkillPool(breathBlast,redirect)
        kuya.setSkills(breathBlast,redirect)
        kuya.setProgress(1.5)
        checkGoTown("the White Lotus' Inn")
    
    if kuya.progress==1.5:
        toTrain=checkTrain("Challenge Master Kai")
        while toTrain==True:
            breathBlastTraining=skill("Breath Blast","AIR",10,5,"Airbend the breath coming out of your mouth to great a blast of air that is both lethal and hard to dodge.")
            redirectTraining=skill("Redirect","AIR",-10,5,"Airbend to redirect an enemy attack headed your way, nullifying damage from weak attacks and reducing damage from stronger ones.")
            airTrainingEnemy=grunt("White Lotus Airbender",1,breathBlastTraining,redirectTraining)
            battle(airTrainingEnemy)
            checkGoTown("the White Lotus' Inn")
            toTrain=checkTrain("Challenge Master Kai")

        readConvo(1.16)
        breathBlast=skill("Breath Blast","AIR",40,25,"Airbend the breath coming out of your mouth to great a blast of air that is both lethal and hard to dodge.")
        redirect=skill("Redirect","AIR",-30,15,"Airbend to redirect an enemy attack headed your way, nullifying damage from weak attacks and reducing damage from stronger ones.")
        airMaster=master("Airbending Master Kai",2,breathBlast,breathBlast,breathBlast,redirect)
        battle(airMaster)
        readConvo(1.17)
        readText(1.18)
        kuya.setProgress(1.6)

    if kuya.progress==1.6:
        kuya.clearSkillPool()
        waterScytheTraining=skill("Water Scythe","WATER",10,5,"Form a razor sharp scythe to slash your enemy, dealing large amounts of damage.")
        waterSphereTraining=skill("Water Sphere","WATER",-10,5,"Form a full sphere of water around yourself, strong enough to nullify some attacks.")
        kuya.addSkillPool(waterScytheTraining,waterSphereTraining)
        checkGoTown("the White Lotus' Inn")
        while len(kuya.equippedSkills)<3:
            readConvo(1.19)
            goTown("the White Lotus' Inn")

        readConvo("1.20")
        while True:
            waterTrainingEnemy=grunt("White Lotus Waterbender",1,waterScytheTraining,waterSphereTraining)
            battle(waterTrainingEnemy)
            if kuya.waterLvl>=2:
                readText(1.21)
                break
            checkGoTown("the White Lotus' Inn")

        waterScythe=skill("Water Scythe","WATER",60,40,"Form a razor sharp scythe to slash your enemy, dealing large amounts of damage.")
        waterSphere=skill("Water Sphere","WATER",-60,40,"Form a full sphere of water around yourself, strong enough to nullify some attacks.")
        kuya.clearSkillPool()
        kuya.addSkillPool(waterScythe,waterSphere)
        kuya.setSkills(waterScythe,waterSphere)
        kuya.setProgress(1.7)
        checkGoTown("the White Lotus' Inn")
    
    if kuya.progress==1.7:
        toTrain=checkTrain("Challenge Master Eska")
        while toTrain==True:
            waterScytheTraining=skill("Water Scythe","WATER",10,5,"Form a razor sharp scythe to slash your enemy, dealing large amounts of damage.")
            waterSphereTraining=skill("Water Sphere","WATER",-10,5,"Form a full sphere of water around yourself, strong enough to nullify some attacks.")
            waterTrainingEnemy=grunt("White Lotus Waterbender",1,waterScytheTraining,waterSphereTraining)
            battle(waterTrainingEnemy)
            checkGoTown("the White Lotus' Inn")
            toTrain=checkTrain("Challenge Master Eska")

        readConvo(1.22)
        waterScythe=skill("Water Scythe","WATER",60,40,"Form a razor sharp scythe to slash your enemy, dealing large amounts of damage.")
        waterSphere=skill("Water Sphere","WATER",-60,40,"Form a full sphere of water around yourself, strong enough to nullify some attacks.")
        waterMaster=master("Waterbending Master Eska",2,waterScythe,waterScythe,waterSphere)
        battle(waterMaster)
        readConvo(1.23)
        readText(1.24)
        kuya.setProgress(2)
        sleep(2)
  
def chap2():
    if kuya.progress==2:
        print(figlet_format("THE NEXT DAY"))
        sleep(2)
        print("...")
        input()
        system("cls")
        readConvo(2.01)
        kuya.clearSkillPool()
        kuya.setNumEquipped(5)
        boulderToss=skill("Boulder Toss","EARTH",30,25,"Pick up a boulder and toss it at your enemy.")
        pebbleWall=skill("Pebble Wall","EARTH",-50,30,"Quickly gather small pebbles nearby to create a small yet reliable wall, reducing incoming damage.")
        fireball=skill("Fireball","FIRE",50,30,"Hurl a flaming ball at the enemy.")
        fireWall=skill("Fire Wall","FIRE",-30,25,"Raise a wall of flames, reducing enemy line of sight and the power of an enemy skill.")
        breathBlast=skill("Breath Blast","AIR",40,25,"Airbend the breath coming out of your mouth to great a blast of air that is both lethal and hard to dodge.")
        redirect=skill("Redirect","AIR",-30,15,"Airbend to redirect an enemy attack headed your way, nullifying damage from weak attacks and reducing damage from stronger ones.")
        waterScythe=skill("Water Scythe","WATER",60,40,"Form a razor sharp scythe to slash your enemy, dealing large amounts of damage.")
        waterSphere=skill("Water Sphere","WATER",-60,40,"Form a full sphere of water around yourself, strong enough to nullify some attacks.")
        kuya.addSkillPool(boulderToss,pebbleWall,fireball,fireWall,breathBlast,redirect,waterScythe,waterSphere)
        if kuya.earthLvl==5:
            rockArmor=skill("Rock Armor","EARTH",-999,100,"Form a suit of armor out of rocks to completely nullify one attack.")
            kuya.addSkillPool(rockArmor)
        if kuya.fireLvl==5:
            infernoVortex=skill("Inferno Vortex","FIRE",120,85,"Trap your enemy in a vortex of flames, dealing lethal damage to them.")
            kuya.addSkillPool(infernoVortex)
        if kuya.airLvl==5:
            suffocate=skill("Asphyxiate","AIR",999,150,"Spend a large amount of mana to airbend out of your enemy's lungs, instantly killing them.")
            kuya.addSkillPool(suffocate)
        if kuya.waterLvl==5:
            iceBarrier=skill("Ice Barrier","WATER",-120,60,"Form a huge ice barrier that's brittle yet strong, negating a large amount of damage to yourself.")
            kuya.addSkillPool(iceBarrier)
        kuya.setProgress(2.1)
        checkGoTown("the recreation room")
        while len(kuya.equippedSkills)<kuya.numEquipped:
            readConvo(2.02)
            goTown("the recreation room")

    if kuya.progress==2.1:
        readText(2.03)
        print(figlet_format("MEANWHILE"))
        sleep(2)
        print("Somewhere in the Earth Kingdom...\n...")
        input()
        system("cls")
        readConvo(2.04)
        readText(2.05)
        readConvo(2.06)
        kuya.setProgress(2.2)
        checkGoTown("the Eastern Air Temple Hall")
    
    if kuya.progress==2.2:
        readText(2.07)
        readConvo(2.08)
        readText(2.09)
        readConvo("2.10")
        print("Three spirits and the Airbender attack you.\n...")
        input()
        system("cls")
        bite=skill("Bite","SPIRIT",20,10,"Bite the enemy.")
        phase=skill("Phase","SPIRIT",-20,10,"Phase through a skill.")
        for num in range(3):
            if num%2==0:
                checkHealBoss("the spirit")
            spiritGrunt=grunt("Angered Dog Spirit",1,bite,phase)
            battle(spiritGrunt)
        checkHealBoss("the mysterious Airbender")
        vortexBlast=skill("Vortex Blast","AIR",40,25,"Airbend the breath coming out of your mouth to great a blast of air that is both lethal and hard to dodge.")
        redirect=skill("Redirect","AIR",-30,15,"Airbend to redirect an enemy attack headed your way, nullifying damage from weak attacks and reducing damage from stronger ones.")
        boulderToss=skill("Boulder Toss","EARTH",30,25,"Pick up a boulder and toss it at your enemy.")
        waterScythe=skill("Water Scythe","WATER",60,40,"Form a razor sharp scythe to slash your enemy, dealing large amounts of damage.")
        fireWall=skill("Fire Wall","FIRE",-30,25,"Raise a wall of flames, reducing enemy line of sight and the power of an enemy skill.")
        aang=master("Mysterious Airbender",3,vortexBlast,redirect,boulderToss,waterScythe,fireWall)
        battle(aang)
        readConvo(2.11)
        readText(2.12)
        readConvo(2.13)
        readText(2.14)
        kuya.setProgress(2.3)
        goTown()

    if kuya.progress==2.3:
        readConvo(2.15)
        readText(2.16)
        peck=skill("peck","SPIRIT",20,10,"Bite the enemy.")
        phase=skill("Phase","SPIRIT",-20,10,"Phase through a skill.")
        for num in range(4):
            if num%2==0:
                checkHealBoss("the spirit")
            spiritGrunt=grunt("Angered Bird Spirit",1,peck,phase)
            battle(spiritGrunt)
        checkHealBoss("Avatar Roku")
        fireBreath=skill("Fire Breath","FIRE",50,30,"Hurl a flaming ball at the enemy.")
        fireWall=skill("Fire Wall","FIRE",-30,25,"Raise a wall of flames, reducing enemy line of sight and the power of an enemy skill.")
        pebbleWall=skill("Pebble Wall","EARTH",-50,30,"Quickly gather small pebbles nearby to create a small yet reliable wall, reducing incoming damage.")
        breathBlast=skill("Breath Blast","AIR",40,25,"Airbend the breath coming out of your mouth to great a blast of air that is both lethal and hard to dodge.")
        boulderToss=skill("Boulder Toss","EARTH",30,25,"Pick up a boulder and toss it at your enemy.")
        roku=master("Avatar Roku",3,fireBreath,fireWall,pebbleWall,breathBlast,boulderToss)
        battle(roku)
        readConvo(2.17)
        readText(2.18)
        readConvo(2.19)
        kuya.setProgress==2.4
        goTown()
    
    if kuya.progress==2.4:
        readConvo("2.20")
        readText(2.21)
        scratch=skill("Scratch","SPIRIT",20,10,"Bite the enemy.")
        phase=skill("Phase","SPIRIT",-20,10,"Phase through a skill.")
        for num in range(5):
            if num%2==0:
                checkHealBoss("the spirit")
            spiritGrunt=grunt("Angered Ape Spirit",1,scratch,phase)
            battle(spiritGrunt)
        checkHealBoss("Avatar Kyoshi")
        boulderToss=skill("Boulder Toss","EARTH",30,25,"Pick up a boulder and toss it at your enemy.")
        fanSlash=skill("Fan Slash","EARTH",-50,30,"Quickly gather small pebbles nearby to create a small yet reliable wall, reducing incoming damage.")
        fireball=skill("Fireball","FIRE",50,30,"Hurl a flaming ball at the enemy.")
        redirect=skill("Redirect","AIR",-30,15,"Airbend to redirect an enemy attack headed your way, nullifying damage from weak attacks and reducing damage from stronger ones.")
        waterSphere=skill("Water Sphere","WATER",-60,40,"Form a full sphere of water around yourself, strong enough to nullify some attacks.")
        kyoshi=master("Avatar Kyoshi",4,boulderToss,fanSlash,fireball,redirect,waterSphere)
        battle(kyoshi)
        readConvo(2.22)
        readText(2.23)
        kuya.setProgress(2.5)
        goTown()
    
    if kuya.progress==2.5:
        readConvo(2.24)
        readText(2.25)
        slash=skill("Slash","SPIRIT",20,10,"Bite the enemy.")
        phase=skill("Phase","SPIRIT",-20,10,"Phase through a skill.")
        for num in range(7):
            if num%2==0:
                checkHealBoss("the spirit")
            spiritGrunt=grunt("Angered Sea Spirit",1,slash,phase)
            battle(spiritGrunt)
        checkHealBoss("Avatar Kuruk")
        rain=skill("Torrential Downpour","WATER",80,40,"Form a razor sharp scythe to slash your enemy, dealing large amounts of damage.")
        waterSphere=skill("Water Sphere","WATER",-60,40,"Form a full sphere of water around yourself, strong enough to nullify some attacks.")
        breathBlast=skill("Breath Blast","AIR",40,25,"Airbend the breath coming out of your mouth to great a blast of air that is both lethal and hard to dodge.")
        fireball=skill("Fireball","FIRE",50,30,"Hurl a flaming ball at the enemy.")
        redirect=skill("Redirect","AIR",-30,15,"Airbend to redirect an enemy attack headed your way, nullifying damage from weak attacks and reducing damage from stronger ones.")
        kuruk=master("Avatar Kuruk",4,rain,waterSphere,breathBlast,fireball,redirect)
        battle(kuruk)
        readConvo(2.26)
        readText(2.27)
        kuya.setProgress(2.6)
        goTown()

    if kuya.progress==2.6:
        readConvo(2.28)
        checkHealBoss("Avatar Yangchen")
        breathBlast=skill("Breath Blast","AIR",40,25,"Airbend the breath coming out of your mouth to great a blast of air that is both lethal and hard to dodge.")
        redirect=skill("Redirect","AIR",-30,15,"Airbend to redirect an enemy attack headed your way, nullifying damage from weak attacks and reducing damage from stronger ones.")
        pebbleWall=skill("Pebble Wall","EARTH",-50,30,"Quickly gather small pebbles nearby to create a small yet reliable wall, reducing incoming damage.")
        fireball=skill("Fireball","FIRE",50,30,"Hurl a flaming ball at the enemy.")
        tornado=skill("Tornado","AIR",60,20,"Forms a tornado.")
        yangchen=master(breathBlast,breathBlast,redirect,pebbleWall,fireball,tornado)
        battle(yangchen)
        readConvo(2.29)
        readText("2.30")
        readConvo(2.31)
        kuya.setProgress(3)
        goTown()

def chap3():
    if kuya.progress==3:
        readConvo(3.01)
        readText(3.02)
        readText(3.03)
        phase=skill("Phase","SPIRIT",-40,10,"Phase through a skill.")
        bite=skill("Bite","SPIRIT",30,10,"Bite the enemy.")
        peck=skill("peck","SPIRIT",30,10,"Bite the enemy.")
        scratch=skill("Scratch","SPIRIT",30,10,"Bite the enemy.")
        slash=skill("Slash","SPIRIT",30,10,"Bite the enemy.")

        spirit=master("Hybrid dog-bird Spirit",3,phase,bite,peck)
        battle(spirit)
        checkHealBoss("the next spirit")

        spirit=master("Sea ape Spirit",3,phase,scratch,slash)
        battle(spirit)
        checkHealBoss("the next spirit")

        spirit=master("Hybrid dog-ape spirit",3,phase,bite,scratch)
        battle(spirit)
        checkHealBoss("the next spirit")

        spirit=master("Sea bird spirit",3,phase,peck,slash)
        battle(spirit)
        checkHealBoss("the next spirit")

        spirit=master("Sea dog spirit",3,phase,bite,slash)
        battle(spirit)
        checkHealBoss("the next spirit")

        spirit=master("Hybrid bird-ape spirit",3,phase,peck,scratch)
        battle(spirit)

        readText(3.04)
        kuya.setProgress(3.1)
        checkGoTown()

    if kuya.progress==3.1:
        readText(3.05)
        bite=skill("Bite","SPIRIT",30,10,"Bite the enemy.")
        for num in range(2):
            spirit=grunt("Angered Dark Spirit",3,bite,bite)
            battle(spirit)
        readText(3.06)
        readConvo(3.07)
        checkHealBoss("Former Liutenant Bohan")
        boulderToss=skill("Boulder Toss","EARTH",30,25,"Pick up a boulder and toss it at your enemy.")
        pebbleWall=skill("Pebble Wall","EARTH",-50,30,"Quickly gather small pebbles nearby to create a small yet reliable wall, reducing incoming damage.")
        groundBreak=skill("Ground Shatter","EARTH",60,60,"Breaks the ground under you.")
        bohan=master("Former Liutenant Bohan",3,boulderToss,boulderToss,boulderToss,pebbleWall,groundBreak)
        battle(bohan)
        readConvo(3.08)
        kuya.setProgress(3.2)
        checkGoTown()

    if kuya.progress==3.2:
        readText(3.09)
        readConvo("3.10")
        boulderToss=skill("Boulder Toss","EARTH",30,25,"Pick up a boulder and toss it at your enemy.")
        pebbleWall=skill("Pebble Wall","EARTH",-50,30,"Quickly gather small pebbles nearby to create a small yet reliable wall, reducing incoming damage.")
        spectralWhip=skill("Spectral Whip","SPIRIT",30,25,"Whip the enemy with spiritual energy.")
        barrier=skill("Spiritual Barrier","SPIRIT",-30,30,"Forms a barrier of spiritual energy.")
        tien=master("Corrupted Tien",5,boulderToss,boulderToss,pebbleWall,spectralWhip,spectralWhip,barrier)
        battle(tien)
        readText(3.11)
        readConvo(3.12)
        readText(3.13)
        kuya.setProgress(4)
        checkGoTown()

def chap4():
    readText(4.01)
    while True:
        try:
            checkSave=int(input("Would you like to save your game?\n1. Yes\n2. No\n"))
        except:
            print("Please input a valid number!")
            sleep(2)
            system("cls")
        else:
            if checkSave==1:
                saveProgress()
                sleep(2)
                break
            elif checkSave==2:
                sleep(2)
                break
            else:
                print("Please input a valid number!")
                sleep(2)
                system("cls")
    system("cls")
    sleep(2)
    print(figlet_format("\nAVATAR"))
    sleep(2)
    print("\tThe Redemption of Kuya\n")
    sleep(2)
    print("...")
    input()
    quit()

def main():
    checkLoad()
    if kuya.progress==0: chap0()
    if int(kuya.progress)==1: chap1()
    if int(kuya.progress)==2: chap2()
    if int(kuya.progress)==3: chap3()
    if kuya.progress==4: chap4()

main()