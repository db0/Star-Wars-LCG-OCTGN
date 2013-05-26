### ANR CARD SCRIPTS ###
# 5 Equal Signs (=) signifiies a break between the description (what you're currently reading) and the code
# 5 Dashes  (-) signifies a break between the card name, the GUID and the card scripts. The card name is ignored by the code, only the GUID and Scripts are used.
# 5 Plus Signs (+) signifies a break between AutoActions and AutoScripts for the same card
# 5 Dots (.) signifies a break between different cards.
# Do not edit below the line
ScriptsLocal = '''
=====
"Backstabber"
-----
ff4fb461-8060-457a-9c16-000000000050
-----
onPlay:Deal1Damage-AutoTargeted-atObjective-isOptional-isCurrentObjective-onlyDuringEngagement
+++++

.....
A Disturbance In the Force
-----
ff4fb461-8060-457a-9c16-000000000113
-----
onPlay:Put1Focus-AutoTargeted-atUnit-isCommited-targetOpponents
+++++

.....
A Hero's Journey
-----
ff4fb461-8060-457a-9c16-000000000063
-----

+++++

.....
A Journey to Dagobah
-----
ff4fb461-8060-457a-9c16-000000000149
-----
onThwart:CustomScript
+++++

.....
A New Hope
-----
ff4fb461-8060-457a-9c16-000000000197
-----

+++++

.....
A-Wing
-----
ff4fb461-8060-457a-9c16-000000000012
-----
onStrike:Draw1Card
+++++

.....
Admiral Ackbar
-----
ff4fb461-8060-457a-9c16-000000000187
-----
onPlay:Deal1Damage-AutoTargeted-atUnit-targetOpponents-isParticipating-onlyDuringEngagement-isOptional
+++++

.....
Admiral Motti
-----
ff4fb461-8060-457a-9c16-000000000070
-----
afterRefresh:Remove1Focus-AutoTargeted-atUnit-targetMine-choose1-hasMarker{Focus}-duringMyTurn
+++++

.....
Advisor to the Emperor
-----
ff4fb461-8060-457a-9c16-000000000115
-----

+++++

.....
Aft Armor Plating
-----
ff4fb461-8060-457a-9c16-000000000061
-----
Placement:Vehicle_and_Unit||onHostParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}
+++++

.....
Ancient Monument
-----
ff4fb461-8060-457a-9c16-000000000170
-----
ConstantEffect:Force1Bonus
+++++

.....
Astromech Droid Upgrade
-----
ff4fb461-8060-457a-9c16-000000000175
-----
Placement:Vehicle_and_Unit||BonusIcons:UD:1, BD:1
+++++

.....
AT-ST
-----
ff4fb461-8060-457a-9c16-000000000002
-----
onPlay:Draw1Card
+++++

.....
AT-ST
-----
ff4fb461-8060-457a-9c16-000000000060
-----
onPlay:Draw1Card
+++++

.....
AT-ST Commander
-----
ff4fb461-8060-457a-9c16-000000000059
-----

+++++

.....
Battlefield Engineers
-----
ff4fb461-8060-457a-9c16-000000000015
-----
onAttack:Remove1Focus-AutoTargeted-atEnhancement-choose1-hasMarker{Focus}
+++++

.....
Believer in the Old Ways
-----
ff4fb461-8060-457a-9c16-000000000141
-----

+++++

.....
Believer in the Old Ways
-----
ff4fb461-8060-457a-9c16-000000000169
-----

+++++

.....
Black Squadron Assault
-----
ff4fb461-8060-457a-9c16-000000000126
-----

+++++
Put1Focus-isCost$$Remove1Focus-Targeted-atBlack Squadron
.....
Black Squadron Pilot
-----
ff4fb461-8060-457a-9c16-000000000129
-----
onPlay:CustomScript||BonusIcons:UD:1, BD:1
+++++

.....
Blaster Pistol
-----
ff4fb461-8060-457a-9c16-000000000079
-----
Placement:Character_and_Unit||BonusIcons:UD:1
+++++

.....
Boba Fett
-----
ff4fb461-8060-457a-9c16-000000000076
-----

+++++
CaptureTarget-Targeted-atCharacter
.....
Bounty Collection
-----
ff4fb461-8060-457a-9c16-000000000080
-----
onPlay:Remove1Focus-DemiAutoTargeted-atnonUnit-choose3
+++++

.....
C-3PO
-----
ff4fb461-8060-457a-9c16-000000000156
-----

+++++
DestroyMyself$$SimplyAnnounce{cancel the effects of the event card}$$Put1Effects Cancelled-DemiAutoTargeted-atEvent-isReady-choose1-isSilent
.....
Cloud City Casino
-----
ff4fb461-8060-457a-9c16-000000000019
-----

+++++

.....
Common Ground
-----
ff4fb461-8060-457a-9c16-000000000201
-----
Placement:Objective||onHostGenerate:Put1Ignores Affiliation Match-AutoTargeted-isUnpaid
+++++

.....
Control Room
-----
ff4fb461-8060-457a-9c16-000000000032
-----

+++++

.....
Control Room
-----
ff4fb461-8060-457a-9c16-000000000037
-----

+++++

.....
Corellian Engineer
-----
ff4fb461-8060-457a-9c16-000000000163
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}
+++++

.....
Corporate Exploitation
-----
ff4fb461-8060-457a-9c16-000000000081
-----

+++++
Put1Focus-isCost$$SimplyAnnounce{put a unit of printed cost 1 or lower into play}
.....
Coruscant Defense Fleet
-----
ff4fb461-8060-457a-9c16-000000000023
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}
+++++
Remove1Damage-DemiAutoTargeted-atCoruscant-hasMarker{Damage}-choose1-isCost$$Put1Damage
.....
Counsel of the Sith
-----
ff4fb461-8060-457a-9c16-000000000114
-----
atTurnStart:Draw1Card-duringOpponentTurn
+++++

.....
Counter-stroke
-----
ff4fb461-8060-457a-9c16-000000000142
-----
onPlay:SimplyAnnounce{cancel the effects of the event}$$Put1Effects Cancelled-Targeted-atEvent-isReady-choose1-isSilent
+++++

.....
Covering Fire
-----
ff4fb461-8060-457a-9c16-000000000007
-----
onPlay:DestroyTarget-Targeted-atUnit$$Put1Shield-AutoTargeted-atUnit-targetMine-isParticipating-hasntMarker{Shield}
+++++

.....
Crossfire
-----
ff4fb461-8060-457a-9c16-000000000021
-----

+++++

.....
Cruel Interrogations
-----
ff4fb461-8060-457a-9c16-000000000120
-----
onPlay:CustomScript
+++++

.....
Dagobah Training Grounds
-----
ff4fb461-8060-457a-9c16-000000000068
-----

+++++

.....
Dagobah Training Grounds
-----
ff4fb461-8060-457a-9c16-000000000139
-----

+++++

.....
Dark Alliance
-----
ff4fb461-8060-457a-9c16-000000000220
-----
whileInPlay:IgnoreAffiliationMatch
+++++

.....
Dark Alliance
-----
ff4fb461-8060-457a-9c16-000000000221
-----
whileInPlay:IgnoreAffiliationMatch
+++++

.....
Dark Precognition
-----
ff4fb461-8060-457a-9c16-000000000118
-----
onPlay:Draw2Cards
+++++

.....
Dark Side Apprentice
-----
ff4fb461-8060-457a-9c16-000000000104
-----

+++++

.....
Darth Vader
-----
ff4fb461-8060-457a-9c16-000000000103
-----
whileInPlay:Deal1Damage-perCardPlayed-byMe-typeEvent_and_Sith-AutoTargeted-atUnit-choose1-targetOpponents-onlyOnce
+++++

.....
Death and Despayre
-----
ff4fb461-8060-457a-9c16-000000000034
-----

+++++

.....
Death from Above
-----
ff4fb461-8060-457a-9c16-000000000044
-----
onPlay:Put1Death from Above:BD-Targeted-atVehicle_and_Unit
+++++

.....
Death from Above
-----
ff4fb461-8060-457a-9c16-000000000049
-----

+++++

.....
Death Star Trooper
-----
ff4fb461-8060-457a-9c16-000000000053
-----

+++++

.....
Death Star Trooper
-----
ff4fb461-8060-457a-9c16-000000000054
-----

+++++

.....
Decoy at Dantooine
-----
ff4fb461-8060-457a-9c16-000000000192
-----
whileInPlay:Lose1Dial-perObjectiveThwarted-byOpponent
+++++

.....
Defense Protocol
-----
ff4fb461-8060-457a-9c16-000000000040
-----
afterRefresh:Lose1Reserves-isOptional-duringMyTurn$$Put1Activation-isSilent$$Deal1Damage-AutoTargeted-atUnit-choose1-targetOpponents||afterDraw:Remove1Activation-duringMyTurn-isCost-isSilent$$Gain1Reserves
+++++

.....
Defense Upgrade
-----
ff4fb461-8060-457a-9c16-000000000038
-----
Placement:Objective
+++++

.....
Detained
-----
ff4fb461-8060-457a-9c16-000000000055
-----
onPlay:CaptureTarget-Targeted-atCharacter_or_Droid
+++++

.....
Devastator
-----
ff4fb461-8060-457a-9c16-000000000035
-----

+++++
R1:Gain1Dial
.....
Double Strike
-----
ff4fb461-8060-457a-9c16-000000000153
-----
onPlay:Remove1Focus-Targeted-atCharacter-hasMarker{Focus}
+++++

.....
Draw Their Fire
-----
ff4fb461-8060-457a-9c16-000000000186
-----

+++++

.....
Duty Officer
-----
ff4fb461-8060-457a-9c16-000000000071
-----

+++++

.....
Emergency Repair
-----
ff4fb461-8060-457a-9c16-000000000165
-----
onPlay:Remove999Damage-Targeted-atObjective
+++++

.....
Emperor Palpatine
-----
ff4fb461-8060-457a-9c16-000000000097
-----

+++++
R0:Retrieve1Card-typeEvent_and_Sith-fromDiscard
.....
Emperor's Royal Guard
-----
ff4fb461-8060-457a-9c16-000000000098
-----

+++++
Remove1Damage-DemiAutoTargeted-atCharacter-hasMarker{Damage}-choose1-isCost$$Put1Damage
.....
Espo Trooper
-----
ff4fb461-8060-457a-9c16-000000000082
-----

+++++

.....
Espo Trooper
-----
ff4fb461-8060-457a-9c16-000000000083
-----

+++++

.....
Espo Trooper
-----
ff4fb461-8060-457a-9c16-000000000084
-----

+++++

.....
Espo Trooper
-----
ff4fb461-8060-457a-9c16-000000000085
-----

+++++

.....
Espo Trooper
-----
ff4fb461-8060-457a-9c16-000000000086
-----

+++++

.....
Ewok Scout
-----
ff4fb461-8060-457a-9c16-000000000205
-----
onAttack:Put1Ewok Scouted-DemiAutoTargeted-atUnit-hasntMarker{Focus}-targetOpponents-choose1
+++++

.....
Ewok Scout
-----
ff4fb461-8060-457a-9c16-000000000206
-----
onAttack:Put1Ewok Scouted-DemiAutoTargeted-atUnit-hasntMarker{Focus}-targetOpponents-choose1
+++++

.....
Fall Back!
-----
ff4fb461-8060-457a-9c16-000000000196
-----
onPlay:ReturnTarget-Targeted-atUnit
+++++

.....
Fall of the Jedi
-----
ff4fb461-8060-457a-9c16-000000000102
-----

+++++

.....
False Lead
-----
ff4fb461-8060-457a-9c16-000000000195
-----
Placement:Objective||onHostObjectiveThwarted:Lose1Dial
+++++

.....
Fleeing the Empire
-----
ff4fb461-8060-457a-9c16-000000000132
-----
afterRefresh:Put1Shield-AutoTargeted-atUnit_or_Objective-targetMine-choose1-hasntMarker{Shield}-duringMyTurn
+++++

.....
Fleet Command Center
-----
ff4fb461-8060-457a-9c16-000000000190
-----
afterRefresh:Put1Shield-AutoTargeted-atUnit-hasntMarker{Shield}-targetMine-choose1-duringMyTurn
+++++

.....
Fleet Officer
-----
ff4fb461-8060-457a-9c16-000000000134
-----

+++++

.....
Force Choke
-----
ff4fb461-8060-457a-9c16-000000000101
-----
onPlay:Deal1Damage-Targeted-atCharacter_or_Creature
+++++

.....
Force Choke
-----
ff4fb461-8060-457a-9c16-000000000106
-----
onPlay:Deal1Damage-Targeted-atCharacter_or_Creature
+++++

.....
Force Lightning
-----
ff4fb461-8060-457a-9c16-000000000100
-----
onPlay:DestroyTarget-Targeted-atUnit-hasMarker{Focus}
+++++

.....
Force Rejuvenation
-----
ff4fb461-8060-457a-9c16-000000000166
-----
onPlay:Remove999Focus$$Remove999Damage-Targeted-atCharacter
+++++

.....
Force Stasis
-----
ff4fb461-8060-457a-9c16-000000000026
-----
onPlay:Put1Force Stasis-Targeted-atCharacter_or_Creature
+++++

.....
Forgotten Heroes
-----
ff4fb461-8060-457a-9c16-000000000144
-----
whileInPlay:Draw1Card-perCardPlayed-byMe-typeForce User
+++++

.....
Grand Moff Tarkin
-----
ff4fb461-8060-457a-9c16-000000000029
-----

+++++

.....
Guardian of Peace
-----
ff4fb461-8060-457a-9c16-000000000158
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}
+++++
R0:Remove1Damage-DemiAutoTargeted-atCharacter-hasMarker{Damage}-choose1-isCost$$Put1Damage
.....
Guardian of Peace
-----
ff4fb461-8060-457a-9c16-000000000159
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}
+++++
R0:Remove1Damage-DemiAutoTargeted-atCharacter-hasMarker{Damage}-choose1-isCost$$Put1Damage
.....
Han Solo
-----
ff4fb461-8060-457a-9c16-000000000017
-----
onParticipation:Deal1Damage-AutoTargeted-atUnit-targetOpponents-choose1
+++++

.....
Heat of Battle
-----
ff4fb461-8060-457a-9c16-000000000011
-----
onResolveFate:Deal1Damage-DemiAutoTargeted-atUnit-isParticipating-targetOpponents-choose1
+++++

.....
Heat of Battle
-----
ff4fb461-8060-457a-9c16-000000000039
-----
onResolveFate:Deal1Damage-DemiAutoTargeted-atUnit-isParticipating-targetOpponents-choose1
+++++

.....
Heat of Battle
-----
ff4fb461-8060-457a-9c16-000000000090
-----
onResolveFate:Deal1Damage-DemiAutoTargeted-atUnit-isParticipating-targetOpponents-choose1
+++++

.....
Heat of Battle
-----
ff4fb461-8060-457a-9c16-000000000107
-----
onResolveFate:Deal1Damage-DemiAutoTargeted-atUnit-isParticipating-targetOpponents-choose1
+++++

.....
Heat of Battle
-----
ff4fb461-8060-457a-9c16-000000000148
-----
onResolveFate:Deal1Damage-DemiAutoTargeted-atUnit-isParticipating-targetOpponents-choose1
+++++

.....
Heat of Battle
-----
ff4fb461-8060-457a-9c16-000000000213
-----
onResolveFate:Deal1Damage-DemiAutoTargeted-atUnit-isParticipating-targetOpponents-choose1
+++++

.....
Heavy Blaster Emplacement
-----
ff4fb461-8060-457a-9c16-000000000014
-----

+++++
R0:Put1Focus-isCost$$SimplyAnnounce{force the Dark Side to deal 1 damage to a unit they control.}
.....
Heavy Stormtrooper Squad
-----
ff4fb461-8060-457a-9c16-000000000072
-----

+++++

.....
Heavy Stormtrooper Squad
-----
ff4fb461-8060-457a-9c16-000000000073
-----

+++++

.....
Heroic Sacrifice
-----
ff4fb461-8060-457a-9c16-000000000191
-----
onPlay:DestroyMulti-Targeted-atVehicle-hasProperty{Cost}le4
+++++

.....
Hidden Outpost
-----
ff4fb461-8060-457a-9c16-000000000179
-----

+++++

.....
Hidden Outpost
-----
ff4fb461-8060-457a-9c16-000000000184
-----

+++++

.....
Hit and Run
-----
ff4fb461-8060-457a-9c16-000000000210
-----
whileInPlay:Deal1Damage-AutoTargeted-atObjective-isParticipating-perAttackerEdgeWin-ifAttacker-onlyOnce
+++++

.....
Home One
-----
ff4fb461-8060-457a-9c16-000000000181
-----
onStrike:Deal1Damage-AutoTargeted-atObjective-isNotParticipating-targetOpponents-ifAttacker
+++++

.....
Human Replica Droid
-----
ff4fb461-8060-457a-9c16-000000000088
-----

+++++

.....
Human Replica Droid
-----
ff4fb461-8060-457a-9c16-000000000089
-----

+++++

.....
I'm On the Leader
-----
ff4fb461-8060-457a-9c16-000000000130
-----
onPlay:Put1Focus-Targeted-atFighter
+++++

.....
Imperial Command
-----
ff4fb461-8060-457a-9c16-000000000069
-----

+++++

.....
Imperial Navy
-----
ff4fb461-8060-457a-9c16-000000000095
-----

+++++

.....
Imperial Officer
-----
ff4fb461-8060-457a-9c16-000000000036
-----

+++++
R2:Gain1Dial
.....
In You Must Go
-----
ff4fb461-8060-457a-9c16-000000000137
-----
whileInPlay:Reduce1CostPlay-forEnhancement-onlyOnce-byMe
+++++

.....
Interrogation
-----
ff4fb461-8060-457a-9c16-000000000121
-----

+++++

.....
Interrogation Droid
-----
ff4fb461-8060-457a-9c16-000000000122
-----
onPlay:Discard1Card-ofOpponent
+++++

.....
Interrogation Droid
-----
ff4fb461-8060-457a-9c16-000000000123
-----
onPlay:Discard1Card-ofOpponent
+++++

.....
Intimidated
-----
ff4fb461-8060-457a-9c16-000000000124
-----
Placement:Character_and_Unit-byOpponent||onHostStrike:Put1Focus-atHost
+++++

.....
ISB Interrogators
-----
ff4fb461-8060-457a-9c16-000000000125
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}
+++++

.....
It Binds All Things
-----
ff4fb461-8060-457a-9c16-000000000172
-----
onPlay:Draw1Card-fromDiscard-ifHaventForce||onPlay:Draw2Card-fromDiscard-ifHaveForce
+++++

.....
It Could Be Worse
-----
ff4fb461-8060-457a-9c16-000000000203
-----

+++++

.....
It's Worse
-----
ff4fb461-8060-457a-9c16-000000000222
-----
onPlay:Deal1Damage-Targeted-atUnit
+++++

.....
Jedi
-----
ff4fb461-8060-457a-9c16-000000000143
-----

+++++

.....
Jedi in Hiding
-----
ff4fb461-8060-457a-9c16-000000000147
-----

+++++

.....
Jedi in Hiding
-----
ff4fb461-8060-457a-9c16-000000000168
-----

+++++

.....
Jedi Lightsaber
-----
ff4fb461-8060-457a-9c16-000000000066
-----
Placement:Force User_or_Force Sensitive||BonusIcons:UD:1, BD:1
+++++

.....
Jedi Mind Trick
-----
ff4fb461-8060-457a-9c16-000000000003
-----
onPlay:Put2Focus-Targeted-atCharacter_or_Creature-ifHaveForce||onPlay:Put1Focus-Targeted-atCharacter_or_Creature-ifHaventForce
+++++

.....
Jedi Mind Trick
-----
ff4fb461-8060-457a-9c16-000000000171
-----
onPlay:Put2Focus-Targeted-atCharacter_or_Creature-ifHaveForce||onPlay:Put1Focus-Targeted-atCharacter_or_Creature-ifHaventForce
+++++

.....
Jedi Training
-----
ff4fb461-8060-457a-9c16-000000000167
-----
whileInPlay:Force1Bonus
+++++

.....
Kuat Reinforcements
-----
ff4fb461-8060-457a-9c16-000000000046
-----

+++++

.....
Kuati Security Team
-----
ff4fb461-8060-457a-9c16-000000000024
-----

+++++

.....
Kuati Security Team
-----
ff4fb461-8060-457a-9c16-000000000116
-----

+++++

.....
Last Minute Rescue
-----
ff4fb461-8060-457a-9c16-000000000161
-----
afterRefresh:Remove1Damage-AutoTargeted-atUnit-hasDamage-choose1-targetMine-duringMyTurn
+++++

.....
Leia Organa
-----
ff4fb461-8060-457a-9c16-000000000001
-----
onDiscard:CaptureMyself-byMe$$Remove999Focus-AutoTargeted-targetMine-hasMarker{Focus}-byMe
+++++

.....
Lightsaber Deflection
-----
ff4fb461-8060-457a-9c16-000000000157
-----
onPlay:Remove1Damage-Targeted-atUnit_and_nonVehicle-targetMine-isCost$$Deal1Damage-Targeted-atUnit-targetOpponents
+++++

.....
Log Trap
-----
ff4fb461-8060-457a-9c16-000000000207
-----

+++++
Put1Focus-isCost$$SimplyAnnounce{force opponent to put 1 focus one 1 attacking unit}
.....
Looking for Droids
-----
ff4fb461-8060-457a-9c16-000000000217
-----
whileInPlay:IgnoreAffiliationMatch
+++++

.....
Luke Skywalker
-----
ff4fb461-8060-457a-9c16-000000000064
-----
atTurnStart:Remove1Focus-duringOpponentTurn
+++++

.....
Mandalorian Armor
-----
ff4fb461-8060-457a-9c16-000000000078
-----
Placement:Character_and_Unit
+++++

.....
Mission Briefing
-----
ff4fb461-8060-457a-9c16-000000000010
-----
atTurnStart:Draw1Card-duringOpponentTurn
+++++

.....
Mobilize the Squadrons
-----
ff4fb461-8060-457a-9c16-000000000004
-----
afterRefresh:Remove1Focus-AutoTargeted-atEnhancement_or_Objective-hasMarker{Focus}-targetMine-choose1-duringMyTurn
+++++

.....
Mon Mothma
-----
ff4fb461-8060-457a-9c16-000000000013
-----
ConstantEffect:Edge1Bonus
+++++

.....
Nightsister
-----
ff4fb461-8060-457a-9c16-000000000109
-----
onCommit:Deal1Damage-DemiAutoTargeted-atObjective-targetOpponents-choose1
+++++

.....
Nightsister
-----
ff4fb461-8060-457a-9c16-000000000110
-----
onCommit:Deal1Damage-DemiAutoTargeted-atObjective-targetOpponents-choose1
+++++

.....
Obi-Wan Kenobi
-----
ff4fb461-8060-457a-9c16-000000000145
-----

+++++

.....
Orbital Bombardment
-----
ff4fb461-8060-457a-9c16-000000000074
-----
whileInPlay:IncreaseBD:1-byMe-forUnit
+++++

.....
Our Most Desperate Hour
-----
ff4fb461-8060-457a-9c16-000000000146
-----
onPlay:Put1Shield-Targeted-atCharacter
+++++

.....
Outer Rim Hunter
-----
ff4fb461-8060-457a-9c16-000000000077
-----
onAttack:SimplyAnnounce{force opponent to deal 1 damage to one of their objectives}
+++++

.....
Questionable Contacts
-----
ff4fb461-8060-457a-9c16-000000000016
-----
afterRefresh:Put1Damage-isOptional-duringMyTurn$$Remove1Damage-AutoTargeted-atUnit-hasMarker{Damage}-targetMine-choose1-isCost$$Deal1Damage-AutoTargeted-atUnit-targetOpponents-choose1
+++++

.....
R2-D2
-----
ff4fb461-8060-457a-9c16-000000000151
-----

+++++

.....
Rancor
-----
ff4fb461-8060-457a-9c16-000000000111
-----
afterRefresh:CustomScript
+++++

.....
Rebel Alliance
-----
ff4fb461-8060-457a-9c16-000000000173
-----

+++++

.....
Rebel Assault
-----
ff4fb461-8060-457a-9c16-000000000005
-----
onPlay:Deal2Damage-Targeted-atUnit_or_Objective
+++++

.....
Rebel Assault
-----
ff4fb461-8060-457a-9c16-000000000178
-----
onPlay:Deal2Damage-Targeted-atUnit_or_Objective
+++++

.....
Rebel Sympathizer
-----
ff4fb461-8060-457a-9c16-000000000199
-----
whileInPlay:IgnoreAffiliationMatch-onlyforDummy||Reduce1CostPlay-forAll-onlyforDummy||whileInPlay:DestroyMyself-perCardPlayed-onlyforDummy-isSilent
+++++
R0:DestroyMyself-isSilent$$SimplyAnnounce{reduce the cost of the next card they play this phase by 1 and ignore its resource match requirement}$$CreateDummy-isSilent
.....
Rebel Sympathizer
-----
ff4fb461-8060-457a-9c16-000000000200
-----
whileInPlay:IgnoreAffiliationMatch-onlyforDummy||Reduce1CostPlay-forAll-onlyforDummy||whileInPlay:DestroyMyself-perCardPlayed-onlyforDummy-isSilent
+++++
R0:DestroyMyself-isSilent$$SimplyAnnounce{reduce the cost of the next card they play this phase by 1 and ignore its resource match requirement}$$CreateDummy-isSilent
.....
Rebel Trooper
-----
ff4fb461-8060-457a-9c16-000000000194
-----

+++++

.....
Reconnaissance Mission
-----
ff4fb461-8060-457a-9c16-000000000087
-----
whileInPlay:Gain1Reserves
+++++

.....
Red Five
-----
ff4fb461-8060-457a-9c16-000000000150
-----

+++++

.....
Red Two
-----
ff4fb461-8060-457a-9c16-000000000177
-----
whileInPlay:Remove1Focus-perObjectiveThwarted
+++++

.....
Redemption
-----
ff4fb461-8060-457a-9c16-000000000162
-----

+++++

.....
Repair Droid
-----
ff4fb461-8060-457a-9c16-000000000183
-----

+++++
Remove1Damage-DemiAutoTargeted-atVehicle-targetMine-choose1-onlyOnce
.....
Rescue Mission
-----
ff4fb461-8060-457a-9c16-000000000202
-----
onPlay:CustomScript
+++++

.....
Return of the Jedi
-----
ff4fb461-8060-457a-9c16-000000000164
-----
onPlay:CustomScript
+++++

.....
Rookie Pilot
-----
ff4fb461-8060-457a-9c16-000000000006
-----

+++++

.....
Rumors at the Cantina
-----
ff4fb461-8060-457a-9c16-000000000198
-----
whileInPlay:IgnoreAffiliationMatch
+++++

.....
Scum and Villainy
-----
ff4fb461-8060-457a-9c16-000000000093
-----

+++++

.....
Secret Informant
-----
ff4fb461-8060-457a-9c16-000000000211
-----

+++++
CustomScript
.....
Secret Informant
-----
ff4fb461-8060-457a-9c16-000000000212
-----

+++++
CustomScript
.....
Shadows of Dathomir
-----
ff4fb461-8060-457a-9c16-000000000108
-----

+++++

.....
Shii-Cho-Training
-----
ff4fb461-8060-457a-9c16-000000000140
-----
Placement:Force User_and_Unit
+++++

.....
Sith
-----
ff4fb461-8060-457a-9c16-000000000094
-----

+++++

.....
Sith Library
-----
ff4fb461-8060-457a-9c16-000000000025
-----

+++++

.....
Sith Library
-----
ff4fb461-8060-457a-9c16-000000000099
-----

+++++

.....
Sith Library
-----
ff4fb461-8060-457a-9c16-000000000117
-----

+++++

.....
Smugglers and Spies
-----
ff4fb461-8060-457a-9c16-000000000216
-----

+++++

.....
Stolen Plans
-----
ff4fb461-8060-457a-9c16-000000000133
-----
Placement:Objective-byOpponent||onHostGenerate:Draw1Card
+++++

.....
Stormtrooper Elite
-----
ff4fb461-8060-457a-9c16-000000000031
-----

+++++

.....
Superlaser Blast
-----
ff4fb461-8060-457a-9c16-000000000033
-----
onPlay:DestroyTarget-Targeted-atObjective
+++++

.....
Superlaser Engineer
-----
ff4fb461-8060-457a-9c16-000000000030
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}||onPlay:CustomScript
+++++

.....
Swindled
-----
ff4fb461-8060-457a-9c16-000000000020
-----
onPlay:ReturnTarget-Targeted-atUnit-hasProperty{Cost}le2
+++++

.....
Take Them Prisoner
-----
ff4fb461-8060-457a-9c16-000000000052
-----
onPlay:CustomScript
+++++

.....
Tallon Roll
-----
ff4fb461-8060-457a-9c16-000000000043
-----
onPlay:Remove1Focus-Targeted-atFighter
+++++

.....
Tallon Roll
-----
ff4fb461-8060-457a-9c16-000000000051
-----
onPlay:Remove1Focus-Targeted-atFighter
+++++

.....
Target of Opportunity
-----
ff4fb461-8060-457a-9c16-000000000062
-----
onResolveFate:Deal1Damage-AutoTargeted-atObjective-isParticipating-ifAttacker
+++++

.....
Target of Opportunity
-----
ff4fb461-8060-457a-9c16-000000000091
-----
onResolveFate:Deal1Damage-AutoTargeted-atObjective-isParticipating-ifAttacker
+++++

.....
Target of Opportunity
-----
ff4fb461-8060-457a-9c16-000000000131
-----
onResolveFate:Deal1Damage-AutoTargeted-atObjective-isParticipating-ifAttacker
+++++

.....
Target of Opportunity
-----
ff4fb461-8060-457a-9c16-000000000154
-----
onResolveFate:Deal1Damage-AutoTargeted-atObjective-isParticipating-ifAttacker
+++++

.....
Target of Opportunity
-----
ff4fb461-8060-457a-9c16-000000000185
-----
onResolveFate:Deal1Damage-AutoTargeted-atObjective-isParticipating-ifAttacker
+++++

.....
Target of Opportunity
-----
ff4fb461-8060-457a-9c16-000000000215
-----
onResolveFate:Deal1Damage-AutoTargeted-atObjective-isParticipating-ifAttacker
+++++

.....
Tear This Ship Apart
-----
ff4fb461-8060-457a-9c16-000000000057
-----
onPlay:DestroyTarget-Targeted-atEnhancement
+++++

.....
The Bespin Exchange
-----
ff4fb461-8060-457a-9c16-000000000075
-----
whileInPlay:Remove1Focus-AutoTargeted-atObjective-hasMarker{Focus}-choose1-perUnitCardCapturedFromTable
+++++

.....
The Defense of Yavin 4
-----
ff4fb461-8060-457a-9c16-000000000174
-----

+++++

.....
The Emperor's Web
-----
ff4fb461-8060-457a-9c16-000000000096
-----
whileInPlay:Reduce1CostPlay-forEvent_and_Sith-onlyOnce
+++++

.....
The Endor Gambit
-----
ff4fb461-8060-457a-9c16-000000000058
-----
afterRefresh:Remove1Focus-AutoTargeted-atVehicle-hasMarker{Focus}-choose1-duringMyTurn-targetMine
+++++

.....
The Hand's Blessing
-----
ff4fb461-8060-457a-9c16-000000000112
-----
Placement:Character_and_Unit||afterRefresh:Remove999Focus-AutoTargeted-onHost-duringMyTurn
+++++

.....
The Heart of the Empire
-----
ff4fb461-8060-457a-9c16-000000000022
-----
onDiscard:LoseGame-forOwner
+++++

.....
The Rebel Fleet
-----
ff4fb461-8060-457a-9c16-000000000180
-----

+++++

.....
The Secret of Yavin 4
-----
ff4fb461-8060-457a-9c16-000000000155
-----

+++++
CustomScript
.....
The Ultimate Power
-----
ff4fb461-8060-457a-9c16-000000000028
-----

+++++

.....
There Is No Escape
-----
ff4fb461-8060-457a-9c16-000000000027
-----
onPlay:SendToBottomMulti-AutoTargeted-atUnit-warnLotsofStuff
+++++

.....
TIE Advanced
-----
ff4fb461-8060-457a-9c16-000000000128
-----
whileInPlay:Deal1Damage-AutoTargeted-atObjective-isParticipating-perUnopposedEngagement-ifAttacker-ifParticipating
+++++

.....
TIE Attack Squadron
-----
ff4fb461-8060-457a-9c16-000000000041
-----
whileInPlay:Put1TIE Attack Squadron:UD-perResolveFate-byMe-onlyOnce-ifParticipating||afterEngagement:Remove999TIE Attack Squadron:UD-isSilent$$Remove999Activation-isSilent
+++++

.....
TIE Bomber
-----
ff4fb461-8060-457a-9c16-000000000047
-----

+++++

.....
TIE Fighter
-----
ff4fb461-8060-457a-9c16-000000000042
-----

+++++

.....
TIE Fighter
-----
ff4fb461-8060-457a-9c16-000000000048
-----

+++++

.....
Trench Run
-----
ff4fb461-8060-457a-9c16-000000000009
-----
EngagedAsObjective||onPlay:CustomScript||onDiscard:LoseGame-forDark Side
+++++

.....
Tribal Support
-----
ff4fb461-8060-457a-9c16-000000000204
-----

+++++

.....
Trooper Assault
-----
ff4fb461-8060-457a-9c16-000000000056
-----
onPlay:CreateDummy||whileInPlay:IncreaseBD:1-byMe-forTrooper-isAttacking||whileInPlay:IncreaseUD:1-byMe-forTrooper-isAttacking-onlyforDummy||afterEngagement:DestroyMyself-onlyforDummy-isSilent
+++++

.....
Trust Your Feelings
-----
ff4fb461-8060-457a-9c16-000000000065
-----
Placement:Character_and_Unit
+++++
Put1Focus-isCost$$Remove1Focus-AutoTargeted-onHost
.....
Twi'lek Loyalist
-----
ff4fb461-8060-457a-9c16-000000000067
-----

+++++

.....
Twi'lek Loyalist
-----
ff4fb461-8060-457a-9c16-000000000152
-----

+++++

.....
Twi'lek Smuggler
-----
ff4fb461-8060-457a-9c16-000000000018
-----

+++++

.....
Twist of Fate
-----
ff4fb461-8060-457a-9c16-000000000045
-----
onResolveFate:CustomScript
+++++

.....
Twist of Fate
-----
ff4fb461-8060-457a-9c16-000000000092
-----
onResolveFate:CustomScript
+++++

.....
Twist of Fate
-----
ff4fb461-8060-457a-9c16-000000000119
-----
onResolveFate:CustomScript
+++++

.....
Twist of Fate
-----
ff4fb461-8060-457a-9c16-000000000136
-----
onResolveFate:CustomScript
+++++

.....
Twist of Fate
-----
ff4fb461-8060-457a-9c16-000000000160
-----
onResolveFate:CustomScript
+++++

.....
Twist of Fate
-----
ff4fb461-8060-457a-9c16-000000000214
-----
onResolveFate:CustomScript
+++++

.....
Vader's Lightsaber
-----
ff4fb461-8060-457a-9c16-000000000105
-----
Placement:Force User_or_Force Sensitive|||BonusIcons:UD:1
+++++

.....
Vader's TIE Advanced
-----
ff4fb461-8060-457a-9c16-000000000127
-----
onStrike:CustomScript
+++++

.....
Viper Probe Droid
-----
ff4fb461-8060-457a-9c16-000000000218
-----

+++++

.....
Viper Probe Droid
-----
ff4fb461-8060-457a-9c16-000000000219
-----

+++++

.....
Wookiee Navigator
-----
ff4fb461-8060-457a-9c16-000000000193
-----

+++++

.....
X-Wing
-----
ff4fb461-8060-457a-9c16-000000000008
-----

+++++

.....
X-Wing
-----
ff4fb461-8060-457a-9c16-000000000189
-----

+++++

.....
X-Wing Escort
-----
ff4fb461-8060-457a-9c16-000000000188
-----
onDiscard:SimplyAnnounce{force opponent to sacrifice a Vehicle unit they control}
+++++

.....
Y-Wing
-----
ff4fb461-8060-457a-9c16-000000000176
-----

+++++

.....
Y-Wing
-----
ff4fb461-8060-457a-9c16-000000000182
-----

+++++

.....
Yoda
-----
ff4fb461-8060-457a-9c16-000000000138
-----
onStrike:CustomScript
+++++

.....
You're My Only Hope
-----
ff4fb461-8060-457a-9c16-000000000135
-----
onPlay:DestroyTarget-Targeted-atUnit$$Draw2Cards
+++++

.....
Yub Yub!
-----
ff4fb461-8060-457a-9c16-000000000208
-----
onPlay:Put1Focus-Targeted-onEwok-hasntMarker{Focus}$$DestroyTarget-Targeted-atEnhancement
+++++

.....
Yub Yub!
-----
ff4fb461-8060-457a-9c16-000000000209
-----
onPlay:Put1Focus-Targeted-onEwok-hasntMarker{Focus}$$DestroyTarget-Targeted-atEnhancement
+++++

.....
A Message from Beyond
-----
ff4fb461-8060-457a-9c16-000000000223
-----

+++++
R0:Put1Damage$$Retrieve1Card-typeEnhancement-fromDiscard-isTopmost
.....
Battle of Hoth
-----
ff4fb461-8060-457a-9c16-000000000258
-----
onResolveFate:Deal1Damage-Targeted-atObjective_and_Hoth-targetOpponents-noTargetingError||onResolveFate:Remove1Damage-Targeted-atObjective_and_Hoth-targetMine-noTargetingError
+++++

.....
Calm
-----
ff4fb461-8060-457a-9c16-000000000227
-----
onPlay:Remove999Focus-Targeted-atCharacter
+++++

.....
Communications Officer
-----
ff4fb461-8060-457a-9c16-000000000249
-----

+++++

.....
Darth Vader
-----
ff4fb461-8060-457a-9c16-000000000248
-----
whileInPlay:IncreaseBD:1-byMe-forUnit-isAttacking-ifOrigParticipating
+++++

.....
Echo Base Defense
-----
ff4fb461-8060-457a-9c16-000000000229
-----

+++++

.....
Fear
-----
ff4fb461-8060-457a-9c16-000000000244
-----
Placement:Character_and_Unit||onPlay:UncommitTarget-Targeted-atCharacter
+++++

.....
Heat of Battle
-----
ff4fb461-8060-457a-9c16-000000000228
-----
onResolveFate:Deal1Damage-DemiAutoTargeted-atUnit-isParticipating-targetOpponents-choose1
+++++

.....
Hoth Operations
-----
ff4fb461-8060-457a-9c16-000000000235
-----
whileInPlay:Edge1Bonus-perEverySpeeder-AutoTargeted-atSpeeder-targetMine-isParticipating-isDistributedEffect-ifSuperiorityHoth
+++++

.....
Hoth Survival Gear
-----
ff4fb461-8060-457a-9c16-000000000239
-----
Placement:Character_and_Unit
+++++

.....
Icetromper
-----
ff4fb461-8060-457a-9c16-000000000242
-----

+++++
R0:SacrificeMyself$$DisengageTarget-Targeted-atUnit_and_nonVehicle$$Put1Damage-Targeted-atUnit_and_nonVehicle
.....
Icetromper
-----
ff4fb461-8060-457a-9c16-000000000243
-----

+++++
R0:SacrificeMyself$$DisengageTarget-Targeted-atUnit_and_nonVehicle$$Put1Damage-Targeted-atUnit_and_nonVehicle
.....
Imperial Suppression
-----
ff4fb461-8060-457a-9c16-000000000252
-----
onPlay:SimplyAnnounce{cancel the effects of the event card and return it to the top of its owners command deck}$$Put1Effects Cancelled-Targeted-atEvent-isReady-isSilent$$Put1Destination:Command Deck-Targeted-atEvent-isReady-isSilent
+++++

.....
Lord Vader's Command
-----
ff4fb461-8060-457a-9c16-000000000247
-----
whileInPlay:Increase1CostPlay-forEvent-byOpponent-ifOrigHasntMarker{Damage}
+++++

.....
Old Ben's Spirit
-----
ff4fb461-8060-457a-9c16-000000000224
-----
Placement:Character_and_Unit
+++++
R0:DestroyMyself$$Remove999Damage-AutoTargeted-onHost
.....
Old Ben's Spirit
-----
ff4fb461-8060-457a-9c16-000000000225
-----
Placement:Character_and_Unit
+++++
R0:DestroyMyself$$Remove999Damage-AutoTargeted-onHost
.....
Probe Droid
-----
ff4fb461-8060-457a-9c16-000000000250
-----
onDiscard:Put1Damage-DemiAutoTargeted-atObjective-choose1-targetOpponents-byMe
+++++

.....
Probe Droid
-----
ff4fb461-8060-457a-9c16-000000000251
-----
onDiscard:Put1Damage-DemiAutoTargeted-atObjective-choose1-targetOpponents-byMe
+++++

.....
Rogue Three
-----
ff4fb461-8060-457a-9c16-000000000237
-----
onStrike:CustomScript
+++++

.....
Shadows on the Ice
-----
ff4fb461-8060-457a-9c16-000000000253
-----

+++++

.....
Snowspeeder
-----
ff4fb461-8060-457a-9c16-000000000238
-----

+++++

.....
Subzero Defenses
-----
ff4fb461-8060-457a-9c16-000000000233
-----

+++++
R0:DestroyTarget-Targeted-atUnit
.....
Subzero Defenses
-----
ff4fb461-8060-457a-9c16-000000000234
-----

+++++
R0:DestroyTarget-Targeted-atUnit
.....
Succumb to the Cold!
-----
ff4fb461-8060-457a-9c16-000000000256
-----
onPlay:Put1Focus-Targeted-atUnit-targetOpponents
+++++

.....
Succumb to the Cold!
-----
ff4fb461-8060-457a-9c16-000000000257
-----
onPlay:Put1Focus-Targeted-atUnit-targetOpponents
+++++

.....
Target of Opportunity
-----
ff4fb461-8060-457a-9c16-000000000240
-----
onResolveFate:Deal1Damage-AutoTargeted-atObjective-isParticipating-ifAttacker
+++++

.....
The Desolation of Hoth
-----
ff4fb461-8060-457a-9c16-000000000245
-----
onPlay:RequestInt-Msg{How many damage do you want to move to the enemy unit or objective?}$$Remove1Damage-perX-Targeted-atObjective_and_Hoth-targetMine-isCost$$Put1Damage-perX-Targeted-atObjective_and_Hoth_or_Unit-targetOpponents
+++++

.....
The Killing Cold
-----
ff4fb461-8060-457a-9c16-000000000241
-----

+++++
R0:SacrificeTarget-Targeted-atUnit$$Remove1Damage-Targeted-atObjective_and_Hoth-targetMine
.....
Twist of Fate
-----
ff4fb461-8060-457a-9c16-000000000246
-----
onResolveFate:CustomScript
+++++

.....
Wampa
-----
ff4fb461-8060-457a-9c16-000000000254
-----
onPay:Reduce2CostPlay-perEveryHoth-AutoTargeted-atObjective_and_Hoth
+++++

.....
Wampa
-----
ff4fb461-8060-457a-9c16-000000000255
-----
onPay:Reduce2CostPlay-perEveryHoth-AutoTargeted-atObjective_and_Hoth
+++++

.....
Weapon Mastery
-----
ff4fb461-8060-457a-9c16-000000000226
-----
onPlay:RequestInt-Msg{How many enhancements does the target unit have?}$$Put1Weapon Mastery:UD-perX-Targeted-atCharacter$$CreateDummy-isSilent||afterConflict:Remove999Weapon Mastery:UD-AutoTargeted-hasMarker{Weapon Mastery:UD}-isSilent-onlyforDummy$$DestroyMyself-onlyforDummy-isSilent
+++++

.....
Wedge Antilles
-----
ff4fb461-8060-457a-9c16-000000000236
-----
onPlay:CustomScript
+++++
R0:Put1Focus-isCost$$Remove1Focus-AutoTargeted-onHost
.....
Wilderness Fighters
-----
ff4fb461-8060-457a-9c16-000000000230
-----
ExtraIcon:UD:1-perEveryHoth-AutoTargeted-atObjective_and_Hoth-targetMine
+++++

.....
Wilderness Fighters
-----
ff4fb461-8060-457a-9c16-000000000231
-----
ExtraIcon:UD:1-perEveryHoth-AutoTargeted-atObjective_and_Hoth-targetMine
+++++

.....
Wilderness Fighters
-----
ff4fb461-8060-457a-9c16-000000000232
-----
ExtraIcon:UD:1-perEveryHoth-AutoTargeted-atObjective_and_Hoth-targetMine
+++++

.....
AAC-1 Speeder Tank
-----
ff4fb461-8060-457a-9c16-000000000279
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}
+++++

.....
AAC-1 Speeder Tank
-----
ff4fb461-8060-457a-9c16-000000000280
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}
+++++

.....
Admiral's Orders
-----
ff4fb461-8060-457a-9c16-000000000288
-----
onPlay:SimplyAnnounce{reduce the cost of the next capital ship they play this phase by 2}$$CreateDummy-isSilent||whileInPlay:Reduce2CostPlay-forCapital Ship-onlyforDummy||whileInPlay:DestroyMyself-perCardPlayed-typeCapital Ship-onlyforDummy-isSilent
+++++

.....
Death Squadron Command
-----
ff4fb461-8060-457a-9c16-000000000287
-----
whileInPlay:Remove1Focus-perObjectiveThwarted
+++++

.....
Death Squadron Star Destroyer
-----
ff4fb461-8060-457a-9c16-000000000284
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}
+++++

.....
Death Squadron Star Destroyer
-----
ff4fb461-8060-457a-9c16-000000000285
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}
+++++

.....
Deploy the Fleet
-----
ff4fb461-8060-457a-9c16-000000000283
-----
whileInPlay:Reduce1CostPlay-forCapital Ship-onlyforDummy||whileInPlay:DestroyMyself-perCardPlayed-typeCapital Ship-onlyforDummy-isSilent
+++++
R0:SimplyAnnounce{reduce the cost of the next capital ship they play this phase by 1}$$CreateDummy-isSilent-doNotDiscard
.....
Echo Base
-----
ff4fb461-8060-457a-9c16-000000000262
-----
ConstantEffect:Trait{Objective_and_Hoth}1Bonus
+++++

.....
Echo Base Shield Generator
-----
ff4fb461-8060-457a-9c16-000000000263
-----

+++++
R0:Put1Damage-onlyOnce$$Put1Shield-Targeted-atUnit_or_Objective_and_Hoth$$ReturnMyself-ifMarkers{Damage}eq3$$Remove999Damage-ifMarkers{Damage}eq3
.....
Echo Caverns
-----
ff4fb461-8060-457a-9c16-000000000269
-----

+++++
R0:CustomScript
.....
Echo Defender
-----
ff4fb461-8060-457a-9c16-000000000260
-----
ExtraIcon:EE-UD:1-perEveryHoth-AutoTargeted-atObjective_and_Hoth-targetMine
+++++

.....
Echo Defender
-----
ff4fb461-8060-457a-9c16-000000000261
-----
ExtraIcon:EE-UD:1-perEveryHoth-AutoTargeted-atObjective_and_Hoth-targetMine
+++++

.....
First Marker
-----
ff4fb461-8060-457a-9c16-000000000264
-----
Placement:Objective_and_Hoth||ConstantEffect:Protection-fromVehicle-onHost
+++++

.....
Fleet Navigator
-----
ff4fb461-8060-457a-9c16-000000000286
-----

+++++

.....
Get Me Solo!
-----
ff4fb461-8060-457a-9c16-000000000276
-----
onPlay:CaptureTarget-Targeted-atUnit-fromHand
+++++

.....
Hoth Scout
-----
ff4fb461-8060-457a-9c16-000000000278
-----

+++++
R0:SacrificeMyself$$Put1Shield-Targeted-atUnit_or_Objective
.....
Jabba's Orders
-----
ff4fb461-8060-457a-9c16-000000000271
-----

+++++

.....
Jabba's Palace
-----
ff4fb461-8060-457a-9c16-000000000275
-----

+++++

.....
Jawa Trading Crawler
-----
ff4fb461-8060-457a-9c16-000000000274
-----

+++++

.....
Munitions Expert
-----
ff4fb461-8060-457a-9c16-000000000268
-----

+++++
R0:Put1Focus$$Put1Munitions Expert:UD-Targeted-atUnit
.....
Preparation for Battle
-----
ff4fb461-8060-457a-9c16-000000000277
-----
whileInPlay:IncreaseBD:1-byMe-forUnit-hasMarker{Shield}-ifDialge8
+++++

.....
Renegade Squadron
-----
ff4fb461-8060-457a-9c16-000000000266
-----
onStrike:Put1Damage-isOptional$$RescueTarget-Targeted-isCaptured
+++++

.....
Renegade Squadron Mobilization
-----
ff4fb461-8060-457a-9c16-000000000265
-----
whileInPlay:Draw1Card-perUnitDestroyed-forOpponent
+++++

.....
Renegade Squadron Operative
-----
ff4fb461-8060-457a-9c16-000000000267
-----

+++++

.....
Sensors Are Placed
-----
ff4fb461-8060-457a-9c16-000000000259
-----

+++++

.....
Shelter from the Storm
-----
ff4fb461-8060-457a-9c16-000000000282
-----
onPlay:Put1Shield-Targeted-atCharacter-targetMine$$Put1Shelter from the Storm:Protection-Targeted-atCharacter-targetMine
+++++

.....
Target of Opportunity
-----
ff4fb461-8060-457a-9c16-000000000270
-----
onResolveFate:Deal1Damage-AutoTargeted-atObjective-isParticipating-ifAttacker
+++++

.....
Tauntaun
-----
ff4fb461-8060-457a-9c16-000000000281
-----

+++++

.....
Weequay Elite
-----
ff4fb461-8060-457a-9c16-000000000272
-----
onPay:Reduce2CostPlay-perEveryCard-AutoTargeted-isCaptured-maxReduce2
+++++

.....
Weequay Elite
-----
ff4fb461-8060-457a-9c16-000000000273
-----
onPay:Reduce2CostPlay-perEveryCard-AutoTargeted-isCaptured-maxReduce2
+++++

.....
A Dark Time for the Rebellion
-----
ff4fb461-8060-457a-9c16-000000000307
-----
afterRefresh:SimplyAnnounce{force each opponent to deal 1 damage to a unit or objective they control}
+++++

.....
Action-series Bulk Transport
-----
ff4fb461-8060-457a-9c16-000000000298
-----
onStrike:Retrieve1Card-typeCharacter-hasProperty{Cost}le2-toTable-onTop5Cards-isOptional$$ShuffleDeck
+++++

.....
Anger
-----
ff4fb461-8060-457a-9c16-000000000305
-----
Placement:Character||whileInPlay:SacrificeTarget-AutoTargeted-onHost-perForceStruggleLost-duringOpponentTurn
+++++

.....
Anzati Elite
-----
ff4fb461-8060-457a-9c16-000000000304
-----

+++++

.....
Battle of Hoth
-----
ff4fb461-8060-457a-9c16-000000000300
-----
onResolveFate:Deal1Damage-Targeted-atObjective_and_Hoth-targetOpponents-noTargetingError||onResolveFate:Remove1Damage-Targeted-atObjective_and_Hoth-targetMine-noTargetingError
+++++

.....
Carbonite Chamber Activation
-----
ff4fb461-8060-457a-9c16-000000000318
-----
onPlay:Put1Focus-Targeted-atUnit_and_nonVehicle
+++++

.....
Cloud City Incinerator
-----
ff4fb461-8060-457a-9c16-000000000317
-----

+++++
R0:DestroyTarget-Targeted-isCaptured-onlyOnce
.....
Colonel Starck
-----
ff4fb461-8060-457a-9c16-000000000308
-----
ExtraIcon:UD:2-isAttacking-isDamagedObjective||ExtraIcon:BD:2-isAttacking-isDamagedObjective
+++++

.....
Force Push
-----
ff4fb461-8060-457a-9c16-000000000306
-----
onPlay:Put2Focus-Targeted-atUnit_and_nonUnique
+++++

.....
Gotal Outcast
-----
ff4fb461-8060-457a-9c16-000000000290
-----
ExtraIcon:BD:2-ifHaveForce
+++++

.....
Gotal Outcast
-----
ff4fb461-8060-457a-9c16-000000000291
-----
ExtraIcon:BD:2-ifHaveForce
+++++

.....
Heat of Battle
-----
ff4fb461-8060-457a-9c16-000000000294
-----
onResolveFate:Deal1Damage-DemiAutoTargeted-atUnit-isParticipating-targetOpponents-choose1
+++++

.....
Heavy Fire
-----
ff4fb461-8060-457a-9c16-000000000312
-----
onPlay:Put1Heavy Fire:UD-Targeted-atUnit||onPlay:Put1Heavy Fire:BD-Targeted-atUnit
+++++

.....
Ion Cannon Burst
-----
ff4fb461-8060-457a-9c16-000000000299
-----
onPlay:Put1Ion Damaged-Targeted-atUnit_and_Vehicle_or_Unit_and_Droid
+++++

.....
MTV-7
-----
ff4fb461-8060-457a-9c16-000000000309
-----
ExtraIcon:BD:1-isAttacking-isDamagedObjective
+++++

.....
MTV-7
-----
ff4fb461-8060-457a-9c16-000000000310
-----
ExtraIcon:BD:1-isAttacking-isDamagedObjective
+++++

.....
Prepare for Evacuation
-----
ff4fb461-8060-457a-9c16-000000000295
-----

+++++
R0:ReturnTarget-Targeted-atUnit
.....
Prophet of the Dark Side
-----
ff4fb461-8060-457a-9c16-000000000302
-----
onPlay:CustomScript
+++++

.....
Prophet of the Dark Side
-----
ff4fb461-8060-457a-9c16-000000000303
-----
onPlay:CustomScript
+++++

.....
Renegade Squadron Escort
-----
ff4fb461-8060-457a-9c16-000000000296
-----

+++++
R0:Remove1Damage-DemiAutoTargeted-atVehicle-hasMarker{Damage}-choose1-isCost$$Put1Damage
.....
Renegade Squadron Escort
-----
ff4fb461-8060-457a-9c16-000000000297
-----

+++++
R0:Remove1Damage-DemiAutoTargeted-atVehicle-hasMarker{Damage}-choose1-isCost$$Put1Damage
.....
Self Preservation
-----
ff4fb461-8060-457a-9c16-000000000289
-----
ConstantEffect:Force1Bonus-AutoTargeted-atUnit-hasntMarker{Focus}-isCommited-perEveryUnit
+++++

.....
Serve the Emperor
-----
ff4fb461-8060-457a-9c16-000000000301
-----
ConstantEffect:Force1Bonus
+++++

.....
Soresu Training
-----
ff4fb461-8060-457a-9c16-000000000292
-----
Placement:Force User_and_Unit||onHostParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}
+++++

.....
The Hunt for Han Solo
-----
ff4fb461-8060-457a-9c16-000000000313
-----
whileInPlay:Remove1Focus-DemiAutoTargeted-atScum and Villainy-choose1-hasMarker{Focus}-perUnitCardCaptured
+++++

.....
The Moorsh Moraine
-----
ff4fb461-8060-457a-9c16-000000000311
-----
ConstantEffect:Unopposed1Bonus
+++++

.....
Ugnaught
-----
ff4fb461-8060-457a-9c16-000000000314
-----
whileInPlay:Remove1Damage-DemiAutoTargeted-atUnit_and_Vehicle_or_Unit_and_Droid-targetMine-choose1-hasMarker{Damage}-perCardCaptured
+++++

.....
Unwavering Resolve
-----
ff4fb461-8060-457a-9c16-000000000293
-----
onPlay:Put1Unwavering Resolve-Targeted-atUnit-targetMine
+++++

.....
Z-95 Headhunter
-----
ff4fb461-8060-457a-9c16-000000000315
-----
onStrike:CustomScript
+++++

.....
Z-95 Headhunter
-----
ff4fb461-8060-457a-9c16-000000000316
-----
onStrike:CustomScript
+++++

.....

ENDSCRIPTS
=====
'''