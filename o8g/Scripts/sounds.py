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

def playParticipateSound(card):
   debugNotify(">>> playParticipateSound  with card: {}".format(card))
   if not getSetting('Sounds', True): return
   if card.name == 'Han Solo': playSound('participate_Han_Solo')
   elif card.name == 'C-3PO': playSound('participate_c3p0')
   elif card.name == 'Luke Skywalker': playSound('participate_Luke')
   elif card.name == 'Darth Vader': playSound('participate_Vader')
   elif re.search(r'Capital Ship',card.Traits): playSound('participate_capital_ship{}'.format(rnd(1,1)))
   elif re.search(r'Fighter',card.Traits):
      if card.Side == 'Light': playSound('participate_fighter_LS{}'.format(rnd(1,4)))
      else: playSound('participate_fighter_DS{}'.format(rnd(1,4)))
   elif re.search(r'Transport',card.Traits): playSound('participate_transport{}'.format(rnd(1,3)))
   elif re.search(r'Force User',card.Traits): playSound('participate_force_user{}'.format(rnd(1,3)))
   elif re.search(r'Character',card.Traits): playSound('participate_character{}'.format(rnd(1,3)))
   elif re.search(r'Creature',card.Traits): playSound('participate_creature{}'.format(rnd(1,2)))
   elif re.search(r'Droid',card.Traits): playSound('participate_droid{}'.format(rnd(1,3)))
   elif re.search(r'Vehicle',card.Traits): playSound('participate_vehicle{}'.format(rnd(1,4)))
   
def playStrikeSound(card):
   debugNotify(">>> playStrikeSound  with card: {}".format(card))
   if not getSetting('Sounds', True): return
   if card.name == 'R2-D2': playSound('strike_r2d2')
   elif card.name == 'C-3PO': playSound('strike_c3p0')
   elif re.search(r'Wookiee',card.name) or card.name == 'Chewbacca': playSound('strike_wookiee{}'.format(rnd(1,3)))
   elif re.search(r'Capital Ship',card.Traits): playSound('strike_capital_ship{}'.format(rnd(1,1)))
   elif re.search(r'Fighter',card.Traits):
      if card.Side == 'Light': playSound('strike_fighter_LS{}'.format(rnd(1,2)))
      else: playSound('strike_fighter_DS{}'.format(rnd(1,1)))
   elif re.search(r'Force User',card.Traits): playSound('strike_force_user{}'.format(rnd(1,4)))
   elif re.search(r'Trooper',card.Traits): playSound('strike_trooper{}'.format(rnd(1,2)))
   elif re.search(r'Droid',card.Traits): playSound('strike_droid{}'.format(rnd(1,4)))
   elif re.search(r'Vehicle',card.Traits): playSound('strike_vehicle{}'.format(rnd(1,4)))
   elif re.search(r'Character',card.Traits): playSound('strike_character{}'.format(rnd(1,4)))
   elif re.search(r'Creature',card.Traits): playSound('strike_creature{}'.format(rnd(1,1)))
   
def playDestroySound(card):
   debugNotify(">>> playDestroySound  with card: {}".format(card))
   if not getSetting('Sounds', True): return
   if card.Type == 'Unit':
      if re.search(r'Droid',card.Traits): playSound('destroy_droid{}'.format(rnd(1,2)))
      elif re.search(r'Vehicle',card.Traits): playSound('destroy_vehicle{}'.format(rnd(1,2)))
      elif re.search(r'Character',card.Traits): playSound('destroy_character{}'.format(rnd(1,4)))

def playThwartSound(): 
   debugNotify(">>> playThwartSound")
   if not getSetting('Sounds', True): return
   playSound('thwart_objective{}'.format(rnd(1,4)))
   
def playUnitSound(card):
   debugNotify(">>> playUnitSound  with card: {}".format(card))
   if not getSetting('Sounds', True): return
   if re.search(r'Greedo',card.name): playSound('play_Greedo')
   if re.search(r'Jabba the Hutt',card.name): playSound('play_Jabba')
   if re.search(r'Jawa',card.name): playSound('play_Jawa')
   if re.search(r'R2-D2',card.name): playSound('play_R2D2')
   if re.search(r'Vader',card.name): playSound('play_Vader')
   if re.search(r'Yoda',card.name): playSound('play_Yoda')
   if re.search(r'Leia',card.name): playSound('play_Leia')
   if re.search(r'Palpatine',card.name): playSound('play_Palpatine')
   if re.search(r'Luke Skywalker',card.name): playSound('play_Luke')
   if re.search(r'Obi-Wan',card.name): playSound('play_Obi_Wan')
   if re.search(r'Han Solo',card.name): playSound('play_Han_Solo')
   if re.search(r'Millennium Falcon',card.name): playSound('play_falcon')
   if re.search(r'C-3PO',card.name): playSound('play_c3p0')

def playEventSound(card):
   debugNotify(">>> playEventSound  with card: {}".format(card))
   if not getSetting('Sounds', True): return
   if re.search(r'Force',card.Traits) and card.Type == 'Event':
      if card.name == 'Force Choke': playSound('play_force_choke')
      elif card.Name == 'Force Lightning': playSound('play_force_lightning')
      elif re.search(r'Control',card.Traits) and re.search(r'Sense',card.Traits) and re.search(r'Alter',card.Traits): playSound('play_force_control_alter_sense')   
      elif re.search(r'Control',card.Traits) and re.search(r'Alter',card.Traits): playSound('play_force_control_alter')   
      elif re.search(r'Control',card.Traits) and re.search(r'Sense',card.Traits): playSound('play_force_control_sense')   
      elif re.search(r'Alter',card.Traits) and re.search(r'Sense',card.Traits): playSound('play_force_sense_alter')   
      elif re.search(r'Alter',card.Traits): playSound('play_force_alter')   
      elif re.search(r'Control',card.Traits): playSound('play_force_control')   
      elif re.search(r'Sense',card.Traits): playSound('play_force_sense')   
   