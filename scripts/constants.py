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
             Focus =                   ("Resource", "c93d4582-16a0-4e2d-9e63-71be20fbfa0c"),
             Damage =                  ("Damage", "224b865d-173b-49fd-9aed-17df678259b0"),
             PlusOnePerm =             ("Permanent +1", "2246648d-1581-4be9-9636-1b75129313a6"),
             PlusOne =                 ("Temporary +1", "987d0d3f-0965-49ae-a96c-03394783d47a"),
             MinusOne =                ("Temporary -1", "21487438-e108-4f0c-a804-bd2a7f9a1ae5"),
             Shield =                  ("Shield", "8559643f-7a15-4605-937d-0f39d59c9eda"))

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
    "Opponent's Turn",
    "Balance Phase: {}.".format(me),
    "Refresh Phase: {}.".format(me),
    "Draw Phase: {}.".format(me),
    "Deployment Phase: {}.".format(me),
    "Conflict Phase: {}.".format(me),
    "Force Phase: {}.".format(me)]
