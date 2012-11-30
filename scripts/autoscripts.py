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


#------------------------------------------------------------------------------
# Helper Functions
#------------------------------------------------------------------------------
       
def findTarget(Autoscript): # Function for finding the target of an autoscript
   if debugVerbosity >= 1: notify(">>> findTarget(){}".format(extraASDebug(Autoscript))) #Debug
   try:
      targetC = None
      foundTargets = []
      if re.search(r'Targeted', Autoscript):
         validTargets = [] # a list that holds any type that a card must be, in order to be a valid target.
         validNamedTargets = [] # a list that holds any name or allegiance that a card must have, in order to be a valid target.
         invalidTargets = [] # a list that holds any type that a card must not be to be a valid target.
         invalidNamedTargets = [] # a list that holds the name or allegiance that the card must not have to be a valid target.
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
            validTargets.remove(ValidTargetsSnapshot[iter]) # Finally, remove the multicondition keyword from the valid list. Its individual elements should now be on this list or the invalid targets one.
         if debugVerbosity >= 2: notify("### About to start checking all targeted cards.\ntargetGroups:{}".format(targetGroups)) #Debug
         for targetLookup in table: # Now that we have our list of restrictions, we go through each targeted card on the table to check if it matches.
            if ((targetLookup.targetedBy and targetLookup.targetedBy == me) or (re.search(r'AutoTargeted', Autoscript) and targetLookup.highlight != UnpaidColor and targetLookup.highlight != EdgeColor and targetLookup.highlight != CapturedColor)) and chkPlayer(Autoscript, targetLookup.controller, False): # The card needs to be targeted by the player. If the card needs to belong to a specific player (me or rival) this also is taken into account.
            # OK the above target check might need some decoding:
            # Look through all the cards on the table and start checking only IF...
            # * Card is targeted and targeted by the player OR target search has the -AutoTargeted modulator and it is NOT highlighted as a Dummy, Revealed or Inactive.
            # * The player who controls this card is supposed to be me or the enemy.
               if debugVerbosity >= 3: notify("### Checking {}".format(targetLookup)) #Debug
               del cardProperties[:] # Cleaning the previous entries
               cardProperties.append(targetLookup.name) # We are going to check its name
               cardProperties.append(targetLookup.Type) # We are going to check its Type
               cardProperties.append(targetLookup.Affiliation) # We are going to check its Affiliation
               cardSubtypes = card.Traits.split('-') # And each individual trait. Traits are separated by " - "
               for cardSubtype in cardSubtypes:
                  strippedCS = cardSubtype.strip() # Remove any leading/trailing spaces between traits. We need to use a new variable, because we can't modify the loop iterator.
                  if strippedCS: cardProperties.append(strippedCS) # If there's anything left after the stip (i.e. it's not an empty string anymrore) add it to the list.
               cardProperties.append(c.Side) # We are also going to check if the card is for Dark or Light Side
               for restrictionsGroup in targetGroups: 
               # We check each card against each restrictions group of valid + invalid properties.
               # Each Restrictions group is a tuple of two lists. First list (tuple[0]) is the valid properties, and the second list is the invalid properties
               # Then we put all the card properties in a list
               # We check if all the properties from the valid list are in the card properties
               # And then we check if no properties from the invalid list are in the properties
               # If both of these are true, then the card is retained as a valid target for our action.
                  if targetC: break # If the card is a valid target from a previous restrictions group, we just chose it.
                  if len(restrictionsGroup[0]) > 0: targetC = targetLookup # If there are no positive restrictions, any targeted card is acceptable
                  else:
                     for validtargetCHK in restrictionsGroup: # look if the card we're going through matches our valid target checks
                        if debugVerbosity >= 4: notify("### Checking for valid match on {}".format(validtargetCHK)) #Debug
                        if validtargetCHK not in cardProperties
                           targetC = targetLookup
                     for validtargetCHK in validNamedTargets: # look if the card we're going through matches our valid target checks
                        if validtargetCHK == fetchProperty(targetLookup, 'name'):
                           targetC = targetLookup
               if len(invalidTargets) > 0: # If we have no target restrictions, any selected card will do as long as it's a valid target.
                  for invalidtargetCHK in invalidTargets:
                     if debugVerbosity >= 4: notify("### Checking for invalid match on {}".format(invalidtargetCHK)) #Debug
                     if re.search(r'{}'.format(invalidtargetCHK), fetchProperty(targetLookup, 'Type')) or re.search(r'{}'.format(invalidtargetCHK), fetchProperty(targetLookup, 'Keywords')) or re.search(r'{}'.format(invalidtargetCHK), targetLookup.Side):
                        targetC = None
               if len(invalidNamedTargets) > 0: # If we have no target restrictions, any selected card will do as long as it's a valid target.
                  for invalidtargetCHK in invalidNamedTargets:
                     if invalidtargetCHK == fetchProperty(targetLookup, 'name'):
                        targetC = None
               if targetC and not targetC in foundTargets: 
                  if debugVerbosity >= 3: notify("### About to append {}".format(targetC)) #Debug
                  foundTargets.append(targetC) # I don't know why but the first match is always processed twice by the for loop.
               elif debugVerbosity >= 3: notify("### findTarget() Rejected {}".format(targetLookup))
         if targetC == None and not re.search(r'AutoTargeted', Autoscript): 
            targetsText = ''
            if len(validTargets) > 0: targetsText += "\nValid Target types: {}.".format(validTargets)
            if len(validNamedTargets) > 0: targetsText += "\nSpecific Valid Targets: {}.".format(validNamedTargets)
            if len(invalidTargets) > 0: targetsText += "\nInvalid Target types: {}.".format(invalidTargets)
            if len(invalidNamedTargets) > 0: targetsText += "\nSpecific Invalid Targets: {}.".format(invalidNamedTargets)
            if not chkPlayer(Autoscript, targetLookup.controller, False): 
               allegiance = re.search(r'by(Opponent|Me)', Autoscript)
               requiredAllegiances.append(allegiance.group(1))
            if len(requiredAllegiances) > 0: targetsText += "\nValid Target Allegiance: {}.".format(requiredAllegiances)
            whisper("You need to target a valid card before using this action{}".format(targetsText))
      #confirm("List is: {}".format(foundTargets)) # Debug
      if debugVerbosity >= 3: 
         tlist = []
         for foundTarget in foundTargets: tlist.append(fetchProperty(foundTarget, 'name')) # Debug
         notify("<<< findTarget() by returning: {}".format(tlist))
      return foundTargets
   except ValueError: notify("!!!ERROR!!! Null value on findTarget()")

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
   except ValueError: notify("!!!ERROR!!! Null value on chkPlayer()")
      