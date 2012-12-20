    # Python Scripts for the Star Wards LCG definition for OCTGN
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


import re, time

Automations = {'Play'    : True, # If True, game will automatically trigger card effects when playing or double-clicking on cards. Requires specific preparation in the sets.
               'Phase'                  : True, # If True, game will automatically trigger effects happening at the start of the player's phase, from cards they control.                
               'Triggers'               : True, # If True, game will search the table for triggers based on player's actions, such as installing a card, or discarding one.
               'WinForms'               : True, # If True, game will use the custom Windows Forms for displaying multiple-choice menus and information pop-ups
               'Placement'              : True, # If True, game will try to auto-place cards on the table after you paid for them.
               'Start/End-of-Turn/Phase': True, # If True, game will automatically trigger effects happening at the start of the player's turn, from cards they control.                
              }


UniCode = True # If True, game will display credits, clicks, trash, memory as unicode characters

debugVerbosity = -1 # At -1, means no debugging messages display

startupMsg = False # Used to check if the player has checked for the latest version of the game.

gameGUID = None # A Unique Game ID that is fetched during game launch.
#totalInfluence = 0 # Used when reporting online
#gameEnded = False # A variable keeping track if the players have submitted the results of the current game already.

CardsAA = {} # Dictionary holding all the AutoAction scripts for all cards
CardsAS = {} # Dictionary holding all the AutoScript scripts for all cards
Stored_Keywords = {} # A Dictionary holding all the Keywords a card has.

cardAttachementsNR = {} # A dictionary which counts how many attachment each host has
hostCards = {} # A dictionary which holds which is the host of each attachment
    
def storeSpecial(card): 
# Function stores into a shared variable some special cards that other players might look up.
   if debugVerbosity >= 1: notify(">>> storeSpecial(){}".format(extraASDebug())) #Debug
   specialCards = eval(me.getGlobalVariable('specialCards'))
   specialCards[card.Type] = card._id
   me.setGlobalVariable('specialCards', str(specialCards))

def storeObjective(card): 
# Function stores into a shared variable the current objectives of the player, so that other players might look them up.
# This function also reorganizes the objectives on the table
   if debugVerbosity >= 1: notify(">>> storeObjective(){}".format(extraASDebug())) #Debug
   currentObjectives = eval(me.getGlobalVariable('currentObjectives'))
   destroyedObjectives = eval(getGlobalVariable('destroyedObjectives'))
   for card_id in destroyedObjectives: 
      try:
         currentObjectives.remove(card_id) # Removing destroyed objectives before checking.
         destroyedObjectives.remove(card_id) # When we successfully remove an objective stored in this list, we clear it as well, so that we don't check it again in the future.
      except ValueError: pass # If an exception is thrown, it means that destroyed objective does not exist in this objective list
   currentObjectives.append(card._id)
   if debugVerbosity >= 2: notify("About to iterate the list: {}".format(currentObjectives))
   for iter in range(len(currentObjectives)):
      Objective = Card(currentObjectives[iter])
      Objective.moveToTable(playerside * -400, (playerside * 95) + (70 * iter * playerside) + yaxisMove(Objective))
      xPos, yPos = Objective.position
      countCaptures = 0 
      capturedCards = eval(getGlobalVariable('Captured Cards'))
      for capturedC in capturedCards: # once we move our objectives around, we want to move their captured cards with them as well.
         if capturedCards[capturedC] == Objective._id:
            if debugVerbosity >= 2: notify("Moved Objective has Captured cards. Moving them...")
            countCaptures += 1
            Card(capturedC).moveToTable(xPos - (cwidth(Objective) * playerside / 2 * countCaptures), yPos, True)
            Card(capturedC).sendToBack()
      #Objective.orientation = Rot90
   me.setGlobalVariable('currentObjectives', str(currentObjectives))
   setGlobalVariable('destroyedObjectives', str(destroyedObjectives))
   executePlayScripts(card, 'PLAY')

def getSpecial(cardType,player = me):
# Functions takes as argument the name of a special card, and the player to whom it belongs, and returns the card object.
   if debugVerbosity >= 1: notify(">>> getSpecial(){}".format(extraASDebug())) #Debug
   if cardType == 'BotD':   
      BotD = getGlobalVariable('Balance of the Force')
      if debugVerbosity >= 3: notify("<<< getSpecial() by returning: {}".format(Card(num(BotD))))
      return Card(num(BotD))
   else: 
      specialCards = eval(player.getGlobalVariable('specialCards'))
      if debugVerbosity >= 3: notify("<<< getSpecial() by returning: {}".format(Card(specialCards[cardType])))
      return Card(specialCards[cardType])

