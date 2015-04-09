Changelog - Star Wars LCG OCTGN Game Definition
===============================================
### 2.15.1.x

Objective and button sizes have been fixes (thank to killerangel1863)

### 2.15.0.x

Draw Their Fire set added; limited automations on some cards.

### 2.14.0.x

Ready for Takeoff set added; limited automations on some cards.

### 2.13.0.x

Between the Shadows set added; Old fate cards (Heat, ToO) have been scripted, as has Pay Out and the Security Task Force cards.

### 2.12.0.x

Large batch of Echoes cycle script added by BolivarShagnasty; roughly half have been tested. Take special note of the following:

*All Echoes of the Force should now work
*All Seeds of Decay should now work
*All Force Struggle Resources should work
*Believer Initiate is not a constant effect, only on Force Struggle resolve
*Hate works, but token it places to cancel text must be manually removed if Hate is moved
*Salacious Crumb only works for 1 Focus on any Character; if Jabba you need to manually remove the second Focus

The following scripts are untested; if they do not work, please file an issue here: https://github.com/BolivarShagnasty/Star-Wars-LCG-OCTGN/issues :
*Zuckuss 
*Flight of the Crow
*My Ally is the Force 
*The Hoth Gambit
*Carlist Rieekan 
*Snowspeeder Counterattack
*Hyperspace Marauder 
*Hired Hands
*Make Your Own Luck 
*Sariss
*Slave Trade Galactic 
*Scum
*May the Force Be With You 
*Winter
*Tactical Genius
*Infiltration - must manually engage card
*Force Shield 
*Facility Repair
*Consumed by the Dark Side 
*Green Squadron A-Wing
*Reinforcements - must manually commit card
*Security Checkpoint 
*Award Ceremony - must manually commit card

### 2.10.0.x

* Added **Darkness and light**. Some basic automations included from SmokeyJ

### 2.10.0.x

* Added **It Binds All Things**. Some basic automations included

### 2.9.0.x

* Added Join Us or Die

### 2.7.6.x

Fixed LotDS keywords

### 2.7.5.x

* Implemented Reconnections


### 2.7.4.x

Added some basic automations for H&L and LotDS


### 2.7.3.x

Lure of The Dark Side added unscripted

### 2.7.2.x

Fixed some bad blocks and traits

### 2.7.0.x

* Heroes and Legends added unscripted

### 2.6.5.x

* Tying in BOTD now scripts as if the current holder is the winner

### 2.6.4.x

* Balance of the Force now scripted. Some notes:
  * Shistavanen Wolfman won't trigger from your discard pile. You have to play him manually when you win the force struggle accordingly.
  * Rapid Fire doesn't enforce the targets. Just make sure you select units from different opponents.
  * Arcona Rumor Monger: Not rules enforced
  * Trandoshan Security Team: Not rules enforced.
  * A Price on their heads doesn't enforce the targets. Just make sure you select units from different opponents.
  * Dash Rendar cannot be triggered by a player who doesn't control him but once they are triggered any ally can play their cost normally.
* Stopped cards from triggering their reacts while previous triggers are already waiting.  
* Moving captured cards from one objective to another will properly mention that they're just being transferred and the objectives involved.

### 2.6.3.x

* Allied participating units will now pass control to the main players to allow cards like Orbital Bombardment to work correctly
* Fixed Jawa Scavenger triggering when allies were the main players.
* Reviewed all cards until Edge of Darkness for MP-tweaking


### 2.6.2.x

* Made game 2v2 compatible (Added Common Reserves and code for it etc)
* Leia Organa will now properly ask the captor on which objective to go to.
* Moving cards around manually will carry their attached cards with them. This means objectives moving in the refresh phase will take their attachments will them finally.
* Made phase changes common for each team.
* Made cards like Vader's Fist and Interrogation Droid work properly in multiplayer.
* In MP the game will now ask which opponent you're targeting when only one needs to be selected.
* Playing Edge cards as an ally should now stack with the main player's other edge cards.
* Can now target a card and press Del to discard it. This way you can destroy objectives and units from your opponent yourself.

