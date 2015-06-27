    # Python Scripts for the Star Wards LCG definition for OCTGN
    # Copyright (C) 2013  Konstantine Thoukydides

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
# This file contains the autoscripting for cards with specialized effects. So called 'CustomScripts'
# * UseCustomAbility() is used among other scripts, and it just one custom ability among other normal core commands
# * CustomScipt() is a completely specialized effect, that is usually so unique, that it's not worth updating my core commands to facilitate it for just one card.
# Remote Functions are custom functions coming from specific cards which usually affect other players and are called via remoteCall()
###=================================================================================================================###

def UseCustomAbility(Autoscript, announceText, card, targetCards = None, notification = None, n = 0):
   mute()
   debugNotify(">>> UseCustomAbility() with Autoscript: {}".format(Autoscript)) #Debug
   if card.name == "Mara Jade": 
      remoteCall(card.controller,'MaraJade',[card])
      announceString = ''
   else: announceString = announceText 
   debugNotify("<<< UseCustomAbility() with announceString: {}".format(announceString)) #Debug
   return announceString

def CustomScript(card, action = 'PLAY'): # Scripts that are complex and fairly unique to specific cards, not worth making a whole generic function for them.
   debugNotify(">>> CustomScript() with action: {}".format(action)) #Debug
   mute()
   discardPile = me.piles['Discard Pile']
   objectives = me.piles['Objective Deck']
   deck = me.piles['Command Deck']
   if card.name == 'A Journey to Dagobah' and action == 'THWART' and card.owner == me:
      debugNotify("Journey to Dagobath Script")
      objList = []
      debugNotify("Moving objectives to removed from game pile")
      for c in objectives:
         c.moveTo(me.ScriptingPile)
         objList.append(c._id)
      rnd(1,10)
      objNames = []
      objDetails = []
      debugNotify("Storing objective properties and moving them back")
      for obj in objList:
         debugNotify("Card Name: {}".format(Card(obj).name),3)
         if Card(obj).name in objNames: 
            objList.remove(obj)
         else: 
            objNames.append(Card(obj).name)
            objDetails.append((Card(obj).Resources,Card(obj).properties['Damage Capacity'], Card(obj).Text)) # Creating a tuple with some details per objective
         Card(obj).moveTo(objectives)
      objChoices = []
      for iter in range(len(objList)):
         objChoices.append("{}\
                          \nResources {}, Damage Capacity: {}\
                          \nText: {}\
                          ".format(objNames[iter], objDetails[iter][0], objDetails[iter][1], objDetails[iter][2]))
      choice = SingleChoice("Which objective do you want to put into play from your deck?", objChoices, type = 'button', default = 0)
      if choice:
         storeObjective(Card(objList[choice]))
         shuffle(objectives)
         debugNotify("About to announce")
         notify("{} uses the ability of {} to replace it with {}".format(me,card,Card(objList[choice])))
   elif card.name == 'Black Squadron Pilot' and action == 'PLAY':
      if len(findTarget('AutoTargeted-atFighter_and_Unit-targetMine')) > 0 and confirm("This unit has an optional ability which allows it to be played as an enchantment on a fighter. Do so now?"):
         fighter = findTarget('AutoTargeted-atFighter_and_Unit-targetMine-choose1')
         if len(fighter) == 0: return
         hostCards = eval(getGlobalVariable('Host Cards'))
         hostCards[card._id] = fighter[0]._id
         setGlobalVariable('Host Cards',str(hostCards))
         cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == fighter[0]._id])
         debugNotify("About to move into position") #Debug
         x,y = fighter[0].position
         card.moveToTable(x, y - ((cwidth(card) / 4 * playerside) * cardAttachementsNR))
         card.sendToBack()
         TokensX('Put1isEnhancement-isSilent', '', card)
   elif card.name == 'Wedge Antilles' and action == 'PLAY':
      if len(findTarget('AutoTargeted-atFighter_or_Speeder-byAlly')) > 0 and confirm("This unit has an optional ability which allows it to be played as an enchantment on a Fighter or Speeder. Do so now?"):
         fighter = findTarget('AutoTargeted-atFighter_or_Speeder-byMe-choose1')
         if len(fighter) == 0: return
         hostCards = eval(getGlobalVariable('Host Cards'))
         hostCards[card._id] = fighter[0]._id
         setGlobalVariable('Host Cards',str(hostCards))
         cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == fighter[0]._id])
         debugNotify("About to move into position") #Debug
         x,y = fighter[0].position
         card.moveToTable(x, y - ((cwidth(card) / 4 * playerside) * cardAttachementsNR))
         card.sendToBack()
         TokensX('Put1isEnhancement-isSilent', '', card)
   elif card.name == 'Cruel Interrogations' and action == 'PLAY':
      for opponentPL in fetchAllOpponents():
         if len(opponentPL.hand) == 0: 
            whisper("{} had no cards in their hand.".format(opponentPL))
            continue
         captureTarget = opponentPL.hand.random()
         capture(chosenObj = card, targetC = captureTarget)
   elif card.name == 'Rancor' and action == 'afterCardRefreshing' and card.controller == me:
      possibleTargets = [c for c in table if c.Type == 'Unit' and not re.search('Vehicle',c.Traits)]
      if len(possibleTargets) == 0: return 'ABORT' # Nothing to kill
      minCost = 10 
      currTargets = []
      for c in possibleTargets:
         debugNotify("Checking {}".format(c),4)
         if num(c.Cost) < minCost:
            del currTargets[:]
            currTargets.append(c)
            minCost = num(c.Cost)
         elif num(c.Cost) == minCost: currTargets.append(c)
         else: pass
      debugNotify("Finished currTargets") #Debug         
      if debugVerbosity >= 4 and len(currTargets) > 0: notify("### Minimum Cost Targets = {}".format([c.name for c in currTargets])) #Debug
      if len(currTargets) == 1: finalTarget = currTargets[0]
      else: 
         choice = SingleChoice("Choose one unit to be destroyed by the Rancor", makeChoiceListfromCardList(currTargets), type = 'button', default = 0)
         if choice == None: 
            notify(":::NOTICE::: {} has skipped Rancor's effects this turn".format(me))
            return
         finalTarget = currTargets[choice]
      debugNotify("finalTarget = {}".format(finalTarget)) #Debug
      if finalTarget.controller == me: discard(finalTarget,silent = True)
      else: remoteCall(finalTarget.controller, 'discard', [finalTarget,0,0,True,False,me])
      if finalTarget == card: notify("{}'s Rancor destroys itself in its wild rampage".format(me))
      else: notify("{}'s Rancor rampages and destroys {}".format(me,finalTarget))
   elif card.name == 'Rescue Mission' and action == 'PLAY':
      currentTargets = findTarget('Targeted-isCaptured')
      if len(currentTargets) == 0: return
      targetC = currentTargets[0] # We always only have one target.
      targetC.isFaceUp = True
      loopChk(targetC,'Type')
      removeCapturedCard(targetC) 
      targetC.highlight = None
      if targetC.Type == 'Unit' and confirm("You have rescued {}. Do you want to put immediately into play?".format(targetC.name)): 
         placeCard(targetC)
         notify("{} has rescued {} and put them straight into action".format(me,targetC))
      else: 
         targetC.moveTo(targetC.owner.hand)
         notify("{} has rescued a card".format(me))
   elif card.name == 'Return of the Jedi' and action == 'PLAY':
      debugNotify("Return of the Jedi")
      discardList = []
      debugNotify("Moving Force Users to 'removed from game' pile from discard pile")
      for c in discardPile:
         c.moveTo(me.ScriptingPile)
         discardList.append(c._id)
      rnd(1,10)
      unitNames = []
      unitDetails = []
      ForceUserList = []
      debugNotify("Storing unit properties and moving them back")
      for unit in discardList:
         debugNotify("Card Name: {}".format(Card(unit).name),3)
         if not Card(unit).name in unitNames and re.search(r'Force User',Card(unit).Traits):
            ForceUserList.append(unit)
            unitNames.append(Card(unit).name)
            unitDetails.append((Card(unit).properties['Damage Capacity'],Card(unit).Traits,parseCombatIcons(Card(unit).properties['Combat Icons']),Card(unit).Text)) # Creating a tuple with some details per objective
         debugNotify("Finished Storing. Moving back",3)
         Card(unit).moveTo(discardPile)
      if len(ForceUserList) == 0: 
         whisper("::ERROR::: There is no force user in your discard pile!")
         return
      elif len(ForceUserList) == 1:
         choice = 0
      else:
         unitChoices = []
         for iter in range(len(ForceUserList)):
            unitChoices.append("{}\
                             \nDamage Capacity: {}\
                             \nTraits {}\
                             \nIcons: {}\
                             \nText: {}\
                             ".format(unitNames[iter], unitDetails[iter][0], unitDetails[iter][1], unitDetails[iter][2],unitDetails[iter][3]))
         choice = SingleChoice("Which Force User unit do you want to put into play from your discard pile?", unitChoices, type = 'button', default = 0)
      if choice:
         placeCard(Card(ForceUserList[choice]))
         debugNotify("About to announce")
         notify("{} returns into play".format(Card(ForceUserList[choice])))
   elif card.name == 'Superlaser Engineer' and action == 'PLAY': 
      cardList = []
      sendToBottomList = []
      iter = 0
      for c in deck.top(5):
         c.moveToTable((cwidth(c) * 2) - (iter * cwidth(c)),0)
         cardList.append(c._id)
         c.highlight = DummyColor
         iter += 1
      rnd(1,10)
      revealedCards = ''
      for cid in cardList: revealedCards += '{}, '.format(Card(cid))
      notify("{} activates the ability of their Superlaser Engineer and reveals the top 5 cards of their deck: {}".format(me,revealedCards))
      rnd(1,10)      
      for cid in cardList:
         if (Card(cid).Type == 'Event' or Card(cid).Type == 'Enhancement') and Card(cid).Affiliation == 'Imperial Navy' and num(Card(cid).Cost) >= 3:
            notify(":> {} moves {} to their hand".format(me,Card(cid)))
            Card(cid).moveTo(me.hand)
         else:
            sendToBottomList.append(Card(cid))
      sendToBottom(sendToBottomList)
   elif card.name == 'Take Them Prisoner' and action == 'PLAY': 
      debugNotify("Enterring 'Take Them Prisoner' Automation",1)
      turn = num(getGlobalVariable('Turn'))
      cardList = []
      cardNames = []
      cardDetails = []
      debugNotify("About to move cards to me.ScriptingPile",2)
      opponentPL = findOpponent('Ask','Choose player on whom to use Take Them Prisoner')
      for c in opponentPL.piles['Command Deck'].top(3):
         c.moveTo(me.ScriptingPile)
         cardList.append(c._id)
      rnd(1,10)
      for cid in cardList:
         debugNotify("Card Name: {}".format(Card(cid).name))
         cardNames.append(Card(cid).name)
         cardDetails.append((Card(cid).Type,Card(cid).properties['Damage Capacity'],Card(cid).Resources,Card(cid).Traits,parseCombatIcons(Card(cid).properties['Combat Icons']),Card(cid).Text)) # Creating a tuple with some details per objective
         debugNotify("Finished Storing.")
      ChoiceTXT = []
      for iter in range(len(cardList)):
         ChoiceTXT.append("{}\
                          \nType: {}\
                          \nDamage Capacity: {}, Resources: {}\
                          \nTraits: {}\
                          \nIcons: {}\
                          \nText: {}\
                          ".format(cardNames[iter], cardDetails[iter][0], cardDetails[iter][1], cardDetails[iter][2],cardDetails[iter][3],cardDetails[iter][4],cardDetails[iter][5]))
      choice = SingleChoice("Which card do you wish to capture?", ChoiceTXT, type = 'button', default = 0)
      if choice != None:
         capturedC = Card(cardList.pop(choice))
         capturedC.moveTo(opponentPL.piles['Command Deck']) # We move it back to the deck, so that the capture function can announce the correct location from which it was taken.
         debugNotify("About to capture.")
         capture(chosenObj = card,targetC = capturedC, silent = True)
         debugNotify("Removing choice text")
         ChoiceTXT.pop(choice) # We also remove the choice text entry at that point.
         choice = SingleChoice("Which card do you wish to leave on top of your opponent's command deck?", ChoiceTXT, type = 'button', default = 0,cancelButton = False)
         for iter in range(len(cardList)):
            debugNotify("Iter = {}".format(iter))
            if debugVerbosity >= 4: confirm("#### Moving {} (was at position {}. choice was {})".format(Card(cardList[iter]).name, iter,choice))
            if iter == choice: Card(cardList[iter]).moveTo(opponentPL.piles['Command Deck'],0)
            else: Card(cardList[iter]).moveTo(opponentPL.piles['Command Deck'],1)
         notify(":> {} activates Takes Them Prisoner to capture one card from the top 3 cards of {}'s command deck".format(me,opponentPL))
   elif card.name == 'Trench Run' and action == 'PLAY': # We move this card to the opponent's exile in order to try and give control to them automatically.
      if me.hasInvertedTable(): card.moveToTable(0,0)
      else:  card.moveToTable(0,-cheight(card))
      card.setController(findOpponent())
      debugNotify("About to whisper") # Debug
      whisper(":::IMPORTANT::: Please make sure that the controller for this card is always the Dark Side player")
   elif card.name == 'Twist of Fate' and action == 'RESOLVEFATE': 
      for card in table:
         if card.highlight == EdgeColor or card.highlight == FateColor:
            card.moveTo(card.owner.piles['Discard Pile'])
      notify(":> {} discards all edge cards and restarts the edge battle".format(card))
   elif card.name == "Vader's TIE Advanced" and action == 'STRIKE':
      delayed_whisper("-- Calculating Vader's TIE Advanced Combat Icons. Please wait...")
      TokensX('Remove999Vaders TIE Advance:UD-isSilent', '', card)
      TokensX('Remove999Vaders TIE Advance:BD-isSilent', '', card)
      TokensX('Remove999Vaders TIE Advance:Tactics-isSilent', '', card)
      if not confirm("Do you want to use Vader's TIE Advanced reaction?"): return
      disCard = deck.top()
      disCard.moveTo(discardPile)
      rnd(1,10)
      Unit_Damage, Blast_Damage, Tactics = calculateCombatIcons(card = disCard)
      if Unit_Damage: TokensX('Put{}Vaders TIE Advance:UD-isSilent'.format(Unit_Damage), '', card)
      if Blast_Damage: TokensX('Put{}Vaders TIE Advance:BD-isSilent'.format(Blast_Damage), '', card)
      if Tactics: TokensX('Put{}Vaders TIE Advance:Tactics-isSilent'.format(Tactics), '', card)
      if Unit_Damage or Blast_Damage or Tactics:
         notify("{} discards {} and Vader's TIE Advanced strike is boosted by {}".format(me,disCard,parseCombatIcons(disCard.properties['Combat Icons'])))
      else: 
         notify("{} discards {} and Vader's TIE Advanced strike is not boosted".format(me,disCard,parseCombatIcons(disCard.properties['Combat Icons'])))
   elif (card.name == "Yoda" or card.name == "Rogue Three") and action == 'STRIKE':
      delayed_whisper("-- Calculating Extra Combat Icons from enhancements. Please wait...")
      TokensX('Remove999Enhancement Bonus:UD-isSilent', '', card)
      TokensX('Remove999Enhancement Bonus:BD-isSilent', '', card)
      hostCards = eval(getGlobalVariable('Host Cards'))
      cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == card._id])
      if cardAttachementsNR and gotEdge():
         TokensX('Put{}Enhancement Bonus:UD-isSilent'.format(cardAttachementsNR), '', card)
         TokensX('Put{}Enhancement Bonus:BD-isSilent'.format(cardAttachementsNR), '', card)
   elif card.name == "Secret Informant" and action == 'USE':
      if card.orientation != Rot90:
         whisper(":::ERROR::: Secret Informant must be participating in the engagement to use her ability")
         return
      if len([c for c in table if c.highlight == FateColor and c.Type == 'Fate' and c.owner == me]) and not confirm("You are supposed to use this effect once you're already used all your fate cards on the table (i.e. they all should have a silver highlight now)\
                  \n\nHave you done this already?"): return
      for c in table:
         if c.highlight == EdgeColor and c.Type == 'Fate' and c.owner == me:
            c.highlight = FateColor
      notify("{}'s secret informant allows them to resolve all their fate cards an extra time this battle".format(me))
   elif card.name == "The Secret of Yavin 4" and action == 'USE':
      EngagedObjective = getGlobalVariable('Engaged Objective')
      if EngagedObjective == 'None': 
         whisper(":::Error::: No Engagement Currently ongoing")
         return
      else:
         currentTarget = Card(num(EngagedObjective))     
         if currentTarget.controller != me or currentTarget == card:
            whisper(":::Error::: Current engagement not at another one of your objectives.")
            return
      currentTarget.highlight = None
      card.highlight = DefendColor
      setGlobalVariable('Engaged Objective',str(card._id))
      notify("{} activates {} and moves the engagement to it".format(me,card))
   elif card.name == "Echo Caverns" and action == 'USE':
      if (card.markers[mdict['Focus']]
            and card.markers[mdict['Focus']] >= 1
            and not confirm("Card is already exhausted. Bypass?")):
         return 
      currentTargets = findTarget('Targeted-atUnit')
      if len(currentTargets) != 2:
         delayed_whisper(":::ERROR::: You must target exactly 2 units to use this ability")
         return
      cardATraits = currentTargets[0].Traits.split('-')
      cardBTraits = currentTargets[1].Traits.split('-')
      commonTrait = False
      for TraitA in cardATraits:
         if TraitA == 'Unique': continue # "Unique" is not an actual trait.
         if TraitA in cardBTraits: commonTrait = True
      if not commonTrait: 
         delayed_whisper(":::ERROR::: The two target units must share a common Trait.")
         return
      targetChoices = makeChoiceListfromCardList(currentTargets)
      choiceC = SingleChoice("Choose from which card to remove a combat icon", targetChoices, type = 'button', default = 0)
      if choiceC == 'ABORT': return
      debugNotify("choiceC = {}".format(choiceC),4) # Debug
      debugNotify("currentTargets = {}".format([currentTarget.name for currentTarget in currentTargets]),4) # Debug
      sourceCard = currentTargets.pop(choiceC)
      debugNotify("sourceCard = {}".format(sourceCard)) # Debug
      targetCard = currentTargets[0] # After we pop() the choice card, whatever remains is the target card.
      debugNotify("targetCard = {}".format(targetCard)) # Debug
      printedIcons = parseCombatIcons(sourceCard.properties['Combat Icons'])
      IconChoiceList = ["Unit Damage","Edge-Enabled Unit Damage","Blast Damage","Edge-Enabled Blast Damage","Tactics","Edge-Enabled Tactics"] # This list is a human readable one for the user to choose an icon
      IconList = ["UD","EE-UD","BD","EE-BD","Tactics","EE-Tactics"] # This list has the same icons as the above, but uses the keywords that the game expects in a marker, so it makes it easier to figure out which icon the user selected.
      debugNotify("About to select combat icon to steal")
      choiceIcons = SingleChoice("The card has the following printed Combat Icons: {}.\nChoose a combat icon to steal.\n(We leave the choice open, in case the card has received a combat icon from a card effect)".format(printedIcons), IconChoiceList, type = 'button', default = 0)
      #card.markers[mdict['Focus']] += 1
      addMarker(card, 'Focus',1, True)
      TokensX('Put1Echo Caverns:minus{}-isSilent'.format(IconList[choiceIcons]), '', sourceCard)
      TokensX('Put1Echo Caverns:{}-isSilent'.format(IconList[choiceIcons]), '', targetCard)
      notify("{} activates {} to move one {} icon from {} to {}".format(me,card,IconChoiceList[choiceIcons],sourceCard,targetCard))
   elif card.name == "Prophet of the Dark Side" and action == 'PLAY':
         debugNotify("Using Prophet of the Dark Side ability")
         cardView = me.piles['Command Deck'][1]
         cardView.moveTo(me.ScriptingPile)
         rnd(1,10)
         if not haveForce():
            delayed_whisper(":> The Prophet foresees that {} is upcoming!".format(cardView)) # If the player doesn't have the force, we just announce the card
         else: # If the player has the force, he has a chance to draw the card in their hand.
            StackTop = [cardView]
            cardDetails = makeChoiceListfromCardList(StackTop, True)
            if confirm("The Prophet Foresees:\n{}\n\nDo you want to draw this card".format(cardDetails[0])):
               cardView.moveTo(me.hand)
               notify("The Prophet of the Dark Side has drawn 1 card for {}".format(me))
         if cardView.group == me.ScriptingPile: cardView.moveTo(me.piles['Command Deck'])
         rnd(1,10)
   elif card.name == "Z-95 Headhunter" and action == 'STRIKE':
      opponentPL = findOpponent('Ask',"Choose one opponent on whom to use {}".format(card.name))
      shownCards = showatrandom(targetPL = opponentPL, silent = True)
      if len(shownCards) == 0:
         notify("{} has no cards in their hand".format(opponentPL))
         return
      notify("{} discovers {} in an surprise strike!".format(card,shownCards[0]))
      rnd(1,10)
      if fetchProperty(shownCards[0], 'Type') == 'Unit': 
         capture(targetC = shownCards[0], silent = True)
         notify("{} has captured a unit.".format(card))
      else: shownCards[0].moveTo(shownCards[0].owner.hand)
      rnd(1,10)
   elif card.name == "Last Defense of Hoth" and action == 'USE':
      if oncePerTurn(card, silent = True, act = 'manual') == 'ABORT': return
      if confirm("Do you want to use Last Defence of Hoth's special ability?"):
         topCard = me.piles['Command Deck'].top()
         if playEdge(topCard,True) != 'ABORT':
            notify("{} used {} to play an edge card from the top of their command deck".format(me,card))
   elif card.model == 'ff4fb461-8060-457a-9c16-000000000518': # Luke Skywalker B64/2
      if action == 'PLAY': # In this scenario, Luke is attaching to a fighter or speeder the player had targeted before they played him.
         vehicle = findTarget('Targeted-atFighter_or_Speeder-targetAllied-noTargetingError')
         if len(vehicle) > 0: #If the player has targeted a fighter or speeder we assume they wanted to play Luke in it.
            hostCards = eval(getGlobalVariable('Host Cards'))
            hostCards[card._id] = vehicle[0]._id
            setGlobalVariable('Host Cards',str(hostCards))
            cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == vehicle[0]._id])
            debugNotify("About to move into position") #Debug
            x,y = vehicle[0].position
            card.moveToTable(x, y - ((cwidth(card) / 4 * playerside) * cardAttachementsNR))
            card.sendToBack()
            TokensX('Put1isEnhancement-isSilent', '', card)
            notify("{} climbs into {}".format(card,vehicle[0]))
      if re.search(r'HOST-LEAVING',action): # In this scenario, Luke is coming into play after his host card left play.
            TokensX('Remove1isEnhancement-isSilent', '', card) # We unset Luke from being an enhancement
            hostCards = eval(getGlobalVariable('Host Cards')) # We clear Luke from the hostcards as this would lead him to get removed from play when his previous host left.
            del hostCards[card._id]
            setGlobalVariable('Host Cards',str(hostCards))
            placeCard(card)
            executePlayScripts(card, 'PLAY') # We execute the play scripts here only if the card is 0 cost.
            autoscriptOtherPlayers('CardPlayed',card)
            notify("{} ejects from their vehicle to safety".format(card))
   elif card.name == "Dengar" and action == 'STRIKE':
      delayed_whisper("-- Calculating Extra Combat Icons from captured cards. Please wait...")
      TokensX('Remove999Captured Bonus:UD-isSilent', '', card)
      TokensX('Remove999Captured Bonus:BD-isSilent', '', card)
      TokensX('Remove999Captured Bonus:Tactics-isSilent', '', card)
      capturedCards = eval(getGlobalVariable('Captured Cards'))
      cardCapturesNR = len([att_id for att_id in capturedCards if capturedCards[att_id] == card._id])
      if cardCapturesNR:
         for iconIter in range(cardCapturesNR):
            choice = SingleChoice("Choose the {} icon".format(numOrder(iconIter)), ['Unit Damage','Blast Damage', 'Tactics'], type = 'button', default = 0)
            if choice == 0: TokensX('Put1Captured Bonus:UD-isSilent', '', card)
            elif choice == 1: TokensX('Put1Captured Bonus:BD-isSilent', '', card)
            elif choice == 2: TokensX('Put1Captured Bonus:Tactics-isSilent', '', card)
            else: break
   elif card.model == 'ff4fb461-8060-457a-9c16-000000000548' and action == 'Automatic': # Obi-Wan Kenobi B91/2
      for player in myAllies: remoteCall(player,'ObiWan_B91',[card])
   elif card.name == "Blue Squadron Support" and action == 'USE':
      for player in myAllies: remoteCall(player,'BlueSquadronSupport',[card])
   elif card.name == "Repair and Refurbish" and action == 'Start':
      for player in myAllies: remoteCall(player,'RepairRefurbish',[card])
   elif card.name == "Weapons Upgrade" and action == 'PLAY':
      hostCards = eval(getGlobalVariable('Host Cards'))
      try:
         if Card(hostCards[card._id]).controller != me:
            DrawX('Draw1Card', "{} provides a {} to a friendly unit to".format(me,card), card, targetCards = None, notification = 'Quick', n = 0)
      except: whisper(":::ERROR::: when looking for host of {}".format(card))
   elif card.model == 'ff4fb461-8060-457a-9c16-000000000902': # Derek "Hobbie" Klivian B141/2
      if action == 'PLAY': # In this scenario, Hobbie is attaching to a vehicle the player had targeted before they played him.
         vehicle = findTarget('Targeted-atVehicle-targetAllied-noTargetingError')
         if len(vehicle) > 0: #If the player has targeted a fighter or speeder we assume they wanted to put Hobbie in it.
            hostCards = eval(getGlobalVariable('Host Cards'))
            hostCards[card._id] = vehicle[0]._id
            setGlobalVariable('Host Cards',str(hostCards))
            cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == vehicle[0]._id])
            debugNotify("About to move into position") #Debug
            x,y = vehicle[0].position
            card.moveToTable(x, y - ((cwidth(card) / 4 * playerside) * cardAttachementsNR))
            card.sendToBack()
            TokensX('Put1isEnhancement-isSilent', '', card)
            notify("{} climbs into {}".format(card,vehicle[0]))
   elif card.model == 'ff4fb461-8060-457a-9c16-000000000908': # Lando Calrissian B142/2
      if action == 'PLAY': # In this scenario, Lando is attaching to a vehicle the player had targeted before they played him.
         vehicle = findTarget('Targeted-atVehicle-targetAllied-noTargetingError')
         if len(vehicle) > 0: #If the player has targeted a fighter or speeder we assume they wanted to put Lando in it.
            hostCards = eval(getGlobalVariable('Host Cards'))
            hostCards[card._id] = vehicle[0]._id
            setGlobalVariable('Host Cards',str(hostCards))
            cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == vehicle[0]._id])
            debugNotify("About to move into position") #Debug
            x,y = vehicle[0].position
            card.moveToTable(x, y - ((cwidth(card) / 4 * playerside) * cardAttachementsNR))
            card.sendToBack()
            TokensX('Put1isEnhancement-isSilent', '', card)
            notify("{} climbs into {}".format(card,vehicle[0]))
   elif card.model == 'ff4fb461-8060-457a-9c16-000000000914': # "Mauler" Mithel B143/2
      if action == 'PLAY': # In this scenario, Mauler is attaching to a vehicle the player had targeted before they played him.
         vehicle = findTarget('Targeted-atVehicle-targetAllied-noTargetingError')
         if len(vehicle) > 0: #If the player has targeted a fighter or speeder we assume they wanted to put Mauler in it.
            hostCards = eval(getGlobalVariable('Host Cards'))
            hostCards[card._id] = vehicle[0]._id
            setGlobalVariable('Host Cards',str(hostCards))
            cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == vehicle[0]._id])
            debugNotify("About to move into position") #Debug
            x,y = vehicle[0].position
            card.moveToTable(x, y - ((cwidth(card) / 4 * playerside) * cardAttachementsNR))
            card.sendToBack()
            TokensX('Put1isEnhancement-isSilent', '', card)
            notify("{} climbs into {}".format(card,vehicle[0]))
   elif card.model == 'ff4fb461-8060-457a-9c16-000000000920': # Baron Fel B144/2
      if action == 'PLAY': # In this scenario, Fel is attaching to a vehicle the player had targeted before they played him.
         vehicle = findTarget('Targeted-atVehicle-targetAllied-noTargetingError')
         if len(vehicle) > 0: #If the player has targeted a fighter or speeder we assume they wanted to put Fel in it.
            hostCards = eval(getGlobalVariable('Host Cards'))
            hostCards[card._id] = vehicle[0]._id
            setGlobalVariable('Host Cards',str(hostCards))
            cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == vehicle[0]._id])
            debugNotify("About to move into position") #Debug
            x,y = vehicle[0].position
            card.moveToTable(x, y - ((cwidth(card) / 4 * playerside) * cardAttachementsNR))
            card.sendToBack()
            TokensX('Put1isEnhancement-isSilent', '', card)
            notify("{} climbs into {}".format(card,vehicle[0]))
   elif card.model == 'ff4fb461-8060-457a-9c16-000000000926': # Niles Ferrier B145/2
      if action == 'PLAY': # In this scenario, Niles is attaching to a vehicle the player had targeted before they played him.
         vehicle = findTarget('Targeted-atVehicle-noTargetingError')
         if len(vehicle) > 0: #If the player has targeted a fighter or speeder we assume they wanted to put Niles in it.
            hostCards = eval(getGlobalVariable('Host Cards'))
            hostCards[card._id] = vehicle[0]._id
            setGlobalVariable('Host Cards',str(hostCards))
            cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == vehicle[0]._id])
            debugNotify("About to move into position") #Debug
            x,y = vehicle[0].position
            card.moveToTable(x, y - ((cwidth(card) / 4 * playerside) * cardAttachementsNR))
            card.sendToBack()
            TokensX('Put1isEnhancement-isSilent', '', card)
            notify("{} climbs into {}".format(card,vehicle[0]))
   elif card.model == 'ff4fb461-8060-457a-9c16-000000000938': # Grey Squadron Gunner B147/2
      if action == 'PLAY': # In this scenario, Gunner is attaching to a vehicle the player had targeted before they played him.
         vehicle = findTarget('Targeted-atVehicle-targetAllied-noTargetingError')
         if len(vehicle) > 0: #If the player has targeted a vehicle we assume they wanted to put Gunner in it.
            hostCards = eval(getGlobalVariable('Host Cards'))
            hostCards[card._id] = vehicle[0]._id
            setGlobalVariable('Host Cards',str(hostCards))
            cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == vehicle[0]._id])
            debugNotify("About to move into position") #Debug
            x,y = vehicle[0].position
            card.moveToTable(x, y - ((cwidth(card) / 4 * playerside) * cardAttachementsNR))
            card.sendToBack()
            TokensX('Put1isEnhancement-isSilent', '', card)
            notify("{} climbs into {}".format(card,vehicle[0]))
   elif card.model == 'ff4fb461-8060-457a-9c16-000000000944': # LE-B02D9 B148/2
      if action == 'PLAY': # In this scenario, LE-B02D9 is attaching to a vehicle the player had targeted before they played him.
         vehicle = findTarget('Targeted-atVehicle--targetAllied-noTargetingError')
         if len(vehicle) > 0: #If the player has targeted a Vehicle we assume they wanted to put LE-B02D9 in it.
            hostCards = eval(getGlobalVariable('Host Cards'))
            hostCards[card._id] = vehicle[0]._id
            setGlobalVariable('Host Cards',str(hostCards))
            cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == vehicle[0]._id])
            debugNotify("About to move into position") #Debug
            x,y = vehicle[0].position
            card.moveToTable(x, y - ((cwidth(card) / 4 * playerside) * cardAttachementsNR))
            card.sendToBack()
            TokensX('Put1isEnhancement-isSilent', '', card)
            notify("{} climbs into {}".format(card,vehicle[0]))
   elif card.model == 'ff4fb461-8060-457a-9c16-000000000950': # Maarek Stele B149/2
      if action == 'PLAY': # In this scenario, Maarek is attaching to a vehicle the player had targeted before they played him.
         vehicle = findTarget('Targeted-atVehicle-targetAllied-noTargetingError')
         if len(vehicle) > 0: #If the player has targeted a Vehicle we assume they wanted to put Maarek in it.
            hostCards = eval(getGlobalVariable('Host Cards'))
            hostCards[card._id] = vehicle[0]._id
            setGlobalVariable('Host Cards',str(hostCards))
            cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == vehicle[0]._id])
            debugNotify("About to move into position") #Debug
            x,y = vehicle[0].position
            card.moveToTable(x, y - ((cwidth(card) / 4 * playerside) * cardAttachementsNR))
            card.sendToBack()
            TokensX('Put1isEnhancement-isSilent', '', card)
            notify("{} climbs into {}".format(card,vehicle[0]))
   elif card.model == 'ff4fb461-8060-457a-9c16-000000000956': # DS-61-3 B150/2
      if action == 'PLAY': # In this scenario, DS-61-3 is attaching to a vehicle the player had targeted before they played him.
         vehicle = findTarget('Targeted-atVehicle-targetAllied-noTargetingError')
         if len(vehicle) > 0: #If the player has targeted a Vehicle we assume they wanted to put DS-61-3 in it.
            hostCards = eval(getGlobalVariable('Host Cards'))
            hostCards[card._id] = vehicle[0]._id
            setGlobalVariable('Host Cards',str(hostCards))
            cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == vehicle[0]._id])
            debugNotify("About to move into position") #Debug
            x,y = vehicle[0].position
            card.moveToTable(x, y - ((cwidth(card) / 4 * playerside) * cardAttachementsNR))
            card.sendToBack()
            TokensX('Put1isEnhancement-isSilent', '', card)
            notify("{} climbs into {}".format(card,vehicle[0]))			
   elif card.model == 'ff4fb461-8060-457a-9c16-000000000980': # Academy Pilot B154/2
      if action == 'PLAY': # In this scenario, Academy Pilot is attaching to a vehicle the player had targeted before they played him.
         vehicle = findTarget('Targeted-atVehicle-targetAllied-noTargetingError')
         if len(vehicle) > 0: #If the player has targeted a Vehicle we assume they wanted to put DS-61-3 in it.
            hostCards = eval(getGlobalVariable('Host Cards'))
            hostCards[card._id] = vehicle[0]._id
            setGlobalVariable('Host Cards',str(hostCards))
            cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == vehicle[0]._id])
            debugNotify("About to move into position") #Debug
            x,y = vehicle[0].position
            card.moveToTable(x, y - ((cwidth(card) / 4 * playerside) * cardAttachementsNR))
            card.sendToBack()
            TokensX('Put1isEnhancement-isSilent', '', card)
            notify("{} climbs into {}".format(card,vehicle[0]))			
   elif card.model == 'ff4fb461-8060-457a-9c16-000000000981': # Academy Pilot B154/3
      if action == 'PLAY': # In this scenario, Academy Pilot is attaching to a vehicle the player had targeted before they played him.
         vehicle = findTarget('Targeted-atVehicle-targetAllied-noTargetingError')
         if len(vehicle) > 0: #If the player has targeted a Vehicle we assume they wanted to put DS-61-3 in it.
            hostCards = eval(getGlobalVariable('Host Cards'))
            hostCards[card._id] = vehicle[0]._id
            setGlobalVariable('Host Cards',str(hostCards))
            cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == vehicle[0]._id])
            debugNotify("About to move into position") #Debug
            x,y = vehicle[0].position
            card.moveToTable(x, y - ((cwidth(card) / 4 * playerside) * cardAttachementsNR))
            card.sendToBack()
            TokensX('Put1isEnhancement-isSilent', '', card)
            notify("{} climbs into {}".format(card,vehicle[0]))			
   else: notify("{} uses {}'s ability".format(me,card)) # Just a catch-all.
   
