Android:Netrunner LCG plugin for OCTGN
=========================
The Star Wars universe as a Head2Head Living card game

More instructions will be forthcoming soon. Stay tuned...

Enjoy!

Tutorials
---------

[Step-by-Step Tutorial Video (v.1.0.2)](http://www.youtube.com/watch?v=Ll5TFxR1TK4)

Screenshots
---------
(Click for larger size)

The Dark side destroys the last objective to win the game

[![](http://i.imgur.com/Ooq0Vl.png)](http://i.imgur.com/Ooq0V.png)

Demo game at v1.0.0

[![](http://i.imgur.com/GutHll.jpg)](http://i.imgur.com/GutHl.jpg)

Changelog
---------

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