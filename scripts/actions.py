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
unpaidCard = None # A variable that holds the card object of a card that has not been paid yet, for ease of find.
edgeCount = 0 # How many edge cards the player has played per engagement.
edgeRevealed = False # Remembers if the player has revealed their edge cards yet or not.

#---------------------------------------------------------------------------
# Phases
#---------------------------------------------------------------------------

def showCurrentPhase(): # Just say a nice notification about which phase you're on.
   notify(phases[num(me.getGlobalVariable('Phase'))].format(me))
   
def nextPhase(group, x = 0, y = 0):  
# Function to take you to the next phase. 
   mute()
   phase = num(me.getGlobalVariable('Phase'))
   if getGlobalVariable('Engaged Objective') != 'None': finishEngagement()
   if phase == 6: 
      me.setGlobalVariable('Phase','-1') # In case we're on the last phase (Force), we end our turn.
      opponent.setGlobalVariable('Phase','0') # Phase 0 means they're ready to start their turn
      notify("{} has ended their turn".format(me))
      return
   elif phase < 0:
      if not confirm("Your opponent has not finished their turn yet. Are you sure you want to continue?"): return
      me.setGlobalVariable('Phase','1')
      opponent.setGlobalVariable('Phase','-1')
   else: 
      phase += 1
      me.setGlobalVariable('Phase',str(phase)) # Otherwise, just move up one phase
   if phase == 1: goToBalance()
   elif phase == 2: goToRefresh()
   elif phase == 3: goToDraw()
   elif phase == 4: goToDeployment()
   elif phase == 5: goToConflict()
   elif phase == 6: goToForce()

def goToBalance(group = table, x = 0, y = 0): # Go directly to the Balance phase
   if debugVerbosity >= 1: notify(">>> goToBalance(){}".format(extraASDebug())) #Debug
   mute()
   me.setGlobalVariable('Phase','1')
   showCurrentPhase()
   BotD = getSpecial('BotD')
   if Side == 'Dark': 
      if BotD.isAlternateImage:
         modifyDial(2)
         notify(":> The Force is with the Dark Side! The Death Star dial advances by 2")
      else:
         modifyDial(1)
         notify(":> The Death Star dial advances by 1")
   else:
      if not BotD.isAlternateImage:
         opponentObjectives = eval(opponent.getGlobalVariable('currentObjectives'))
         objectiveList = []
         for objectve_ID in opponentObjectives:
            objective = Card(objectve_ID)
            objectiveList.append(objective.name)
         choice = SingleChoice("The Balance of the Force is in your favour. Choose one Dark Side objective to damage", objectiveList, type = 'radio', default = 0)
         chosenObj = Card(opponentObjectives[choice])
         chosenObj.markers[mdict['Damage']] += 1
         notify(":> The Force is with the Light Side! The rebel forces press the advantage and damage {}".format(chosenObj))      

def goToRefresh(group = table, x = 0, y = 0): # Go directly to the Refresh phase
   if debugVerbosity >= 1: notify(">>> goToRefresh(){}".format(extraASDebug())) #Debug
   mute()
   me.setGlobalVariable('Phase','2')
   showCurrentPhase()
   for card in table:
      if card.owner == me and card.controller == me and card.highlight != CapturedColor:
         if card.markers[mdict['Focus']] and card.markers[mdict['Focus']] > 0: 
            card.markers[mdict['Focus']] -=1
            if re.search(r'Elite.', card.Text) and card.markers[mdict['Focus']] > 0: 
               card.markers[mdict['Focus']] -=1 # Cards with the Elite text, remove an extra focus during refresh.
         if card.markers[mdict['Shield']] and card.markers[mdict['Shield']] > 0: 
            card.markers[mdict['Shield']] = 0
   currentObjectives = eval(me.getGlobalVariable('currentObjectives'))
   destroyedObjectives = eval(getGlobalVariable('destroyedObjectives'))
   for card_id in destroyedObjectives: 
      try: currentObjectives.remove(card_id) # Removing destroyed objectives before checking.
      except ValueError: pass 
   while len(currentObjectives) < 3:
      card = me.piles['Objective Deck'].top()
      storeObjective(card)
      currentObjectives = eval(me.getGlobalVariable('currentObjectives')) # We don't need to clear destroyed objectives anymore, since that is taken care of during storeObjective()
   notify(":> {} refreshed all their cards".format(me))   

