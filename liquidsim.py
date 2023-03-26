#okay idea:
#yoink angrydoge idea
#use background colors
#make blocks placeable (Selector is an "S"?)
#etc

#TODO
#REMOVE ALL WATER ON A SURFACE WHEN THE SOURCE ABOVE IT IS REMOVED, BUT ALL AT THE SAME TIME
#test it lol

from threading import Thread
import time,os,random



waterodds = 1/5 #this will spawn about 6 water everytime (30 slots on each row) can easily be changed just saying (max is 1 though)

#for random simulation
watergenodds = 1/30 #1/30 = usually about 5
wallodds = 1/10 #1/10 = usually about 15



if os.name=='nt':
  import msvcrt
else:
  from getkey import getkey as Getkey

somekeys = {'H': 'up', 'P': 'down', 'K': 'left', 'M': 'right', '\\r': 'enter', '\\x08': 'backspace','\\xe0':'yippe yay','\\t':'tab'}
def getkey():
    return (h if (h:=str(msvcrt.getch())[2:-1]) not in somekeys.keys() or h in ['P','H','K','M'] else somekeys[h] if h!='\\xe0' else somekeys[str(msvcrt.getch())[2:-1]]).lower() if os.name=='nt' else Getkey.lower()
thing=list('''
------------------------------
------------------------------
------------------------------
------------------------------
------------------------------
------------------------------
------------------------------
------------------------------
------------------------------
------------------------------
------------------------------
''') #0-30?
#first make rainfall (wait what if the color changed the lower it went :0)
colors={
  'G':"\033[48;5;34m", #water generator, add later lol
  'R':"\033[48;5;26m", #water
  'W':"\033[48;5;239m", #wall
}
print('\033[?25l')
def c():
    os.system('cls')
def upscreen():
  print("\033[H",end="")
  for ind,i in enumerate(thing):
    if ind in [0,len(thing)-1]:
        print("|",end='')
        continue
    print(((" " if i!='\n' and ind!=spos else '|\n|' if i=='\n' else '') if i not in colors.keys() else colors[i])+('\033[38;5;4mS' if ind==spos else "" if i in ['-','\n'] else " "),end='\033[0m')
def selecting():
  global spos,thing,upit
  spos=1
  while True:
    h=getkey()
    if h=='c':
      c()
    elif h=='k':
      generate(True)
    elif h=='n':
      thing=list('\n'+("------------------------------\n"*11))
    elif h=='j':
      print(spos)
    elif h in ['1','2','0']:#wall, generator, delete
      thing[(spos if thing[spos]!='\n' else spos+1)]='W' if h=='1' else 'G' if h=='2' else '-'
    elif h in ['w','a','s','d']:
      spos+=((-1 if spos>1 else 0) if h=='a' else (1 if spos<=339 else 0) if h=='d' else (31 if spos<=309 else 0) if h=='s' else (-31 if spos>30 else 0))
    else:
      continue
    upit=True
    if spos%31==0:
      spos+=(-1 if h=='a' else 1)
def generate(OVER=False):
  #randomly generate water first
  global thing
  thing=list((('\n'+('-'*30))*11)+'\n') #reset
  for i in range(1,31):
    if random.randint(0,(1/waterodds))==0:
      thing[i]='R'
  if not select or OVER:
    for i in range(91,270):
      if random.randint(0,1/wallodds)==0: #makes walls more probable with elifs
        j='W' 
      elif random.randint(0,1/watergenodds)==0:
        j='G'
      else:
        continue
      thing[i]=j if thing[i]!='\n' else '\n'
  
if input("Pick a mode:\nSay 'S' to play selecting mode:\n\tUse WASD to move the S selector\n\t1 to place a wall\n\t2 to place a water generator\n\t0 to delete\n\tK to get a random generation\n\tC to reset screen (fix weirdness)\n\tN to nuke entire screen\n\nAnything else leads to random generation of walls.\n\n>").lower()=='s':
  select=True
  newerthannew=Thread(target=selecting)
  newerthannew.start()
else:
  select=False
  spos=378259337
      
c()
generate() #yay

def iswat(num):
  return thing[num]=='R' or num-1%30==0
upit=True
#main update screen loop/water update
goods = ['R','G'] #for checking if a water should remain 
walls = ['G','W'] #youll never guessed what these are
while True:
  upscreen()
  if select:
    for i in range(6):
      if upit:
        upscreen()
        upit=False
      time.sleep(.1)
  else:
    time.sleep(.5)
  #water
  li=[]
  checkthing=True
  for ind,i in enumerate(thing):
    if ind in li or i in ['-','W','\n'] or ind>309: #if the character has already been adjusted or its useless or its in the bottom row
      if ind>309 and thing[ind]=='R' and thing[ind-31] not in goods:
        thing[ind]='-'
      continue
    if i=='R': #if in top, or top is water, or on ground and surrunded by water, OR on side water+wall underneath that
      #if this passes, its good to survive/reproduce i guess
      if (ind<31 or thing[ind-31] in goods) or (thing[ind+31] in walls and iswat(ind-1) and iswat(ind+1)) or ((iswat(ind-1) and thing[ind+30] in walls) or (iswat(ind+1) and thing[ind+32] in walls)): 
        if thing[ind-31] not in goods and checkthing and ind>30 and thing[ind+31] in walls:
          goodie=False
          lisT=[ind]
          for I in [-1,1]: #forwards/back
            count=1
            while iswat(ind+(count*I)) and thing[ind+31+(count*I)] in walls:
              if thing[ind-31+(count*I)] in goods:
                goodie=True
                break
              lisT.append(ind+(count*I))
              count+=1
          if not goodie:
            for E in lisT:
              thing[E]='-'
          checkthing=False
        if thing[ind+31]=='-':
          thing[ind+31]='R'
          li.append(ind+31)
        elif thing[ind+31]!='R':
          for i2 in [ind+1,ind-1]:
            if thing[i2]=='-':
              thing[i2]='R'
              li.append(i2)
              break
        if thing[ind+31] not in walls:
          checkthing=True
      else:
        thing[ind]='-'
        li.append(ind+31)
    elif i=='G' and ind<=309:
      if thing[ind+31]=='-':
        thing[ind+31]='R'
              