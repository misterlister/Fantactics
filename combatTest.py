from units import *

location = None

lg_divider = "\n" + ("*" * 10) + "\n"
sm_divider = "-" * 3


unitList = {}
peasant = Peasant(location)
soldier = Soldier(location)
sorcerer = Sorcerer(location)
healer = Healer(location)
archer = Archer(location)
cavalry = Cavalry(location)
archmage = Archmage(location)
general = General(location)

unitList2 = {}
peasant2 = Peasant(location)
soldier2 = Soldier(location)
sorcerer2 = Sorcerer(location)
healer2 = Healer(location)
archer2 = Archer(location)
cavalry2 = Cavalry(location)
archmage2 = Archmage(location)
general2 = General(location)

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

def combat(attacker, atk_name, defender, def_name):
    #print(sm_divider)
    attacker.basic_attack(defender)
    if def_name not in damagePerHit[atk_name]:
        damagePerHit[atk_name][def_name] = defender.get_max_hp() - defender.get_curr_hp()
    #print(f"{atk_name} attacks {def_name}")
    #print(f"{atk_name}: Hp{attacker.get_curr_hp()}/{attacker.get_max_hp()}")
    #print(f"{def_name}: Hp{defender.get_curr_hp()}/{defender.get_max_hp()}")
    if defender.is_dead():
        #print(f"{def_name} is dead.")
        #print(f"Round {round}:")
        #print(f"{atk_name}: Hp{attacker.get_curr_hp()}/{attacker.get_max_hp()}")
        #print(f"{def_name}: Hp{defender.get_curr_hp()}/{defender.get_max_hp()}")
        if atk_name not in winList:
            winList[atk_name] = []
            hpRemain[atk_name] = []
        winList[atk_name].append(def_name)
        hpRemain[atk_name].append(f"{attacker.get_curr_hp()}/{attacker.get_max_hp()}")
        return False
    else:    
        #print(sm_divider)
        defender.retaliate(attacker)
        if atk_name not in retaliateDamage[def_name]:
            retaliateDamage[def_name][atk_name] = attacker.get_max_hp() - attacker.get_curr_hp()
        #print(f"{def_name} attacks {atk_name}")
        #print(f"{def_name}: Hp{defender.get_curr_hp()}/{defender.get_max_hp()}")
        #print(f"{atk_name}: Hp{attacker.get_curr_hp()}/{attacker.get_max_hp()}")
        if attacker.is_dead():
            #print(f"{atk_name} is dead.")
            #print(f"Round {round}:")
            #print(f"{atk_name}: Hp{attacker.get_curr_hp()}/{attacker.get_max_hp()}")
            #print(f"{def_name}: Hp{defender.get_curr_hp()}/{defender.get_max_hp()}")
            if atk_name not in loseList:
                loseList[atk_name] = []
                targetHp[atk_name] = []
            loseList[atk_name].append(def_name)
            targetHp[atk_name].append(f"{defender.get_curr_hp()}/{defender.get_max_hp()}")
            return False
        else:
            return True

def matchup(attacker, atk_name, defender, def_name, round):
    #print(f"Round {round}:")
    if (combat(attacker, atk_name, defender, def_name)):
        matchup(attacker, atk_name, defender, def_name, round+1)
    else:
        return


for attacker in unitList:
    for defender in unitList2:
        #print(lg_divider)
        #print(f"{unitList[attacker]} vs {unitList2[defender]}")
        matchup(attacker, unitList[attacker], defender, unitList2[defender], 1)
        attacker.heal(100)
        defender.heal(100)

print(lg_divider)
print("Wins on attack, with remaining hp: \n")
for unit in winList:
    print(unit + ": ", end="") 
    for i in range(len(winList[unit])):
        print(winList[unit][i] + ": ", end="")
        print(hpRemain[unit][i] + ", ", end="")
    print("\n" + sm_divider)


print(lg_divider)
print("Losses on attack, with damage dealt: \n")
for unit in loseList:
    print(unit + ": ", end="")
    for i in range(len(loseList[unit])):
        print(loseList[unit][i] + ": ", end="")
        print(targetHp[unit][i] + ", ", end="")
    print("\n" + sm_divider)

print(lg_divider)
print("Damage per hit when attacking: \n")
for unit in damagePerHit:
    print(unit + ": ", end="")
    for target in damagePerHit[unit]:
        print(target + ": ", end = "")
        print(str(damagePerHit[unit][target]) + ", ", end = "")
    print("\n" + sm_divider)

print(lg_divider)
print("Damage per hit when retaliating: \n")
for unit in retaliateDamage:
    print(unit + ": ", end="")
    for target in retaliateDamage[unit]:
        print(target + ": ", end = "")
        print(str(retaliateDamage[unit][target]) + ", ", end = "")
    print("\n" + sm_divider)