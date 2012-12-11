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
#------------------------------------------------------------------------------
# Play/Score/Rez/Trash trigger
#------------------------------------------------------------------------------

def executePlayScripts(card, action):
   #action = action.upper() # Just in case we passed the wrong case
   if debugVerbosity >= 1: notify(">>> executePlayScripts() with action: {}".format(action)) #Debug
   global failedRequirement
   if not Automations['Play']: return
   if not card.isFaceUp: return
   if CardsAS.get(card.model,'') == '': return
   if card.highlight == CapturedColor or card.highlight == EdgeColor or card.highlight == UnpaidColor: return
   failedRequirement = False
   X = 0
   Autoscripts = CardsAS.get(card.model,'').split('||') # When playing cards, the || is used as an "and" separator, rather than "or". i.e. we don't do choices (yet)
   AutoScriptsSnapshot = list(Autoscripts) # Need to work on a snapshot, because we'll be modifying the list.
   for autoS in AutoScriptsSnapshot: # Checking and removing any "AtTurnStart" clicks.
      if (re.search(r'atTurn(Start|End)', autoS) or 
          re.search(r'after([A-za-z]+)', autoS) or 
          re.search(r'ConstantEffect', autoS) or 
          re.search(r'onPay', autoS) or # onPay effects are only useful before we go to the autoscripts, for the cost reduction.
          re.search(r'-isTrigger', autoS)): Autoscripts.remove(autoS)
      elif re.search(r'excludeDummy', autoS) and card.highlight == DummyColor: Autoscripts.remove(autoS)
      elif re.search(r'onlyforDummy', autoS) and card.highlight != DummyColor: Autoscripts.remove(autoS)
      elif re.search(r'CustomScript', autoS): 
         CustomScript(card,action)
         Autoscripts.remove(autoS)
   if len(Autoscripts) == 0: return
   for AutoS in Autoscripts:
      if debugVerbosity >= 2: notify("### First Processing: {}".format(AutoS)) # Debug
      effectType = re.search(r'(on[A-Za-z]+|while[A-Za-z]+):', AutoS) 
      if ((effectType.group(1) == 'onPlay' and action != 'PLAY') or 
          (effectType.group(1) == 'onScore' and action != 'SCORE') or
          (effectType.group(1) == 'onStrike' and action != 'STRIKE') or
          (effectType.group(1) == 'onDamage' and action != 'DAMAGE') or
          (effectType.group(1) == 'onDefense' and action != 'DEFENSE') or
          (effectType.group(1) == 'onAttack' and action != 'ATTACK') or
          (effectType.group(1) == 'onDiscard' and action != 'DISCARD') or
          (effectType.group(1) == 'onCommit' and action != 'COMMIT') or
          (effectType.group(1) == 'onThwart' and action != 'THWART')): continue 
      if re.search(r'-onlyDuringEngagement', AutoS) and getGlobalVariable('Engaged Objective') == 'None': 
         return 'ABORT' # If this is an optional ability only for engagements, then we abort
      if re.search(r'-isOptional', AutoS):
         if not confirm("This card has an optional ability you can activate at this point. Do you want to do so?"): 
            notify("{} opts not to activate {}'s optional ability".format(me,card))
            return 'ABORT'
         else: notify("{} activates {}'s optional ability".format(me,card))
      selectedAutoscripts = AutoS.split('$$')
      if debugVerbosity >= 2: notify ('### selectedAutoscripts: {}'.format(selectedAutoscripts)) # Debug
      for activeAutoscript in selectedAutoscripts:
         if debugVerbosity >= 2: notify("### Second Processing: {}".format(activeAutoscript)) # Debug
         #if chkWarn(card, activeAutoscript) == 'ABORT': return
         if re.search(r':Pass\b', activeAutoscript): return # Pass is a simple command of doing nothing ^_^
         effect = re.search(r'\b([A-Z][A-Za-z]+)([0-9]*)([A-Za-z& ]*)\b([^:]?[A-Za-z0-9_&{}\|: -]*)', activeAutoscript)
         if debugVerbosity >= 2: notify('### effects: {}'.format(effect.groups())) #Debug
         if effectType.group(1) == 'whilePlayed' or effectType.group(1) == 'whileScored':
            if effect.group(1) != 'Gain' and effect.group(1) != 'Lose': continue # The only things that whileRezzed and whileScored affect in execute Automations is GainX scripts (for now). All else is onTrash, onPlay etc
            if action == 'TRASH': Removal = True
            else: Removal = False
         elif action == 'TRASH': return # If it's just a one-off event, and we're trashing it, then do nothing.
         else: Removal = False
         targetC = findTarget(activeAutoscript)
         targetPL = ofwhom(activeAutoscript,card.controller) # So that we know to announce the right person the effect, affects.
         announceText = "{}".format(targetPL)
         if debugVerbosity >= 3: notify("#### targetC: {}".format(targetC)) # Debug
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
               if CreateDummy(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            elif regexHooks['DrawX'].search(passedScript): 
               if DrawX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            elif regexHooks['TokensX'].search(passedScript): 
               if TokensX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            elif regexHooks['RollX'].search(passedScript): 
               rollTuple = RollX(passedScript, announceText, card, targetC, notification = 'Quick', n = X)
               if rollTuple == 'ABORT': return
               X = rollTuple[1] 
            elif regexHooks['RequestInt'].search(passedScript): 
               numberTuple = RequestInt(passedScript, announceText, card, targetC, notification = 'Quick', n = X)
               if numberTuple == 'ABORT': return
               X = numberTuple[1] 
            elif regexHooks['DiscardX'].search(passedScript): 
               discardTuple = DiscardX(passedScript, announceText, card, targetC, notification = 'Quick', n = X)
               if discardTuple == 'ABORT': return
               X = discardTuple[1] 
            elif regexHooks['ReshuffleX'].search(passedScript): 
               reshuffleTuple = ReshuffleX(passedScript, announceText, card, targetC, notification = 'Quick', n = X)
               if reshuffleTuple == 'ABORT': return
               X = reshuffleTuple[1]
            elif regexHooks['ShuffleX'].search(passedScript): 
               if ShuffleX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            elif regexHooks['ChooseKeyword'].search(passedScript): 
               if ChooseKeyword(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            elif regexHooks['InflictX'].search(passedScript): 
               if InflictX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            elif regexHooks['ModifyStatus'].search(passedScript): 
               if ModifyStatus(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
         if failedRequirement: break # If one of the Autoscripts was a cost that couldn't be paid, stop everything else.
         if debugVerbosity >= 2: notify("Loop for scipt {} finished".format(passedScript))

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
      if debugVerbosity >= 2: notify('Checking {}'.format(card)) # Debug
      if not card.isFaceUp: continue # Don't take into accounts cards that are face down for some reason. 
      if card.highlight == CapturedColor or card.highlight == EdgeColor or card.highlight == FateColor or card.highlight == UnpaidColor: return # We do not care about inactive cards.
      costText = '{} activates {} to'.format(card.controller, card) 
      Autoscripts = CardsAS.get(card.model,'').split('||')
      if debugVerbosity >= 4: notify("### {}'s AS: {}".format(card,Autoscripts)) # Debug
      AutoScriptSnapshot = list(Autoscripts)
      for autoS in AutoScriptSnapshot: # Checking and removing anything other than whileRezzed or whileScored.
         if not re.search(r'while(Played|Scored)', autoS): Autoscripts.remove(autoS)
      if len(Autoscripts) == 0: continue
      for AutoS in Autoscripts:
         if debugVerbosity >= 2: notify('Checking AutoS: {}'.format(AutoS)) # Debug
         if not re.search(r'{}'.format(lookup), AutoS): continue # Search if in the script of the card, the string that was sent to us exists. The sent string is decided by the function calling us, so for example the ProdX() function knows it only needs to send the 'GeneratedSpice' string.
         if chkPlayer(AutoS, card.controller,False) == 0: continue # Check that the effect's origninator is valid.
         if re.search(r'onlyOnce',autoS) and oncePerTurn(card, silent = True, act = 'automatic') == 'ABORT': continue # If the card's ability is only once per turn, use it or silently abort if it's already been used
         chkType = re.search(r'-type([A-Za-z ]+)',autoS)
         if chkType: #If we have this modulator in the script, then need ot check what type of property it's looking for
            if debugVerbosity >= 4: notify("### Looking for : {}".format(chkType.group(1)))
            cardProperties = []
            del cardProperties [:] # Just in case
            cardProperties.append(origin_card.Type) # Its type
            cardSubtypes = getKeywords(origin_card).split('-') # And each individual trait. Traits are separated by " - "
            for cardSubtype in cardSubtypes:
               strippedCS = cardSubtype.strip() # Remove any leading/trailing spaces between traits. We need to use a new variable, because we can't modify the loop iterator.
               if strippedCS: cardProperties.append(strippedCS) # If there's anything left after the stip (i.e. it's not an empty string anymrore) add it to the list.
            cardProperties.append(origin_card.Side) # We are also going to check if the card is for runner or corp.
            if debugVerbosity >= 4: notify("### card Properies: {}".format(cardProperties))
            if not chkType.group(1) in cardProperties: continue 
         if re.search(r'onTriggerCard',autoS): targetCard = [origin_card] # if we have the "-onTriggerCard" modulator, then the target of the script will be the original card (e.g. see Grimoire)
         else: targetCard = None
         if debugVerbosity >= 2: notify("### Automatic Autoscripts: {}".format(AutoS)) # Debug
         #effect = re.search(r'\b([A-Z][A-Za-z]+)([0-9]*)([A-Za-z& ]*)\b([^:]?[A-Za-z0-9_&{} -]*)', AutoS)
         #passedScript = "{}".format(effect.group(0))
         #confirm('effects: {}'.format(passedScript)) #Debug
         if regexHooks['GainX'].search(AutoS):
            gainTuple = GainX(AutoS, costText, card, targetCard, notification = 'Automatic', n = count)
            if gainTuple == 'ABORT': break
         elif regexHooks['TokensX'].search(AutoS): 
            if TokensX(AutoS, costText, card, targetCard, notification = 'Automatic', n = count) == 'ABORT': break
         elif regexHooks['DrawX'].search(AutoS):
            if DrawX(AutoS, costText, card, targetCard, notification = 'Automatic', n = count) == 'ABORT': break
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
      if card.highlight == CapturedColor or card.highlight == EdgeColor or card.highlight == UnpaidColor: return # We do not care about inactive cards.
      if not card.isFaceUp: continue
      Autoscripts = CardsAS.get(card.model,'').split('||')
      for autoS in Autoscripts:
         if debugVerbosity >= 3: notify("### Processing {} Autoscript: {}".format(card, autoS))
         if re.search(r'after([A-za-z]+)',Time): effect = re.search(r'(after[A-za-z]+):(.*)', autoS) # Putting Run in a group, only to retain the search results groupings later
         else: effect = re.search(r'atTurn(Start|End):(.*)', autoS) #Putting "Start" or "End" in a group to compare with the Time variable later
         if not effect: continue
         if debugVerbosity >= 3: notify("### Time maches. Script triggers on: {}".format(effect.group(1)))
         if chkPlayer(effect.group(2), card.controller,False) == 0: continue # Check that the effect's origninator is valid. 
         if effect.group(1) != Time: continue # If the effect trigger we're checking (e.g. start-of-run) does not match the period trigger we're in (e.g. end-of-turn)
         if debugVerbosity >= 3: notify("### split Autoscript: {}".format(autoS))
         if debugVerbosity >= 2 and effect: notify("!!! effects: {}".format(effect.groups()))
         if re.search(r'excludeDummy', autoS) and card.highlight == DummyColor: continue
         if re.search(r'onlyforDummy', autoS) and card.highlight != DummyColor: continue
         if re.search(r'isOptional', effect.group(2)):
            extraCountersTXT = '' 
            for cmarker in card.markers: # If the card has any markers, we mention them do that the player can better decide which one they wanted to use (e.g. multiple bank jobs)
               extraCountersTXT += " {}x {}\n".format(card.markers[cmarker],cmarker[0])
            if extraCountersTXT != '': extraCountersTXT = "\n\nThis card has the following counters on it\n" + extraCountersTXT
            if not confirm("{} can have its optional ability take effect at this point. Do you want to activate it?{}".format(fetchProperty(card, 'name'),extraCountersTXT)): continue         
         if re.search(r'onlyOnce',autoS) and oncePerTurn(card, silent = True, act = 'automatic') == 'ABORT': continue
         splitAutoscripts = effect.group(2).split('$$')
         for passedScript in splitAutoscripts:
            targetC = findTarget(passedScript, card = card)
            if not TitleDone and not (len(targetC) == 0 and re.search(r'AutoTargeted',passedScript)): # We don't want to put a title if we have a card effect that activates only if we have some valid targets (e.g. Admiral Motti)
               if re.search(r'after([A-za-z]+)',Time): 
                  Phase = re.search(r'after([A-za-z]+)',Time)
                  title = "{}'s Post-{} Effects".format(me,Phase.group(1))
               else: title = "{}'s {}-of-Turn Effects".format(me,effect.group(1))
               notify("{:=^36}".format(title))
               TitleDone = True
            if debugVerbosity >= 2: notify("### passedScript: {}".format(passedScript))
            if card.highlight == DummyColor: announceText = "{}'s lingering effects:".format(card)
            else: announceText = "{}:".format(card)
            if regexHooks['GainX'].search(passedScript):
               gainTuple = GainX(passedScript, announceText, card, targetC, notification = 'Automatic', n = X)
               if gainTuple == 'ABORT': break
               X = gainTuple[1] 
            elif regexHooks['DrawX'].search(passedScript):
               if debugVerbosity >= 2: notify("### About to DrawX()")
               if DrawX(passedScript, announceText, card, targetC, notification = 'Automatic', n = X) == 'ABORT': break
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
            elif regexHooks['CustomScript'].search(passedScript):
               if CustomScript(card, action = 'Turn{}'.format(Time)) == 'ABORT': break
            if failedRequirement: break # If one of the Autoscripts was a cost that couldn't be paid, stop everything else.
   #markerEffects(Time) 
   if TitleDone: notify(":::{:=^30}:::".format('='))   
   if debugVerbosity >= 3: notify("<<< atTimedEffects()") # Debug

def markerEffects(Time = 'Start'):
   if debugVerbosity >= 1: notify(">>> markerEffects() at time: {}".format(Time)) #Debug
### Following is not yet implemented. It's from Netrunner classic. Commented out just in case I need it.
#   CounterHold = getSpecial('Identity')
   ### Checking triggers from markers in our own Counter Hold.
#   for marker in CounterHold.markers: # Not used in ANR (yet)
#      count = CounterHold.markers[marker]
#      if debugVerbosity >= 3: notify("### marker: {}".format(marker[0])) # Debug
#      if re.search(r'virusScaldan',marker[0]) and Time == 'Start':
#         total = 0
#         for iter in range(count):
#            rollTuple = RollX('Roll1Dice', 'Scaldan virus:', CounterHold, notification = 'Automatic')
#            if rollTuple[1] >= 5: total += 1
#         me.counters['Bad Publicity'].value += total
#         if total: notify("--> {} receives {} Bad Publicity due to their Scaldan virus infestation".format(me,total))
#      if re.search(r'virusSkivviss',marker[0]) and Time == 'Start':
#         passedScript = 'Draw{}Cards'.format(count)
#         DrawX(passedScript, "Skivviss virus:", CounterHold, notification = 'Automatic')
#      if re.search(r'virusTax',marker[0]) and Time == 'Start':
#         GainX('Lose1Credits-perMarker{virusTax}-div2', "Tax virus:", CounterHold, notification = 'Automatic')
#      if re.search(r'Doppelganger',marker[0]) and Time == 'Start':
#         GainX('Lose1Credits-perMarker{Doppelganger}', "{}:".format(marker[0]), CounterHold, notification = 'Automatic')
#      if re.search(r'virusPipe',marker[0]) and Time == 'Start':
#         passedScript = 'Infect{}forfeitCounter:Clicks'.format(count)
#         TokensX(passedScript, "Pipe virus:", CounterHold, notification = 'Automatic')
#      if re.search(r'Data Raven',marker[0]) and Time == 'Start':
#         GainX('Gain1Tags-perMarker{Data Raven}', "{}:".format(marker[0]), CounterHold, notification = 'Automatic')
#      if re.search(r'Mastiff',marker[0]) and Time == 'Run':
#         InflictX('Inflict1BrainDamage-perMarker{Mastiff}', "{}:".format(marker[0]), CounterHold, notification = 'Automatic')
#      if re.search(r'Cerberus',marker[0]) and Time == 'Run':
#         InflictX('Inflict2NetDamage-perMarker{Cerberus}', "{}:".format(marker[0]), CounterHold, notification = 'Automatic')
#      if re.search(r'Baskerville',marker[0]) and Time == 'Run':
#         InflictX('Inflict2NetDamage-perMarker{Baskerville}', "{}:".format(marker[0]), CounterHold, notification = 'Automatic')
#   targetPL = ofwhom('-ofOpponent')          
   ### Checking triggers from markers in opponent's Counter Hold.
#   CounterHold = getSpecial('Identity', targetPL) # Some viruses also trigger on our opponent's turns
#   for marker in CounterHold.markers:
#      count = CounterHold.markers[marker]
#      if marker == mdict['virusButcherBoy'] and Time == 'Start':
#         GainX('Gain1Credits-onOpponent-perMarker{virusButcherBoy}-div2', "Opponent's Butcher Boy virus:", OpponentCounterHold, notification = 'Automatic')
   ### Checking triggers from markers the rest of our cards.
   
   
#------------------------------------------------------------------------------
# Core Commands
#------------------------------------------------------------------------------
   
def GainX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0, actionType = 'USE'): # Core Command for modifying counters or global variables
   if debugVerbosity >= 1: notify(">>> GainX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   gain = 0
   extraTXT = ''
   reduction = 0
   action = re.search(r'\b(Gain|Lose|SetTo)([0-9]+)([A-Z][A-Za-z &]+)-?', Autoscript)
   if debugVerbosity >= 2: notify("### action groups: {}. Autoscript: {}".format(action.groups(0),Autoscript)) # Debug
   gain += num(action.group(2))
   targetPL = ofwhom(Autoscript, card.controller)
   if targetPL != me and not notification: otherTXT = ' force {} to'.format(targetPL)
   else: otherTXT = ''
   multiplier = per(Autoscript, card, n, targetCards) # We check if the card provides a gain based on something else, such as favour bought, or number of dune fiefs controlled by rivals.
   if debugVerbosity >= 3: notify("### GainX() after per") #Debug
   gainReduce = findCounterPrevention(gain * multiplier, action.group(3), targetPL) # If we're going to gain counter, then we check to see if we have any markers which might reduce the cost.
   #confirm("multiplier: {}, gain: {}, reduction: {}".format(multiplier, gain, gainReduce)) # Debug
   if re.match(r'Reserves', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.counters['Reserves'].value = 0 # If we're setting to a specific value, we wipe what it's currently.
      targetPL.counters['Reserves'].value += gain * multiplier
      if targetPL.counters['Reserves'].value < 0: targetPL.counters['Reserves'].value = 0
   else: 
      whisper("Gain what?! (Bad autoscript)")
      return 'ABORT'
   if debugVerbosity >= 2: notify("### Gainx() Finished counter manipulation")
   if notification != 'Automatic': # Since the verb is in the middle of the sentence, we want it lowercase.
      if action.group(1) == 'Gain': verb = 'gain'
      elif action.group(1) == 'Lose': 
         if re.search(r'isCost', Autoscript): verb = 'pay'
         else: verb = 'lose'
      else: verb = 'set to'
      if notification == 'Quick':
         if verb == 'gain' or verb == 'lose' or verb == 'pay': verb += 's'
         else: verb = 'sets to'      
   else: verb = action.group(1) # Automatic notifications start with the verb, so it needs to be capitaliszed. 
   if abs(gain) == abs(999): total = 'all' # If we have +/-999 as the count, then this mean "all" of the particular counter.
   elif action.group(1) == 'Lose' and not re.search(r'isPenalty', Autoscript): total = abs(gain * multiplier) - overcharge
   else: total = abs(gain * multiplier) - reduction# Else it's just the absolute value which we announce they "gain" or "lose"
   closureTXT = ASclosureTXT(action.group(3), total)
   if debugVerbosity >= 2: notify("### Gainx() about to announce")
   if notification == 'Quick': announceString = "{}{} {} {}{}".format(announceText, otherTXT, verb, closureTXT,extraTXT)
   else: announceString = "{}{} {} {}{}".format(announceText, otherTXT, verb, closureTXT,extraTXT)
   if notification and multiplier > 0: notify(':> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< Gain() total: {}".format(total))
   return (announceString,total)
   
def TokensX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for adding tokens to cards
   if debugVerbosity >= 1: notify(">>> TokensX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   if len(targetCards) == 0:
      targetCards.append(card) # If there's been to target card given, assume the target is the card itself.
      targetCardlist = ' on it' 
   else:
      targetCardlist = ' on' # A text field holding which cards are going to get tokens.
      for targetCard in targetCards:
         targetCardlist += ' {},'.format(targetCard)
   #confirm("TokensX List: {}".format(targetCardlist)) # Debug
   foundKey = False # We use this to see if the marker used in the AutoAction is already defined.
   infectTXT = '' # We only inject this into the announcement when this is an infect AutoAction.
   preventTXT = '' # Again for virus infections, to note down how much was prevented.
   action = re.search(r'\b(Put|Remove|Refill|Use|Infect|Deal)([0-9]+)([A-Za-z: ]+)-?', Autoscript)
   #confirm("{}".format(action.group(3))) # Debug
   if action.group(3) in mdict: token = mdict[action.group(3)]
   else: # If the marker we're looking for it not defined, then either create a new one with a random color, or look for a token with the custom name we used above.
      if action.group(1) == 'Infect': 
         victim = ofwhom(Autoscript, card.controller)
         if targetCards[0] == card: targetCards[0] = getSpecial('Identity',victim)
      if targetCards[0].markers:
         for key in targetCards[0].markers:
            #confirm("Key: {}\n\naction.group(3): {}".format(key[0],action.group(3))) # Debug
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
      #confirm("TargetCard ID: {}".format(targetCard._id)) # Debug
      if action.group(1) == 'Put' or action.group(1) == 'Deal': modtokens = count * multiplier
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
         if count == 999: # 999 effectively means "all markers on card"
            if targetCard.markers[token]: count = targetCard.markers[token]
            else: 
               whisper("There was nothing to remove.")
               count = 0
         elif re.search(r'isCost', Autoscript) and (not targetCard.markers[token] or (targetCard.markers[token] and count > targetCard.markers[token])):
            if notification != 'Automatic': whisper ("No markers to remove. Aborting!") #Some end of turn effect put a special counter and then remove it so that they only run for one turn. This avoids us announcing that it doesn't have markers every turn.
            return 'ABORT'
         elif not targetCard.markers[token]: 
            whisper("There was nothing to remove.")        
            count = 0 # If we don't have any markers, we have obviously nothing to remove.
         modtokens = -count * multiplier
      targetCard.markers[token] += modtokens # Finally we apply the marker modification
   if abs(num(action.group(2))) == abs(999): total = 'all'
   else: total = abs(modtokens)
   if re.search(r'isPriority', Autoscript): card.highlight = PriorityColor
   if action.group(1) == 'Deal': countersTXT = '' # If we "deal damage" we do not want to be writing "deals 1 damage counters"
   else: countersTXT = 'counters'
   if notification == 'Quick' and action.group(1) == 'Deal': 
         announceString = "{}'s {} {}s{} {} {} {}{}{}".format(announceText, card, action.group(1).lower(),infectTXT, total, token[0],countersTXT,targetCardlist,preventTXT)
   else: announceString = "{} {}{} {} {} {}{}{}".format(announceText, action.group(1).lower(),infectTXT, total, token[0],countersTXT,targetCardlist,preventTXT)
   if notification and modtokens != 0: notify(':> {}.'.format(announceString))
   if debugVerbosity >= 2: notify("### TokensX() String: {}".format(announceString)) #Debug
   if debugVerbosity >= 3: notify("<<< TokensX()")
   return announceString
 
def DrawX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> DrawX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   destiVerb = 'draw'
   action = re.search(r'\bDraw([0-9]+)Card', Autoscript)
   targetPL = ofwhom(Autoscript, card.controller)
   if debugVerbosity >= 3: notify("### Setting Source")
   if targetPL != me: destiVerb = 'move'
   if re.search(r'-fromDiscard', Autoscript): source = targetPL.piles['Discard Pile']
   else: source = targetPL.piles['Command Deck']
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
   if notification == 'Quick': announceString = "{} draws {} cards".format(announceText, count)
   elif targetPL == me: announceString = "{} {} {} cards from their {}{}".format(announceText, destiVerb, count, source.name, destPath)
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
   global Stored_Type, Stored_Cost, Stored_Keywords, Stored_AutoActions, Stored_AutoScripts
   dummyCard = None
   action = re.search(r'\bCreateDummy[A-Za-z0-9_ -]*(-with)(?!onOpponent|-doNotDiscard|-nonUnique)([A-Za-z0-9_ -]*)', Autoscript)
   if debugVerbosity >= 3 and action: notify('clicks regex: {}'.format(action.groups())) # debug
   targetPL = ofwhom(Autoscript, card.controller)
   for c in table:
      if c.model == card.model and c.controller == targetPL and c.highlight == DummyColor: dummyCard = c # We check if already have a dummy of the same type on the table.
   if not dummyCard or re.search(r'nonUnique',Autoscript): #Some create dummy effects allow for creating multiple copies of the same card model.
      if Dummywarn and re.search('onOpponent',Autoscript):
         if not confirm("This action creates an effect for your opponent and a way for them to remove it.\
                       \nFor this reason we've created a dummy card on the table and marked it with a special highlight so that you know that it's just a token.\
                     \n\nYou opponent can activate any abilities meant for them on the Dummy card. If this card has one, they can activate it by double clicking on the dummy. Very often, this will often remove the dummy since its effect will disappear.\
                     \n\nOnce the   dummy card is on the table, please right-click on it and select 'Pass control to {}'\
                     \n\nDo you want to see this warning again?".format(targetPL)): Dummywarn = False      
      elif Dummywarn:
         if not confirm("This card's effect requires that you trash it, but its lingering effects will only work automatically while a copy is in play.\
                       \nFor this reason we've created a dummy card on the table and marked it with a special highlight so that you know that it's just a token.\
                     \n\nSome cards provide you with an ability that you can activate after they're been trashed. If this card has one, you can activate it by double clicking on the dummy. Very often, this will often remove the dummy since its effect will disappear.\
                     \n\nDo you want to see this warning again?"): Dummywarn = False
      elif re.search(r'onOpponent', Autoscript): information('The dummy card just created is meant for your opponent. Please right-click on it and select "Pass control to {}"'.format(targetPL))
      dummyCard = table.create(card.model, -680, 200 * playerside, 1) # This will create a fake card like the one we just created.
      dummyCard.highlight = DummyColor
      storeProperties(dummyCard)
   #confirm("Dummy ID: {}\n\nList Dummy ID: {}".format(dummyCard._id,passedlist[0]._id)) #Debug
   if not re.search(r'doNotTrash',Autoscript): card.moveTo(card.owner.piles['Heap/Archives(Face-up)'])
   if action: announceString = TokensX('Put{}'.format(action.group(2)), announceText,dummyCard, n = n) # If we have a -with in our autoscript, this is meant to put some tokens on the dummy card.
   else: announceString = announceText + 'create a lingering effect for {}'.format(targetPL)
   if debugVerbosity >= 3: notify("<<< CreateDummy()")
   return announceString # Creating a dummy isn't usually announced.

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
   action = re.search(r'\b(Discard|Exile)(Target|Parent|Multi|Myself)[-to]*([A-Z][A-Za-z&_ ]+)?', Autoscript)
   if action.group(2) == 'Myself': 
      del targetCards[:] # Empty the list, just in case.
      targetCards.append(card)
   if action.group(3): dest = action.group(3)
   else: dest = 'hand'
   for targetCard in targetCards: 
      if action.group(1) == 'Derez': targetCardlist += '{},'.format(fetchProperty(targetCard, 'name')) # Derez saves the name because by the time we announce the action, the card will be face down.
      else: targetCardlist += '{},'.format(targetCard)
   targetCardlist = targetCardlist.strip(',') # Re remove the trailing comma
   for targetCard in targetCards:
      if re.search(r'-ifEmpty',Autoscript) and targetCard.markers[mdict['Credits']] and targetCard.markers[mdict['Credits']] > 0: 
         if len(targetCards) > 1: continue #If the modification only happens when the card runs out of credits, then we abort if it still has any
         else: return announceText # If there's only 1 card and it's not supposed to be trashed yet, do nothing.
      if action.group(1) == 'Trash':
         trashResult = Discard(targetCard, silent = True)
         if trashResult == 'ABORT': return 'ABORT'
         elif trashResult == 'COUNTERED': extraTXT = " (Countered!)"
      elif action.group(1) == 'Exile' and exileCard(targetCard, silent = True) != 'ABORT': pass
      else: return 'ABORT'
      if action.group(2) != 'Multi': break # If we're not doing a multi-targeting, abort after the first run.
   if notification == 'Quick': announceString = "{} {}es {}{}".format(announceText, action.group(1), targetCardlist,extraTXT)
   else: announceString = "{} {} {}{}".format(announceText, action.group(1), targetCardlist, extraTXT)
   if notification: notify(':> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< ModifyStatus()")
   return announceString
            
def UseCustomAbility(Autoscript, announceText, card, targetCards = None, notification = None, n = 0):
   announceString = Autoscript
   return announceString
   
def CustomScript(card, action = 'PLAY'): # Scripts that are complex and fairly unique to specific cards, not worth making a whole generic function for them.
   if debugVerbosity >= 1: notify(">>> CustomScript() with action: {}".format(action)) #Debug
   mute()
   discard = me.piles['Discard Pile']
   objectives = me.piles['Objective Deck']
   deck = me.piles['Command Deck']
   if card.model == 'ff4fb461-8060-457a-9c16-000000000149' and action == 'THWART' and card.owner == me:
      if not confirm("Do you want to use the optional interrupt of Journey To Dagobath?"): return
      if debugVerbosity >= 2: notify("### Journey to Dagobath Script")
      objList = []
      if debugVerbosity >= 2: notify("### Moving objectives to removed from game pile")
      for c in objectives:
         c.moveTo(me.piles['Removed from Game'])
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
      choice = SingleChoice("Which objective do you want to put into play from your deck?", objChoices, type = 'button', default = 0)
      storeObjective(Card(objList[choice]))
      shuffle(objectives)
      if debugVerbosity >= 2: notify("#### About to announce")
      notify("{} uses the ability of {} to replace it with {}".format(me,card,Card(objList[choice])))
      
#------------------------------------------------------------------------------
# Helper Functions
#------------------------------------------------------------------------------
       
def findTarget(Autoscript, fromHand = False, card = None): # Function for finding the target of an autoscript
   if debugVerbosity >= 1: notify(">>> findTarget(){}".format(extraASDebug(Autoscript))) #Debug
   try:
      if fromHand == True: group = me.hand
      else: group = table
      targetC = None
      foundTargets = []
      if re.search(r'Targeted', Autoscript):
         validTargets = [] # a list that holds any type that a card must be, in order to be a valid target.
         requiredAllegiances = []
         targetGroups = []
         cardProperties = []
         whatTarget = re.search(r'\bat([A-Za-z_{},& ]+)[-]?', Autoscript) # We signify target restrictions keywords by starting a string with "or"
         if debugVerbosity >= 2: notify("###Splitting on _or_") #Debug
         if whatTarget: validTargets = whatTarget.group(1).split('_or_') # If we have a list of valid targets, split them into a list, separated by the string "_or_". Usually this results in a list of 1 item.
         ValidTargetsSnapshot = list(validTargets) # We have to work on a snapshot, because we're going to be modifying the actual list as we iterate.
         for iter in range(len(ValidTargetsSnapshot)): # Now we go through each list item and see if it has more than one condition (Eg, non-desert fief)
            if debugVerbosity >= 2: notify("### Creating empty list tuple") #Debug            
            targetGroups.insert(iter,([],[])) # We create a tuple of two list. The first list is the valid properties, the second the invalid ones
            multiConditionTargets = ValidTargetsSnapshot[iter].split('_and_') # We put all the mutliple conditions in a new list, separating each element.
            if debugVerbosity >= 2: notify("###Splitting on _and_. _or_ ") #Debug
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
         if debugVerbosity >= 2: notify("### About to start checking all targeted cards.\ntargetGroups:{}".format(targetGroups)) #Debug
         for targetLookup in group: # Now that we have our list of restrictions, we go through each targeted card on the table to check if it matches.
            if ((targetLookup.targetedBy and targetLookup.targetedBy == me) or (re.search(r'AutoTargeted', Autoscript) and targetLookup.highlight != UnpaidColor and targetLookup.highlight != EdgeColor and targetLookup.highlight != CapturedColor and targetLookup.highlight !=FateColor)) and chkPlayer(Autoscript, targetLookup.controller, False): # The card needs to be targeted by the player. If the card needs to belong to a specific player (me or rival) this also is taken into account.
            # OK the above target check might need some decoding:
            # Look through all the cards on the group and start checking only IF...
            # * Card is targeted and targeted by the player OR target search has the -AutoTargeted modulator and it is NOT highlighted as a Fate, Edge or Captured.
            # * The player who controls this card is supposed to be me or the enemy.
               if debugVerbosity >= 3: notify("### Checking {}".format(targetLookup)) #Debug
               del cardProperties[:] # Cleaning the previous entries
               if debugVerbosity >= 4: notify("### Appending name") #Debug                
               cardProperties.append(targetLookup.name) # We are going to check its name
               if debugVerbosity >= 4: notify("### Appending Type") #Debug                
               cardProperties.append(targetLookup.Type) # We are going to check its Type
               if debugVerbosity >= 4: notify("### Appending Affiliation") #Debug                
               cardProperties.append(targetLookup.Affiliation) # We are going to check its Affiliation
               if debugVerbosity >= 4: notify("### Appending Traits") #Debug                
               cardSubtypes = targetLookup.Traits.split('-') # And each individual trait. Traits are separated by " - "
               for cardSubtype in cardSubtypes:
                  strippedCS = cardSubtype.strip() # Remove any leading/trailing spaces between traits. We need to use a new variable, because we can't modify the loop iterator.
                  if strippedCS: cardProperties.append(strippedCS) # If there's anything left after the stip (i.e. it's not an empty string anymrore) add it to the list.
               if debugVerbosity >= 4: notify("### Appending Side") #Debug                
               cardProperties.append(targetLookup.Side) # We are also going to check if the card is for Dark or Light Side
               if debugVerbosity >= 2: notify("### Card Properties: {}".format(cardProperties)) #Debug                
               for restrictionsGroup in targetGroups: 
               # We check each card against each restrictions group of valid + invalid properties.
               # Each Restrictions group is a tuple of two lists. First list (tuple[0]) is the valid properties, and the second list is the invalid properties
               # Then we put all the card properties in a list
               # We check if all the properties from the valid list are in the card properties
               # And then we check if no properties from the invalid list are in the properties
               # If both of these are true, then the card is retained as a valid target for our action.
                  if debugVerbosity >= 3: notify("### restrictionsGroup checking: {}".format(restrictionsGroup))
                  if targetC: break # If the card is a valid target from a previous restrictions group, we just chose it.
                  targetC = targetLookup
                  if len(targetGroups) > 0 and len(restrictionsGroup[0]) > 0: 
                     for validtargetCHK in restrictionsGroup[0]: # look if the card we're going through matches our valid target checks
                        if debugVerbosity >= 4: notify("### Checking for valid match on {}".format(validtargetCHK)) #Debug
                        if validtargetCHK not in cardProperties: targetC = None
                  elif debugVerbosity >= 4: notify("### No positive restrictions")
                  if len(targetGroups) > 0 and len(restrictionsGroup[1]) > 0: # If we have no target restrictions, any selected card will do as long as it's a valid target.
                     for invalidtargetCHK in restrictionsGroup[1]:
                        if debugVerbosity >= 4: notify("### Checking for invalid match on {}".format(invalidtargetCHK)) #Debug
                        if invalidtargetCHK in cardProperties: targetC = None
                  elif debugVerbosity >= 4: notify("### No negative restrictions")
                  markerName = re.search(r'-hasMarker{([\w ]+)}',Autoscript) # Checking if we need specific markers on the card.
                  if markerName: #If we're looking for markers, then we go through each targeted card and check if it has any relevant markers
                     if debugVerbosity >= 2: notify("### Checking marker restrictions")# Debug
                     if debugVerbosity >= 2: notify("### Marker Name: {}".format(markerName.group(1)))# Debug
                     marker = findMarker(targetLookup, markerName.group(1))
                     if not marker: targetC = None
                  elif debugVerbosity >= 2: notify("### No marker restrictions.")
                  if re.search(r'isCurrentObjective',Autoscript):
                     if targetLookup.highlight != DefendColor: targetC = None
                  if re.search(r'isParticipating',Autoscript):
                     if targetLookup.orientation != Rot90: targetC = None
                  if re.search(r'isCommited',Autoscript):
                     if targetLookup.highlight != LightForceColor and targetLookup.highlight != DarkForceColor: targetC = None
               if targetC and not targetC in foundTargets: 
                  if debugVerbosity >= 3: notify("### About to append {}".format(targetC)) #Debug
                  foundTargets.append(targetC) # I don't know why but the first match is always processed twice by the for loop.
               elif debugVerbosity >= 3: notify("### findTarget() Rejected {}".format(targetLookup))# Debug
               targetC = None
         if len(foundTargets) == 0 and not re.search(r'AutoTargeted', Autoscript): 
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
            if not chkPlayer(Autoscript, targetLookup.controller, False): 
               allegiance = re.search(r'by(Opponent|Me)', Autoscript)
               requiredAllegiances.append(allegiance.group(1))
            if len(requiredAllegiances) > 0: targetsText += "\nValid Target Allegiance: {}.".format(requiredAllegiances)
            whisper(":::ERROR::: You need to target a valid card before using this action{}.".format(targetsText))
         elif len(foundTargets) >= 1 and re.search(r'-choose',Autoscript):
            if debugVerbosity >= 2: notify("### Going for a choice menu")# Debug
            choiceType = re.search(r'-choose([0-9]+)',Autoscript)
            targetChoices = []
            if debugVerbosity >= 2: notify("### About to prepare choices list.")# Debug
            for T in foundTargets:
               markers = 'Counters:'
               if T.markers[mdict['Damage']] and T.markers[mdict['Damage']] >= 1: markers += " {} Damage,".format(T.markers[mdict['Damage']])
               if T.markers[mdict['Focus']] and T.markers[mdict['Focus']] >= 1: markers += " {} Focus,".format(T.markers[mdict['Focus']])
               if T.markers[mdict['Shield']] and T.markers[mdict['Shield']] >= 1: markers += " {} Shield.".format(T.markers[mdict['Shield']])
               if markers != '': markers += '\n'
               stats = ''
               if num(T.Resources) >= 1: stats += "Resources: {}. ".format(T.Resources)
               if num(T.properties['Damage Capacity']) >= 1: stats += "HP: {}.".format(T.properties['Damage Capacity'])
               if T.Type == 'Unit': combatIcons = parseCombatIcons(T.properties['Combat Icons'])
               else: combatIcons = ''
               choiceTXT = "{}\n{}{}\nIcons: {}".format(T.name,markers,stats,combatIcons)
               targetChoices.append(choiceTXT)
            if not card: choiceTitle = "Choose one of the valid targets for this effect"
            else: choiceTitle = "Choose one of the valid targets for {}'s ability".format(card.name)
            if debugVerbosity >= 2: notify("### Checking for SingleChoice")# Debug
            if choiceType.group(1) == '1':
               if len(foundTargets) == 1: choice = 0 # If we only have one valid target, autoselect it.
               else: choice = SingleChoice(choiceTitle, targetChoices, type = 'button', default = 0)
               foundTargets = [foundTargets.pop(choice)] # if we select the target we want, we make our list only hold that target
      if debugVerbosity >= 3: # Debug
         tlist = []
         for foundTarget in foundTargets: tlist.append(foundTarget.name) # Debug
         notify("<<< findTarget() by returning: {}".format(tlist))
      return foundTargets
   except: notify("!!!ERROR!!! on findTarget()")

def chkPlayer(Autoscript, controller, manual): # Function for figuring out if an autoscript is supposed to target an opponent's cards or ours.
# Function returns 1 if the card is not only for rivals, or if it is for rivals and the card being activated it not ours.
# This is then multiplied by the multiplier, which means that if the card activated only works for Rival's cards, our cards will have a 0 gain.
# This will probably make no sense when I read it in 10 years...
   if debugVerbosity >= 1: notify(">>> chkPlayer(). Controller is: {}".format(controller)) #Debug
   try:
      byOpponent = re.search(r'byOpponent', Autoscript)
      byMe = re.search(r'byMe', Autoscript)
      if manual: 
         if debugVerbosity >= 3: notify("<<< chkPlayer() with return 1 (Manual)")
         return 1 #manual means that the clicks was called by a player double clicking on the card. In which case we always do it.
      elif not byOpponent and not byMe: 
         if debugVerbosity >= 3: notify("<<< chkPlayer() with return 1 (Neutral)")   
         return 1 # If the card has no restrictions on being us or a rival.
      elif byOpponent and controller != me: 
         if debugVerbosity >= 3: notify("<<< chkPlayer() with return 1 (byOpponent)")   
         return 1 # If the card needs to be played by a rival.
      elif byMe and controller == me: 
         if debugVerbosity >= 3: notify("<<< chkPlayer() with return 1 (byMe)")   
         return 1 # If the card needs to be played by us.
      if debugVerbosity >= 3: notify("<<< chkPlayer() with return 0") # Debug
      else: return 0 # If all the above fail, it means that we're not supposed to be triggering, so we'll return 0 whic
   except: notify("!!!ERROR!!! Null value on chkPlayer()")

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
         if not confirm("This card performs a lot of complex clicks that will very difficult to undo. Are you sure you want to proceed?"):
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
         perCHK = per.group(3).split('_on_') # First we check to see if in our conditions we're looking for markers or card properties, to remove them from the checks
         perCHKSnapshot = list(perCHK)
         for chkItem in perCHKSnapshot:
            if re.search(r'(Marker|Property|Any)',chkItem):
               perCHK.remove(chkItem) # We remove markers and card.properties from names of the card keywords  we'll be looking for later.
         cardProperties = [] #we're making a big list with all the properties of the card we need to match
         if re.search(r'fromHand', Autoscript): cardgroup = findTarget('Targeted-at' + chkItem, fromHand = True)
         else: cardgroup = findTarget('Targeted-at' + chkItem)
         for c in cardgroup: # Go through each card on the table and gather its properties, then see if they match.
            perCHK = True # Variable to show us if the card we're checking is still passing all the requirements.
            if debugVerbosity >= 2: notify("### Starting check of found cards") # Debug
            if re.search(r'Marker',per.group(3)): #If we're looking for markers, then we go through each targeted card and check if it has any relevant markers
               markerName = re.search(r'Marker{([\w ]+)}',per.group(3)) # If we're looking for markers on the card, increase the multiplier by the number of markers found.
               marker = findMarker(card, markerName.group(1))
               if marker: multiplier += card.markers[marker]
            elif re.search(r'Property',per.group(3)): # If we're looking for a specific property on the card, increase the multiplier by the total of the properties on the cards found.
               property = re.search(r'Property{([\w ]+)}',per.group(3))
               multiplier += num(c.properties[property.group(1)]) # Don't forget to turn it into an integer first!
            else: multiplier += 1 * chkPlayer(Autoscript, c.controller, False) # If the perCHK remains 1 after the above loop, means that the card matches all our requirements. We only check faceup cards so that we don't take into acoount peeked face-down ones.
                                                                                  # We also multiply it with chkPlayer() which will return 0 if the player is not of the correct allegiance (i.e. Rival, or Me)
      else: #If we're not looking for a particular target, then we check for everything else.
         if debugVerbosity >= 2: notify("### Doing no table lookup") # Debug.
         if per.group(3) == 'X': multiplier = count # Probably not needed and the next elif can handle alone anyway.
         elif count: multiplier = num(count) * chkPlayer(Autoscript, card.controller, False) # All non-special-rules per<somcething> requests use this formula.
                                                                                              # Usually there is a count sent to this function (eg, number of favour purchased) with which to multiply the end result with
                                                                                              # and some cards may only work when a rival owns or does something.
         elif re.search(r'Marker',per.group(3)):
            markerName = re.search(r'Marker{([\w ]+)}',per.group(3)) # I don't understand why I had to make the curly brackets optional, but it seens atTurnStart/End completely eats them when it parses the CardsAS.get(card.model,'')
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
   