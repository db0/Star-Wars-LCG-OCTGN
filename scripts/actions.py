    # Python Scripts for the Star Wars LCG definition for OCTGN
    # Copyright (C) 2012  Konstantine Thoukydides & JMCB

    # This python script is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this script.  If not, see <http://www.gnu.org/licenses/>.

###==================================================File Contents==================================================###
# This file contains the basic table actions in SW LCG. They are the ones the player calls when they use an action in the menu.
# Many of them are also called from the autoscripts.
###=================================================================================================================###

import re
#---------------------------------------------------------------------------
# Global variables
#---------------------------------------------------------------------------

Side = None # The side of the player. 
Affiliation = None
opponent = None # A variable holding the player object of our opponent.
SetupPhase = False

#---------------------------------------------------------------------------
# Phases
#---------------------------------------------------------------------------

def showCurrentPhase(): # Just say a nice notification about which phase you're on.
   notify(phases[num(me.getGlobalVariable('Phase'))].format(me))
   
def nextPhase(group, x = 0, y = 0):  
# Function to take you to the next phase. 
   mute()
   phase = num(me.getGlobalVariable('Phase'))
   if phase == 6: 
      me.setGlobalVariable('Phase','-1') # In case we're on the last phase (Force), we end our turn.
      opponent.setGlobalVariable('Phase','0') # Phase 0 means they're ready to start their turn
      notify("{} has ended their turn".format(me))
      return
   elif phase < 0:
      if not confirm("Your opponent has not finished their turn yet. Are you sure you want to continue?"): return
      me.setGlobalVariable('Phase','1')
      opponent.setGlobalVariable('Phase','-1')
   else: me.setGlobalVariable('Phase',str(phase + 1)) # Otherwise, just move up one phase
   showCurrentPhase()

def goToBalance(group, x = 0, y = 0): # Go directly to the Balance phase
   mute()
   me.setGlobalVariable('Phase','1')
   showCurrentPhase()
   clearHandRanks() # Clear the Hand Ranks, in case one is leftover from last High Noon.

def goToRefresh(group, x = 0, y = 0): # Go directly to the Refresh phase
   mute()
   me.setGlobalVariable('Phase','2')
   showCurrentPhase()

def goToDraw(group, x = 0, y = 0): # Go directly to the Draw phase
   mute()
   me.setGlobalVariable('Phase','3')
   showCurrentPhase()

def goToDeployment(group, x = 0, y = 0): # Go directly to the Deployment phase
   mute()
   me.setGlobalVariable('Phase','4')
   showCurrentPhase()   
    
def goToConflict(group, x = 0, y = 0): # Go directly to the Conflict phase
   mute()
   me.setGlobalVariable('Phase','5')
   showCurrentPhase()   

def goToForce(group, x = 0, y = 0): # Go directly to the Force phase
   mute()
   me.setGlobalVariable('Phase','6')
   showCurrentPhase()   
#---------------------------------------------------------------------------
# Rest
#---------------------------------------------------------------------------

