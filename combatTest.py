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


def combat(attacker, atk_name, defender, def_name):
    #print(sm_divider)
    attacker.basic_attack(defender)
    #print(f"{atk_name} attacks {def_name}")
    #print(f"{atk_name}: Hp{attacker.get_curr_hp()}/{attacker.get_max_hp()}")
    #print(f"{def_name}: Hp{defender.get_curr_hp()}/{defender.get_max_hp()}")

def matchup(attacker, atk_name, defender, def_name, round):
    #print(f"Round {round}:")
    combat(attacker, atk_name, defender, def_name)
    if defender.is_dead():
        #print(f"{def_name} is dead.")
        print(f"Round {round}:")
        print(f"{atk_name}: Hp{attacker.get_curr_hp()}/{attacker.get_max_hp()}")
        print(f"{def_name}: Hp{defender.get_curr_hp()}/{defender.get_max_hp()}")
    else:    
        combat(defender, def_name, attacker, atk_name)
        if attacker.is_dead():
            #print(f"{atk_name} is dead.")
            print(f"Round {round}:")
            print(f"{atk_name}: Hp{attacker.get_curr_hp()}/{attacker.get_max_hp()}")
            print(f"{def_name}: Hp{defender.get_curr_hp()}/{defender.get_max_hp()}")
        else:
            matchup(attacker, atk_name, defender, def_name, round+1)


for attacker in unitList:
    for defender in unitList2:
        print(lg_divider)
        print(f"{unitList[attacker]} vs {unitList2[defender]}")
        matchup(attacker, unitList[attacker], defender, unitList2[defender], 1)
        attacker.heal(100)
        defender.heal(100)

                
        



        