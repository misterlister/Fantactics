# Fantactics

A two-player turn-based game, based on a fusion of chess and turn-based strategy video games.

## Set up

To run this program, execute the following commands in the directory containing the game:

### Create the virtual environment and install dependencies (first time only)

Run the setup script the first time the game is being used on a machine.
This command will create a virtual environment under the name '.venv', and will install all dependencies

```bash
./setup.sh
```

### Activate Virtual Environment

Next, the virtual environment needs to be activated with the following command

```bash
source .venv/bin/activate
```

### Start the server (optional)

Next, if playing across different machines on a network, one player must start a server with the following command

```bash
python3 server.py
```

### Start the game client

- If no server is running, this command will start the game as single-client hotseat mode
- If a server is running, this command will connect to the server

```bash
python3 main.py
```

### Begin

From here, simply select 'Play' on the main menu to begin the game

- If playing with a server, the client will wait for the second player to join to begin
- If not playing with a server, the game will begin immediately

## Game Rules

- When the game begins, two players begin with a set of units on opposing sides of the game board.
- Each turn, a player may select one of their units, and do the following
  - **Move** the unit, and/or
    - **Attack** an adjacent enemy unit
    - Use the unit's **Special Ability** (Effects differ depending on the type of unit in question)
    - Take no action
- Play continues until either:
  - A player's *General* is slain
  - Every one of a player's units, other than their *General* is slain
- Once one of these occurs, that player loses the game!

## Unit Types

Units are divided into the following Unit Types, each with their own strengths and weaknesses.

Each unit has:

- An **HP** stat which represents the amount of damage this unit can take before dying
- An **Attack** stat which represents how much damage this unit deals when attacking
- A **Damage Type**, representing the type of damage this unit's weapon deals
- An **Armour Type**, which effects how much damage this unit takes from different damage types
- A **Movement Range**, which defines how many spaces this unit can move in a turn
- A **Movement Type**, which effects how the unit can move over different types of terrain
- A **Passive Ability** which grants that unit some special bonus
- An **Active Ability** which that unit can use to benefit its player

### Peasant

The weakest of a player's units, *Peasants* have below average capabilities in all areas.

- **Damage Type:** Bludgeoning
- **Armour Type:** Padded
- **Passive Ability:** *Promotion* - If a *Peasant* reaches the far side of the board, they can promote to any other type of unit (Other than *General* or *Archmage*)
- **Active Ability:** *Surge of Bravery* - Once per game, each *Peasant* can increase their stats for the duration of a single turn. 

### Soldier

Sturdy and resolute, *Soldiers* protect allies from ranged attacks and can take blows for them.

- **Damage Type:** Piercing
- **Armour Type:** Chain
- **Passive Ability:** *Protective Cover* - Any unit adjacent to an allied *Soldier* may not be targetted by ranged abilities.
- **Active Ability:** *Guarded Advance* - A *Soldier* may swap places with an adjacent ally.

### Archer

Careful and tactical, *Archers* maximize the benefits of their terrain and send volleys of arrows at the enemy.

- **Damage Type:** Piercing
- **Armour Type:** Padded
- **Passive Ability:** *Entrench* - An *Archer* gains a bonus to both attack and defense equal to the defensive value of their terrain (effectively doubling the standard bonus to their defense).
- **Active Ability:** *Arrow Volley* - An *Archer* may strike enemies from considerable range.

### Cavalry

Swift and mighty, *Cavalry* can quickly dispatch lightly armoured targets, and harry foes to prevent them from using special abilities.

- **Damage Type:** Slashing
- **Armour Type:** Plate
- **Passive Ability:** *Swift Charge* - *Cavalry* can move through spaces of allied units, and through all enemies except *Soldiers*
- **Active Ability:** *Harrying Strike* - *Cavalry* can strike a foe with a slightly weaker attack that disables the enemy from using abilities for 2 turns.

### Sorcerer

Mysterious and powerful, *Sorcerers* can strike several foes at once with their magic, healing themself by siphoning their essence.

- **Damage Type:** Piercing
- **Ability Damage Type:** Magic
- **Armour Type:** Robes
- **Passive Ability:** *Siphon Essence* - For each foe damaged, a *Sorcerer* will heal themself by 1 hp.
- **Active Ability:** *Sorcerous Assault* - *Sorcerers* can strike up to three foes in a horizontal line with a ranged spell attack.

### Healer

Radiant and protective, *Healers* aid nearby allies by boosting their defense and healing them.

- **Damage Type:** Bludgeoning
- **Armour Type:** Chain
- **Passive Ability:** *Protective Aura* - Every ally within 2 spaces increases their defense by 1.
- **Active Ability:** *Healing Radiance* - *Healers* can restore up to 5 hp to all adjacent allies.

### Archmage

Fearsome and majestic, *Archmages* fly above the battlefield, raining down destruction on their foes.

- **Damage Type:** Bludgeoning
- **Ability Damage Type:** Magic
- **Armour Type:** Robes
- **Passive Ability:** *Destructive Aura* - Every foe within 2 spaces decreases their defense by 1.
- **Active Ability:** *Arcane Vortex* - An *Archmage* can strike up to five foes in a cross pattern with a ranged spell attack.

### General

Regal and Inspiring, *Generals* are the leaders of their forces, boasting incredible fighting power. If they fall, however, their forces will lose the battle.

- **Damage Type:** Slashing
- **Armour Type:** Plate
- **Passive Ability:** *Leadership Aura* - Every ally within 2 spaces increases their attack power by 1.
- **Active Ability:** *Inspirational Rally* - Once per battle, a *General* may inspire their forces, allowing two units to act on a single turn.

## Damage and Armour Effectiveness

Each damage type has different levels of effectiveness, depending on the targets armour type.

- **Slashing Damage**
  - *Effective* against **Robes** and **Padded** armour.
  - *Ineffective* against **Chain** and **Plate** armour

- **Piercing Damage**
  - *Effective* against **Robes** armour.
  - *Ineffective* against **Plate** armour
  - *Neutral* against **Padded** and **Chain** armour

- **Bludgeoning Damage**
  - *Neutral* against all armour types.

- **Magic Damage**
  - *Effective* against **Plate** armour.
  - *Ineffective* against **Robes** armour
  - *Neutral* against **Padded** and **Chain** armour

## Terrain Effects

Each *Terrain Type* has different effects on units that occupy its space.

- **Plains**
  - The basic *Terrain Type*. Provides no special effects.
- **Paths**
  - A *Terrain Type* that provides additional movement speed for units traveling on it.
- **Forests**
  - A *Terrain Type* That provides 1 defense to any unit within it. In addition, *Forests* limit the movement of units traveling on it, especially those who are mounted on horses.
- **Fortresses**
  - A defensive *Terrain Type* which provides 2 defense to any unit within it.