def checkUnique (card):
   if debugVerbosity >= 1: notify(">>> checkUnique(){}".format(extraASDebug())) #Debug
   mute()
   if not re.search(r'Unique', getKeywords(card)): 
      if debugVerbosity >= 3: notify("<<< checkUnique() - Not a unique card") #Debug
      return True #If the played card isn't unique do nothing.
   ExistingUniques = [ c for c in table
         if c.owner == me and c.isFaceUp and fetchProperty(c, 'name') == fetchProperty(card, 'name') and re.search(r'Unique', getKeywords(c)) ]
   if len(ExistingUniques) != 0 and not confirm("This unique card is already in play. Are you sure you want to play {}?\n\n(If you do, your existing unique card will be Trashed at no cost)".format(fetchProperty(card, 'name'))) : return False
   else:
      for uniqueC in ExistingUniques: trashForFree(uniqueC)
   if debugVerbosity >= 3: notify("<<< checkUnique() - Returning True") #Debug
   return True   

def ofwhom(Autoscript, controller = me): 
   if debugVerbosity >= 1: notify(">>> ofwhom(){}".format(extraASDebug(Autoscript))) #Debug
   targetPL = None
   if re.search(r'o[fn]Opponent', Autoscript):
      if len(players) > 1:
         if controller == me: # If we're the current controller of the card who's scripts are being checked, then we look for our opponent
            for player in players:
               if player.getGlobalVariable('Side') == '': continue # This is a spectator 
               elif player != me and player.getGlobalVariable('Side') != Side:
                  targetPL = player # Opponent needs to be not us, and of a different type. 
                                    # In the future I'll also be checking for teams by using a global player variable for it and having players select their team on startup.
         else: targetPL = me # if we're not the controller of the card we're using, then we're the opponent of the player (i.e. we're trashing their card)
      else: 
         if debugVerbosity >= 1: whisper("There's no valid Opponents! Selecting myself.")
         targetPL = me
   else: 
      if len(players) > 1:
         if controller != me: targetPL = controller         
         else: targetPL = me
      else: targetPL = me
   if debugVerbosity >= 3: notify("<<< ofwhom() returns {}".format(targetPL))
   return targetPL

def modifyDial(value):
   for player in players: player.counters['Death Star Dial'].value += value
   if me.counters['Death Star Dial'].value >= 12:
      notify("===::: The Dark Side wins the Game! :::====")

def resetAll(): # Clears all the global variables in order to start a new game.
   if debugVerbosity >= 1: notify(">>> resetAll(){}".format(extraASDebug())) #Debug
   global unpaidCard, edgeCount, edgeRevealed, firstTurn, debugVerbosity
   global Side, Affiliation, opponent, limitedPlayed
   mute()
   Side = None
   Affiliation = None
   unpaidCard = None 
   opponent = None
   edgeCount = 0 
   edgeRevealed = False
   firstTurn = True
   limitedPlayed = False
   cardAttachementsNR.clear()
   hostCards.clear()
   debugVerbosity = -1 # Reset means normal game.
   unitAmount = eval(getGlobalVariable('Existing Units')) # We clear the variable that holds how many units we have in tha game
   unitAmount[me.name] = 0  # This variable is used for unit placement
   setGlobalVariable('Existing Units',str(unitAmount))
   capturedCards = eval(getGlobalVariable('Captured Cards')) # This variable is for captured cards.
   capturedCards.clear()
   setGlobalVariable('Captured Cards',str(capturedCards))
   edgeRevealed = eval(getGlobalVariable('Revealed Edge'))
   for plName in edgeRevealed: edgeRevealed[plName] = False # Clearing some variables just in case they were left over. 
   setGlobalVariable('Revealed Edge',str(edgeRevealed))
   setGlobalVariable('Engaged Objective','None')
   setGlobalVariable('Engagement Phase','0')
   setGlobalVariable('Turn','0')
   me.setGlobalVariable('currentObjectives', '[]')
   if debugVerbosity >= 1: notify("<<< resetAll()") #Debug

