from random import randint
# Base Character class
class Character:    
    my_turn = True
    invulnerable_turns = 0
    cooldown_turns = 0
    paralized_turns = 0
    # verbum ad tuum momma
    # verba = [noun, verb, past-participle, past-participle, noun, verb ending in -es]
    verba = []
    
    
    def __init__(self, name, health, attack_power, action_points):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.action_points = action_points # action points define repeating attacks, except light attacks
        
        self.max_health = health  # Store the original health for maximum limit
        self.max_action_points = action_points # Store the original action points for maximum limit
        # specials hash w/ ability_num, hash of type, function, arguments, name, print_desc and menu_desc -- called from menu by choice input
        self.specials = {
            '1': {
                'type': '', # ability or attack
                'func': None, # backend
                'args': [], # custom args list for flexibility
                'name': '', # name for function output, and menu_desc
                'print_desc': '', # ability description for function output
                'menu_desc': '' # description for turn_menu in battle() -- see main
            },
            '2': {},
            '3': {},
            '4': {}
        }
        self.attack_names = {
            'light': '',
            'heavy': ''
        }

    def attack(self, attack_func, opponent):
            attack_output = attack_func
            opponent.health -= attack_output[0]
            print(f"{self.name} attacks {opponent.name} with {attack_output[1]} for {attack_output[0]} damage!")
        
    # set attack names sets values of dictionary -> names of light attack, heavy attack, special attack 1, and special attack 2
    def set_attack_names(self, light_attack_name, heavy_attack_name):
        self.attack_names['light'] = light_attack_name
        self.attack_names['heavy'] = heavy_attack_name
        
    # Mage class inherits from Character
    def light_attack(self):
        return randint(self.attack_power - 5, self.attack_power), self.attack_names['light']
    
    def heavy_attack(self):
        self.action_points -= 1
        return randint(self.attack_power - 5, self.attack_power + 10), self.attack_name['heavy']
    
    def perform_special(self, ability_num):
        self.action_points -= 2
        self.cooldown_turns = 1
        
        special = self.specials[ability_num]
        
        original_desc = special['print_desc'] #capture original description in case descriptions have conditional changes
        
        print(f"{special['name']} activated!")
        special['func'](*special['args'])
        
        if special['type'] == 'ability':
            print(f"With a {verba[0]}, you {special['print_desc']}. The evil wizard stands there {verba[1]}, almost in awe of such awesome power.\n\"THAT POWER WILL BE MINE, TOO!\" The power-blinded wizard shrieks")
        elif special['type'] == 'attack':
            print(f"You {special['print_desc']}. The wizard howls at a maddening decibel.\n\"You are strong, but you'll never truly hurt me!\" The wizard seethed and spat curses.")
            print(f"\"Your reaction says otherwise,\" you quip.")
            
        special['print_desc'] = original_desc # revert to original
    
    # Add your heal method here
    def heal(self, amount):
        self.action_points -= 3
        if self.health + amount > self.max_health:
            self.health = self.max_health
        else:
            self.health += amount
        print(f"{self.name} healed themselves for {amount} hp! Current health: {self.health}")
        
    def display_stats(self):
        print(f"{self.name}'s Stats - Health: {self.health}/{self.max_health}, Attack Power: {self.attack_power}")
        
    def __str__(self):
        return f"Name: {self.name}\n Health: {self.health}\n Attack Power: {self.attack_power} specials: {self.specials} myTurn? {self.my_turn} inCd? {self.cooldown_turns} inv? {self.invulnerable_turns}"
        
    @classmethod
    def toggle_turn(cls):
        cls.my_turn = not cls.my_turn