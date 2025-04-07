from random import randint

# Base Character class
class Character:    
    my_turn = True
    invulnerable_turns = 0
    invulnerable_type = ['are shielded', 'will evade', 'have a magic barrier', 'will counter-attack']
    cooldown_turns = 0
    paralyzed_turns = 0
    # verbum ad tuum momma
    # verba = [noun, verb, past-participle, past-participle, noun, verb ending in -es]
    verba = []
    opponents = [None]
    
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
        
        self.team = [self]
        
    # set attack names sets values of dictionary -> names of light attack, heavy attack, special attack 1, and special attack 2
    def set_attack_names(self, light_attack_name, heavy_attack_name):
        self.attack_names['light'] = light_attack_name
        self.attack_names['heavy'] = heavy_attack_name

    def attack(self, attack_func):
        if type(self).__name__ in [EvilWizard, SummonedEntity]: # if npc class
            opponent = self.opponents[-1]
        else:
            opponent = self.target_opponent()
        attack_output = attack_func
        opponent.health -= attack_output[0]
        print(f"{self.name} attacks {opponent.name} with {attack_output[1]} for {attack_output[0]} damage!")

    def focus(self):
        self.cooldown_turns += 1
        self.action_points += randint(self.max_action_point // 2, self.max_action_points)  # Regain a random amount from half upto full
        print(f"{self.name} is focusing their energy to restore some action point.")
    
    def light_attack(self):
        self.action_points -= 1
        return randint(self.attack_power - 5, self.attack_power), self.attack_names['light']
    
    def heavy_attack(self):
        self.action_points -= 2
        return randint(self.attack_power - 5, self.attack_power + 10), self.attack_name['heavy']
    
    def perform_special(self, ability_num):
        self.action_points -= 2
        self.cooldown_turns = 1
        
        special = self.specials[ability_num]
        
        original_desc = special['print_desc'] #capture original description in case descriptions have conditional changes
        
        print(f"{special['name']} activated!")
        special['func'](*special['args'])
        
        if special['type'] == 'ability':
            print(f"With {verba[0]}, you {special['print_desc']}. The evil wizard stands there {verba[1]}, almost in awe of such awesome power.\n\"THAT POWER WILL BE MINE, TOO!\" The power-blinded wizard shrieks")
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
        print(f"{self.name}'s health has been rejuvinated.")
        
    def display_stats(self):
        print(f"{self.name}'s Stats - Health Points: {self.health}/{self.max_health}, Attack Power: {self.attack_power}, Action Points: {self.action_points}")
        has_status = lambda stat: 'Yes' if stat else 'No'
        print(f"Invulnerable?:\t{has_status(self.invulnerable_turns)}| Paralyzed?:\t  {has_status(self.paralyzed_turns)}| In Cooldown?: {has_status(self.cooldown_turns)}\n")
        
    def __str__(self):
        return f"Name: {self.name}\n Health: {self.health}\n Attack Power: {self.attack_power} specials: {self.specials} myTurn? {self.my_turn} inCd? {self.cooldown_turns} inv? {self.invulnerable_turns}"
        
    def target_opponent(self):
        if len(self.opponents) == 1: return self.opponents[0] # target wizard if no other option
        
        print('----Your opponents----')
        for i in range(len(self.opponents)):
            print(f'{i + 1}.\t{self.opponents[i].name}')
        try:
            char_choice = input('Choose your target by name or number:')
            if char_choice not in map(lambda opp: opp.name, self.opponents) or char_choice not in ['1', '2', '3']:
                raise ValueError
            if char_choice in ['1', '2', '3']:
                return opponents[int(char_choice) - 1]
            else:
                for opp in opponents:
                    if opp.name.lower() == char_choice.lower() or char_choice.lower() in opp.name.lower():
                        return opp
        except ValueError: 
            print("I don't know who that is, but they're not here. Please try again.")
            time.sleep(1)
            target_opponents(self.opponents)
            
    def align_minions(self):
        for minion in self.team[1:]:
            minion.team = self.team
            minion.opponents = self.opponents
    
    def take_turn(self):
        while self.my_turn:
            available_options = [1, 6]
            print("\n--- Your Turn ---")
            print("1. Focus Energy")
            if self.action_points >=  1:
                available_options.append(2)
                print("2. Use Light Attack")
            elif self.action_points >=  2:
                available_options.append(3)
                print("3. Use Heavy Attack")
                if not self.cooldown:
                    available_options.append(4)
                    print("4. Use Specia)")
            elif self.action_points >= 3:
                available_options.append(5)
                print("5. Heal")
            print("6. View Stats")
    

            choice = input("Choose an action: ")
            #disable actions based on if they are part of the action menu
            if choice == '1':
                self.attack(self.light_attack(self.attack_name['light']), wizard)
            elif choice == '2' and choice in available_options:
                self.attack(self.heavy_attack(self.attack_name['heavy']), wizard)
            elif choice == '3' and choice in available_options:
                specials_prompt()
            elif choice == '4' and choice in available_options:
                self.heal()
                
            elif choice == '5':
                print(f'Player: ')
                self.display_stats()
                
                print('Enemy Team:')
                for opp in self.opponents:
                    opp.display_stats()
                
                input('Press any key to return to the turn menu...')
                turn_menu(self) # displaying stats doesn't skip turn
            else:
                print(f"{self.name}, don't fail us. Choose from the available options.")
                turn_menu(self)
            toggle_turn()
        clear_dead()
    
    @classmethod
    def toggle_turn(cls):
        cls.my_turn = not cls.
        
    def clear_dead(self):
        for opp in opponents[1:]:
            if opp.health <= 0:
                print(f"{opp.name} is dead.")
                del opp
        gc.collect()