def placeCard(card): 
   mute()
   if debugVerbosity >= 1: notify(">>> placeCard()") #Debug
   if Automations['Placement']:
      if card.Type == 'Unit': # For now we only place Units
         unitAmount = eval(getGlobalVariable('Existing Units'))
         if debugVerbosity >= 2: notify("### my unitAmount is: {}.".format(unitAmount[me.name])) #Debug
         freePositions = eval(me.getGlobalVariable('freePositions')) # We store the currently released position
         if debugVerbosity >= 2: notify("### my freePositions is: {}.".format(freePositions)) #Debug
         if freePositions != []: # We use this variable to see if there were any discarded units and we use their positions first.
            positionC = freePositions.pop() # This returns the last position in the list of positions and deletes it from the list.
            if debugVerbosity >= 2: notify("### positionC is: {}.".format(positionC)) #Debug
            card.moveToTable(positionC[0],positionC[1])
            me.setGlobalVariable('freePositions',str(freePositions))
         else:
            loopsNR = unitAmount[me.name] / 8
            loopback = 8 * loopsNR
            if unitAmount[me.name] == 0: xoffset = 0
            else: xoffset = -playerside * (1 - (2 * (unitAmount[me.name] % 2))) * (((unitAmount[me.name] - loopback) + 1) / 2) * cheight(card)
            if debugVerbosity >= 2: notify("### xoffset is: {}.".format(xoffset)) #Debug
            yoffset = yaxisMove(card) + (cheight(card,3) * (loopsNR + 1) * playerside)
            card.moveToTable(xoffset,yoffset)
         unitAmount[me.name] += 1
         setGlobalVariable('Existing Units',str(unitAmount)) # We update the amount of units we have
      if card.Type == 'Enhancement':
         hostType = re.search(r'Placement:([A-Za-z1-9:_ ]+)', CardsAS.get(card.model,''))
         if hostType:
            if debugVerbosity >= 2: notify("### hostType: {}.".format(hostType.group(1))) #Debug
            host = findTarget('Targeted-at{}'.format(hostType.group(1)))
            if host == []: 
               whisper("ABORTING!")
               return
            else:
               if debugVerbosity >= 2: notify("### About to update cardAttachementsNR dict") #Debug
               global cardAttachementsNR, hostCards
               hostCards[card._id] = host[0]._id
               try: cardAttachementsNR[host[0]._id] += 1
               except: cardAttachementsNR[host[0]._id] = 1
               if debugVerbosity >= 2: notify("### About to move into position") #Debug
               x,y = host[0].position
               card.moveToTable(x, y - ((cwidth(card) / 4 * playerside) * cardAttachementsNR[host[0]._id]))
               card.sendToBack()
   if debugVerbosity >= 3: notify("<<< placeCard()") #Debug
   
def findMarker(card, markerDesc): # Goes through the markers on the card and looks if one exist with a specific description
   if debugVerbosity >= 1: notify(">>> findMarker(){}".format(extraASDebug())) #Debug
   foundKey = None
   if markerDesc in mdict: markerDesc = mdict[markerDesc][0] # If the marker description is the code of a known marker, then we need to grab the actual name of that.
   for key in card.markers:
      if debugVerbosity >= 3: notify("### Key: {}\nmarkerDesc: {}".format(key[0],markerDesc)) # Debug
      if re.search(r'{}'.format(markerDesc),key[0]) or markerDesc == key[0]:
         foundKey = key
         if debugVerbosity >= 2: notify("### Found {} on {}".format(key[0],card))
         break
   if debugVerbosity >= 3: notify("<<< findMarker() by returning: {}".format(foundKey))
   return foundKey

def parseCombatIcons(STRING):
   # This function takes the printed combat icons of a card and returns a string that contains only the non-zero ones.
   if debugVerbosity >= 1: notify(">>> parseCombatIcons() with STRING: {}".format(STRING)) #Debug
   parsedIcons = ''
   UD = re.search(r'(?<!-)UD:([1-9])',STRING)
   EEUD = re.search(r'EE-UD:([1-9])',STRING)
   BD = re.search(r'(?<!-)BD:([1-9])',STRING)
   EEBD = re.search(r'EE-BD:([1-9])',STRING)
   T = re.search(r'(?<!-)T:([1-9])',STRING)
   EET = re.search(r'EE-T:([1-9])',STRING)
   if UD: parsedIcons += 'UD:{}. '.format(UD.group(1))
   if EEUD: parsedIcons += 'EE-UD:{}. '.format(EEUD.group(1))
   if BD: parsedIcons += 'BD:{}. '.format(BD.group(1))
   if EEBD: parsedIcons += 'EE-BD:{}. '.format(EEBD.group(1))
   if T: parsedIcons += 'T:{}. '.format(T.group(1))
   if EET: parsedIcons += 'EE-T:{}.'.format(EET.group(1))
   if debugVerbosity >= 3: notify("<<< parseCombatIcons() with return: {}".format(parsedIcons)) # Debug
   return parsedIcons

