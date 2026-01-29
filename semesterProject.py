'''
Program relating to the tabletop game Warhammer 40,000. Game features combat with various properties
 that influence dice rolls to determine success. Program would prompt user for characteristics of said attack
   and characteristics of target, as well as checking if certain temporary buffs or debuffs are active. 
   Program would then randomly “roll” dice to generate a hypothetical attack.
Would feature damage done with that “roll”, average amount of damage that should be done, and percentage of successful attacks, 
both on that roll and on average. Would feature options for quickly “re-rolling” and possibly comparing one roll with another with different characteristics.
Math library expected to be used

'''

import math
from tkinter import *
import tkinter as tk
#from tkinter.ttk import *
import random
#import semesterTkinter as tk
from multiprocessing import Process, Queue, Pipe

#paths = sys.path
#num = 1
#for path in paths:
#    print('{}. {}'.format(num, path))
#    num += 1
#import numpy as np
'''RULES OF THE GAME
    This program simulates the shooting,charge(hopefully),and fight phases of the tabletop game Warhammer 40,000, built for its 10th edition.
    Every unit in the game has ranged and/or melee weapons, which the program prompts you to input the characteristics of. 
    It is ideal to have the unit's datasheet on hand to make this easy, but for simple testing of functionality any numbers will do.
    In the shooting phase, units make attacks with ranged weapons. These weapons are always assumed to be in range, as otherwise would require simulating a game board
    The program will "roll" an amount of imaginary dice that correspond to the attacks innate to that weapon, multiplied by the amount of models that have that weapon
    Those dice that are >= the BS(or WS in case of melee) listed on that weapon's profile are kept as successessful hits,
    with certain values being noted aside for rules interactions.
    The successful hits are then rolled, and those that meet the wound requirements for their target(influenced by the S of the weapon against the T of the target)
    are kept.
    The computer rolls the wound dice, and those that meet the Sv requirements nullify a successful wound.
    The dice that do not meet the Sv requirement are failed saves, and damage is allocated accordingly based off the D of the weapon.
    A note for damage taken is that, unless in certain cases, damage does not "spill over" from one model to another.
    For example, if a model with 2 wounds(health) fails a save against a 3 damage weapon, the next model in the unit(if there is one),
    does not take the extra 1 damage, it is lost. This is counted for by the computer, so everything displayed is correct to the game
'''
#from semesterTkinter import run as tk
#from semesterTkinter import f
#    parent_conn,child_conn = Pipe()
#    p = Process(target = f, args = (child_conn,))
#    p.start()
#    print(parent_conn.recv())
names = dict()
enemyNames = dict()
goodPointer = 0#pointers for your units and the enemy units
badPointer = 0
class statLine:
    #When going through the weapons for the unit, go through the bs and ws lists. With a bs list of n length and ws of m length, the s list will be 
    # n + m long, and the first n entries we know are for ranged weapons.
    #Also, the checks for toughness, saves,etc. will be done in the shooting/fight phase, because those can technically change throughout the game
    #if leaders are sniped out or their bodyguards are killed,etc.. For the average user it won't matter but it does give it technically more options for simulation
    #When a unit is created at the start of the game, it only has an offensive profile. When a unit is created during your attacks, it only has a defensive profile.
    #In the subsequent phases where they hit you back and you take damage, your unit is given a defensive profile and the enemy is given an offensive profie;
    def __init__(self,name,a = [],bs = [],ws = [],s = [], ap = [], d = [],t = 0, sv = 0, inv = 0, w =0, m = 0):
        self.name = name
        self.a = a
        self.bs = bs
        self.ws = ws
        self.s = s
        self.ap = ap
        self.d = d
        self.t = t
        self.sv = sv
        self.inv = inv
        self.w = w
        self.m = m
def checkedInput(typeToBe,forcePositive = False,binary = False):
    temp = input().strip()
    #I don't really think it's necessary to have a special method for checking input but I wanted to give protection against bad inputs and flex recursion
    if typeToBe == "int":
        try:temp = int(temp)
        except ValueError:
            print(f'Invalid input, please put in a {typeToBe} value instead')
            checkedInput(typeToBe,forcePositive,binary)
    elif str(type(temp)) != f"<class '{typeToBe}'>":
        print(f'Invalid input, please put in a {typeToBe} value instead')
        checkedInput(typeToBe,forcePositive,binary)
    if forcePositive == True:
        if temp < 0:
            #print("NON-NEGATIVE INTEGER")
            checkedInput(typeToBe,True,binary)
    if binary == True:
        if temp.upper() != "Y" and temp.upper() != "N":
            print("Y/N")
            checkedInput(typeToBe,forcePositive,binary)
        return temp.upper()
    return temp