### 2.6.1.x

* Resampled all sounds to 44100
* Added placement code which can also handle 2v2, 2v1 and 3v1

### 2.6.0.x

* Added Balance of the Force unscripted

### 2.5.2.x

* Fixed Luke Skywalker as attachment. Now gives Tactics instead of BD

### 2.5.1.x

* Escape from Hoth now scripted. Some notes:
  * Luke Skywalker, to use his ability, make sure you've targeted an appropriate unit when you play him. 
  * Executor's ability will only fire with cards which cause a sacrifice through scripts. If you destroy a unit by mousing over it and pressing delete, you will have to trigger its ability manually, by double-clicking it.
  * ISB Liaison not fully automated. It sacrifices but just announces its ability. Simply look at the relevant card manually and then draw a card.
  * Aggression not automated. It just announces.
* Leia won't trigger if captured from hand.
* Captured Units or ones in Edge stacks won't appear as strike choices anymore
* "It could be worse" now will remove 1 damage from a target.
* Carbonite Transport shouldn't reveal the card name to the opponent anymore.

### 2.5.0.x

* **Escape from Hoth** added unscripted

### 2.4.6.x

* Multiple Choices for Tactics or UD will now paginate if there's more than 7 possible choices
* Proximity Mine won't damage non-participating units now.
* Abilities from objectives which turn off when they're damaged, will not turn off if they get damaged with more than 1 damage at a time.
* Questionable Contacts and Han Solo's Ability will now use the targeted unit if it exists
* SnowSpeeder Launch Bay is now only once per turn

### 2.4.5.x

* Improved Strikes further.
  * Now game will ask if you want to use Tactics or Unit Damage first if you have both and will announce the order they were used.
  * Game will now take into account if a unit has targeted strike, and will ignore non-participating targeted units if it doesn't.
  * Game will now confirm with the player if they want to allow it to auto-target, in case they forgot to target units before they strike. This will attempt to figure out which units are valid targets and provide a selection window.
  * Pressing cancel on selecting units (or not using automatic discovery), will not put the tokens anywhere, allowing for manual placement.
* Scripted Crossfire
* Changed timing of Message from beyond to trigger after Refresh
* Added an announcement to Confronting the Terror
* Added Targeted Strike script to all the appropriate cards

### 2.4.4.x

* Fixed Prophet of the Dark Side.
* Added some commands while viewing the command and objective deck. This will allow you to play specific objectives, or draw specific cards by double clicking on them
* Fixed Old Ben's Spirit


### 2.4.3.x

* **Significant** Strikes which have Tactics and Damage, or Tactics>1 will actually ask the player for the right targets. A multiple choice menu will appear for all the units you've targeted, and you'll be able to select which units to damage and which to focus
* When striking without a target, the game will try to smartly figure out who your target might be and ask for instuctions if confused.
* Automated Shii-Cho Training
* Echo Base shouldn't provide a bonus as an edge card anymore
* Rogue Two should not get bonuses from non-participating units

### 2.4.2.x

* Enabled Statistics Gathering

### 2.4.1.x

* Orbital Resupply Station should now properly only affect units with cost >= 4

### 2.4.0.x

* **The Battle of Hoth** has been added fully scripted!
* Now Deck Checking Happens on Deck load
* Now fresh script grabbing happens on game start
* Death Star Dial will be adjusted for both players when one does it manually.
* Game will clear card attachments when someone manually moves a card away from the table.

### 2.3.13.x

* Added third button to be used to notify your opponent that you're giving them an opportunity to play actions
* Added an option in the Game menu to permanently disable the buttons

### 2.3.12.x

* Sounds how now been activated. About 100 different sound effects included!

### 2.3.11.x

