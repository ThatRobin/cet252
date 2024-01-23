class Item(dict):
    def __init__(self, name):
        dict.__init__(self, name=name)
        self.name = name

class Class:
    def __init__(self, modid, id, name, stat, stat2):
        self.id = id
        self.modid = modid
        self.name = name
        self.stat = stat
        self.stat2 = stat2

class Race:
    def __init__(self, modid, id, name, stat, stat2):
        self.id = id
        self.modid = modid
        self.name = name
        self.stat = stat
        self.stat2 = stat2

class Monster:
    def __init__(self, id, name, initiative, attack, defence):
        self.id = id
        self.name = name
        self.initiative = initiative
        self.attack = attack
        self.defence = defence