def goToDraw(group = table, x = 0, y = 0): # Go directly to the Draw phase
   if debugVerbosity >= 1: notify(">>> goToDraw(){}".format(extraASDebug())) #Debug
   mute()
   me.setGlobalVariable('Phase','3')
   showCurrentPhase()
   if len(me.hand) == 0: refillHand()
   elif not confirm("Do you wish to discard a card before refilling your hand?\
                \n\n(if you press yes, discard your card and then press Ctrl+R to refill)"):
      refillHand()
   
def goToDeployment(group = table, x = 0, y = 0): # Go directly to the Deployment phase
   if debugVerbosity >= 1: notify(">>> goToDeployment(){}".format(extraASDebug())) #Debug
   mute()
   me.setGlobalVariable('Phase','4')
   showCurrentPhase()   
   
def goToConflict(group = table, x = 0, y = 0): # Go directly to the Conflict phase
   if debugVerbosity >= 1: notify(">>> goToConflict(){}".format(extraASDebug())) #Debug
   mute()
   me.setGlobalVariable('Phase','5')
   showCurrentPhase()   

def goToForce(group = table, x = 0, y = 0): # Go directly to the Force phase
   if debugVerbosity >= 1: notify(">>> goToForce(){}".format(extraASDebug())) #Debug
   mute()
   if getGlobalVariable('Engaged Objective') != 'None': finishEngagement() # If the playes jump to the force phase after engagement, we make sure we clear the engagement.
   me.setGlobalVariable('Phase','6')
   showCurrentPhase()
   whisper(":::ATTENTION::: Once you've committed all the units you want to the force, press Ctrl+F6 to resolve the force struggle")

def resolveForceStruggle(group = table, x = 0, y = 0): # Calculate Force Struggle
   mute()
   myStruggleTotal = 0
   opponentStruggleTotal = 0
   if Side == 'Light': 
      commitColor = LightForceColor
      commitOpponent = DarkForceColor
   else: 
      commitColor = DarkForceColor
      commitOpponent = LightForceColor
   if debugVerbosity >= 2: notify("Counting my committed cards") #Debug
   commitedCards = [c for c in table if c.controller == me and c.highlight == commitColor]
   if debugVerbosity >= 2: notify("About to loop") #Debug
   for card in commitedCards:
      try: 
         if card.markers[mdict['Focus']] == 0: myStruggleTotal += num(card.Force)
      except: myStruggleTotal += num(card.Force) # If there's an exception, it means the card didn't ever have a focus marker
   if debugVerbosity >= 2: notify("Counting my opponents cards") #Debug
   opponentCommitedCards  = [c for c in table if c.controller == opponent and c.highlight == commitOpponent]
   for card in opponentCommitedCards:
      try: 
         if card.markers[mdict['Focus']] == 0: opponentStruggleTotal += num(card.Force)
      except: opponentStruggleTotal += num(card.Force) # If there's an exception, it means the card didn't ever have a focus marker
   if debugVerbosity >= 2: notify("Checking Struggle") #Debug
   BotD = getSpecial('BotD')
   if myStruggleTotal - opponentStruggleTotal > 0: 
      if debugVerbosity >= 2: notify("struggleTotal Positive") #Debug
      if (Side == 'Light' and BotD.isAlternateImage) or (Side == 'Dark' and not BotD.isAlternateImage):
         if debugVerbosity >= 2: notify("About to flip BotD due to my victory") #Debug
         BotD.switchImage
         x,y = Affiliation.position
         if debugVerbosity >= 2: notify("My Affiliation is {} at position {} {}".format(Affiliation, x,y,)) #Debug
         BotD.moveToTable(x - (playerside * 70), y)
         notify(":> The force struggle tips the balance of the force towards the {} side ({}: {} - {}: {})".format(Side,me,myStruggleTotal,opponent,opponentStruggleTotal))
   elif myStruggleTotal - opponentStruggleTotal < 0: 
      if debugVerbosity >= 2: notify("struggleTotal Negative") #Debug
      if (Side == 'Light' and not BotD.isAlternateImage) or (Side == 'Dark' and BotD.isAlternateImage):
         if debugVerbosity >= 2: notify("About to flip BotD due to my opponent's victory") #Debug
         BotD.switchImage
         opponentAffiliation = getSpecial('Affiliation',opponent)
         x,y = opponentAffiliation.position
         if debugVerbosity >= 2: notify("Opponent Affiliation is {} at position {} {}".format(opponentAffiliation, x,y,)) #Debug
         BotD.moveToTable(x - (playerside * 70), y)
         notify(":> The force struggle tips the balance of the force towards the {} side ({}: {} - {}: {})".format(opponent.getGlobalVariable('Side'),me,myStruggleTotal,opponent,opponentStruggleTotal))
   if debugVerbosity >= 3: notify("<<< resolveForceStruggle()") #Debug
         
