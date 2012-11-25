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
              }


UniCode = True # If True, game will display credits, clicks, trash, memory as unicode characters

debugVerbosity = -1 # At -1, means no debugging messages display

startupMsg = False # Used to check if the player has checked for the latest version of the game.

gameGUID = None # A Unique Game ID that is fetched during game launch.
#totalInfluence = 0 # Used when reporting online
#gameEnded = False # A variable keeping track if the players have submitted the results of the current game already.
turn = 0 # used during game reporting to report how many turns the game lasted


    
def storeSpecial(card): 
# Function stores into a shared variable some special cards that other players might look up.
   if debugVerbosity >= 1: notify(">>> storeSpecial(){}".format(extraASDebug())) #Debug
   specialCards = eval(me.getGlobalVariable('specialCards'))
   specialCards[card.Type] = card._id
   me.setGlobalVariable('specialCards', str(specialCards))

def getSpecial(cardType,player = me):
# Functions takes as argument the name of a special card, and the player to whom it belongs, and returns the card object.
   if debugVerbosity >= 1: notify(">>> getSpecial(){}".format(extraASDebug())) #Debug
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
   
def switchWinForms(group,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> switchWinForms(){}".format(extraASDebug())) #Debug
   switchAutomation('WinForms')
   
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
# Debugging
#------------------------------------------------------------------------------
   
def TrialError(group, x=0, y=0): # Debugging
   global Side, debugVerbosity
   mute()
   ######## Testing Corner ########
   #for hook in regexHooks: notify("regex for {} is {}".format(hook, regexHooks[hook]))
   #if regexHooks['GainX'].search('TrashMyself'): confirm("Found!")
   #else: confirm("Not Found :(")
   ###### End Testing Corner ######
   if debugVerbosity >=0: 
      if debugVerbosity == 0: 
         debugVerbosity = 1
         ImAProAtThis() # At debug level 1, we also disable all warnings
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
      
