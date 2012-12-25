    # Python Scripts for the Star Wars LCG definition for OCTGN
    # Copyright (C) 2012  Konstantine Thoukydides

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
firstTurn = True # A variable to allow the engine to skip some phases on the first turn.
handRefillDone = False # A variable which tracks if the player has refilled their hand during the draw phase. Allows the game to go faster.
forceStruggleDone = False # A variable which tracks if the player's have actually done the force struggle for this turn (just in case it's forgotten)
ModifyDraw = 0 # When 1 it signifies an effect that affects the number of cards drawn per draw.
limitedPlayed = False # A Variable which records if the player has played a limited card this turn
reversePlayerChk = False # The reversePlayerChk variable is set to true by the calling function if we want the scripts to explicitly treat who discarded the objective opposite. For example for the ability of Decoy at Dantooine, since it's the objective's own controller that discards the cards usually, we want the game to treat it always as if their opponent is discarding instead.
warnZeroCostEvents = True # Warns the player about zero cost events.

#---------------------------------------------------------------------------
# Phases
#---------------------------------------------------------------------------

def showCurrentPhase(): # Just say a nice notification about which phase you're on.
   if getGlobalVariable('Engaged Objective') != 'None':
      notify(engagementPhases[num(getGlobalVariable('Engagement Phase'))])
   else: 
      notify(phases[num(me.getGlobalVariable('Phase'))])
   
def nextPhase(group = table, x = 0, y = 0, setTo = None):  
# Function to take you to the next phase. 
   if debugVerbosity >= 1: notify(">>> nextPhase(){}".format(extraASDebug())) #Debug
   mute()
   if getGlobalVariable('Engaged Objective') != 'None':
      phase = num(getGlobalVariable('Engagement Phase'))
      if setTo: phase = setTo
      else: phase += 1
      if phase == 4: revealEdge(forceCalc = True) # Just to make sure it wasn't forgotten.
      setGlobalVariable('Engagement Phase',str(phase))
      showCurrentPhase()
      if not setTo:
         if phase == 1: delayed_whisper(":::NOTE::: You can now start selecting engagement participants by double-clicking on them")
         elif phase == 5: finishEngagement() # If it's the reward unopposed phase, we simply end the engagement immediately after
   else:
      phase = num(me.getGlobalVariable('Phase'))
      if getGlobalVariable('Engaged Objective') != 'None': finishEngagement()
      if phase == 6: 
         if not forceStruggleDone and Automations['Start/End-of-Turn/Phase']: resolveForceStruggle() # If the player forgot to do their force stuggle, then we just do it quickly for them.
         me.setGlobalVariable('Phase','0') # In case we're on the last phase (Force), we end our turn.
         setGlobalVariable('Active Player', opponent.name)
         atTimedEffects(Time = 'End') # Scripted events at the end of the player's turn
         notify("=== {} has ended their turn ===.".format(me))
         for card in table:
            if card.markers[mdict['Activation']]: card.markers[mdict['Activation']] = 0 # At the end of each turn we clear the once-per turn abilities.
         if debugVerbosity >= 3: notify("<<< nextPhase(). Active Player: {}".format(getGlobalVariable('Active Player'))) #Debug
         return
      elif getGlobalVariable('Active Player') != me.name:
         if debugVerbosity >= 2: notify("### Active Player: {}".format(getGlobalVariable('Active Player'))) #Debug
         if not confirm("Your opponent has not finished their turn yet. Are you sure you want to continue?"): return
         me.setGlobalVariable('Phase','1')
         setGlobalVariable('Active Player', me.name)
         phase = 1
      else: 
         phase += 1
         me.setGlobalVariable('Phase',str(phase)) # Otherwise, just move up one phase
      if phase == 1: goToBalance()
      elif phase == 2: goToRefresh()
      elif phase == 3: goToDraw()
      elif phase == 4: 
         if not handRefillDone and Automations['Start/End-of-Turn/Phase']: refillHand() # If the player forgot to refill their hand in the Draw Phase, do it automatically for them now.
         goToDeployment()
      elif phase == 5:
         if firstTurn and Side == 'Dark':
            global firstTurn
            notify(":::NOTICE::: {} skips his first conflict phase".format(me))
            firstTurn = False
            goToForce()
         else: goToConflict()
      elif phase == 6: goToForce()

def goToBalance(group = table, x = 0, y = 0): # Go directly to the Balance phase
   if debugVerbosity >= 1: notify(">>> goToBalance(){}".format(extraASDebug())) #Debug
   mute()
   atTimedEffects(Time = 'Start') # Scripted events at the start of the player's turn
   me.setGlobalVariable('Phase','1')
   showCurrentPhase()
   global limitedPlayed
   limitedPlayed = False # Player can now play another limited card.
   turn = num(getGlobalVariable('Turn'))
   turn += 1 # Increase the counter for how many turns the player has played.
   setGlobalVariable('Turn',str(turn))
   if not Automations['Start/End-of-Turn/Phase']: return
   if Side == 'Dark': 
      if haveForce():
         modifyDial(2)
         notify(":> The Force is with the Dark Side! The Death Star dial advances by 2")
      else:
         modifyDial(1)
         notify(":> The Death Star dial advances by 1")
   else:
      if haveForce():
         opponentObjectives = eval(opponent.getGlobalVariable('currentObjectives'))
         objectiveList = []
         for objectve_ID in opponentObjectives:
            objective = Card(objectve_ID)
            if objective.markers[mdict['Damage']] and objective.markers[mdict['Damage']] >= 1: 
               extraTXT = " ({} Damage)".format(objective.markers[mdict['Damage']])
            else: extraTXT = ''
            objectiveList.append(objective.name + extraTXT)
         choice = SingleChoice("The Balance of the Force is in your favour. Choose one Dark Side objective to damage", objectiveList, type = 'radio', default = 0)
         chosenObj = Card(opponentObjectives[choice])
         chosenObj.markers[mdict['Damage']] += 1
         notify(":> The Force is with the Light Side! The rebel forces press the advantage and damage {}".format(chosenObj))      

def goToRefresh(group = table, x = 0, y = 0): # Go directly to the Refresh phase
   if debugVerbosity >= 1: notify(">>> goToRefresh(){}".format(extraASDebug())) #Debug
   atTimedEffects(Time = 'afterBalance')   
   mute()
   global firstTurn
   me.setGlobalVariable('Phase','2')
   showCurrentPhase()
   if not Automations['Start/End-of-Turn/Phase']: return
   if not firstTurn: notify(":> {} refreshed all their cards".format(me))   
   for card in table:
      if card.controller == me and card.highlight != CapturedColor:
         if firstTurn and Side == 'Light':
            notify(":::NOTICE::: {} skips his first card refresh".format(me))
            firstTurn = False
         else:
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
   atTimedEffects(Time = 'afterRefresh') # We put "afterRefresh" in the refresh phase, as cards trigger immediately after refreshing. Not afte the refresh phase as a whole.

def goToDraw(group = table, x = 0, y = 0): # Go directly to the Draw phase
   if debugVerbosity >= 1: notify(">>> goToDraw(){}".format(extraASDebug())) #Debug
   mute()
   global handRefillDone
   handRefillDone = False
   me.setGlobalVariable('Phase','3')
   showCurrentPhase()
   if not Automations['Start/End-of-Turn/Phase']: return
   if len(me.hand) == 0: refillHand() # If the player's hand is empty, there's no option to take. Just refill.
   
def goToDeployment(group = table, x = 0, y = 0): # Go directly to the Deployment phase
   if debugVerbosity >= 1: notify(">>> goToDeployment(){}".format(extraASDebug())) #Debug
   atTimedEffects(Time = 'afterDraw')
   mute()
   me.setGlobalVariable('Phase','4')
   showCurrentPhase()   
   if not Automations['Start/End-of-Turn/Phase']: return
   
def goToConflict(group = table, x = 0, y = 0): # Go directly to the Conflict phase
   if debugVerbosity >= 1: notify(">>> goToConflict(){}".format(extraASDebug())) #Debug
   atTimedEffects(Time = 'afterDeployment')   
   mute()
   me.setGlobalVariable('Phase','5')
   showCurrentPhase()   
   if not Automations['Start/End-of-Turn/Phase']: return

