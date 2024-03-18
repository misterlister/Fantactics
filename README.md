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
  - Move the unit, and/or
    - Attack an adjacent enemy unit
    - Use the unit's special ability (Effects differ depending on the type of unit in question)
    - Take no action
- Play continues until either:
  - A player's General is slain
  - Every one of a player's units, other than their General is slain
- Once one of these occurs, that player loses the game!

## Unit Types

Units are divided into the following Unit Types, each with their own strengths and weaknesses.

Each unit has:

- An HP stat which represents the amount of damage this unit can take before dying
- An attack stat which represents how much damage this unit deals when attacking
- A damage type, representing the type of damage this unit's weapon deals
- An armour type, which effects how much damage this unit takes from different damage types
- A movement range, which defines how many spaces this unit can move in a turn
- A movement type, which effects how the unit can move over different types of terrain
- A passive ability which grants that unit some special bonus
- An active ability which that unit can use to benefit its player

### Peasant

### Soldier

### Archer

### Cavalry

### Sorcerer

### Healer

### Archmage

### General