#Debating making this a class to allow you to check every unit's performance by the round with objects representing their shooting/fighting
def rollDice(amount):
    rolled = [0] * amount
    i = 0
    while i < len(rolled):
        rolled[i] = random.randint(1,6)
        i += 1
    return rolled

#Tkinter section. Ideally I'd get the below segment to work so I could have the computations and tkinter be two separate files linked by a pipe. Oh well.
#from multiprocessing import Process, Pipe
#FUTURE PLAN IS TO USE MULTIPROCESSING TO OPEN A PIPE BETWEEN THE TKINTER AND THE CODE AND SEND MESSAGES THROUGH
#As im re writing this I realize it may not be a great idea. If I have time i'll try to implement and if not the whole thing will be in the tkinter part
#def f(child_conn):
#    msg = "test"
#   child_conn.send(msg)
#    child_conn.close()

root = tk.Tk()
root.geometry('600x600')
root.title("Warhammer 40,000 10th Edition Damage Calculator")
input = tk.StringVar()
output = tk.StringVar()
#plan for moving through the program is to have methods for each phase part, and just relabel the boxes and such, then return the values needed to the main program
input1 = tk.StringVar(root,"Attacks")#General purpose inputs and input boxes. Initialized to values for creating a unit cuz that's what you'll do first
input2 = tk.StringVar(root,"Skill")
input3 = tk.StringVar(root,"Strength")
input4 = tk.StringVar(root,"Armor Piercing")
input5 = tk.StringVar(root,"Damage")
input6 = tk.StringVar(root,"Name")#Debating changing this to Models and then having the function of inputting name folded temporarily into a dif. variable
input7 = tk.StringVar(root,"Num. Models")
inputB1 = tk.Entry(root)
inputB2 = tk.Entry(root)
inputB3 = tk.Entry(root)
inputB4 = tk.Entry(root)
inputB5 = tk.Entry(root)
inputB7 = tk.Entry(root)
proceed = tk.Button(root)
button2 = tk.Button(root)
intro = tk.Label(root)
#IMPLEMENT GRID CLEARING METHOD TO CLEAR WHOLE 
def cleanUp():
    for i in root.grid_slaves():
        i.grid_forget()
def startUp():
    #intro = tk.Label(root,text = "Welcome to Warhammer 40,000 10th Edition Damage Calculator. To begin, please press the button.")
    intro.configure(text = "Welcome to Warhammer 40,000 10th Edition Damage Calculator. To begin, please press the button.")
    proceed.configure(text = "Begin",command = lambda:addUnit("your"))
    intro.grid(row = 0, column = 2)
    proceed.grid(row = 1, column = 2)
def setDefault():
    inputB1.configure(textvariable = input1)
    inputB2.configure(textvariable = input2)
    inputB3.configure(textvariable = input3)
    inputB4.configure(textvariable = input4)
    inputB5.configure(textvariable = input5)
    inputB1.grid(row = 1, column = 0,pady = 0)
    inputB2.grid(row = 2, column = 0,pady = 0)
    inputB3.grid(row = 3, column = 0,pady = 0)
    inputB4.grid(row = 4, column = 0,pady = 0)
    inputB5.grid(row = 5, column = 0,pady = 0)
