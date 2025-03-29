from character import *

"""my_turn = True
    invulnerable_turns = 0
    cooldown_turns = 0
    paralized_turns = 0
    # verba = [noun, verb, past-participle, past-participle, noun, verb ending in -es]
    verba = []
    def __init__(self, name, health, attack_power, action_points):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.action_points = action_points # action points define repeating attacks, except light attacks
        
        self.max_health = health  # Store the original health for maximum limit
        self.max_action_points = action_points # Store the original action points for maximum limit
        # specials hash w/ function, arguments, name, and description
        self.specials = {
            '1': {
                'type': 'ability',
                'func': None,
                'args': [],
                'name': '',
                'print_phrase': '',
                'description': ''
            }   *4
        }
        self.attack_names = {
            'light': '',
            'heavy': ''
        }"""

# Warrior class (inherits from Character)
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=140, attack_power=25, action_points=6) 
        self.set_attack_names('Slash', 'Mighty Swing')
        # special funcs will start with sab or sat, [s]pecial [ab]ility or [s]pecial [at]tack respectively
        specials['1'] = {
            'type': 'ability',
            'func': self.sab_find_shield,
            'args': [opponents],
            'name': 'Improvised Shield',
            'print_phrase': 'You grab the armor from the half-buried remains of two fallen heroes. With a grunt you pull them from the ground and hold them in front of you. A morbid detritus is flung in all directions',
            'description': 'Shield yourself for 2 turns'
        }
        specials['2'] = {
            'type': 'ability',
            'func': self.sab_gain_strength,
            'args': [],
            'name': 'Gain Strength',
            'print_phrase': 'harness your adrenaline and will your muscles stronger. The wizard senses a shift in your prowess',
            'description': 'Add 10 points to your base attack power'
        }
        specials['3'] = {
            'type': 'attack',
            'func': self.sat_intimidate_reality,
            'args': [opponent],
            'name': 'Intimidate Reality',
            'print_phrase': 'cry at the heavens with a mighty roar. Your attack is mighty and unstoppable',
            'description': 'Opponent loses shield and you hit will do double your base power in damage'
        }
        specials['4'] = {
            'type': 'attack',
            'func': self.sat_throw_something,
            'args': [opponent, '4'],
            'name': 'Throw something',
            'print_phrase': "grip something you saw out of the corner of your eye. ",
            'description': 'Throw something as hard as you can. It can do up do double damage.'
        }
        
        #With a {verba[0]}, you {ability['desc']}. The evil wizard stands there {verba[1]}, almost in awe of such awesome power
        # Your corpse will be paraded around the kingdom, the {verba[2]} {verba[3]} which will instill inaction for the coming generations.\nThe evil wizard's reign will be unending. All hope {verba[4]}
        self.verba = ['a complete lack of grace', 'in utter disbelief', 'glinting', 'volcanic glass that was a person, is imortalized. The face, melting, frames a grimace of abject terror', 'is harder than your monument to failure.']



    def sab_find_shield(self, opponents):
        self.invulnerable_turns = 2
        for opponent in opponents:
            opponent.health -= randint(2, 5)
            
    def sab_gain_strength(self):
        self.attack_power += 10
        self.cooldown = False
        print(f"{self.name} gains 10 attack power! Current attack power: {self.attack_power}")
            
    def sat_intimidate_reality(self, opponent):
        opponent.invulnerable_turns = 0
        opponent.health -= 2 * self.attack_power
        
    def sat_throw_something(self, opponent, ability_num):
        power_range = (self.attack_power - 10, self.attack_power * 2 + 1)
        something = randint(*power_range)
        opponent.health
        # throw something random based on attack_power - your mom, if you roll a nat20
        if something in range(power_range[0], power_range[1] / 3 + 1):
            something_string = 'A rat'
        elif something in range(power_range[1] / 3, power_range[1] * 2/3 + 1):
            something_string = 'A disembodied spine'
        elif something in range(power_range[1] * 2/3, power_range[1] * 2):
            something_string = 'A boulder'
        elif something == power_range[1] - 1:
            something_string = 'Your mom'
        # print description reverted in super().perform_special
        self.specials[ability_num]['print_desc'] += something_string + " is suddenly flung through the air, hurled at the wizard"

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
    def regenerate(self, opponent):
        self.health += randint(2,opponent.attack_power)  # Lower regeneration amount
        print(f"{self.name} regenerates 5 health! Current health: {self.health}")