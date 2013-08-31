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
onPlay:Deal1Damage-AutoTargeted-atObjective-isCurrentObjective-onlyDuringEngagement-isReact||DeployAllowance:Conflict
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
onThwart:CustomScript-isReact
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
onStrike:Draw1Card-isReact
+++++

.....
Admiral Ackbar
-----
ff4fb461-8060-457a-9c16-000000000187
-----
onPlay:Deal1Damage-AutoTargeted-atUnit-targetOpponents-isParticipating-onlyDuringEngagement-isReact||DeployAllowance:Conflict
+++++

.....
Admiral Motti
-----
ff4fb461-8060-457a-9c16-000000000070
-----
afterCardRefreshing:Remove1Focus-AutoTargeted-atUnit-targetMine-choose1-hasMarker{Focus}-duringMyTurn-isReact
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
Placement:Vehicle_and_Unit||onHostParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough
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
onPlay:Draw1Card-isReact
+++++

.....
AT-ST
-----
ff4fb461-8060-457a-9c16-000000000060
-----
onPlay:Draw1Card-isReact
+++++

.....
AT-ST Commander
-----
ff4fb461-8060-457a-9c16-000000000059
-----

+++++
R1:Put1Shield-AutoTargeted-atUnit_and_Vehicle-isParticipating-targetMine-choose1-hasntMarker{Shield}
.....
Battlefield Engineers
-----
ff4fb461-8060-457a-9c16-000000000015
-----
onAttack:Remove1Focus-AutoTargeted-atEnhancement-choose1-hasMarker{Focus}-isReact
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
R0:Put1Focus-isCost$$Remove1Focus-Targeted-atBlack Squadron
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
R0:CaptureTarget-Targeted-atCharacter
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
R0:DestroyMyself$$SimplyAnnounce{cancel the effects of the event card}$$Put1Effects Cancelled-DemiAutoTargeted-atEvent-isReady-choose1-isSilent
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
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough
+++++

.....
Corporate Exploitation
-----
ff4fb461-8060-457a-9c16-000000000081
-----

+++++
R0:Put1Focus-isCost$$BringToPlayTarget-Targeted-atUnit-fromHand
.....
Coruscant Defense Fleet
-----
ff4fb461-8060-457a-9c16-000000000023
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough
+++++
R0:Remove1Damage-DemiAutoTargeted-atCoruscant-hasMarker{Damage}-choose1-isCost$$Put1Damage
.....
Counsel of the Sith
-----
ff4fb461-8060-457a-9c16-000000000114
-----
atTurnStart:Draw1Card-duringOpponentTurn-isReact
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
onPlay:SacrificeTarget-DemiAutoTargeted-atUnit-targetMine-choose1$$Put1Shield-AutoTargeted-atUnit-targetMine-isParticipating-hasntMarker{Shield}
+++++

.....
Crossfire
-----
ff4fb461-8060-457a-9c16-000000000021
-----
onPlay:Put1Crossfire:UD-Targeted-atCharacter||onPlay:Put1Crossfire:BD-Targeted-atCharacter||onPlay:Put1Crossfire:Tactics-Targeted-atCharacter
+++++

.....
Cruel Interrogations
-----
ff4fb461-8060-457a-9c16-000000000120
-----
onPlay:CustomScript-isReact
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
whileInPlay:Deal1Damage-foreachCardPlayed-byMe-typeEvent_and_Sith-DemiAutoTargeted-atUnit-choose1-targetOpponents-onlyOnce-isReact
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
whileInPlay:Lose1Dial-foreachObjectiveThwarted-byOpponent-isReact
+++++

.....
Defense Protocol
-----
ff4fb461-8060-457a-9c16-000000000040
-----
afterRefresh:Lose1Reserves-duringMyTurn-isReact$$Put1Activation-isSilent$$Deal1Damage-AutoTargeted-atUnit-choose1-targetOpponents||afterDraw:Remove1Activation-duringMyTurn-isCost-isSilent$$Gain1Reserves
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
whileInPlay:Retrieve1Card-grabEvent_and_Sith-fromDiscard-foreachObjectiveThwarted-isReact
+++++

.....
Emperor's Royal Guard
-----
ff4fb461-8060-457a-9c16-000000000098
-----

+++++
R0:Remove1Damage-DemiAutoTargeted-atCharacter-hasMarker{Damage}-choose1-isCost$$Put1Damage
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
onAttack:Put1Ewok Scouted-DemiAutoTargeted-atUnit-hasntMarker{Focus}-targetOpponents-choose1-isReact
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
afterRefresh:SendToBottomTarget-Targeted-fromHand-duringMyTurn-isReact
+++++

.....
False Lead
-----
ff4fb461-8060-457a-9c16-000000000195
-----
Placement:Objective||onHostObjectiveThwarted:Lose1Dial-isReact
+++++

.....
Fleeing the Empire
-----
ff4fb461-8060-457a-9c16-000000000132
-----
afterRefresh:Put1Shield-DemiAutoTargeted-atUnit_or_Objective-targetMine-choose1-hasntMarker{Shield}-duringMyTurn-isReact
+++++

.....
Fleet Command Center
-----
ff4fb461-8060-457a-9c16-000000000190
-----
afterRefresh:Put1Shield-DemiAutoTargeted-atUnit-hasntMarker{Shield}-targetMine-choose1-duringMyTurn-isReact
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
whileInPlay:Draw1Card-foreachCardPlayed-byMe-typeForce User-isReact
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
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough
+++++
R0:Remove1Damage-DemiAutoTargeted-atCharacter-hasMarker{Damage}-choose1-isCost$$Put1Damage
.....
Guardian of Peace
-----
ff4fb461-8060-457a-9c16-000000000159
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough
+++++
R0:Remove1Damage-DemiAutoTargeted-atCharacter-hasMarker{Damage}-choose1-isCost$$Put1Damage
.....
Han Solo
-----
ff4fb461-8060-457a-9c16-000000000017
-----
onParticipation:Deal1Damage-DemiAutoTargeted-atUnit-targetOpponents-choose1-isReact||ConstantAbility:TargetStrike
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
onPlay:SacrificeTarget-Targeted-atVehicle-targetMine$$DestroyTarget-Targeted-atVehicle-hasProperty{Cost}le4-targetOpponents
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
whileInPlay:Deal1Damage-AutoTargeted-atObjective-isParticipating-foreachAttackerEdgeWin-ifOrigAttacking-onlyOnce-isReact
+++++

.....
Home One
-----
ff4fb461-8060-457a-9c16-000000000181
-----
onStrike:Deal1Damage-AutoTargeted-atObjective-isNotParticipating-targetOpponents-ifOrigAttacking-isReact
+++++

.....
Human Replica Droid
-----
ff4fb461-8060-457a-9c16-000000000088
-----
DeployAllowance:Conflict
+++++

.....
Human Replica Droid
-----
ff4fb461-8060-457a-9c16-000000000089
-----
DeployAllowance:Conflict
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
whileInPlay:Reduce1CostPlay-affectsEnhancement-onlyOnce-forMe
+++++

