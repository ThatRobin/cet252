import json
import os

import registryClasses
from registry import classRegistry, raceRegistry
from screen import Screen


class PlayerData:
    def __init__(self, name, level, exp, attack, defence, initiative, cRace, cClass, inventory: list):
        self.name = name
        self.level = level
        self.attack = attack
        self.defence = defence
        self.initiative = initiative
        self.exp = exp
        self.cRace = cRace
        self.cClass = cClass
        self.inventory = inventory

    def saveInventory(self):
        data = {}
        if os.path.getsize("save_file.json") > 0:
            with open("save_file.json", "r") as read_file:
                data = json.load(read_file)

        data[self.name]["inventory"] = self.inventory
        with open("save_file.json", "w") as write_file:
            json.dump(data, write_file, sort_keys=True, indent=4)
        return

    def serialize(self):
        test = {
            "name": self.name,
            "level": self.level,
            "exp": self.exp,
            "attack": self.attack,
            "defence": self.defence,
            "initiative": self.initiative,
            "race": self.cRace,
            "class": self.cClass,
            "inventory": self.inventory
        }
        data = {}
        if os.path.getsize("save_file.json") > 0:
            with open("save_file.json", "r") as read_file:
                data = json.load(read_file)

        if data.get(self.name) is not None:
            replace = input("A character with this name already exists. would you like to replace it? (y/n): ").lower()
            if replace == "y":
                data[self.name] = test
            else:
                print("character creation aborted. returning to menu.")
                return

        data[self.name] = test
        with open("save_file.json", "w") as write_file:
            json.dump(data, write_file, sort_keys=True, indent=4)
        return

    @staticmethod
    def deserialize(name):
        with open("save_file.json", "r") as read_file:
            data = json.load(read_file)
        for key in data.keys():
            if name == key:
                stats = data.get(name)
                return PlayerData(name, stats.get("level"), stats.get("exp"), stats.get("attack"), stats.get("defence"), stats.get("initiative"), stats.get("race"), stats.get("class"), stats.get("inventory"))
        return None

    @staticmethod
    def createCharacter():
        name = input("What do you want this character to be called? ")

        cRace = PlayerData.chooseRace()
        cClass = PlayerData.chooseClass()
        assert isinstance(cRace, registryClasses.Race)
        assert isinstance(cClass, registryClasses.Class)
        level = 0
        exp = 0
        attack = cRace.stat + cClass.stat
        defence = cRace.stat2 + cClass.stat2
        initiative = 1
        character = PlayerData(name, level, exp, attack, defence, initiative, cRace.id, cClass.id, [])
        character.serialize()
        for i in range(0, 4):
            print("Character '" + name + "' created Successfully!\nreturning to menu" + ("." * i))
        return character

    @staticmethod
    def getCharacter():
        name = input("What is the Characters name? ")
        character = PlayerData.deserialize(name)
        if character is not None:
            print("Found Character!")
            return character

    @staticmethod
    def displayCharacterList():
        characters = PlayerData.listCharacters()
        for character in characters:
            print("Name: " + character.name)
            print("Level: " + str(character.level))
            print("Exp: " + str(character.exp))
            print("Race: " + character.cRace)
            print("Class: " + character.cClass)
        return characters[0]

    @staticmethod
    def listCharacters():
        characters = []
        with open("save_file.json", "r") as read_file:
            data = json.load(read_file)
        for key in data.keys():
            characters.append(PlayerData.deserialize(key))
        return characters

    @staticmethod
    def chooseClass():
        classChoices = ["Class Options:"]
        classChoiceResults = [None]

        classes = classRegistry.getClasses()
        for closs in classes:
            classChoices.append(str(classes.index(closs)+1) + ") " + closs.name + " ("+closs.modid+")")
            classChoiceResults.append(closs)

        classChoices.append("Which would you like to choose? ")
        classChoiceResults.append(None)
        classScreen = Screen(classChoices, classChoiceResults)
        return classScreen.display()

    @staticmethod
    def chooseRace():
        raceChoices = ["Race Options:"]
        raceChoiceResults = [None]

        races = raceRegistry.getRaces()
        for race in races:
            raceChoices.append(str(races.index(race)+1) + ") " + race.name + " ("+race.modid+")")
            raceChoiceResults.append(race)
        raceChoices.append("Which would you like to choose? ")
        raceChoiceResults.append(None)

        raceScreen = Screen(raceChoices, raceChoiceResults)
        return raceScreen.display()