def calculateCombatIcons(card = None, CIString = None):
   # This function calculates how many combat icons a unit is supposed to have in a battle by adding bonuses from attachments as well.
   if debugVerbosity >= 1: notify(">>> calculateCombatIcons()") #Debug
   if card: combatIcons = card.properties['Combat Icons']
   elif CIString: combatIcons = CIString
   else: return
   if debugVerbosity >= 2: notify("### Setting Variables") #Debug
   Unit_Damage = 0
   Blast_Damage = 0
   Tactics = 0
   if debugVerbosity >= 2: notify("### About to process CI: {}".format(combatIcons)) #Debug
   UD = re.search(r'(?<!-)UD:([1-9])',combatIcons)
   EEUD = re.search(r'EE-UD:([1-9])',combatIcons)
   BD = re.search(r'(?<!-)BD:([1-9])',combatIcons)
   EEBD = re.search(r'EE-BD:([1-9])',combatIcons)
   T = re.search(r'(?<!-)T:([1-9])',combatIcons)
   EET = re.search(r'EE-T:([1-9])',combatIcons)
   if debugVerbosity >= 2: notify("### Icons Processed. Incrementing variables") #Debug
   if UD: Unit_Damage += num(UD.group(1))
   if EEUD and gotEdge(): Unit_Damage += num(EEUD.group(1))
   if BD: Blast_Damage += num(BD.group(1))
   if EEBD and gotEdge(): Blast_Damage += num(EEBD.group(1))
   if T: Tactics += num(T.group(1))
   if EET and gotEdge(): Tactics += num(EET.group(1))
   if debugVerbosity >= 2: notify("### Checking Markers") #Debug
   for marker in card.markers:
      if re.search(r':UD',marker[0]): Unit_Damage += card.markers[marker]
      if re.search(r':BD',marker[0]): Blast_Damage += card.markers[marker]
      if re.search(r':Tactics',marker[0]): Tactics += card.markers[marker]
   if debugVerbosity >= 2: notify("### Checking Attachments") #Debug
   if card: # We only check attachments if we're checking a host's Combat Icons.
      for attachment in hostCards:
         if hostCards[attachment] == card._id:
            if debugVerbosity >= 2: notify("### Found Attachment!") #Debug
            AS = CardsAS.get(Card(attachment).model,'')
            if AS == '': continue
            Autoscripts = AS.split('||')
            for AutoS in Autoscripts:
               if re.search(r'BonusIcons:',AutoS):
                  UD, BD, T = calculateCombatIcons(CIString = AutoS) # Recursion FTW!
                  Unit_Damage += UD
                  Blast_Damage += BD
                  Tactics += T
   if debugVerbosity >= 3: notify("<<< calculateCombatIcons() with return: {}".format((Unit_Damage,Blast_Damage,Tactics))) # Debug
   return (Unit_Damage,Blast_Damage,Tactics)
   
def gotEdge():
   if Affiliation.markers[mdict['Edge']] and Affiliation.markers[mdict['Edge']] == 1: return True
   else: return False

def getKeywords(card): # A function which combines the existing card keywords, with markers which give it extra ones.
   if debugVerbosity >= 1: notify(">>> getKeywords(){}".format(extraASDebug())) #Debug
   global Stored_Keywords
   #confirm("getKeywords") # Debug
   keywordsList = []
   cKeywords = card.Traits
   strippedKeywordsList = cKeywords.split('-')
   for cardKW in strippedKeywordsList:
      strippedKW = cardKW.strip() # Remove any leading/trailing spaces between traits. We need to use a new variable, because we can't modify the loop iterator.
      if strippedKW: keywordsList.append(strippedKW) # If there's anything left after the stip (i.e. it's not an empty string anymrore) add it to the list.   
   if card.markers:
      for key in card.markers:
         markerKeyword = re.search('Trait:([\w ]+)',key[0])
         if markerKeyword:
            #confirm("marker found: {}\n key: {}".format(markerKeyword.groups(),key[0])) # Debug
            #if markerKeyword.group(1) == 'Barrier' or markerKeyword.group(1) == 'Sentry' or markerKeyword.group(1) == 'Code Gate': #These keywords are mutually exclusive. An Ice can't be more than 1 of these
               #if 'Barrier' in keywordsList: keywordsList.remove('Barrier') # It seems in ANR, they are not so mutually exclusive. See: Tinkering
               #if 'Sentry' in keywordsList: keywordsList.remove('Sentry') 
               #if 'Code Gate' in keywordsList: keywordsList.remove('Code Gate')
            if re.search(r'Breaker',markerKeyword.group(1)):
               if 'Barrier Breaker' in keywordsList: keywordsList.remove('Barrier Breaker')
               if 'Sentry Breaker' in keywordsList: keywordsList.remove('Sentry Breaker')
               if 'Code Gate Breaker' in keywordsList: keywordsList.remove('Code Gate Breaker')
            keywordsList.append(markerKeyword.group(1))
   keywords = ''
   for KW in keywordsList:
      keywords += '{}-'.format(KW)
   Stored_Keywords[card._id] = keywords[:-1] # We also update the global variable for this card, which is used by many functions.
   if debugVerbosity >= 3: notify("<<< getKeywords() by returning: {}.".format(keywords[:-1]))
   return keywords[:-1] # We need to remove the trailing dash '-'

