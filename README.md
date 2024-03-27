# Fantactics

A two-player turn-based game, based on a fusion of chess and turn-based strategy video games.

## Set up

To run this program, execute the following commands in the directory containing the game:

### Create a virtual environment

```bash
python3 -m venv .venv
```

### Activate the virtual environment

```bash
source .venv/bin/activate
```

### Install requirements

```bash
pip install -r requirements.txt
```

### Start the game

```bash
python3 main.py
```

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
- **Active Ability:** *Surge of Bravery - Once per game, each *Peasant* can increase their stats for the duration of a single turn. 

### Soldier

### Archer

### Cavalry

### Sorcerer

### Healer

### Archmage

### General