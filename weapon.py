#Super classe arma com atributos básicos e métodos
class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

#Subclasse espada com ataque especificado
class Sword(Weapon):
    def __init__(self):
        super().__init__("Espada", 10)

#Subclasse varinha mágina com ataque especificado
class Wand(Weapon):
    def __init__(self):
        super().__init__("Cajado Mágico", 8) 