* Returning Units to hand will now discard their enhancements.
* Jabba's Orders now has a proper react trigger that simply announces its effect. You need to the rest manually
* Greedo will only trigger when participating now.
* Deploy the Fleet will now get damaged when used.
* Deploy the Fleet can now spawn more than 1 reduction effect.
* Dummy Cards (resident effects) will now spawn further up and stack for visibility.
* Dummy Cards (resident effects) will now inform about their purpose once per player.
* Leia will now clear player's focus tokens rather than opponent's.
* Leia will now properly clear all focus tokens.
* Fleeing the empire will now autoselect targeted cards.
* Renegade Squadron Mobilization will now trigger correctly only at opponent's units leaving the table.
* Edge Card placements will now reset properly.
* Tatooine Crash will capture automatically at itself, without asking.
* Changed Yoda's and Rogue Three's icons to be more generically named

### 2.3.10.x

* HARDCORE mode setting will now be retained between sessions.
* The information window about triggers will only appear once per player.
* Each new MOTD will appear once per player.
* Prepared for Stat Submission but not activated yet as missing the web form.
* Added keyborad shortcuts reference card to the documents menu.

### 2.3.9.x

* Implemented new placement defaults and the ability to be placing your units in a left-aligned formation. This setting will be retained between sessions.
* If people drag units outside the table, the unit placeent won't start zooming out of the table in an attempt to find free space.
* Forced effects of cards which have been manually dragged out of the table will be silenced at next phase change now.

### 2.3.8.x

* Fixed Moorsh Moraine and Raise the Stakes unopposed bonus stacking
* Fixed Greedo and Jawa Scavengers not triggering sometimes.
* Changed the Button art to make more sense thematically :)
* Darth Vader (Sith) will now choose any targeted cards if they exist.
* Fixed Bounty not triggering on Refresh
* Fixed Preparation for Battle always triggering if Dial is above 8
* Fixed Self-Preservation giving LS extra force for each committed DS unit, when the DS calculated the force struggle. Regression Bugs might have been introduced with this fix though, lemme know if you see anything weird.

### 2.3.7.x

* Fixed Gaffi Stick firing outside of engagement
* Fixed Asteroid Sanctuary
* Fixed Carbonite Transport

### 2.3.6.x

Fixed Alternate Affiliations not having resources and not clearing Edge

### 2.3.5.x

* Added a little surprise :)

### 2.3.4.x

* Added a Pause and a Wait button to allow some quick communication

### 2.3.3.x

* Card played as edge should not reduce costs or provide extra combat icons anymore.

### 2.3.2.x

* Consolidated Automation switches and added switch to disable them all together.
* During Multiple Choice Targeting windows, cards will now mention how many captures and attachments they have.
* Tie Advanced and Wookie Navigator should now work more robustly. 

### 2.3.1.x

* Fixed Wraiths not participating when focused and opponent calculates the force struggle.
* Made info window higher
* Fixed Imperial Blockade not increasing costs.
* Made Chewie have a react window, but his ability still doesn't put the damage, just announces it.
* Fixed Various Wrong timings on "After Refresh" triggers.
* Fixed Wookie Warriors added icons.
* Fixed Various Typos

### 2.3.0.x

* **Very Significant:** Completely reworked the way automations work functionally. Reacts and Interrupts no longer trigger automatically during phase changes or specific triggers, rather, cards which have a relevant react/interrupt will now simply highlight themselves at the appropriate moment, much like events, at which point you can simply double-click on them to signify you're using their effect.
  While they are highlighted, your opponent also has the chance to play interrupts which will cancel their effects, such as "Over My Dead Body". 
  Cards which have normal actions, will highlight after your double clicked them and paid their cost, at which point your opponent has a chance to interrupt and afterward you must double click them again to release their effect.
  The highlight phase will also give you an opportunity to target the appropriate cards if you need to.
  Reacts/Interrupts available for use will only remain active for one phase. As soon as someone pressed [ctrl]+[Enter], all unused triggers will disappear.
  Forced Reacts/Interrupts will not disappear until you use them.
  To signify you don't want to use a react, either ignore it until the phase changes, or use the built-in action "Ignore Card Trigger" [Ctrl]+[Z] on the card.
  Effects which are built-in to the cards, such as cost-reductions, shielding and other things which cannot be interrupted, will work automatically as before. You don't need to trigger them manually.