def chkLookupRestrictions(card,lookup,origin_card):
   debugNotify(">>> chkLookupRestrictions()") # Debug
   validCard = True
   if card.name == "Agent of the Hand": # This card check requires that we compare the variables in lookup before we proceed. 
      takeoverRegex = re.search(r'(\w+):CardTakeover:(\w+)', lookup)
      playedReserveRegex = re.search(r'(\w+):ReservesPlayed:(\w+)', lookup)
      if takeoverRegex:
         debugNotify("takeoverRegex = {}".format(takeoverRegex.groups()), 4)
         if takeoverRegex.group(1) != card.controller.name or takeoverRegex.group(2) == card.controller.name: 
            debugNotify("Failed {} chkLookupRestrictions() for {}".format(card,lookup))
            validCard = False
            # Agent of the hand only triggers if its controller took control of a unit from another player.  group(1) is the player who took control, group(2) is the player who had control before.
            # So if the lookup was a takeover regex but the new controller (group(1)) is not the controller of AotH or the old controller (group(2)) was the same player, then it failed the check
      elif playedReserveRegex: 
         debugNotify("playedReserveRegex = {}".format(playedReserveRegex.groups()), 4)
         if playedReserveRegex.group(1) != card.controller.name or playedReserveRegex.group(2) == card.controller.name: 
            debugNotify("Failed {} chkLookupRestrictions() for {}".format(card,lookup))
            validCard = False      
            # Agent of the hand's ReservesPlayed only triggers if its controller is the reserves playing player (group(1)) and they played a common reserves card from another player (group(2))   
      else: 
         debugNotify("Failed {} chkLookupRestrictions() because there's no valid lookup".format(card))
         validCard = False
   debugNotify("<<< chkLookupRestrictions() with validCard == {}".format(validCard)) # Debug
   return validCard

