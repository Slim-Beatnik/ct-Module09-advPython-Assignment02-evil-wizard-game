from random import randint
# Base Character class
class Character:
    def __init__(self, name, health, attack_power, action_points):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.action_points = action_points # action points define repeating attacks, except light attacks
        
        self.max_health = health  # Store the original health for maximum limit
        self.max_action_points = action_points # Store the original action points for maximum limit

    def attack(self, attack_type, opponent):
        attack_output = attack_type(self.attack_power)
        opponent.health -= attack_output[0]
        print(f"{self.name} attacks {opponent.name} with a {attack_output[1]} attack for {attack_output[0]} damage!")
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")
            
    def light_attack(self, name):
        return (randint(self.attack_power // 2 + 5, self.attack_power), name)
    
    def heavy_attack(self, name):
        self.action_points -= 1
        return (randint(self.attack_power - 5, self.attack_power + 10), name)
    
    def special_attack(self, name):
        self.action_points -= 2
        return (randint(self.attack_power, self.attack_power * 2), name)
    
    def special_action(self, name, abilityHash):
        self.action_points -= 2
        return (abilityHash[func](abilityHash[args]), name)

    def display_stats(self):
        print(f"{self.name}'s Stats - Health: {self.health}/{self.max_health}, Attack Power: {self.attack_power}")

    def __repr__(self):
        return f"Name: {self.name}, Health: {self.health}, Attack Power: {self.attack_power}, 
    
    # Add your heal method here
    def heal(self, amount):
        self.action_points -= 2
        if self.health + amount > self.max_health:
            self.health = self.max_health
        else:
            self.health += amount
        print(f"{self.name} healed themselves for {amount} hp! Current health: {self.health}")


# Warrior class (inherits from Character)
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=140, attack_power=25, action_points=6)  # Boost health and attack power

    # Add your power attack method here


# Mage class (inherits from Character)
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=35, action_points=6)

    # Add your cast spell method here

class Archer(Character):
    def __init__(self, name):
        super().__init__(name, health=80, attack_power=20, action_points=8)
        
class Paladin(Character):
    def __init__(self, name):
        super().__init__(name, health=120, attack_power=30, action_points=5) 
    
class Traveler(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=20, action_point=20)

# EvilWizard class (inherits from Character)
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=250, attack_power=20, action_points=12)  # Lower attack power
    
    # Evil Wizard's special ability: it can regenerate health
    def regenerate(self):
        self.health += 5  # Lower regeneration amount
        print(f"{self.name} regenerates 5 health! Current health: {self.health}")