.....
Interrogation
-----
ff4fb461-8060-457a-9c16-000000000121
-----
onPlay:SimplyAnnounce{look at opponent's hand and discard 1 card}
+++++

.....
Interrogation Droid
-----
ff4fb461-8060-457a-9c16-000000000122
-----
onPlay:Discard1Card-ofOpponent-isRandom-isReact
+++++

.....
Interrogation Droid
-----
ff4fb461-8060-457a-9c16-000000000123
-----
onPlay:Discard1Card-ofOpponent-isRandom-isReact
+++++

.....
Intimidated
-----
ff4fb461-8060-457a-9c16-000000000124
-----
Placement:Character_and_Unit-byOpponent||onHostStrike:Put1Focus-atHost-isReact-isForced
+++++

.....
ISB Interrogators
-----
ff4fb461-8060-457a-9c16-000000000125
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough
+++++

.....
It Binds All Things
-----
ff4fb461-8060-457a-9c16-000000000172
-----
onPlay:Draw1Card-fromDiscard-ifHaventForce$$Draw2Card-fromDiscard-ifHaveForce
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
onPlay:Put2Focus-Targeted-atCharacter_or_Creature-ifHaveForce$$Put1Focus-Targeted-atCharacter_or_Creature-ifHaventForce
+++++

.....
Jedi Mind Trick
-----
ff4fb461-8060-457a-9c16-000000000171
-----
onPlay:Put2Focus-Targeted-atCharacter_or_Creature-ifHaveForce$$Put1Focus-Targeted-atCharacter_or_Creature-ifHaventForce
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
R0:Discard0Card-Targeted-fromHand$$Put1Resource:Neutral-AutoTargeted-isUnpaid-perX
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
afterCardRefreshing:Remove1Damage-DemiAutoTargeted-atUnit-hasMarker{Damage}-choose1-targetMine-noTargetingError-duringMyTurn-isReact
+++++

.....
Leia Organa
-----
ff4fb461-8060-457a-9c16-000000000001
-----
onLeaving:Remove999Focus-AutoTargeted-targetMine-hasMarker{Focus}-isReact$$Remove999Focus-AutoTargeted-targetMine-hasMarker{Focus}$$CaptureMyself
+++++

.....
Lightsaber Deflection
-----
ff4fb461-8060-457a-9c16-000000000157
-----
onPlay:Transfer1Damage-Targeted-atUnit-sourceUnit_and_nonVehicle-targetMine-hasMarker{Damage}-destinationUnit
+++++

.....
Log Trap
-----
ff4fb461-8060-457a-9c16-000000000207
-----

+++++
R0:Put1Focus-isCost$$SimplyAnnounce{force opponent to put 1 focus one 1 attacking unit}
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
atTurnStart:Remove1Focus-duringOpponentTurn-isReact||ConstantAbility:TargetStrike
+++++

.....
Mandalorian Armor
-----
ff4fb461-8060-457a-9c16-000000000078
-----
Placement:Character_and_Unit||ConstantAbility:TargetStrike-ifHostBoba Fett
+++++

.....
Mission Briefing
-----
ff4fb461-8060-457a-9c16-000000000010
-----
atTurnStart:Draw1Card-duringOpponentTurn-isReact
+++++

.....
Mobilize the Squadrons
-----
ff4fb461-8060-457a-9c16-000000000004
-----
afterCardRefreshing:Remove1Focus-AutoTargeted-atEnhancement_or_Objective-hasMarker{Focus}-targetMine-choose1-duringMyTurn-isReact
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
onCommit:Deal1Damage-DemiAutoTargeted-atObjective-targetOpponents-choose1-isReact
+++++

.....
Nightsister
-----
ff4fb461-8060-457a-9c16-000000000110
-----
onCommit:Deal1Damage-DemiAutoTargeted-atObjective-targetOpponents-choose1-isReact
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
whileInPlay:IncreaseBD:1-forMe-typeUnit
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
onAttack:SimplyAnnounce{force opponent to deal 1 damage to one of their objectives}-isReact
+++++

.....
Questionable Contacts
-----
ff4fb461-8060-457a-9c16-000000000016
-----
afterCardRefreshing:Put1Damage-duringMyTurn-isReact$$Remove1Damage-DemiAutoTargeted-atUnit-hasMarker{Damage}-targetMine-choose1-isCost$$Deal1Damage-DemiAutoTargeted-atUnit-targetOpponents-choose1
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
afterCardRefreshing:CustomScript-isReact-isForced-duringMyTurn
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
whileInPlay:IgnoreAffiliationMatch-onlyforDummy||Reduce1CostPlay-affectsAll-onlyforDummy||whileInPlay:DestroyMyself-foreachCardPlayed-onlyforDummy-isSilent
+++++
R0:DestroyMyself-isSilent$$SimplyAnnounce{reduce the cost of the next card they play this phase by 1 and ignore its resource match requirement}$$CreateDummy-isSilent-nonUnique
.....
Rebel Sympathizer
-----
ff4fb461-8060-457a-9c16-000000000200
-----
whileInPlay:IgnoreAffiliationMatch-onlyforDummy||Reduce1CostPlay-affectsAll-onlyforDummy||whileInPlay:DestroyMyself-foreachCardPlayed-onlyforDummy-isSilent
+++++
R0:DestroyMyself-isSilent$$SimplyAnnounce{reduce the cost of the next card they play this phase by 1 and ignore its resource match requirement}$$CreateDummy-isSilent-nonUnique
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
onPlay:Gain1Reserves||onThwart:Lose1Reserves
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
whileInPlay:Remove1Focus-foreachObjectiveThwarted-isReact
+++++

.....
Redemption
-----
ff4fb461-8060-457a-9c16-000000000162
-----

+++++
R0:ReturnTarget-Targeted-atUnit-onlyOnce
.....
Repair Droid
-----
ff4fb461-8060-457a-9c16-000000000183
-----

+++++
R0:Remove1Damage-DemiAutoTargeted-atVehicle-targetMine-choose1-onlyOnce
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
R0:CustomScript
.....
Secret Informant
-----
ff4fb461-8060-457a-9c16-000000000212
-----

+++++
R0:CustomScript
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
Placement:Force User_and_Unit||ConstantAbility:ShiiCho
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
Placement:Objective-targetOpponents||onHostGenerate:Draw1Card-isReact
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
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough||onPlay:CustomScript-isReact
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
onPlay:CustomScript-isReact
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
onResolveFate:Deal1Damage-AutoTargeted-atObjective-isParticipating-ifOrigAttacking
+++++

.....
Target of Opportunity
-----
ff4fb461-8060-457a-9c16-000000000091
-----
onResolveFate:Deal1Damage-AutoTargeted-atObjective-isParticipating-ifOrigAttacking
+++++

.....
Target of Opportunity
-----
ff4fb461-8060-457a-9c16-000000000131
-----
onResolveFate:Deal1Damage-AutoTargeted-atObjective-isParticipating-ifOrigAttacking
+++++

.....
Target of Opportunity
-----
ff4fb461-8060-457a-9c16-000000000154
-----
onResolveFate:Deal1Damage-AutoTargeted-atObjective-isParticipating-ifOrigAttacking
+++++

.....
Target of Opportunity
-----
ff4fb461-8060-457a-9c16-000000000185
-----
onResolveFate:Deal1Damage-AutoTargeted-atObjective-isParticipating-ifOrigAttacking
+++++

.....
Target of Opportunity
-----
ff4fb461-8060-457a-9c16-000000000215
-----
onResolveFate:Deal1Damage-AutoTargeted-atObjective-isParticipating-ifOrigAttacking
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
whileInPlay:Remove1Focus-AutoTargeted-atObjective-hasMarker{Focus}-choose1-foreachUnitCardCapturedFromTable-isReact
+++++

.....
The Defense of Yavin 4
-----
ff4fb461-8060-457a-9c16-000000000174
-----

+++++
R0:Discard0Card-Targeted-fromHand$$Put1Resource:Neutral-AutoTargeted-isUnpaid-perX
.....
The Emperor's Web
-----
ff4fb461-8060-457a-9c16-000000000096
-----
whileInPlay:Reduce1CostPlay-affectsEvent_and_Sith-onlyOnce
+++++

.....
The Endor Gambit
-----
ff4fb461-8060-457a-9c16-000000000058
-----
afterCardRefreshing:Remove1Focus-AutoTargeted-atVehicle-hasMarker{Focus}-choose1-duringMyTurn-targetMine-isReact
+++++

.....
The Hand's Blessing
-----
ff4fb461-8060-457a-9c16-000000000112
-----
Placement:Character_and_Unit||afterCardRefreshing:Remove999Focus-AutoTargeted-onHost-duringMyTurn-isReact
+++++

.....
The Heart of the Empire
-----
ff4fb461-8060-457a-9c16-000000000022
-----
onThwart:LoseGame-forOwner
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
R0:CustomScript-isReact-onlyOnce
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
whileInPlay:Deal1Damage-foreachUnopposedEngagement-onTriggerCard-ifOrigAttacking-ifOrigParticipating-isReact
+++++

.....
TIE Attack Squadron
-----
ff4fb461-8060-457a-9c16-000000000041
-----
whileInPlay:Put1TIE Attack Squadron:UD-foreachResolveFate-byMe-onlyOnce-ifOrigParticipating||afterEngagement:Remove999TIE Attack Squadron:UD-isSilent$$Remove999Activation-isSilent
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
EngagedAsObjective||onPlay:CustomScript
+++++

.....
Tribal Support
-----
ff4fb461-8060-457a-9c16-000000000204
-----
afterCardRefreshing:Discard1Card-Targeted-fromHand-duringMyTurn-isCost-isReact$$Retrieve1Card-fromDiscard-grabEwok
+++++

.....
Trooper Assault
-----
ff4fb461-8060-457a-9c16-000000000056
-----
onPlay:CreateDummy-nonUnique||whileInPlay:IncreaseBD:1-forMe-typeTrooper-isAttacking-onlyforDummy||whileInPlay:IncreaseUD:1-forMe-typeTrooper-isAttacking-onlyforDummy||afterEngagement:DestroyMyself-onlyforDummy-isSilent
+++++

.....
Trust Your Feelings
-----
ff4fb461-8060-457a-9c16-000000000065
-----
Placement:Character_and_Unit
+++++
R0:Put1Focus-isCost$$Remove1Focus-AutoTargeted-onHost
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
Placement:Force User_or_Force Sensitive|||BonusIcons:UD:1||ConstantAbility:TargetStrike-ifHostDarth Vader
+++++

.....
Vader's TIE Advanced
-----
ff4fb461-8060-457a-9c16-000000000127
-----
onStrike:CustomScript-isReact
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
whileInPlay:AttackTarget-ifOrigAttacking-ifOrigParticipating-foreachFinishedEngagement-onTriggerCard-isReact
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
onLeaving:SimplyAnnounce{force opponent to sacrifice a Vehicle unit they control}-isReact
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
afterCardRefreshing:Put1Damage$$Retrieve1Card-grabEnhancement-fromDiscard-isTopmost-duringMyTurn-isReact
+++++

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
whileInPlay:IncreaseBD:1-forMe-typeUnit-isAttacking-ifOrigParticipating
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
ConstantEffect:Edge1Bonus-perEverySpeeder-AutoTargeted-atSpeeder-targetMine-isParticipating-isDistributedEffect-ifSuperiorityHoth
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
R0:SacrificeMyself$$DisengageTarget-Targeted-atUnit_and_nonVehicle$$Deal1Damage-Targeted-atUnit_and_nonVehicle
.....
Icetromper
-----
ff4fb461-8060-457a-9c16-000000000243
-----

+++++
R0:SacrificeMyself$$DisengageTarget-Targeted-atUnit_and_nonVehicle$$Deal1Damage-Targeted-atUnit_and_nonVehicle
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
whileInPlay:Increase1CostPlay-affectsEvent-byOpponent-ifOrigHasntMarker{Damage}
+++++

.....
Old Ben's Spirit
-----
ff4fb461-8060-457a-9c16-000000000224
-----
Placement:Character_and_Unit
+++++
R0:Remove999Damage-AutoTargeted-onHost-isReact$$DestroyMyself
.....
Old Ben's Spirit
-----
ff4fb461-8060-457a-9c16-000000000225
-----
Placement:Character_and_Unit
+++++
R0:Remove999Damage-AutoTargeted-onHost$$DestroyMyself
.....
Probe Droid
-----
ff4fb461-8060-457a-9c16-000000000250
-----
onLeaving:Deal1Damage-DemiAutoTargeted-atObjective-choose1-targetOpponents-isReact
+++++

.....
Probe Droid
-----
ff4fb461-8060-457a-9c16-000000000251
-----
onLeaving:Deal1Damage-DemiAutoTargeted-atObjective-choose1-targetOpponents-isReact
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
onResolveFate:Deal1Damage-AutoTargeted-atObjective-isParticipating-ifOrigAttacking
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
onPlay:RequestInt-Msg{How many enhancements does the target unit have?}$$Put1Weapon Mastery:UD-perX-Targeted-atCharacter$$CreateDummy-nonUnique-isSilent||afterConflict:Remove999Weapon Mastery:UD-AutoTargeted-hasMarker{Weapon Mastery:UD}-isSilent-onlyforDummy$$DestroyMyself-onlyforDummy-isSilent
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
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough
+++++

.....
AAC-1 Speeder Tank
-----
ff4fb461-8060-457a-9c16-000000000280
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough
+++++

.....
Admiral's Orders
-----
ff4fb461-8060-457a-9c16-000000000288
-----
onPlay:SimplyAnnounce{reduce the cost of the next capital ship they play this phase by 2}$$CreateDummy-nonUnique-isSilent||whileInPlay:Reduce2CostPlay-affectsCapital Ship-onlyforDummy||whileInPlay:DestroyMyself-foreachCardPlayed-typeCapital Ship-onlyforDummy-isSilent
+++++

.....
Death Squadron Command
-----
ff4fb461-8060-457a-9c16-000000000287
-----
whileInPlay:Remove1Focus-foreachObjectiveThwarted-isReact
+++++

.....
Death Squadron Star Destroyer
-----
ff4fb461-8060-457a-9c16-000000000284
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough
+++++

.....
Death Squadron Star Destroyer
-----
ff4fb461-8060-457a-9c16-000000000285
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough
+++++

.....
Deploy the Fleet
-----
ff4fb461-8060-457a-9c16-000000000283
-----
whileInPlay:Reduce1CostPlay-affectsCapital Ship-onlyforDummy||whileInPlay:DestroyMyself-foreachCardPlayed-typeCapital Ship-onlyforDummy-isSilent
+++++
R0:SimplyAnnounce{damage it in order to reduce the cost of the next capital ship they play this phase by 1}$$CreateDummy-nonUnique-isSilent-doNotDiscard$$Deal1Damage-isSilent
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
Placement:Objective_and_Hoth||ConstantEffect:Protection-typeVehicle-onHost
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
onPlay:SimplyAnnounce{look at opponent's hand}-isReact
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
whileInPlay:IncreaseBD:1-forMe-typeUnit-hasMarker{Shield}-ifDialge8
+++++

.....
Renegade Squadron
-----
ff4fb461-8060-457a-9c16-000000000266
-----
onStrike:Put1Damage-isReact$$RescueTarget-Targeted-isCaptured
+++++

.....
Renegade Squadron Mobilization
-----
ff4fb461-8060-457a-9c16-000000000265
-----
whileInPlay:Draw1Card-foreachCardLeavingPlay-typeUnit-byOpposingOriginController-isReact
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
onResolveFate:Deal1Damage-AutoTargeted-atObjective-isParticipating-ifOrigAttacking
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
afterCardRefreshing:SimplyAnnounce{force each opponent to deal 1 damage to a unit or objective they control}-duringMyTurn-isReact
+++++

.....
Action-series Bulk Transport
-----
ff4fb461-8060-457a-9c16-000000000298
-----
onStrike:Retrieve1Card-grabCharacter-hasProperty{Cost}le2-toTable-onTop5Cards-isReact$$ShuffleDeck
+++++

.....
Anger
-----
ff4fb461-8060-457a-9c16-000000000305
-----
Placement:Character||whileInPlay:SacrificeTarget-AutoTargeted-onHost-foreachForceStruggleLost-duringOpponentTurn-isReact-isForced
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
whileInPlay:DestroyTarget-Targeted-isCaptured-onlyOnce-foreachCardCaptured-ifHaveForce-isReact
+++++

.....
Colonel Starck
-----
ff4fb461-8060-457a-9c16-000000000308
-----
ExtraIcon:UD:2-ifOrigAttacking-isDamagedObjective||ExtraIcon:BD:2-ifOrigAttacking-isDamagedObjective
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
ExtraIcon:BD:1-ifOrigAttacking--isDamagedObjective
+++++

.....
MTV-7
-----
ff4fb461-8060-457a-9c16-000000000310
-----
ExtraIcon:BD:1-ifOrigAttacking--isDamagedObjective
+++++

.....
Prepare for Evacuation
-----
ff4fb461-8060-457a-9c16-000000000295
-----
whileInPlay:ReturnTarget-Targeted-atUnit-foreachObjectiveThwarted-typeHoth-isReact
+++++

.....
Prophet of the Dark Side
-----
ff4fb461-8060-457a-9c16-000000000302
-----
onPlay:CustomScript-isReact
+++++

.....
Prophet of the Dark Side
-----
ff4fb461-8060-457a-9c16-000000000303
-----
onPlay:CustomScript-isReact
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
ConstantEffect:Force1Bonus-AutoTargeted-atUnit-hasntMarker{Focus}-isCommited-targetMine-perEveryUnit
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
Placement:Force User_and_Unit||onHostParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough
+++++

.....
The Hunt for Han Solo
-----
ff4fb461-8060-457a-9c16-000000000313
-----
whileInPlay:Remove1Focus-DemiAutoTargeted-atScum and Villainy-choose1-hasMarker{Focus}-foreachUnitCardCaptured-ifCapturingObjective-isReact
+++++

.....
The Moorsh Moraine
-----
ff4fb461-8060-457a-9c16-000000000311
-----
ConstantEffect:Unopposed2Raise-forMe
+++++

.....
Ugnaught
-----
ff4fb461-8060-457a-9c16-000000000314
-----
whileInPlay:Remove1Damage-DemiAutoTargeted-atUnit_and_Vehicle_or_Unit_and_Droid-targetMine-choose1-hasMarker{Damage}-foreachCardCaptured-isReact
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
onStrike:CustomScript-isReact
+++++

.....
Z-95 Headhunter
-----
ff4fb461-8060-457a-9c16-000000000316
-----
onStrike:CustomScript-isReact
+++++

.....
A Stinging Insult
-----
ff4fb461-8060-457a-9c16-000000000329
-----
onPlay:EngageTarget-Targeted-atUnit-targetOpponents-hasntMarker{Focus}
+++++

.....
Battle of Hoth
-----
ff4fb461-8060-457a-9c16-000000000336
-----
onResolveFate:Deal1Damage-Targeted-atObjective_and_Hoth-targetOpponents-noTargetingError||onResolveFate:Remove1Damage-Targeted-atObjective_and_Hoth-targetMine-noTargetingError
+++++

.....
Battle of Hoth
-----
ff4fb461-8060-457a-9c16-000000000342
-----
onResolveFate:Deal1Damage-Targeted-atObjective_and_Hoth-targetOpponents-noTargetingError||onResolveFate:Remove1Damage-Targeted-atObjective_and_Hoth-targetMine-noTargetingError
+++++

.....
Battle of Hoth
-----
ff4fb461-8060-457a-9c16-000000000354
-----
onResolveFate:Deal1Damage-Targeted-atObjective_and_Hoth-targetOpponents-noTargetingError||onResolveFate:Remove1Damage-Targeted-atObjective_and_Hoth-targetMine-noTargetingError
+++++

.....
Blizzard Force AT-ST
-----
ff4fb461-8060-457a-9c16-000000000339
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough
+++++

.....
Blizzard Force AT-ST
-----
ff4fb461-8060-457a-9c16-000000000340
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough
+++++

.....
Col Serra
-----
ff4fb461-8060-457a-9c16-000000000326
-----
ConstantEffect:Edge1Bonus||ConstantEffect:Protection-ifhasEdge
+++++

.....
Daughters of Allya
-----
ff4fb461-8060-457a-9c16-000000000320
-----
onCommit:Remove1Damage-AutoTargeted-atObjective-hasMarker{Damage}-targetMine-isReact
+++++

.....
Daughters of Allya
-----
ff4fb461-8060-457a-9c16-000000000321
-----
onCommit:Remove1Damage-AutoTargeted-atObjective-hasMarker{Damage}-targetMine-isReact
+++++

.....
Don't Get Cocky
-----
ff4fb461-8060-457a-9c16-000000000330
-----
onPlay:Put2Cocky:BD-Targeted-atUnit-isParticipating
+++++

.....
Explosive Charge
-----
ff4fb461-8060-457a-9c16-000000000347
-----
onPlay:DestroyTarget-Targeted-atEnhancement
+++++

.....
Forward Command Post
-----
ff4fb461-8060-457a-9c16-000000000352
-----
whileInPlay:IncreaseBD:1-forMe-typeUnit-hasMarker{Shield}
+++++

.....
Forward Command Post
-----
ff4fb461-8060-457a-9c16-000000000353
-----
whileInPlay:IncreaseBD:1-forMe-typeUnit-hasMarker{Shield}
+++++

.....
FX-7 Medical Assistant
-----
ff4fb461-8060-457a-9c16-000000000333
-----
onStrike:Remove1AnyTokenType-AutoTargeted-atEnhancement_or_Character-hasMarker{AnyTokenType}-choose1-isReact
+++++

.....
General Veers
-----
ff4fb461-8060-457a-9c16-000000000338
-----
whileInPlay:IncreaseUD:1-forMe-typeWalker_or_Trooper
+++++

.....
Knowledge and Defense
-----
ff4fb461-8060-457a-9c16-000000000319
-----

+++++
R0:ReturnTarget-Targeted-atUnit
.....
Last Defense of Hoth
-----
ff4fb461-8060-457a-9c16-000000000325
-----
afterEngagement:Remove999Activation-isSilent
+++++
R0:CustomScript
.....
Lucrative Contract
-----
ff4fb461-8060-457a-9c16-000000000343
-----
afterCardRefreshing:Remove1Focus-AutoTargeted-atUnit_and_Mercenary_or_Unit_and_Bounty Hunter-targetMine-choose1-hasMarker{Focus}-duringMyTurn-isReact
+++++

.....
Protection
-----
ff4fb461-8060-457a-9c16-000000000324
-----
onResolveFate:Put1Shield-Targeted-atUnit_or_Objective
+++++

.....
Renegade Squadron X-Wing
-----
ff4fb461-8060-457a-9c16-000000000327
-----

+++++
R0:SacrificeMyself$$ReturnTarget-Targeted-atUnit-hasProperty{Cost}le2
.....
Sabotage in the Snow
-----
ff4fb461-8060-457a-9c16-000000000349
-----
afterDeployment:Transfer1Shield-Targeted-sourceAny-hasMarker{Shield}-targetOpponents-destinationAny-hasntMarker{Shield}-targetMine-duringMyTurn-isReact
+++++

.....
Snowtrooper Vanguard
-----
ff4fb461-8060-457a-9c16-000000000351
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough
+++++

.....
The General's Imperative
-----
ff4fb461-8060-457a-9c16-000000000337
-----
onPlay:Gain1Reserves||onDamage:Lose1Reserves||onHeal:Gain1Reserves||onThwart:Lose1Reserves-ifOrigHasntMarker{Damage}
+++++

.....
Turbolaser Battery
-----
ff4fb461-8060-457a-9c16-000000000341
-----
whileInPlay:SacrificeMyself-foreachObjectiveThwarted-byMe-isReact$$DestroyMulti-AutoTargeted-atEnhancement
+++++

.....
Twist of Fate
-----
ff4fb461-8060-457a-9c16-000000000348
-----
onResolveFate:CustomScript-isReact
+++++

.....
WED-15-1016
-----
ff4fb461-8060-457a-9c16-000000000332
-----
afterCardRefreshing:Remove1AnyTokenType-AutoTargeted-atObjective_and_Hoth-hasMarker{AnyTokenType}-choose1-duringMyTurn
+++++

.....
Yoda's Protection
-----
ff4fb461-8060-457a-9c16-000000000322
-----
Placement:Objective||whileInPlay:Put1Shield-AutoTargeted-onHost-hasntMarker{Shield}-foreachEngagedObjective-ifOrigCurrentObjectiveHost-isReact
+++++

.....
Confronting The Terror
-----
ff4fb461-8060-457a-9c16-000000000323
-----
onPlay:SimplyAnnounce{force their opponent to instead divide the damage among any number of units and objectives they control}
+++++

.....
Chewbacca
-----
ff4fb461-8060-457a-9c16-000000000356
-----
onDamage:SimplyAnnounce{deals twice that much damage to a target participating enemy unit}-onlyDuringEngagement-isReact
+++++

.....
Wookiee Warrior
-----
ff4fb461-8060-457a-9c16-000000000357
-----
ExtraIcon:BD:1-ifOrigHasMarker{Damage}||ExtraIcon:UD:1-ifOrigHasMarker{Damage}
+++++

.....
Wookiee Warrior
-----
ff4fb461-8060-457a-9c16-000000000358
-----
ExtraIcon:BD:1-ifOrigHasMarker{Damage}||ExtraIcon:UD:1-ifOrigHasMarker{Damage}
+++++

.....
Let the Wookiee Win
-----
ff4fb461-8060-457a-9c16-000000000359
-----
onPlay:Deal1Damage-DemiAutoTargeted-atUnit-targetMine-choose1$$Deal1Damage-DemiAutoTargeted-atUnit_and_nonVehicle-choose1
+++++

.....
Heat of Battle
-----
ff4fb461-8060-457a-9c16-000000000360
-----
onResolveFate:Deal1Damage-DemiAutoTargeted-atUnit-isParticipating-targetOpponents-choose1
+++++

.....
Raise the Stakes
-----
ff4fb461-8060-457a-9c16-000000000361
-----
ConstantEffect:Unopposed2Raise-forMe-ifOrigHasntMarker{Damage}
+++++

.....
Blockade Runner
-----
ff4fb461-8060-457a-9c16-000000000362
-----

+++++

.....
Cloud City Operative
-----
ff4fb461-8060-457a-9c16-000000000363
-----
onPlay:Transfer1Focus-Targeted-atUnit-sourceUnit-hasMarker{Focus}-destinationUnit-hasProperty{Cost}le2-isReact
+++++

.....
Bothan Spy
-----
ff4fb461-8060-457a-9c16-000000000364
-----
onPlay:SimplyAnnounce{look at opponent's hand}-isReact
+++++

.....
Smuggling Compartment
-----
ff4fb461-8060-457a-9c16-000000000365
-----
Placement:Vehicle
+++++
R0:Draw1Card
.....
Swindled
-----
ff4fb461-8060-457a-9c16-000000000366
-----
onPlay:ReturnTarget-Targeted-atUnit-hasProperty{Cost}le2
+++++

.....
Trust Me
-----
ff4fb461-8060-457a-9c16-000000000367
-----

+++++
Put2Damage$$SimplyAnnounce{cancel the effects of the event card}$$Put1Effects Cancelled-DemiAutoTargeted-atEvent-isReady-choose1-isSilent
.....
Lando Calrissian
-----
ff4fb461-8060-457a-9c16-000000000368
-----

+++++
R1:DisengageTarget-DemiAutoTargeted-atUnit-isParticipating-choose1-onlyOnce
.....
Saboteur
-----
ff4fb461-8060-457a-9c16-000000000369
-----
onPlay:DestroyTarget-Targeted-atEnhancement-hasProperty{Cost}le2-choose1-isReact
+++++

.....
Sabotage
-----
ff4fb461-8060-457a-9c16-000000000371
-----
onPlay:DestroyMultiple-AutoTargeted-atUnit-isParticipating
+++++

.....
Target of Opportunity
-----
ff4fb461-8060-457a-9c16-000000000372
-----
onResolveFate:Deal1Damage-AutoTargeted-atObjective-isParticipating-ifOrigAttacking
+++++

.....
Asteroid Sanctuary
-----
ff4fb461-8060-457a-9c16-000000000373
-----
whileInPlay:Draw1Card-foreachEdgeWin-ifOrigEdgeWinner-isReact
+++++

.....
Millennium Falcon
-----
ff4fb461-8060-457a-9c16-000000000374
-----
ConstantEffect:Edge1Bonus
+++++
R0:ReturnMyself$$BringToPlayTarget-Targeted-atCharacter_or_Droid-fromHand
.....
Cloud City Operative
-----
ff4fb461-8060-457a-9c16-000000000375
-----
onPlay:Transfer1Focus-Targeted-atUnit-sourceUnit-hasMarker{Focus}-destinationUnit-hasProperty{Cost}le2-isReact
+++++

.....
Bamboozle
-----
ff4fb461-8060-457a-9c16-000000000377
-----
onPlay:Transfer1Focus-Targeted-atCharacter-sourceCharacter-hasMarker{Focus}-destinationCharacter
+++++

.....
Twist of Fate
-----
ff4fb461-8060-457a-9c16-000000000378
-----
onResolveFate:CustomScript
+++++

.....
Escape from Ord Mantell
-----
ff4fb461-8060-457a-9c16-000000000379
-----
whileInPlay:Remove1Damage-DemiAutoTargeted-atObjective-hasMarker{Damage}-choose1-foreachCardPlayed-typeEvent-isReact
+++++

.....
Mission Commander
-----
ff4fb461-8060-457a-9c16-000000000380
-----
onStrike:Put1Damage-isReact$$RescueTarget-Targeted-isCapturedCurrentObjective
+++++

.....
Covert Sniper
-----
ff4fb461-8060-457a-9c16-000000000381
-----
afterCardRefreshing:Deal1Damage-DemiAutoTargeted-atUnit-targetOpponents-isCommited-choose1-duringMyTurn-isReact
+++++

.....
Short Range Hauler
-----
ff4fb461-8060-457a-9c16-000000000382
-----

+++++

.....
Bring 'Em On
-----
ff4fb461-8060-457a-9c16-000000000383
-----
onPlay:Put2Bring Em On:UD-Targeted-atUnit-isParticipating
+++++

.....
Over My Dead Body
-----
ff4fb461-8060-457a-9c16-000000000384
-----
onPlay:SimplyAnnounce{cancel the effects of the unit's ability}$$Put1Effects Cancelled-Targeted-atUnit-isReady-isSilent
+++++

.....
Lobot
-----
ff4fb461-8060-457a-9c16-000000000386
-----
whileInPlay:CustomScript-ifOrigParticipating
+++++

.....
Security Control Center
-----
ff4fb461-8060-457a-9c16-000000000389
-----
whileInPlay:Put1Shield-foreachCardPlayed-onTriggerCard-typeUnit-isReact
+++++

.....
Protection
-----
ff4fb461-8060-457a-9c16-000000000390
-----
onResolveFate:Put1Shield-Targeted-atUnit_or_Objective
+++++

.....
Across the Anoat Sector
-----
ff4fb461-8060-457a-9c16-000000000391
-----
whileInPlay:IncreaseBD:1-forMe-typeSmugglers and Spies-isAttacking-isAlone
+++++

.....
Undercover Operative
-----
ff4fb461-8060-457a-9c16-000000000394
-----

+++++

.....
Smuggler's Run
-----
ff4fb461-8060-457a-9c16-000000000395
-----
onPlay:TakeoverTarget-Targeted-atEnhancement-targetOpponents
+++++

.....
Over My Dead Body
-----
ff4fb461-8060-457a-9c16-000000000396
-----
onPlay:SimplyAnnounce{cancel the effects of the unit's ability}$$Put1Effects Cancelled-Targeted-atUnit-isReady-isSilent
+++++

.....
Embers of Hope
-----
ff4fb461-8060-457a-9c16-000000000397
-----
ConstantEffect:PreventDraw-forOpponent-ifOrigHasntMarker{Damage}
+++++

.....
Moisture Farmer
-----
ff4fb461-8060-457a-9c16-000000000398
-----

+++++
R0:Remove1Damage-DemiAutoTargeted-atTatooine-hasMarker{Damage}-choose1-isCost$$Put1Damage
.....
Moisture Farmer
-----
ff4fb461-8060-457a-9c16-000000000399
-----

+++++
R0:Remove1Damage-DemiAutoTargeted-atTatooine-hasMarker{Damage}-choose1-isCost$$Put1Damage
.....
Makashi Training
-----
ff4fb461-8060-457a-9c16-000000000400
-----
Placement:Force User||ConstantAbility:TargetStrike
+++++

.....
Force Precognition
-----
ff4fb461-8060-457a-9c16-000000000401
-----
Placement:Force User
+++++

.....
Secret Guardian ### We use this weird 'whileInPlay' trick because you cannot put markers on cards in your hand, and targeting is wiped when the card is moved by the previous script.
-----
ff4fb461-8060-457a-9c16-000000000402
-----
onPlay:BringToPlayTarget-Targeted-atCharacter-fromHand||whileInPlay:Put1Secret Guardian-foreachCardPlayed-onTriggerCard-typeCharacter-isSilent
+++++

.....
Alderaan's Promise
-----
ff4fb461-8060-457a-9c16-000000000403
-----
onThwart:Gain1Dial-isReact-isForced
+++++

.....
Bail Organa
-----
ff4fb461-8060-457a-9c16-000000000404
-----
ExtraIcon:Tactics:1-perEveryAlderaan-max1-AutoTargeted-atAlderaan_and_Objective||whileInPlay:SacrificeMyself-foreachObjectiveThwarted-typeAlderaan's Promise-isReact-isForced
+++++

.....
Tantive IV
-----
ff4fb461-8060-457a-9c16-000000000405
-----
onPlay:Retrieve1Card-grabUnique-onTop5Cards-isReact$$ShuffleDeck
+++++

.....
Alderaanian Artist
-----
ff4fb461-8060-457a-9c16-000000000406
-----
whileInPlay:SacrificeMyself-foreachObjectiveThwarted-typeAlderaan's Promise-isReact-isForced
+++++

.....
Diplomatic Presence
-----
ff4fb461-8060-457a-9c16-000000000407
-----
Placement:Objective-targetMine
+++++

.....
Misdirection
-----
ff4fb461-8060-457a-9c16-000000000408
-----
onPlay:Transfer1Damage-Targeted-atObjective-targetMine-sourceObjective-targetMine-hasMarker{Damage}-destinationObjective-targetMine
+++++

.....
To Arms!
-----
ff4fb461-8060-457a-9c16-000000000409
-----
whileInPlay:Reduce2CostPlay-affectsEnhancement_and_Weapon-onlyOnce-forMe
+++++

.....
Sullustan Weapon Tech
-----
ff4fb461-8060-457a-9c16-000000000410
-----
whileInPlay:Draw1Card-foreachCardPlayed-typeEnhancement_and_Weapon-forMe-isReact
+++++

.....
Sullustan Weapon Tech
-----
ff4fb461-8060-457a-9c16-000000000411
-----
whileInPlay:Draw1Card-foreachCardPlayed-typeEnhancement_and_Weapon-byMe-isReact
+++++

.....
Han's Heavy Blaster Pistol
-----
ff4fb461-8060-457a-9c16-000000000412
-----
Placement:Character||BonusIcons:UD:1, BD:1||ConstantEffect:Edge1Bonus-perEveryUnit-AutoTargeted-onHost-atHan Solo
+++++

.....
Chewbacca's Bowcaster
-----
ff4fb461-8060-457a-9c16-000000000413
-----
Placement:Character||BonusIcons:UD:1, BD:1
+++++

.....
Hidden Cache
-----
ff4fb461-8060-457a-9c16-000000000414
-----
onPlay:Retrieve1Card-grabEnhancement_and_Weapon$$ShuffleDeck
+++++

.....
Massassi Temple Lookout
-----
ff4fb461-8060-457a-9c16-000000000416
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough-onlyOnce-failSilently||afterEngagement:Pass-onlyOnce-failSilently
+++++

.....
Massassi Temple Lookout
-----
ff4fb461-8060-457a-9c16-000000000417
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough-onlyOnce-failSilently||afterEngagement:Pass-onlyOnce-failSilently
+++++

.....
Ion Cannon Barrage
-----
ff4fb461-8060-457a-9c16-000000000418
-----
onPlay:Remove999Shield-AutoTargeted-hasMarker{Shield}
+++++

.....
Proximity Mine
-----
ff4fb461-8060-457a-9c16-000000000419
-----

+++++
R0:SacrificeMyself$$Deal2Damage-AutoTargeted-atUnit-isAttacking-targetOpponents-isParticipating
.....
Protection
-----
ff4fb461-8060-457a-9c16-000000000420
-----
onResolveFate:Put1Shield-Targeted-atUnit_or_Objective
+++++

.....
Hive of Scum and Villainy
-----
ff4fb461-8060-457a-9c16-000000000421
-----
whileInPlay:DecreaseUD:1-typeUnit-isAttacking-ifOrigCurrentObjective
+++++

.....
Greedo
-----
ff4fb461-8060-457a-9c16-000000000422
-----
whileInPlay:Deal1Damage-foreachEdgeWin-ifOrigEdgeLoser-ifOrigParticipating-isReact-isForced
+++++

.....
Bounty
-----
ff4fb461-8060-457a-9c16-000000000425
-----
Placement:Unit-targetOpponents||whileInPlay:SacrificeMyself-foreachAttackerEdgeWin-ifOrigDefending-ifEdgeDiffge3||whileInPlay:SacrificeMyself-foreachDefenderEdgeWin-ifOrigAttacking-ifEdgeDiffge3||afterCardRefreshing:CaptureHost-duringMyTurn
+++++

.....
Captured
-----
ff4fb461-8060-457a-9c16-000000000426
-----
onPlay:CaptureTarget-Targeted-atUnit
+++++

.....
Jabba's Reach
-----
ff4fb461-8060-457a-9c16-000000000427
-----
whileInPlay:Gain1Reserves-foreachCardCaptured-ifCapturingObjective||whileInPlay:Lose1Reserves-foreachCardRescued-ifCapturingObjective||onThwart:Lose1Reserves-perEveryCard-AutoTargeted-isCaptured-isJailer-noTargetingError
+++++

.....
Jabba the Hutt
-----
ff4fb461-8060-457a-9c16-000000000428
-----

+++++
R0:Put1Focus-isCost$$BringToPlayTarget-Targeted-atUnit_or_Enhancement-hasProperty{Cost}le2-fromHand
.....
Jabba's Pleasure Barge
-----
ff4fb461-8060-457a-9c16-000000000429
-----
afterDeployment:Remove1Focus-DemiAutoTargeted-atCharacter-hasMarker{Focus}-targetMine-choose1-isCost-duringMyTurn-isReact$$Put1Focus
+++++

.....
Reversal of Fate
-----
ff4fb461-8060-457a-9c16-000000000432
-----

+++++

.....
The Tatooine Crash
-----
ff4fb461-8060-457a-9c16-000000000433
-----
afterCardRefreshing:CaptureTarget-AutoTargeted-fromTopDeckOpponents-captureOnMyself-duringMyTurn-isReact
+++++

.....
Jawa Scavenger
-----
ff4fb461-8060-457a-9c16-000000000434
-----
whileInPlay:ReturnMyself-foreachEdgeWin-ifOrigEdgeLoser-isReact-isForced
+++++

.....
Jawa Scavenger
-----
ff4fb461-8060-457a-9c16-000000000435
-----
whileInPlay:ReturnMyself-foreachEdgeWin-ifOrigEdgeLoser-isReact-isForced
+++++

.....
Sandcrawler
-----
ff4fb461-8060-457a-9c16-000000000436
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough||onLeaving:Put1Focus-AutoTargeted-atCharacter_or_Droid-isReact-isForced
+++++

.....
Utinni!
-----
ff4fb461-8060-457a-9c16-000000000437
-----
onPlay:CaptureTarget-Targeted-atEnhancement-targetOpponents
+++++

.....
Twist of Fate
-----
ff4fb461-8060-457a-9c16-000000000438
-----
onResolveFate:CustomScript
+++++

.....
The Shadow of Nar Shaddaa
-----
ff4fb461-8060-457a-9c16-000000000439
-----

+++++
R0:Put2Focus-isCost$$Put1Focus-DemiAutoTargeted-atUnit-isAttacking-choose1
.....
Assassin Droid
-----
ff4fb461-8060-457a-9c16-000000000440
-----

+++++
R0:Remove1Focus
.....
Aqualish Thug
-----
ff4fb461-8060-457a-9c16-000000000441
-----
onPlay:SimplyAnnounce{force each opponent to deal 2 damage divided among any number of objectives he controls.}-isReact
+++++

.....
Aqualish Thug
-----
ff4fb461-8060-457a-9c16-000000000442
-----
onPlay:SimplyAnnounce{force each opponent to deal 2 damage divided among any number of objectives he controls.}-isReact
+++++

.....
Spice Visions
-----
ff4fb461-8060-457a-9c16-000000000443
-----
onPlay:Remove1Focus-Targeted-atCharacter_or_Creature$$Put1Damage-Targeted-atCharacter_or_Creature
+++++

.....
Protection
-----
ff4fb461-8060-457a-9c16-000000000444
-----
onResolveFate:Put1Shield-Targeted-atUnit_or_Objective
+++++

.....
Carbonite Transport
-----
ff4fb461-8060-457a-9c16-000000000445
-----
afterCardRefreshing:CaptureTarget-Targeted-isCaptured-duringMyTurn-isReact
+++++

.....
Slave I
-----
ff4fb461-8060-457a-9c16-000000000446
-----
ExtraIcon:BD:1-perEveryObjective-AutoTargeted-atObjective-hasCaptures-targetMine
+++++

.....
Traitorous Wing Guard
-----
ff4fb461-8060-457a-9c16-000000000447
-----
ExtraIcon:BD:1-perEveryObjective-AutoTargeted-atObjective-hasCaptures-max1-targetMine
+++++

.....
Tractor Beam
-----
ff4fb461-8060-457a-9c16-000000000449
-----
onPlay:Transfer1Focus-Targeted-atVehicle-sourceVehicle-hasMarker{Focus}-destinationVehicle
+++++

.....
Target of Opportunity
-----
ff4fb461-8060-457a-9c16-000000000450
-----
onResolveFate:Deal1Damage-AutoTargeted-atObjective-isParticipating-ifOrigAttacking
+++++

.....
Bossk
-----
ff4fb461-8060-457a-9c16-000000000452
-----
onPlay:Put2Focus-isCost-isReact$$CaptureTarget-DemiAutoTargeted-atCharacter-hasMarker{Focus}-choose1
+++++

.....
Bounty
-----
ff4fb461-8060-457a-9c16-000000000455
-----
Placement:Unit-targetOpponents||whileInPlay:SacrificeMyself-foreachAttackerEdgeWin-ifOrigDefending-ifEdgeDiffge3||whileInPlay:SacrificeMyself-foreachDefenderEdgeWin-ifOrigAttacking-ifEdgeDiffge3||afterCardRefreshing:CaptureHost-duringMyTurn
+++++

.....
Heat of Battle
-----
ff4fb461-8060-457a-9c16-000000000456
-----
onResolveFate:Deal1Damage-DemiAutoTargeted-atUnit-isParticipating-targetOpponents-choose1
+++++

.....
Feeding the Pit
-----
ff4fb461-8060-457a-9c16-000000000457
-----

+++++
R0:DestroyTarget-Targeted-isCaptured$$Remove1Damage$$Draw1Card
.....
Spice Visions
-----
ff4fb461-8060-457a-9c16-000000000461
-----
onPlay:Remove1Focus-Targeted-atCharacter_or_Creature$$Put1Damage-Targeted-atCharacter_or_Creature
+++++

.....
The Almighty Sarlacc
-----
ff4fb461-8060-457a-9c16-000000000462
-----
Placement:Objective_and_Tatooine-targetMine
+++++
R0:Put1Damage-AutoTargeted-onHost$$Remove1Focus-AutoTargeted-onHost
.....
The Ghosts of the Dark Side
-----
ff4fb461-8060-457a-9c16-000000000463
-----
ConstantEffect:Force1Bonus
+++++

.....
Force Wraith
-----
ff4fb461-8060-457a-9c16-000000000464
-----
ConstantEffect:Unwavering
+++++

.....
Force Wraith
-----
ff4fb461-8060-457a-9c16-000000000465
-----
ConstantEffect:Unwavering
+++++

.....
Dark Memories
-----
ff4fb461-8060-457a-9c16-000000000466
-----
Placement:Character-targetOpponents||onHostMarkerAddFocus:Deal1Damage-AutoTargeted-onHost-isReact
+++++

.....
Dark Memories
-----
ff4fb461-8060-457a-9c16-000000000467
-----
Placement:Character-targetOpponents||onHostMarkerAddFocus:Deal1Damage-AutoTargeted-onHost-isReact
+++++

.....
Force Shockwave
-----
ff4fb461-8060-457a-9c16-000000000468
-----
onPlay:Deal1Damage-AutoTargeted-atUnit-isNotCommited-targetOpponents
+++++

.....
Imperial Blockade
-----
ff4fb461-8060-457a-9c16-000000000469
-----
whileInPlay:Increase1CostPlay-affectsUnit-byOpponent-ifOrigHasntMarker{Damage}-onlyOnce
+++++

.....
Captain Needa
-----
ff4fb461-8060-457a-9c16-000000000470
-----
whileInPlay:Reduce2CostPlay-affectsCapital Ship-onlyOnce-forMe
+++++

.....
Apology Accepted
-----
ff4fb461-8060-457a-9c16-000000000473
-----
onPlay:SacrificeTarget-Targeted-atUnit_and_Imperial Navy_and_Officer$$Remove999Focus-Targeted-atUnit_and_Imperial Navy_and_Vehicle
+++++

.....
Tractor Beam
-----
ff4fb461-8060-457a-9c16-000000000474
-----
onPlay:Transfer1Focus-Targeted-atVehicle-sourceVehicle-hasMarker{Focus}-destinationVehicle
+++++

.....
Across the Jundland Wastes
-----
ff4fb461-8060-457a-9c16-000000000475
-----
whileInPlay:Put1Focus-foreachUnitStrike-onTriggerCard-typeCharacter-isReact-isForced
+++++

.....
Bantha
-----
ff4fb461-8060-457a-9c16-000000000476
-----
whileInPlay:Retrieve1Card-grabEnhancement-fromDiscard-isTopmost-foreachCardPlayed-typeScavenger-isReact
+++++

.....
Tusken Raider
-----
ff4fb461-8060-457a-9c16-000000000477
-----
onStrike:ReturnMyself-isReact
+++++

.....
Tusken Raider
-----
ff4fb461-8060-457a-9c16-000000000478
-----
onStrike:ReturnMyself-isReact
+++++

.....
Tusken Raider
-----
ff4fb461-8060-457a-9c16-000000000479
-----
onStrike:ReturnMyself-isReact
+++++

.....
Gaffi Stick
-----
ff4fb461-8060-457a-9c16-000000000480
-----
Placement:Scavenger||ConstantEffect:Edge1Bonus-perEveryUnit-AutoTargeted-atUnit-targetMine-isParticipating-isDistributedEffect-ignore1-ifOrigParticipatingHost
+++++

.....
Asteroid Pursuit
-----
ff4fb461-8060-457a-9c16-000000000481
-----
afterCardRefreshing:Deal1Damage-duringMyTurn-isReact-isForced
+++++

.....
Lictor-class Dungeon Ship
-----
ff4fb461-8060-457a-9c16-000000000482
-----
ExtraIcon:UD:1-perEveryObjective-AutoTargeted-atObjective-hasCaptures-max1-targetMine||ExtraIcon:BD:1-perEveryObjective-AutoTargeted-atObjective-hasCaptures-max1-targetMine
+++++

.....
Trooper Sentry
-----
ff4fb461-8060-457a-9c16-000000000483
-----
onPlay:Put1Shield-DemiAutoTargeted-atUnit_or_Objective-choose1-isReact
+++++

.....
Trooper Sentry
-----
ff4fb461-8060-457a-9c16-000000000484
-----
onPlay:Put1Shield-DemiAutoTargeted-atUnit_or_Objective-choose1-isReact
+++++

.....
Armed and Ready
-----
ff4fb461-8060-457a-9c16-000000000485
-----
onPlay:CreateDummy-nonUnique||whileInPlay:IncreaseBD:1-forMe-typeUnit-hasMarker{Shield}-onlyforDummy||whileInPlay:IncreaseUD:1-forMe-typeUnit-hasMarker{Shield}-onlyforDummy||afterPhase:DestroyMyself-onlyforDummy-isSilent
+++++

.....
Protection
-----
ff4fb461-8060-457a-9c16-000000000486
-----
onResolveFate:Put1Shield-Targeted-atUnit_or_Objective
+++++

.....
501st Trooper
-----
ff4fb461-8060-457a-9c16-000000000506
-----
ExtraIcon:BD:1-ifOrigAttacking-hasObjectiveTrait-typeHoth
+++++

.....
501st Trooper
-----
ff4fb461-8060-457a-9c16-000000000507
-----
ExtraIcon:BD:1-ifOrigAttacking-hasObjectiveTrait-typeHoth
+++++

.....
Aggressive Assault
-----
ff4fb461-8060-457a-9c16-000000000516
-----
onPlay:Deal1Damage-AutoTargeted-atObjective-targetOpponents
+++++

.....
AT-AT
-----
ff4fb461-8060-457a-9c16-000000000512
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough||onStrike:DestroyTarget-Targeted-atEnhancement-isStrikeAlternative-isReact
+++++

.....
AT-AT
-----
ff4fb461-8060-457a-9c16-000000000513
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough||onStrike:DestroyTarget-Targeted-atEnhancement-isStrikeAlternative-isReact
+++++

.....
AT-AT Assault Formation
-----
ff4fb461-8060-457a-9c16-000000000514
-----
onParticipation:Put1Shield-AutoTargeted-atUnit_or_Objective-isParticipating-targetMine-choose1-hasntMarker{Shield}-notHARDCOREenough||onStrike:Deal1Damage-AutoTargeted-atObjective_and_Hoth-targetOpponents-isReact
+++++

.....
Attack Pattern Delta
-----
ff4fb461-8060-457a-9c16-000000000487
-----
   
+++++
R0:Retrieve1Card-grabVehicle-hasProperty{Cost}le2-toTable-onTop1Cards-tellPlayer-isReact-onlyOnce
.....
Battle of Hoth
-----
ff4fb461-8060-457a-9c16-000000000492
-----

+++++

.....
Battle of Hoth
-----
ff4fb461-8060-457a-9c16-000000000504
-----
onResolveFate:Deal1Damage-Targeted-atObjective_and_Hoth-targetOpponents-noTargetingError||onResolveFate:Remove1Damage-Targeted-atObjective_and_Hoth-targetMine-noTargetingError
+++++

.....
Battle of Hoth
-----
ff4fb461-8060-457a-9c16-000000000510
-----
onResolveFate:Deal1Damage-Targeted-atObjective_and_Hoth-targetOpponents-noTargetingError||onResolveFate:Remove1Damage-Targeted-atObjective_and_Hoth-targetMine-noTargetingError
+++++

.....
Coordinated Strike
-----
ff4fb461-8060-457a-9c16-000000000503
-----
onPlay:SimplyAnnounce{immediately strike again with another ready participating unit they control}
+++++

.....
E-Web Heavy Repeating Blaster
-----
ff4fb461-8060-457a-9c16-000000000509
-----

+++++
R0:Put1Focus-isCost-isSilent$$Put1EWeb Heavy Repeating Blaster:BD-Targeted-atTrooper-isSilent
.....
Hold-out Blaster
-----
ff4fb461-8060-457a-9c16-000000000496
-----
Placement:Smugglers and Spies_and_Character||BonusIcons:Double-ifOrigHasLess-typeUnit
+++++

.....
Hoth Rearguard
-----
ff4fb461-8060-457a-9c16-000000000500
-----

+++++
R0:Remove1Damage-DemiAutoTargeted-atHoth-hasMarker{Damage}-choose1-isCost$$Put1Damage
.....
Hoth Rearguard
-----
ff4fb461-8060-457a-9c16-000000000501
-----

+++++
R0:Remove1Damage-DemiAutoTargeted-atHoth-hasMarker{Damage}-choose1-isCost$$Put1Damage
.....
Hoth Rearguard
-----
ff4fb461-8060-457a-9c16-000000000502
-----

+++++

.....
Narrow Escape
-----
ff4fb461-8060-457a-9c16-000000000497
-----
onPlay:SimplyAnnounce{choose a new target for the effect}
+++++

.....
Orbital Resupply Station
-----
ff4fb461-8060-457a-9c16-000000000515
-----
whileInPlay:Reduce1CostPlay-affectsUnit_and_Vehicle_and_Imperial Navy-hasProperty{Cost}ge4-forMe
+++++

.....
Rogue Leader
-----
ff4fb461-8060-457a-9c16-000000000488
-----
ExtraIcon:Tactics:1-perEveryRogueTwo-AutoTargeted-atRogue Two-targetMine
+++++

.....
Rogue Two
-----
ff4fb461-8060-457a-9c16-000000000489
-----
ExtraIcon:EE-BD:1-perEverySpeeder-AutoTargeted-atSpeeder-targetMine-isAttacking-isParticipating
+++++

.....
Shadow Operative
-----
ff4fb461-8060-457a-9c16-000000000494
-----

+++++
R0:ReturnMyself
.....
Shadow Operative
-----
ff4fb461-8060-457a-9c16-000000000495
-----

+++++
R0:ReturnMyself
.....
Snowspeeder Launch Bay
-----
ff4fb461-8060-457a-9c16-000000000491
-----
whileInPlay:Deal1Damage-Targeted-atVehicle-targetOpponents-foreachUnitStrike-typeSpeeder-isReact-onlyOnce$$Put1Focus-Targeted-atVehicle_and_Walker-targetOpponents
+++++

.....
Tactical Retreat
-----
ff4fb461-8060-457a-9c16-000000000498
-----
onPlay:ReturnMulti-Targeted-atUnit-targetMine
+++++

.....
Undercover Dealings
-----
ff4fb461-8060-457a-9c16-000000000493
-----
afterCardRefreshing:Draw999Cards-ifOrigHasLess-typeUnit-duringOpponentTurn-isReact
+++++

.....
Vader's Fist
-----
ff4fb461-8060-457a-9c16-000000000505
-----
onPlay:Lose1Reserves-onOpponent||onDamage:Gain1Reserves-onOpponent||onHeal:Lose1Reserves-onOpponent||onThwart:Gain1Reserves-onOpponent-ifOrigHasntMarker{Damage}
+++++

.....

ENDSCRIPTS
=====
'''