#------------------------------------------------------------------------------
# Remote Functions
#------------------------------------------------------------------------------
      
def ObiWan_B91(card):
   mute()
   debugNotify(">>> ObiWan_B91()") # Debug
   if len(me.piles['Discard Pile']) >= 1:
      topCard = me.piles['Discard Pile'].top()
      cardTexts = makeChoiceListfromCardList([topCard], True, True)
      if confirm("Obi-Wan's guidance allows you to return the top card of your discard pile to your hand. Do so?\n\n{}".format(cardTexts[0])): 
         topCard.moveTo(me.hand)
         notify(":> {} receives {}'s Guidance.".format(me,card))
   else: notify(":> {} tried to mentor {} but the young padawan hasn't discarded any cards yet.".format(card,me))
   debugNotify("<<< ObiWan_B91()") # Debug

def BlueSquadronSupport(card):
   mute()
   debugNotify(">>> BlueSquadronSupport()") # Debug
   if len(me.piles['Command Deck']) == 1:
      me.piles['Command Deck'].top().moveTo(me.hand)
      notify(":> {} resolved their {} to draw their last card from their deck.".format(me,card))
   elif len(me.piles['Command Deck']) == 0: notify(":> {} tried to resolve their {} but had no more cards in their deck.".format(me,card))
   else:
      topCards = list(me.piles['Command Deck'].top(2))
      for c in topCards: c.moveTo(me.hand) # We move them to the hand to allow us to read their properties
      choice = None
      while choice == None: choice = SingleChoice("== Blue Squadron Support == \n\nWhich card do you wish put at the bottom of your deck?", makeChoiceListfromCardList(topCards, True, True))
      topCards[choice].moveToBottom(me.piles['Command Deck']) # Finally we place the remaining card at the bottom of our deck
      notify(":> {} resolved their {}.".format(me,card))
   debugNotify("<<< BlueSquadronSupport()") # Debug
   
