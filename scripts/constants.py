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

    
Resource = ("Resource", "62a2ba76-9872-481b-b8fc-ec35447ca640") #Temp 
Damage = ("Damage", "38d55f36-04d7-4cf9-a496-06cb84de567d") # Temp
Shield = ("Shield", "e9a419ff-5154-41cf-b84f-95149cc19a2a") # Temp

    
mdict = dict( # A dictionary which holds all the hard coded markers (in the markers file)
             Resource =                ("Resource", "62a2ba76-9872-481b-b8fc-ec35447ca640"),
             Damage =                  ("Damage", "38d55f36-04d7-4cf9-a496-06cb84de567d"),
             Shield =                  ("Shield", "e9a419ff-5154-41cf-b84f-95149cc19a2a"))

ScoredColor = "#00ff44"
SelectColor = "#009900"
DummyColor = "#000000" # Marks cards which are supposed to be out of play, so that players can tell them apart.
RevealedColor = "#ffffff"
PriorityColor = "#ffd700"
InactiveColor = "#888888" # Cards which are in play but not active yet
AttackColor = "#ff0000"
DefendColor = "#0000ff"

Xaxis = 'x'
Yaxis = 'y'

phases = [
    "Balance Phase: {}.".format(me),
    "Refresh Phase: {}.".format(me),
    "Draw Phase: {}.".format(me),
    "Deployment Phase: {}.".format(me),
    "Conflict Phase: {}.".format(me),
    "Force Phase: {}.".format(me)]
