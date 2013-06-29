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

import re

failedRequirement = True #A Global boolean that we set in case an Autoscript cost cannot be paid, so that we know to abort the rest of the script.
selectedAbility = {} # Used to track which ability of multiple the player is trying to pay.
Dummywarn = True
#------------------------------------------------------------------------------
# Play/Score/Rez/Trash trigger
#------------------------------------------------------------------------------

def executePlayScripts(card, action):
   #action = action.upper() # Just in case we passed the wrong case
   if debugVerbosity >= 1: notify(">>> executePlayScripts() with action: {}".format(action)) #Debug
   global failedRequirement
   if not Automations['Play']: return
   if not card.isFaceUp: return
   if CardsAS.get(card.model,'') != '': # Commented in order to allow scripts in attacked cards to trigger
      if debugVerbosity >= 2: notify("#### We have autoScripts!") # Debug
      if card.highlight == CapturedColor or card.highlight == EdgeColor or card.highlight == UnpaidColor: return
      failedRequirement = False
      X = 0
      Autoscripts = CardsAS.get(card.model,'').split('||') # When playing cards, the || is used as an "and" separator, rather than "or". i.e. we don't do choices (yet)
      autoScriptsSnapshot = list(Autoscripts) # Need to work on a snapshot, because we'll be modifying the list.
      if debugVerbosity >= 2: notify("#### List of autoscripts before scrubbing: {}".format(Autoscripts)) # Debug
      for autoS in autoScriptsSnapshot: # Checking and removing any "AtTurnStart" clicks.
         if (re.search(r'atTurn(Start|End)', autoS) or 
             re.search(r'after([A-za-z]+)', autoS) or 
             re.search(r'Placement', autoS) or 
             re.search(r'BonusIcons', autoS) or 
             re.search(r'Increase', autoS) or 
             re.search(r'ExtraIcon', autoS) or 
             re.search(r'DeployAllowance', autoS) or 
             re.search(r'ConstantEffect', autoS) or 
             re.search(r'EngagedAsObjective', autoS) or 
             re.search(r'IgnoreAffiliationMatch', autoS) or 
             re.search(r'onPay', autoS) or # onPay effects are only useful before we go to the autoscripts, for the cost reduction.
             re.search(r'-isTrigger', autoS) or
             re.search(r'Empty', autoS)): Autoscripts.remove(autoS) # Empty means the card has no autoscript, but we still want an empty list.
         elif re.search(r'excludeDummy', autoS) and card.highlight == DummyColor: Autoscripts.remove(autoS)
         elif re.search(r'onlyforDummy', autoS) and card.highlight != DummyColor: Autoscripts.remove(autoS)
         elif re.search(r'CustomScript', autoS): 
            CustomScript(card,action)
            Autoscripts.remove(autoS)
      if debugVerbosity >= 2: notify ('Looking for multiple choice options') # Debug
      if action == 'PLAY': trigger = 'onPlay' # We figure out what can be the possible multiple choice trigger
      elif action == 'TRASH': trigger = 'onDiscard'
      elif action == 'CAPTURE': trigger = 'onCapture'
      else: trigger = 'N/A'
      if debugVerbosity >= 2: notify ('trigger = {}'.format(trigger)) # Debug
      if trigger != 'N/A': # If there's a possibility of a multiple choice trigger, we do the check
         TriggersFound = [] # A List which will hold any valid abilities for this trigger
         for AutoS in Autoscripts:
            if re.search(r'{}:'.format(trigger),AutoS): # If the script has the appropriate trigger, we put it into the list.
               TriggersFound.append(AutoS)
         if debugVerbosity >= 2: notify ('TriggersFound = {}'.format(TriggersFound)) # Debug
         if len(TriggersFound) > 1: # If we have more than one option for this trigger, we need to ask the player for which to use.
            if Automations['WinForms']: ChoiceTXT = "This card has multiple abilities that can trigger at this point.\nSelect the ones you would like to use."
            else: ChoiceTXT = "This card has multiple abilities that can trigger at this point.\nType the number of the one you would like to use."
            triggerInstructions = re.search(r'{}\[(.*?)\]'.format(trigger),card.Instructions) # If the card has multiple options, it should also have some card instructions to have nice menu options.
            if not triggerInstructions and debugVerbosity >= 1: notify("## Oops! No multiple choice instructions found and I expected some. Will crash prolly.") # Debug
            cardInstructions = triggerInstructions.group(1).split('|-|') # We instructions for trigger have a slightly different split, so as not to conflict with the instructions from AutoActions.
            choices = cardInstructions
            abilChoice = SingleChoice(ChoiceTXT, choices, type = 'button')
            if abilChoice == 'ABORT' or abilChoice == None: return # If the player closed the window, or pressed Cancel, abort.
            TriggersFound.pop(abilChoice) # What we do now, is we remove the choice we made, from the list of possible choices. We remove it because then we will remove all the other options from the main list "Autoscripts"
            for unchosenOption in TriggersFound:
               if debugVerbosity >= 4: notify (' Removing unused option: {}'.format(unchosenOption)) # Debug
               Autoscripts.remove(unchosenOption)
            if debugVerbosity >= 2: notify ('Final Autoscripts after choices: {}'.format(Autoscripts)) # Debug
      if debugVerbosity >= 2: notify("#### List of autoscripts after scrubbing: {}".format(Autoscripts)) # Debug
      if len(Autoscripts) == 0 and debugVerbosity >= 2: notify("### No autoscripts remaining.") # Debug
      for autoS in Autoscripts:
         if debugVerbosity >= 2: notify("### First Processing: {}".format(autoS)) # Debug
         effectType = re.search(r'(on[A-Za-z]+|while[A-Za-z]+):', autoS)
         scriptHostCHK = re.search(r'(?<!-)onHost([A-Za-z]+)',effectType.group(1))
         actionHostCHK = re.search(r'HOST-([A-Z]+)',action)
         currObjID = getGlobalVariable('Engaged Objective')
         if currObjID != 'None':
            if re.search(r'-ifAttacker', autoS) and Card(num(currObjID)).owner != opponent: 
               if debugVerbosity >= 2: notify("### Rejected onAttack script for defender")
               continue
            if re.search(r'-ifDefender', autoS) and Card(num(currObjID)).owner != me: 
               if debugVerbosity >= 2: notify("### Rejected onDefense script for attacker")
               continue
         elif re.search(r'-ifAttacker', autoS) or re.search(r'-ifDefender', autoS): 
            if debugVerbosity >= 2: notify("### Rejected onAttack/Defense script outside of engagement")
            continue # If we're looking for attakcer or defender and we're not in an enagement, return.
         if debugVerbosity >= 2 and scriptHostCHK: notify ('### scriptHostCHK: {}'.format(scriptHostCHK.group(1))) # Debug
         if debugVerbosity >= 2 and actionHostCHK: notify ('### actionHostCHK: {}'.format(actionHostCHK.group(1))) # Debug
         if (scriptHostCHK or actionHostCHK) and not ((scriptHostCHK and actionHostCHK) and (scriptHostCHK.group(1).upper() == actionHostCHK.group(1))): continue # If this is a host card
         if ((effectType.group(1) == 'onPlay' and action != 'PLAY') or 
             (effectType.group(1) == 'whileInPlay' and action != 'PLAY' and action != 'LEAVING' and action != 'THWART') or # whieInPlay cards only trigger when played or discarded
             (effectType.group(1) == 'onResolveFate' and action != 'RESOLVEFATE') or
             (effectType.group(1) == 'onStrike' and action != 'STRIKE') or
             (effectType.group(1) == 'onDamage' and action != 'DAMAGE') or
             (effectType.group(1) == 'onDefense' and action != 'DEFENSE') or
             (effectType.group(1) == 'onAttack' and action != 'ATTACK') or
             (effectType.group(1) == 'onParticipation' and action != 'PARTICIPATION') or
             (effectType.group(1) == 'onLeaving' and action != 'LEAVING') or
             (effectType.group(1) == 'onCommit' and action != 'COMMIT') or
             (effectType.group(1) == 'onGenerate' and action != 'GENERATE') or
             (effectType.group(1) == 'onThwart' and action != 'THWART')):
            if debugVerbosity >= 2: notify("### Skipping autoS. Not triggered.\n#### EffectType: {}\n#### action = {}".format(effectType.group(1),action)) 
            continue 
         if re.search(r'-onlyDuringEngagement', autoS) and getGlobalVariable('Engaged Objective') == 'None': 
            continue # If this is an optional ability only for engagements, then we abort
         if re.search(r'-isOptional', autoS):
            if not confirm("This card has an optional ability you can activate at this point. Do you want to do so?"): 
               notify("{} opts not to activate {}'s optional ability".format(me,card))
               continue
            else: notify("{} activates {}'s optional ability".format(me,card))
         if re.search(r'-ifHaveForce', autoS) and not haveForce(): 
            if debugVerbosity >= 2: notify("### Rejected -ifHaveForce script")
            continue
         if re.search(r'-ifHaventForce', autoS) and haveForce(): 
            if debugVerbosity >= 2: notify("### Rejected -ifHaventForce script")
            continue         
         selectedAutoscripts = autoS.split('$$')
         if debugVerbosity >= 2: notify ('### selectedAutoscripts: {}'.format(selectedAutoscripts)) # Debug
         for activeAutoscript in selectedAutoscripts:
            if debugVerbosity >= 2: notify("### Second Processing: {}".format(activeAutoscript)) # Debug
            if chkWarn(card, activeAutoscript) == 'ABORT': return
            if chkPlayer(activeAutoscript, card.controller,False) == 0: continue
            if re.search(r':Pass\b', activeAutoscript): continue # Pass is a simple command of doing nothing ^_^
            effect = re.search(r'\b([A-Z][A-Za-z]+)([0-9]*)([A-Za-z& ]*)\b([^:]?[A-Za-z0-9_&{}\|: -]*)', activeAutoscript)
            if debugVerbosity >= 2: notify('### effects: {}'.format(effect.groups())) #Debug
            if effectType.group(1) == 'whileInPlay' or effectType.group(1) == 'whileScored':
               if effect.group(1) != 'Gain' and effect.group(1) != 'Lose': continue # The only things that whileInPlay affect in execute Automations is GainX scripts (for now).
               if action == 'LEAVING' or action == 'THWART': Removal = True
               else: Removal = False
            else: Removal = False
            targetC = findTarget(activeAutoscript,card = card)
            targetPL = ofwhom(activeAutoscript,card.controller) # So that we know to announce the right person the effect, affects.
            announceText = "{} uses {} to".format(targetPL,card)
            if debugVerbosity >= 3: notify("#### targetC: {}".format([c.name for c in targetC])) # Debug
            if effect.group(1) == 'Gain' or effect.group(1) == 'Lose':
               if Removal: 
                  if effect.group(1) == 'Gain': passedScript = "Lose{}{}".format(effect.group(2),effect.group(3))
                  elif effect.group(1) == 'SetTo': passedScript = "SetTo{}{}".format(effect.group(2),effect.group(3))
                  else: passedScript = "Gain{}{}".format(effect.group(2),effect.group(3))
               else: 
                  if effect.group(1) == 'Gain': passedScript = "Gain{}{}".format(effect.group(2),effect.group(3))
                  elif effect.group(1) == 'SetTo': passedScript = "SetTo{}{}".format(effect.group(2),effect.group(3))
                  else: passedScript = "Lose{}{}".format(effect.group(2),effect.group(3))
               if effect.group(4): passedScript += effect.group(4)
               if debugVerbosity >= 2: notify("### passedscript: {}".format(passedScript)) # Debug
               gainTuple = GainX(passedScript, announceText, card, targetC, notification = 'Quick', n = X, actionType = action)
               if gainTuple == 'ABORT': return
               X = gainTuple[1] 
            else: 
               passedScript = effect.group(0)
               if debugVerbosity >= 2: notify("### passedscript: {}".format(passedScript)) # Debug
               if regexHooks['CreateDummy'].search(passedScript): 
                  if debugVerbosity >= 2: notify("### in CreateDummy hook")
                  if CreateDummy(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
               elif regexHooks['DrawX'].search(passedScript): 
                  if debugVerbosity >= 2: notify("### in DrawX hook")
                  if DrawX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
               elif regexHooks['RetrieveX'].search(passedScript): 
                  if debugVerbosity >= 2: notify("### in RetrieveX hook")
                  if RetrieveX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
               elif regexHooks['TokensX'].search(passedScript): 
                  if debugVerbosity >= 2: notify("### in TokensX hook")
                  if TokensX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
               elif regexHooks['RollX'].search(passedScript): 
                  if debugVerbosity >= 2: notify("### in RollX hook")
                  rollTuple = RollX(passedScript, announceText, card, targetC, notification = 'Quick', n = X)
                  if rollTuple == 'ABORT': return
                  X = rollTuple[1] 
               elif regexHooks['RequestInt'].search(passedScript): 
                  if debugVerbosity >= 2: notify("### in RequestInt hook")
                  numberTuple = RequestInt(passedScript, announceText, card, targetC, notification = 'Quick', n = X)
                  if numberTuple == 'ABORT': return
                  X = numberTuple[1] 
               elif regexHooks['DiscardX'].search(passedScript): 
                  if debugVerbosity >= 2: notify("### in DiscardX hook")
                  discardTuple = DiscardX(passedScript, announceText, card, targetC, notification = 'Quick', n = X)
                  if discardTuple == 'ABORT': return
                  X = discardTuple[1] 
               elif regexHooks['ReshuffleX'].search(passedScript): 
                  if debugVerbosity >= 2: notify("### in ReshuffleX hook")
                  reshuffleTuple = ReshuffleX(passedScript, announceText, card, targetC, notification = 'Quick', n = X)
                  if reshuffleTuple == 'ABORT': return
                  X = reshuffleTuple[1]
               elif regexHooks['ShuffleX'].search(passedScript): 
                  if debugVerbosity >= 2: notify("### in ShuffleX hook")
                  if ShuffleX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
               elif regexHooks['ChooseKeyword'].search(passedScript): 
                  if debugVerbosity >= 2: notify("### in ChooseKeyword hook")
                  if ChooseKeyword(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
               elif regexHooks['ModifyStatus'].search(passedScript): 
                  if debugVerbosity >= 2: notify("### in ModifyStatus hook")
                  if ModifyStatus(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
               elif regexHooks['GameX'].search(passedScript): 
                  if debugVerbosity >= 2: notify("### in GameX hook")
                  if GameX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
               elif regexHooks['SimplyAnnounce'].search(passedScript): 
                  if debugVerbosity >= 2: notify("### in SimplyAnnounce hook")
                  if SimplyAnnounce(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
               elif debugVerbosity >= 2: notify("### No hooks found for autoscript")
            if failedRequirement: break # If one of the Autoscripts was a cost that couldn't be paid, stop everything else.
            if debugVerbosity >= 2: notify("Loop for scipt {} finished".format(passedScript))
   if debugVerbosity >= 2: notify("#### About to go check if I'm to go into executeAttachmentScripts()") # Debug
   if not re.search(r'HOST-',action): executeAttachmentScripts(card, action) # if the automation we're doing now is not for an attachment, then we check the current card's attachments for more scripts

#------------------------------------------------------------------------------
# Attached cards triggers
#------------------------------------------------------------------------------

def executeAttachmentScripts(card, action):
   if debugVerbosity >= 1: notify(">>> executeEnhancementScripts() with action: {}".format(action)) #Debug
   hostCards = eval(getGlobalVariable('Host Cards'))
   for attachment in hostCards:
      if hostCards[attachment] == card._id:
         executePlayScripts(Card(attachment), 'HOST-' + action)
   if debugVerbosity >= 3: notify("<<< executeEnhancementScripts()") # Debug

#------------------------------------------------------------------------------
# Card Use trigger
#------------------------------------------------------------------------------

def useAbility(card, x = 0, y = 0, paidAbility = False, manual = True): # The start of autoscript activation.
   if debugVerbosity >= 1: notify(">>> useAbility(){}".format(extraASDebug())) #Debug
   mute()
   global failedRequirement,selectedAbility
   AutoscriptsList = [] # An empty list which we'll put the AutoActions to execute.
   failedRequirement = False # We set it to false when we start a new autoscript.
   if debugVerbosity >= 4: notify("+++ Not a tracing card. Checking highlight...")
   if card.highlight == EdgeColor or card.highlight == UnpaidColor:
      whisper("You cannot use egde or unpaid card abilities. Aborting")
      return
   if debugVerbosity >= 4: notify("+++ Not an inactive card. Checking Stored_Autoactions{}...")
   if not Automations['Play']:
      whisper("Play automations have been disabled. Aborting!")
      return
   if debugVerbosity >= 4: notify("+++ Automations active. Checking for CustomScript...")
   if re.search(r'CustomScript', CardsAA.get(card.model,'')): 
      CustomScript(card,'USE') # Some cards just have a fairly unique effect and there's no use in trying to make them work in the generic framework.
      return
   Autoscripts = CardsAA.get(card.model,'').split('||')
   AutoScriptSnapshot = list(Autoscripts)
   for autoS in AutoScriptSnapshot: # Checking and removing any clickscripts which were put here in error.
      if ((re.search(r'onlyforDummy', autoS) and card.highlight != DummyColor)
         or (re.search(r'(CreateDummy|excludeDummy)', autoS) and card.highlight == DummyColor)): # Dummies in general don't create new dummies
         Autoscripts.remove(autoS)
   if debugVerbosity >= 2: notify("### Removed bad options")
   if len(Autoscripts) == 0:
      whisper("This card has no automated abilities. Aborting")
      return 
   if not paidAbility and not selectedAbility.has_key(card._id): # If the player has already paid the ability of this card, we skip all the checking and go straight to the autoscripts
      if debugVerbosity >= 2: notify("### Ability not paid.")
      if debugVerbosity >= 4: notify("+++ All checks done!. Starting Choice Parse...")
      ### Checking if card has multiple autoscript options and providing choice to player.
      if len(Autoscripts) > 1: 
         #abilConcat = "This card has multiple abilities.\nWhich one would you like to use?\
                   #\n\n(Tip: You can put multiple abilities one after the the other (e.g. '110'). Max 9 at once)\n\n" # We start a concat which we use in our confirm window.
         if Automations['WinForms']: ChoiceTXT = "This card has multiple abilities.\nSelect the ones you would like to use, in order, and press the [Finish Selection] button"
         else: ChoiceTXT = "This card has multiple abilities.\nType the ones you would like to use, in order, and press the [OK] button"
         choices = card.Instructions.split('||') # A card with multiple abilities on use MUST use the Instructions properties
         choice = SingleChoice(ChoiceTXT, choices, type = 'button', default = 0)
         if choice == 'ABORT': return
         selectedAutoscripts = Autoscripts[choice].split('$$')
         if debugVerbosity >= 2: notify("### AutoscriptsList: {}".format(AutoscriptsList)) # Debug
      else: 
         selectedAutoscripts = Autoscripts[0].split('$$')
         choice = 0 
      actionCost = re.match(r"R([0-9]+):", selectedAutoscripts[0]) # Any cost will always be at the start
      if actionCost and actionCost.group(1) != '0': # If the card has a cost to be paid...
         previousHighlight = card.highlight
         selectedAbility[card._id] = (choice,num(actionCost.group(1)),previousHighlight) # We set a tuple of variables tracking for which of the card's choices the payment is and how much the player must pay. The third entry in the tuple is the card's previous highlight if it had any.
         card.highlight = UnpaidAbilityColor # We put a special highlight on the card to allow resource generation to be assigned to it.
         notify("{} Attempts to use {}'s ability".format(me,card))
         return
   else: # If we're returning after paying a card's abilities cost, we re-set out selectedAutoscripts
      if manual: checkPaid = checkPaidResources(card) # If this is an attempt to manually pay for the card, we check that the player can afford it (e.g. it's zero cost or has cost reduction effects)
      else: checkPaid = 'USEOK' #If it's not manual, then it means the checkPaidResources() has been run successfully, so we proceed.
      if checkPaid == 'USEOK' or confirm(":::ERROR::: You do have not yet paid the cost of this card's abilities. Bypass?"):
         # if the card has been fully paid, we remove the resource markers and move it at its final position.
         choice = selectedAbility[card._id][0]
         card.highlight = selectedAbility[card._id][2]
         selectedAutoscripts = Autoscripts[choice].split('$$')
         del selectedAbility[card._id]
         for cMarkerKey in card.markers: 
            for resdictKey in resdict:
               if resdict[resdictKey] == cMarkerKey: 
                  card.markers[cMarkerKey] = 0
      else: return # If the ability is not ok  and the player does not confirm to continue, do nothing.
   if debugVerbosity >= 2: notify("### Executing Autoscripts: {}".format(selectedAutoscripts)) # Debug
   announceText = "{} activates {} in order to".format(me,card)
   X = 0 # Variable for special costs.
   if card.highlight == DummyColor: lingering = ' the lingering effect of' # A text that we append to point out when a player is using a lingering effect in the form of a dummy card.
   else: lingering = ''
   for activeAutoscript in selectedAutoscripts:
      #confirm("Active Autoscript: {}".format(activeAutoscript)) #Debug
      ### Checking if any of the card's effects requires one or more targets first
      if re.search(r'(?<!Auto)Targeted', activeAutoscript) and findTarget(activeAutoscript,card = card) == []: return
   for activeAutoscript in selectedAutoscripts:
      if not checkOriginatorRestrictions(activeAutoscript,card): continue # If the card does not fulfil it's requirements do not execute this script.
      if re.search(r'onlyOnce',activeAutoscript) and oncePerTurn(card, silent = True) == 'ABORT': continue
      if not announceText.endswith(' in order to') and not announceText.endswith(' and'): announceText += ' and'   
      targetC = findTarget(activeAutoscript,card = card)
      ### Warning the player in case we need to
      if chkWarn(card, activeAutoscript) == 'ABORT': return
      ### Check if the action needs the player or his opponent to be targeted
      targetPL = ofwhom(activeAutoscript)
      if debugVerbosity >= 2: notify("### Entering useAbility() Choice with Autoscript: {}".format(activeAutoscript)) # Debug
      if regexHooks['GainX'].search(activeAutoscript): 
         gainTuple = GainX(activeAutoscript, announceText, card, targetC, n = X)
         if gainTuple == 'ABORT': announceText == 'ABORT'
         else:
            announceText = gainTuple[0] 
            X = gainTuple[1] 
      elif regexHooks['CreateDummy'].search(activeAutoscript): announceText = CreateDummy(activeAutoscript, announceText, card, targetC, n = X)
      elif regexHooks['ReshuffleX'].search(activeAutoscript): 
         reshuffleTuple = ReshuffleX(activeAutoscript, announceText, card) # The reshuffleX() function is special because it returns a tuple.
         announceText = reshuffleTuple[0] # The first element of the tuple contains the announceText string
         X = reshuffleTuple[1] # The second element of the tuple contains the number of cards that were reshuffled from the hand in the deck.
      elif regexHooks['RollX'].search(activeAutoscript): 
         rollTuple = RollX(activeAutoscript, announceText, card) # Returns like reshuffleX()
         announceText = rollTuple[0] 
         X = rollTuple[1] 
      elif regexHooks['RequestInt'].search(activeAutoscript): 
         numberTuple = RequestInt(activeAutoscript, announceText, card) # Returns like reshuffleX()
         if numberTuple == 'ABORT': announceText == 'ABORT'
         else:
            announceText = numberTuple[0] 
            X = numberTuple[1] 
      elif regexHooks['DiscardX'].search(activeAutoscript): 
         discardTuple = DiscardX(activeAutoscript, announceText, card, targetC, n = X) # Returns like reshuffleX()
         announceText = discardTuple[0] 
         X = discardTuple[1] 
      elif regexHooks['TokensX'].search(activeAutoscript):           announceText = TokensX(activeAutoscript, announceText, card, targetC, n = X)
      elif regexHooks['DrawX'].search(activeAutoscript):             announceText = DrawX(activeAutoscript, announceText, card, targetC, n = X)
      elif regexHooks['RetrieveX'].search(activeAutoscript):         announceText = RetrieveX(activeAutoscript, announceText, card, targetC, n = X)
      elif regexHooks['ShuffleX'].search(activeAutoscript):          announceText = ShuffleX(activeAutoscript, announceText, card, targetC, n = X)
      elif regexHooks['ModifyStatus'].search(activeAutoscript):      announceText = ModifyStatus(activeAutoscript, announceText, card, targetC, n = X)
      elif regexHooks['SimplyAnnounce'].search(activeAutoscript):    announceText = SimplyAnnounce(activeAutoscript, announceText, card, targetC, n = X)
      elif regexHooks['ChooseKeyword'].search(activeAutoscript):     announceText = ChooseKeyword(activeAutoscript, announceText, card, targetC, n = X)
      elif regexHooks['UseCustomAbility'].search(activeAutoscript):  announceText = UseCustomAbility(activeAutoscript, announceText, card, targetC, n = X)
      if debugVerbosity >= 3: notify("<<< useAbility() choice. TXT = {}".format(announceText)) # Debug
      if announceText == 'ABORT': 
         whisper(":::ABORTING:::")
         return
      if failedRequirement: break # If part of an AutoAction could not pay the cost, we stop the rest of it.
   if announceText.endswith(' in order to'): # If our text annouce ends with " to", it means that nothing happened. Try to undo and inform player.
      notify("{}, but there was nothing to do.".format(announceText[:-len(' in order to')]))
   elif announceText.endswith(' and'):
      announceText = announceText[:-len(' and')] # If for some reason we end with " and" (say because the last action did nothing), we remove it.
   notify("{}.".format(announceText)) # Finally announce what the player just did by using the concatenated string.
      
#------------------------------------------------------------------------------
# Other Player trigger
#------------------------------------------------------------------------------
   
def autoscriptOtherPlayers(lookup, origin_card = Affiliation, count = 1): # Function that triggers effects based on the opponent's cards.
# This function is called from other functions in order to go through the table and see if other players have any cards which would be activated by it.
# For example a card that would produce credits whenever a trace was attempted. 
   if not Automations['Triggers']: return
   if debugVerbosity >= 1: notify(">>> autoscriptOtherPlayers() with lookup: {}".format(lookup)) #Debug
   if not Automations['Play']: return # If automations have been disabled, do nothing.
   for card in table:
      if debugVerbosity >= 2: notify('### Checking {}'.format(card)) # Debug
      if not card.isFaceUp: 
         if debugVerbosity >= 4: notify("### Card is not faceup") # Debug
         continue # Don't take into accounts cards that are face down for some reason. 
      if card.highlight == CapturedColor or card.highlight == EdgeColor or card.highlight == FateColor or card.highlight == UnpaidColor: 
         if debugVerbosity >= 4: notify("### Card is inactive") # Debug
         continue # We do not care about inactive cards.
      costText = '{} activates {} to'.format(card.controller, card) 
      Autoscripts = CardsAS.get(card.model,'').split('||')
      if debugVerbosity >= 4: notify("### {}'s AS: {}".format(card,Autoscripts)) # Debug
      autoScriptSnapshot = list(Autoscripts)
      for autoS in autoScriptSnapshot: # Checking and removing anything other than whileRezzed or whileScored.
         if not re.search(r'whileInPlay', autoS): Autoscripts.remove(autoS)
      if len(Autoscripts) == 0: continue
      for autoS in Autoscripts:
         if debugVerbosity >= 2: notify('### autoS: {}'.format(autoS)) # Debug
         cardTriggerRegex = re.search(r'-per([A-Za-z]+)', autoS) # This regex extracts the card's trigger keyword. So if a card says "put1Focus-perCardCaptured", it's trigger word is "CardCaptured".
         if not cardTriggerRegex: continue # If the card does not have a trigger word, it does not have an abilit that's autoscripted by other players.
         debugNotify("cardTriggerRegex Keyword {}".format(cardTriggerRegex.groups(1)))
         if not re.search(r'{}'.format(cardTriggerRegex.group(1)), lookup): # Now we look for the trigger keyword, in what kind of trigger is being checked in this instance.
                                                                            # So if our instance's trigger is currently "UnitCardCapturedFromTable" then the trigger word "CardCaptured" is contained within and will match.
            debugNotify("Couldn't lookup the trigger: {} in autoscript. Ignoring".format(lookup),2)
            continue # Search if in the script of the card, the string that was sent to us exists. The sent string is decided by the function calling us, so for example the ProdX() function knows it only needs to send the 'GeneratedSpice' string.
         if chkPlayer(autoS, card.controller,False) == 0: continue # Check that the effect's origninator is valid.
         currObjID = getGlobalVariable('Engaged Objective')
         if currObjID != 'None':
            if re.search(r'-ifAttacker', autoS) and Card(num(currObjID)).controller == card.controller: 
               if debugVerbosity >= 2: notify("### Rejected onAttack script for defender")
               continue
            if re.search(r'-ifDefender', autoS) and Card(num(currObjID)).controller != card.controller: 
               if debugVerbosity >= 2: notify("### Rejected onDefense script for attacker")
               continue
         elif re.search(r'-ifAttacker', autoS) or re.search(r'-ifDefender', autoS): 
            if debugVerbosity >= 2: notify("### Rejected onAttack/Defense script outside of engagement")
            continue # If we're looking for attakcer or defender and we're not in an enagement, return.
         if re.search(r'-ifEngagementTarget', autoS): # If we have this modulator, then this script is only meant to fire if the card checked it the currently engaged objective 
            if re.search(r'-ifEngagementTargetHost', autoS): # This submodulator fires only if the card being checked for scripts is currently hosted on the engaged objective.
               hostCards = eval(getGlobalVariable('Host Cards')) 
               if Card(num(currObjID)) != Card(hostCards[card._id]): continue
            elif Card(num(currObjID)) != card: continue
         if re.search(r'-ifHaveForce', autoS) and not haveForce(): continue
         if re.search(r'-ifHaventForce', autoS) and haveForce(): continue
         if re.search(r'-ifParticipating', autoS) and card.orientation != Rot90: continue
         if re.search(r'-ifCapturingObjective', autoS) and capturingObjective != card: continue  # If the card required itself to be the capturing objective, we check it here via a global variable.             
         confirmText = re.search(r'ifConfirm{(A-Za-z0-9)+}', autoS) # If the card contains the modified "ifConfirm{some text}" then we present "some text" as a question before proceeding.
                                                                    # This is different from -isOptional in order to be able to trigger abilities we cannot automate otherwise.
         if confirmText and not confirm(confirmText.group(1)): continue
         if not chkDummy(autoS, card): continue
         if not checkCardRestrictions(gatherCardProperties(origin_card), prepareRestrictions(autoS,'type')): continue #If we have the '-type' modulator in the script, then need ot check what type of property it's looking for
         elif debugVerbosity >= 2: notify("### Not Looking for specific type or type specified found.")
         if re.search(r'onlyOnce',autoS) and oncePerTurn(card, silent = True, act = 'automatic') == 'ABORT': continue # If the card's ability is only once per turn, use it or silently abort if it's already been used
         if re.search(r'onTriggerCard',autoS): targetCard = [origin_card] # if we have the "-onTriggerCard" modulator, then the target of the script will be the original card (e.g. see Grimoire)
         else: targetCard = findTarget(autoS, card = card)
         if debugVerbosity >= 2: notify("### Automatic Autoscripts: {}".format(autoS)) # Debug
         #effect = re.search(r'\b([A-Z][A-Za-z]+)([0-9]*)([A-Za-z& ]*)\b([^:]?[A-Za-z0-9_&{} -]*)', autoS)
         #passedScript = "{}".format(effect.group(0))
         #confirm('effects: {}'.format(passedScript)) #Debug
         if regexHooks['GainX'].search(autoS):
            gainTuple = GainX(autoS, costText, card, targetCard, notification = 'Automatic', n = count)
            if gainTuple == 'ABORT': break
         elif regexHooks['TokensX'].search(autoS): 
            if TokensX(autoS, costText, card, targetCard, notification = 'Automatic', n = count) == 'ABORT': break
         elif regexHooks['DrawX'].search(autoS):
            if DrawX(autoS, costText, card, targetCard, notification = 'Automatic', n = count) == 'ABORT': break
         elif regexHooks['ModifyStatus'].search(autoS): 
            if debugVerbosity >= 2: notify("### in ModifyStatus hook")
            if ModifyStatus(autoS, costText, card, targetCard, notification = 'Automatic', n = count) == 'ABORT': break
         elif regexHooks['UseCustomAbility'].search(autoS):
            if UseCustomAbility(autoS, costText, card, targetCard, notification = 'Automatic', n = count) == 'ABORT': break
   if debugVerbosity >= 3: notify("<<< autoscriptOtherPlayers()") # Debug

#------------------------------------------------------------------------------
# Start/End of Turn/Phase trigger
#------------------------------------------------------------------------------
   
def atTimedEffects(Time = 'Start'): # Function which triggers card effects at the start or end of the turn.
   mute()
   if debugVerbosity >= 1: notify(">>> atTimedEffects() at time: {}".format(Time)) #Debug
   if not Automations['Start/End-of-Turn/Phase']: return
   TitleDone = False
   X = 0
   for card in table:
      if debugVerbosity >= 4: notify("### Checking card: {}".format(card))
      if card.highlight == CapturedColor or card.highlight == EdgeColor or card.highlight == UnpaidColor: 
         if debugVerbosity >= 3: notify("### Card inactive. Ignoring")
         continue # We do not care about inactive cards.
      if not card.isFaceUp: 
         if debugVerbosity >= 3: notify("### Card is face down. Ignoring")
         continue
      Autoscripts = CardsAS.get(card.model,'').split('||')
      for autoS in Autoscripts:
         if debugVerbosity >= 2: notify("### Processing {} Autoscript: {}".format(card, autoS))
         if re.search(r'after([A-za-z]+)',Time): effect = re.search(r'(after[A-za-z]+):(.*)', autoS) # Putting Run in a group, only to retain the search results groupings later
         else: effect = re.search(r'atTurn(Start|End):(.*)', autoS) #Putting "Start" or "End" in a group to compare with the Time variable later
         if not effect: continue
         if debugVerbosity >= 3: notify("### Time maches. Script triggers on: {}".format(effect.group(1)))
         if chkPlayer(effect.group(2), card.controller,False) == 0: continue # Check that the effect's origninator is valid. 
         if effect.group(1) != Time: continue # If the effect trigger we're checking (e.g. start-of-run) does not match the period trigger we're in (e.g. end-of-turn)
         if debugVerbosity >= 2 and effect: notify("!!! effects: {}".format(effect.groups()))
         if not chkDummy(autoS, card): continue
         if re.search(r'-ifHaveForce', autoS) and not haveForce(): continue
         if re.search(r'-ifHaventForce', autoS) and haveForce(): continue         
         if re.search(r'isOptional', effect.group(2)):
            if debugVerbosity >= 2: notify("### Checking Optional Effect")
            extraCountersTXT = '' 
            for cmarker in card.markers: # If the card has any markers, we mention them do that the player can better decide which one they wanted to use (e.g. multiple bank jobs)
               extraCountersTXT += " {}x {}\n".format(card.markers[cmarker],cmarker[0])
            if extraCountersTXT != '': extraCountersTXT = "\n\nThis card has the following counters on it\n" + extraCountersTXT
            if not confirm("{} can have its optional ability take effect at this point. Do you want to activate it?{}".format(fetchProperty(card, 'name'),extraCountersTXT)): continue         
         if re.search(r'onlyOnce',autoS) and oncePerTurn(card, silent = True, act = 'automatic') == 'ABORT': continue
         splitAutoscripts = effect.group(2).split('$$')
         for passedScript in splitAutoscripts:
            if debugVerbosity >= 2: notify("### passedScript: {}".format(passedScript))
            targetC = findTarget(passedScript, card = card)
            if not TitleDone and not (len(targetC) == 0 and re.search(r'AutoTargeted',passedScript)): # We don't want to put a title if we have a card effect that activates only if we have some valid targets (e.g. Admiral Motti)
               if re.search(r'after([A-za-z]+)',Time): 
                  Phase = re.search(r'after([A-za-z]+)',Time)
                  title = "{}'s Post-{} Effects".format(me,Phase.group(1))
               else: title = "{}'s {}-of-Turn Effects".format(me,effect.group(1))
               notify("{:=^36}".format(title))
               TitleDone = True
            if debugVerbosity >= 2: notify("### passedScript: {}".format(passedScript))
            targetPL = ofwhom(passedScript,card.controller) # So that we know to announce the right person the effect, affects.
            if card.highlight == DummyColor: announceText = "{}'s lingering effects:".format(card)
            else: announceText = "{} uses {} to".format(targetPL,card)
            if regexHooks['GainX'].search(passedScript):
               gainTuple = GainX(passedScript, announceText, card, targetC, notification = 'Automatic', n = X)
               if gainTuple == 'ABORT': break
               X = gainTuple[1] 
            elif regexHooks['DrawX'].search(passedScript):
               if debugVerbosity >= 2: notify("### About to DrawX()")
               if DrawX(passedScript, announceText, card, targetC, notification = 'Automatic', n = X) == 'ABORT': break
            elif regexHooks['RetrieveX'].search(passedScript):
               if debugVerbosity >= 2: notify("### About to RetrieveX()")
               if RetrieveX(passedScript, announceText, card, targetC, notification = 'Automatic', n = X) == 'ABORT': break
            elif regexHooks['RollX'].search(passedScript):
               rollTuple = RollX(passedScript, announceText, card, targetC, notification = 'Automatic', n = X)
               if rollTuple == 'ABORT': break
               X = rollTuple[1] 
            elif regexHooks['TokensX'].search(passedScript):
               if TokensX(passedScript, announceText, card, targetC, notification = 'Automatic', n = X) == 'ABORT': break
            elif regexHooks['ModifyStatus'].search(passedScript):
               if ModifyStatus(passedScript, announceText, card, targetC, notification = 'Automatic', n = X) == 'ABORT': break
            elif regexHooks['DiscardX'].search(passedScript): 
               discardTuple = DiscardX(passedScript, announceText, card, targetC, notification = 'Automatic', n = X)
               if discardTuple == 'ABORT': break
               X = discardTuple[1] 
            elif regexHooks['RequestInt'].search(passedScript): 
               numberTuple = RequestInt(passedScript, announceText, card, targetC) # Returns like reshuffleX()
               if numberTuple == 'ABORT': break
               X = numberTuple[1] 
            elif regexHooks['SimplyAnnounce'].search(passedScript): 
               if SimplyAnnounce(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            elif regexHooks['CustomScript'].search(passedScript):
               if CustomScript(card, action = Time) == 'ABORT': break
            if failedRequirement: break # If one of the Autoscripts was a cost that couldn't be paid, stop everything else.
   markerEffects(Time) 
   if TitleDone: notify(":::{:=^30}:::".format('='))   
   if debugVerbosity >= 3: notify("<<< atTimedEffects()") # Debug

def markerEffects(Time = 'Start'):
   if debugVerbosity >= 1: notify(">>> markerEffects() at time: {}".format(Time)) #Debug
   cardList = [c for c in table if c.markers]
   for card in cardList:
      for marker in card.markers:
         if (Time == 'afterEngagement'
               and (re.search(r'Death from Above',marker[0])
                 or re.search(r'Vaders TIE Advance',marker[0])
                 or re.search(r'Yoda enhancements',marker[0])
                 or re.search(r'Cocky',marker[0])
                 or re.search(r'Heavy Fire',marker[0])
                 or re.search(r'Ewok Scouted',marker[0]))):
            TokensX('Remove999'+marker[0], marker[0] + ':', card)
            notify("--> {} removes {} effect from {}".format(me,marker[0],card))
         if (Time == 'End' # Time = 'End' means End of Turn
               and (re.search(r'Defense Upgrade',marker[0])
                 or re.search(r'Force Stasis',marker[0]))):
            TokensX('Remove999'+marker[0], marker[0] + ':', card)
            notify("--> {} removes {} effect from {}".format(me,marker[0],card))
         if ((       Time == 'afterBalance' # These are "after-phase" effects
                  or Time == 'afterRefresh'
                  or Time == 'afterDraw'
                  or Time == 'afterDeployment'
                  or Time == 'afterConflict'
                  or Time == 'End')
               and (re.search(r'Munitions Expert',marker[0])
                or re.search(r'Echo Caverns',marker[0])
                or re.search(r'Ion Damaged',marker[0])
                or re.search(r'Unwavering Resolve',marker[0])
                or re.search(r'Shelter from the Storm',marker[0]))):
            TokensX('Remove999'+marker[0], marker[0] + ':', card)
            notify("--> {} removes {} effect from {}".format(me,marker[0],card))

   
   
#------------------------------------------------------------------------------
# Core Commands
#------------------------------------------------------------------------------
   
def GainX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0, actionType = 'USE'): # Core Command for modifying counters or global variables
   if debugVerbosity >= 1: notify(">>> GainX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   gain = 0
   extraTXT = ''
   action = re.search(r'\b(Gain|Lose|SetTo)([0-9]+)([A-Z][A-Za-z &]+)-?', Autoscript)
   if debugVerbosity >= 2: notify("### action groups: {}. Autoscript: {}".format(action.groups(0),Autoscript)) # Debug
   gain += num(action.group(2))
   targetPL = ofwhom(Autoscript, card.controller)
   if targetPL != me and not notification: otherTXT = ' force {} to'.format(targetPL)
   else: otherTXT = ''
   multiplier = per(Autoscript, card, n, targetCards) # We check if the card provides a gain based on something else, such as favour bought, or number of dune fiefs controlled by rivals.
   if action.group(1) == 'Lose': gain *= -1 
   if debugVerbosity >= 3: notify("### GainX() after per") #Debug
   gainReduce = findCounterPrevention(gain * multiplier, action.group(3), targetPL) # If we're going to gain counter, then we check to see if we have any markers which might reduce the cost.
   #confirm("multiplier: {}, gain: {}, reduction: {}".format(multiplier, gain, gainReduce)) # Debug
   if re.match(r'Reserves', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.counters['Reserves'].value = 0 # If we're setting to a specific value, we wipe what it's currently.
      targetPL.counters['Reserves'].value += gain * multiplier
      if targetPL.counters['Reserves'].value < 0: targetPL.counters['Reserves'].value = 0
   elif re.match(r'Dial', action.group(3)):
      modifyDial(gain * multiplier)
   else: 
      whisper("Gain what?! (Bad autoscript)")
      return 'ABORT'
   if debugVerbosity >= 2: notify("### Gainx() Finished counter manipulation")
   if action.group(1) == 'Gain': # Since the verb is in the middle of the sentence, we want it lowercase. 
      if action.group(3) == 'Dial': verb = 'increase'
      else: verb = 'gain'
   elif action.group(1) == 'Lose': 
      if action.group(3) == 'Dial': verb = 'decrease'
      elif re.search(r'isCost', Autoscript): verb = 'pay'
      else: verb = 'lose'
   else: verb = 'set to'
   if debugVerbosity >= 2: notify("### Gainx() Finished preparing verb ({}). Notification was: {}".format(verb,notification))
   if abs(gain) == abs(999): total = 'all' # If we have +/-999 as the count, then this mean "all" of the particular counter.
   else: total = abs(gain * multiplier) # Else it's just the absolute value which we announce they "gain" or "lose"
   if action.group(3) == 'Dial': closureTXT = "the Death Star Dial by {}".format(total)
   else: closureTXT = "{} {}".format(total, action.group(3))
   if debugVerbosity >= 2: notify("### Gainx() about to announce")
   if notification == 'Quick': announceString = "{}{} {} {}{}".format(announceText, otherTXT, verb, closureTXT,extraTXT)
   else: announceString = "{}{} {} {}{}".format(announceText, otherTXT, verb, closureTXT,extraTXT)
   if notification and multiplier > 0: notify(':> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< Gain() total: {}".format(total))
   return (announceString,total)
   
def TokensX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for adding tokens to cards
   if debugVerbosity >= 1: notify(">>> TokensX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   if re.search(r'atHost', Autoscript):
      hostCards = eval(getGlobalVariable('Host Cards'))
      for attachment in hostCards: # We check out attachments dictionary to find out who this card's host is.
         if attachment == card._id: targetCards.append(Card(hostCards[attachment]))
   if len(targetCards) == 0:
      if re.search(r'AutoTargeted',Autoscript): 
         if re.search(r'isCost', Autoscript): return 'ABORT' # If removing a token is an actual cost, then we abort the rest of the script
         else: return announceText # Otherwise we continue with the rest of the script if we only need an automatic target but have no valid one
      else: #Otherwise we just put it on ourself and assume the player forgot to target first. They can move the marker manually if they need to.
         targetCards.append(card) # If there's been to target card given, assume the target is the card itself.
         targetCardlist = ' on it' 
   else:
      targetCardlist = ' on' # A text field holding which cards are going to get tokens.
      for targetCard in targetCards:
         targetCardlist += ' {},'.format(targetCard)
   foundKey = False # We use this to see if the marker used in the AutoAction is already defined.
   infectTXT = '' # We only inject this into the announcement when this is an infect AutoAction.
   preventTXT = '' # Again for virus infections, to note down how much was prevented.
   action = re.search(r'\b(Put|Remove|Refill|Use|Infect|Deal)([0-9]+)([A-Za-z: ]+)-?', Autoscript)
   if action.group(3) in mdict: token = mdict[action.group(3)]
   elif action.group(3) == "AnyTokenType": pass # If the removed token can be of any type, 
                                           # then we need to check which standard tokens the card has and provide the choice for one
                                           # We will do this one we start checking the target cards one-by-one.
   else: # If the marker we're looking for it not defined, then either create a new one with a random color, or look for a token with the custom name we used above.
      if action.group(1) == 'Infect': 
         victim = ofwhom(Autoscript, card.controller)
         if targetCards[0] == card: targetCards[0] = getSpecial('Affiliation',victim)
      if targetCards[0].markers:
         for key in targetCards[0].markers:
            if key[0] == action.group(3):
               foundKey = True
               token = key
      if not foundKey: # If no key is found with the name we seek, then create a new one with a random colour.
         #counterIcon = re.search(r'-counterIcon{([A-Za-z]+)}', Autoscript) # Not possible at the moment
         #if counterIcon and counterIcon.group(1) == 'plusOne':             # See https://github.com/kellyelton/OCTGN/issues/446
         #   token = ("{}".format(action.group(3)),"aa261722-e12a-41d4-a475-3cc1043166a7")         
         #else:
         rndGUID = rnd(1,8)
         token = ("{}".format(action.group(3)),"00000000-0000-0000-0000-00000000000{}".format(rndGUID)) #This GUID is one of the builtin ones
   count = num(action.group(2))
   multiplier = per(Autoscript, card, n, targetCards, notification)
   for targetCard in targetCards:
      if action.group(3) == "AnyTokenType": # If we need to find which token to remove, we have to do it once we know which cards we're checking.
         markerChoices = []
         if action.group(1) == 'Remove':
            if targetCard.markers[mdict['Shield']]: markerChoices.append("Shield")
            if targetCard.markers[mdict['Focus']]: markerChoices.append("Focus")
            if targetCard.markers[mdict['Damage']]: markerChoices.append("Damage")
         else: markerChoices = ["Shield","Focus","Damage"] # If we're adding any type of token, then we always provide a full choice list.
         if len(markerChoices) == 1: 
            token = mdict[markerChoices[0]]
         else:
            tokenChoice = SingleChoice("Choose one token to {} from {}.".format(action.group(1),targetCard.name), markerChoices, type = 'button', default = 0)
            if tokenChoice == 'ABORT': return 'ABORT'
            token = mdict[markerChoices[tokenChoice]]
         del markerChoices[:] # We clear the list for the next loop.
      if action.group(1) == 'Put':
         if re.search(r'isCost', Autoscript) and targetCard.markers[token] and targetCard.markers[token] > 0:
            whisper(":::ERROR::: This card already has a {} marker on it".format(token[0]))
            return 'ABORT'
         else: modtokens = count * multiplier
      elif action.group(1) == 'Deal': modtokens = count * multiplier
      elif action.group(1) == 'Refill': modtokens = count - targetCard.markers[token]
      elif action.group(1) == 'Infect':
         targetCardlist = '' #We don't want to mention the target card for infections. It's always the same.
         victim = ofwhom(Autoscript, card.controller)
         if targetCard == card: targetCard = getSpecial('Affiliation',victim) # For infecting targets, the target is never the card causing the effect.
         modtokens = count * multiplier
         infectTXT = ' {} with'.format(victim)
      elif action.group(1) == 'USE':
         if not targetCard.markers[token] or count > targetCard.markers[token]: 
            whisper("There's not enough counters left on the card to use this ability!")
            return 'ABORT'
         else: modtokens = -count * multiplier
      else: #Last option is for removing tokens.
         debugNotify("About to remove tokens",3)
         if count == 999: # 999 effectively means "all markers on card"
            if targetCard.markers[token]: count = targetCard.markers[token]
            else: 
               if not re.search(r'isSilent', Autoscript): whisper("There was nothing to remove.")
               count = 0
         elif re.search(r'isCost', Autoscript) and (not targetCard.markers[token] or (targetCard.markers[token] and count > targetCard.markers[token])):
            if notification != 'Automatic': whisper ("No enough markers to remove. Aborting!") #Some end of turn effect put a special counter and then remove it so that they only run for one turn. This avoids us announcing that it doesn't have markers every turn.
            debugNotify("Not enough markers to remove as cost. Aborting",2)
            return 'ABORT'
         elif not targetCard.markers[token]:
            if not re.search(r'isSilent', Autoscript): whisper("There was nothing to remove.")
            debugNotify("Found no {} tokens to remove".format(token[0]),2)
            count = 0 # If we don't have any markers, we have obviously nothing to remove.
         modtokens = -count * multiplier
      targetCard.markers[token] += modtokens # Finally we apply the marker modification
   if abs(num(action.group(2))) == abs(999): total = 'all'
   else: total = abs(modtokens)
   if re.search(r'isPriority', Autoscript): card.highlight = PriorityColor
   if action.group(1) == 'Deal': countersTXT = '' # If we "deal damage" we do not want to be writing "deals 1 damage counters"
   else: countersTXT = 'counters'
   announceString = "{} {}{} {} {} {}{}{}".format(announceText, action.group(1).lower(),infectTXT, total, token[0],countersTXT,targetCardlist,preventTXT)
   if notification and modtokens != 0 and not re.search(r'isSilent', Autoscript): notify(':> {}.'.format(announceString))
   if debugVerbosity >= 2: notify("### TokensX() String: {}".format(announceString)) #Debug
   if debugVerbosity >= 3: notify("<<< TokensX()")
   if re.search(r'isSilent', Autoscript): return announceText # If it's a silent marker, we don't want to announce anything. Returning the original announceText will be processed by any receiving function as having done nothing.
   else: return announceString
 
def DrawX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> DrawX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   destiVerb = 'draw'
   action = re.search(r'\bDraw([0-9]+)Card', Autoscript)
   targetPL = ofwhom(Autoscript, card.controller)
   if debugVerbosity >= 3: notify("### Setting Source")
   if targetPL != me: destiVerb = 'move'
   if re.search(r'-fromDiscard', Autoscript):
      source = targetPL.piles['Discard Pile']
      sourcePath =  " from their Discard Pile"
   else: 
      source = targetPL.piles['Command Deck']
      sourcePath =  ""
   if debugVerbosity >= 3: notify("### Setting Destination")
   if re.search(r'-toDeck', Autoscript): 
      destination = targetPL.piles['Command Deck']
      destiVerb = 'move'
   elif re.search(r'-toDiscard', Autoscript):
      destination = targetPL.piles['Discard Pile']
      destiVerb = 'discard'   
   else: destination = targetPL.hand
   if debugVerbosity >= 3: notify("### Setting Destination")
   if destiVerb == 'draw' and ModifyDraw > 0 and not confirm("You have a card effect in play that modifies the amount of cards you draw. Do you want to continue as normal anyway?\n\n(Answering 'No' will abort this action so that you can prepare for the special changes that happen to your draw."): return 'ABORT'
   draw = num(action.group(1))
   if draw == 999:
      multiplier = 1
      if currentHandSize(targetPL) >= len(targetPL.hand): # Otherwise drawMany() is going to try and draw "-1" cards which somehow draws our whole deck except one card.
         count = drawMany(source, currentHandSize(targetPL) - len(targetPL.hand), destination, True) # 999 means we refresh our hand
      else: count = 0 
      #confirm("cards drawn: {}".format(count)) # Debug
   else: # Any other number just draws as many cards.
      multiplier = per(Autoscript, card, n, targetCards, notification)
      count = drawMany(source, draw * multiplier, destination, True)
   if targetPL == me:
      if destiVerb != 'discard': destPath = " to their {}".format(destination.name)
      else: destPath = ''
   else: 
      if destiVerb != 'discard': destPath = " to {}'s {}".format(targetPL,destination.name)
      else: destPath = ''
   if debugVerbosity >= 2: notify("### About to announce.")
   if count == 0: return announceText # If there are no cards, then we effectively did nothing, so we don't change the notification.
   if notification == 'Quick': announceString = "{} draw {} cards{}".format(announceText, count,sourcePath)
   elif targetPL == me: announceString = "{} {} {} cards{}{}".format(announceText, destiVerb, count, sourcePath, destPath)
   elif source == targetPL.piles['Command Deck'] and destination == targetPL.hand: announceString = "{} {} draws {} cards.".format(announceText, targetPL, count)
   else: announceString = "{} {} {} cards from {}'s {}".format(announceText, destiVerb, count, targetPL, source.name, destPath)
   if notification and multiplier > 0: notify(':> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< DrawX()")
   return announceString

def DiscardX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> DiscardX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bDiscard([0-9]+)Card', Autoscript)
   targetPL = ofwhom(Autoscript, card.controller)
   if targetPL != me: otherTXT = ' force {} to'.format(targetPL)
   else: otherTXT = ''
   discardNR = num(action.group(1))
   if discardNR == 999:
      multiplier = 1
      discardNR = len(targetPL.hand) # 999 means we discard our whole hand
   else: # Any other number just discard as many cards at random.
      multiplier = per(Autoscript, card, n, targetCards, notification)
      count = handRandomDiscard(targetPL.hand, discardNR * multiplier, targetPL, silent = True)
      if re.search(r'isCost', Autoscript) and count < discardNR:
         whisper("You do not have enough cards in your hand to discard")
         return ('ABORT',0)
   if count == 0: return (announceText,count) # If there are no cards, then we effectively did nothing, so we don't change the notification.
   if notification == 'Quick': announceString = "{} discards {} cards".format(announceText, count)
   else: announceString = "{}{} discard {} cards from their hand".format(announceText,otherTXT, count)
   if notification and multiplier > 0: notify(':> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< DiscardX()")
   return (announceString,count)
         
def ReshuffleX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # A Core Command for reshuffling a pile into the R&D/Stack
   if debugVerbosity >= 1: notify(">>> ReshuffleX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   mute()
   X = 0
   targetPL = ofwhom(Autoscript, card.controller)
   action = re.search(r'\bReshuffle([A-Za-z& ]+)', Autoscript)
   if debugVerbosity >= 1: notify("!!! regex: {}".format(action.groups())) # Debug
   if action.group(1) == 'Hand':
      namestuple = groupToDeck(targetPL.hand, targetPL , True) # We do a silent hand reshuffle into the deck, which returns a tuple
      X = namestuple[2] # The 3rd part of the tuple is how many cards were in our hand before it got shuffled.
   elif action.group(1) == 'Discard': namestuple = groupToDeck(targetPL.piles['Discard Pile'], targetPL, True)    
   else: 
      whisper("Wat Group? [Error in autoscript!]")
      return 'ABORT'
   shuffle(targetPL.piles['Command Deck'])
   if notification == 'Quick': announceString = "{} shuffles their {} into their {}".format(announceText, namestuple[0], namestuple[1])
   else: announceString = "{} shuffle their {} into their {}".format(announceText, namestuple[0], namestuple[1])
   if notification: notify(':> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< ReshuffleX() return with X = {}".format(X))
   return (announceString, X)

def ShuffleX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # A Core Command for reshuffling a pile into the R&D/Stack
   if debugVerbosity >= 1: notify(">>> ShuffleX(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   mute()
   action = re.search(r'\bShuffle([A-Za-z& ]+)', Autoscript)
   targetPL = ofwhom(Autoscript, card.controller)
   if action.group(1) == 'Discard': pile = targetPL.piles['Discard Pile']
   elif action.group(1) == 'Deck': pile = targetPL.piles['Command Deck']
   elif action.group(1) == 'Objectives': pile = targetPL.piles['Objective Deck']
   random = rnd(10,100) # Small wait (bug workaround) to make sure all animations are done.
   shuffle(pile)
   if notification == 'Quick': announceString = "{} shuffles their {}".format(announceText, pile.name)
   elif targetPL == me: announceString = "{} shuffle their {}".format(announceText, pile.name)
   else: announceString = "{} shuffle {}' {}".format(announceText, targetPL, pile.name)
   if notification: notify(':> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< ShuffleX()")
   return announceString
   
def RollX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> RollX(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   d6 = 0
   d6list = []
   result = 0
   action = re.search(r'\bRoll([0-9]+)Dice(-chk)?([1-6])?', Autoscript)
   multiplier = per(Autoscript, card, n, targetCards, notification)
   count = num(action.group(1)) * multiplier 
   for d in range(count):
      if d == 2: whisper("-- Please wait. Rolling {} dice...".format(count))
      if d == 8: whisper("-- A little while longer...")
      d6 = rolld6(silent = True)
      d6list.append(d6)
      if action.group(3): # If we have a chk modulator, it means we only increase our total if we hit a specific number.
         if num(action.group(3)) == d6: result += 1
      else: result += d6 # Otherwise we add all totals together.
      if debugVerbosity >= 2: notify("### iter:{} with roll {} and total result: {}".format(d,d6,result))
   if notification == 'Quick': announceString = "{} rolls {} on {} dice".format(announceText, d6list, count)
   else: announceString = "{} roll {} dice with the following results: {}".format(announceText,count, d6list)
   if notification: notify(':> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< RollX() with result: {}".format(result))
   return (announceString, result)

def RequestInt(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> RequestInt(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bRequestInt(-Min)?([0-9]*)(-div)?([0-9]*)(-Max)?([0-9]*)(-Msg)?\{?([A-Za-z0-9?$& ]*)\}?', Autoscript)
   if debugVerbosity >= 2:
      if action: notify('!!! regex: {}'.format(action.groups()))
      else: notify("!!! No regex match :(")
   if debugVerbosity >= 2: notify("### Checking for Min")
   if action.group(2): 
      min = num(action.group(2))
      minTXT = ' (minimum {})'.format(min)
   else: 
      min = 0
      minTXT = ''
   if debugVerbosity >= 2: notify("### Checking for Max")
   if action.group(6): 
      max = num(action.group(6))
      minTXT += ' (maximum {})'.format(max)
   else: 
      max = None
   if debugVerbosity >= 2: notify("### Checking for div")
   if action.group(4): 
      div = num(action.group(4))
      minTXT += ' (must be a multiple of {})'.format(div)
   else: div = 1
   if debugVerbosity >= 2: notify("### Checking for Msg")
   if action.group(8): 
      message = action.group(8)
   else: message = "{}:\nThis effect requires that you provide an 'X'. What should that number be?{}".format(fetchProperty(card, 'name'),minTXT)
   number = min - 1
   if debugVerbosity >= 2: notify("### About to ask")
   while number < min or number % div or (max and number > max):
      number = askInteger(message,min)
      if number == None: 
         whisper("Aborting Function")
         return 'ABORT'
   if debugVerbosity >= 3: notify("<<< RequestInt()")
   return (announceText, number) # We do not modify the announcement with this function.
   
def SimplyAnnounce(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> SimplyAnnounce(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bSimplyAnnounce{([A-Za-z0-9&,\. ]+)}', Autoscript)
   if debugVerbosity >= 2: #Debug
      if action: notify("!!! regex: {}".format(action.groups())) 
      else: notify("!!! regex failed :(") 
   if re.search(r'break',Autoscript) and re.search(r'subroutine',Autoscript): penaltyNoisy(card)
   if notification == 'Quick': announceString = "{} {}".format(announceText, action.group(1))
   else: announceString = "{} {}".format(announceText, action.group(1))
   if notification: notify(':> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< SimplyAnnounce()")
   return announceString

def CreateDummy(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for creating dummy cards.
   if debugVerbosity >= 1: notify(">>> CreateDummy(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   global Dummywarn
   dummyCard = None
   action = re.search(r'\bCreateDummy[A-Za-z0-9_ -]*(-with)(?!onOpponent|-doNotDiscard|-nonUnique)([A-Za-z0-9_ -]*)', Autoscript)
   # We only want this regex to be true if the dummycard is going to have tokens put on it automatically.
   if action and debugVerbosity >= 3: notify('### Regex: {}'.format(action.groups())) # debug
   elif debugVerbosity >= 3: notify('### No regex match! Aborting') # debug
   targetPL = ofwhom(Autoscript, card.controller)
   for c in table:
      if c.model == card.model and c.controller == targetPL and c.highlight == DummyColor: dummyCard = c # We check if already have a dummy of the same type on the table.
   if debugVerbosity >= 2: notify('### Checking to see what our dummy card is') # debug
   if not dummyCard or re.search(r'nonUnique',Autoscript): #Some create dummy effects allow for creating multiple copies of the same card model.
      if debugVerbosity >= 2: notify('### Dummywarn = {}'.format(Dummywarn)) # debug .
      if debugVerbosity >= 2: notify('### no dummyCard exists') # debug . Dummywarn = {}'.format(Dummywarn)
      if Dummywarn and re.search('onOpponent',Autoscript):
         if not confirm("This action creates an effect for your opponent and a way for them to remove it.\
                       \nFor this reason we've created a dummy card on the table and marked it with a special highlight so that you know that it's just a token.\
                     \n\nYou opponent can activate any abilities meant for them on the Dummy card. If this card has one, they can activate it by double clicking on the dummy. Very often, this will often remove the dummy since its effect will disappear.\
                     \n\nOnce the   dummy card is on the table, please right-click on it and select 'Pass control to {}'\
                     \n\nDo you want to see this warning again?".format(targetPL)): Dummywarn = False      
      elif Dummywarn:
         information("This card is now supposed to go to your discard pile, but its lingering effects will only work automatically while a copy is in play.\
                       \nFor this reason we've created a dummy card on the table and marked it with a special highlight so that you know that it's just a token.\
                     \n\n(This message will not appear again.)")
         Dummywarn = False
      elif re.search(r'onOpponent', Autoscript): 
         if debugVerbosity >= 2: notify('### about to pop information') # debug
         information('The dummy card just created is meant for your opponent. Please right-click on it and select "Pass control to {}"'.format(targetPL))
      if debugVerbosity >= 2: notify('### Finished warnings. About to announce.') # debug
      dummyCard = table.create(card.model, playerside * 300, 150 * playerside, 1) # This will create a fake card like the one we just created.
      dummyCard.highlight = DummyColor
   if debugVerbosity >= 2: notify('### About to move to discard pile if needed') # debug
   if not re.search(r'doNotDiscard',Autoscript): card.moveTo(card.owner.piles['Discard Pile'])
   if action: announceString = TokensX('Put{}'.format(action.group(2)), announceText,dummyCard, n = n) # If we have a -with in our autoscript, this is meant to put some tokens on the dummy card.
   else: announceString = announceText + 'create a lingering effect for {}'.format(targetPL)
   if debugVerbosity >= 3: notify("<<< CreateDummy()")
   if re.search(r'isSilent', Autoscript): return announceText
   else: return announceString # Creating a dummy isn't usually announced.

def ChooseTrait(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for marking cards to be of a different trait than they are
   if debugVerbosity >= 1: notify(">>> ChooseTrait(){}".format(extraASDebug(Autoscript))) #Debug
   #confirm("Reached ChooseTrait") # Debug
   choiceTXT = ''
   targetCardlist = ''
   existingTrait = None
   if targetCards is None: targetCards = []
   if len(targetCards) == 0: targetCards.append(card) # If there's been to target card given, assume the target is the card itself.
   for targetCard in targetCards: targetCardlist += '{},'.format(targetCard)
   targetCardlist = targetCardlist.strip(',') # Re remove the trailing comma
   action = re.search(r'\bChooseTrait{([A-Za-z\| ]+)}', Autoscript)
   #confirm("search results: {}".format(action.groups())) # Debug
   traits = action.group(1).split('|')
   #confirm("List: {}".format(traits)) # Debug
   if len(traits) > 1:
      for i in range(len(traits)): choiceTXT += '{}: {}\n'.format(i, traits[i])
      choice = len(traits)
   else: choice = 0
   while choice > len(traits) - 1: 
      choice = askInteger("Choose one of the following traits to assign to this card:\n\n{}".format(choiceTXT),0)
      if choice == None: return 'ABORT'
   for targetCard in targetCards:
      if targetCard.markers:
         for key in targetCard.markers:
            if re.search('Trait:',key[0]):
               existingTrait = key
      if re.search(r'{}'.format(traits[choice]),targetCard.Traits): 
         if existingTrait: targetCard.markers[existingTrait] = 0
         else: pass # If the trait is anyway the same printed on the card, and it had no previous trait, there is nothing to do
      elif existingTrait:
         if debugVerbosity >= 1: notify("### Searching for {} in {}".format(traits[choice],existingTrait[0])) # Debug               
         if re.search(r'{}'.format(traits[choice]),existingTrait[0]): pass # If the trait is the same as is already there, do nothing.
         else: 
            targetCard.markers[existingTrait] = 0 
            TokensX('Put1Trait:{}'.format(traits[choice]), '', targetCard)
      else: TokensX('Put1Trait:{}'.format(traits[choice]), '', targetCard)
   if notification == 'Quick': announceString = "{} marks {} as being {} now".format(announceText, targetCardlist, traits[choice])
   else: announceString = "{} mark {} as being {} now".format(announceText, targetCardlist, traits[choice])
   if notification: notify(':> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< ChooseTrait()")
   return announceString
            
def ModifyStatus(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for modifying the status of a card on the table.
   if debugVerbosity >= 1: notify(">>> ModifyStatus(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   targetCardlist = '' # A text field holding which cards are going to get tokens.
   extraTXT = ''
   action = re.search(r'\b(Destroy|Exile|Capture|Rescue|Return|SendToBottom|Commit|Uncommit|Engage|Disengage|Sacrifice)(Target|Host|Multi|Myself)[-to]*([A-Z][A-Za-z&_ ]+)?', Autoscript)
   if action.group(2) == 'Myself': 
      del targetCards[:] # Empty the list, just in case.
      targetCards.append(card)
   if action.group(3): dest = action.group(3)
   else: dest = 'hand'
   if debugVerbosity >= 2: notify("### targetCards(){}".format(targetCards)) #Debug   
   for targetCard in targetCards: 
      if action.group(1) == 'Capture': targetCardlist += '{},'.format(fetchProperty(targetCard, 'name')) # Capture saves the name because by the time we announce the action, the card will be face down.
      else: targetCardlist += '{},'.format(targetCard)
   if debugVerbosity >= 3: notify("### Preparing targetCardlist")      
   targetCardlist = targetCardlist.strip(',') # Re remove the trailing comma
   if action.group(1) == 'SendToBottom': # For SendToBottom, we need a different mthod, as we need to shuffle the cards.
      if action.group(2) == 'Multi': 
         if debugVerbosity >= 3: notify("### Sending Multiple card to the bottom")   
         sendToBottom(targetCards) 
      else: 
         if debugVerbosity >= 3: notify("### Sending Single card to the bottom")   
         sendToBottom([targetCards[0]])
   for targetCard in targetCards:
      if action.group(1) == 'Destroy' or action.group(1) == 'Sacrifice':
         trashResult = discard(targetCard, silent = True)
         if trashResult == 'ABORT': return 'ABORT'
         elif trashResult == 'COUNTERED': extraTXT = " (Countered!)"
      elif action.group(1) == 'Exile' and exileCard(targetCard, silent = True) != 'ABORT': pass
      elif action.group(1) == 'Return': 
         if targetCard.group == table and targetCard.highlight != EdgeColor and targetCard.highlight != FateColor and card.highlight != CapturedColor: 
            executePlayScripts(targetCard, 'LEAVING')
            autoscriptOtherPlayers('CardLeavingPlay',targetCard)
         targetCard.moveTo(targetCard.owner.hand)
         extraTXT = " to their owner's hand"
      elif action.group(1) == 'Capture': capture(targetC = targetCard, silent = True)
      elif action.group(1) == 'Engage': participate(targetCard, silent = True)
      elif action.group(1) == 'Disengage': clearParticipation(targetCard, silent = True)
      elif action.group(1) == 'Rescue':
         if targetCard.isFaceUp: 
            notify(":::ERROR::: Target Card was not captured!")
            return 'ABORT'
         else: rescue(targetCard)
      elif action.group(1) == 'Uncommit':
         if targetCard.Side == 'Light': commitColor = LightForceColor
         else: commitColor = DarkForceColor
         if targetCard.highlight == commitColor: targetCard.highlight = None
      else: return 'ABORT'
      if action.group(2) != 'Multi': break # If we're not doing a multi-targeting, abort after the first run.
   if debugVerbosity >= 2: notify("### Finished Processing Modifications. About to announce")
   if notification == 'Quick': announceString = "{} {} {}{}".format(announceText, action.group(1), targetCardlist,extraTXT)
   else: announceString = "{} {} {}{}".format(announceText, action.group(1), targetCardlist, extraTXT)
   if notification and not re.search(r'isSilent', Autoscript): notify(':> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< ModifyStatus()")
   if re.search(r'isSilent', Autoscript): return announceText
   else: return announceString

def GameX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for alternative victory conditions
   if debugVerbosity >= 1: notify(">>> GameX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\b(Lose|Win)Game', Autoscript)
   if debugVerbosity >= 2: #Debug
      if action: notify("!!! regex: {}".format(action.groups())) 
      else: notify("!!! regex failed :(") 
   if re.search(r'forController', Autoscript): player = card.controller
   elif re.search(r'forOwner', Autoscript): player = card.owner 
   elif re.search(r'forDark Side', Autoscript): 
      if Side == 'Dark': player = me
      else: player == opponent
   elif re.search(r'forLight Side', Autoscript): 
      if Side == 'Light': player = me
      else: player == opponent
   else: player == me
   if action.group(1) == 'Lose': announceString = "=== {} loses the game! ===".format(player)
   else: announceString = "=== {} wins the game! ===".format(player)
   notify(announceString)
   if debugVerbosity >= 3: notify("<<< GameX()")
   return announceString

def RetrieveX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for finding a specific card from a pile and putting it in hand or discard pile
   if debugVerbosity >= 1: notify(">>> RetrieveX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bRetrieve([0-9]+)Card', Autoscript)
   targetPL = ofwhom(Autoscript, card.controller)
   if debugVerbosity >= 2: notify("### Setting Source")
   if re.search(r'-fromDiscard', Autoscript):
      source = targetPL.piles['Discard Pile']
      sourcePath =  "from their Discard Pile"
   else: 
      source = targetPL.piles['Command Deck']
      sourcePath =  "from their Command Deck"
   if debugVerbosity >= 2: notify("### Setting Destination")
   if re.search(r'-toTable', Autoscript):
      destination = table
      destiVerb = 'play'   
   else: 
      destination = targetPL.hand
      destiVerb = 'retrieve'
   if debugVerbosity >= 2: notify("### Fething Script Variables")
   count = num(action.group(1))
   multiplier = per(Autoscript, card, n, targetCards, notification)
   if source != targetPL.piles['Discard Pile']: # The discard pile is anyway visible.
      if debugVerbosity >= 2: notify("### Turning Pile Face Up")
      cover = table.create("8b5a86df-fb10-4e5e-9133-7dc03fbae22d",0,0,1,True) # Creating a dummy card to cover that player's source pile
      cover.moveTo(source) # Moving that dummy card on top of their source pile
      for c in source: c.isFaceUp = True # We flip all cards in the player's deck face up so that we can grab their properties
   restrictions = prepareRestrictions(Autoscript, seek = 'type')
   cardList = []
   countRestriction = re.search(r'-onTop([0-9]+)Cards', Autoscript)
   if countRestriction: topCount = num(countRestriction.group(1))
   else: topCount = len(source)
   if count == 999: count = topCount # Retrieve999Cards means the script will retrieve all cards that match the requirements, regardless of how many there are. As such, a '-onTop#Cards' modulator should always be included.
   for c in source.top(topCount):
      if debugVerbosity >= 4: notify("### Checking card: {}".format(c))
      if checkCardRestrictions(gatherCardProperties(c), restrictions) and checkSpecialRestrictions(Autoscript,c):
         cardList.append(c)
         if re.search(r'-isTopmost', Autoscript) and len(cardList) == count: break # If we're selecting only the topmost cards, we select only the first matches we get.         
   if debugVerbosity >= 3: notify("### cardList: {}".format(cardList))
   chosenCList = []
   if len(cardList) > count:
      cardChoices = []
      cardTexts = []
      for iter in range(count):
         if debugVerbosity >= 4: notify("#### iter: {}/{}".format(iter,count))
         del cardChoices[:]
         del cardTexts[:]
         for c in cardList:
            if c.Text not in cardTexts: # we don't want to provide the player with a the same card as a choice twice.
               if debugVerbosity >= 4: notify("### Appending card")
               cardChoices.append(c)
               cardTexts.append(c.Text) # We check the card text because there are cards with the same name in different sets (e.g. Darth Vader)            
         choice = SingleChoice("Choose card to retrieve{}".format({1:''}.get(count,' {} {}'.format(iter + 1,count))), makeChoiceListfromCardList(cardChoices), type = 'button')
         chosenCList.append(cardChoices[choice])
         cardList.remove(cardChoices[choice])
   else: chosenCList = cardList
   if debugVerbosity >= 2: notify("### chosenCList: {}".format(chosenCList))
   for c in chosenCList:
      if destination == table: placeCard(c)
      else: c.moveTo(destination)
   if source != targetPL.piles['Discard Pile']:
      if debugVerbosity >= 2: notify("### Turning Pile Face Down")
      for c in source: c.isFaceUp = False # We hide again the source pile cards.
      cover.moveTo(me.ScriptingPile) # we cannot delete cards so we just hide it.
   if debugVerbosity >= 2: notify("### About to announce.")
   if len(chosenCList) == 0: announceString = "{} attempts to {} a card {}, but there were no valid targets.".format(announceText, destiVerb, sourcePath)
   else: announceString = "{} {} {} {}.".format(announceText, destiVerb, [c.name for c in chosenCList], sourcePath)
   if notification and multiplier > 0: notify(':> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< RetrieveX()")
   return announceString
   
def UseCustomAbility(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # not used yet.
   announceString = announceText 
   return announceString

def CustomScript(card, action = 'PLAY'): # Scripts that are complex and fairly unique to specific cards, not worth making a whole generic function for them.
   if debugVerbosity >= 1: notify(">>> CustomScript() with action: {}".format(action)) #Debug
   mute()
   global opponent
   discardPile = me.piles['Discard Pile']
   objectives = me.piles['Objective Deck']
   deck = me.piles['Command Deck']
   if card.name == 'A Journey to Dagobah' and action == 'THWART' and card.owner == me:
      if not confirm("Do you want to use the optional interrupt of Journey To Dagobath?"): return
      if debugVerbosity >= 2: notify("### Journey to Dagobath Script")
      objList = []
      if debugVerbosity >= 2: notify("### Moving objectives to removed from game pile")
      for c in objectives:
         c.moveTo(me.ScriptingPile)
         objList.append(c._id)
      rnd(1,10)
      objNames = []
      objDetails = []
      if debugVerbosity >= 2: notify("### Storing objective properties and moving them back")
      for obj in objList:
         if debugVerbosity >= 3: notify("#### Card Name: {}".format(Card(obj).name))
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
      choice = SingleChoice("Which objective do you want to put into play from your deck?", objChoices, type = 'button', default = 0,cancelButton = False)
      storeObjective(Card(objList[choice]))
      shuffle(objectives)
      if debugVerbosity >= 2: notify("#### About to announce")
      notify("{} uses the ability of {} to replace it with {}".format(me,card,Card(objList[choice])))
   elif card.name == 'Black Squadron Pilot' and action == 'PLAY':
      if len(findTarget('AutoTargeted-atFighter_and_Unit-byMe')) > 0 and confirm("This unit has an optional ability which allows it to be played as an enchantment on a fighter. Do so now?"):
         fighter = findTarget('AutoTargeted-atFighter_and_Unit-byMe-choose1')
         if len(fighter) == 0: return
         hostCards = eval(getGlobalVariable('Host Cards'))
         hostCards[card._id] = fighter[0]._id
         setGlobalVariable('Host Cards',str(hostCards))
         cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == fighter[0]._id])
         if debugVerbosity >= 2: notify("### About to move into position") #Debug
         x,y = fighter[0].position
         card.moveToTable(x, y - ((cwidth(card) / 4 * playerside) * cardAttachementsNR))
         card.sendToBack()
         TokensX('Put1isEnhancement-isSilent', '', card)
   elif card.name == 'Wedge Antilles' and action == 'PLAY':
      if len(findTarget('AutoTargeted-atFighter_or_Speeder-byMe')) > 0 and confirm("This unit has an optional ability which allows it to be played as an enchantment on a Fighter or Speeder. Do so now?"):
         fighter = findTarget('AutoTargeted-atFighter_or_Speeder-byMe-choose1')
         if len(fighter) == 0: return
         hostCards = eval(getGlobalVariable('Host Cards'))
         hostCards[card._id] = fighter[0]._id
         setGlobalVariable('Host Cards',str(hostCards))
         cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == fighter[0]._id])
         if debugVerbosity >= 2: notify("### About to move into position") #Debug
         x,y = fighter[0].position
         card.moveToTable(x, y - ((cwidth(card) / 4 * playerside) * cardAttachementsNR))
         card.sendToBack()
         TokensX('Put1isEnhancement-isSilent', '', card)
   elif card.name == 'Cruel Interrogations' and action == 'PLAY':
      if not confirm("Do you wish to use Cruel Interrogations' Reaction?"): return
      while len(opponent.hand) == 0: 
         if not confirm("Your opponent has no cards in their hand.\n\nRetry?"): return
      turn = num(getGlobalVariable('Turn'))
      captureTarget = opponent.hand.random()
      capture(chosenObj = card, targetC = captureTarget)
   elif card.name == 'Rancor' and action == 'afterRefresh' and card.controller == me:
      possibleTargets = [c for c in table if c.Type == 'Unit' and not re.search('Vehicle',c.Traits)]
      if len(possibleTargets) == 0: return 'ABORT' # Nothing to kill
      minCost = 10 
      currTargets = []
      for c in possibleTargets:
         if debugVerbosity >= 4: notify("### Checking {}".format(c))
         if num(c.Cost) < minCost:
            del currTargets[:]
            currTargets.append(c)
            minCost = num(c.Cost)
         elif num(c.Cost) == minCost: currTargets.append(c)
         else: pass
      if debugVerbosity >= 2: notify("### Finished currTargets") #Debug         
      if debugVerbosity >= 4 and len(currTargets) > 0: notify("### Minimum Cost Targets = {}".format([c.name for c in currTargets])) #Debug
      if len(currTargets) == 1: finalTarget = currTargets[0]
      else: 
         choice = SingleChoice("Choose one unit to be destroyed by the Rancor", makeChoiceListfromCardList(currTargets), type = 'button', default = 0)
         if choice == 'ABORT': 
            notify(":::NOTICE::: {} has skipped Rancor's effects this turn".format(me))
            return
         finalTarget = currTargets[choice]
      if debugVerbosity >= 2: notify("### finalTarget = {}".format(finalTarget)) #Debug
      discard(finalTarget,silent = True)
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
      if debugVerbosity >= 2: notify("### Return of the Jedi")
      discardList = []
      if debugVerbosity >= 2: notify("### Moving Force Users to 'removed from game' pile from discard pile")
      for c in discardPile:
         c.moveTo(me.ScriptingPile)
         discardList.append(c._id)
      rnd(1,10)
      unitNames = []
      unitDetails = []
      ForceUserList = []
      if debugVerbosity >= 2: notify("### Storing unit properties and moving them back")
      for unit in discardList:
         if debugVerbosity >= 3: notify("#### Card Name: {}".format(Card(unit).name))
         if not Card(unit).name in unitNames and re.search(r'Force User',Card(unit).Traits):
            ForceUserList.append(unit)
            unitNames.append(Card(unit).name)
            unitDetails.append((Card(unit).properties['Damage Capacity'],Card(unit).Traits,parseCombatIcons(Card(unit).properties['Combat Icons']),Card(unit).Text)) # Creating a tuple with some details per objective
         if debugVerbosity >= 3: notify("#### Finished Storing. Moving back")
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
         choice = SingleChoice("Which Force User unit do you want to put into play from your discard pile?", unitChoices, type = 'button', default = 0, cancelButton = False)
      placeCard(Card(ForceUserList[choice]))
      if debugVerbosity >= 2: notify("#### About to announce")
      notify("{} returns into play".format(Card(ForceUserList[choice])))
   elif card.name == 'Superlaser Engineer' and action == 'PLAY': 
      if not confirm("Do you want to activate the optional ability of reaction of Superlaser Engineer?"): return
      cardList = []
      sendToBottomList = []
      iter = 0
      for c in deck.top(5):
         c.moveToTable((cwidth(c) * 2) - (iter * cwidth(c)),0)
         cardList.append(c._id)
         c.highlight = '#FF2222'
         iter += 1
      rnd(1,10)
      revealedCards = ''
      for cid in cardList: revealedCards += '{}, '.format(Card(cid))
      notify("{} activates the ability of their Superlaser Engineer and reveals the top 5 cards of their deck: {}".format(me,revealedCards))      
      for cid in cardList:
         if (Card(cid).Type == 'Event' or Card(cid).Type == 'Enhancement') and Card(cid).Affiliation == 'Imperial Navy' and num(Card(cid).Cost) >= 3:
            notify(":> {} moves {} to their hand".format(me,Card(cid)))
            Card(cid).moveTo(me.hand)
         else:
            sendToBottomList.append(Card(cid))
      sendToBottom(sendToBottomList)
   elif card.name == 'Take Them Prisoner' and action == 'PLAY': 
      debugNotify("Enterring 'Take Them Prisoner' Automation",1)
      if not confirm("Do you want to activate the optional ability of Take Them Prisoner?"): return
      turn = num(getGlobalVariable('Turn'))
      cardList = []
      cardNames = []
      cardDetails = []
      debugNotify("About to move cards to me.ScriptingPile",2)
      for c in opponent.piles['Command Deck'].top(3):
         c.moveTo(me.ScriptingPile)
         cardList.append(c._id)
      rnd(1,10)
      for cid in cardList:
         if debugVerbosity >= 3: notify("#### Card Name: {}".format(Card(cid).name))
         cardNames.append(Card(cid).name)
         cardDetails.append((Card(cid).Type,Card(cid).properties['Damage Capacity'],Card(cid).Resources,Card(cid).Traits,parseCombatIcons(Card(cid).properties['Combat Icons']),Card(cid).Text)) # Creating a tuple with some details per objective
         if debugVerbosity >= 3: notify("#### Finished Storing.")
      ChoiceTXT = []
      for iter in range(len(cardList)):
         ChoiceTXT.append("{}\
                          \nType: {}\
                          \nDamage Capacity: {}, Resources: {}\
                          \nTraits: {}\
                          \nIcons: {}\
                          \nText: {}\
                          ".format(cardNames[iter], cardDetails[iter][0], cardDetails[iter][1], cardDetails[iter][2],cardDetails[iter][3],cardDetails[iter][4],cardDetails[iter][5]))
      choice = SingleChoice("Which card do you wish to capture?", ChoiceTXT, type = 'button', default = 0,cancelButton = False)
      capturedC = Card(cardList.pop(choice))
      capturedC.moveTo(opponent.piles['Command Deck']) # We move it back to the deck, so that the capture function can announce the correct location from which it was taken.
      if debugVerbosity >= 3: notify("#### About to capture.")
      capture(chosenObj = card,targetC = capturedC, silent = True)
      if debugVerbosity >= 3: notify("#### Removing choice text")
      ChoiceTXT.pop(choice) # We also remove the choice text entry at that point.
      choice = SingleChoice("Which card do you wish to leave on top of your opponent's command deck?", ChoiceTXT, type = 'button', default = 0,cancelButton = False)
      for iter in range(len(cardList)):
         if debugVerbosity >= 2: confirm("#### Moving {} (was at position {}. choice was {})".format(Card(cardList[iter]).name, iter,choice))
         if iter == choice: Card(cardList[iter]).moveTo(opponent.piles['Command Deck'],0)
         else: Card(cardList[iter]).moveTo(opponent.piles['Command Deck'],1)
      notify(":> {} activates Takes Them Prisoner to capture one card from the top 3 cards of {}'s command deck".format(me,opponent))
   elif card.name == 'Trench Run' and action == 'PLAY': # We move this card to the opponent's exile in order to try and give control to them automatically.
      card.moveTo(opponent.ScriptingPile)
      rnd(1,10)
      if me.hasInvertedTable(): card.moveToTable(0,0)
      else:  card.moveToTable(0,-cheight(card))
      if debugVerbosity >= 2: notify("About to whisper") # Debug
      whisper(":::IMPORTANT::: Please make sure that the controller for this card is always the Dark Side player")
   elif card.name == 'Twist of Fate' and action == 'RESOLVEFATE': 
      for card in table:
         if card.highlight == EdgeColor or card.highlight == FateColor:
            card.moveTo(card.owner.piles['Discard Pile'])
      global edgeCount
      edgeCount = 0            
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
      delayed_whisper("-- Calculating Yoda's Combat Icons. Please wait...")
      TokensX('Remove999Yoda enhancements:UD-isSilent', '', card)
      TokensX('Remove999Yoda enhancements:BD-isSilent', '', card)
      hostCards = eval(getGlobalVariable('Host Cards'))
      cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == card._id])
      if cardAttachementsNR and gotEdge():
         TokensX('Put{}Yoda enhancements:UD-isSilent'.format(cardAttachementsNR), '', card)
         TokensX('Put{}Yoda enhancements:BD-isSilent'.format(cardAttachementsNR), '', card)
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
            whisper(":::Error::: Current engagement not at another on of your objectives.")
            return
      if oncePerTurn(card) == 'ABORT': return
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
      if debugVerbosity >= 4: notify("### choiceC = {}".format(choiceC)) # Debug
      if debugVerbosity >= 4: notify("### currentTargets = {}".format([currentTarget.name for currentTarget in currentTargets])) # Debug
      sourceCard = currentTargets.pop(choiceC)
      if debugVerbosity >= 2: notify("### sourceCard = {}".format(sourceCard)) # Debug
      targetCard = currentTargets[0] # After we pop() the choice card, whatever remains is the target card.
      if debugVerbosity >= 2: notify("### targetCard = {}".format(targetCard)) # Debug
      printedIcons = parseCombatIcons(sourceCard.properties['Combat Icons'])
      IconChoiceList = ["Unit Damage","Edge-Enabled Unit Damage","Blast Damage","Edge-Enabled Blast Damage","Tactics","Edge-Enabled Tactics"] # This list is a human readable one for the user to choose an icon
      IconList = ["UD","EE-UD","BD","EE-BD","Tactics","EE-Tactics"] # This list has the same icons as the above, but uses the keywords that the game expects in a marker, so it makes it easier to figure out which icon the user selected.
      if debugVerbosity >= 2: notify("### About to select combat icon to steal")
      choiceIcons = SingleChoice("The card has the following printed Combat Icons: {}.\nChoose a combat icon to steal.\n(We leave the choice open, in case the card has received a combat icon from a card effect)".format(printedIcons), IconChoiceList, type = 'button', default = 0)
      card.markers[mdict['Focus']] += 1
      TokensX('Put1Echo Caverns:minus{}-isSilent'.format(IconList[choiceIcons]), '', sourceCard)
      TokensX('Put1Echo Caverns:{}-isSilent'.format(IconList[choiceIcons]), '', targetCard)
      notify("{} activates {} to move one {} icon from {} to {}".format(me,card,IconChoiceList[choiceIcons],sourceCard,targetCard))
   elif card.name == "Prophet of the Dark Side" and action == 'PLAY':
         cardView = me.piles['Command Deck'][1]
         ScriptingPile
         cardView.moveTo(me.ScriptingPile)
         #cardView.isFaceUp = True
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
      if confirm("You you want to use Z-95 Headhunter's interrupt?"):
         opponent = findOpponent()
         shownCards = showatrandom(targetPL = opponent, silent = True)
         if len(shownCards) == 0:
            notify("{} has no cards in their hand".format(opponent))
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
   else: notify("{} uses {}'s ability".format(me,card)) # Just a catch-all.
#------------------------------------------------------------------------------
# Helper Functions
#------------------------------------------------------------------------------
       
def findTarget(Autoscript, fromHand = False, card = None): # Function for finding the target of an autoscript
   if debugVerbosity >= 1: notify(">>> findTarget(){}".format(extraASDebug(Autoscript))) #Debug
   try:
      if fromHand == True or re.search(r'-fromHand',Autoscript): group = me.hand
      else: group = table
      foundTargets = []
      if re.search(r'Targeted', Autoscript):
         requiredAllegiances = []
         targetGroups = prepareRestrictions(Autoscript)
         if debugVerbosity >= 2: notify("### About to start checking all targeted cards.\n### targetGroups:{}".format(targetGroups)) #Debug
         for targetLookup in group: # Now that we have our list of restrictions, we go through each targeted card on the table to check if it matches.
            if ((targetLookup.targetedBy and targetLookup.targetedBy == me) or re.search(r'AutoTargeted', Autoscript)) and targetLookup.highlight != EdgeColor and targetLookup.highlight !=FateColor: 
            # OK the above target check might need some decoding:
            # Look through all the cards on the group and start checking only IF...
            # * Card is targeted and targeted by the player OR target search has the -AutoTargeted modulator and it is NOT highlighted as a Fate, Edge or Captured.
            # * The player who controls this card is supposed to be me or the enemy.
               if debugVerbosity >= 2: notify("### Checking {}".format(targetLookup))
               if not checkSpecialRestrictions(Autoscript,targetLookup): continue
               if re.search(r'-onHost',Autoscript):   
                  if debugVerbosity >= 2: notify("### Looking for Host")
                  if not card: continue # If this targeting script targets only a host and we have not passed what the attachment is, we cannot find the host, so we abort.
                  if debugVerbosity >= 2: notify("### Attachment is: {}".format(card))
                  hostCards = eval(getGlobalVariable('Host Cards'))
                  isHost = False
                  for attachment in hostCards:
                     if attachment == card._id and hostCards[attachment] == targetLookup._id: 
                        if debugVerbosity >= 2: notify("### Host found! {}".format(targetLookup))
                        isHost = True
                  if not isHost: continue
               if checkCardRestrictions(gatherCardProperties(targetLookup), targetGroups): 
                  if not targetLookup in foundTargets: 
                     if debugVerbosity >= 3: notify("### About to append {}".format(targetLookup)) #Debug
                     foundTargets.append(targetLookup) # I don't know why but the first match is always processed twice by the for loop.
               elif debugVerbosity >= 3: notify("### findTarget() Rejected {}".format(targetLookup))# Debug
         if debugVerbosity >= 2: notify("### Finished seeking. foundTargets List = {}".format([c.name for c in foundTargets]))
         if re.search(r'DemiAutoTargeted', Autoscript):
            if debugVerbosity >= 2: notify("### Checking DemiAutoTargeted switches")# Debug
            targetNRregex = re.search(r'-choose([1-9])',Autoscript)
            targetedCards = 0
            foundTargetsTargeted = []
            if debugVerbosity >= 2: notify("### About to count targeted cards")# Debug
            for targetC in foundTargets:
               if targetC.targetedBy and targetC.targetedBy == me: foundTargetsTargeted.append(targetC)
            if targetNRregex:
               if debugVerbosity >= 2: notify("!!! targetNRregex exists")# Debug
               if num(targetNRregex.group(1)) > len(foundTargetsTargeted): pass # Not implemented yet. Once I have choose2 etc I'll work on this
               else: # If we have the same amount of cards targeted as the amount we need, then we just select the targeted cards
                  foundTargets = foundTargetsTargeted # This will also work if the player has targeted more cards than they need. The later choice will be simply between those cards.
            else: # If we do not want to choose, then it's probably a bad script. In any case we make sure that the player has targeted something (as the alternative it giving them a random choice of the valid targets)
               del foundTargets[:]
         if len(foundTargets) == 0 and not re.search(r'(?<!Demi)AutoTargeted', Autoscript) and not re.search(r'noTargetingError', Autoscript): 
            targetsText = ''
            mergedList = []
            for posRestrictions in targetGroups: 
               if debugVerbosity >= 2: notify("### About to notify on restrictions")# Debug
               if targetsText == '': targetsText = '\nYou need: '
               else: targetsText += ', or '
               del mergedList[:]
               mergedList += posRestrictions[0]
               if len(mergedList) > 0: targetsText += "{} and ".format(mergedList)  
               del mergedList[:]
               mergedList += posRestrictions[1]
               if len(mergedList) > 0: targetsText += "not {}".format(mergedList)
               if targetsText.endswith(' and '): targetsText = targetsText[:-len(' and ')]
            if debugVerbosity >= 2: notify("### About to chkPlayer()")# Debug
            reversed = False
            if card:
               if card.controller != me: # If we have provided the originator card to findTarget, and the card is not our, we assume that we need to treat the script as being run by our opponent
                  global reversePlayerChk
                  reversePlayerChk = True
                  reversed = True
            if not chkPlayer(Autoscript, targetLookup.controller, False, True): 
               allegiance = re.search(r'target(Opponents|Mine)', Autoscript)
               requiredAllegiances.append(allegiance.group(1))
            if reversed: reversePlayerChk = False # We return things to normal now.
            if len(requiredAllegiances) > 0: targetsText += "\nValid Target Allegiance: {}.".format(requiredAllegiances)
            whisper(":::ERROR::: You need to target a valid card before using this action{}.".format(targetsText))
         elif len(foundTargets) >= 1 and re.search(r'-choose',Autoscript):
            if debugVerbosity >= 2: notify("### Going for a choice menu")# Debug
            choiceType = re.search(r'-choose([0-9]+)',Autoscript)
            targetChoices = makeChoiceListfromCardList(foundTargets)
            if not card: choiceTitle = "Choose one of the valid targets for this effect"
            else: choiceTitle = "Choose one of the valid targets for {}'s ability".format(card.name)
            if debugVerbosity >= 2: notify("### Checking for SingleChoice")# Debug
            if choiceType.group(1) == '1':
               if len(foundTargets) == 1: choice = 0 # If we only have one valid target, autoselect it.
               else: choice = SingleChoice(choiceTitle, targetChoices, type = 'button', default = 0)
               if choice == 'ABORT': del foundTargets[:]
               else: foundTargets = [foundTargets.pop(choice)] # if we select the target we want, we make our list only hold that target
      if debugVerbosity >= 3: # Debug
         tlist = [] 
         for foundTarget in foundTargets: tlist.append(foundTarget.name) # Debug
         notify("<<< findTarget() by returning: {}".format(tlist))
      return foundTargets
   except: notify("!!!ERROR!!! on findTarget()")

def gatherCardProperties(card):
   if debugVerbosity >= 1: notify(">>> gatherCardProperties()") #Debug
   cardProperties = []
   if debugVerbosity >= 4: notify("### Appending name") #Debug                
   cardProperties.append(card.name) # We are going to check its name
   if debugVerbosity >= 4: notify("### Appending Type") #Debug                
   cardProperties.append(card.Type) # We are going to check its Type
   if debugVerbosity >= 4: notify("### Appending Affiliation") #Debug                
   cardProperties.append(card.Affiliation) # We are going to check its Affiliation
   if debugVerbosity >= 4: notify("### Appending Traits") #Debug                
   cardSubtypes = card.Traits.split('-') # And each individual trait. Traits are separated by " - "
   for cardSubtype in cardSubtypes:
      strippedCS = cardSubtype.strip() # Remove any leading/trailing spaces between traits. We need to use a new variable, because we can't modify the loop iterator.
      if strippedCS: cardProperties.append(strippedCS) # If there's anything left after the stip (i.e. it's not an empty string anymrore) add it to the list.
   if debugVerbosity >= 4: notify("### Appending Side") #Debug                
   cardProperties.append(card.Side) # We are also going to check if the card is for Dark or Light Side
   if debugVerbosity >= 3: notify("<<< gatherCardProperties() with Card Properties: {}".format(cardProperties)) #Debug
   return cardProperties

def prepareRestrictions(Autoscript, seek = 'target'):
# This is a function that takes an autoscript and attempts to find restrictions on card traits/types/names etc. 
# It goes looks for a specific working and then gathers all restrictions into a list of tuples, where each tuple has a negative and a positive entry
# The positive entry (position [0] in the tuple) contains what card properties a card needs to have to be a valid selection
# The negative entry (position [1] in the tuple) contains what card properties a card needs to NOT have to be a vaid selection.
   if debugVerbosity >= 1: notify(">>> prepareRestrictions() {}".format(extraASDebug(Autoscript))) #Debug
   validTargets = [] # a list that holds any type that a card must be, in order to be a valid target.
   targetGroups = []
   if seek == 'type': whatTarget = re.search(r'\b(type|from)([A-Za-z_{},& ]+)[-]?', Autoscript) # seek of "type" is used by autoscripting other players, and it's separated so that the same card can have two different triggers (e.g. see Darth Vader)
   else: whatTarget = re.search(r'\b(at|for)([A-Za-z_{},& ]+)[-]?', Autoscript) # We signify target restrictions keywords by starting a string with "or"
   if whatTarget: 
      if debugVerbosity >= 2: notify("### Splitting on _or_") #Debug
      validTargets = whatTarget.group(2).split('_or_') # If we have a list of valid targets, split them into a list, separated by the string "_or_". Usually this results in a list of 1 item.
      ValidTargetsSnapshot = list(validTargets) # We have to work on a snapshot, because we're going to be modifying the actual list as we iterate.
      for iter in range(len(ValidTargetsSnapshot)): # Now we go through each list item and see if it has more than one condition (Eg, non-desert fief)
         if debugVerbosity >= 2: notify("### Creating empty list tuple") #Debug            
         targetGroups.insert(iter,([],[])) # We create a tuple of two list. The first list is the valid properties, the second the invalid ones
         multiConditionTargets = ValidTargetsSnapshot[iter].split('_and_') # We put all the mutliple conditions in a new list, separating each element.
         if debugVerbosity >= 2: notify("###Splitting on _and_ & _or_ ") #Debug
         if debugVerbosity >= 4: notify("### multiConditionTargets is: {}".format(multiConditionTargets)) #Debug
         for chkCondition in multiConditionTargets:
            if debugVerbosity >= 4: notify("### Checking: {}".format(chkCondition)) #Debug
            regexCondition = re.search(r'(no[nt]){?([A-Za-z,& ]+)}?', chkCondition) # Do a search to see if in the multicondition targets there's one with "non" in front
            if regexCondition and (regexCondition.group(1) == 'non' or regexCondition.group(1) == 'not'):
               if debugVerbosity >= 4: notify("### Invalid Target") #Debug
               if regexCondition.group(2) not in targetGroups[iter][1]: targetGroups[iter][1].append(regexCondition.group(2)) # If there is, move it without the "non" into the invalidTargets list.
            else: 
               if debugVerbosity >= 4: notify("### Valid Target") #Debug
               targetGroups[iter][0].append(chkCondition) # Else just move the individual condition to the end if validTargets list
   elif debugVerbosity >= 2: notify("### No restrictions regex") #Debug 
   if debugVerbosity >= 3: notify("<<< prepareRestrictions() by returning: {}.".format(targetGroups))
   return targetGroups

def checkCardRestrictions(cardPropertyList, restrictionsList):
   if debugVerbosity >= 1: notify(">>> checkCardRestrictions()") #Debug
   if debugVerbosity >= 2: notify("### cardPropertyList = {}".format(cardPropertyList)) #Debug
   if debugVerbosity >= 2: notify("### restrictionsList = {}".format(restrictionsList)) #Debug
   validCard = True
   for restrictionsGroup in restrictionsList: 
   # We check each card's properties against each restrictions group of valid + invalid properties.
   # Each Restrictions group is a tuple of two lists. First list (tuple[0]) is the valid properties, and the second list is the invalid properties
   # We check if all the properties from the valid list are in the card properties
   # And then we check if no properties from the invalid list are in the properties
   # If both of these are true, then the card is a valid choice for our action.
      validCard = True # We need to set it here as well for further loops
      if debugVerbosity >= 3: notify("### restrictionsGroup checking: {}".format(restrictionsGroup))
      if len(restrictionsList) > 0 and len(restrictionsGroup[0]) > 0: 
         for validtargetCHK in restrictionsGroup[0]: # look if the card we're going through matches our valid target checks
            if debugVerbosity >= 4: notify("### Checking for valid match on {}".format(validtargetCHK)) #Debug
            if not validtargetCHK in cardPropertyList: 
               if debugVerbosity >= 4: notify("### {} not found in {}".format(validtargetCHK,cardPropertyList)) #Debug
               validCard = False
      elif debugVerbosity >= 4: notify("### No positive restrictions")
      if len(restrictionsList) > 0 and len(restrictionsGroup[1]) > 0: # If we have no target restrictions, any selected card will do as long as it's a valid target.
         for invalidtargetCHK in restrictionsGroup[1]:
            if debugVerbosity >= 4: notify("### Checking for invalid match on {}".format(invalidtargetCHK)) #Debug
            if invalidtargetCHK in cardPropertyList: validCard = False
      elif debugVerbosity >= 4: notify("### No negative restrictions")
      if validCard: break # If we already passed a restrictions check, we don't need to continue checking restrictions 
   if debugVerbosity >= 1: notify("<<< checkCardRestrictions() with return {}".format(validCard)) #Debug
   return validCard

def checkSpecialRestrictions(Autoscript,card):
# Check the autoscript for special restrictions of a valid card
# If the card does not validate all the restrictions included in the autoscript, we reject it
   if debugVerbosity >= 1: notify(">>> checkSpecialRestrictions() {}".format(extraASDebug(Autoscript))) #Debug
   if debugVerbosity >= 1: notify("### Card: {}".format(card)) #Debug
   validCard = True
   if re.search(r'isCurrentObjective',Autoscript) and card.highlight != DefendColor: 
      debugNotify("Failing Because it's not current objective", 2)
      validCard = False
   if re.search(r'isParticipating',Autoscript) and card.orientation != Rot90 and card.highlight != DefendColor: 
      debugNotify("Failing Because it's not participating", 2)
      validCard = False
   if re.search(r'isCaptured',Autoscript) and card.highlight != CapturedColor: 
      debugNotify("Was looking for a captured card but this ain't it", 2)
      validCard = False
   if re.search(r'isUnpaid',Autoscript) and card.highlight != UnpaidColor: 
      debugNotify("Failing Because card is not Unpaid", 2)
      validCard = False
   if re.search(r'isReady',Autoscript) and card.highlight != UnpaidColor and card.highlight != ReadyEventColor: 
      debugNotify("Failing Because card is not Paid", 2)
      validCard = False
   if re.search(r'isNotParticipating',Autoscript) and (card.orientation == Rot90 or card.highlight == DefendColor): 
      debugNotify("Failing Because unit is participating", 2)
      validCard = False
   if re.search(r'isAttacking',Autoscript) or re.search(r'isDefending',Autoscript):
      EngagedObjective = getGlobalVariable('Engaged Objective')
      if EngagedObjective == 'None': 
         debugNotify("Failing Because we're looking for at Attacker/Defender and there's no objective", 2)
         validCard = False
      else:
         currentTarget = Card(num(EngagedObjective))
         if re.search(r'isAttacking',Autoscript) and currentTarget.controller == card.controller: 
            debugNotify("Failing Because unit it not attacking", 2)
            validCard = False
         elif re.search(r'isDefending',Autoscript)  and currentTarget.controller != card.controller: 
            debugNotify("Failing Because unit is not defending", 2)
            validCard = False
   if re.search(r'isDamagedObjective',Autoscript): # If this keyword is there, the current objective needs to be damaged
      debugNotify("Checking for Damaged Objective", 2)
      EngagedObjective = getGlobalVariable('Engaged Objective')
      if EngagedObjective == 'None': 
         debugNotify("Failing Because we're looking for a damaged objective and there's no objective at all", 2)         
         validCard = False
      else:
         currentTarget = Card(num(EngagedObjective))
         if not currentTarget.markers[mdict['Damage']]:
            try: debugNotify("Requires Damaged objective but {} Damage Markers found on {}".format(currentTarget.markers[mdict['Damage']],currentTarget),2)
            except: debugNotify("Oops! I guess markers were null", 2)
            validCard = False
   if re.search(r'isCommited',Autoscript) and card.highlight != LightForceColor and card.highlight != DarkForceColor: 
      debugNotify("Failing Because card is not committed to the force", 2)
      validCard = False
   if not chkPlayer(Autoscript, card.controller, False, True): 
      debugNotify("Failing Because not the right controller", 2)
      validCard = False
   markerName = re.search(r'-hasMarker{([\w :]+)}',Autoscript) # Checking if we need specific markers on the card.
   if markerName: #If we're looking for markers, then we go through each targeted card and check if it has any relevant markers
      if debugVerbosity >= 2: notify("### Checking marker restrictions")# Debug
      if debugVerbosity >= 2: notify("### Marker Name: {}".format(markerName.group(1)))# Debug
      if markerName.group(1) == 'AnyTokenType': #
         if not (card.markers[mdict['Focus']] or card.markers[mdict['Shield']] or card.markers[mdict['Damage']]): 
            debugNotify("Failing Because card is missing all default markers", 2)
            validCard = False
      else: 
         marker = findMarker(card, markerName.group(1))
         if not marker: 
            debugNotify("Failing Because it's missing marker", 2)
            validCard = False
   markerNeg = re.search(r'-hasntMarker{([\w ]+)}',Autoscript) # Checking if we need to not have specific markers on the card.
   if markerNeg: #If we're looking for markers, then we go through each targeted card and check if it has any relevant markers
      if debugVerbosity >= 2: notify("### Checking negative marker restrictions")# Debug
      if debugVerbosity >= 2: notify("### Marker Name: {}".format(markerNeg.group(1)))# Debug
      marker = findMarker(card, markerNeg.group(1))
      if marker: 
         debugNotify("Failing Because it has marker", 2)
         validCard = False
   elif debugVerbosity >= 4: notify("### No negative marker restrictions.")
   # Checking if the target needs to have a property at a certiain value. 
   propertyReq = re.search(r'-hasProperty{([\w ]+)}(eq|le|ge|gt|lt)([0-9])',Autoscript) 
   if propertyReq: validCard = compareValue(propertyReq.group(2), num(card.properties[propertyReq.group(1)]), num(propertyReq.group(3)))
   # Checking if the target needs to have a markers at a particular value.
   MarkerReq = re.search(r'-ifMarkers{([\w ]+)}(eq|le|ge|gt|lt)([0-9])',Autoscript)
   if MarkerReq: 
      if debugVerbosity >= 4: notify("Found marker comparison req. regex groups: {}".format(MarkerReq.groups()))
      markerSeek = findMarker(card, MarkerReq.group(1))
      if markerSeek:
         validCard = compareValue(MarkerReq.group(2), card.markers[markerSeek], num(MarkerReq.group(3)))
   # Checking if the DS Dial needs to be at a specific value
   DialReq = re.search(r'-ifDial(eq|le|ge|gt|lt)([0-9]+)',Autoscript)
   if DialReq: validCard = compareValue(DialReq.group(1), me.counters['Death Star Dial'].value, num(DialReq.group(2)))
   if debugVerbosity >= 1: notify("<<< checkSpecialRestrictions() with return {}".format(validCard)) #Debug
   return validCard

def checkOriginatorRestrictions(Autoscript,card):
# Check the autoscript for special restrictions on the originator of a specific effect. 
# If the card does not validate all the restrictions included in the autoscript, we reject it
# For example Darth Vader 41/2 requires that he is attacking before his effect takes place. In this case we'd check that he is currently attacking and return True is he is
   if debugVerbosity >= 1: notify(">>> checkOriginatorRestrictions() {}".format(extraASDebug(Autoscript))) #Debug
   if debugVerbosity >= 1: notify("### Card: {}".format(card)) #Debug
   validCard = True
   if re.search(r'ifOrigCurrentObjective',Autoscript) and card.highlight != DefendColor: validCard = False
   if re.search(r'ifOrigParticipating',Autoscript) and card.orientation != Rot90 and card.highlight != DefendColor: validCard = False
   if re.search(r'ifOrigNotParticipating',Autoscript) and (card.orientation == Rot90 or card.highlight == DefendColor): validCard = False
   if re.search(r'ifOrigAttacking',Autoscript) or re.search(r'ifOrigDefending',Autoscript):
      EngagedObjective = getGlobalVariable('Engaged Objective')
      if EngagedObjective == 'None': validCard = False
      else:
         currentTarget = Card(num(EngagedObjective))
         if re.search(r'ifOrigAttacking',Autoscript) and currentTarget.controller == card.controller: validCard = False
         elif re.search(r'ifOrigDefending',Autoscript)  and currentTarget.controller != card.controller: validCard = False
   if re.search(r'ifOrigCommited',Autoscript) and card.highlight != LightForceColor and card.highlight != DarkForceColor: validCard = False
   if not chkPlayer(Autoscript, card.controller, False, True): validCard = False
   markerName = re.search(r'-ifOrigHasMarker{([\w :]+)}',Autoscript) # Checking if we need specific markers on the card.
   if markerName: #If we're looking for markers, then we go through each targeted card and check if it has any relevant markers
      if debugVerbosity >= 2: notify("### Checking marker restrictions")# Debug
      if debugVerbosity >= 2: notify("### Marker Name: {}".format(markerName.group(1)))# Debug
      marker = findMarker(card, markerName.group(1))
      if not marker: validCard = False
   markerNeg = re.search(r'-ifOrigHasntMarker{([\w ]+)}',Autoscript) # Checking if we need to not have specific markers on the card.
   if markerNeg: #If we're looking for markers, then we go through each targeted card and check if it has any relevant markers
      if debugVerbosity >= 2: notify("### Checking negative marker restrictions")# Debug
      if debugVerbosity >= 2: notify("### Marker Name: {}".format(markerNeg.group(1)))# Debug
      marker = findMarker(card, markerNeg.group(1))
      if marker: validCard = False
   elif debugVerbosity >= 4: notify("### No negative marker restrictions.")
   # Checking if the originator needs to have a property at a certiain value. 
   propertyReq = re.search(r'-ifOrigHasProperty{([\w ]+)}(eq|le|ge|gt|lt)([0-9])',Autoscript) 
   if propertyReq: validCard = compareValue(propertyReq.group(2), num(card.properties[propertyReq.group(1)]), num(propertyReq.group(3)))
   # Checking if the target needs to have a markers at a particular value.
   MarkerReq = re.search(r'-ifOrigmarkers{([\w ]+)}(eq|le|ge|gt|lt)([0-9])',Autoscript)
   if MarkerReq: validCard = compareValue(MarkerReq.group(2), card.markers.get(findMarker(card, MarkerReq.group(1)),0), num(MarkerReq.group(3)))
   # Checking if the DS Dial needs to be at a specific value
   DialReq = re.search(r'-ifDial(eq|le|ge|gt|lt)([0-9]+)',Autoscript)
   if DialReq: validCard = compareValue(DialReq.group(1), me.counters['Death Star Dial'].value, num(DialReq.group(2)))
   if debugVerbosity >= 1: notify("<<< checkOriginatorRestrictions() with return {}".format(validCard)) #Debug
   return validCard
   
def compareValue(comparison, value, requirement):
   debugNotify(">>> compareValue()")
   if comparison == 'eq' and value != requirement: return False # 'eq' stands for "Equal to"
   if comparison == 'le' and value > requirement: return False # 'le' stands for "Less or Equal"
   if comparison == 'ge' and value < requirement: return False # 'ge' stands for "Greater or Equal"
   if comparison == 'lt' and value >= requirement: return False # 'lt' stands for "Less Than"
   if comparison == 'gt' and value <= requirement: return False # 'gt' stands for "Greater Than"
   debugNotify("<<< compareValue() with return True")
   return True # If none of the requirements fail, we return true
     
def makeChoiceListfromCardList(cardList,includeText = False):
# A function that returns a list of strings suitable for a choice menu, out of a list of cards
# Each member of the list includes a card's name, traits, resources, markers and, if applicable, combat icons
   if debugVerbosity >= 1: notify(">>> makeChoiceListfromCardList()")
   targetChoices = []
   if debugVerbosity >= 2: notify("### About to prepare choices list.")# Debug
   for T in cardList:
      if debugVerbosity >= 4: notify("### Checking {}".format(T))# Debug
      markers = 'Counters:'
      if T.markers[mdict['Damage']] and T.markers[mdict['Damage']] >= 1: markers += " {} Damage,".format(T.markers[mdict['Damage']])
      if T.markers[mdict['Focus']] and T.markers[mdict['Focus']] >= 1: markers += " {} Focus,".format(T.markers[mdict['Focus']])
      if T.markers[mdict['Shield']] and T.markers[mdict['Shield']] >= 1: markers += " {} Shield.".format(T.markers[mdict['Shield']])
      if markers != 'Counters:': markers += '\n'
      else: markers = ''
      if debugVerbosity >= 4: notify("### Finished Adding Markers. Adding stats...")# Debug               
      stats = ''
      if num(T.Resources) >= 1: stats += "Resources: {}. ".format(T.Resources)
      if num(T.properties['Damage Capacity']) >= 1: stats += "HP: {}.".format(T.properties['Damage Capacity'])
      if T.Type == 'Unit': combatIcons = "Printed Icons: " + parseCombatIcons(T.properties['Combat Icons'])
      else: combatIcons = ''
      if includeText: cText = '\n' + fetchProperty(T, 'Text')
      else: cText = ''
      if debugVerbosity >= 4: notify("### Finished Adding Stats. Going to choice...")# Debug               
      choiceTXT = "{}\n{}\n{}{}\n{}\nBlock: {}{}".format(T.name,T.Type,markers,stats,combatIcons,T.Block,cText)
      targetChoices.append(choiceTXT)
   return targetChoices
   if debugVerbosity >= 3: notify("<<< makeChoiceListfromCardList()")

   
def chkPlayer(Autoscript, controller, manual, targetChk = False): # Function for figuring out if an autoscript is supposed to target an opponent's cards or ours.
# Function returns 1 if the card is not only for rivals, or if it is for rivals and the card being activated it not ours.
# This is then multiplied by the multiplier, which means that if the card activated only works for Rival's cards, our cards will have a 0 gain.
# This will probably make no sense when I read it in 10 years...
   if debugVerbosity >= 1: notify(">>> chkPlayer(). Controller is: {}".format(controller)) #Debug
   try:
      if targetChk: # If set to true, it means we're checking from the findTarget() function, which needs a different keyword in case we end up with two checks on a card's controller on the same script (e.g. Darth Vader)
         byOpponent = re.search(r'targetOpponents', Autoscript)
         byMe = re.search(r'targetMine', Autoscript)
      else:
         byOpponent = re.search(r'(byOpponent|duringOpponentTurn|forOpponent)', Autoscript)
         byMe = re.search(r'(byMe|duringMyTurn|forMe)', Autoscript)
      if manual or len(players) == 1: # If there's only one player, we always return true for debug purposes.
         if debugVerbosity >= 2: notify("### Succeeded at Manual/Debug")
         validPlayer = 1 #manual means that the clicks was called by a player double clicking on the card. In which case we always do it.
      elif not byOpponent and not byMe: 
         if debugVerbosity >= 2: notify("### Succeeded at Neutral")   
         validPlayer = 1 # If the card has no restrictions on being us or a rival.
      elif byOpponent and controller != me: 
         if debugVerbosity >= 2: notify("### Succeeded at byOpponent")   
         validPlayer =  1 # If the card needs to be played by a rival.
      elif byMe and controller == me: 
         if debugVerbosity >= 2: notify("### Succeeded at byMe")   
         validPlayer =  1 # If the card needs to be played by us.
      else: 
         if debugVerbosity >= 2: notify("### Failed all checks") # Debug
         validPlayer =  0 # If all the above fail, it means that we're not supposed to be triggering, so we'll return 0 whic
      if not reversePlayerChk: 
         if debugVerbosity >= 3: notify("<<< chkPlayer() with validPlayer") # Debug
         return validPlayer
      else: # In case reversePlayerChk is set to true, we want to return the opposite result. This means that if a scripts expect the one running the effect to be the player, we'll return 1 only if the one running the effect is the opponent. See Decoy at Dantoine for a reason
         if debugVerbosity >= 3: notify("<<< chkPlayer() reversed!") # Debug      
         if validPlayer == 0 or len(players) == 1 or manual or (not byOpponent and not byMe): return 1 # For debug purposes, I want it to be true when there's  only one player in the match
         else: return 0
   except: 
      notify("!!!ERROR!!! Null value on chkPlayer()")
      return 0

def chkWarn(card, Autoscript): # Function for checking that an autoscript announces a warning to the player
   if debugVerbosity >= 1: notify(">>> chkWarn(){}".format(extraASDebug(Autoscript))) #Debug
   global AfterRunInf, AfterTraceInf
   warning = re.search(r'warn([A-Z][A-Za-z0-9 ]+)-?', Autoscript)
   if warning:
      if warning.group(1) == 'Discard': 
         if not confirm("This action requires that you discard some cards. Have you done this already?"):
            whisper(":> Aborting action. Please discard the necessary amount of cards and run this action again")
            return 'ABORT'
      if warning.group(1) == 'ReshuffleOpponent': 
         if not confirm("This action will reshuffle your opponent's pile(s). Are you sure?\n\n[Important: Please ask your opponent not to take any clicks with their piles until this clicks is complete or the game might crash]"):
            whisper(":> Aborting action.")
            return 'ABORT'
      if warning.group(1) == 'GiveToOpponent': confirm('This card has an effect which if meant for your opponent. Please use the menu option "pass control to" to give them control.')
      if warning.group(1) == 'Reshuffle': 
         if not confirm("This action will reshuffle your piles. Are you sure?"):
            whisper(":> Aborting action.")
            return 'ABORT'
      if warning.group(1) == 'Workaround':
         notify(":::Note:::{} is using a workaround autoscript".format(me))
      if warning.group(1) == 'LotsofStuff': 
         if not confirm("This card modify the cards on the table significantly and very difficult to undo. Are you ready to proceed?"):
            whisper(":> Aborting action.")
            return 'ABORT'
   if debugVerbosity >= 3: notify("<<< chkWarn() gracefully") 
   return 'OK'

def per(Autoscript, card = None, count = 0, targetCards = None, notification = None): # This function goes through the autoscript and looks for the words "per<Something>". Then figures out what the card multiplies its effect with, and returns the appropriate multiplier.
   if debugVerbosity >= 1: notify(">>> per(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   div = 1
   ignore = 0
   per = re.search(r'\b(per|upto)(Target|Parent|Every)?([A-Z][^-]*)-?', Autoscript) # We're searching for the word per, and grabbing all after that, until the first dash "-" as the variable.   
   if per: # If the  search was successful...
      multiplier = 0
      if debugVerbosity >= 2: notify("Groups: {}. Count: {}".format(per.groups(),count)) #Debug
      if per.group(2) and (per.group(2) == 'Target' or per.group(2) == 'Every'): # If we're looking for a target or any specific type of card, we need to scour the requested group for targets.
         if debugVerbosity >= 2: notify("Checking for Targeted per")
         if per.group(2) == 'Target' and len(targetCards) == 0: 
            delayed_whisper(":::ERROR::: Script expected a card targeted but found none! Exiting with 0 multiplier.")
            # If we were expecting a target card and we have none we shouldn't even be in here. But in any case, we return a multiplier of 0
         elif per.group(2) == 'Every' and len(targetCards) == 0: pass #If we looking for a number of cards and we found none, then obviously we return 0
         else:
            if per.group(2) == 'Host': 
               if debugVerbosity >= 2: notify("Checking for perHost")
               hostCards = eval(getGlobalVariable('Host Cards'))
               hostID = hostCards.get(card._id,None)
               if hostID: # If we do not have a parent, then we do nothing and return 0
                  targetCards = [Card(hostID)] # if we have a host, we make him the only one in the list of cards to process.
            for perCard in targetCards:
               if not checkSpecialRestrictions(Autoscript,perCard): continue
               if debugVerbosity >= 2: notify("perCard = {}".format(perCard))
               if re.search(r'Marker',per.group(3)):
                  markerName = re.search(r'Marker{([\w :]+)}',per.group(3)) # I don't understand why I had to make the curly brackets optional, but it seens atTurnStart/End completely eats them when it parses the CardsAS.get(card.model,'')
                  marker = findMarker(perCard, markerName.group(1))
                  if marker: multiplier += perCard.markers[marker]
               elif re.search(r'Property',per.group(3)):
                  property = re.search(r'Property{([\w ]+)}',per.group(3))
                  multiplier += num(perCard.properties[property.group(1)])
               else: multiplier += 1 # If there's no special conditions, then we just add one multiplier per valid (auto)target. Ef. "-perEvery-AutoTargeted-onICE" would give 1 multiplier per ICE on the table
         if per.group(2) == 'Every': # If we're checking every card of a specific trait, we may have cards that give bonus to that amount (e.g. Echo base), so we look for those bonuses now.
            for c in table: # We check for cards for give bonus objective traits (e.g. Echo Base)
               Autoscripts = CardsAS.get(c.model,'').split('||')
               for autoS in Autoscripts:
                  if debugVerbosity >= 2: notify("### Checking {} for Objective Trait boosting AS: {}".format(c,autoS))
                  TraitRegex = re.search(r'Trait\{([A-Za-z_ ]+)\}([0-9])Bonus',autoS)
                  if TraitRegex: 
                     if debugVerbosity >= 3: notify("TraitRegex found. Groups = {}".format(TraitRegex.groups()))
                     TraitsList = TraitRegex.group(1).split('_and_') # We make a list of all the traits the bonus effect of the cardprovides
                     if debugVerbosity >= 4: notify("### TraitsList = {}".format(TraitsList)) 
                     TraitsRestrictions = prepareRestrictions(Autoscript) # Then we gather the trait restrictions the original effect was looking for
                     if debugVerbosity >= 4: notify("### TraitsRestrictions = {}".format(TraitsRestrictions))
                     if checkCardRestrictions(TraitsList, TraitsRestrictions) and checkSpecialRestrictions(Autoscript,c): # Finally we compare the bonus traits of the card we found, wit  h the traits the original effect was polling for.
                        multiplier += num(TraitRegex.group(2)) * chkPlayer(autoS, c.controller, False, True) # If they match, we increase our multiplier by the relevant number, if the card has the appropriate controller according to its effect.
      else: #If we're not looking for a particular target, then we check for everything else.
         if debugVerbosity >= 2: notify("### Doing no table lookup") # Debug.
         if per.group(3) == 'X': multiplier = count # Probably not needed and the next elif can handle alone anyway.
         elif count: multiplier = num(count) * chkPlayer(Autoscript, card.controller, False) # All non-special-rules per<somcething> requests use this formula.
                                                                                              # Usually there is a count sent to this function (eg, number of favour purchased) with which to multiply the end result with
                                                                                              # and some cards may only work when a rival owns or does something.
         elif re.search(r'Marker',per.group(3)):
            markerName = re.search(r'Marker{([\w :]+)}',per.group(3)) # I don't understand why I had to make the curly brackets optional, but it seens atTurnStart/End completely eats them when it parses the CardsAS.get(card.model,'')
            marker = findMarker(card, markerName.group(1))
            if marker: multiplier = card.markers[marker]
            else: multiplier = 0
         elif re.search(r'Property',per.group(3)):
            property = re.search(r'Property{([\w ]+)}',per.group(3))
            multiplier = card.properties[property.group(1)]
      if debugVerbosity >= 2: notify("### Checking ignore") # Debug.            
      ignS = re.search(r'-ignore([0-9]+)',Autoscript)
      if ignS: ignore = num(ignS.group(1))
      if debugVerbosity >= 2: notify("### Checking div") # Debug.            
      divS = re.search(r'-div([0-9]+)',Autoscript)
      if divS: div = num(divS.group(1))
   else: multiplier = 1
   if debugVerbosity >= 2: notify("<<< per() with Multiplier: {}".format((multiplier - ignore) / div)) # Debug
   return (multiplier - ignore) / div
   