def MaraJade(card):
   debugNotify(">>> MaraJade()") # Debug
   mute()
   if len(myAllies) > 1 and confirm("Do you want to pass control of Mara Jade to another friendly player?"):
      targetAlly = ofwhom('-ofAllies', me)
      giveCard(card,targetAlly[0])
      remoteCall(targetAlly[0],'placeCard',[card])
      notify(":> {} passed control of {} to {}.".format(me,card,targetAlly[0]))
      #autoscriptOtherPlayers('{}:CardTakeover:{}'.format(targetAlly,me),card) # To allow Agent of the Hand to work
   debugNotify("<<< MaraJade()") # Debug      

def RepairRefurbish(card):
   mute()
   debugNotify(">>> RepairRefurbish()") # Debug
   damagedObjs = [c for c in table if c.Type == 'Objective' and c.controller == me and c.markers[mdict['Damage']]]
   debugNotify("{} damagedObjs gathered".format(len(damagedObjs)))
   if len(damagedObjs):
      choice = SingleChoice("Which of your objectives would you like to repair and refurbish?", makeChoiceListfromCardList(damagedObjs))
      damagedObjs[choice].markers[mdict['Damage']] -= 1
      notify(":> {} {}es {}.".format(me,card,damagedObjs[choice]))
   debugNotify("<<< RepairRefurbish()") # Debug

   
def RemoteFunctionTemplate():
# Quick Copy this into a new Remote Function
   mute()
   debugNotify(">>> RemoteFunctionTemplate()") # Debug
   debugNotify("<<< RemoteFunctionTemplate()") # Debug   
