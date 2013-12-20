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
SetupPhase = False
unpaidCard = None # A variable that holds the card object of a card that has not been paid yet, for ease of find.
edgeRevealed = False # Remembers if the player has revealed their edge cards yet or not.
firstTurn = True # A variable to allow the engine to skip some phases on the first turn.
handRefillDone = False # A variable which tracks if the player has refilled their hand during the draw phase. Allows the game to go faster.
forceStruggleDone = False # A variable which tracks if the player's have actually done the force struggle for this turn (just in case it's forgotten)
ModifyDraw = 0 # When 1 it signifies an effect that affects the number of cards drawn per draw.
limitedPlayed = False # A Variable which records if the player has played a limited card this turn
capturingObjective = None # A global variable which holds which objective just captured a card.

#---------------------------------------------------------------------------
# Phases
#---------------------------------------------------------------------------

def showCurrentPhase(phaseNR = None): # Just say a nice notification about which phase you're on.
   if phaseNR: notify(phases[phaseNR])
   else:
      if getGlobalVariable('Engaged Objective') != 'None':
         notify(engagementPhases[num(getGlobalVariable('Engagement Phase'))])
      else:
         phaseRegex = re.search(r'(Dark|Light):([0-6])',getGlobalVariable('Phase'))
         debugNotify("phaseRegex groups = {}".format(phaseRegex.groups()),4)
         if not phaseRegex: 
            notify(":::ERROR::: Something went wrong with the phase set. Resetting to Dark:0")
            setGlobalVariable('Phase','Dark:0')
            return
         notify(phases[num(phaseRegex.group(2))])
   
def nextPhase(group = table, x = 0, y = 0, setTo = None):  
# Function to take you to the next phase. 
   global firstTurn
   debugNotify(">>> nextPhase()") #Debug
   mute()
   clearAllEffects(True) # First we clear all non-used triggered effects.
   if getGlobalVariable('Engaged Objective') != 'None':
      debugNotify("We got engaged objective")
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
      debugNotify("Normal Phase change")
      phaseRegex = re.search(r'(Dark|Light):([0-6])',getGlobalVariable('Phase'))
      debugNotify("phaseRegex groups = {}".format(phaseRegex.groups()),3)
      debugNotify("phaseRegex group(1) = [{}]. My Side = [{}]".format(phaseRegex.group(1), Side),4)
      if not phaseRegex: 
         notify(":::ERROR::: Something went wrong with the phase set. Resetting to Dark:0")
         setGlobalVariable('Phase','Dark:0')
         return
      if phaseRegex.group(1) != Side:
         debugNotify("Not currently the active Side")
         if confirm(":::WARNING::: It is not the {} side turn yet. Do you want to bypass and jump to your own refresh phase?".format(Side)):
            grabTurn(findAlly()) # Give the turn to ally in position #1
            setGlobalVariable('Phase','{}:0'.format(Side))
            phase = 0
         else: return  
      phase = num(phaseRegex.group(2))
      if Side == 'Light': opSide = 'Dark'
      else: opSide = 'Light'
      if phase == 6: 
         debugNotify("We'at turn End")
         if not forceStruggleDone and Automations['Start/End-of-Turn/Phase']: resolveForceStruggle() # If the player forgot to do their force stuggle, then we just do it quickly for them.
         setGlobalVariable('Phase','{}:0'.format(opSide)) # In case we're on the last phase (Force), we end our turn.
         atTimedEffects(Time = 'End') # Scripted events at the end of the player's turn
         notify("=== The {} side has ended their turn ===.".format(Side))
         opponent = findOpponent()
         opponent.setActivePlayer() # new in OCTGN 3.0.5.47 
         for card in table:
            if card.markers[mdict['Activation']]: card.markers[mdict['Activation']] = 0 # At the end of each turn we clear the once-per turn abilities.
         debugNotify("Exiting Because we've finished our turn")
         return
      else: 
         debugNotify("Normal Phase change")
         phase += 1
         #setGlobalVariable('Phase','{}:{}'.format(Side,str(phase))) # Otherwise, just move up one phase # Prolly unnecessary 
      if phase == 1: goToBalance()
      elif phase == 2: goToRefresh()
      elif phase == 3: goToDraw()
      elif phase == 4: 
         if not handRefillDone and Automations['Start/End-of-Turn/Phase']: refillHand() # If the player forgot to refill their hand in the Draw Phase, do it automatically for them now.
         goToDeployment()
      elif phase == 5:
         if firstTurn and Side == 'Dark':
            notify(":::NOTICE::: The Dark Side skips their first conflict phase".format(me))
            clearFirstTurn()
            goToForce()
         else: goToConflict()
      elif phase == 6: goToForce()

def goToBalance(group = table, x = 0, y = 0): # Go directly to the Balance phase
   if debugVerbosity >= 1: notify(">>> goToBalance(){}".format(extraASDebug())) #Debug
   mute()
   atTimedEffects(Time = 'Start') # Scripted events at the start of the player's turn
   phaseRegex = re.search(r'(Dark|Light):([0-6])',getGlobalVariable('Phase'))
   if not phaseRegex: 
      notify(":::ERROR::: Something went wrong with the phase set. Resetting to Dark:0")
      setGlobalVariable('Phase','Dark:0')
      return
   if phaseRegex.group(1) != Side:
      if not confirm("The opposing side has not finished their turn yet. Are you sure you want to continue to your own balance phase?"): return
      else: grabTurn(findAlly())
   setGlobalVariable('Phase','{}:1'.format(Side))
   showCurrentPhase(1)
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
         incrStat('forceturns',me.name) # We store that the opponent has won a force struggle
      else:
         modifyDial(1)
         notify(":> The Death Star dial advances by 1")
   else:
      if haveForce():
         objectiveList = []
         for opponent in fetchAllOpponents():
            opponentObjectives = eval(opponent.getGlobalVariable('currentObjectives'))
            objectiveList.extend([Card(objective_ID) for objective_ID in opponentObjectives])
         choice = SingleChoice("The Balance of the Force is in your favour. Choose one Dark Side objective to damage.", makeChoiceListfromCardList(objectiveList), default = 0)
         if choice == None: return
         chosenObj = Card(opponentObjectives[choice])
         addMarker(chosenObj, 'Damage',1, True)
         notify(":> The Force is with the Light Side! The rebel forces press the advantage and damage {}".format(chosenObj))      
         incrStat('forceturns',me.name) # We store that the opponent has won a force struggle
         
def goToRefresh(group = table, x = 0, y = 0): # Go directly to the Refresh phase
   if debugVerbosity >= 1: notify(">>> goToRefresh(){}".format(extraASDebug())) #Debug
   atTimedEffects(Time = 'afterBalance')   
   mute()
   setGlobalVariable('Phase','{}:2'.format(Side))
   showCurrentPhase(2)
   if not Automations['Start/End-of-Turn/Phase']: return
   if not firstTurn: notify(":> {} refreshed all their cards".format(me))   
   if firstTurn and Side == 'Light':
      notify(":::NOTICE::: The Light Side skips their first card refresh")
      clearFirstTurn()
   else:
      for card in table:
         if card.controller == me and card.highlight != CapturedColor:
            if debugVerbosity >= 2: notify("### Removing Focus Tokens")
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
   atTimedEffects(Time = 'afterCardRefreshing') 
   
def goToDraw(group = table, x = 0, y = 0): # Go directly to the Draw phase
   if debugVerbosity >= 1: notify(">>> goToDraw(){}".format(extraASDebug())) #Debug
   atTimedEffects(Time = 'afterRefresh') # We put "afterRefresh" in the refresh phase, as cards trigger immediately after refreshing. Not after the refresh phase as a whole.
   mute()
   global handRefillDone
   handRefillDone = False
   setGlobalVariable('Phase','{}:3'.format(Side))
   showCurrentPhase(3)
   if not Automations['Start/End-of-Turn/Phase']: return
   if len(me.hand) == 0: refillHand() # If the player's hand is empty, there's no option to take. Just refill.
   
def goToDeployment(group = table, x = 0, y = 0): # Go directly to the Deployment phase
   if debugVerbosity >= 1: notify(">>> goToDeployment(){}".format(extraASDebug())) #Debug
   atTimedEffects(Time = 'afterDraw')
   mute()
   setGlobalVariable('Phase','{}:4'.format(Side))
   showCurrentPhase(4)   
   if not Automations['Start/End-of-Turn/Phase']: return
   
def goToConflict(group = table, x = 0, y = 0): # Go directly to the Conflict phase
   if debugVerbosity >= 1: notify(">>> goToConflict(){}".format(extraASDebug())) #Debug
   atTimedEffects(Time = 'afterDeployment')   
   mute()
   setGlobalVariable('Phase','{}:5'.format(Side))
   showCurrentPhase(5)   
   if not Automations['Start/End-of-Turn/Phase']: return

def goToForce(group = table, x = 0, y = 0): # Go directly to the Force phase
   if debugVerbosity >= 1: notify(">>> goToForce(){}".format(extraASDebug())) #Debug
   atTimedEffects(Time = 'afterConflict')   
   mute()
   global forceStruggleDone
   forceStruggleDone = False # At the start of the force phase, the force struggle is obviously not done yet.
   if getGlobalVariable('Engaged Objective') != 'None': finishEngagement() # If the playes jump to the force phase after engagement, we make sure we clear the engagement.
   setGlobalVariable('Phase','{}:6'.format(Side))
   showCurrentPhase(6)
   delayed_whisper(":::ATTENTION::: Once you've committed all the units you want to the force, press Ctrl+F6 to resolve the force struggle")
   if not Automations['Start/End-of-Turn/Phase']: return