def engageTarget(group = table, x = 0, y = 0): # Start an Engagement Phase
   if debugVerbosity >= 1: notify(">>> engageTarget(){}".format(extraASDebug())) #Debug
   mute()
   if me.getGlobalVariable('Phase') != '5' and not confirm("You need to be in the conflict phase before you can engage an objective. Bypass?"):
      return
   if getGlobalVariable('Engaged Objective') != 'None': finishEngagement() 
   if debugVerbosity >= 2: notify("About to find targeted objectives.") #Debug
   cardList = [c for c in table if c.Type == 'Objective' and c.targetedBy and c.targetedBy == me and c.owner == opponent]
   if debugVerbosity >= 2: notify("About to count found objectives list. List is {}".format(cardList)) #Debug
   if len(cardList) == 0: 
      whisper("You need to target an opposing Objective to start an Engagement")
      return
   else: targetObjective = cardList[0]
   targetObjective.highlight = DefendColor
   if debugVerbosity >= 2: notify("About set the global variable") #Debug
   setGlobalVariable('Engaged Objective',str(targetObjective._id))
   if debugVerbosity >= 2: notify("About to announce") #Debug
   notify("{} forces have engaged {}'s {}".format(me,targetObjective.owner, targetObjective))
   rnd(1,10)
   whisper(":::NOTE::: You can now start selecting engagement participants by double-clicking on them")
   if debugVerbosity >= 3: notify("<<< engageTarget()") #Debug
   
def finishEngagement():
   if debugVerbosity >= 1: notify(">>> finishEngagement(){}".format(extraASDebug())) #Debug
   for card in table:
      if card.orientation == Rot90: card.orientation = Rot0
      if card.highlight == DefendColor: card.highlight = None
   notify("The engagement at {} is finished".format(Card(num(getGlobalVariable('Engaged Objective')))))
   setGlobalVariable('Engaged Objective','None')
   for card in table: # We get rid of all the Edge cards at the end of an engagement in case the player hasn't done so already.
      if card.owner == me and card.highlight == EdgeColor: discard(card)
   clearEdgeMarker() # We clear the edge, in case another player's affiliation card had it
   if debugVerbosity >= 3: notify("<<< finishEngagement()") #Debug  
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
      if not ofwhom('ofOpponent') and len(players) > 1: # If the other player hasn't chosen their side yet, it means they haven't yet tried to setup their table, so we abort
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
      if Side == 'Dark': me.setGlobalVariable('Phase','0') # We now allow the dark side to start
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
      Affiliation.moveToTable(playerside * -400, (playerside * 20) + yaxisMove(Affiliation))
      if Side == 'Dark': #We create the balance of the force card during the dark side's setup, to avoid duplicates.
         BotD = table.create("e31c2ba8-3ffc-4029-94fd-5f98ee0d78cc", 0, 0, 1, True)
         BotD.moveToTable(playerside * -470, (playerside * 20) + yaxisMove(Affiliation)) # move it next to the affiliation card for now.
         setGlobalVariable('Balance of the Force', str(BotD._id))
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