def gameSetup(group, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> gameSetup(){}".format(extraASDebug())) #Debug
   global Side, Affiliation, SetupPhase, opponent
   mute()
   deck = me.piles['Command Deck']
   objectives = me.piles['Objective Deck']
   #if not startupMsg: fetchCardScripts() # We only download the scripts at the very first setup of each play session.
   #versionCheck()
   if SetupPhase:
      if ofwhom('ofOpponent') == me and len(players) > 1: # If the other player hasn't chosen their side yet, it means they haven't yet tried to setup their table, so we abort
         whisper("Please wait until your opponent has drawn their objectives before proceeding")
         return
      if len(me.hand) > 3 and not confirm("Have you moved one of your 4 objectives to the bottom of your objectives deck?"): return
      for card in me.hand:
         if card.Type != 'Objective': 
            whisper(":::Warning::: You are not supposed to have any non-Objective cards in your hand at this point")
            card.moveToBottom(deck)
            continue
         else: storeObjective(card)
      shuffle(deck)
      drawMany(deck, 6, silent = True)
      opponent = ofwhom('ofOpponent') # Setting a variable to quickly have the opponent's object when we need it.
      notify("{} has played their objectives and drawn their starting commands".format(me))
      SetupPhase = False
   else: # This choice is only for a new game.
      if Side and Affiliation and not confirm("Are you sure you want to setup for a new game? (This action should only be done after a table reset)"): return
      Side = None
      Affiliation = None
      SetupPhase = True
      if not table.isTwoSided() and not confirm(":::WARNING::: This game is designed to be played on a two-sided table. Things will be extremely uncomfortable otherwise!! Please start a new game and makde sure the  the appropriate button is checked. Are you sure you want to continue?"): return
      chooseSide()
      if debugVerbosity >= 5: confirm("Checking Deck")
      if len(deck) == 0:
         whisper ("Please load a deck first!")
         return
      if debugVerbosity >= 5: confirm("Reseting Variables")
      #resetAll()
      if debugVerbosity >= 5: confirm("Placing Identity")
      for card in me.hand:
         if card.Type != 'Affiliation': 
            whisper(":::Warning::: You are not supposed to have any non-Affiliation cards in your hand when you start the game")
            if card.Type == 'Objective': card.moveToBottom(objectives)
            else: card.moveToBottom(deck)
            continue
         else: 
            Side = card.Side
            storeSpecial(card)
            me.setGlobalVariable('Side', Side)
            Affiliation = card
      if not Side: 
         confirm("You need to have your Affiliation card in your hand when you try to setup the game. If you have it in your deck, please look for it and put it in your hand before running this function again")
         return
      if debugVerbosity >= 5: confirm("Placing Affiliation")
      Affiliation.moveToTable(playerside * -400, playerside * 20)
      rnd(1,10)  # Allow time for the affiliation to be recognised
      notify("{} is representing the {}.".format(me,Affiliation))
      if debugVerbosity >= 5: confirm("Shuffling Decks")
      shuffle(objectives)
      if debugVerbosity >= 5: confirm("Drawing 4 Objectives")
      drawMany(objectives, 4, silent = True)
      notify("{} is choosing their objectives.".format(me))
      whisper(":::ATTENTION::: Once both players have discarded their 4th objective, press Ctrl+Shift+S to place your objectives on the table and draw your starting hand.")
      if debugVerbosity >= 5: confirm("Reshuffling Deck")
      shuffle(objectives) # And another one just to be sure
      shuffle(deck)
   
def refreshAll(group, x = 0, y = 0):
	mute()
	notify("{} untaps all his cards".format(me))
	for card in group: 
		if card.controller == me:
			card.orientation &= ~Rot90			
			
def clearAll(group, x = 0, y = 0):
    notify("{} clears all targets and combat.".format(me))
    for card in group:
		if card.controller == me:
			card.target(False)
			card.highlight = None

def focus(card, x = 0, y = 0):
    mute()
    card.orientation ^= Rot90
    if card.orientation & Rot90 == Rot90:
		notify('{} taps {}'.format(me, card))
    else:
        notify('{} untaps {}'.format(me, card))
		  

def handDiscard(card):
   if debugVerbosity >= 1: notify(">>> handDiscard(){}".format(extraASDebug())) #Debug
   mute()
   if card.Type == "Objective": 
      card.moveToBottom(me.piles['Objective Deck']) # This should only happen during the game setup
      notify("{} chose their 3 starting objectives.".format(me))
   else:
      card.moveTo(me.piles['Discard Pile'])
      notify("{} discards {}".format(me,card))
      
def discard(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> discard(){}".format(extraASDebug())) #Debug
   mute()
   if card.Type == "Objective":
      if card.owner == me:
         if debugVerbosity >= 2: notify("About to score objective")
         card.moveTo(opponent.piles['Victory Pile']) # Objectives are won by the opponent
         opponent.counters['Objectives Destroyed'].value += 1
         if Side == 'Light': 
            modifyDial(opponent.counters['Destroyed Objectives'].value)
            notify("{} thwarts {}. The Death Star Dial advances by {}".format(opponent,card,opponent.counters['Objectives Destroyed'].value))
         else: notify("{} thwarts {}.".format(opponent,card))
      else:
         card.moveTo(me.piles['Victory Pile']) # Objectives are won by the opponent
         notify("{} thwarts {}.".format(me,card))
         me.counters['Objectives Destroyed'].value += 1
         if Side == 'Dark': 
            modifyDial(opponent.counters['Destroyed Objectives'].value)
            notify("{} thwarts {}. The Death Star Dial advances by {}".format(me,card,me.counters['Objectives Destroyed'].value))
         else: notify("{} thwarts {}.".format(me,card))
   elif card.Type == "Affiliation": whisper("This isn't the card you're looking for...")
   else:
      card.moveTo(card.owner.piles['Discard Pile'])
      notify("{} discards {}".format(me,card))

def modifyDial(value):
   for player in players: player.counters['Death Star Dial'].value += value
   
def play(card, x = 0, y = 0):
	mute()
	src = card.group
	card.moveToTable(0, 0)
	notify("{} plays {} from their {}.".format(me, card, src.name))

def mulligan(group):
    mute()
    newCount = len(group) - 1
    if newCount < 0: return
    if not confirm("Mulligan down to %i ?" % newCount): return
    notify("{} mulligans down to {}".format(me, newCount))
    librarycount = len(me.piles["Life Deck"])
    for card in group:
        n = rnd(0, librarycount)
        card.moveTo(me.piles["Life Deck"], n)
    me.piles["Life Deck"].shuffle()
    for card in me.piles["Life Deck"].top(newCount):
        card.moveTo(me.hand)

def randomDiscard(group):
	mute()
	card = group.random()
	if card == None: return
	notify("{} randomly discards {}.".format(me,card.name))
	card.moveTo(me.piles['Discard Pile'])

def draw(group, x = 0, y = 0):
	if len(group) == 0: return
	mute()
	group[0].moveTo(me.hand)
	notify("{} draws a card.".format(me))

def drawMany(group, count = None, destination = None, silent = False):
   if debugVerbosity >= 1: notify(">>> drawMany(){}".format(extraASDebug())) #Debug
   if debugVerbosity >= 2: notify("source: {}".format(group.name))
   if debugVerbosity >= 2 and destination: notify("destination: {}".format(destination.name))
   mute()
   if destination == None: destination = me.hand
   SSize = len(group)
   if SSize == 0: return 0
   if count == None: count = askInteger("Draw how many cards?", 5)
   if count == None: return 0
   if count > SSize : 
      count = SSize
      whisper("You do not have enough cards in your deck to complete this action. Will draw as many as possible")
   for c in group.top(count): 
      c.moveTo(destination)
   if not silent: notify("{} draws {} cards.".format(me, count))
   if debugVerbosity >= 3: notify("<<< drawMany() with return: {}".format(count))
   return count

def drawBottom(group, x = 0, y = 0):
	if len(group) == 0: return
	mute()
	group.bottom().moveTo(me.hand)
	notify("{} draws a card from the bottom.".format(me))

def shuffle(group):
	group.shuffle()
	
def addResource(card, x = 0, y = 0):
    mute()
    notify("{} adds a Resource to {}.".format(me, card))
    card.markers[Resource] += 1
    
def addDamage(card, x = 0, y = 0):
    mute()
    notify("{} adds a Damage to {}.".format(me, card))
    card.markers[Damage] += 1    
    
def addShield(card, x = 0, y = 0):
    mute()
    notify("{} adds a Shield to {}.".format(me, card))
    card.markers[Shield] += 1        

def subResource(card, x = 0, y = 0):
    subToken(card, Resource)

def subDamage(card, x = 0, y = 0):
    subToken(card, Damage)

def subShield(card, x = 0, y = 0):
    subToken(card, Shield)

def subToken(card, tokenType):
    mute()
    notify("{} removes a {} from {}.".format(me, tokenType[0], card))
    card.markers[tokenType] -= 1	