def resolveForceStruggle(group = table, x = 0, y = 0): # Calculate Force Struggle
   mute()
   if not re.search(r'6',getGlobalVariable('Phase')) and not confirm("The force struggle is only supposed to happen at the end of your force phase. Bypass?"):
      return # If it's not the force phase, give the player an opportunity to abort.
   global forceStruggleDone
   myStruggleTotal = 0
   opponentStruggleTotal = 0
   if Side == 'Light': 
      commitColor = LightForceColor
      commitOpponent = DarkForceColor
      opSide = 'Dark'
   else: 
      commitColor = DarkForceColor
      commitOpponent = LightForceColor
      opSide = 'Light'
   debugNotify("### Counting my committed cards") #Debug
   commitedCards = [c for c in table if c.controller in myAllies and (c.highlight == commitColor or findMarker(c, "Unwavering Resolve"))]
   debugNotify("### About to loop") #Debug
   for card in commitedCards:
      try: 
         if card.markers[mdict['Focus']] == 0 or findMarker(card, "Unwavering Resolve") or re.search(r'ConstantEffect:Unwavering',CardsAS.get(card.model,'')): myStruggleTotal += num(card.Force)
         # We only include cards in the force struggle if they are not exausted and/or have a special ability on them
      except: myStruggleTotal += num(card.Force) # If there's an exception, it means the card didn't ever have a focus marker
   debugNotify("### Counting my opponents cards") #Debug
   opponentCommitedCards  = [c for c in table if c.highlight == commitOpponent]
   for card in opponentCommitedCards:
      try: 
         if card.markers[mdict['Focus']] == 0 or findMarker(card, "Unwavering Resolve") or re.search(r'ConstantEffect:Unwavering',CardsAS.get(card.model,'')): opponentStruggleTotal += num(card.Force)
      except: opponentStruggleTotal += num(card.Force) # If there's an exception, it means the card didn't ever have a focus marker
   debugNotify("### About to check for bonus force cards") #Debug
   for c in table:
      debugNotify("Checking {}".format(c),4) #Debug
      Autoscripts = CardsAS.get(c.model,'').split('||')
      for autoS in Autoscripts:
         debugNotify("autoS: {}".format(autoS),4) #Debug
         bonusForce = re.search(r'Force([0-9])Bonus',autoS)
         if bonusForce:
            targetCards = findTarget(autoS,card = c) # Some cards give a bonus according to other cards on the table (e.g. Self Preservation). So we gather those cards by an AutoTargeted search
            multiplier = per(autoS, targetCards = targetCards) # Then we calculate the multiplier with per()
            debugNotify("### Found card with Bonus force") #Debug
            fBonus = (num(bonusForce.group(1)) * multiplier)
            if c.controller == me: myStruggleTotal += fBonus
            else: opponentStruggleTotal += fBonus
            if fBonus: notify("-- {}: +{} force total for {}".format(c,fBonus,c.controller))
   debugNotify("### Checking Struggle") #Debug
   BotD = getSpecial('BotD')
   if myStruggleTotal - opponentStruggleTotal > 0: 
      debugNotify("### struggleTotal Positive") #Debug
      if (Side == 'Light' and not BotD.alternate == '') or (Side == 'Dark' and not BotD.alternate == 'DarkSide'):
         debugNotify("About to flip BotD due to my victory") #Debug
         if Side == 'Light': BotD.switchTo()
         else: BotD.switchTo('DarkSide')
         firstPlayer = findAlly()
         mainAffiliation = getSpecial('Affiliation',firstPlayer)
         x,y = mainAffiliation.position
         debugNotify("First Affiliation is {} at position {} {}".format(mainAffiliation, x,y,)) #Debug
         BotD.moveToTable(x, y + (playerside * 75))
         notify(":> The force struggle tips the balance of the force towards the {} side ({}: {} - {}: {})".format(Side,Side,myStruggleTotal,opSide,opponentStruggleTotal))
      else: notify(":> The balance of the force remains skewed towards the {}. ({}: {} - {}: {})".format(Side,Side,myStruggleTotal,opSide,opponentStruggleTotal))         
      autoscriptOtherPlayers('ForceStruggleWon',BotD)
      incrStat('forcev',me.name) # We store that the player has won a force struggle
   elif myStruggleTotal - opponentStruggleTotal < 0: 
      debugNotify("struggleTotal Negative") #Debug
      if (Side == 'Light' and BotD.alternate == '') or (Side == 'Dark' and BotD.alternate == 'DarkSide'):
         debugNotify("About to flip BotD due to my opponent's victory") #Debug
         if Side == 'Light': BotD.switchTo('DarkSide')
         else: BotD.switchTo()
         firstOpponent = findOpponent()
         opponentAffiliation = getSpecial('Affiliation',firstOpponent)
         x,y = opponentAffiliation.position
         debugNotify("firstOpponent Affiliation is {} at position {} {}".format(opponentAffiliation, x,y,)) #Debug
         BotD.moveToTable(x - (playerside * 70), y)
         notify(":> The force struggle tips the balance of the force towards the {} side ({}: {} - {}: {})".format(firstOpponent.getGlobalVariable('Side'),Side,myStruggleTotal,opSide,opponentStruggleTotal))
      else: notify(":> The balance of the force remains skewed towards the {}. ({}: {} - {}: {})".format(firstOpponent.getGlobalVariable('Side'),Side,myStruggleTotal,opSide,opponentStruggleTotal))
      autoscriptOtherPlayers('ForceStruggleLost',BotD)
      incrStat('forcev',firstOpponent.name) # We store that the opponent has won a force struggle
   else: # If the current force totals are tied, we just announce that.
      debugNotify("Force struggle is tied") #Debug
      if BotD.alternate == 'DarkSide': BotDside = 'Dark'
      else: BotDside = 'Light'
      notify(":> The force struggle is tied. The Balance remains tiped to the {} Side. ({}: {} - {}: {})".format(BotDside,Side,myStruggleTotal,opSide,opponentStruggleTotal))
      if debugVerbosity >= 0:
         if confirm("Debug Force Win/Loss?"):
            if confirm("Win Force?"): autoscriptOtherPlayers('ForceStruggleWon',BotD)
            else: autoscriptOtherPlayers('ForceStruggleLost',BotD)
   forceStruggleDone = True # Set that the forcestruggle is done.
   debugNotify("<<< resolveForceStruggle()") #Debug
         
def engageTarget(group = table, x = 0, y = 0,targetObjective = None,silent = False): # Start an Engagement Phase
   if debugVerbosity >= 1: notify(">>> engageTarget(){}".format(extraASDebug())) #Debug
   mute()
   if not re.search(r'5',getGlobalVariable('Phase')) and not confirm("You need to be in the conflict phase before you can engage an objective. Bypass?"):
      return
   if getGlobalVariable('Engaged Objective') != 'None': finishEngagement() 
   if debugVerbosity >= 2: notify("About to find targeted objectives.") #Debug
   if not targetObjective:
      cardList = [c for c in table if (c.Type == 'Objective' or re.search(r'EngagedAsObjective',CardsAS.get(c.model,''))) and c.targetedBy and c.targetedBy == me and c.controller in fetchAllOpponents()]
      if debugVerbosity >= 2: notify("About to count found objectives list. List is {}".format(cardList)) #Debug
      if len(cardList) == 0: 
         whisper("You need to target an opposing Objective to start an Engagement")
         return
      else: targetObjective = cardList[0]
   targetObjective.highlight = DefendColor
   if debugVerbosity >= 2: notify("About set the global variable") #Debug
   setGlobalVariable('Engaged Objective',str(targetObjective._id))
   setGlobalVariable('Current Attacker',str(me._id))
   showCurrentPhase()
   #setGlobalVariable('Engagement Phase','1')
   if debugVerbosity >= 2: notify("About to announce") #Debug
   if not silent: notify("{} forces have engaged {}'s {}".format(me,targetObjective.controller, targetObjective))
   rnd(1,10)
   autoscriptOtherPlayers('EngagedObjective',targetObjective)
   incrStat('attacks',me.name) # We store that the player has attacked an objective
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
   if len(players) == 1 and debugVerbosity >= 0 and confirm("Set unopposed for single-player debug?"): unopposed = True # last part is for Debug
   if (unopposed and currentTarget in table): 
      # We need to check for special restrictions for unopposed battles
      # These are by hardcoded for now, until I see more of them.
      cancel = False
      unopposedDamage = 1
      for c in table:
         debugNotify("### Checking unopposed effects from {}".format(c), 4) # Debug
         if c.name == 'Echo Base Defense' and re.search(r'Hoth',currentTarget.Traits) and currentTarget.controller == c.controller:
            if debugVerbosity >= 2: notify("### Found Echo Base Defense")
            HothControllers = compareObjectiveTraits('Hoth')
            if len(HothControllers) == 1 and HothControllers[0] == c.controller:
               cancel = True
               notify(":> The engagement at {} finished unopposed, but the extra damage is prevented by {}'s Echo Base Defense.".format(currentTarget,c.controller))
               break
         Autoscripts = CardsAS.get(c.model,'').split('||')
         for autoS in Autoscripts:
            debugNotify("autoS: {}".format(autoS),4) #Debug
            raiseUnopposed = re.search(r'Unopposed([0-9])Raise',autoS)
            if raiseUnopposed and chkPlayer(autoS, c.controller, False) and checkOriginatorRestrictions(autoS,c):
               debugNotify("Found unopposed Raise: {}".format(raiseUnopposed.group(1)),4) #Debug
               targetCards = findTarget(autoS, card = c) # Some cards give a bonus according to other cards on the table. So we gather those cards by an AutoTargeted search
               multiplier = per(autoS, targetCards = targetCards) # Then we calculate the multiplier with per()
               if debugVerbosity >= 2: notify("### Found card which raises unopposed bonus") #Debug
               uBonus = (num(raiseUnopposed.group(1)) * multiplier)
               if uBonus > unopposedDamage:
                  if uBonus: notify("-- {} raises Unopposed damage to {}".format(c,uBonus))
                  unopposedDamage = uBonus
      if not cancel:
         debugNotify("### Unopposed Damage not cancelled")
         if currentTarget.controller.getGlobalVariable('Side') == 'Dark': attackerSide = 'Light'
         else: attackerSide = 'Dark'
         if debugVerbosity >= 1: notify("Unopposed prolly Happens because debugVerbosity >= 1")
         else: notify(":> The {} Side managed to finish the engagement at {} unopposed. They inflict {} extra damage to the objective.".format(attackerSide,currentTarget,unopposedDamage))
         addMarker(currentTarget, 'Damage',unopposedDamage, True)
         autoscriptOtherPlayers('UnopposedEngagement',currentTarget)
   autoscriptOtherPlayers('FinishedEngagement',currentTarget)
   for card in table:
      if card.orientation == Rot90: card.orientation = Rot0
      if card.highlight == DefendColor: card.highlight = None
   notify("The engagement at {} is finished.".format(Card(num(getGlobalVariable('Engaged Objective')))))
   setGlobalVariable('Engaged Objective','None')
   setGlobalVariable('Current Attacker','None')
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
   global SetupPhase
   deck = me.piles['Command Deck']
   objectives = me.piles['Objective Deck']
   if SetupPhase and len(me.hand) != 1: # If the hand has only one card, we assume the player reset and has the affiliation now there.
      if debugVerbosity >= 3: notify("### Executing Second Setup Phase")
      if len(fetchAllOpponents()) == 0: # If the other player hasn't chosen their side yet, it means they haven't yet tried to setup their table, so we abort
         whisper("Please wait until all your opponents have loaded their decks before proceeding")
         return
      if len(me.hand) > 3 and not confirm("Have you moved one of your 4 objectives to the bottom of your objectives deck?"): return
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
      if not Affiliation:
         information("::: ERROR::: No Affiliation card found! Please load a deck which contains an Affiliation card.")
         return
      else:
         if Affiliation.group == table and not confirm("Are you sure you want to setup for a new game? (This action should only be done after a table reset)"): return
      if debugVerbosity >= 3: notify("### Setting SetupPhase Variable")
      SetupPhase = True
      if len(deck) == 0:
         whisper ("Please load a deck first!")
         return
      if setupMultiPlayer() == 'ABORT': return
      if debugVerbosity >= 3: notify("### Placing Affiliation")
      Affiliation.moveToTable(MPxOffset + (playerside * -380) - 25, MPyOffset + (playerside * 20) + yaxisMove(Affiliation))
      if getSetting('Buttons', True):
         if len(myAllies) == 1:
            table.create("eeb4f11c-3bb0-4e84-bc4e-97f51bf2dbdc", (playerside * 340) - 25, (playerside * 20) + yaxisMove(Affiliation), 1, True) # The OK Button
            table.create("92df7072-0613-4e76-9fb0-e1b2b6d46473", (playerside * 340) - 25, (playerside * 60) + yaxisMove(Affiliation), 1, True) # The Wait! Button
            table.create("ef1f6e91-4d7f-4a10-963c-832953f985b8", (playerside * 340) - 25, (playerside * 100) + yaxisMove(Affiliation), 1, True) # The Actions? Button
         else: # With multiplayer we place the buttons below each affiliation to save space
            table.create("eeb4f11c-3bb0-4e84-bc4e-97f51bf2dbdc", MPxOffset + (playerside * -340) - 25, MPyOffset + (playerside * 180) + yaxisMove(Affiliation), 1, True) # The OK Button
            table.create("92df7072-0613-4e76-9fb0-e1b2b6d46473", MPxOffset + (playerside * -390) - 25, MPyOffset + (playerside * 180) + yaxisMove(Affiliation), 1, True) # The Wait! Button
            table.create("ef1f6e91-4d7f-4a10-963c-832953f985b8", MPxOffset + (playerside * -440) - 25, MPyOffset + (playerside * 180) + yaxisMove(Affiliation), 1, True) # The Actions? Button         
      if Side == 'Light' or len(players) == 1: #We create the balance of the force card during the dark side's setup, to avoid duplicates. 
                                               # We also create it if there's only one player for debug purposes
         if me.getGlobalVariable('PLnumber') == '#1' or len(myAllies) == 1:
            BotD = table.create("e31c2ba8-3ffc-4029-94fd-5f98ee0d78cc", 0, 0, 1, True)
            BotD.moveToTable( MPxOffset + (playerside * -380) - 25, MPyOffset + (playerside * 95) + yaxisMove(Affiliation)) # move it next to the affiliation card for now.
            if debugVerbosity >= 2: notify("### BOTD alternate is : {}".format(BotD.alternate))
            setGlobalVariable('Balance of the Force', str(BotD._id))
      #else: setGlobalVariable('Active Player', me.name) # If we're DS, set ourselves as the current player, since the Dark Side goes first.
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
      initGame()
      debugNotify(str(Automations),4)