def goToForce(group = table, x = 0, y = 0): # Go directly to the Force phase
   if debugVerbosity >= 1: notify(">>> goToForce(){}".format(extraASDebug())) #Debug
   atTimedEffects(Time = 'afterConflict')   
   mute()
   global forceStruggleDone
   forceStruggleDone = False # At the start of the force phase, the force struggle is obviously not done yet.
   if getGlobalVariable('Engaged Objective') != 'None': finishEngagement() # If the playes jump to the force phase after engagement, we make sure we clear the engagement.
   me.setGlobalVariable('Phase','6')
   showCurrentPhase()
   delayed_whisper(":::ATTENTION::: Once you've committed all the units you want to the force, press Ctrl+F6 to resolve the force struggle")
   if not Automations['Start/End-of-Turn/Phase']: return

def resolveForceStruggle(group = table, x = 0, y = 0): # Calculate Force Struggle
   mute()
   if num(me.getGlobalVariable('Phase')) != 6 and not confirm("The force struggle is only supposed to happen at the end of your force phase. Bypass?"):
      return # If it's not the force phase, give the player an opportunity to abort.
   global forceStruggleDone
   myStruggleTotal = 0
   opponentStruggleTotal = 0
   if Side == 'Light': 
      commitColor = LightForceColor
      commitOpponent = DarkForceColor
   else: 
      commitColor = DarkForceColor
      commitOpponent = LightForceColor
   if debugVerbosity >= 2: notify("### Counting my committed cards") #Debug
   commitedCards = [c for c in table if c.controller == me and c.highlight == commitColor]
   if debugVerbosity >= 2: notify("### About to loop") #Debug
   for card in commitedCards:
      try: 
         if card.markers[mdict['Focus']] == 0: myStruggleTotal += num(card.Force)
      except: myStruggleTotal += num(card.Force) # If there's an exception, it means the card didn't ever have a focus marker
   if debugVerbosity >= 2: notify("### Counting my opponents cards") #Debug
   opponentCommitedCards  = [c for c in table if c.controller == opponent and c.highlight == commitOpponent]
   for card in opponentCommitedCards:
      try: 
         if card.markers[mdict['Focus']] == 0: opponentStruggleTotal += num(card.Force)
      except: opponentStruggleTotal += num(card.Force) # If there's an exception, it means the card didn't ever have a focus marker
   if debugVerbosity >= 2: notify("### About to check for bonus force cards") #Debug
   for c in table:
      if debugVerbosity >= 4: notify("#### Checking {}".format(c)) #Debug
      bonusForce = re.search(r'Force([0-9])Bonus',CardsAS.get(c.model,''))
      if bonusForce:
         if debugVerbosity >= 2: notify("### Found card with Bonus force") #Debug
         if c.controller == me: myStruggleTotal += num(bonusForce.group(1))
         else: opponentStruggleTotal += num(bonusForce.group(1))
   if debugVerbosity >= 2: notify("### Checking Struggle") #Debug
   BotD = getSpecial('BotD')
   if myStruggleTotal - opponentStruggleTotal > 0: 
      if debugVerbosity >= 2: notify("### struggleTotal Positive") #Debug
      if (Side == 'Light' and BotD.isAlternateImage) or (Side == 'Dark' and not BotD.isAlternateImage):
         if debugVerbosity >= 2: notify("### About to flip BotD due to my victory") #Debug
         BotD.switchImage
         x,y = Affiliation.position
         if debugVerbosity >= 2: notify("### My Affiliation is {} at position {} {}".format(Affiliation, x,y,)) #Debug
         BotD.moveToTable(x - (playerside * 70), y)
         notify(":> The force struggle tips the balance of the force towards the {} side ({}: {} - {}: {})".format(Side,me,myStruggleTotal,opponent,opponentStruggleTotal))
      else: notify(":> The balance of the force remains skewed towards the {}. ({}: {} - {}: {})".format(Side,me,myStruggleTotal,opponent,opponentStruggleTotal))         
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
      else: notify(":> The balance of the force remains skewed towards the {}. ({}: {} - {}: {})".format(opponent.getGlobalVariable('Side'),me,myStruggleTotal,opponent,opponentStruggleTotal))
   else: # If the current force totals are tied, we just announce that.
      if debugVerbosity >= 2: notify("Force struggle is tied") #Debug
      if BotD.isAlternateImage: BotDside = 'Dark'
      else: BotDside = 'Light'
      notify(":> The force struggle is tied. The Balance remains tiped to the {} Side. ({}: {} - {}: {})".format(BotDside,me,myStruggleTotal,opponent,opponentStruggleTotal))
   forceStruggleDone = True # Set that the forcestruggle is done.
   if debugVerbosity >= 3: notify("<<< resolveForceStruggle()") #Debug
         
def engageTarget(group = table, x = 0, y = 0): # Start an Engagement Phase
   if debugVerbosity >= 1: notify(">>> engageTarget(){}".format(extraASDebug())) #Debug
   mute()
   if me.getGlobalVariable('Phase') != '5' and not confirm("You need to be in the conflict phase before you can engage an objective. Bypass?"):
      return
   if getGlobalVariable('Engaged Objective') != 'None': finishEngagement() 
   if debugVerbosity >= 2: notify("About to find targeted objectives.") #Debug
   cardList = [c for c in table if (c.Type == 'Objective' or re.search(r'EngagedAsObjective',CardsAS.get(c.model,'')))  and c.targetedBy and c.targetedBy == me and c.controller == opponent]
   if debugVerbosity >= 2: notify("About to count found objectives list. List is {}".format(cardList)) #Debug
   if len(cardList) == 0: 
      whisper("You need to target an opposing Objective to start an Engagement")
      return
   else: targetObjective = cardList[0]
   targetObjective.highlight = DefendColor
   if debugVerbosity >= 2: notify("About set the global variable") #Debug
   setGlobalVariable('Engaged Objective',str(targetObjective._id))
   showCurrentPhase()
   #setGlobalVariable('Engagement Phase','1')
   if debugVerbosity >= 2: notify("About to announce") #Debug
   notify("{} forces have engaged {}'s {}".format(me,targetObjective.controller, targetObjective))
   rnd(1,10)
   if debugVerbosity >= 3: notify("<<< engageTarget()") #Debug
   
def finishEngagement(group = table, x=0, y=0, automated = False):
   mute()
   if debugVerbosity >= 1: notify(">>> finishEngagement(){}".format(extraASDebug())) #Debug
   # First we check for unopposed bonus
   if not automated and getGlobalVariable('Engaged Objective') == 'None': 
      whisper(":::ERROR::: You are not currently in an engagement")
      return
   currentTarget = Card(num(getGlobalVariable('Engaged Objective')))
   if getGlobalVariable('Engaged Objective') == 'None': 
      whisper(":::ERROR::: There is no engagement currently.")
      return
   if num(getGlobalVariable('Engagement Phase')) < 5: nextPhase(setTo = 5)
   unopposed = False
   for card in table: # If the attacker still has participants in the battle. there is a chance this is unopposed.
      if card.orientation == Rot90 and card.controller != currentTarget.controller: unopposed = True 
   if unopposed: # If the attacker still has units remaining then we check to see if the defender has any as well. 
      for card in table: # If they do, then the battle is not unnoposed.
         if card.orientation == Rot90 and card.controller == currentTarget.controller: unopposed = False
   if unopposed and currentTarget in table: 
      notify(":> {} managed to finish the engagement at {} unopposed. They inflict an extra damage to the objective.".format(me,currentTarget))
      currentTarget.markers[mdict['Damage']] += 1
      autoscriptOtherPlayers('UnopposedEngagement',currentTarget)
   for card in table:
      if card.orientation == Rot90: card.orientation = Rot0
      if card.highlight == DefendColor: card.highlight = None
   notify("The engagement at {} is finished.".format(Card(num(getGlobalVariable('Engaged Objective')))))
   setGlobalVariable('Engaged Objective','None')
   setGlobalVariable('Engagement Phase','0')
   for card in table: # We get rid of all the Edge cards at the end of an engagement in case the player hasn't done so already.
      if card.highlight == EdgeColor or card.highlight == FateColor: discard(card) # We remove both player's edge cards
   edgeRevealed = eval(getGlobalVariable('Revealed Edge'))
   for plName in edgeRevealed: edgeRevealed[plName] = False # Clearing some variables just in case they were left over. 
   setGlobalVariable('Revealed Edge',str(edgeRevealed))
   clearEdgeMarker() # We clear the edge, in case another player's affiliation card had it
   clearTargets() # We clear the targets in case they were forgotten.
   atTimedEffects('afterEngagement')
   if debugVerbosity >= 3: notify("<<< finishEngagement()") #Debug 
#---------------------------------------------------------------------------
# Rest
#---------------------------------------------------------------------------

