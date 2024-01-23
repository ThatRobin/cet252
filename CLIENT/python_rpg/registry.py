import json
import os

from registryClasses import Item, Race, Class, Monster


class Registry:
    def __init__(self, path):
        self.path = path
        self.entries = {}

    def getEntries(self):
        return self.entries

    def getBaseData(self):
        entries = {}
        path = "base"
        path += "/" + self.path
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".json"):
                with open(path + "/" + filename, "r") as read_file:
                    entries[filename.replace(".json", "")] = json.load(read_file)
                continue
        self.entries["base"] = entries

    def getModData(self, modid):
        entries = {}
        path = "mods"
        directories = os.listdir(path)
        for directory2 in os.listdir(path + "/" + modid):
            if directory2 == self.path:
                files = os.listdir(path + "/" + modid + "/" + directory2)
                for file in files:
                    filename = os.fsdecode(file)
                    if filename.endswith(".json"):
                        with open(path + "/" + modid + "/" + self.path + "/" + filename, "r") as read_file:
                            entries[filename.replace(".json", "")] = json.load(read_file)
                        continue
            self.entries[modid] = entries
        self.mods = directories


class ItemRegistry():
    def __init__(self):
        self.path = "items"
        self.entries = []

    def getItems(self):
        return self.entries

    def getBaseData(self):
        path = "base/" + self.path
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".json"):
                with open(path + "/" + filename, "r") as read_file:
                    data = json.load(read_file)
                    self.entries.append(Item(data.get("name")))

    def getModData(self, modid):
        path = "mods"
        for directory2 in os.listdir(path + "/" + modid):
            if directory2 == self.path:
                files = os.listdir(path + "/" + modid + "/" + directory2)
                for file in files:
                    filename = os.fsdecode(file)
                    if filename.endswith(".json"):
                        with open(path + "/" + modid + "/" + self.path + "/" + filename, "r") as read_file:
                            data = json.load(read_file)
                            self.entries.append(Item(data.get("name")))


class RaceRegistry():
    def __init__(self):
        self.path = "races"
        self.entries = []

    def getRaces(self):
        return self.entries

    def getBaseData(self):
        path = "base/" + self.path
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".json"):
                with open(path + "/" + filename, "r") as read_file:
                    data = json.load(read_file)
                    name = filename.replace(".json", "")
                    stats = []
                    for i in data.get("stats"):
                        stats.append(data.get("stats").get(i))
                    self.entries.append(Race("base", name, data.get("name"), stats[0], stats[1]))

    def getModData(self, modid):
        path = "mods"
        directories = os.listdir(path)
        for directory2 in os.listdir(path + "/" + modid):
            if directory2 == self.path:
                files = os.listdir(path + "/" + modid + "/" + directory2)
                for file in files:
                    filename = os.fsdecode(file)
                    if filename.endswith(".json"):
                        with open(path + "/" + modid + "/" + self.path + "/" + filename, "r") as read_file:
                            data = json.load(read_file)
                            name = filename.replace(".json", "")
                            stats = []
                            for i in data.get("stats"):
                                stats.append(data.get("stats").get(i))
                            data["path"] = "/" + modid + "/" + self.path + "/" + filename.replace(".json", "")
                            self.entries.append(Race(modid, name, data.get("name"), stats[0], stats[1]))


class ClassRegistry():
    def __init__(self):
        self.path = "classes"
        self.entries = []

    def getClasses(self):
        return self.entries

    def getBaseData(self):
        path = "base/" + self.path
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".json"):
                with open(path + "/" + filename, "r") as read_file:
                    data = json.load(read_file)
                    name = filename.replace(".json", "")
                    stats = []
                    for i in data.get("stats"):
                        stats.append(data.get("stats").get(i))
                    self.entries.append(Class("base", name, data.get("name"), stats[0], stats[1]))

    def getModData(self, modid):
        entries = {}
        path = "mods"
        directories = os.listdir(path)
        for directory2 in os.listdir(path + "/" + modid):
            if directory2 == self.path:
                files = os.listdir(path + "/" + modid + "/" + directory2)
                for file in files:
                    filename = os.fsdecode(file)
                    if filename.endswith(".json"):
                        with open(path + "/" + modid + "/" + self.path + "/" + filename, "r") as read_file:
                            data = json.load(read_file)
                            name = filename.replace(".json", "")
                            stats = []
                            for i in data.get("stats"):
                                stats.append(data.get("stats").get(i))
                            self.entries.append(Class(modid, name, data.get("name"), stats[0], stats[1]))

class MonsterRegistry():
    def __init__(self):
        self.path = "monsters"
        self.entries = []

    def getMonsters(self):
        return self.entries

    def getBaseData(self):
        path = "base/" + self.path
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".json"):
                with open(path + "/" + filename, "r") as read_file:
                    data = json.load(read_file)
                    name = filename.replace(".json", "")
                    stats = []
                    for i in data.get("stats"):
                        stats.append(data.get("stats").get(i))
                    self.entries.append(Monster(name, data.get("name"), stats[0], stats[1], stats[2]))

    def getModData(self, modid):
        entries = {}
        path = "mods"
        directories = os.listdir(path)
        for directory2 in os.listdir(path + "/" + modid):
            if directory2 == self.path:
                files = os.listdir(path + "/" + modid + "/" + directory2)
                for file in files:
                    filename = os.fsdecode(file)
                    if filename.endswith(".json"):
                        with open(path + "/" + modid + "/" + self.path + "/" + filename, "r") as read_file:
                            data = json.load(read_file)
                            name = filename.replace(".json", "")
                            stats = []
                            for i in data.get("stats"):
                                stats.append(data.get("stats").get(i))
                            self.entries.append(Monster(name, data.get("name"), stats[0], stats[1], stats[2]))


raceRegistry = RaceRegistry()
classRegistry = ClassRegistry()
itemRegistry = ItemRegistry()
monsterRegistry = MonsterRegistry()

raceRegistry.getBaseData()
classRegistry.getBaseData()
itemRegistry.getBaseData()
monsterRegistry.getBaseData()
for mod in os.listdir("mods"):
    raceRegistry.getModData(mod)
    classRegistry.getModData(mod)
    itemRegistry.getModData(mod)
    monsterRegistry.getModData(mod)

def getRaceRegistry():
    return raceRegistry


def getClassRegistry():
    return classRegistry