#When adding weapon, also add list(or something else) to determine how many models have that weapon
#add config to allow smart death of units?(Models equipped with basic weapons will be killed before models with special weapons)
def addUnit(string,toUpdate = None, yours = True,defensive = False):
    #button2.configure(text = "Submit Name",pady = 0, command ) Debating separate button to confirm and submit name, but if I'm switching pages and text register
    #then I wouldn't have to worry about overwriting the inputted name until the next time a unit is made.
    #ADD UNIT DEFENSIVE STATS HERE
    #Have a truth value that determines if its adding to your units or the enemy's. Then when you fill out the initial info it checks it and updates the dictionary accordingly
    #Also upon switching screens it resets the inputs to the proper names and stores the name you filled in so that it can still access it.
    cleanUp()
    def addWeapon(string, toUpdate = None,yours = True,defensive = False): 
        #Using inputs 2-6
        print(f'Defensive?{defensive}')
        if toUpdate == None:
            if yours == True:names.update({str(input6.get()):statLine(str(input6.get()),[],[],[],[],[],[],int(input2.get()),int(input3.get()),int(input4.get()),int(input5.get()),int(input7.get()))})
            else:enemyNames.update({str(input6.get()):statLine(str(input6.get()),[],[],[],[],[],[],int(input2.get()),int(input3.get()),int(input4.get()),int(input5.get()),int(input7.get()))})
        if defensive == False:
            cleanUp()
            intro.grid()
            proceed.grid()
            button2.grid()
            intro.configure(text = "Is " +  string + " unit equipped with a ranged weapon?",pady = 0)
            proceed.configure(text = "Yes",pady = 0,command = lambda:recursiveAddWeapon(string, True, toUpdate,yours,defensive))
            button2.configure(text = "No",pady = 0, command = lambda:recursiveAddWeapon(string, False, toUpdate,yours,defensive))
            intro.grid(row = 0, column = 2)#Can call grid with no parameters to make it appear again
            proceed.grid(row = 1, column = 1)
            button2.grid(row = 1, column = 2)
        else:chooseUnits()
        def recursiveAddWeapon(string, ranged, toUpdate = None,yours = True,defensive = False):
            #have ranged be boolean and if its true then add the values into bs instead of ws
            
            cleanUp()
            setDefault()
            intro.grid()
            intro.configure(text = "Please input the characteristics of the weapon in the boxes below as INTEGER ONLY, then press submit to confirm")
            intro.grid(row = 0, column = 0)
            def addValues(string, ranged, toUpdate = None,yours = True,defensive = False):
                nonlocal a,bs,ws,s,ap,d
                cleanUp()
                def helper( toUpdate = None,defensive = False):
                    global input6#probably not needed because just reading input6
                    #if toUpdate == None:
                    #names.update({str(input6.get()):statLine(str(input6.get()),a,bs,ws,s,ap,d,0,0,0,0,int(inputB7.get()))})
                    if toUpdate != None:defensive = True
                    if defensive == False:
                        print(f'added {a},{bs},{ws},{s},{ap},{d}')
                        intro.configure(text = "Would you like to add any other units?")
                        proceed.configure(text = "Yes",pady = 0,command = lambda:addUnit(string))
                        button2.configure(text = "No",pady = 0, command = lambda:chooseUnits())
                        intro.grid(row = 0, column = 2)
                        proceed.grid(row = 1, column = 4)
                        button2.grid(row = 1, column = 5)
                    else:
                        print("Choosing weapon")
                        chooseWeapon(goodPointer,badPointer)
                    #print(toUpdate in names, toUpdate in enemyNames,toUpdate.name)
                a.append(int(input1.get()))
                if ranged == True:bs.append(int(input2.get()))
                else:ws.append(int(input2.get()))
                s.append(int(input3.get()))
                ap.append(int(input4.get()))
                d.append(int(input5.get()))
                if yours == True:names.update({str(input6.get()):statLine(str(input6.get()),a,bs,ws,s,ap,d,names[str(input6.get())].t,names[str(input6.get())].sv,names[str(input6.get())].inv,names[str(input6.get())].w,names[str(input6.get())].m)})
                else:enemyNames.update({str(input6.get()):statLine(str(input6.get()),a,bs,ws,s,ap,d,enemyNames[str(input6.get())].t,enemyNames[str(input6.get())].sv,enemyNames[str(input6.get())].inv,enemyNames[str(input6.get())].w,enemyNames[str(input6.get())].m)})
                #inputB6.grid_forget()
                intro.grid()
                proceed.grid()
                button2.grid()
                intro.configure(text = "Is " + string + " unit equipped with more weapons?",pady = 0)
                proceed.configure(text = "Yes",pady = 0,command = lambda:recursiveAddWeapon(string,ranged,toUpdate,yours,defensive))
                button2.configure(text = "No",pady = 0, command = lambda:helper(toUpdate,defensive))#
                intro.grid(row = 0, column = 2)
                proceed.grid(row = 1, column = 4)
                button2.grid(row = 1, column = 5)
            #print(inputB1.get())input tetvariables not needed, can just grab directy
            setDefault()
            input1.set("Attacks")
            input2.set("Skill")
            input3.set("Strength")
            input4.set("Armor Piercing")
            input5.set("Damage")
            proceed.configure(text = "Finish",pady = 0,command = lambda: addValues(string, ranged, toUpdate,yours,defensive))
            proceed.grid(row = 6,column = 0)
    #Setting up the defensive profile of the unit. Values are confirmed upon click of Next Page
    a = []
    bs = []
    ws = []
    s = []
    ap = []
    d = []
    setDefault()#skill strnegh ap dam, inputs 2-5
    input6.set("Name")
    input2.set("Toughness")
    input3.set("Armor Save")
    input4.set("Invulnerable Save")
    input5.set("Wounds Per Model")
    input7.set("Num. Models")
    intro.configure(text = "Please enter a name and Num. Models for this unit")
    intro.grid(row = 0, column = 2)
    inputB1.configure(textvariable = input6)
    inputB1.grid(row = 1, column = 0)
    inputB7.configure(textvariable = input7)
    inputB7.grid(row = 7, column = 0, pady = 0)
    #Add boolean here for if im doing a special case where I only want to add a defensive profile
    proceed.configure(text = "Next Page",pady = 0,command = lambda: addWeapon(string, yours))
    proceed.grid(row = 1, column = 5)