def gameSetup(group, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> gameSetup(){}".format(extraASDebug())) #Debug
   mute()
   global SetupPhase, Side, Affiliation
   deck = me.piles['Command Deck']
   objectives = me.piles['Objective Deck']
   if not startupMsg: fetchCardScripts() # We only download the scripts at the very first setup of each play session.
   versionCheck()
   if SetupPhase and len(me.hand) != 1: # If the hand has only one card, we assume the player reset and has the affiliation now there.
      if debugVerbosity >= 3: notify("### Executing Second Setup Phase")
      global opponent
      if not ofwhom('ofOpponent') and len(players) > 1: # If the other player hasn't chosen their side yet, it means they haven't yet tried to setup their table, so we abort
         whisper("Please wait until your opponent has placed their Affiliation down before proceeding")
         return
      if len(me.hand) > 3 and not confirm("Have you moved one of your 4 objectives to the bottom of your objectives deck?"): return
      opponent = ofwhom('ofOpponent') # Setting a variable to quickly have the opponent's object when we need it.
      for card in me.hand:
         if card.Type != 'Objective': 
            whisper(":::Warning::: You are not supposed to have any non-Objective cards in your hand at this point")
            card.moveToBottom(deck)
            continue
         else: storeObjective(card, GameSetup = True)
      shuffle(deck)
      drawMany(deck, 6, silent = True)
      notify("{} has planned their starting objectives and drawn their starting commands.".format(me))
      delayed_whisper(":::ATTENTION::: Once your opponent has put down their starting objectives and decided to mulligan or not, double click on one of your objectives to reveal them and trigger any effects.")
      SetupPhase = False
   else: # This choice is only for a new game.
      if debugVerbosity >= 3: notify("### Executing First Setup Phase")
      if Side and Affiliation and not confirm("Are you sure you want to setup for a new game? (This action should only be done after a table reset)"): return
      if debugVerbosity >= 3: notify("### Setting SetupPhase Variable")
      SetupPhase = True
      if not table.isTwoSided() and not confirm(":::WARNING::: This game is designed to be played on a two-sided table. Things will be extremely uncomfortable otherwise!! Please start a new game and makde sure the  the appropriate button is checked. Are you sure you want to continue?"): return
      if debugVerbosity >= 3: notify("### Choosing Side")
      chooseSide()
      if debugVerbosity >= 3: notify("### Checking Deck")
      if len(deck) == 0:
         whisper ("Please load a deck first!")
         return
      if debugVerbosity >= 3: notify("### Reseting Variables")
      resetAll()
      if debugVerbosity >= 3: notify("### Placing Identity")
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
      if debugVerbosity >= 3: notify("### Placing Affiliation")
      Affiliation.moveToTable(playerside * -400, (playerside * 20) + yaxisMove(Affiliation))
      if Side == 'Light' or len(players) == 1: #We create the balance of the force card during the dark side's setup, to avoid duplicates. 
                                               # We also create it if there's only one player for debug purposes
         BotD = table.create("e31c2ba8-3ffc-4029-94fd-5f98ee0d78cc", 0, 0, 1, True)
         BotD.moveToTable(playerside * -470, (playerside * 20) + yaxisMove(Affiliation)) # move it next to the affiliation card for now.
         setGlobalVariable('Balance of the Force', str(BotD._id))
      else: setGlobalVariable('Active Player', me.name) # If we're DS, set ourselves as the current player, since the Dark Side goes first.
      rnd(1,10)  # Allow time for the affiliation to be recognised
      notify("{} is representing the {}.".format(me,Affiliation))
      if debugVerbosity >= 3: notify("### Shuffling Decks")
      shuffle(objectives)
      if debugVerbosity >= 3: notify("### Drawing 4 Objectives")
      drawMany(objectives, 4, silent = True)
      notify("{} is choosing their objectives.".format(me))
      whisper(":::ATTENTION::: Once both players have discarded their 4th objective, press Ctrl+Shift+S to place your objectives on the table and draw your starting hand.")
      if debugVerbosity >= 3: notify("### Reshuffling Deck")
      shuffle(objectives) # And another one just to be sure
      shuffle(deck)

def defaultAction(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> defaultAction(){}".format(extraASDebug())) #Debug
   mute()
   if card.highlight == FateColor: 
      #whisper(":::ATTENTION::: No fate card automation yet I'm afraid :-(\nPlease do things manually for now.")
      notify("{} resolves the ability of fate card {}".format(me,card))
      executePlayScripts(card, 'RESOLVEFATE')
      autoscriptOtherPlayers('ResolveFate',card)
      card.highlight = EdgeColor
   elif card.highlight == ObjectiveSetupColor:
      myObjectives = [c for c in table if c.controller == me and c.highlight == ObjectiveSetupColor]
      for c in myObjectives: 
         c.highlight = None
         c.orientation = Rot0
         c.isFaceUp = True # First we turn them all face up (We do two different loops to give the cards time to flip completely, so that we can grab their properties without having to put rnd(1,10) every time.
      for c in myObjectives: 
         loopChk(c,'Type') # We make sure we can read the card's properties first
         executePlayScripts(c, 'PLAY')
      notify("{} of the {} has revealed their starting objectives".format(me,Affiliation))
      if Side == 'Dark': 
         me.setGlobalVariable('Phase','0') # We now allow the dark side to start
         notify("--> {} of the Dark Side has the initiative".format(me))
   elif card.highlight == EdgeColor: revealEdge()
   elif card.highlight == UnpaidColor: purchaseCard(card)
   elif num(card.Resources) > 0 and findUnpaidCard(): 
      if debugVerbosity >= 2: notify("Card has resources") # Debug
      generate(card)
   elif card.Type == 'Unit' and getGlobalVariable('Engaged Objective') != 'None':
      if debugVerbosity >= 2: notify("Card is Unit and it's engagement time") # Debug
      if card.orientation == Rot0: participate(card)
      else: strike(card)
   elif card.model == 'e31c2ba8-3ffc-4029-94fd-5f98ee0d78cc': 
      card.switchImage # If the players double click on the Balance of the Force, we assume they want to flip it.
      notify(":::ATTENTION::: {} flipped the balance of the force manually".format(me))
   elif CardsAA.get(card.model,'') != '': useAbility(card)
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
   #notify("{} strikes with {}.".format(me, card))
   if num(getGlobalVariable('Engagement Phase')) < 4: nextPhase(setTo = 4)
   card.markers[mdict['Focus']] += 1
   if card.highlight == LightForceColor or card.highlight == DarkForceColor: card.markers[mdict['Focus']] += 1
   if debugVerbosity >= 2: notify("Focus Added") #Debug
   executePlayScripts(card, 'STRIKE') # Strike effects almost universally happen after focus.
   autoscriptOtherPlayers('UnitStrike',card)
   if debugVerbosity >= 2: notify("PlayScripts done. Calculating Icons") #Debug
   AnnounceText = ''
   Unit_DamageTXT = ''
   TacticsTXT = ''
   targetUnit = None
   Unit_Damage, Blast_Damage, Tactics = calculateCombatIcons(card)
   currentTarget = Card(num(getGlobalVariable('Engaged Objective'))) # We find the current objective target to see who's the owner, because only the attacker does blast damage
   if currentTarget.controller == opponent: currentTarget.markers[mdict['Damage']] += Blast_Damage # We assign the blast damage automatically, since there's only ever one target for it.
   for c in table: # We check to see if the attacking player has already selected a target.
      if c.targetedBy and c.targetedBy == me and c.Type == 'Unit': targetUnit = c
   if Unit_Damage and not Tactics and targetUnit:  # if our strike only does unit damage, and we've already targeted a unit, then just automatically apply it to it.
      targetUnit.markers[mdict['Damage']] += Unit_Damage
      Unit_DamageTXT = " to {}".format(targetUnit)
   elif not Unit_Damage and Tactics == 1 and targetUnit:  # If our strike does only 1 focus and nothing else, then we can auto-assign it to the targeted unit.
      targetUnit.markers[mdict['Focus']] += Tactics
      TacticsTXT = " (exhausting {})".format(targetUnit)
   elif ((Unit_Damage and Tactics) or Tactics > 1) and targetUnit: # We inform the user why we didn't assign markers automatically.
      delayed_whisper(":::ATTENTION::: Due to multiple effects, no damage or focus counters have been auto assigned. Please use Alt+D and Alt+F to assign markers to targeted units manually")
   elif not targetUnit and (Unit_Damage or Tactics): # We give some informatory whispers to the players to help them perform strikes faster in the future
      delayed_whisper(":::ATTENTION::: You had no units targeted with shift+click, so no counters were autoassigned. Remember to target cards before striking with simple effects, to avoid having to add counters manually afterwards")
   if Unit_Damage: AnnounceText += ' {} Unit Damage{}'.format(Unit_Damage,Unit_DamageTXT)
   if Tactics: 
      if AnnounceText == '': AnnounceText += ' {} Tactics{}'.format(Tactics,TacticsTXT)
      elif Blast_Damage: AnnounceText += ', {} Tactics{}'.format(Tactics,TacticsTXT)
      else: AnnounceText += ' and {} Tactics{}'.format(Tactics,TacticsTXT)
   if Blast_Damage: 
      if AnnounceText == '': AnnounceText += ' {} Blast Damage'.format(Blast_Damage)
      else: AnnounceText += ' and {} Blast Damage'.format(Blast_Damage)
   if AnnounceText == '': AnnounceText = " no effect"
   notify("{} strikes with {} for{}.".format(me,card,AnnounceText))
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
   if getGlobalVariable('Engaged Objective') == 'None':
      whisper(":::ERROR::: Please start an engagement first!")
      return
   currentTarget = Card(num(getGlobalVariable('Engaged Objective')))      
   if currentTarget.controller == opponent:
      if num(getGlobalVariable('Engagement Phase')) < 1: nextPhase(setTo = 1)
      notify("{} selects {} as an attacker.".format(me, card))
      executePlayScripts(card, 'ATTACK')   
   else:
      if num(getGlobalVariable('Engagement Phase')) < 2: nextPhase(setTo = 2)
      notify("{} selects {} as a defender.".format(me, card))
      executePlayScripts(card, 'DEFEND')   
   card.orientation = Rot90
   executePlayScripts(card, 'PARTICIPATION')
   autoscriptOtherPlayers('UnitParticipates',card)
   clearTargets() # We clear the targets to make sure there's no random markers being put by mistake.
   if debugVerbosity >= 3: notify("<<< participate()") #Debug

def clearParticipation(card,x=0,y=0): # Clears a unit from participating in a battle, to undo mistakes
   if card.orientation == Rot90: 
      card.orientation = Rot0
      notify("{} takes {} out of the engagement.".format(me, card))
   else: whisper(":::ERROR::: Unit is not currently participating in battle")
        
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
   executePlayScripts(card, 'GENERATE')
   autoscriptOtherPlayers('ResourceGenerated',card)
   if checkPaidResources(unpaidC) == 'OK': purchaseCard(unpaidC, manual = False)
   elif checkPaidResources(unpaidC) == 'USEOK': useAbility(unpaidC, paidAbility = True, manual = False) 
   if debugVerbosity >= 3: notify("<<< generate()") #Debug

def findUnpaidCard():
   if debugVerbosity >= 1: notify(">>> findUnpaidCard(){}".format(extraASDebug())) #Debug
   if unpaidCard: return unpaidCard
   else:
      for card in table:
         if (card.highlight == UnpaidColor or card.highlight == UnpaidAbilityColor) and card.controller == me: return card
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
            if debugVerbosity >= 2: notify("About to check found resource affiliaton") #Debug
            if 'Resource:{}'.format(card.Affiliation) == resdictKey: # if the card's affiliation also matches the currently checked resource
               affiliationMatch = True # We set that we've also got a matching resource affiliation
      if cMarkerKey[0] == "Ignores Affiliation Match": affiliationMatch = True # If we have a marker that ignores affiliations, we can start ignoring this card's as well
   for c in table:
      if c.controller == me and re.search("IgnoreAffiliationMatch",CardsAS.get(c.model,'')): affiliationMatch = True
   if debugVerbosity >= 2: notify("About to check successful cost. Count: {}, Affiliation: {}".format(count,card.Affiliation)) #Debug
   if card.highlight == UnpaidAbilityColor:
      reduction = reduceCost(card, 'USE', selectedAbility[card._id][1] - count, dryRun = True) # We do a dry run first. We do not want to trigger once-per turn abilities until the point where we've actually paid the cost.
      if count >= selectedAbility[card._id][1] - reduction and (card.Affiliation == 'Neutral' or affiliationMatch or (not affiliationMatch and (selectedAbility[card._id][1] - reduction) == 0)):
         if debugVerbosity >= 3: notify("<<< checkPaidResources(). Return USEOK") #Debug
         reduceCost(card, 'USE', selectedAbility[card._id][1] - count) # Now that we've actually made sure we've paid the cost, we use any ability that reduces costs.
         return 'USEOK'
      else:
         if debugVerbosity >= 3: notify("<<< checkPaidResources(). Return NOK") #Debug
         return 'NOK'      
   else:
      reduction = reduceCost(card, 'PLAY', num(card.Cost) - count, dryRun = True) # We do a dry run first. We do not want to trigger once-per turn abilities until the point where we've actually paid the cost.
      if count >= num(card.Cost) - reduction and (card.Affiliation == 'Neutral' or affiliationMatch or (not affiliationMatch and (num(card.Cost) - reduction) == 0)):
         if debugVerbosity >= 3: notify("<<< checkPaidResources(). Return OK") #Debug
         reduceCost(card, 'PLAY', num(card.Cost) - count) # Now that we've actually made sure we've paid the cost, we use any ability that reduces costs.
         return 'OK'
      else:
         if debugVerbosity >= 3: notify("<<< checkPaidResources(). Return NOK") #Debug
         return 'NOK'

def purchaseCard(card, x=0, y=0, manual = True):
   if debugVerbosity >= 1: notify(">>> purchaseCard(){}".format(extraASDebug())) #Debug
   global unpaidCard
   if manual: checkPaid = checkPaidResources(card) # If this is an attempt to manually pay for the card, we check that the player can afford it (e.g. it's zero cost or has cost reduction effects)
   else: checkPaid = 'OK' #If it's not manual, then it means the checkPaidResources() has been run successfully, so we proceed.
   if checkPaid == 'OK' or confirm(":::ERROR::: You do have not yet paid the cost of this card. Bypass?"):
      # if the card has been fully paid, we remove the resource markers and move it at its final position.
      card.highlight = None
      placeCard(card)
      for cMarkerKey in card.markers: 
         for resdictKey in resdict:
            if resdict[resdictKey] == cMarkerKey: 
               card.markers[cMarkerKey] = 0
      unpaidCard = None
      if checkPaid == 'OK': notify("{} has paid for {}".format(me,card)) 
      else: notify(":::ATTENTION::: {} has brought in {} by skipping its full cost".format(me,card))
      executePlayScripts(card, 'PLAY')
      autoscriptOtherPlayers('CardPlayed',card)
      if card.Type == "Event": card.moveTo(card.owner.piles['Discard Pile']) # We discard events as soon as their effects are resolved.
   if debugVerbosity >= 3: notify("<<< purchaseCard()") #Debug

def commit(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> commit(){}".format(extraASDebug())) #Debug
   mute()
   if Side == 'Light': commitColor = LightForceColor
   else: commitColor = DarkForceColor
   if card.Type != 'Unit':
      whisper(":::ERROR::: You can only commit units to the force.")
      return      
   commitedCards = [c for c in table if c.controller == me and c.highlight == commitColor]
   if len(commitedCards) >= 3:
      whisper(":::ERROR::: You already have 3 cards committed to the source. You cannot commit any more without losing on of those. ABORTING!")
      return
   notify("{} commits {} to the force.".format(me, card))
   card.highlight = commitColor
   executePlayScripts(card, 'COMMIT')
   autoscriptOtherPlayers('ForceCommit',card)
   if debugVerbosity >= 3: notify("<<< commit()") #Debug

def clearCommit(card, x=0, y=0): # Clears a unit from participating in a battle, to undo mistakes
   mute()
   if debugVerbosity >= 1: notify(">>> clearCommit(){}".format(extraASDebug())) #Debug
   if Side == 'Light': commitColor = LightForceColor
   else: commitColor = DarkForceColor
   if debugVerbosity >= 2: notify("### Checking for commitColor: {}".format(commitColor)) #Debug
   if card.highlight == commitColor:
      if debugVerbosity >= 2: notify("### commitColor found!") #Debug
      card.highlight = None
      if debugVerbosity >= 2: notify("### About to notify!") #Debug
      notify(":::ATTENTION::: {} takes {} out of its commitment to the force.".format(me, card))
   else: whisper(":::ERROR::: Unit is not currently committed to the force.")

def handDiscard(card):
   if debugVerbosity >= 1: notify(">>> handDiscard(){}".format(extraASDebug())) #Debug
   mute()
   if card.Type == "Objective": 
      card.moveToBottom(me.piles['Objective Deck']) # This should only happen during the game setup
      notify("{} chose their 3 starting objectives.".format(me))
   else:
      card.moveTo(me.piles['Discard Pile'])
      notify("{} discards {}".format(me,card))
      
def discard(card, x = 0, y = 0, silent = False):
   if debugVerbosity >= 1: notify(">>> discard()") #Debug
   mute()
   if card.Type == "Objective":
      if card.controller == me:
         if not silent and not confirm("Did your opponent thwart {}?".format(card.name)): return 'ABORT'
         if debugVerbosity >= 2: notify("About to score objective")
         currentObjectives = eval(me.getGlobalVariable('currentObjectives'))
         currentObjectives.remove(card._id)
         rescuedCount = rescueFromObjective(card)
         if rescuedCount >= 1: extraTXT = ", rescuing {} of their captured cards".format(rescuedCount)
         else: extraTXT = ''
         me.setGlobalVariable('currentObjectives', str(currentObjectives))
         card.moveTo(opponent.piles['Victory Pile']) # Objectives are won by the opponent
         opponent.counters['Objectives Destroyed'].value += 1         
         if Side == 'Light': 
            modifyDial(opponent.counters['Objectives Destroyed'].value)
            notify("{} thwarts {}. The Death Star Dial advances by {}".format(opponent,card,opponent.counters['Objectives Destroyed'].value))
         else: 
            notify("{} thwarts {}{}.".format(opponent,card,extraTXT))
            if me.counters['Objectives Destroyed'].value >= 3: 
               notify("===::: The Light Side wins the Game! :::====")
         executePlayScripts(card, 'THWART')
         global reversePlayerChk
         reversePlayerChk = True
         autoscriptOtherPlayers('ObjectiveThwarted',card)
         reversePlayerChk = False
      else:
         if not silent and not confirm("Are you sure you want to thwart {}?".format(card.name)): return 'ABORT'
         destroyedObjectives = eval(getGlobalVariable('destroyedObjectives')) 
         # Since we cannot modify the shared variables of other players, we store the destroyed card ids in a global variable
         # Then when the other player tries to refresh, it first removes any destroyed objectives from their list.
         destroyedObjectives.append(card._id)
         rescuedCount = rescueFromObjective(card)
         if rescuedCount >= 1: extraTXT = ", rescuing {} of their captured cards".format(rescuedCount)
         else: extraTXT = ''
         setGlobalVariable('destroyedObjectives', str(destroyedObjectives))
         card.moveTo(me.piles['Victory Pile']) # Objectives are won by the opponent
         me.counters['Objectives Destroyed'].value += 1
         if Side == 'Dark': 
            modifyDial(opponent.counters['Objectives Destroyed'].value)
            notify("{} thwarts {}. The Death Star Dial advances by {}".format(me,card,me.counters['Objectives Destroyed'].value))
         else: 
            notify("{} thwarts {}{}.".format(me,card,extraTXT))
            if opponent.counters['Objectives Destroyed'].value >= 3: 
               notify("===::: The Light Side wins the Game! :::====")
         executePlayScripts(card, 'THWART')
         autoscriptOtherPlayers('ObjectiveThwarted',card)
   elif card.Type == "Affiliation" or card.Type == "BotD": 
      whisper("This isn't the card you're looking for...")
      return 'ABORT'
   elif card.highlight == EdgeColor:
      global edgeCount
      edgeCount = 0
      card.moveTo(card.owner.piles['Discard Pile'])
   elif card.highlight == CapturedColor:
      removeCapturedCard(card)
      card.moveTo(card.owner.piles['Discard Pile'])   
   elif card.Type == 'Unit':
      if Automations['Placement']:
         if card.owner == me:
            freePositions = eval(me.getGlobalVariable('freePositions')) # We store the currently released position
            freePositions.append(card.position)
            me.setGlobalVariable('freePositions',str(freePositions))
         unitAmount = eval(getGlobalVariable('Existing Units'))
         unitAmount[card.owner.name] -= 1
         setGlobalVariable('Existing Units',str(unitAmount))
      card.moveTo(card.owner.piles['Discard Pile'])
      if not silent: notify("{} discards {}".format(me,card))
      autoscriptOtherPlayers('UnitDestroyed',card)
   else:
      card.moveTo(card.owner.piles['Discard Pile'])
      if not silent: notify("{} discards {}".format(me,card))
   executePlayScripts(card, 'DISCARD')
   if debugVerbosity >= 2: notify("### Checking if the card has attachments to discard as well.")      
   clearAttachLinks(card)
   if debugVerbosity >= 1: notify("<<< discard()") #Debug
   return 'OK'

def capture(group = table,x = 0,y = 0, chosenObj = None, targetC = None, silent = False): # Tries to find a targeted card in the table or the oppomnent's hand to capture
   if debugVerbosity >= 1: notify(">>> capture(){}".format(extraASDebug())) #Debug
   if debugVerbosity >= 2 and chosenObj: notify("### chosenObj = {}".format(chosenObj)) #Debug
   if debugVerbosity >= 2 and targetC: notify("### targetC = {}".format(targetC)) #Debug
   mute()
   if not targetC:
      if debugVerbosity >= 2: notify("Don't have preset target. Seeking...")
      for card in table:
         if debugVerbosity >= 2: notify("### Searching table") #Debug
         if card.targetedBy and card.targetedBy == me and card.Type != "Objective": 
            if card.highlight == CapturedColor and not confirm("Are you sure you want to move this captured card to a different objective?"): continue
            targetC = card
      if targetC: captureTXT = "{} has captured {}'s {}".format(me,targetC.owner,targetC)
      else:
         if debugVerbosity >= 2: notify("### Searching opponent's hand") #Debug
         for card in opponent.hand:
            if card.targetedBy and card.targetedBy == me: targetC = card
         if targetC: captureTXT = "{} has captured one card from {}'s hand".format(me,targetC.owner)
         else:
            if debugVerbosity >= 2: notify("### Searching command deck") #Debug
            for card in opponent.piles['Command Deck'].top(3):
               if debugVerbosity >= 3: notify("### Checking {}".format(card)) #Debug
               if card.targetedBy and card.targetedBy == me: targetC = card
            if targetC: captureTXT = "{} has captured one card from {}'s Command Deck".format(me,targetC.owner)
   else: captureTXT = ":> {} has captured one card from {}'s {}".format(me,targetC.owner,targetC.group.name)
   if not targetC: whisper(":::ERROR::: You need to target a command card in the table or your opponent's hand or deck before taking this action")
   else: 
      captureGroup = targetC.group.name
      if Side == 'Light': captor = opponent # Only dark side can capture.
      else: captor = me 
      if not chosenObj or chosenObj.owner != captor:
         if debugVerbosity >= 2: notify("Don't have preset objective. Seeking...")
         myObjectives = eval(captor.getGlobalVariable('currentObjectives'))
         objectiveList = []
         for objectve_ID in myObjectives:
            objective = Card(objectve_ID)
            if objective.markers[mdict['Damage']] and objective.markers[mdict['Damage']] >= 1: 
               extraTXT = " ({} Damage)".format(objective.markers[mdict['Damage']])
            else: extraTXT = ''
            objectiveList.append(objective.name + extraTXT)
         choice = SingleChoice("Choose in to which objective to capture the card.", objectiveList, type = 'radio', default = 0)
         chosenObj = Card(myObjectives[choice])
      if debugVerbosity >= 2: notify("About to Announce")
      captureTXT += " as part of their {} objective".format(chosenObj)
      if not silent: notify(captureTXT)
      rnd(1,10)
      if debugVerbosity >= 2: notify("About evaluate capture cards")
      capturedCards = eval(getGlobalVariable('Captured Cards'))
      capturedCards[targetC._id] = chosenObj._id
      xPos, yPos = chosenObj.position
      countCaptures = 0 
      for capturedC in capturedCards:
         if capturedCards[capturedC] == chosenObj._id: countCaptures += 1
      if captureGroup == 'Table': clearAttachLinks(targetC) # If the card was in the table, we check if it had any attachments to discard
      if debugVerbosity >= 2: notify("About to move to objective")
      targetCType = targetC.Type # Used later for the autoscripting of other cards
      if targetCType == '?': targetCType = ''
      targetC.moveToTable(xPos - (cwidth(targetC) * playerside / 2 * countCaptures), yPos, True)
      targetC.sendToBack()
      targetC.isFaceUp = False
      targetC.orientation = Rot0
      targetC.highlight = CapturedColor
      targetC.target(False)
      if debugVerbosity >= 2: notify("About to reset shared variable")
      setGlobalVariable('Captured Cards',str(capturedCards))
      if debugVerbosity >= 2: notify("About to initiate autoscripts")
      autoscriptOtherPlayers('{}CardCapturedFrom{}'.format(targetCType,captureGroup),targetC) # We send also the card type. Some capture hooks only trigger of a specific kind of captured card (e.g. bespin exchange)
   if debugVerbosity >= 1: notify("<<< capture()") #Debug

def clearAttachLinks(card):
# This function takes care to discard any attachments of a card that left play (discarded or captured)
# It also clear the card from the host dictionary, if it was itself attached to another card
   if debugVerbosity >= 1: notify(">>> clearAttachLinks()") #Debug
   hostCards = eval(getGlobalVariable('Host Cards'))
   cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == card._id])
   if cardAttachementsNR >= 1:
      hostCardSnapshot = dict(hostCards)
      for attachment in hostCardSnapshot:
         if hostCardSnapshot[attachment] == card._id:
            if Card(attachment) in table: discard(Card(attachment))
            del hostCards[attachment]
   if debugVerbosity >= 2: notify("### Checking if the card is attached to unlink.")      
   if hostCards.has_key(card._id): del hostCards[card._id] # If the card was an attachment, delete the link
   setGlobalVariable('Host Cards',str(hostCards))
   if debugVerbosity >= 3: notify("<<< clearAttachLinks()") #Debug
   
def removeCapturedCard(card): # This function removes a captured card from the dictionary which records which cards are captured at which objective.
   if debugVerbosity >= 1: notify(">>> removeCapturedCard()") #Debug
   try: 
      mute()
      capturedCards = eval(getGlobalVariable('Captured Cards'))
      if capturedCards.has_key(card._id):
         if debugVerbosity >= 2: notify("{} was in the capturedCards dict.".format(card))
         del capturedCards[card._id]
         if debugVerbosity >= 3: notify("Double Checking if entry exists: {}".format(capturedCards.get(card._id,'DELETED')))
      card.highlight = None
      if debugVerbosity >= 4: 
         notify("Captured Cards: {}".format([Card(id).name for id in capturedCards]))
         rnd(1,10)
      setGlobalVariable('Captured Cards',str(capturedCards))
   except: notify("!!!ERROR!!! in removeCapturedCard()") # Debug
   if debugVerbosity >= 3: notify("<<< removeCapturedCard()") #Debug

def rescueFromObjective(obj): # THis function returns all captured cards from an objective to their owner's hand
   try:
      count = 0
      capturedCards = eval(getGlobalVariable('Captured Cards')) # This is a dictionary holding how many and which cards are captured at each objective.
      for capturedC in capturedCards: # We check each entry in the dictionary. Each entry is a card's unique ID
         if capturedCards[capturedC] == obj._id: # If the value we have for that card's ID is the unique ID of the current dictionary, it means that card is currently being captured at our objective.
            count += 1 # We count how many captured cards we found
            rescuedC = Card(capturedC) # We generate the card object by the card's unique ID
            removeCapturedCard(rescuedC) # We remove the card from the dictionary
            rescuedC.moveTo(rescuedC.owner.hand) # We return the card to its owner's hand
            autoscriptOtherPlayers('CardRescued',rescuedC) # We check if any card on the table has a trigger out of rescued cards.
      return count
   except: notify("!!!ERROR!!! in rescueFromObjective()") # Debug

def clearCaptures(card, x=0, y=0): # Simply clears all the cards that the game thinks the objective has captured
   capturedCards = eval(getGlobalVariable('Captured Cards')) # This is a dictionary holding how many and which cards are captured at each objective.
   for capturedC in capturedCards: # We check each entry in the dictionary. Each entry is a card's unique ID
      if capturedCards[capturedC] == card._id: # If the value we have for that card's ID is the unique ID of the current dictionary, it means that card is currently being captured at our objective.
         removeCapturedCard(Card(capturedC)) # We remove the card from the dictionary
   whisper("All associated captured cards for this objective have been cleared")
   
def rescue(card,x = 0, y = 0):
   removeCapturedCard(card) 
   card.moveTo(card.owner.hand)

def exileCard(card, silent = False):
   if debugVerbosity >= 1: notify(">>> exileCard(){}".format(extraASDebug())) #Debug
   # Puts the removed card in the player's removed form game pile.
   mute()
   storeProperties(card)
   if card.Type == "Affiliation" or card.Type == "BotD": 
      whisper("This isn't the card you're looking for...")
      return 'ABORT'
   else:
      if card.highlight != CapturedColor: executePlayScripts(card,'TRASH') # We don't want to run automations on simply revealed cards.
      card.moveTo(me.piles['Removed from Game'])
   if not silent: notify("{} removed {} from play{}.".format(me,card))
   executePlayScripts(card, 'DISCARD')
 
def inspectCard(card, x = 0, y = 0): # This function shows the player the card text, to allow for easy reading until High Quality scans are procured.
   if debugVerbosity >= 1: notify(">>> inspectCard(){}".format(extraASDebug())) #Debug
   #if debugVerbosity > 0: finalTXT = 'AutoScript: {}\n\n AutoAction: {}'.format(CardsAS.get(card.model,''),CardsAA.get(card.model,''))
   if card.model == "e31c2ba8-3ffc-4029-94fd-5f98ee0d78cc": 
      information("This is the Balance of the Force card.\
                 \nIt automatically flips during the force resolution depending on who has the most force commited\
               \n\nIf for some reason the force struffle calculation did not give an accurate result, you can simply double click this card to flip it manually.")
   elif card.Type == 'Affiliation':
      information("This is the {} affiliation card.\
                 \nIt does not have any abilities other than providing {} resources.\
               \n\nTo produce the resources simply attempt to play a card from your hand and then double click this card.".format(card.Affiliation, card.Affiliation))
   else:          
      if debugVerbosity >= 0: finalTXT = "{}\n\nTraits:{}\n\nCard Text: {}\n\nAS: {}\n\nAA: {}".format(card.name, card.Traits, card.Text,CardsAS.get(card.model,'N/A'),CardsAA.get(card.model,'N/A'))
      else: finalTXT = "{}\n\nTraits:{}\n\nCard Text: {}".format(card.name, card.Traits, card.Text)
      information("{}".format(finalTXT))

def inspectTargetCard(group, x = 0, y = 0): # This function shows the player the card text, to allow for easy reading until High Quality scans are procured.
   if debugVerbosity >= 1: notify(">>> inspectTargetCard(){}".format(extraASDebug())) #Debug
   for card in table:
      if card.targetedBy and card.targetedBy == me: inspectCard(card)

def concede(group,x=0,y=0):
   notify("=== {} Concedes the Game ===".format(me))
      
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
   extraTXT = ''
   if card.Type == 'Fate': 
      playEdge(card)
      return # If the player double clicked on a Fate card, assume he wanted to play it as an edge card.
   if card.Type == 'Enhancement':
      hostType = re.search(r'Placement:([A-Za-z1-9:_ ]+)', CardsAS.get(card.model,''))
      if hostType:
         if debugVerbosity >= 2: notify("### hostType: {}.".format(hostType.group(1))) #Debug
         host = findTarget('Targeted-at{}'.format(hostType.group(1)))
         if host == []: 
            whisper("ABORTING!")
            return
         else: extraTXT = ' on {}'.format(host[0])
   if re.search(r'Limited\.',card.Text):
      global limitedPlayed
      if limitedPlayed:
         if confirm("You've already played a limited card this turn. Bypass?"):
            extraTXT += " (Bypassing Limit!)"
         else: return
      else: limitedPlayed = True
   if re.search(r'Unique',card.Traits):
      foundUnique = None
      for c in table:
         if c.name == card.name: 
            foundUnique = c
            break
      if foundUnique:
         if foundUnique.owner == me: confirmTXT = "This card is unique and you already have a copy of {} in play.\n\nBypass uniqueness restriction?".format(foundUnique.name)
         else: confirmTXT = "This card is unique and {} already has a copy of {} in play.\n\nBypass uniqueness restriction?".format(foundUnique.owner.name,foundUnique.name)
         if confirm(confirmTXT):
            extraTXT += " (Bypassing Uniqueness Restriction!)"
         else: return         
   card.moveToTable(0, 0 + yaxisMove(card))
   if num(card.Cost) > 0 or card.Type == 'Event': # We do not trigger events automatically, in order to give the opponent a chance to play counter cards
      card.highlight = UnpaidColor                # We let everything else, as I'm not aware of cards which cancel units or enhancements coming into play.
      unpaidCard = card
      notify("{} attempts to play {}{}.".format(me, card,extraTXT))
      global warnZeroCostEvents
      if num(card.Cost) == 0 and card.Type == 'Event' and warnZeroCostEvents: 
         information("This event may have 0 cost, but we've set it as unpaid in order to allow your opponent to play interrupts.\
                    \nOnce your opponent had the chance to play any interrupts, double click on the event to finalize playing it and trigger any effects.\
                  \n\n(This message will not appear again")
         warnZeroCostEvents = False
   else: 
      placeCard(card)
      notify("{} plays {}{}.".format(me, card,extraTXT))
      executePlayScripts(card, 'PLAY') # We execute the play scripts here only if the card is 0 cost.
      autoscriptOtherPlayers('CardPlayed',card)

def playEdge(card):
   if debugVerbosity >= 1: notify(">>> playEdge(){}".format(extraASDebug())) #Debug
   if getGlobalVariable('Engaged Objective') == 'None': 
      whisper(":::ERROR::: You have to be in an engagement to play edge cards. ABORTING!")
      return
   if num(getGlobalVariable('Engagement Phase')) < 3: nextPhase(setTo = 3)
   global edgeCount
   mute()
   card.moveToTable(playerside * 450, (playerside * 30) + yaxisMove(card) + (playerside * 40 * edgeCount), True)
   card.highlight = EdgeColor
   edgeCount += 1
   if edgeCount > 7: edgeCount = 0 # Just in case.
   edgeRevealed = eval(getGlobalVariable('Revealed Edge'))
   edgeRevealed[card.owner.name] = False # Clearing some variables just in case they were left over. 
   setGlobalVariable('Revealed Edge',str(edgeRevealed))
   notify("{} places a card in their edge stack.".format(me, card))
   
def revealEdge(group = table, x=0, y=0, forceCalc = False):
   mute()
   if debugVerbosity >= 1: notify(">>> revealEdge(){}".format(extraASDebug())) #Debug
   if num(getGlobalVariable('Engagement Phase')) < 3: nextPhase(setTo = 3)
   edgeRevealed = eval(getGlobalVariable('Revealed Edge'))
   if not edgeRevealed.get(me.name,False) and not forceCalc:
      fateNr = 0
      edgeNr = 0
      if debugVerbosity >= 2: notify("Edge cards not revealed yet. About to do that") #Debug
      for card in table:
         if card.highlight == EdgeColor and not card.isFaceUp and card.owner == me:
            card.isFaceUp = True
            if card.Type == 'Fate': 
               fateNr += 1
               card.highlight = FateColor
            edgeNr += 1
      if fateNr > 0: extraTXT = " They have {} fate cards".format(fateNr)
      else: extraTXT = ''
      if edgeNr > 0: notify("{} reveals their edge stack.{}".format(me,extraTXT))
      else: notify("{} has played no edge cards for this engagement.".format(me))
      edgeRevealed[me.name] = True
      setGlobalVariable('Revealed Edge',str(edgeRevealed))
   else:
      if debugVerbosity >= 2: notify("Edge cards already revealed. Gonna calculate edge") #Debug
      if forceCalc: # forceCalc is only used to make sure the edge has been assigned. If a player already has the edge, we don't change it
         for player in players: # This is because they may have calculated the edge in the edge phase and discarded their edge cards laready.
            plAffiliation = getSpecial('Affiliation',player)
            if plAffiliation.markers[mdict['Edge']] and plAffiliation.markers[mdict['Edge']] == 1: return
      myEdgeTotal = 0
      opponentEdgeTotal = 0
      for card in table:
         if debugVerbosity >= 4: notify("#### Checking {}".format(card)) #Debug
         if (card.highlight == EdgeColor or card.highlight == FateColor) and card.isFaceUp:
            if card.owner == me: myEdgeTotal += num(card.Force)
            else: opponentEdgeTotal += num(card.Force)
            if card.highlight == FateColor: notify(":::WARNING::: {} has not yet resolved their {}".format(card.owner,card))
         bonusEdge = re.search(r'Edge([0-9])Bonus',CardsAS.get(card.model,''))
         if bonusEdge and card.orientation == Rot90:
            if debugVerbosity >= 2: notify("### Found card with Bonus edge") #Debug
            if card.controller == me: myEdgeTotal += num(bonusEdge.group(1))
            else: opponentEdgeTotal += num(bonusEdge.group(1))
      currentTarget = Card(num(getGlobalVariable('Engaged Objective'))) # We find out what the current objective as we can use it to figure out if we're an attacker or defender.
      if myEdgeTotal > opponentEdgeTotal:
         if debugVerbosity >= 2: notify("### I've got the edge") #Debug
         if not (Affiliation.markers[mdict['Edge']] and Affiliation.markers[mdict['Edge']] == 1): 
         # We check to see if we already have the edge marker on our affiliation card (from our opponent running the same script)
            clearEdgeMarker() # We clear the edge, in case another player's affiliation card had it
            Affiliation.markers[mdict['Edge']] = 1
            notify("The {} has the edge in this engagement ({}: {} force VS {}: {} force)".format(me,me, myEdgeTotal, opponent, opponentEdgeTotal))
            if currentTarget.controller == opponent: autoscriptOtherPlayers('AttackerEdgeWin',currentTarget)
            else: autoscriptOtherPlayers('DefenderEdgeWin',currentTarget)
         elif not forceCalc: whisper(":::NOTICE::: You already have the edge. Nothing else to do.")
      elif myEdgeTotal < opponentEdgeTotal:
         if debugVerbosity >= 2: notify("### Opponent has the edge") #Debug
         oppAffiliation = getSpecial('Affiliation',opponent)
         if not (oppAffiliation.markers[mdict['Edge']] and oppAffiliation.markers[mdict['Edge']] == 1): 
         # We check to see if our opponent already have the edge marker on our affiliation card (from our opponent running the same script)
            clearEdgeMarker() # We clear the edge, in case another player's affiliation card had it
            oppAffiliation.markers[mdict['Edge']] = 1
            notify("The {} have the edge in this engagement ({}: {} force VS {}: {} force)".format(oppAffiliation,me, myEdgeTotal, opponent, opponentEdgeTotal))
            if currentTarget.controller == opponent: autoscriptOtherPlayers('AttackerEdgeWin',currentTarget)
            else: autoscriptOtherPlayers('DefenderEdgeWin',currentTarget)
         elif not forceCalc: whisper(":::NOTICE::: Your opponent already have the edge. Nothing else to do.")
      else: 
         if debugVerbosity >= 2: notify("### Edge is a Tie") #Debug
         if debugVerbosity >= 2: notify("### Finding defender's Affiliation card.") #Debug
         defenderAffiliation = getSpecial('Affiliation',currentTarget.controller)
         unopposed = True
         for card in table:
            if card.orientation == Rot90 and card.controller == currentTarget.controller: unopposed = False
         if unopposed: 
            if debugVerbosity >= 2: notify("### Unopposed Attacker") #Debug
            if not (Affiliation.markers[mdict['Edge']] and Affiliation.markers[mdict['Edge']] == 1): 
               clearEdgeMarker() # We clear the edge, in case another player's affiliation card had it
               Affiliation.markers[mdict['Edge']] = 1
               notify("The engagement of {} is unopposed, so {} automatically gains edge as the attacker.".format(currentTarget,me))
               autoscriptOtherPlayers('AttackerEdgeWin',currentTarget)
            elif not forceCalc: whisper(":::NOTICE::: The attacker already has the edge. Nothing else to do.")
         else:
            if debugVerbosity >= 2: notify("### Defender's Advantage") #Debug
            if not (defenderAffiliation.markers[mdict['Edge']] and defenderAffiliation.markers[mdict['Edge']] == 1): 
               clearEdgeMarker() # We clear the edge, in case another player's affiliation card had it
               defenderAffiliation.markers[mdict['Edge']] = 1
               notify("Nobody managed to get the upper hand in the edge struggle ({}: {} force VS {}: {} force), so {} retains the edge as the defender.".format(me, myEdgeTotal, opponent, opponentEdgeTotal,currentTarget.controller))
               autoscriptOtherPlayers('DefenderEdgeWin',currentTarget)
            elif not forceCalc: whisper(":::NOTICE::: The defender already has the edge. Nothing else to do.")
      if debugVerbosity >= 3: notify("<<< revealEdge()") #Debug

def groupToDeck (group = me.hand, player = me, silent = False):
   if debugVerbosity >= 1: notify(">>> groupToDeck(){}".format(extraASDebug())) #Debug
   mute()
   deck = player.piles['R&D/Stack']
   count = len(group)
   for c in group: c.moveTo(deck)
   if not silent: notify ("{} moves their whole {} to their {}.".format(player,pileName(group),pileName(deck)))
   if debugVerbosity >= 3: notify("<<< groupToDeck() with return:\n{}\n{}\n{}".format(pileName(group),pileName(deck),count)) #Debug
   return(pileName(group),pileName(deck),count) # Return a tuple with the names of the groups.
   
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
   drawMany(count = 6)   
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

def handRandomDiscard(group, count = None, player = None, destination = None, silent = False):
   if debugVerbosity >= 1: notify(">>> handRandomDiscard(){}".format(extraASDebug())) #Debug
   mute()
   if not player: player = me
   if not destination: destination = player.piles['Discard Pile']
   SSize = len(group)
   if SSize == 0: return 0
   if count == None: count = askInteger("Discard how many cards?", 1)
   if count == None: return 0
   if count > SSize : 
      count = SSize
      whisper("You do not have enough cards in your hand to complete this action. Will discard as many as possible")   
   for iter in range(count):
      if debugVerbosity >= 3: notify("#### : handRandomDiscard() iter: {}".format(iter + 1)) # Debug
      card = group.random()
      if card == None: return iter + 1 # If we have no more cards, then return how many we managed to discard.
      card.moveTo(destination)
      if not silent: notify("{} discards {} at random.".format(player,card))
   if debugVerbosity >= 2: notify("<<< handRandomDiscard() with return {}".format(iter + 1)) #Debug
   return iter + 1 #We need to increase the iter by 1 because it starts iterating from 0
   
def randomDiscard(group):
	mute()
	card = group.random()
	if card == None: return
	notify("{} randomly discards {}.".format(me,card.name))
	card.moveTo(me.piles['Discard Pile'])

def sendToBottom(cards,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> sendToBottom()") #Debug
   if debugVerbosity >= 1: notify("### Card List = {}".format([c.name for c in cards])) #Debug
   mute()
   if debugVerbosity >= 2: notify("### Original List: {}".format([card.name for card in cards])) #Debug
   for iter in range(len(cards)):
      if iter % 5 == 0: notify("---PLEASE DO NOT MOVE ANY CARDS AROUND---")
      if iter % 2 == 0: notify("Randomizing({}/{} done)...".format(iter, len(cards)))
      swap = rnd(iter,len(cards) - 1)
      cards[iter], cards[swap] = cards[swap], cards[iter]
   if debugVerbosity >= 2: notify("### Randomized List: {}".format([card.name for card in cards])) #Debug
   if cards[0].group == me.hand:
      notify("{} sends {} cards from their hand to the bottom of their respective decks in random order.".format(me,len(cards)))
   else:
      notify("{} sends {} to the bottom of their respective decks in random order.".format(me,[card.name for card in cards]))
   for card in cards: 
      if card.group == table: clearAttachLinks(card)
      card.moveToBottom(card.owner.piles['Command Deck'])

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
   if debugVerbosity >= 2: notify(">>> About to announce(){}") #Debug
   if not silent: notify("{}'s new objective is {}.".format(me,card))
   
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
      delayed_whisper("You do not have enough cards in your deck to complete this action. Will draw as many as possible")
   for c in group.top(count): 
      c.moveTo(destination)
   if not silent: notify("{} draws {} cards.".format(me, count))
   if debugVerbosity >= 3: notify("<<< drawMany() with return: {}".format(count))
   return count

def refillHand(group = me.hand): # Simply refills the player's hand to their reserve maximum
   if debugVerbosity >= 1: notify(">>> refillHand(){}".format(extraASDebug())) #Debug
   mute()
   global handRefillDone
   if len(me.hand) < me.Reserves: 
      drawMany(count = me.Reserves - len(me.hand))
   notify(":> {} Refills their hand to their reserve maximum".format(me))
   handRefillDone = True
   if debugVerbosity >= 3: notify("<<< refillHand()")
      
   
def drawBottom(group, x = 0, y = 0):
	if len(group) == 0: return
	mute()
	group.bottom().moveTo(me.hand)
	notify("{} draws a card from the bottom.".format(me))

def shuffle(group):
	group.shuffle()

#---------------------------------------------------------------------------
# Tokens and Markers
#---------------------------------------------------------------------------
	
def addFocus(card, x = 0, y = 0):
   mute()
   card.markers[mdict['Focus']] += 1
   notify("{} adds a Focus token on {} (Total: {}).".format(me, card, card.markers[mdict['Focus']]))
    
def addDamage(card, x = 0, y = 0):
   mute()
   card.markers[mdict['Damage']] += 1    
   notify("{} adds a Damage token on {} (Total: {}).".format(me, card, card.markers[mdict['Damage']]))
    
def addShield(card, x = 0, y = 0):
   mute()
   if card.markers[mdict['Shield']] and card.markers[mdict['Shield']] >= 1 and not confirm("This {} already has a shield. You are normally allowed only one shield per card.\n\nBypass Restriction?".format(card.Type)): return
   notify("{} adds a Shield token on {}.".format(me, card))
   card.markers[mdict['Shield']] += 1        

def addFocusTarget(group, x = 0, y = 0):
   mute()
   for card in table:
      if card.targetedBy and card.targetedBy == me:
         card.markers[mdict['Focus']] += 1
         notify("{} adds a Focus token on {} (Total: {}).".format(me, card, card.markers[mdict['Focus']]))
    
def addDamageTarget(group, x = 0, y = 0):
   mute()
   for card in table:
      if card.targetedBy and card.targetedBy == me:
         card.markers[mdict['Damage']] += 1    
         notify("{} adds a Damage token on {} (Total: {}).".format(me, card, card.markers[mdict['Damage']]))
    
def addShieldTarget(group, x = 0, y = 0):
   mute()
   for card in table:
      if card.targetedBy and card.targetedBy == me:
         if card.markers[mdict['Shield']] and card.markers[mdict['Shield']] >= 1 and not confirm("{} already has a shield. You are normally allowed only one shield per card.\n\nBypass Restriction?".format(card.name)): return
         card.markers[mdict['Shield']] += 1        
         notify("{} adds a Shield token on {}.".format(me, card))

def subFocus(card, x = 0, y = 0):
   subToken(card, 'Focus')

def subDamage(card, x = 0, y = 0):
   subToken(card, 'Damage')

def subShield(card, x = 0, y = 0):
   subToken(card, 'Shield')

def subFocusTarget(group, x = 0, y = 0):
   for card in table:
      if card.targetedBy and card.targetedBy == me: subToken(card, 'Focus')

def subDamageTarget(group, x = 0, y = 0):
   for card in table:
      if card.targetedBy and card.targetedBy == me: subToken(card, 'Damage')

def subShieldTarget(group, x = 0, y = 0):
   for card in table:
      if card.targetedBy and card.targetedBy == me: subToken(card, 'Shield')

def subToken(card, tokenType):
   mute()
   notify("{} removes a {} from {}.".format(me, tokenType, card))
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
         
def gainEdge(card, x = 0, y = 0):
   mute()
   clearEdgeMarker()
   notify("{} gains the Egde.".format(me))
   Affiliation.markers[mdict['Edge']] = 1             
   
def findCounterPrevention(count, counter, targetPL): # Find out if the player has any markers preventing them form gaining specific counters (Credits, Agenda Points etc)
   if debugVerbosity >= 1: notify(">>> findCounterPrevention(){}".format(extraASDebug())) #Debug
   preventionFound = 0
   forfeit = None
   preventionType = 'preventCounter:{}'.format(counter)
   forfeitType = 'forfeitCounter:{}'.format(counter)
   cardList = [c for c in table
               if c.controller == targetPL
               and c.markers]
   for card in sortPriority(cardList):
      foundMarker = findMarker(card, preventionType)
      if not foundMarker: foundMarker = findMarker(card, forfeitType)
      if foundMarker: # If we found a counter prevention marker of the specific type we're looking for...
         while count > 0 and card.markers[foundMarker] > 0: # For each point of damage we do.
            preventionFound += 1 # We increase the prevention found by 1
            count -= 1 # We reduce how much counter we still need to add by 1
            card.markers[foundMarker] -= 1 # We reduce the specific counter prevention counters by 1
         if count == 0: break # If we've found enough protection to alleviate all counters, stop the search.
   if debugVerbosity >= 3: notify("<<< findCounterPrevention() by returning: {}".format(preventionFound))
   return preventionFound   
 
#---------------------------------------------------------------------------
# Announcements
#--------------------------------------------------------------------------- 

def declarePass(group, x=0, y=0):
   notify("{} Passes".format(me))

