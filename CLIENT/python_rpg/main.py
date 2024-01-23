import random
import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir)
os.chdir(script_dir)

import registry
import registryClasses
from player_data import PlayerData
from menus import TitleScreen
from registry import itemRegistry, monsterRegistry
from screen import Screen

random.seed(random.random())
character = None


def init():
    main = TitleScreen()
    main.main()
    global character
    character = main.character


def checkCharacter():
    global character
    while character is None:
        print("Please select a character.")
        init()
    return


checkCharacter()

assert isinstance(character, PlayerData)


# character = PlayerData("Robin", 0, 0, "tiefling", "sorcerer", [])
class Encounter:
    def __init__(self, character):
        assert isinstance(character, PlayerData)
        self.character = character
        self.rollTable = {
            1: self.nothing,
            2: self.market,
            3: self.item,
            4: self.treasure,
            5: self.player_duel,
            6: self.monster_duel
        }

    def nothing(self):
        print("there was nothing to be found")

    def market(self):
        sale = itemRegistry.getItems()
        print("Welcome to the market! here are some of the wares: ")
        for i in range(0, len(sale)):
            print(str(i + 1) + ") " + sale[i])
        self.character.inventory.append(sale)
        self.character.saveInventory()

    def item(self):
        items = itemRegistry.getItems()
        item = random.choice(items)
        print("you have found a " + str(item.name))
        self.character.inventory.append(item)
        self.character.saveInventory()

    def treasure(self):
        print("insert event here")

    def player_duel(self):
        print("get player from save data. battle them.")

    def monster_duel(self):
        print(character.name)

        monster = random.choice(monsterRegistry.getMonsters())
        assert isinstance(monster, registryClasses.Monster)
        print(monster.name)

    def encounter(self):
        # roll = random.randint(1, 6)
        roll = 6
        result = self.rollTable.get(roll)
        result()


encounter = Encounter(character)
encounter.encounter()