def pointer(pointer,pointed):#General purpose method to change general purpose pointers    
    print(f'setting {pointer} to {pointed}')
    pointer = pointed#Possibly could delete this and just assign the pointers manually, I'll see how many times I can use it and if it's worth
    print(pointer == pointed)
    print(pointer)
    #print(pointer.a)
    return pointer
def specialPointer(pointed):
    global goodPointer
    print(f'setting good {goodPointer} to {pointed}')
    goodPointer = pointed
    print(f'{goodPointer == pointed}, {goodPointer}')
    return goodPointer
def specialEvilPointer(pointed):
    global badPointer
    print(f'setting bad {badPointer} to {pointed}')
    badPointer = pointed
    print(f'{goodPointer == pointed}, {badPointer}')
#Combat phase consists of listing available units and available enemy targets(radio list). If you want to split-fire(shoot different weapons at different targets)
# then go through the selection part again. Initialized to no enemy targets, so will be a button that allows to add a new target profile.
def chooseUnits(dict,enemyDict,init = False,melee = False,final = False):
    cleanUp()
    intro.grid()
    intro.configure(text = "Choose from BOTH lists which unit is attacking and who, or create a target")
    button2.grid()
    button2.configure(text = "Add New Unit(Target)",pady = 0,command = lambda : addUnit("their",None,False,True))
    button2.grid(row = 5, column = 1)
    proceed.grid()
    proceed.configure(text = "Attack with selected units()", pady = 0, command = lambda : wrapper())
    button3 = tk.Button(root)
    if melee and final:button3.configure(text = "End Turn", command = lambda : chooseUnits(enemyDict,dict,True,False))
    elif final == False:button3.configure(text = "End Turn", command = lambda : chooseUnits(enemyDict,dict,True,melee,True))
    else:button3.configure(text = "End Turn", command = lambda : chooseUnits(dict,enemyDict,True,True,False))
    button3.grid(row = 7, column = 1)
    def wrapper():
        global activated
        activated[int(input1.get())] = True
        chooseWeapon(badPointer,goodPointer,melee)
    #Creates two radio buttons from your units and the enemy units, which when clicked will assign their respective pointers to them.
    #Upon clicking finalize or whatever I decide to name it, the computer will calculate combat based on the objects linked to those two pointers.
    #Note:Add protection for trying to add units with the same name
    i = 1
    for name in names.keys():
        
        Radiobutton(root, text = name,variable = input1,value = name,command = lambda : specialPointer(names[name])).grid(row = i, column = 0)
        i += 1
    i = 0
    for badName in enemyNames.keys():
        Radiobutton(root,text = badName, variable = input2, value = badName, command = lambda : specialEvilPointer(enemyNames[badName])).grid(row = i, column = 3)
        i += 1
