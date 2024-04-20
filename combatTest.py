from units import (
    Peasant,
    Soldier,
    Sorcerer,
    Healer,
    Archer,
    Cavalry,
    Archmage,
    General,
    Unit
)

LG_DIVIDER = "\n" + ("*" * 10) + "\n"
SM_DIVIDER = "-" * 3


unitList = {}

peasant = Peasant()
soldier = Soldier()
sorcerer = Sorcerer()
healer = Healer()
archer = Archer()
cavalry = Cavalry()
archmage = Archmage()
general = General()

unitList2 = {}

peasant2 = Peasant()
soldier2 = Soldier()
sorcerer2 = Sorcerer()
healer2 = Healer()
archer2 = Archer()
cavalry2 = Cavalry()
archmage2 = Archmage()
general2 = General()

unitList[peasant] = "Peasant"
unitList[soldier] = "Soldier"
unitList[sorcerer] = "Sorcerer"
unitList[healer] = "Healer"
unitList[archer] = "Archer"
unitList[cavalry] = "Cavalry"
unitList[archmage] = "Archmage"
unitList[general] = "General"

unitList2[peasant2] = "Peasant"
unitList2[soldier2] = "Soldier"
unitList2[sorcerer2] = "Sorcerer"
unitList2[healer2] = "Healer"
unitList2[archer2] = "Archer"
unitList2[cavalry2] = "Cavalry"
unitList2[archmage2] = "Archmage"
unitList2[general2] = "General"


winList = {}
hpRemain = {}
loseList = {}
targetHp = {}
damagePerHit = {}
retaliateDamage = {}

for unit in unitList:
    damagePerHit[unitList[unit]] = {}
    retaliateDamage[unitList[unit]] = {}

def combat(attacker: Unit, atk_name: str, defender: Unit, def_name: str):
    defender_hp = defender.get_curr_hp()
    attacker.basic_attack(defender)
    if def_name not in damagePerHit[atk_name]:
        damagePerHit[atk_name][def_name] = defender_hp - defender.get_curr_hp()

    print(SM_DIVIDER)
    print(f"{atk_name} attacks {def_name}")
    print(f"{atk_name}: Hp{attacker.get_curr_hp()}/{attacker.get_max_hp()}")
    print(f"{def_name}: Hp{defender.get_curr_hp()}/{defender.get_max_hp()}")

    if defender.is_dead():
        #print(f"{def_name} is dead.")
        if atk_name not in winList:
            winList[atk_name] = []
            hpRemain[atk_name] = []
        winList[atk_name].append(def_name)
        hpRemain[atk_name].append(f"{attacker.get_curr_hp()}/{attacker.get_max_hp()}")
        return False
    else:
        attacker_hp = attacker.get_curr_hp()
        defender.retaliate(attacker)
        if atk_name not in retaliateDamage[def_name]:
            retaliateDamage[def_name][atk_name] = attacker_hp - attacker.get_curr_hp()

        print(SM_DIVIDER)
        print(f"{def_name} retaliates against {atk_name}")
        print(f"{def_name}: Hp{defender.get_curr_hp()}/{defender.get_max_hp()}")
        print(f"{atk_name}: Hp{attacker.get_curr_hp()}/{attacker.get_max_hp()}")

        if attacker.is_dead():
            #print(f"{atk_name} is dead.")
            if atk_name not in loseList:
                loseList[atk_name] = []
                targetHp[atk_name] = []
            loseList[atk_name].append(def_name)
            targetHp[atk_name].append(f"{defender.get_curr_hp()}/{defender.get_max_hp()}")
            return False
        else:
            return True

def matchup(attacker: Unit, atk_name: str, defender: Unit, def_name: str, round: int):
    print(f"{SM_DIVIDER}\nRound {round}:")
    if (combat(attacker, atk_name, defender, def_name)):
        matchup(defender, def_name, attacker, atk_name, round+1)

###################################################

for attacker in unitList:
    for defender in unitList2:
        print(LG_DIVIDER)
        print(f"{unitList[attacker]} vs {unitList2[defender]}")
        matchup(attacker, unitList[attacker], defender, unitList2[defender], 1)
        attacker.heal(100)
        defender.heal(100)
        attacker.revive()
        defender.revive()

###################################################

print(LG_DIVIDER)
print("Wins on attack, with remaining hp: \n")
for unit in winList:
    print(unit + ": ", end="") 
    for i in range(len(winList[unit])):
        print(winList[unit][i] + ": ", end="")
        print(hpRemain[unit][i] + ", ", end="")
    print("\n" + SM_DIVIDER)


print(LG_DIVIDER)
print("Losses on attack, with damage dealt: \n")
for unit in loseList:
    print(unit + ": ", end="")
    for i in range(len(loseList[unit])):
        print(loseList[unit][i] + ": ", end="")
        print(targetHp[unit][i] + ", ", end="")
    print("\n" + SM_DIVIDER)

print(LG_DIVIDER)
print("Damage per hit when attacking: \n")
for unit in damagePerHit:
    print(unit + ": ", end="")
    for target in damagePerHit[unit]:
        print(target + ": ", end = "")
        print(str(damagePerHit[unit][target]) + ", ", end = "")
    print("\n" + SM_DIVIDER)

print(LG_DIVIDER)
print("Damage per hit when retaliating: \n")
for unit in retaliateDamage:
    print(unit + ": ", end="")
    for target in retaliateDamage[unit]:
        print(target + ": ", end = "")
        print(str(retaliateDamage[unit][target]) + ", ", end = "")
    print("\n" + SM_DIVIDER)

###################################################