def reduceCost(card, action = 'PLAY', fullCost = 0, dryRun = False):
# A Functiona that scours the table for cards which reduce the cost of other cards.
# if dryRun is set to True, it means we're just checking what the total reduction is going to be and are not actually removing or adding any counters.
   type = action.capitalize()
   if debugVerbosity >= 1: notify(">>> reduceCost(). Action is: {}. FullCost = {}".format(type,fullCost)) #Debug
   if fullCost == 0: return 0 # If there's no cost, there's no use checking the table.
   fullCost = abs(fullCost)
   reduction = 0
   ### First we check if the card has an innate reduction. 
   Autoscripts = CardsAS.get(card.model,'').split('||') 
   if debugVerbosity >= 2: notify("### About to check if there's any onPay triggers on the card")
   if len(Autoscripts): 
      for autoS in Autoscripts:
         if not re.search(r'onPay', autoS): 
            if debugVerbosity >= 2: notify("### No onPay trigger found in {}!".format(autoS))
            continue
         elif debugVerbosity >= 2: notify("### onPay trigger found in {}!".format(autoS))
         reductionSearch = re.search(r'Reduce([0-9]+)Cost({}|All)'.format(type), autoS)
         if debugVerbosity >= 2: #Debug
            if reductionSearch: notify("!!! self-reduce regex groups: {}".format(reductionSearch.groups()))
            else: notify("!!! No self-reduce regex Match!")
         reduction += num(reductionSearch.group(1))
         fullCost -= 1
   if debugVerbosity >= 2: notify("### About to gather cards on the table")
   ### Now we check if any card on the table has an ability that reduces costs
   cardList = sortPriority([c for c in table
                           if c.controller == me
                           and c.isFaceUp])
   if debugVerbosity >= 2: notify("### About to iterate cards on the table")
   for c in cardList: # Then check if there's other cards in the table that reduce its costs.
      if fullCost == 0: 
         if debugVerbosity >= 2: notify("### No more cost. Aborting")
         break # If we don't have any more reduction to do, just break out.
      Autoscripts = CardsAS.get(c.model,'').split('||')
      if len(Autoscripts) == 0: continue
      for autoS in Autoscripts:
         if debugVerbosity >= 2: notify("### Checking {} with AS: {}".format(c, autoS)) #Debug
         reductionSearch = re.search(r'Reduce([0-9#X]+)Cost({}|All)-for([A-Z][A-Za-z ]+)(-not[A-Za-z_& ]+)?'.format(type), autoS) 
         if debugVerbosity >= 2: #Debug
            if reductionSearch: notify("!!! Regex is {}".format(reductionSearch.groups()))
            else: notify("!!! No reduceCost regex Match!") 
         if re.search(r'excludeDummy', autoS) and c.highlight == DummyColor: continue 
         if reductionSearch: # If the above search matches (i.e. we have a card with reduction for Rez and a condition we continue to check if our card matches the condition)
            if debugVerbosity >= 3: notify("### Possible Match found in {}".format(c)) # Debug         
            if reductionSearch.group(4): 
               exclusion = re.search(r'-not([A-Za-z_& ]+)'.format(type), reductionSearch.group(4))
               if exclusion and (re.search(r'{}'.format(exclusion.group(1)), fetchProperty(card, 'Type')) or re.search(r'{}'.format(exclusion.group(1)), fetchProperty(card, 'Keywords'))): continue
            if reductionSearch.group(3) == 'All' or re.search(r'{}'.format(reductionSearch.group(3)), card.Type) or re.search(r'{}'.format(reductionSearch.group(3)), card.Traits) or re.search(r'{}'.format(reductionSearch.group(3)), card.Affiliation): #Looking for the type of card being reduced into the properties of the card we're currently paying.
               if debugVerbosity >= 3: notify(" ### Search match! Group is {}".format(reductionSearch.group(1))) # Debug
               if re.search(r'onlyOnce',autoS):
                  if dryRun and oncePerTurn(c, silent = True, act = 'dryRun') == 'ABORT': continue
                  elif oncePerTurn(c, silent = True, act = 'automatic') == 'ABORT': continue # if the card's effect has already been used, check the next one
               if reductionSearch.group(1) == '#': # Still code from ANR. Not used yet but might be.
                  markersCount = c.markers[mdict['Credits']]
                  markersRemoved = 0
                  while fullCost > 0 and markersCount > 0:
                     if debugVerbosity >= 2: notify("### Reducing Cost with and Markers from {}".format(c)) # Debug
                     reduction += 1
                     fullCost -= 1
                     markersCount -= 1
                     markersRemoved += 1
                  if not dryRun: c.markers[mdict['Credits']] -= markersRemoved # If we have a dryRun, we don't remove any tokens.
               elif reductionSearch.group(1) == 'X':
                  markerName = re.search(r'-perMarker{([\w ]+)}', autoS)
                  try: 
                     marker = findMarker(c, markerName.group(1))
                     if marker: reduction = c.markers[marker]
                  except: notify("!!!ERROR!!! ReduceXCost - Bad Script")
               else:
                  reduction += num(reductionSearch.group(1)) # if there is a match, the total reduction for this card's cost is increased.
   if debugVerbosity >= 3: notify("<<< reduceCost() with reduction: {}".format(reduction))
   return reduction   
   