def chooseWeapon(target,attacker):
    cleanUp()
    intro.grid()
    button2.grid_forget()
    intro.configure(text = "Choose from the available weapons which to attack with")
    intro.grid(row = 0, column = 0, pady = 0)
    i = 0
    range = True
    index = 0
    #badPointer = 0
    #possibility to not need specialPointer and just declare it again here.Maybe.....
    lethal = tk.BooleanVar()
    sust = tk.BooleanVar()
    dev = tk.BooleanVar()
    rapid = tk.BooleanVar()
    blast = tk.BooleanVar()
    critH = tk.BooleanVar()
    critW = tk.BooleanVar()
    plusS = tk.BooleanVar()
    plusH = tk.BooleanVar()
    plusStr = tk.BooleanVar()
    plusW = tk.BooleanVar()
    sDebf = tk.BooleanVar()
    hDebf = tk.BooleanVar()
    wDebf = tk.BooleanVar()
    cover = tk.BooleanVar()
    #I really really hate this whole section, basically undid all my work condensing other methods. Note to self, maybe create two lists,
    #one of tk.BooleanVar()s and then the other of the texts for the toggles. Then loop through those and pass each value of the list to the attack method
    #Unfortunately I don't think I can define the options in a loop like before, because I need to check each button simultaeneously
    button1 = tk.Checkbutton(root, text = "Lethal Hits", variable = lethal, onvalue = True, offvalue = False )
    buttonB = tk.Checkbutton(root, text = "Sustained Hits 1", variable = sust, onvalue = True, offvalue = False )
    buttonC = tk.Checkbutton(root, text = "Devastating Wounds", variable = dev, onvalue = True, offvalue = False )
    button4 = tk.Checkbutton(root, text = "Rapid Fire 1", variable = rapid, onvalue = True, offvalue = False )
    button5 = tk.Checkbutton(root, text = "Blast", variable = blast, onvalue = True, offvalue = False )
    #Possibly make radio button for crit hits 4? Not sure if that exists
    button6 = tk.Checkbutton(root, text = "Crit Hits 5+", variable = critH, onvalue = True, offvalue = False)
    button7 = tk.Checkbutton(root, text = "Crit Wounds 5+", variable = critW, onvalue = True, offvalue = False)
    button8 = tk.Checkbutton(root, text = "+1 to BS/WS", variable = plusS, onvalue = True, offvalue = False)
    button9 = tk.Checkbutton(root, text = "+1 to Hit", variable = plusH, onvalue = True, offvalue = False)
    button10 = tk.Checkbutton(root, text = "+1 to Strength", variable = plusStr, onvalue = True, offvalue = False)
    button11 = tk.Checkbutton(root, text = "+1 to Wound", variable = plusW, onvalue = True, offvalue = False)
    button12 = tk.Checkbutton(root, text = "-1 to BS/WS", variable = sDebf, onvalue = True, offvalue = False)
    button13 = tk.Checkbutton(root, text = "-1 to Hit",variable = hDebf, onvalue = True, offvalue = False)
    button14 = tk.Checkbutton(root, text = "-1 to Wound", variable = wDebf, onvalue = True, offvalue = False)
    button15 = tk.Checkbutton(root, text = "Has Cover", variable = cover, onvalue = True, offvalue = False)
    #Maybe turn this into a for loop, but then I'd still have to do the variable names. I'll look into it
    button1.grid(row = 1, column = 3)
    buttonB.grid(row = 2, column = 3)
    buttonC.grid(row = 3, column = 3)
    button4.grid(row = 4, column = 3)
    button5.grid(row = 5, column = 3)
    button6.grid(row = 6, column = 3)
    button7.grid(row = 7, column = 3)
    button8.grid(row = 8, column = 3)
    button9.grid(row = 9, column = 3)
    button10.grid(row = 10, column = 3)
    button11.grid(row = 11, column = 3)
    button12.grid(row = 1, column = 2)
    button13.grid(row = 2, column = 2)
    button14.grid(row = 3, column = 2)
    button15.grid(row = 4, column = 2)
    #indexes 0-4, defined below,. index 5 is crit hits on 5+, which I believe is the lowest it goes
    buffNames = ["Lethal Hits", "Sustained Hits 1", "Devastating Wounds", "Rapid Fire 1", "Blast"]
    #buffs = [False,False,False,False,False,False]
    while i < len(attacker.s):
        if range == True:
            #Idea is to set goodPointer to i and then have another button that will call the attack gunction with i, which will refer to a specific weapons specs
            Radiobutton(root,text = "Weapon " + str(i + 1), variable = input1, value = i, command = lambda: pointer(index, i)).grid(row = i + 1,column = 0, pady = 0)
            #Once i gets to be 1 larger than the len(bs), then it will be switched to 0 and going through the ws.Still look into combining them
        else:
            #Remember to use i % len(attacker.bs) when getting the ws so you can just use the same i for all
            Radiobutton(root, text = "Melee Weapon " + str(i % (len(attacker.bs)) + 1), variable = input1, command = lambda: pointer(index, i)).grid(row = i, column = 0, pady = 0)
        i += 1
        if i == len(attacker.bs):range == False
    proceed.grid()
    proceed.configure(text = "Attack", command = lambda: attack(target,attacker,index))
    proceed.grid(row = i + 1, column = 0, pady = 0)
    #Note that this method is ONLY for simulating the attacks and damage, choosing who you're attacking with and the target are separate. 
    #add radio list for buffs and debuffs
    #Idea to make this more efficient, call the objects and reference their stats. However, for like bs and ws that are in separate lists, one number wont work.
    #Possibly combine bs and ws into one list and have an internal boundary?
    #Actually, when selecting weapons, the radio list will call the relevant numbers so this doesnt matter
    #Possible attack modifications, these are PER INDIVIDUAL WEAPON, so 5 models with a BLAST weapon will add 5 extra attacks when attacking a unit of 5:
    #Lethal Hits:Hit rolls of 6 automatically wound
    #Sustained Hits x: Hit rolls of 6 add x extra hits to your total
    #Devastating Wounds:Wound rolls of 6 automatically wound
    #Rapid Fire x: Firing within half range adds x extra attacks
    #Blast: For every 5 models in the targeted unit, add 1 extra attack
