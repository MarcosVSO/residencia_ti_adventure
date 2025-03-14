class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

class Sword(Weapon):
    def __init__(self):
        super().__init__("Espada de Aço", 10)

class Wand(Weapon):
    def __init__(self):
        super().__init__("Cajado Mágico", 8) 