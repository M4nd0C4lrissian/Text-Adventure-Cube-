import random

class Enemy:
  def __init__(self, H, name, ap, ev, df):
    self.health = H
    self.name = name
    self.AP = ap
    self.EV = ev
    self.DF = df

  def get_stats(self):
    return (self.AP, self.EV, self.DF)

  def get_health(self):
    return self.health

  def get_name(self):
    return self.name

  def decr_health(self, damage):
    self.health -= damage

class Player:
  def __init__(self, H, cap, name, ap, ev, df):
    self.health = H
    self.inventory = []
    self.capacity = cap
    self.load = 0
    self.name = name
    self.AP = ap
    self.EV = ev
    self.DF = df
    self.weapon = Weapon("fists", 0, (0,0,0))

  def get_stats(self):
    return [self.AP, self.EV, self.DF]

  def get_health(self):
    return self.health

  def get_inventory(self):
    return self.inventory

  def get_name(self):
    return self.name

  def get_load(self):
    return self.load

  def decr_health(self, damage):
    self.health -= damage

  def pickup(self, item):
    w = item.get_weight()
    if(self.capacity < self.load + w): 
      print("Can't carry this. Try dropping something.")
      bool = True
      while bool:
        j = eval(input("Would you like to drop other items to make room? Press 0 if yes and 1 if no, then enter."))
        if j != 0 and j != 1:
          print("Please enter a valid option")
          continue
        if j == 0:
          s = ""
          for i in range(len(self.inventory)):
            it = self.inventory[i]
            s += str(i) + ": (" + it.get_name() + ", " + str(it.get_weight()) + "), "
          print(s)
          space_required = w - (self.capacity - self.load)
          print("You require " + str(space_required) + " more capacity to carry " + item.get_name())
          d = eval(input("Input the associated index of the item you wish to delete."))
          ##this while loop condition looks weird
          while len(self.inventory) != 0 and (d < 0  or d >= len(self.inventory)):  
            d = eval(input("Input the associated index of the item you wish to delete."))

          self.drop(d)
          space_required = w - (self.capacity - self.load)
          if space_required <= 0:
            self.inventory.append(item)
            self.load += w
            break

        else:
          bool = False

    else:
      self.inventory.append(item)
      self.load += w

  def drop(self, ind):
    if(ind >= 0 and ind < len(self.inventory)):
        item = self.inventory[ind]
        self.inventory.pop(ind)
        self.load -= item.get_weight()
    else:
      print("Item index does not exist")

  ##current item drop system won't account for stat changes like in this method
  def equip(self, w):
    player_stat = self.get_stats()
    cweapon_stat = self.weapon.get_stats()
    nweapon_stat = w.get_stats()
    for i in range(3):
      player_stat[i] += nweapon_stat[i] - cweapon_stat[i]

    self.weapon = w
    self.AP = player_stat[0]
    self.EV = player_stat[1]
    self.DF = player_stat[2]


class Item:

  def __init__(self, name, weight):
    self.name = name
    self.w = weight
    ##add AP buff and getter
  def get_name(self):
    return self.name

  def get_weight(self):
    return self.w

class Weapon(Item):
  def __init__(self, name, weight, stat_mods):
    self.name = name
    self.w = weight 
    self.s = stat_mods

  def get_stats(self):
    return self.s

##w = Weapon("weapon", 10, (4,4,4))
##print(w.get_weight())


## H, cap, name, ap, ev, df):
'''
p1 = Player(10, 12, "eamon", 2, 3, 4)

i1 = Item("sword", 2)
i2 = Item("swor3d", 5)
i3 = Item("Sword", 4)

items = [i1, i2, i3]

for i in range(3):
  print(p1.get_load())

  p1.pickup(items[i])

  l = p1.get_inventory()
  for j in range(len(l)):
    print(l[j].get_name() + ",")

p1.pickup(i3)
'''