def attack(target,attacker,index):
    print(target,attacker)
    print(attacker.a[index],attacker.m,attacker.a[index]*attacker.m)
    print(attacker.d[index])
    print(target.w)
    hits = rollDice((attacker.a[index]*attacker.m))
    print("Hit Roll")
    print(hits)
    #Possibly incorporate success measuring into rollDice?
    if index >= len(attacker.bs):
        wsBs = attacker.ws[index % len(attacker.bs)]
    else:wsBs = attacker.bs[index]
    sucH = len([x for x in hits if x >= wsBs])
    critSuccesses = len([x for x in hits if x == 6])
    #Rolling for wounds. Remember to add parameter/variable to allow for sustained hits and such
    wounds = rollDice(sucH)
    print("Wound Roll")
    print(wounds)
    if attacker.s[index] > 2 * target.t: woundMin = 2
    elif attacker.s[index] > target.t: woundMin = 3
    elif attacker.s[index] == target.t: woundMin = 4
    elif attacker.s[index] < target.t: woundMin = 5
    elif 2 * attacker.s[index] < target.t: woundMin = 6
    #note, add a variable to woundMin that is normally zero, but can be 1(or -1) depending on how I do it, to allow for +1 wound stratagems
    sucW = len([x for x in wounds if x >= woundMin])#Amount of dice that were able to successfully "wound" the target
    critSuccess = len([x for x in wounds if x == 6])#critical successes are those dice that land on 6 or in some cases 5. They are separate because they can activate special rules
    #Rolling saving throws. Add parameter for devastating wounds
    saves = rollDice(sucW)
    print("Saving Throw(s)")
    print(saves)
    if cover:
        if target.sv < 3 or target.sv - attacker.ap[index] < 3:hasCover = True
        else:hasCover = False
    else:hasCover = False
    failSaves = len([x for x in saves if x - attacker.ap[index]  + int(hasCover) < target.sv])#No critical saving throws(I think), and there's no reason to track them
    realFS = failSaves
    failSaves += critSuccesses * int(dev)
    realDev = critSuccesses * int(dev)
    expecDev = int(dev) * math.floor((expecW * (1 + int(critW5))/6))
    expecFail = math.floor(expecW * ((target.sv - attacker.ap[index] + int(hasCover))/6)) - expecDev
    #Formula for models killed is: models -= (hits /(math.ceil(wounds per model / damage per hit)) doing non-integer division to allow for damaged models and then also rounding up
    #doing integer division for the time being until i implement damaged models surviving
    killed = failSaves // math.ceil(target.w / attacker.d[index])
    target.m -= killed#yeah this should definitely be an object
    diceResults(hits, wounds, saves,sucH,sucW,failSaves,killed)