def defaultAction(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> defaultAction(){}".format(extraASDebug())) #Debug
   mute()
   selectedAbility = eval(getGlobalVariable('Stored Effects'))
   if card.Type == 'Button': # The Special button cards.
      if card.name == 'Wait!': BUTTON_Wait()
      elif card.name == 'Actions?': BUTTON_Actions()
      else: BUTTON_OK()
      return
   elif card.highlight == FateColor: 
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
      if rnd(1,10) == 10 or me.name == 'db0': # Finally, we do some randomness :) 
         Affiliation.switchTo('FullBleed')
         if Affiliation.name == 'Sith': notify("{} has embraced their rage!".format(me))
         if Affiliation.name == 'Imperial Navy': notify("{}'s weapons are at full power!".format(me))
         if Affiliation.name == 'Scum and Villainy': notify("There's a price on your head and {} aims to collect.".format(me))
         if Affiliation.name == 'Jedi': notify("{} has become one with the force...".format(me))
         if Affiliation.name == 'Rebel Alliance': notify("{} is accelerating to attack speed".format(me))
         if Affiliation.name == 'Smugglers and Spies': notify("{} is going in against all odds.".format(me))
      if Side == 'Dark': 
         me.setGlobalVariable('Phase','0') # We now allow the dark side to start
         notify("--> {} of the Dark Side has the initiative".format(me))
         me.setActivePlayer() # If we're DS, set ourselves as the current player, since the Dark Side goes first.
   elif card.highlight == EdgeColor: revealEdge()
   elif selectedAbility.has_key(card._id): # we check via the dictionary, as this can be then used without a highlight via the "Hardcore mode"
      if card.highlight != ReadyEffectColor: # If the card has a selectedAbility entry but no highlight, it means the player is in hardcore mode, so we need to light up the card to allow their opponent to react.
         readyEffect(card,True)
         return
      debugNotify("selectedAbility Tuple = {}".format(selectedAbility[card._id]),4)
      if selectedAbility[card._id][4]: preTargets = [Card(selectedAbility[card._id][4])] # The 5th value of the tuple is special target card's we'll be using for this run.
      else: preTargets = None
      debugNotify("preTargets = {}".format(preTargets),3)
      if findMarker(card, "Effects Cancelled"): 
         notify("{}'s effects have been cancelled".format(card))
      else: 
         splitTargets = selectedAbility[card._id][0].split('$$')
         for targetSeek in splitTargets:
            if re.search(r'(?<!Auto)Targeted', targetSeek) and re.search(r'onPlay', targetSeek) and findTarget(targetSeek,card = card) == []: 
               if card.Type == 'Event': bracketInfo = "(Cancelling will abort the effect and return this card back to your hand. Saying NO will allow you to target and double click this card to try again.)"
               else: bracketInfo = "(Cancelling will dismiss this react trigger. Saying NO will allow you to target and double click this card to try again.)"
               if confirm(":::ERROR::: Required Targets for this effect not found! You need to target with shift-click accordingly\
                       \n\nWould you like to completely cancel this effect?\
                         \n{}".format(bracketInfo)):
                  clearStoredEffects(card,True,False) # Now that we won't cancel anymore, we clear the card's resident effect now, whatever happens, so that it can remove itself from play.
                  if card.Type == 'Event': card.moveTo(card.owner.hand)
                  notify("{} has aborted using {}".format(me,card))
                  return
               else: return # If the script needs a target but we don't have any, abort.
         notify("{} resolves the effects of {}".format(me,card)) 
         clearStoredEffects(card,True,False) # Now that we won't cancel anymore, we clear the card's resident effect now, whatever happens, so that it can remove itself from play.
                                             # We don't remove it from play yet though, we do it after we've executed all its scripts
         if re.search(r'LEAVING',selectedAbility[card._id][3]): 
            cardsLeaving(card,'append')
         if executeAutoscripts(card,selectedAbility[card._id][0],count = selectedAbility[card._id][5], action = selectedAbility[card._id][3],targetCards = preTargets) == 'ABORT': 
            # If we have an abort, we need to restore the card to its triggered mode so that the player may change targets and try again. 
            # Since we've already cleared the card to avoid it's "in-a-trigger" state from affecting effects which remove it from play, we need to re-store it now.
            # Since we already have its tuple stored locally, we just use storeCardEffects to save it back again.
            storeCardEffects(card,selectedAbility[card._id][0],selectedAbility[card._id][1],selectedAbility[card._id][2],selectedAbility[card._id][3],selectedAbility[card._id][4],selectedAbility[card._id][5])
            readyEffect(card,True)
            return
      debugNotify("selectedAbility action = {}".format(selectedAbility[card._id][3]),2)
      continueOriginalEvent(card,selectedAbility)
      if card.Type == 'Event': 
         autoscriptOtherPlayers('CardPlayed',card)
         if findMarker(card, "Destination:Command Deck"):
            notify(" -- {} is moved to the top of {}'s command deck".format(card,card.owner))
            rnd(1,100) # To allow any notifications to announce the card correctly first.
            card.moveTo(card.owner.piles['Command Deck'])
         else: card.moveTo(card.owner.piles['Discard Pile']) # We discard events as soon as their effects are resolved.      
   elif card.highlight == UnpaidColor: purchaseCard(card) # If the player is double clicking on an unpaid card, we assume they just want to bypass complete payment.
   elif num(card.Resources) > 0 and findUnpaidCard(): 
      if debugVerbosity >= 2: notify("Card has resources") # Debug
      generate(card)
   elif card.Type == 'Unit' and getGlobalVariable('Engaged Objective') != 'None' and not findMarker(card, "isEnhancement"): 
      if debugVerbosity >= 2: notify("Card is Unit and it's engagement time") # Debug
      if card.orientation == Rot0: participate(card)
      else: strike(card)
   elif card.model == 'e31c2ba8-3ffc-4029-94fd-5f98ee0d78cc': # If the players double click on the Balance of the Force, we assume they want to flip it.
      if debugVerbosity >= 2: 
         notify("### Flipping : {}".format(card))
         rnd(1,100)
      if card.alternate == 'DarkSide': card.switchTo() 
      else: card.switchTo('DarkSide')
      if debugVerbosity >= 2: notify("### BOTD alternate is now : {}".format(card.alternate))
      notify(":::ATTENTION::: {} flipped the balance of the force manually".format(me))
   elif CardsAA.get(card.model,'') != '': useAbility(card)
   else: whisper(":::ERROR::: There is nothing to do with this card at this moment!")
   if debugVerbosity >= 3: notify("<<< defaultAction()") #Debug
     
def strike(card, x = 0, y = 0, Continuing = False):
   if debugVerbosity >= 1: notify(">>> strike(){}".format(extraASDebug())) #Debug
   mute()
   if not Continuing: # this variable is set when we pause a strike to allow a unit to trigger a react. If it is not set, it means it's a fresh react.
      if card.Type != 'Unit': 
         whisper(":::ERROR::: Only units may perform strikes")
         return
      if (card.markers[mdict['Focus']]
            and card.markers[mdict['Focus']] >= 1
            and not confirm("Unit is already exhausted. Bypass?")):
         return 
      #notify("{} strikes with {}.".format(me, card))
      if num(getGlobalVariable('Engagement Phase')) < 4:
         if confirm("Have you resolved the edge battle already?\n\n(If you press Yes, Edge will be resolved and you'll proceed to strike with this unit)"): nextPhase(setTo = 4)
         else: return
      #card.markers[mdict['Focus']] += 1
      addMarker(card, 'Focus',1, True)
      #if card.highlight == LightForceColor or card.highlight == DarkForceColor: card.markers[mdict['Focus']] += 1
      if card.highlight == LightForceColor or card.highlight == DarkForceColor: addMarker(card, 'Focus',1, True)
      if debugVerbosity >= 2: notify("Focus Added") #Debug
      playStrikeSound(card)
      debugNotify("Executing Strike Scripts",2)      
      if executePlayScripts(card, 'STRIKE') == 'POSTPONED': 
         return # Strike effects almost universally happen after focus.
   autoscriptOtherPlayers('UnitStrike',card)
   if debugVerbosity >= 2: notify("PlayScripts done. Calculating Icons") #Debug
   Unit_DamageTXT = ''
   TacticsTXT = ''
   Unit_Damage, Blast_Damage, Tactics = calculateCombatIcons(card)
   AnnounceText = "{} strikes with {} for ".format(me,card)
   if Unit_Damage and not Tactics: 
      targetsUD = resolveUD(card,Unit_Damage) # if our strike only does unit damage then just go ahead and resolve it
      if len(targetsUD): AnnounceText += "{} Unit Damage on {}".format(Unit_Damage,targetsUD)
      else: AnnounceText += "{} Unit Damage".format(Unit_Damage)
   elif Tactics and not Unit_Damage: 
      targetsT = resolveTactics(card,Tactics) # If our strike does only 1 focus and nothing else, then we can auto-assign it to the targeted unit.
      if len(targetsT): AnnounceText += "{} Tactics on {}".format(Tactics,targetsT)
      else: AnnounceText += "{} Tactics".format(Tactics)
   elif Unit_Damage and Tactics:
      if confirm("Resolve Unit Damage first?"):
         targetsUD = resolveUD(card,Unit_Damage)
         targetsT = resolveTactics(card,Tactics)
         if len(targetsT) and len(targetsUD): AnnounceText += "{} Unit Damage on {}, then {} Tactics on {}".format(Unit_Damage,targetsUD,Tactics,targetsT)      
         elif len(targetsT) and not len(targetsUD): AnnounceText += "{} Unit Damage, then {} Tactics on {}".format(Unit_Damage,Tactics,targetsT)      
         elif not len(targetsT) and len(targetsUD): AnnounceText += "{} Unit Damage on {}, then {} Tactics".format(Unit_Damage,targetsUD,Tactics)      
         else: AnnounceText += "{} Unit Damage, then {} Tactics".format(Unit_Damage,Tactics)      
      else: 
         targetsT = resolveTactics(card,Tactics)
         targetsUD = resolveUD(card,Unit_Damage)
         if len(targetsT) and len(targetsUD): AnnounceText += "{} Tactics on {}, then {} Unit Damage on {}".format(Tactics,targetsT,Unit_Damage,targetsUD)      
         elif len(targetsT) and not len(targetsUD): AnnounceText += "{} Tactics on {}, then {} Unit Damage".format(Tactics,targetsT,Unit_Damage)      
         elif not len(targetsT) and len(targetsUD): AnnounceText += "{} Tactics, then {} Unit Damage on {}".format(Tactics,Unit_Damage,targetsUD)      
         else: AnnounceText += "{} Tactics, then {} Unit Damage".format(Tactics,Unit_Damage)      
   currentTarget = Card(num(getGlobalVariable('Engaged Objective'))) # We find the current objective target to see who's the owner, because only the attacker does blast damage
   if currentTarget.controller in fetchAllOpponents() and not hasDamageProtection(currentTarget,card): 
      addMarker(currentTarget, 'Damage',Blast_Damage, True) # We assign the blast damage automatically, since there's only ever one target for it.
      if Blast_Damage: 
         if Unit_Damage or Tactics: AnnounceText += " and {} Blast Damage on {}".format(Blast_Damage,currentTarget)
         else: AnnounceText += "{} Blast Damage on {}".format(Blast_Damage,currentTarget)
   if not Blast_Damage and not Unit_Damage and not Tactics: AnnounceText += "no effect"
   AnnounceText += '.'
   notify(AnnounceText)
   markerEffects('afterStrike')
   if debugVerbosity >= 3: notify("<<< strike()") #Debug    
      
def participate(card, x = 0, y = 0, silent = False):
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
   if currentTarget.controller in fetchAllOpponents():
      if num(getGlobalVariable('Engagement Phase')) < 1: nextPhase(setTo = 1)
      if not silent: notify("{} selects {} as an attacker.".format(me, card))
      executePlayScripts(card, 'ATTACK')   
   else:
      if num(getGlobalVariable('Engagement Phase')) < 2: nextPhase(setTo = 2)
      if not silent: notify("{} selects {} as a defender.".format(me, card))
      executePlayScripts(card, 'DEFEND')   
   card.orientation = Rot90
   playParticipateSound(card)
   executePlayScripts(card, 'PARTICIPATION')
   autoscriptOtherPlayers('UnitParticipates',card)
   clearTargets() # We clear the targets to make sure there's no random markers being put by mistake.
   if debugVerbosity >= 3: notify("<<< participate()") #Debug

def clearParticipation(card,x=0,y=0,silent = False): # Clears a unit from participating in a battle, to undo mistakes
   mute()
   if card.orientation == Rot90: 
      card.orientation = Rot0
      if not silent: notify("{} takes {} out of the engagement.".format(me, card))
   else: whisper(":::ERROR::: Unit is not currently participating in battle")

def cancelPaidAbility(card,x=0,y=0):
# This function clears a card's paid ability in case the player tried to use it but realized they couldn't.
   mute()
   clearStoredEffects(card, True, ignoredEffect = True)
   clrResourceMarkers(card)
   notify("{} has canceled {}'s ability".format(me,card))

def ignoreTrigger(card,x=0,y=0):
   mute()
   clearStoredEffects(card,silent = True,ignoredEffect = True)
   notify("{} chose not to activate {}'s ability".format(me,card))

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
   cardResources = calcResources(card)
   if cardResources == 0: 
      whisper("Resources, this card produces not!")
      return
   elif cardResources > 1: 
      count = askInteger("Card can generate up to {} resources. How many do you want to produce?".format(cardResources), 1)
      if not count: return # If the player closed the window or put 0, do nothing.
      while count > cardResources:
         count = askInteger(":::ERROR::: This card cannot generate so many resources.\
                         \n\nPlease input again how many resources to produce (Max {})".format(cardResources), 1)
         if not count: return # If the player closed the window or put 0, do nothing.      
   else: count = 1
   try: unpaidC.markers[resdict['Resource:{}'.format(card.Affiliation)]] += count
   except: unpaidC.markers[resdict['Resource:Neutral']] += count
   addMarker(card, 'Focus',count, True)
   notify("{} exhausts {} to produce {} {} Resources.".format(me, card, count,card.Affiliation))
   executePlayScripts(card, 'GENERATE')
   autoscriptOtherPlayers('ResourceGenerated',card)
   resResult = checkPaidResources(unpaidC)
   if resResult == 'OK': purchaseCard(unpaidC, manual = False)
   elif resResult == 'USEOK': readyEffect(unpaidC)
   incrStat('resources',me.name) # We store that the player has played a unit
   if debugVerbosity >= 3: notify("<<< generate()") #Debug

def calcResources(card):
   debugNotify(">>> calcResources()") #Debug
   extraResources = 0
   if card.name == 'Hunt Them Down': # This objective has +1 resource for each captured card
      capturedCards = eval(getGlobalVariable('Captured Cards'))
      for capturedC in capturedCards: # We check each entry in the dictionary. Each entry is a card's unique ID
         if capturedCards[capturedC] == card._id: # If the value we have for that card's ID is the unique ID of the current dictionary, it means that card is currently being captured at our objective.
            extraResources += 1 # Thus we increase the provided resources by one.
   debugNotify("<<< calcResources() with return {}".format(num(card.Resources) + extraResources)) #Debug
   return num(card.Resources) + extraResources
   
def findUnpaidCard():
   debugNotify(">>> findUnpaidCard()") #Debug
   if unpaidCard: return unpaidCard
   else:
      for card in table:
         if (card.highlight == UnpaidColor or card.highlight == UnpaidAbilityColor) and card.controller == me: return card
   if debugVerbosity >= 3: notify("<<< findUnpaidCard()") #Debug
   return None # If not unpaid card is found, return None

def checkPaidResources(card):
   if debugVerbosity >= 1: notify(">>> checkPaidResources()") #Debug
   count = 0
   affiliationMatch = False
   for cMarkerKey in card.markers: #We check the key of each marker on the card
      for resdictKey in resdict:  #against each resource type available
         if debugVerbosity >= 2: notify("About to compare marker keys: {} and {}".format(resdict[resdictKey],cMarkerKey)) #Debug
         if resdict[resdictKey] == cMarkerKey: # If the marker is a resource
            count += card.markers[cMarkerKey]  # We increase the count of how many resources have been paid for this card
            if debugVerbosity >= 2: notify("About to check found resource affiliaton") #Debug
            if 'Resource:{}'.format(card.Affiliation) == resdictKey: # if the card's affiliation also matches the currently checked resource
               if debugVerbosity >= 3: notify("### Affiliation match. Affiliation = {}. Marker = {}.".format(card.Affiliation,resdictKey))
               affiliationMatch = True # We set that we've also got a matching resource affiliation
      if cMarkerKey[0] == "Ignores Affiliation Match": 
         if debugVerbosity >= 3: notify("### Ignoring affiliation match due to marker on card. Marker = {}".format(cMarkerKey))
         affiliationMatch = True # If we have a marker that ignores affiliations, we can start ignoring this card's as well
   for c in table:
      if c.controller == me and re.search("IgnoreAffiliationMatch",CardsAS.get(c.model,'')) and chkDummy(CardsAS.get(c.model,''), c): 
         notify(":> Affiliation match ignored due to {}.".format(c))
         affiliationMatch = True
   if debugVerbosity >= 2: notify("About to check successful cost. Count: {}, Affiliation: {}".format(count,card.Affiliation)) #Debug
   if card.highlight == UnpaidAbilityColor:
      selectedAbility = eval(getGlobalVariable('Stored Effects'))
      reduction = reduceCost(card, 'USE', selectedAbility[card._id][1] - count, dryRun = True) # We do a dry run first. We do not want to trigger once-per turn abilities until the point where we've actually paid the cost.
      if count >= selectedAbility[card._id][1] - reduction:
         if debugVerbosity >= 3: notify("<<< checkPaidResources(). Return USEOK") #Debug
         reduceCost(card, 'USE', selectedAbility[card._id][1] - count) # Now that we've actually made sure we've paid the cost, we use any ability that reduces costs.
         return 'USEOK'
      else:
         if count >= selectedAbility[card._id][1] - reduction and not affiliationMatch:
            notify(":::WARNING::: Ability cost reached but there is no affiliation match!")
         if debugVerbosity >= 3: notify("<<< checkPaidResources(). Return NOK") #Debug
         return 'NOK'      
   else:
      reduction = reduceCost(card, 'PLAY', num(card.Cost) - count, dryRun = True) # We do a dry run first. We do not want to trigger once-per turn abilities until the point where we've actually paid the cost.
      if count >= num(card.Cost) - reduction and (card.Affiliation == 'Neutral' or affiliationMatch or (not affiliationMatch and (num(card.Cost) - reduction) == 0)):
         if debugVerbosity >= 3: notify("<<< checkPaidResources(). Return OK") #Debug
         reduceCost(card, 'PLAY', num(card.Cost) - count) # Now that we've actually made sure we've paid the cost, we use any ability that reduces costs.
         return 'OK'
      else:
         if count >= num(card.Cost) - reduction and not affiliationMatch:
            notify(":::WARNING::: Card cost reached but there is no affiliation match!")
         if debugVerbosity >= 3: notify("<<< checkPaidResources(). Return NOK") #Debug
         return 'NOK'

def purchaseCard(card, x=0, y=0, manual = True):
   if debugVerbosity >= 1: notify(">>> purchaseCard(){}".format(extraASDebug())) #Debug
   global unpaidCard
   if manual and card.highlight != ReadyEffectColor: checkPaid = checkPaidResources(card)
   # If this is an attempt to manually pay for the card, we check that the player can afford it (e.g. it's zero cost or has cost reduction effects)
   # Events marked as 'ReadyEffectColor' have already been paid, so we do not need to check them again.
   else: checkPaid = 'OK' #If it's not manual, then it means the checkPaidResources() has been run successfully, so we proceed.
   if checkPaid == 'OK' or confirm(":::ERROR::: You do have not yet paid the cost of this card. Bypass?"):
      # if the card has been fully paid, we remove the resource markers and move it at its final position.
      card.highlight = None
      placeCard(card)
      clrResourceMarkers(card)
      unpaidCard = None
      if checkPaid == 'OK': notify("{} has paid for {}".format(me,card)) 
      else: notify(":::ATTENTION::: {} has played {} by skipping its full cost".format(me,card))
      playEventSound(card)
      executePlayScripts(card, 'PLAY') 
      if card.Type != 'Event': autoscriptOtherPlayers('CardPlayed',card) # We script for playing events only after their events have finished resolving in the default action.
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
   debugNotify(">>> handDiscard()") #Debug
   mute()
   if card.Type == "Objective": 
      card.moveToBottom(me.piles['Objective Deck']) # This should only happen during the game setup
      notify("{} chose their 3 starting objectives.".format(me))
   else:
      card.moveTo(me.piles['Discard Pile'])
      notify("{} discards {}".format(me,card))
   debugNotify("<<< handDiscard()") #Debug

def discardTarget(group, x = 0, y = 0): # Discards target card
   mute()
   for c in table:
      if c.targetedBy and c.targetedBy == me:
         remoteCall(c.owner, 'discard', [c,0,0,False,False,me])
   
def discard(card, x = 0, y = 0, silent = False, Continuing = False, initPlayer = me):
   debugNotify(">>> discard() card = {}".format(card)) #Debug
   mute()
   previousHighlight = card.highlight # We store the highlight before we move the card to the discard pile, to be able to check if it's an edge card to avoid triggering its autoscripts
   debugNotify("previous Highlight = {}".format(previousHighlight),2)   
   if card.highlight == DummyColor: 
      card.moveTo(card.owner.piles['Discard Pile'])
      if not silent: notify("{}'s resident effect ends".format(card))
   elif card.Type == "Objective":
      if initPlayer == me: 
         confirmTXT = 'your opponent'
         opponentList = fetchAllOpponents()
         choice = SingleChoice("Choose which opponent thwarted this objective.", [pl.name for pl in opponentList])
         if choice == None: return
         opponentPL = opponentList[choice]
         silent = True # We silence so that the game doesn't put out a second dialogue
      else: 
         confirmTXT = initPlayer.name
         opponentPL = initPlayer         
      if not Continuing and not silent and not confirm("Did {} thwart {}?".format(confirmTXT,card.name)): return 'ABORT'
      if not Continuing and not cardsLeaving(card):
         execution = executePlayScripts(card, 'THWART')
         if execution == 'POSTPONED': 
            return # If the unit has a Ready Effect it means we're pausing our discard to allow the player to decide to use the react or not. 
      debugNotify(" About to score objective")
      currentObjectives = eval(me.getGlobalVariable('currentObjectives'))
      currentObjectives.remove(card._id)
      rescuedCount = rescueFromObjective(card)
      if rescuedCount >= 1: extraTXT = ", rescuing {} of their captured cards".format(rescuedCount)
      else: extraTXT = ''
      me.setGlobalVariable('currentObjectives', str(currentObjectives))      
      if Side == 'Light': 
         opponentPL.counters['Objectives Destroyed'].value += 1         
         modifyDial(opponentPL.counters['Objectives Destroyed'].value)
         notify("{} thwarts {}. The Death Star Dial advances by {}".format(opponentPL,card,opponentPL.counters['Objectives Destroyed'].value))
      else: 
         for player in fetchAllOpponents(): # Light side players share destroyed objectives number
            player.counters['Objectives Destroyed'].value += 1         
         notify("{} thwarts {}{}.".format(opponentPL,card,extraTXT))
         if len(myAllies) == 2: objRequired = 5
         else: objRequired = 3
         if opponentPL.counters['Objectives Destroyed'].value >= objRequired: 
            notify("===::: The Light Side wins the Game! :::====")
            reportGame('ObjectiveDefeat')
      autoscriptOtherPlayers('ObjectiveThwarted',card, origin_player = opponentPL)
      playThwartSound()
      card.moveTo(opponentPL.piles['Victory Pile']) # Objectives are won by the opponent
      cardsLeaving(card,'remove')
   elif card.Type == "Affiliation" or card.Type == "BotD": 
      whisper("This isn't the card you're looking for...")
      return 'ABORT'
   elif card.highlight == EdgeColor:
      card.moveTo(card.owner.piles['Discard Pile'])
   elif card.highlight == CapturedColor and not Continuing: # If we're continuing a script and the card is now captured, it means its own effect made it so, so we leave it where it is (e.g. Leia Organa)
      removeCapturedCard(card)
      card.moveTo(card.owner.piles['Discard Pile'])   
   else:
      if previousHighlight != FateColor and previousHighlight != EdgeColor and previousHighlight != UnpaidColor and previousHighlight != CapturedColor:
         if not Continuing and not cardsLeaving(card):
            debugNotify("Executing Discard leaving play scripts. Highlight was {}".format(previousHighlight),2)
            execution = executePlayScripts(card, 'LEAVING-DISCARD') # Objective discard scripts are dealt with onThwart.
            autoscriptOtherPlayers('CardLeavingPlay',card)
            if execution == 'POSTPONED': 
               return # If the unit has a Ready Effect it means we're pausing our discard to allow the player to decide to use the react or not. 
         rescuedCount = rescueFromObjective(card) # Since Escape from Hoth, Units can capture cards as well.
         if rescuedCount >= 1: extraTXT = ", rescuing {} captured cards".format(rescuedCount)
         else: extraTXT = ''
         freeUnitPlacement(card)
         debugNotify("About to discard card. Highlight is {}. Group is {}".format(card.highlight,card.group.name),2)
         if card.group == table and card.highlight != CapturedColor:
            if not Continuing: clearStoredEffects(card,True) # Making sure that the player didn't discard a card waiting for an effect. We only do it if we're not continuing an existing script, as then its's done there and it will cause an infinite loop in here.
            card.moveTo(card.owner.piles['Discard Pile']) # If the card was not moved around via another effect, then discard it now.
            cardsLeaving(card,'remove')
            playDestroySound(card)
         if not silent: notify("{} discards {}{}".format(me,card,extraTXT))
   if previousHighlight != DummyColor:
      debugNotify("Checking if the card has attachments to discard as well.")      
      if card.group != table: clearAttachLinks(card) # If a card effect did not prevent the card from leaving the table, then we clear all attachments
   debugNotify("<<< discard()") #Debug
   return 'OK'

def capture(group = table,x = 0,y = 0, chosenObj = None, targetC = None, silent = False, Continuing = False): # Tries to find a targeted card in the table or the oppomnent's hand to capture
   global capturingObjective
   if Continuing: chosenObj = capturingObjective
   debugNotify(">>> capture(){}".format(extraASDebug())) #Debug
   if debugVerbosity >= 2 and chosenObj: notify("### chosenObj = {}".format(chosenObj)) #Debug
   if debugVerbosity >= 2 and targetC: notify("### targetC = {}".format(targetC)) #Debug
   mute()
   if not targetC:
      debugNotify("Don't have preset target. Seeking...")
      for card in table:
         debugNotify("### Searching table") #Debug
         if card.targetedBy and card.targetedBy == me and card.Type != "Objective": 
            if card.highlight == CapturedColor and not confirm("Are you sure you want to move this captured card to a different objective?"): continue
            targetC = card
      if targetC: captureTXT = "{} has captured {}'s {}".format(me,targetC.owner,targetC)
      else:
         debugNotify("### Searching opponents' hand") #Debug
         for opponentPL in fetchAllOpponents():
            for card in opponentPL.hand:
               if card.targetedBy and card.targetedBy == me: targetC = card
            if targetC: captureTXT = "{} has captured one card from {}'s hand".format(me,targetC.owner)
            else:
               debugNotify("### Searching command deck") #Debug
               for card in opponentPL.piles['Command Deck'].top(3):
                  debugNotify("### Checking {}".format(card), 3) #Debug
                  if card.targetedBy and card.targetedBy == me: targetC = card
               if targetC: captureTXT = "{} has captured one card from {}'s Command Deck".format(me,targetC.owner)
   else: captureTXT = ":> {} has captured one card from {}'s {}".format(me,targetC.owner,targetC.group.name)
   if not targetC: whisper(":::ERROR::: You need to target a command card in the table or your opponent's hand or deck before taking this action")
   else: 
      captureGroup = targetC.group.name
      if Side == 'Light': 
         opponentList = fetchAllOpponents()
         choice = SingleChoice("Choose which opponent captured this card.", [pl.name for pl in opponentList])
         if choice == None: return
         captor = opponentList[choice]
      else: captor = me 
      if not chosenObj or chosenObj.owner != captor:
         debugNotify("Don't have preset objective. Seeking...")
         myObjectives = eval(captor.getGlobalVariable('currentObjectives'))
         objectiveList = [Card(objective_ID) for objective_ID in myObjectives]
         otherHosts = [] #There are some non-objective cards, like Dengar, which are also allowed to capture cards. In the below loop we try to discover if any of them are possible to be used.
         debugNotify("About to discover otherHosts")
         for c in table:
            Autoscripts = CardsAS.get(c.model,'').split('||')
            for autoS in Autoscripts:
               if re.search(r'CanCapture',autoS):
                  if re.search(r'ifInPlay',autoS) and targetC.group != table: continue
                  if not checkCardRestrictions(gatherCardProperties(targetC), prepareRestrictions(autoS,'type')): continue
                  debugNotify("Appending {} to otherHosts".format(c),4)
                  otherHosts.append(c)
         objectiveList.extend(otherHosts)
         choice = SingleChoice("Choose in to which objective to capture the card.", makeChoiceListfromCardList(objectiveList), default = 0)
         if choice == None: return
         if choice + 1 > len(myObjectives): chosenObj = otherHosts[choice - len(myObjectives)]
         else: chosenObj = Card(myObjectives[choice])
      debugNotify("About to Announce")
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
      if targetC.controller in fetchAllOpponents(): xAxis = 1
      else: xAxis = -1
      if captureGroup == 'Table' and targetC.highlight != EdgeColor and targetC.highlight != FateColor and targetC.highlight != RevealedColor: # If the card was on the table, we also trigger "removed from play" effects
         if not Continuing and not cardsLeaving(targetC):
            debugNotify("Executing Capture Leaving Play Scripts. Highlight was {}".format(targetC.highlight),2)
            execution = executePlayScripts(targetC, 'LEAVING-CAPTURED')
            autoscriptOtherPlayers('CardLeavingPlay',targetC)
            if execution == 'POSTPONED': 
               capturingObjective = chosenObj
               return
            selectedAbility = eval(getGlobalVariable('Stored Effects'))
      if not Continuing: clearStoredEffects(targetC,True)            
      freeUnitPlacement(targetC)
      targetC.moveToTable(xPos - (cwidth(targetC) * playerside * xAxis / 2 * countCaptures), yPos, True)
      targetC.sendToBack()
      targetC.isFaceUp = False
      if chosenObj.owner == me: targetC.peek()
      targetC.orientation = Rot0
      targetC.highlight = CapturedColor
      targetC.target(False)
      targetC.markers[mdict['Shield']] = 0
      targetC.markers[mdict['Damage']] = 0
      targetC.markers[mdict['Focus']] = 0
      targetC.setController(chosenObj.owner)
      debugNotify("Finished Capturing. Removing from cardsLeavingPlay var",2)
      cardsLeaving(targetC,'remove')
      debugNotify("About to reset shared variable",2)
      setGlobalVariable('Captured Cards',str(capturedCards))
      debugNotify("About to initiate autoscripts",2)
      capturingObjective = chosenObj # We use a global variable in order for scripts which require it, to find out which objective got the captured card.
      autoscriptOtherPlayers('{}CardCapturedFrom{}'.format(targetCType,captureGroup),targetC) # We send also the card type. Some capture hooks only trigger of a specific kind of captured card (e.g. bespin exchange)
      capturingObjective = None # We clear it at the end.
   debugNotify("<<< capture()") #Debug

def clearCaptures(card, x=0, y=0): # Simply clears all the cards that the game thinks the objective has captured
   debugNotify(">>> clearCaptures()")
   capturedCards = eval(getGlobalVariable('Captured Cards')) # This is a dictionary holding how many and which cards are captured at each objective.
   for capturedC in capturedCards: # We check each entry in the dictionary. Each entry is a card's unique ID
      if capturedCards[capturedC] == card._id: # If the value we have for that card's ID is the unique ID of the current dictionary, it means that card is currently being captured at our objective.
         removeCapturedCard(Card(capturedC)) # We remove the card from the dictionary
   whisper("All associated captured cards for this objective have been cleared")
   debugNotify("<<< clearCaptures()")
   
def rescue(card,x = 0, y = 0,silent = False):
   debugNotify(">>> rescue()")
   if card.isFaceUp: 
      notify(":::ERROR::: Target Card was not captured!")
      return 'ABORT'
   global capturingObjective
   capturingObjective = removeCapturedCard(card) # We use a global variable in order for scripts which require it, to find out from which objective we rescued the card from.
   card.moveTo(card.owner.hand)
   autoscriptOtherPlayers('CardRescued',card) 
   if not silent: notify("{} rescued a card from {}".format(me,capturingObjective))
   capturingObjective = None # We clear it at the end.
   debugNotify("<<< rescue()")
   

def rescueTargets(group,x = 0, y = 0):
   debugNotify(">>> rescueTargets()")
   for card in table:
      if card.highlight == CapturedColor and card.targetedBy and card.targetedBy == me: rescue(card)
   debugNotify("<<< rescueTargets()")

def exileCard(card, silent = False,Continuing = False):
   debugNotify(">>> exileCard(){}".format(extraASDebug())) #Debug
   # Puts the removed card in the player's removed form game pile.
   mute()
   if card.Type == "Affiliation" or card.Type == "BotD": 
      whisper("This isn't the card you're looking for...")
      return 'ABORT'
   else:
      if targetCard.group == table and targetCard.highlight != EdgeColor and targetCard.highlight != FateColor and card.highlight != CapturedColor:
         if not Continuing and not cardsLeaving(card):
            debugNotify("Executing Exile Leaving Play Scripts",2)
            execution = executePlayScripts(targetCard, 'LEAVING-EXILE')
            autoscriptOtherPlayers('CardLeavingPlay',targetCard)
            if execution == 'POSTPONED': 
               return
      if card.highlight != CapturedColor or (card.highlight == CapturedColor and not Continuing):
         if card.group == table: clearAttachLinks(card)
         freeUnitPlacement(card)
         card.moveTo(me.piles['Removed from Game'])
         cardsLeaving(card,'remove')
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
   reportGame('Conceded')
   notify("=== {} Concedes the Game ===".format(me))
      
def rulings(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> rulings(){}".format(extraASDebug())) #Debug
   mute()
   #if not card.isFaceUp: return
   #openUrl('http://www.netrunneronline.com/cards/{}/'.format(card.Errata))
   openUrl('http://www.cardgamedb.com/index.php/netrunner/star-wars-card-search?text={}&fTS=0'.format(card.name)) # Errata is not filled in most card so this works better until then

def play(card):
   if debugVerbosity >= 1: notify(">>> play(){}".format(extraASDebug())) #Debug
   global unpaidCard, limitedPlayed
   mute()
   extraTXT = ''
   if card.Type == 'Fate': 
      playEdge(card)
      return # If the player double clicked on a Fate card, assume he wanted to play it as an edge card.
   elif card.Type == 'Objective': 
      handDiscard(card)
      return # If the player double clicked on an objective, we assume they were selecting one of their three objectives to to put at the bot. of their deck.
   if card.Type == 'Enhancement' or card.Type == 'Unit':
      if not re.search(r'4',getGlobalVariable('Phase')) and (re.search(r'5',getGlobalVariable('Phase')) and not re.search(r'DeployAllowance:Conflict',CardsAS.get(card.model,''))):
         if not confirm(":::WARNING:::\n\nNormally this type of card cannot be played outside the deployment phase. Are you sure you want to continue?"): 
            return # If the card is a unit or enhancement, it can only be played during the deployment phase. Here we add a check to prevent the player from playing it out-of-phase.
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
   card.moveToTable(MPxOffset, MPyOffset + yaxisMove(card))
   if checkPaidResources(card) == 'NOK':
      card.highlight = UnpaidColor 
      unpaidCard = card
      notify("{} attempts to play {}{}.".format(me, card,extraTXT))
      # if num(card.Cost) == 0 and card.Type == 'Event': readyEffect(card)
   else: 
      if card.Type == 'Event':
         playEventSound(card)
         executePlayScripts(card, 'PLAY') # We do not trigger events automatically, in order to give the opponent a chance to play counter cards
      else:
         placeCard(card)
         notify("{} plays {}{}.".format(me, card,extraTXT))
         executePlayScripts(card, 'PLAY') # We execute the play scripts here only if the card is 0 cost.
         autoscriptOtherPlayers('CardPlayed',card)
      
def playEdge(card, silent = False):
   if debugVerbosity >= 1: notify(">>> playEdge(){}".format(extraASDebug())) #Debug
   if getGlobalVariable('Engaged Objective') == 'None': 
      whisper(":::ERROR::: You have to be in an engagement to play edge cards. ABORTING!")
      return 'ABORT'
   if num(getGlobalVariable('Engagement Phase')) < 3: nextPhase(setTo = 3)
   edgeCount = len([c for c in table if (c.highlight == EdgeColor or c.highlight == FateColor) and c.controller == me])
   mute()
   card.moveToTable(MPxOffset + (playerside * 250), MPyOffset + (playerside * 30) + yaxisMove(card) + (playerside * 40 * edgeCount), True)
   attacker = Player(num(getGlobalVariable('Current Attacker')))
   currentTarget = Card(num(getGlobalVariable('Engaged Objective')))
   if attacker != me and currentTarget.controller != me: # If we play an edge card as an ally, we always place it on the main player's edge stack
      if attacker in myAllies: edgeOwner = attacker
      else: edgeOwner = currentTarget.controller
      card.setController(edgeOwner)
      if edgeCount > 0: 
         for c in table:
            if (c.highlight == EdgeColor or c.highlight == FateColor) and c.controller == edgeOwner: lastEdge = c
         x,y = c.position
         c.moveToTable(x, y + (playerside * 40)) # We try to move the allie's edge card to the edge stack
   card.highlight = EdgeColor
   card.peek()
   edgeRevealed = eval(getGlobalVariable('Revealed Edge'))
   edgeRevealed[card.owner.name] = False # Clearing some variables just in case they were left over. 
   setGlobalVariable('Revealed Edge',str(edgeRevealed))
   if not silent: notify("{} places a card in their edge stack.".format(me, card))
   
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
         if card.highlight == EdgeColor and not card.isFaceUp and card.controller in myAllies:
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
      winnerDifference = 0
      if debugVerbosity >= 2: notify("Edge cards already revealed. Gonna calculate edge") #Debug
      if forceCalc: # forceCalc is only used to make sure the edge has been assigned. If a player already has the edge, we don't change it
         for player in getPlayers(): # This is because they may have calculated the edge in the edge phase and discarded their edge cards laready.
            plAffiliation = getSpecial('Affiliation',player)
            if plAffiliation.markers[mdict['Edge']] and plAffiliation.markers[mdict['Edge']] == 1: return
      myEdgeTotal = 0
      opponentEdgeTotal = 0
      if Side == 'Light': opSide = 'Dark'
      else: opSide = 'Light'
      for card in table:
         if debugVerbosity >= 4: notify("#### Checking {}".format(card)) #Debug
         if (card.highlight == EdgeColor or card.highlight == FateColor) and card.isFaceUp:
            if card.controller in myAllies: myEdgeTotal += num(card.Force)
            else: opponentEdgeTotal += num(card.Force)
            if card.highlight == FateColor: notify(":::WARNING::: {} has not yet resolved their {}".format(card.owner,card))
         bonusEdge = calcBonusEdge(card)
         if bonusEdge: # Card with edge need to be participating.
            if debugVerbosity >= 2: notify("### Found card with Bonus edge") #Debug
            if card.controller in myAllies: myEdgeTotal += bonusEdge
            else: opponentEdgeTotal += bonusEdge
      currentTarget = Card(num(getGlobalVariable('Engaged Objective'))) # We find out what the current objective as we can use it to figure out if we're an attacker or defender.
      if myEdgeTotal > opponentEdgeTotal:
         winnerDifference = myEdgeTotal - opponentEdgeTotal
         if debugVerbosity >= 2: notify("### I've got the edge") #Debug
         if not (Affiliation.markers[mdict['Edge']] and Affiliation.markers[mdict['Edge']] == 1): 
         # We check to see if we already have the edge marker on our affiliation card (from our opponent running the same script)
            clearEdgeMarker() # We clear the edge, in case another player's affiliation card had it
            Affiliation.markers[mdict['Edge']] = 1
            notify("The {} Side has the edge in this engagement ({}: {} force VS {}: {} force)".format(Side,Side, myEdgeTotal, opSide, opponentEdgeTotal))
            if currentTarget.controller in fetchAllOpponents(): autoscriptOtherPlayers('AttackerEdgeWin',currentTarget, winnerDifference)
            else: autoscriptOtherPlayers('DefenderEdgeWin',currentTarget, winnerDifference)
            incrStat('edgev',me.name) # We store that the player has won an edge battle
         elif not forceCalc: delayed_whisper(":::NOTICE::: You already have the edge. Nothing else to do.")
      elif myEdgeTotal < opponentEdgeTotal:
         winnerDifference = opponentEdgeTotal - myEdgeTotal
         debugNotify("Opponent has the edge") #Debug
         try:
            opponentPL = Player(num(getGlobalVariable('Current Attacker')))
         except: 
            notify(":::ERROR::: Nobody is currently attacking. Aborting!")
            return
         oppAffiliation = getSpecial('Affiliation',opponentPL)
         if not (oppAffiliation.markers[mdict['Edge']] and oppAffiliation.markers[mdict['Edge']] == 1): 
         # We check to see if our opponent already have the edge marker on our affiliation card (from our opponent running the same script)
            clearEdgeMarker() # We clear the edge, in case another player's affiliation card had it
            oppAffiliation.markers[mdict['Edge']] = 1
            notify("The {} Side has the edge in this engagement ({}: {} force VS {}: {} force)".format(opSide,Side, myEdgeTotal, opSide, opponentEdgeTotal))
            if currentTarget.controller in fetchAllOpponents(): autoscriptOtherPlayers('AttackerEdgeWin',currentTarget, winnerDifference)
            else: autoscriptOtherPlayers('DefenderEdgeWin',currentTarget, winnerDifference)
            incrStat('edgev',opponentPL.name) # We store that the player has won an edge battle
         elif not forceCalc: whisper(":::NOTICE::: Your opponent already have the edge. Nothing else to do.")
      else: 
         if debugVerbosity >= 2: notify("### Edge is a Tie") #Debug
         if debugVerbosity >= 2: notify("### Finding defender's Affiliation card.") #Debug
         defenderAffiliation = getSpecial('Affiliation',currentTarget.controller)
         unopposed = True
         for card in table:
            if card.orientation == Rot90 and card.controller in fetchAllAllies(currentTarget.controller): unopposed = False
         if unopposed:
            try:
               attacker = Player(num(getGlobalVariable('Current Attacker')))
            except: 
               notify(":::ERROR::: Nobody is currently attacking. Aborting!")
               return
            if debugVerbosity >= 2: notify("### Unopposed Attacker") #Debug
            if not (Affiliation.markers[mdict['Edge']] and Affiliation.markers[mdict['Edge']] == 1): 
               clearEdgeMarker() # We clear the edge, in case another player's affiliation card had it
               Affiliation.markers[mdict['Edge']] = 1
               notify("The engagement of {} is unopposed, so {} automatically gains edge as the attacker.".format(currentTarget,attacker))
               autoscriptOtherPlayers('AttackerEdgeWin',currentTarget, 0)
               incrStat('edgev',attacker.name) # We store that the player has won an edge battle
            elif not forceCalc: whisper(":::NOTICE::: The attacker already has the edge. Nothing else to do.")
         else:
            if debugVerbosity >= 2: notify("### Defender's Advantage") #Debug
            if not (defenderAffiliation.markers[mdict['Edge']] and defenderAffiliation.markers[mdict['Edge']] == 1): 
               clearEdgeMarker() # We clear the edge, in case another player's affiliation card had it
               defenderAffiliation.markers[mdict['Edge']] = 1
               notify("Nobody managed to get the upper hand in the edge struggle ({}: {} force VS {}: {} force), so {} retains the edge as the defender.".format(Side, myEdgeTotal, opSide, opponentEdgeTotal,currentTarget.controller))
               autoscriptOtherPlayers('DefenderEdgeWin',currentTarget, 0)
               incrStat('edgev',currentTarget.controller.name) # We store that the player has won an edge battle
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

def sendToBottom(cards = None,x=0,y=0, Continuing = False,silent = False):
   debugNotify(">>> sendToBottom()") #Debug
   global randomizedArray
   scriptWaiting = False
   firstTime = False
   if Continuing: 
      cards = randomizedArray
   elif not cards:
      delayed_whisper(":::ERROR::: There's no cards selected to send to the Bottom of your deck. Aborting!")
      return
   else:
      if debugVerbosity >= 1: notify("### Card List = {}".format([c.name for c in cards])) #Debug
      mute()
      if len(cards) == 0: return
      if debugVerbosity >= 2: notify("### Original List: {}".format([card.name for card in cards])) #Debug
      for iter in range(len(cards)):
         if iter % 5 == 0: notify("---PLEASE DO NOT MOVE ANY CARDS AROUND---")
         if iter % 2 == 0: notify("Randomizing({}/{} done)...".format(iter, len(cards)))
         swap = rnd(iter,len(cards) - 1)
         cards[iter], cards[swap] = cards[swap], cards[iter]
      if debugVerbosity >= 2: notify("### Randomized List: {}".format([card.name for card in cards])) #Debug
      if cards[0].group == me.hand:
         if not silent: notify("{} sends {} cards from their hand to the bottom of their respective decks in random order.".format(me,len(cards)))
      else:
         if not silent: notify("{} sends {} to the bottom of their respective decks in random order.".format(me,[card.name for card in sorted(cards)])) # We sort the list so that the players cannot see the true random order in the announcement
   debugNotify("Executing card scripts one by one",2)
   for card in cards: 
      if not scriptWaiting and not Continuing and not cardsLeaving(card) and card.group == table and card.highlight != EdgeColor and card.highlight != FateColor and card.highlight != CapturedColor: 
         debugNotify("Executing SendToBottom Leaving Play Scripts",2)
         if executePlayScripts(card, 'LEAVING-DECKBOTTOM') == 'POSTPONED': firstTime = True
         autoscriptOtherPlayers('CardLeavingPlay',card)
   debugNotify("Checking if we've already executed the scripts",2)
   for card in cards: 
      if Continuing: silentChk = True
      else: silentChk = False
      if chkEffectTrigger(card,'send to bottom',silentChk): # We check all cards in our array to see if any still have scripts to use
         randomizedArray = cards
         scriptWaiting = True
   debugNotify("Checking if we need to abort or ask.",2)
   if scriptWaiting: 
      debugNotify("scriptWaiting = True.",3)
      if not Continuing and not firstTime: #If we're not continuing and we didn't just execute the scripts for these cards, it means the player manually run the SendToBottom() function again, so they may be trying to force it.
         if confirm("You seem to have card scripts still waiting to trigger. Are you sure you want to continue and send all cards to the bottom?"):
            for card in cards: 
               if not Continuing: clearStoredEffects(card,True)
         else: return
      else: return # If we went to this function from the Default Action and we still have cards to trigger, then we just abort and wait until the player has had a chance to trigger all effects.
   debugNotify("About to send to bottom.",2)
   for card in cards: 
      if card.highlight != CapturedColor or (card.highlight == CapturedColor and not Continuing):
         if card.group == table: clearAttachLinks(card)
         freeUnitPlacement(card)
         card.moveToBottom(card.owner.piles['Command Deck'])
         cardsLeaving(card,'remove')
         randomizedArray = None
   debugNotify("<<< sendToBottom()") #Debug

def returnToHand(card,x = 0,y = 0,silent = False,Continuing = False):
   debugNotify(">>> returnToHand()") #Debug
   if card.group == table and card.highlight != EdgeColor and card.highlight != FateColor and card.highlight != CapturedColor:
      if not Continuing and not cardsLeaving(card):
         execution = executePlayScripts(card, 'LEAVING-HAND')
         autoscriptOtherPlayers('CardLeavingPlay',card)
         if execution == 'POSTPONED': 
            return # If the unit has a Ready Effect it means we're pausing our discard to allow the player to decide to use the react or not. 
         rnd(1,10)
   if not chkEffectTrigger(card,'Card Return'):
      if card.group == table and card.highlight != CapturedColor:
         if not Continuing: clearStoredEffects(card,True)
         cardsLeaving(card,'remove')
         if card.group == table: clearAttachLinks(card)
         freeUnitPlacement(card)
         card.moveTo(card.owner.hand)
   if not silent: notify("{} returned {} to its owner's hand".format(me,card))
   debugNotify("<<< returnToHand()") #Debug
   
   
def drawCommand(group, silent = False):
   if debugVerbosity >= 1: notify(">>> drawCommand(){}".format(extraASDebug())) #Debug
   mute()
   if len(group) == 0 and len(myAllies) == 1:
      notify(":::ATTENTION::: {} cannot draw another card. {} loses the game!".format(me,me))
      reportGame('DeckDefeat')   
   card = group.top()
   card.moveTo(me.hand)
   if not silent: notify("{} Draws a command card.".format(me))

def drawCommandCard(card):
   if debugVerbosity >= 1: notify(">>> drawCommand(){}".format(extraASDebug())) #Debug
   mute()
   notify("{} Takes a command card from the {} position in their command deck to their hand.".format(me,numOrder(card.getIndex)))
   card.moveTo(me.hand)

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
   if debugVerbosity >= 2: notify(">>> About to announce()") #Debug
   if not silent: notify("{}'s new objective is {}.".format(me,card))
   
def playObjectiveCard(card):
   if debugVerbosity >= 1: notify(">>> drawObjective(){}".format(extraASDebug())) #Debug
   mute()
   currentObjectives = eval(me.getGlobalVariable('currentObjectives'))
   destroyedObjectives = eval(getGlobalVariable('destroyedObjectives'))
   for card_id in destroyedObjectives: 
      try: currentObjectives.remove(card_id) # Removing destroyed objectives before checking.
      except ValueError: pass 
   if len(currentObjectives) >= 3 and not confirm("You already control the maximum of 3 objectives. Are you sure you want to play another?"): return
   storeObjective(card)
   notify("{}'s new objective is {}.".format(me,card))
   
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
   if count > SSize and len(myAllies) == 1: 
      notify(":::ATTENTION::: {} cannot draw {} cards. {} loses the game!".format(me,count,me))
      reportGame('DeckDefeat')
      return 0
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

def flipCard(card,x,y):
   card.isFaceUp = True
   
def showatrandom(group = None, count = 1, targetPL = None, silent = False, covered = False):
   debugNotify(">>> showatrandom(){}".format(extraASDebug())) #Debug
   mute()
   shownCards = []
   side = 1
   if not targetPL: targetPL = me
   if not group: group = targetPL.hand
   if targetPL in fetchAllOpponents(): side = -1
   if len(group) == 0:
      whisper(":::WARNING::: {} had no cards in their hand!".format(targetPL))
      return shownCards
   elif count > len(group):
      whisper(":::WARNING::: {} has only {} cards in their hand.".format(targetPL,len(group)))
      count = len(group)
   for iter in range(count):
      card = group.random()
      if card.controller != me: # If we're revealing a card from another player's hand, we grab its properties before we put it on the table, as as not to give away if we're scanning it right now or not.
         card.isFaceUp = True
      if card == None:
         notify(":::Info:::{} has no more cards in their hand to reveal".format(targetPL))
         break
      if covered:
         cover = table.create("8b5a86df-fb10-4e5e-9133-7dc03fbae22d",playerside * side * iter * cwidth(card) - (count * cwidth(card) / 2), 0 - yaxisMove(card) * side,1,False)
         cover.moveToTable(playerside * side * iter * cwidth(card) - (count * cwidth(card) / 2), 0 - yaxisMove(card) * side,False)
      card.moveToTable(playerside * side * iter * cwidth(card) - (count * cwidth(card) / 2), 0 - yaxisMove(card) * side, False)
      card.highlight = RevealedColor
      card.sendToBack()
      if not covered: loopChk(card) # A small delay to make sure we grab the card's name to announce
      shownCards.append(card) # We put the revealed cards in a list to return to other functions that call us
   if not silent: notify("{} reveals {} at random from their hand.".format(targetPL,card))
   debugNotify("<<< showatrandom() with return {}".format(card), 2) #Debug
   return shownCards


#---------------------------------------------------------------------------
# Tokens and Markers
#---------------------------------------------------------------------------
	
def addFocus(card, x = 0, y = 0, count = 1):
   addMarker(card,'Focus',count)   
    
def addDamage(card, x = 0, y = 0, count = 1):
   addMarker(card,'Damage',count)    
   
def addShield(card, x = 0, y = 0, count = 1):
   addMarker(card,'Shield',count)

def addFocusTarget(group, x = 0, y = 0, count = 1):
   mute()
   for card in table:
      if card.targetedBy and card.targetedBy == me: addMarker(card,'Focus',count)
    
def addDamageTarget(group, x = 0, y = 0, count = 1):
   mute()
   for card in table:
      if card.targetedBy and card.targetedBy == me: addMarker(card,'Damage',count)
    
def addShieldTarget(group, x = 0, y = 0, count = 1):
   mute()
   for card in table:
      if card.targetedBy and card.targetedBy == me: addMarker(card,'Shield',count)

def addMarker(card, tokenType,count = 1, silent = False):
   debugNotify(">>> addMarker() with tokenType = {}".format(tokenType))
   mute()
   if tokenType == 'Shield':
      if not silent and card.markers[mdict['Shield']] and card.markers[mdict['Shield']] >= 1 and not confirm("This {} already has a shield. You are normally allowed only one shield per card.\n\nBypass Restriction?".format(card.Type)): return 'ABORT'
   if tokenType == 'Damage' and card.markers[mdict[tokenType]] == 0 and count > 0: # If this is the first damage marker this card gets, then we consider the card to be freshly damaged.
      executePlayScripts(card, 'DAMAGE')
   card.markers[mdict[tokenType]] += count	
   if not silent: notify("{} adds {} {} to {}.".format(me, count, tokenType, card))
   if tokenType == 'Shield' or tokenType == 'Focus' or tokenType == 'Damage':
      executePlayScripts(card, 'MARKERADD{}'.format(tokenType.upper()))
      #autoscriptOtherPlayers('{}MarkerAdded'.format(tokenType),card,count) # Don't need it yet, so I reduce the load
   debugNotify("<<< addMarker()")
      
def subFocus(card, x = 0, y = 0, count = 1):
   subMarker(card,'Focus',count)

def subDamage(card, x = 0, y = 0, count = 1):
   subMarker(card,'Damage',count)

def subShield(card, x = 0, y = 0, count = 1):
   subMarker(card,'Shield',count)

def subFocusTarget(group, x = 0, y = 0, count = 1):
   for card in table:
      if card.targetedBy and card.targetedBy == me: subMarker(card,'Focus',count)

def subDamageTarget(group, x = 0, y = 0, count = 1):
   for card in table:
      if card.targetedBy and card.targetedBy == me: subMarker(card,'Damage',count)

def subShieldTarget(group, x = 0, y = 0, count = 1):
   for card in table:
      if card.targetedBy and card.targetedBy == me: subMarker(card,'Shield',count)

def subMarker(card, tokenType,count = 1,silent = False):
   debugNotify(">>> subMarker() with tokenType = {}".format(tokenType))
   mute()
   if not silent: notify("{} removes {} {} from {}.".format(me, count, tokenType, card))
   card.markers[mdict[tokenType]] -= count	
   if tokenType == 'Shield' or tokenType == 'Focus' or tokenType == 'Damage':
      executePlayScripts(card, 'MARKERSUB{}'.format(tokenType.upper()))
      # autoscriptOtherPlayers('{}MarkerRemoved'.format(tokenType),card,count)  # Don't need it yet, so I reduce the load
   if tokenType == 'Damage' and not card.markers[mdict[tokenType]]:
      executePlayScripts(card, 'HEAL')
      # autoscriptOtherPlayers('CardHealed',card,count)  # Don't need it yet, so I reduce the load
   debugNotify("<<< subMarker()")
   
    
def addCustomMarker(cards, x = 0, y = 0): # A simple function to manually add any of the available markers.
   if debugVerbosity >= 1: notify(">>> addMarker(){}".format(extraASDebug())) #Debug
   mute()
   marker, quantity = askMarker() # Ask the player how many of the same type they want.
   if quantity == 0: return
   for card in cards: # Then go through their cards and add those markers to each.
      card.markers[marker] += quantity
      notify("{} adds {} {} counter to {}.".format(me, quantity, marker[0], card))

def clearEdgeMarker():
   debugNotify(">>> clearEdgeMarker()") #Debug
   for card in table:
      debugNotify("Checking {} which has {} edge markers".format(card,card.markers[mdict['Edge']]),4)
      if card.Type == 'Affiliation' and card.markers[mdict['Edge']]:
         debugNotify("Clearing Edge from {}".format(card))
         card.markers[mdict['Edge']] = 0
   debugNotify("<<< clearEdgeMarker()") #Debug
         
def gainEdge(group, x = 0, y = 0):
   mute()
   clearEdgeMarker()
   notify("{} gains the Edge.".format(me))
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
 
#------------------------------------------------------------------------------
# Button and Announcement functions
#------------------------------------------------------------------------------

def BUTTON_OK(group = None,x=0,y=0):
   notify("--- {} has no further reactions.".format(me))

def BUTTON_Wait(group = None,x=0,y=0):  
   notify("--- Wait! {} wants to react.".format(me))

def BUTTON_Actions(group = None,x=0,y=0):  
   notify("--- {} is waiting for opposing actions.".format(me))

def declarePass(group, x=0, y=0):
   notify("--- {} Passes".format(me))    