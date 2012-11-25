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

Side = None # The side of the player. 'runner' or 'corp'
    
#---------------------------------------------------------------------------
# Rest
#---------------------------------------------------------------------------
    
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

def roll20(group, x = 0, y = 0):
    mute()
    n = rnd(1, 20)
    notify("{} rolls {} on a 20-sided die.".format(me, n))

def flipCoin(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1:
        notify("{} flips heads.".format(me))
    else:
        notify("{} flips tails.".format(me))

def focus(card, x = 0, y = 0):
    mute()
    card.orientation ^= Rot90
    if card.orientation & Rot90 == Rot90:
		notify('{} taps {}'.format(me, card))
    else:
        notify('{} untaps {}'.format(me, card))
		  
def discard(card, x = 0, y = 0):
	card.moveTo(me.piles['Discard Pile'])
	notify("{} discards {}".format(me, card))

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

def drawMany(group, count = None):
	if len(group) == 0: return
	mute()
	if count == None: count = askInteger("Draw how many cards?", 0)
	for card in group.top(count): card.moveTo(me.hand)
	notify("{} draws {} cards.".format(me, count))

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