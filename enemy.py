import random

class Enemy:
    def __init__(self, name, health, attack_power, loot, image):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.loot = loot
        self.image = image

    def attack(self):
        return self.attack_power

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def drop_loot(self):
        return self.loot

class Goblin(Enemy):
    def __init__(self):
        loot = {
            'gold': random.randint(5, 15),
            'health_potion': random.choice([0, 1])
        }
        super().__init__("Goblin", health=50, attack_power=8, loot=loot, image="assets/goblin_icon.png")

class Orc(Enemy):
    def __init__(self):
        loot = {
            'gold': random.randint(15, 30),
            'health_potion': random.choice([1, 2])
        }
        super().__init__("Orc", health=80, attack_power=12, loot=loot, image="assets/orc_icon.png") 