class Battle: 

  def __init__(self, players, enemies):
    self.turn_q = []
    self.players = players
    self.enemies = enemies
    #######is_defeated list
    self.p = len(players)
    self.e = len(enemies)
    self.fill_q()
    self.battle_over = False ####battle_over boolean - set by battle_end()

  def fill_q(self):
    for i in range(5): 
      for j in range(self.p):
        self.turn_q.append(Turn(0, j))
      for k in range(self.e):
        self.turn_q.append(Turn(1, k)) 

  ##Assuming turn_q is not empty
  def pop_t(self):
    temp = self.turn_q[0]
    self.turn_q = self.turn_q[1:]
    return temp

  def take_turn(self):
    if len(self.turn_q) <= 0:
      self.fill_q()
    turn = self.pop_t()
    if turn.t == 0:
      if self.players[turn.who].get_health() <= 0:
        return
      self.player_go(turn.who)

    else:
      if self.enemies[turn.who].get_health() <= 0:
        return
      self.enemy_go(turn.who) 

    if self.p <= 0 or self.e <= 0:
      self.battle_end() ##to make 

  def display(self):
    print("\n" + "-----------------------------" + "\n")
    s = ""
    for i in range(len(self.enemies)):
      if self.enemies[i].get_health() <= 0:
        continue 
      s += ("(" + str(i) + " - Name: " + self.enemies[i].get_name() + ", HP: " + str(self.enemies[i].get_health()) + "), ")
    print(s)
    for j in range(len(self.players)):
      print("Hero Title: " + self.players[j].get_name() + ", HP: " + str(self.players[j].get_health()) + ", ")

  def player_go(self, p):
    self.display()

    while True:
      target = eval(input("Input the number index of the enemy you'd like to target: "))
      if target <= (self.e - 1): 
        break

    e_e = self.enemies[target].get_stats()[1]
    chance = random.randint(0,100)
    if e_e >= chance:
      print("The attack was dodged!")
      return

    ##need to handle case where enemy defense > player attack
    a_p = self.players[p].get_stats()[0]
    e_d = self.enemies[target].get_stats()[2]

    if e_d < a_p:
      self.enemies[target].decr_health(a_p - e_d) ##may need to add weapon buff in the future
    else:
      print("The attack was deflected!")

    if self.enemies[target].get_health() <= 0:
      self.e -= 1

  def battle_end(self):
    self.battle_over = True

  def enemy_go(self, e):
    temp = self.players.copy() 
    while True:
      m = 0
      for i in range(1, len(temp)):
        if temp[i].get_health() < temp[m].get_health():
          m = i
      if temp[m].get_health() <= 0:
        temp.pop(m)
        m = 0
      else:
        break 

    p_e = self.players[m].get_stats()[1]
    chance = random.randint(0,100)
    if p_e >= chance:
      print("The attack was dodged!")
      return

    p_d = self.players[m].get_stats()[2]
    e_a = self.enemies[e].get_stats()[0]

    if p_d < e_a:
      self.players[m].decr_health(e_a - p_d) ##had to switch this around
    else:
      print("The attack was deflected!")

    if self.players[m].get_health() <= 0:
      self.p -= 1
        
  
class Turn:
  def __init__(self, faction, actor):
    self.t = faction
    self.who = actor

##script1

name = input("What is you name, hero? \n")

p = Player(20, 10, name, 6, 12, 2)
sword = Weapon("Old Sword", 6, (3,0,0))
p.pickup(sword)
p.equip(sword)

print("You awake, delirious and in an unfamiliar space. Large trees unlike any you'v ever seen tower above you and block out the sun; it is dark. You feel around in the darkness and find your sword laying next to you. How you got in this position eludes you, but the stinging pain on the back of your head gives you some idea. 'I have to find my way back home', you say. Suddenly, a rustling in the bushes can be heard behind you. What do you do?" + "\n")

while True:
  c = eval(input("0 : Turn to face it, sword raised, 1 : Run as fast as you can in the other direction. \n"))
  if c == 0:
    b = Battle([p], [Enemy(12, "Goblin Veteran", 5, 6, 4), Enemy(6, "Goblin Scout", 3, 22, 1)])
    while not(b.battle_over):
      b.take_turn()
  elif c != 1:
    continue
  else:
    ran = random.randint(0,100)
    if ran > p.get_stats()[1]:
      print("Running with your fatigue may not have been the best idea; you fall and injure your leg, taking 5 damage.")
    else: 
      print("You get away safely, though your speed may betray your sight, as in the darkness of the forest you missed a vast cliffside and ran right off of it. In an instant you realize your mistake and attempt to jam your sword into the cliffside, but must first acquire it from your scabbard, which requires deft hands. Your dexterity and the gods hold your fate now.")

      ran = random.randint(0,30)
      if ran > p.get_stats()[1]:
        print("Running with your fatigue may not have been the best idea; you fall and injure your leg, taking 5 damage.")