def diceResults(hits,wounds,saves,sucH,sucW,sucSV,kill):
    cleanUp()
    button2.grid_forget()
    label1 = tk.Label(root, text = "Rolled Hits:")
    hitList = tk.Label(root,text = repr(hits))
    label2 = tk.Label(root, text = "Rolled Wounds:")
    woundList = tk.Label(root, text = repr(wounds))
    label3 = tk.Label(root, text = "Enemy rolled Saves:")
    saveList = tk.Label(root, text = repr(saves))
    damageReport = tk.Label(root, text = "Models dead: " + str(kill))
    label4 = tk.Label(root, text = "Detailed Stats")
    totalH = tk.Label(root, text = "Total Attacks: " + str(len(hits)))
    expecHL = tk.Label(root, text = "Expected Hits: " + str(expecH) + ", " + str(expecExH) + " extra expected Sustained Hits, and " + str(expecLethal) + " expected Lethal Hits")
    realHL = tk.Label(root, text = "Real Hits: " + str(realH) + " and " + str(realExH) + " extra Sustained Hits, and " + str(realLethal) + " Lethal Hits")
    expecWL = tk.Label(root, text = "Expected Wounds: " + str(expecW)  + " and " + str(expecLethal) + " extra expected from Lethal Hits")
    realWL = tk.Label(root, text = "Real Wounds: " + str(len(wounds)) + " with " + str(realLethal) + " extra from Lethal Hits")
    expecFSL = tk.Label(root, text = "Expected Amount of Failed Saves: " + str(expecFail) + " and " + str(expecDev) + " expected Devastating Wounds")
    realFSL = tk.Label(root, text = "Real Failed Saves: " + str(realFS) + " and " + str(realDev) + " Devastating Wounds")
    #button2.configure(text = "End turn", command = lambda : chooseUnits(enemyNames,names))
    proceed.configure(text = "Next Unit",command = lambda: chooseUnits(names,enemyNames))#addUnit("their",badPointer,False))
    label1.grid(row = 1, column = 0, pady = 0)
    hitList.grid(row = 2, column = 0, pady = 0)
    label2.grid(row = 3, column = 0, pady = 0)
    woundList.grid(row = 4, column = 0, pady = 0)
    label3.grid(row = 5, column = 0, pady = 0)
    saveList.grid(row = 6, column = 0, pady = 0)
    intro.config(text=repr(sucSV))
    intro.grid()
    intro.grid(row = 7, column = 0, pady = 0)
    damageReport.grid( row = 8, column = 0, pady = 0)
    proceed.grid()
    proceed.grid( row = 9, column = 0, pady = 0)
    print(badPointer)
    button2.grid(row = 10, column = 3)
    label4.grid(row = 10, column = 0)
    totalH.grid(row = 11, column = 0)
    expecHL.grid(row = 12, column = 0)
    realHL.grid(row = 13, column = 0)
    expecWL.grid(row = 14, column = 0)
    realWL.grid(row = 15, column = 0)
    expecFSL.grid(row = 16, column = 0)
    realFSL.grid(row = 17, column = 0)
    #Go back to your units, and also mark the unit that was just activated as having been activated
    proceed.configure(text = "Next Unit",command = lambda: chooseUnits(names,enemyNames))#addUnit("their",badPointer,False))
    
#Create turn method that takes control of normal turn order
#Creating your units is done in startup, then shooting, charging, and fighting is done in the turn method.

#Turn method takes boolean of whose turn it is
def turn(yourTurn):
    if yourTurn == True:
        chooseUnits(names,enemyNames,True)

startUp()  
root.mainloop()