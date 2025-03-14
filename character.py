from weapon import Sword, Wand

class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.weapon = None
        self.gold = 0
        self.health_potions = 0
        self.level = 1
        self.experience = 0

    def attack(self):
        if self.weapon:
            return self.attack_power + self.weapon.damage
        return self.attack_power

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def use_health_potion(self):
        if self.health_potions > 0:
            self.health_potions -= 1
            heal_amount = 30
            self.health = min(self.max_health, self.health + heal_amount)
            return f"Used a health potion. Healed for {heal_amount} HP!"
        return "No health potions available!"

    def collect_loot(self, loot):
        self.gold += loot.get('gold', 0)
        self.health_potions += loot.get('health_potion', 0)
        
        return f"Coletado: {loot['gold']} de ouro, {loot.get('health_potion', 0)} poções de vida"

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= 100:
            self.level_up()
            
    def level_up(self):
        self.level += 1
        self.experience = 0
        self.max_health += 20
        self.health = self.max_health
        self.attack_power += 5
        return f"Level Up! Now level {self.level}! Health and attack power increased!"

class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=15)
        self.weapon = Sword()
        self.rage = 0

    def special_ability(self):
        if self.rage >= 30:
            self.rage = 0
            return "Berserker Rage: Double damage for next attack!", self.attack() * 2
        self.rage += 10
        return "Not enough rage! (Gained 10 rage)", self.attack()

class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=80, attack_power=10)
        self.weapon = Wand()
        self.mana = 100

    def special_ability(self):
        if self.mana >= 30:
            self.mana -= 30
            return "Fireball: Deal massive magical damage!", self.attack() * 1.8
        return "Not enough mana!", self.attack() 