* **Significant:** Scripted almost all Edge of Darkness cards
  * **Cards not scripted:**
    * Wookie Life Debt (Just drag the damage tokens afterwards manually)
    * Chewbacca
    * Blockade Runner
    * Bothan Spy
    * Cloud City Wing Guard/Chewbaca Bowcaster strike "outside of combat" (Just use the manual "Strike" ability in the card's context menu.)
    * Sleuth Scout
    * Undercover Operative
    * Force Precognition
    * Opening Moves (Just attack the appropriate objective)
    * Reversal of Fate (Just grab the edge manually as required)
    * Spice Visions
    * Bib Fortuna
    * Krayt Dragon (Just don't play any enhancements on it)
  * **Cards with tricky scripting:**
    * Smuggling Compartment - Just double click the enhancement to draw a card and notify why)
    * Millennium Falcon - Target the unit in your hand and then use the Falcon's ability
    * Assassin Droid (Just use its ability to remove a focus)
    * Tractor Beam (Does not check the printed costs)
    * Bossk (Drawing the cards is not automated)
    * Trandoshan Hunter (Just Target the non-participating Wookie)
* Added **HARDCORE** mode. Unleash it from the Game Menu. Hardcore mode is built with the people who want a close experience to the real tabletop, without sacrificing all automations. 
  During HARDCORE mode, your cards will not highlight when their trigger is reached and will not announce it on the chat either. You will need to double click on a card during the appropriate time window at which point it will highlight and announce that your are attempting to use it, to give your opponent a chance to play interrupts.
  HARDCORE mode only affects your cards. If your opponent is not using it, then their own triggers will be automatically highlighted as usual.
  This will not affect innate effects which cannot be interrupted, such as Shielding or Cost Reductions. These will work automatically as usual. Forced effects will also always be highlighted to prevent illegal plays. In other words, HARDCORE mode only affects Reacts and Interrupts.
* Lots of added automations for cards which didn't have them before, such as the General's Imperative
* Added automation for cards which require you to target cards from your hand, such as Kuat Reinforcements or Jabba the Hut. To use those, just target the appropriate number of cards from your hand and "Use Ability" ''Ctrl''+''Q''
* Changed shortcut for Activating a card's ability to [Ctrl]+[Q]
* Added shortcut for Ignoring a card's trigger to [Ctrl]+[Z]

    


### 2.2.4.x

* **Edge of Darkness** has been added without most automations. Fate Cards and 1-2 known automations were copied in. The rest will be coming in v2.2.5.x
* Embers of Hope scripting was added already in order to prevent card draws happening automatically when it shouldn't.

### 2.2.3.x

* Fixed Rogue Squadron Mobilization triggering
* Added confirm dialogue about trying to play a unit or enhancement outside the deployment phase
* Added confirm dialogue about trying to strike with a unit, before finishing edge battle. Should prevent mistakes due to misclicks.

### 2.2.2.x

* Fixed Hoth Operations not adding edge bonuses per participating speeders.
* Moorsh Moraine should now only provide the bonus to the owner.

### 2.2.1.x

* **Significant:** Scripted almost all Assault on Echo Base cards
  * **Cards not scripted:**
    * Col Serra (Only the Edge(1) and Damage Protection is scripted)
    * Confronting the Terror
    * Corrupt Official
    * Echo Control Center
    * Knowledge and Defense
  * **Cards with tricky scripting:**
    * A Stinging Insult - Will engage only unfocused units
* Fixed the placement of Edge Cards and Dummy cards to not force zoom out.
* Double clicking an objective at the start of the game will now select it to put at the bottom of the deck.

### 2.2.0.x

* **Assault on Echo Base** has been added without automations. Those will be coming in v2.2.1.x

### 2.1.4.x

* Added warning when trying to deploy a unit or enhancement out of phase.
* Fixed Reconnaisence mission hopefully
* Fixed Self-Preservation adding force per opposing units
* Fixed A Dark Time for The Rebellion triggering on opponent's turn
* Fixed Error with Jedi Mind Trick and It Binds all Things

### 2.1.3.x

* Paid Abilities don't require an affiliation match anymore

### 2.1.2.x

* Changed triggers to support generic "card leaving play" events
* Fixed Cruel Interrogations and Take them Prisoner.

### 2.1.1.x

* **Significant:** Scripted almost all A Dark Time cards.
* Added helpful documents at documentation menu.
  * [Unofficial Action Window Card](http://boardgamegeek.com/filepage/89570/star-wars-the-card-game-unofficial-action-window) a
  * [Rules Summary 1.3](http://boardgamegeek.com/filepage/86297/star-wars-lcg-rules-summary)
* Force and Unopposed Bonuses are now announced
* Added new Damage marker

### 2.1.0.x

* **A Dark Time** has been added but without any automations yet. Due to the complexity of the new stuff, I opted to put it out first and then I will add the automations with more leisure later

### 2.0.0.x

* Game Definition converted to OCTGN 3.1 format.

### 1.2.0

* **The Search for Skywalker** cards have been added and scripted. Get the latest set file for the goodies.
* Fixed Red Two not automatically using its ability.

### 1.1.3

* Refresh Phase should not clear opponent's shield tokens anymore.

### 1.1.2

* Fixed Rebel Sympathizer reducing costs for both sides without being used at all
* Fixed Red Two Automation

### 1.1.1

* Light Side now really shouldn't refresh on their first turn.
* Card placement on second row should now be fine.

### 1.1.0

* **Desolation of Hoth** cards have been added and scripted. Grab the latest pack for the goodies.
* General scripting improvements which should make future sets easier to script
* Now cards which reduce/incease card costs will be checked when a card is first attempted to be played. 


### 1.0.17

* Zoomed in on the table so that the cards are better seen without having to mouse over them. Re-arranged the placement to make this possible.
* Recon Mission will now reduce the dark-side's reserves when it leaves play, and not the light side's
* You can now cancel a card ability that you've triggered. You can find the appropriate function on the "Manual Actions" menui
* You can now force a card ability (for example if you reduced the cost) . Just double click the card and it will ask you if you want to bypass the payment
* Disturbance in the Force now only target opponent's units
* Added a new message at the end of the game to inform people where to report bugs

### 1.0.16

* Fixed Darth Vader's ability triggering but doing nothing
* Fixed Superlaser Blast not increasing the Death Star Dial
* Fixed Endor Gambit removing focus from opposing units when only those are there.
* Turns sequence will now use the OCTGN internal method to change player, which should look nicer
* Made the hand size icon fit better in the new theme.

### 1.0.15

* Robustness fixes
* Fixed Take Them Prisoner Bug

### 1.0.14

* Game will now check player decks during setup for legality
* A Change in the way events work. Now as soon as you finish paying the cost for an event, the card will change its highlight to green to signify the event is ready to take effect. It is at this point that your opponent is allowed to play interrupts.
  * Interrupts which cancel the effects of events, like C-3PO new require a "ready" event as a target. A "ready event" is an event with a green highlight which has been paid for (or has 0 cost). When that happens, the event will not have any effects when activated by your opponent.
  * Once all players had a chance to play interrupts to events, the controller of each ready event can now double-click on it to have it take effect
  

### 1.0.13

* Common Ground works automatically now
* Recon Mission now reduces its owner's reserves when discarded, and not the rebels'

### 1.0.12

* Reorganized menus
* Added ability to rescue targets
* Leia's ability should not trigger twice
* Fixed Placement of captured and attached cards by opponent's scripts
* Stolen Plans should now work automatically

### 1.0.11

Important bugfixes for the automations

* Now scripts on cards triggered by another player's effects should work
* Leia's Ability should now be working
* Rebel Sympathizer's ability is automated
* Trooper Assault should work now.
* Conceding the game shouldn't give an error anymore
* Various robustness changes.

### 1.0.10

Card automations are now here! 
A very large percentage of the available cards will now trigger their effects as soon as they hit the table 
or as soon their triggers are reached (after specific phases, after striking etc). 
Cards which have their own abilities are also automated, and you can make them work by simply double-clicking on them and having the target of their effect targeted (if one is needed)

So except that, the following have also been done:

* Added capturing mechanic. Many automations will use it automatically, but you can also call it manually.
  * To capture a card from the table, opponents hand or opponent's deck simply target their card and press Ctrl+C on the table. Yes you can target a card in a player's hand or deck normally (shift+click)
* Added a rescuing mechanic. When an objective with captured cards is destroyed, captured cards in it will be returned to their owner's hands. 
  * If you want to manually rescue cards, the controller of the card needs to simply use the "Manual Actions > Rescue card" option
  * IMPORTANT: Due to the attachment mechanics of capturing cards, **You should not move them away from their objective manually**. Use the rescue mechanic
  * If for some reason the rescue mechanic does not work or cannot be used, and you want to clear the cards that are supposedly captured in an objective, use the "Clear of captured variables" option under "Manual Actions".  
* During setup, starting objectives are now placed face down. This allows players to perform their mulligans before using the abilities of those objectives  
  * Once both players have setup their three starting objectives, they just need to double-click on them to reveal them.
* Smugglers & Scouts resources should now be counted correctly.
* Unopposed Bonus is now only applied if the attacker has units left in battle
* Mulligan will now only ever provide 6 cards


### 1.0.4 

* Fixed bug where finishing an unopposed engagement would assign 2 damage
* Thwarting an objective will now ask for confirmation to avoid mistakes
* Renamed the card discard function to point out that it also thwarts objectives.
* Balance of the Force will now spawn on the light side to avoid confusion

### 1.0.3

New version improves engagement by separating it into steps (i.e. phases) as well. 
This means that you can easily communicate who's turn it is to declare participants or when you're ready to start playing edge cards and so on.

The steps work as always, once you're in an engagement, simple press Ctrl+Enter to move to the next step.
The game is also smart enough to auto-announce a phase when you take an action that belongs to it
(For example if you play an edge card, the game will announce the "Edge Battle" step). 

This also includes some extra automation to make things faster and more robust. Reaching the "Reward Unopposed" step will automatically end the engagement, and reaching the strikes step will make sure the edge battle is resolved.

* Fixed various bugs during Edge calculations, such as cards not being revealed
* Now unopposed attacker wins the edge struggle automatically
* Fate cards now have a different highlight when revealed. Once they've been used, they switch to the normal silver highlight for the calculation
* You can now clear participants form the battle or remove units from the force. Normally the game does not allow you, but this is in case you've done a mistake
* Added an option to grab the Edge manually, if for some reason the edge calculation was incorrect

### 1.0.1

* Finishing the engagement now clears the opponent's edge cards as well
* Tactic:1 strikes now focus the target unit
* Spread out the objectives a bit
* Free units/enhancements now are autoplaced.
* Can now manually shuffle the objective deck

### 1.0.0

First working version for the public. It has basic gameplay functionality but not card scripting (i.e. individual card effects are not automated)

However the basic things you need to do quickly and effortlessly should be possible. 

http://i.imgur.com/GutHl.jpg