def haveForce():
   if debugVerbosity >= 1: notify(">>> chkForce()") #Debug
   myForce = False
   BotD = getSpecial('BotD')
   if Side == 'Dark': 
      if BotD.isAlternateImage: myForce = True
   else:
      if not BotD.isAlternateImage: myForce = True
   if debugVerbosity >= 4: notify("<<< chkForce() with return:{}".format(myForce)) #Debug
   return myForce
   
#------------------------------------------------------------------------------
# Switches
#------------------------------------------------------------------------------

def switchAutomation(type,command = 'Off'):
   if debugVerbosity >= 1: notify(">>> switchAutomation(){}".format(extraASDebug())) #Debug
   global Automations
   if (Automations[type] and command == 'Off') or (not Automations[type] and command == 'Announce'):
      notify ("--> {}'s {} automations are OFF.".format(me,type))
      if command != 'Announce': Automations[type] = False
   else:
      notify ("--> {}'s {} automations are ON.".format(me,type))
      if command != 'Announce': Automations[type] = True
   
def switchPlayAutomation(group,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> switchPlayAutomation(){}".format(extraASDebug())) #Debug
   switchAutomation('Play')
   
def switchPhaseAutomation(group,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> switchPhaseAutomation(){}".format(extraASDebug())) #Debug
   switchAutomation('Phase')

def switchTriggersAutomation(group,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> switchTriggersAutomation(){}".format(extraASDebug())) #Debug
   switchAutomation('Triggers')

def switchStartEndAutomation(group,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> switchStartEndAutomation(){}".format(extraASDebug())) #Debug
   if Automations['Start/End-of-Turn/Phase'] and not confirm(":::WARNING::: Disabling these automations means that you'll have to do each phase's effects manually.\
                                                            \nThis means removing a focus from each card, increasing the dial and refreshing your hand.\
                                                            \nThis can add a significant amount of time to each turn's busywork.\
                                                            \nAre you sure you want to disable? (You can re-enable again by using the same menu option)"): return
   switchAutomation('Start/End-of-Turn/Phase')
   
def switchWinForms(group,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> switchWinForms(){}".format(extraASDebug())) #Debug
   switchAutomation('WinForms')

def switchPlacement(group,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> switchPlacement(){}".format(extraASDebug())) #Debug
   switchAutomation('Placement')
   
def switchUniCode(group,x=0,y=0,command = 'Off'):
   if debugVerbosity >= 1: notify(">>> switchUniCode(){}".format(extraASDebug())) #Debug
   global UniCode
   if UniCode and command != 'On':
      whisper("Credits and Clicks will now be displayed as normal ASCII.".format(me))
      UniCode = False
   else:
      whisper("Credits and Clicks will now be displayed as Unicode.".format(me))
      UniCode = True

#------------------------------------------------------------------------------
# Help functions
#------------------------------------------------------------------------------

def HELP_BalancePhase(group,x=0,y=0):
   table.create('d98d94d5-57ef-4616-875d-41224784cb96', x, y, 1)
def HELP_RefreshPhase(group,x=0,y=0):
   table.create('1c13a82f-74f3-40fa-81f3-9b98523acfc3', x, y, 1)
def HELP_DrawPhase(group,x=0,y=0):
   table.create('6b6c8bd3-07ea-4b21-9ced-07562c16e7d7', x, y, 1)
def HELP_DeploymentPhase(group,x=0,y=0):
   table.create('6d18a054-516f-4ce4-aee5-ec22bb1f300f', x, y, 1)
def HELP_ConflictPhase(group,x=0,y=0):
   table.create('987517ed-111d-4ee0-a8a0-66b9f553e0a8', x, y, 1)
def HELP_ForcePhase(group,x=0,y=0):
   table.create('3aaf2774-97e5-4886-8476-49980647ddc1', x, y, 1)
      
#------------------------------------------------------------------------------
#  Online Functions
#------------------------------------------------------------------------------

def versionCheck():
   if debugVerbosity >= 1: notify(">>> versionCheck()") #Debug
   global startupMsg
   me.setGlobalVariable('gameVersion',gameVersion)
   if not startupMsg and len(players) > 1:
      #whisper("+++ Checking Version. Please Wait...")
      #rnd(1,10) # Need to pause a bit, otherwise the above notice will appear after urls have been fetched.
      (url, code) = webRead('https://raw.github.com/db0/Star-Wars-LCG-OCTGN/master/current_version.txt')
      if debugVerbosity >= 2: notify("### url:{}, code: {}".format(url,code)) #Debug
      if code != 200 or not url:
         whisper(":::WARNING::: Cannot check version at the moment.")
         return
      detailsplit = url.split('||')
      currentVers = detailsplit[0].split('.')
      installedVers = gameVersion.split('.')
      if len(installedVers) < 3:
         whisper("Your game definition does not follow the correct version conventions. It is most likely outdated or modified from its official release.")
         startupMsg = True
      elif num(currentVers[0]) > num(installedVers[0]) or num(currentVers[1]) > num(installedVers[1]) or num(currentVers[2]) > num(installedVers[2]):
         notify("{}'s game definition ({}) is out-of-date!".format(me, gameVersion))
         if confirm("There is a new game definition available!\nYour version: {}.\nCurrent version: {}\n{}\
                     {}\
                 \n\nDo you want to be redirected to download the latest version?.\
                   \n(You'll have to download the game definition, any patch for the current version and the markers if they're newer than what you have installed)\
                     ".format(gameVersion, detailsplit[0],detailsplit[2],detailsplit[1])):
            openUrl('https://github.com/db0/Star-Wars-LCG-OCTGN/downloads')
         startupMsg = True
      if not startupMsg: MOTD() # If we didn't give out any other message , we give out the MOTD instead.
      startupMsg = True
   if debugVerbosity >= 3: notify("<<< versionCheck()") #Debug
      
      
def MOTD():
   if debugVerbosity >= 1: notify(">>> MOTD()") #Debug
   (MOTDurl, MOTDcode) = webRead('https://raw.github.com/db0/Star-Wars-LCG-OCTGN/master/MOTD.txt')
   (DYKurl, DYKcode) = webRead('https://raw.github.com/db0/Star-Wars-LCG-OCTGN/master/DidYouKnow.txt')
   if (MOTDcode != 200 or not MOTDurl) or (DYKcode !=200 or not DYKurl):
      whisper(":::WARNING::: Cannot fetch MOTD or DYK info at the moment.")
      return
   DYKlist = DYKurl.split('||')
   DYKrnd = rnd(0,len(DYKlist)-1)
   while MOTDdisplay(MOTDurl,DYKlist[DYKrnd]) == 'MORE': 
      MOTDurl = '' # We don't want to spam the MOTD for the further notifications
      DYKrnd += 1
      if DYKrnd == len(DYKlist): DYKrnd = 0
   if debugVerbosity >= 3: notify("<<< MOTD()") #Debug
   
def MOTDdisplay(MOTD,DYK):
   if debugVerbosity >= 1: notify(">>> MOTDdisplay()") #Debug
   if re.search(r'http',MOTD): # If the MOTD has a link, then we do not sho DYKs, so that they have a chance to follow the URL
      MOTDweb = MOTD.split('&&')      
      if confirm("{}".format(MOTDweb[0])): openUrl(MOTDweb[1].strip())
   elif re.search(r'http',DYK):
      DYKweb = DYK.split('&&')
      if confirm("{}\
              \n\nDid You Know?:\
                \n------------------\
                \n{}".format(MOTD,DYKweb[0])):
         openUrl(DYKweb[1].strip())
   elif confirm("{}\
              \n\nDid You Know?:\
                \n-------------------\
                \n{}\
                \n-------------------\
              \n\nWould you like to see the next tip?".format(MOTD,DYK)): return 'MORE'
   return 'STOP'

def fetchCardScripts(group = table, x=0, y=0): # Creates 2 dictionaries with all scripts for all cards stored, based on a web URL or the local version if that doesn't exist.
   if debugVerbosity >= 1: notify(">>> fetchCardScripts()") #Debug
   global CardsAA, CardsAS # Global dictionaries holding Card AutoActions and Card AutoScripts for all cards.
   whisper("+++ Fetching fresh scripts. Please Wait...")
   if len(players) > 1:
      (ScriptsDownload, code) = webRead('https://raw.github.com/db0/Star-Wars-LCG-OCTGN/master/scripts/CardScripts.py')
   else: # If we have only one player, we assume it's a debug game and load scripts from local to save time.
      code = 0
      ScriptsDownload = None
   if debugVerbosity >= 4: notify("### code:{}, text: {}".format(code, ScriptsDownload)) #Debug
   if code != 200 or not ScriptsDownload or (ScriptsDownload and not re.search(r'ANR CARD SCRIPTS', ScriptsDownload)) or debugVerbosity >= 0: 
      whisper(":::WARNING::: Cannot download card scripts at the moment. Will use localy stored ones.")
      Split_Main = ScriptsLocal.split('=====') # Split_Main is separating the file description from the rest of the code
   else: 
      #WHAT THE FUUUUUCK? Why does it gives me a "value cannot be null" when it doesn't even come into this path with a broken connection?!
      #WHY DOES IT WORK IF I COMMENT THE NEXT LINE. THIS MAKES NO SENSE AAAARGH!
      #ScriptsLocal = ScriptsDownload #If we found the scripts online, then we use those for our scripts
      Split_Main = ScriptsDownload.split('=====')
   if debugVerbosity >= 5:  #Debug
      notify(Split_Main[1])
      notify('=====')
   Split_Cards = Split_Main[1].split('.....') # Split Cards is making a list of a different cards
   if debugVerbosity >= 5: #Debug
      notify(Split_Cards[0]) 
      notify('.....')
   for Full_Card_String in Split_Cards:
      if re.search(r'ENDSCRIPTS',Full_Card_String): break # If we have this string in the Card Details, it means we have no more scripts to load.
      Split_Details = Full_Card_String.split('-----') # Split Details is splitting the card name from its scripts
      if debugVerbosity >= 5:  #Debug
         notify(Split_Details[0])
         notify('-----')
      # A split from the Full_Card_String always should result in a list with 2 entries.
      if debugVerbosity >= 2: notify(Split_Details[0].strip()) # If it's the card name, notify us of it.
      Split_Scripts = Split_Details[2].split('+++++') # List item [1] always holds the two scripts. AutoScripts and AutoActions.
      CardsAS[Split_Details[1].strip()] = Split_Scripts[0].strip()
      CardsAA[Split_Details[1].strip()] = Split_Scripts[1].strip()
      if debugVerbosity >= 4: notify(Split_Details[0].strip() + "-- STORED")
   if num(getGlobalVariable('Turn')) > 0: whisper("+++ All card scripts refreshed!")
   if debugVerbosity >= 4: # Debug
      notify("CardsAS Dict:\n{}".format(str(CardsAS)))
      notify("CardsAA Dict:\n{}".format(str(CardsAA))) 
   if debugVerbosity >= 3: notify("<<< fetchCardScripts()") #Debug
   
#------------------------------------------------------------------------------
# Debugging
#------------------------------------------------------------------------------
   
def TrialError(group, x=0, y=0): # Debugging
   global Side, debugVerbosity
   mute()
   ######## Testing Corner ########
   #findTarget('Targeted-atVehicle_and_Fighter_or_Character_and_nonWookie')
   #BotD.moveToTable(0,0) 
   ###### End Testing Corner ######
   if debugVerbosity >=0: 
      if debugVerbosity == 0: 
         debugVerbosity = 1
         #ImAProAtThis() # At debug level 1, we also disable all warnings
      elif debugVerbosity == 1: debugVerbosity = 2
      elif debugVerbosity == 2: debugVerbosity = 3
      elif debugVerbosity == 3: debugVerbosity = 4
      else: debugVerbosity = 0
      notify("Debug verbosity is now: {}".format(debugVerbosity))
      return
   for player in players:
      if player.name == 'db0' or player.name == 'dbzer0': debugVerbosity = 0
   if not (len(players) == 1 or debugVerbosity >= 0): 
      whisper("This function is only for development purposes")
      return
   if not Side: 
      if confirm("Dark Side?"): Side = "Dark"
      else: Side = "Light"
   me.setGlobalVariable('Side', Side) 
   if not playerside:  # If we've already run this command once, don't recreate the cards.
      chooseSide()
      #createStartingCards()
#   for idx in range(len(testcards)):
#      test = table.create(testcards[idx], (70 * idx) - 150, 0, 1, True)
#      storeProperties(test)
#      if test.Type == 'ICE' or test.Type == 'Agenda' or test.Type == 'Asset': test.isFaceUp = False

def flipcard(card,x,y):
   card.switchImage
   if card.isAlternateImage: notify("is Alternate")
   elif not card.isAlternateImage: notify("is not Alternate")
   
def extraASDebug(Autoscript = None):
   if Autoscript and debugVerbosity >= 3: return ". Autoscript:{}".format(Autoscript)
   else: return ''

def ShowPos(group, x=0,y=0):
   if debugVerbosity >= 1: 
      notify('x={}, y={}'.format(x,y))
      
def ShowPosC(card, x=0,y=0):
   if debugVerbosity >= 1: 
      notify(">>> ShowPosC(){}".format(extraASDebug())) #Debug
      x,y = card.position
      notify('card x={}, y={}'.format(x,y))      
      
