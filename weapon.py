class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

class Sword(Weapon):
    def __init__(self, upgrade=False):
        name = "Steel Sword"
        damage = 10
        if upgrade:
            name = "Enhanced Steel Sword"
            damage = 15
        super().__init__(name, damage)

class Wand(Weapon):
    def __init__(self, upgrade=False):
        name = "Magic Wand"
        damage = 8
        if upgrade:
            name = "Enhanced Magic Wand"
            damage = 12
        super().__init__(name, damage) 