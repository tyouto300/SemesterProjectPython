This program aims to simulate the combat elements of the tabletop game Warhammer 40,000 10th Edition.

In the game, units are equipped with weapons that have a set of characteristics representing that weapon, and the units themselves also have characteristics representing their armor, health, etc.

Offensively, weapons have 5 characteristics:
1)Attacks- This determines how many dice are rolled when attacking with that weapon. A weapon wiwth an Attacks characteristic of 3 will roll 3 dice for each model in that unit equipped with that weapon
2)Skill- Either denoted BS or WS depending on the stage of the game, this determines the result an individual dice on an attack roll must equal or exceed to be considered a hit. Units with a BS of 3+ must roll a 3 or higher for 
  a given attack dice to be a hit. This part of the attack is called the Hit Roll.
3)Strength- The attacker rolls as many dice as were successful hits in the previous Hit Roll, and the minimum result that is needed to successfully Wound is determined by both the Strength of the weapon and the Toughness of the targeted unit.
  Units that have a Toughness > 2 * Strength require a result of 6+ to Wound
  Units that have a Toughness > Strength require a result of 5+ to Wound
  Units that have a Toughness = Strength require a result of 4+ to Wound
  Units that have a Toughness < Strength require a result of 3+ to Wound
  Units that have a Toughness < 1/2 * Strength require a result of 2+ to Wound
  This part is called the Wound Roll
4)Armor Piercing- The targeted player then takes as many dice as were successful Wounds previously, and rolls them. The minimum result required is that of the Saving characteristic on that unit's datasheet. Armor Piercing,
  denoted as a -x, subtracts x from each dice rolled by the defender, effectively increasing the minimum. A weapon with an Armor Piercing of 2 against a Saving throw of 3+ then requires the defender roll 5+ to successfuly Save.
  This is called the Saving Throw
5)Damage- The defender then takes however many dice did not meet the Save requirement above and multiplies that amount by the Damage characteristic of the weapon, and applies it to their unit. In the case of D3 or D6 damage(Not implemented),
  The attacker rolls a dice for each failed Save which the defender then applies the roll of that damage. D3 calculation is done by dividing the normal 6 sided die into 3 sections, 1-2 = 1, 3-4 = 2, 5-6 = 3.

Defensively units have 5 characteristics:
1)Toughness- Function explained above
2)Sv - Function explained above
3)Invulnerable Save- (Not implemented) Can be chosen to be rolled instead of the normal Save, which is called an Armor Save. Invulnerable Saves are usually worse(higher) than Armor Saves, but they are not affected by Armor Piercing.
  Not all units get an Invulnerable Save. For a unit that does not have an Invulnerable Save, enter 0.
4)Wounds- The amount of Wounds(health) per model in the unit.
5)Feel No Pain- (Not implemented) Whenever a unit with a Feel No Pain x+(FNP) fails a save and takes damage, they roll an amount of dice equal to the damage they are about to receive. For each dice that meets/exceeds the listed number on the FNP,
  a single point of Damage is ignored.

Applying Damage:
  When a unit takes damage, it must go to the model in the unit that is not at full Wounds. If none exist, then the defender must choose a model to apply the damage to. In the case where a model is "overkilled", where the damage of each hit of 
  the weapon is greater than that models Wounds, then the extra Damage is lost and not applied. So, 10 failed saves at 1 damage will apply 10 Damage to a unit, and all 10 Damage will be applied to however many models it can kill, as each hit 
  does 1 Damage so no overkilling will happen. A single hit of 2 Damage against a model with 1 Wound will kill that model, but the leftover 1 Damage will not apply to the other models in the unit.

Critical Rolls: A Critical result is a result of 6. This result always succeeds at whatever it is rolling for and ignores negative modifiers. The one exception is with Armor Saves, which can be modified to be > 6 with sufficient Armor Piercing.
  In this case, the defender has no chance of saving that unless they also have an Invulnerable Save.
  
Weapon Buffs and Debuffs:
  In the attack part of the program, you will see two .lists of buffs and debuffs. Buffs are +1 and everything else in that column. Buffs that add +1 are self explanatory, with one note that +1 to BS/WS and +1 to Hit functionally do the same thing,
  but technically are different, and so if both are toggled the Hit Roll will be operating at a +2 to hit. This modifier is applied to the result of the dice roll, not to the required result. You will also see various words that also modify the weapon.
    BUFFS:
    Lethal Hits, when toggled, makes any Critical Hits( Critical results in the Hit Roll) automatically wound the target. Thus the amount of dice you roll to determine the Wound Roll is lower, but is operating at a minimum amount of successes from the
    previous Hit Roll, if you scored any Lethal Hits.
    Sustained Hits 1, when toggled, makes any Critical Hit add 1 extra automatically successful hit to your total, in addition to that hit succeeding. So a weapon that rolls a 6 to Hit with Sustained Hits 1 gets two hits from that one roll.
    Devastating Wounds, when toggled, makes any Critical Wound(Critical Result in the Wound Roll) automatically Wound the target, and also makes them unable to Save that result, regardless of what Save type they use.
    A weapon that rolls 3 Successful Wounds with 1 being a Devastating Wound will roll 2 dice win the Saving Throw, and then when applying damage will add an extra failed save on to however many failed from those 2.
    Rapid Fire 1, when toggled, adds 1 extra Attack to every model using that weapon in the unit. Normally, it would only trigger when within half the specified Range, but that's not simulated here so if you toggle it, then I assume you are in half range.
    Blast, when toggled, adds 1 extra Attack to every model with that weapon, for every 5 models in the targeted unit. So 4 models with a Blast weapon shooting a unit of 10 models will also roll an additional 8 die on the Hit Roll.(4 * (10 / 5))
      If a unit has an amount of models that isn't a multiple of 5, then it still triggers for every 5 that can be fit in.
    Crit Hits and Crit Wounds 5+ lower the requirement for a Critical Result to 5+ in their respective stages.
    The other +1s are self explanatory
    DEBUFFS:
    -1s are self explanatory.
    Cover is a mechanic that triggers when a unit is obscured by terrain. Terrain isn't simulated, so again if you tick it I assume you mean it. Cover adds 1 to the Armor Save of the defending unit based on one of two conditions:
      If the defender has an Armor Save worse(higher min) than 3+, then Cover always applies, adding +1 to the Armor Save result even if the attacking weapon has 0 Armor Piercing
      If the defender has an Armor Save <= 3+, then Cover only Applies to the Armor Save if the atacking weapons Armor Piercing would modify that Armor Save minimum to be > 3.

The Final Attack screen displays the results of your rolls, and also the "average/expected" results of your rolls. The expected result accurately considers Lethal Hits,+1s,etc... 