def defaultAction(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> defaultAction(){}".format(extraASDebug())) #Debug
   mute()
   if card.highlight == EdgeColor: 
      if card.isFaceUp: 
         if card.Type == 'Fate': whisper(":::ATTENTION::: No fate card automation yet I'm afraid :-(\nPlease do things manually for now.")
         else: revealEdge()
      else: revealEdge()
   elif card.highlight == UnpaidColor: purchaseCard(card)
   elif num(card.Resources) > 0 and findUnpaidCard(): 
      if debugVerbosity >= 2: notify("Card has resources") # Debug
      generate(card)
   elif card.Type == 'Unit' and getGlobalVariable('Engaged Objective') != 'None':
      if debugVerbosity >= 2: notify("Card is Unit and it's engagement time") # Debug
      if card.orientation == Rot0: participate(card)
      else: strike(card)
   else: whisper(":::ERROR::: There is nothing to do with this card at this moment!")
   if debugVerbosity >= 3: notify("<<< defaultAction()") #Debug
     
def strike(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> strike(){}".format(extraASDebug())) #Debug
   mute()
   if card.Type != 'Unit': 
      whisper(":::ERROR::: Only units may perform strikes")
      return
   if (card.markers[mdict['Focus']]
         and card.markers[mdict['Focus']] >= 1
         and not confirm("Unit is already exhausted. Bypass?")):
      return 
   notify("{} strikes with {}.".format(me, card))
   card.markers[mdict['Focus']] += 1
   if card.highlight == LightForceColor or card.highlight == DarkForceColor: card.markers[mdict['Focus']] += 1
   if debugVerbosity >= 3: notify("<<< strike()") #Debug
		  
def participate(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> participate(){}".format(extraASDebug())) #Debug
   mute()
   if card.Type != 'Unit': 
      whisper(":::ERROR::: Only units may participate in engagements")
      return
   if (card.markers[mdict['Focus']]
         and card.markers[mdict['Focus']] >= 1
         and not confirm("Unit is not ready. Bypass?")):
      return 
   notify("{} selects {} as an engagement participant.".format(me, card))
   card.orientation = Rot90
   if debugVerbosity >= 3: notify("<<< participate()") #Debug

def generate(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> generate(){}".format(extraASDebug())) #Debug
   mute()
   unpaidC = findUnpaidCard()
   if not unpaidC: 
      whisper(":::ERROR::: You are not attempting to pay for a card or effect. ABORTING!")
      return
   if (card.markers[mdict['Focus']]
         and card.markers[mdict['Focus']] >= 1
         and not confirm("Card is already exhausted. Bypass?")):
      return 
   if num(card.Resources) == 0: 
      whisper("Resources, this card produces not!")
      return
   elif num(card.Resources) > 1: 
      count = askInteger("Card can generate up to {} resources. How many do you want to produce?".format(card.Resources), 1)
      if not count: return # If the player closed the window or put 0, do nothing.
      while count > num(card.Resources):
         count = askInteger(":::ERROR::: This card cannot generate so many resources.\
                         \n\nPlease input again how many resources to produce (Max {})".format(card.Resources), 1)
         if not count: return # If the player closed the window or put 0, do nothing.      
   else: count = 1
   try: unpaidC.markers[resdict['Resource:{}'.format(card.Affiliation)]] += count
   except: unpaidC.markers[resdict['Resource:Neutral']] += count
   card.markers[mdict['Focus']] += count
   notify("{} exhausts {} to produce {} {} Resources.".format(me, card, count,card.Affiliation))
   if checkPaidResources(unpaidC) == 'OK': purchaseCard(unpaidC)
   if debugVerbosity >= 3: notify("<<< generate()") #Debug

def findUnpaidCard():
   if debugVerbosity >= 1: notify(">>> findUnpaidCard(){}".format(extraASDebug())) #Debug
   if unpaidCard: return unpaidCard
   else:
      for card in table:
         if card.highlight == UnpaidColor and card.controller == me: return card
   if debugVerbosity >= 3: notify("<<< findUnpaidCard()") #Debug
   return None # If not unpaid card is found, return None

def checkPaidResources(card):
   if debugVerbosity >= 1: notify(">>> checkPaidResources(){}".format(extraASDebug())) #Debug
   count = 0
   affiliationMatch = False
   for cMarkerKey in card.markers: #We check the key of each marker on the card
      for resdictKey in resdict:  #against each resource type available
         if debugVerbosity >= 2: notify("About to compare marker keys: {} and {}".format(resdict[resdictKey],cMarkerKey)) #Debug
         if resdict[resdictKey] == cMarkerKey: # If the marker is a resource
            count += card.markers[cMarkerKey]  # We increase the count of how many resources have been paid for this card
            if debugVerbosity >= 2: notify("About to check resource found affiliaton") #Debug
            if 'Resource:{}'.format(card.Affiliation) == resdictKey: # if the card's affiliation also matches the currently checked resource
               affiliationMatch = True # We set that we've also got a matching resource affiliation
   if debugVerbosity >= 2: notify("About to check successful cost. Count: {}, Affiliation: {}".format(count,card.Affiliation)) #Debug
   if count >= num(card.Cost) and (card.Affiliation == 'Neutral' or affiliationMatch):
      if debugVerbosity >= 3: notify("<<< checkPaidResources(). Return OK") #Debug
      return 'OK'
   else:
      if debugVerbosity >= 3: notify("<<< checkPaidResources(). Return NOK") #Debug
      return 'NOK'

def purchaseCard(card, x=0, y=0):
   if debugVerbosity >= 1: notify(">>> purchaseCard(){}".format(extraASDebug())) #Debug
   global unpaidCard
   checkPaid = checkPaidResources(card)
   if checkPaid == 'OK' or confirm(":::ERROR::: You do have not yet paid the cost of this card. Bypass?"):
      # if the card has been fully paid, we remove the resource markers and move it at its final position.
      card.highlight = None
      for cMarkerKey in card.markers: 
         for resdictKey in resdict:
            if resdict[resdictKey] == cMarkerKey: 
               card.markers[cMarkerKey] = 0
      unpaidCard = None
      if checkPaid == 'OK': notify("{} has paid for {}".format(me,card)) 
      else: notify(":::ATTENTION::: {} has acquired {} by skipping its full cost".format(me,card))
   if debugVerbosity >= 3: notify("<<< purchaseCard()") #Debug

def commit(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> commit(){}".format(extraASDebug())) #Debug
   mute()
   if Side == 'Light': commitColor = LightForceColor
   else: commitColor = DarkForceColor
   if card.Type != 'Unit':
      whisper(":::ATTENTION::: You can only commit units to the force. ABORTING!")
      return      
   commitedCards = [c for c in table if c.controller == me and c.highlight == commitColor]
   if len(commitedCards) >= 3:
      whisper(":::ATTENTION::: You already have 3 cards committed to the source. You cannot commit any more without losing on of those. ABORTING!")
      return
   notify("{} commits {} to the force.".format(me, card))
   card.highlight = commitColor
   if debugVerbosity >= 3: notify("<<< commit()") #Debug

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
         currentObjectives = eval(me.getGlobalVariable('currentObjectives'))
         currentObjectives.remove(card._id)
         me.setGlobalVariable('currentObjectives', str(currentObjectives))
         card.moveTo(opponent.piles['Victory Pile']) # Objectives are won by the opponent
         opponent.counters['Objectives Destroyed'].value += 1         
         if Side == 'Light': 
            modifyDial(opponent.counters['Objectives Destroyed'].value)
            notify("{} thwarts {}. The Death Star Dial advances by {}".format(opponent,card,opponent.counters['Objectives Destroyed'].value))
         else: notify("{} thwarts {}.".format(opponent,card))
      else:
         destroyedObjectives = eval(getGlobalVariable('destroyedObjectives')) 
         # Since we cannot modify the shared variables of other players, we store the destroyed card ids in a global variable
         # Then when the other player tries to refresh, it first removes any destroyed objectives from their list.
         destroyedObjectives.append(card._id)
         setGlobalVariable('destroyedObjectives', str(destroyedObjectives))
         card.moveTo(me.piles['Victory Pile']) # Objectives are won by the opponent
         me.counters['Objectives Destroyed'].value += 1
         if Side == 'Dark': 
            modifyDial(opponent.counters['Objectives Destroyed'].value)
            notify("{} thwarts {}. The Death Star Dial advances by {}".format(me,card,me.counters['Objectives Destroyed'].value))
         else: notify("{} thwarts {}.".format(me,card))
   elif card.Type == "Affiliation" or card.Type == "BotD": whisper("This isn't the card you're looking for...")
   elif card.highlight == EdgeColor:
      global edgeRevealed, edgeCount
      edgeRevealed = False # Clearing some variables just in case they were left over. 
      # (I've put this here, because it's one of the few places during engagement, where the opponent has to take an action as well)
      edgeCount = 0
      card.moveTo(card.owner.piles['Discard Pile'])
   else:
      card.moveTo(card.owner.piles['Discard Pile'])
      notify("{} discards {}".format(me,card))
 
def inspectCard(card, x = 0, y = 0): # This function shows the player the card text, to allow for easy reading until High Quality scans are procured.
   if debugVerbosity >= 1: notify(">>> inspectCard(){}".format(extraASDebug())) #Debug
   #if debugVerbosity > 0: finalTXT = 'AutoScript: {}\n\n AutoAction: {}'.format(CardsAS.get(card.model,''),CardsAA.get(card.model,''))
   finalTXT = "{}\n\nCard Text: {}".format(card.name, card.Text)
   confirm("{}".format(finalTXT))

def rulings(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> rulings(){}".format(extraASDebug())) #Debug
   mute()
   #if not card.isFaceUp: return
   #openUrl('http://www.netrunneronline.com/cards/{}/'.format(card.Errata))
   openUrl('http://www.cardgamedb.com/index.php/netrunner/star-wars-card-search?text={}&fTS=0'.format(card.name)) # Errata is not filled in most card so this works better until then

def play(card):
   if debugVerbosity >= 1: notify(">>> play(){}".format(extraASDebug())) #Debug
   global unpaidCard
   mute()
   card.moveToTable(0, 0 + yaxisMove(card))
   card.highlight = UnpaidColor
   unpaidCard = card
   notify("{} attempts to play {}.".format(me, card))

def playEdge(card):
   if debugVerbosity >= 1: notify(">>> playEdge(){}".format(extraASDebug())) #Debug
   global edgeCount
   mute()
   card.moveToTable(playerside * 400, 30 + yaxisMove(card) + (40 * edgeCount), True)
   card.highlight = EdgeColor
   edgeCount += 1
   notify("{} places a card in their edge stack.".format(me, card))
   
def revealEdge():
   if debugVerbosity >= 1: notify(">>> revealEdge(){}".format(extraASDebug())) #Debug
   global edgeRevealed
   fateNr = 0
   if not edgeRevealed:
      if debugVerbosity >= 2: notify("Edge cards not revealed yet. About to do that") #Debug
      for card in table:
         if card.highlight == EdgeColor and not card.isFaceUp and card.owner == me:
            card.isFaceUp = True
            if card.Type == 'Fate': fateNr += 1
      if fateNr > 0: extraTXT = " They have {} fate cards".format(fateNr)
      else: extraTXT = ''
      notify("{} reveals their edge stack.{}".format(me,extraTXT))
      edgeRevealed = True
   else:
      if debugVerbosity >= 2: notify("Edge cards already revealed. Gonna calculate edge") #Debug
      myEdgeTotal = 0
      opponentEdgeTotal = 0
      for card in table:
         if card.highlight == EdgeColor and card.isFaceUp:
            if card.owner == me: myEdgeTotal += num(card.Force)
            else: opponentEdgeTotal += num(card.Force)
      if myEdgeTotal > opponentEdgeTotal:
         if debugVerbosity >= 2: notify("I've got the edge") #Debug
         if not (Affiliation.markers[mdict['Edge']] and Affiliation.markers[mdict['Edge']] == 1): 
         # We check to see if we already have the edge marker on our affiliation card (from our opponent running the same script)
            clearEdgeMarker() # We clear the edge, in case another player's affiliation card had it
            Affiliation.markers[mdict['Edge']] = 1
            notify("{} has the edge in this engagement ({}: {} force VS {}: {} force)".format(me,me, myEdgeTotal, opponent, opponentEdgeTotal))
         else: whisper(":::NOTICE::: You already have the edge. Nothing else to do.")
      elif myEdgeTotal < opponentEdgeTotal:
         if debugVerbosity >= 2: notify("Opponent has the edge") #Debug
         oppAffiliation = getSpecial('Affiliation',opponent)
         if not (oppAffiliation.markers[mdict['Edge']] and oppAffiliation.markers[mdict['Edge']] == 1): 
         # We check to see if our opponent already have the edge marker on our affiliation card (from our opponent running the same script)
            clearEdgeMarker() # We clear the edge, in case another player's affiliation card had it
            oppAffiliation.markers[mdict['Edge']] = 1
            notify("{} has the edge in this engagement ({}: {} force VS {}: {} force)".format(oppAffiliation,me, myEdgeTotal, opponent, opponentEdgeTotal))
         else: whisper(":::NOTICE::: Your opponent already have the edge. Nothing else to do.")
      else: 
         if debugVerbosity >= 2: notify("Edge is a Tie") #Debug
         currentTarget = Card(num(getGlobalVariable('Engaged Objective')))
         if debugVerbosity >= 2: notify("Finding defender's Affiliation card.") #Debug
         defenderAffiliation = getSpecial('Affiliation',currentTarget.owner)
         if not (defenderAffiliation.markers[mdict['Edge']] and defenderAffiliation.markers[mdict['Edge']] == 1): 
            clearEdgeMarker() # We clear the edge, in case another player's affiliation card had it
            defenderAffiliation.markers[mdict['Edge']] = 1
            notify("Nobody managed to get the upper hand in the edge struggle ({}: {} force VS {}: {} force), so {} retains the edge as the defender.".format(me, myEdgeTotal, opponent, opponentEdgeTotal,currentTarget.owner))
         else: whisper(":::NOTICE::: The defender already has the edge. Nothing else to do.")
      if debugVerbosity >= 3: notify("<<< revealEdge()") #Debug

def mulligan(group):
   if debugVerbosity >= 1: notify(">>> mulligan(){}".format(extraASDebug())) #Debug
   if not confirm("Are you sure you want to take a mulligan?"): return
   notify("{} is taking a Mulligan...".format(me))
   groupToDeck(group,silent = True)
   #resetAll()
   for i in range(2): 
      shuffle(me.piles['Command Deck']) # We do a good shuffle this time.   
      rnd(1,10)
      whisper("Shuffling...")
   drawMany(count = me.Reserves)   
   if debugVerbosity >= 3: notify("<<< mulligan()") #Debug

def groupToDeck (group = me.hand, player = me, silent = False):
   if debugVerbosity >= 1: notify(">>> groupToDeck(){}".format(extraASDebug())) #Debug
   mute()
   deck = player.piles['Command Deck']
   count = len(group)
   for c in group: c.moveTo(deck)
   if debugVerbosity >= 2: notify("About to announce")
   if not silent: notify ("{} moves their whole {} to their {}.".format(player,group.name,deck.name))
   if debugVerbosity >= 3: notify("<<< groupToDeck() with return:\n{}\n{}\n{}".format(group.name,deck.name,count)) #Debug
   return(group.name,deck.name,count) # Return a tuple with the names of the groups.
   
def randomDiscard(group):
	mute()
	card = group.random()
	if card == None: return
	notify("{} randomly discards {}.".format(me,card.name))
	card.moveTo(me.piles['Discard Pile'])

def drawCommand(group, silent = False):
   if debugVerbosity >= 1: notify(">>> drawCommand(){}".format(extraASDebug())) #Debug
   mute()
   if len(group) == 0: return
   card = group.top()
   card.moveTo(me.hand)
   if not silent: notify("{} Draws a command card.".format(me))

def drawObjective(group = me.piles['Objective Deck'], silent = False):
   if debugVerbosity >= 1: notify(">>> drawObjective(){}".format(extraASDebug())) #Debug
   mute()
   if len(group) == 0: return
   currentObjectives = eval(me.getGlobalVariable('currentObjectives'))
   destroyedObjectives = eval(getGlobalVariable('destroyedObjectives'))
   for card_id in destroyedObjectives: 
      try: currentObjectives.remove(card_id) # Removing destroyed objectives before checking.
      except ValueError: pass 
   if len(currentObjectives) >= 3 and not confirm("You already control the maximum of 3 objectives. Are you sure you want to play another?"): return
   card = group.top()
   storeObjective(card)
   if not silent: notify("{} new objective is {}.".format(me,card))
   
def drawMany(group = me.piles['Command Deck'], count = None, destination = None, silent = False):
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

def refillHand(): # Simply refills the player's hand to their reserve maximum
   mute()
   if len(me.hand) < me.Reserves: 
      drawMany(count = me.Reserves - len(me.hand))
      notify(":> {} Refills their hand to their reserve maximum".format(me))
      
   
def drawBottom(group, x = 0, y = 0):
	if len(group) == 0: return
	mute()
	group.bottom().moveTo(me.hand)
	notify("{} draws a card from the bottom.".format(me))

def shuffle(group):
	group.shuffle()

#---------------------------------------------------------------------------
# Tokena and Markers
#---------------------------------------------------------------------------
	
def addFocus(card, x = 0, y = 0):
    mute()
    notify("{} adds a Focus token on {}.".format(me, card))
    card.markers[mdict['Focus']] += 1
    
def addDamage(card, x = 0, y = 0):
    mute()
    notify("{} adds a Damage token on {}.".format(me, card))
    card.markers[mdict['Damage']] += 1    
    
def addShield(card, x = 0, y = 0):
    mute()
    notify("{} adds a Shield token on {}.".format(me, card))
    card.markers[mdict['Shield']] += 1        

def subResource(card, x = 0, y = 0):
    subToken(card, 'Resource')

def subDamage(card, x = 0, y = 0):
    subToken(card, 'Damage')

def subShield(card, x = 0, y = 0):
    subToken(card, 'Shield')

def subToken(card, tokenType):
    mute()
    notify("{} removes a {} from {}.".format(me, tokenType[0], card))
    card.markers[mdict[tokenType]] -= 1	
    
def addMarker(cards, x = 0, y = 0): # A simple function to manually add any of the available markers.
   if debugVerbosity >= 1: notify(">>> addMarker(){}".format(extraASDebug())) #Debug
   mute()
   marker, quantity = askMarker() # Ask the player how many of the same type they want.
   if quantity == 0: return
   for card in cards: # Then go through their cards and add those markers to each.
      card.markers[marker] += quantity
      notify("{} adds {} {} counter to {}.".format(me, quantity, marker[0], card))

def clearEdgeMarker():
   for card in table:
      if card.Type == 'Affiliation' and card.markers[mdict['Edge']] and card.markers[mdict['Edge']] == 1:
         card.markers[mdict['Edge']] = 0