from weapon import Sword, Wand

#Super classe personagem com atributos básicos e métodos
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
            return f"Usou uma poção de vida. Curou {heal_amount} de vida!"
        return "Não há poções de vida disponíveis!"

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
        return f"Level Up! Agora você está no nível {self.level}! Vida e poder de ataque aumentados!"

#Subclasse guerreiro com as especificações como arma, quantidade inicial de vida e poder de ataque e raiva
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=15)
        self.weapon = Sword()
        self.rage = 0

    def special_ability(self):
        if self.rage >= 30:
            self.rage = 0
            return "Fúria Berserker: Dano duplo para o próximo ataque!", self.attack() * 2
        self.rage += 10
        return "Não há fúria suficiente! (Ganhou 10 fúria)", self.attack()
    
#Subclasse mago com as especificações como arma, quantidade inicial de vida e poder de ataque e mana
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=80, attack_power=10)
        self.weapon = Wand()
        self.mana = 100

    def special_ability(self):
        if self.mana >= 30:
            self.mana -= 30
            return "Bola de Fogo: Causar dano mágico devastador!", self.attack() * 1.8
        return "Não há mana suficiente!", self.attack() 