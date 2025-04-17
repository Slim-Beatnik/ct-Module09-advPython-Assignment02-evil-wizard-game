from random import randint
import gc
import time

# Base Character class
class Character:    
    my_turn = True
    invulnerable_turns = 0
    invulnerable_type = ['is shielded', 'is evading', 'has a magic barrier']
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
        # specials hash w/ ability_num, hash of type, function, arguments, name, print_phrase and description -- called from menu by choice input
        
        self.team = []
        
        self.specials = {
            '1': {
                'type': '', # ability or attack
                'func': None, # backend
                'args': [], # custom args list for flexibility
                'name': '', # name for function output, and description
                'print_phrase': '', # ability description for function output
                'description': '' # description for turn_menu in battle() -- see main
            },
            '2': {},
            '3': {},
            '4': {}
        }
        
        self.attack_names = {
            'light': '',
            'heavy': ''
        }
        
    # set attack names sets values of dictionary -> names of light attack, heavy attack, special attack 1, and special attack 2
    def set_attack_names(self, light_attack_name, heavy_attack_name):
        self.attack_names['light'] = light_attack_name
        self.attack_names['heavy'] = heavy_attack_name

    def focus(self):
        self.cooldown_turns += 1 #if in cooldown when activated, character will remain in cooldown
        self.action_points += randint(self.max_action_points // 2, self.max_action_points)  # Regain a random amount from half upto full
        self.action_points = min(self.action_points, self.max_action_points) # no conditional, maintain action point cap
        print(f"{self.name} is focusing their energy to restore some action point.")
    
    def light_attack(self) -> tuple:
        self.action_points -= 1
        return randint(self.attack_power - 5, self.attack_power), self.attack_names['light']
    
    def heavy_attack(self) -> tuple:
        self.action_points -= 2
        return randint(self.attack_power - 5, self.attack_power + 10), self.attack_names['heavy']
    
    def attack(self, attack_output_tuple): # takes light or heavy attack output as argument tuple( num, attack name as string)
        if type(self).__module__ == 'npc_classes': # if npc class
            opponent = self.opponents[-1] # target last enemy in player.team list
        else:
            opponent = self.target_opponent() # if player, opponents[0] or prompt by opponents length
        if opponent.invulnerable_turns: # once opponent chosen, check if they're currently invulnerable
            print(f"{opponent.name} {opponent.invulnerable_type} and takes no damage from {self.name}'s {attack_output_tuple[1]} attack")
        else:
            opponent.health -= attack_output_tuple[0]
            print(f"{self.name} attacks {opponent.name} with {attack_output_tuple[1]} for {attack_output_tuple[0]} damage!")
    
    def perform_special(self, ability_num):
        self.action_points -= 2
        self.cooldown_turns = 2
        
        special = self.specials[ability_num]
        
        original_desc = special['print_phrase'] #capture original description in case descriptions have conditional changes
        
        print(f"{special['name']} activated!")
        special['func'](*special['args'])
        
        if special['type'] == 'ability':
            print(f"With {self.verba[0]}, you {special['print_phrase']}. The evil wizard stands there {self.verba[1]}, almost in awe of such awesome power.\n\"THAT POWER WILL BE MINE, TOO!\" The power-blinded wizard shrieks")
        elif special['type'] == 'attack':
            print(f"You {special['print_phrase']}. The wizard howls at a maddening decibel.\n\"You are strong, but you'll never truly hurt me!\" The wizard seethed and spat curses.")
            print(f"\"Your reaction says otherwise,\" you quip.")
            
        special['print_phrase'] = original_desc # revert to original
        
    #[SIC] Add your heal method here
    # heal 1/3 to 1/2 health -- no conditional takes min health + additional(third or half) vs max health to maintain cap
    def heal(self):
        self.action_points -= 3
        self.health = min(self.max_health, self.health + randint(self.max_health // 3, self.max_health // 2))
        print(f"{self.name}'s health has been rejuvinated. Their current health is {self.health}/{self.max_health}")
    
    def display_stats(self):
        stats = f"{self.name}'s Stats\nHealth Points: {self.health}/{self.max_health}\t|\tAttack Power: {self.attack_power}\t|\tAction Points: {self.action_points}\n"
        has_status = lambda stat: 'Yes' if stat else 'No'
        status = f"Invulnerable?: {has_status(self.invulnerable_turns)}\t|\tParalyzed?: {has_status(self.paralyzed_turns)}\t\t|\tIn Cooldown?: {has_status(self.cooldown_turns)}\n"
        print(stats + status)
        
    def target_opponent(self):
        if len(self.opponents) == 1: return self.opponents[0] # target wizard if no other option
        
        print('----Your opponents----')
        for i in range(len(self.opponents)):
            print(f'{i + 1}.\t{self.opponents[i].name}')
        try:
            char_choice = input('number:')
            print('\n\n\n')
            if char_choice in ('1', '2', '3'):
                return self.opponents[int(char_choice) - 1]
            else:
                raise ValueError
        except ValueError: 
            print("I don't know who that is, but they're not here. Please try again.")
            time.sleep(1)
            return self.target_opponent()
            
    def align_minions(self):
        for minion in self.team[1:]:
            minion.team = self.team
            minion.invulnerable_type = self.invulnerable_type
            minion.opponents = self.opponents
            
    def toggle_turn(self):
        self.my_turn = not self.my_turn
    
    def clear_dead(self):
        for opp in self.opponents[1:]:
            if opp.health <= 0:
                print(f"{opp.name} is dead.")
                self.opponents.remove(opp)
                del opp
                gc.collect()
        
    def end_turn(self):
        self.action_points += 1
        self.clear_dead()
        for character in self.team:
            self.decrement_status_turns(character)
        # only toggle turns for EvilWizard or Player
        if type(self).__name__ == 'EvilWizard' or type(self).__module__ == 'player_classes':
            self.toggle_turn()
            self.opponents[0].toggle_turn()
    
    def take_turn(self):
        self.opponents = self.opponents[0].team # update opponents based on enemy team
        self.align_minions()
        if self.paralyzed_turns:
            print(f"{self.name} is paralyzed and cannot take their turn")
            self.decrement_status_turns(self)
            self.end_turn()
        else:
            while self.my_turn:
                available_options = [1, 6]
                print("\n--- Your Turn ---")
                print("1. Focus Energy - Add Action Points")
                if self.action_points >=  1:
                    available_options.append(2)
                    print(f"2. Use {self.attack_names['light']} - Light Attack")
                if self.action_points >=  2:
                    available_options.append(3)
                    print(f"3. Use {self.attack_names['heavy']} - Heavy Attack")
                    if not self.cooldown_turns:
                        available_options.append(4)
                        print("4. Go to Special Abilities and Attacks Menu")
                if self.action_points >= 3:
                    available_options.append(5)
                    print("5. Heal Yourself")
                print("6. View Stats - Your team's Stats and Enemy Team Stats")
        

                choice = input("Choose an action: ")
                print('\n\n\n')
                #disable actions based on if they are part of the action menu
                if choice == '1':
                    self.focus()
                elif choice == '2':
                    self.attack(self.light_attack())
                elif choice == '3' and int(choice) in available_options:
                    self.attack(self.heavy_attack())
                elif choice == '4' and int(choice) in available_options:
                    self.specials_prompt()
                elif choice == '5' and int(choice) in available_options:
                    self.heal()
                elif choice == '6':
                    print(f'Player: ')
                    self.display_stats()
                    if len(self.team) > 1:
                        print("Player's Team: ")
                        for member in self.team[1:]:
                            member.display_stats()
                    
                    print('Enemy Team:')
                    for opp in self.opponents:
                        opp.display_stats()
                    
                    input('Press Enter key to return to the turn menu...')
                    print('\n\n\n')
                    self.take_turn() # displaying stats doesn't skip turn
                else:
                    print(f"{self.name}, don't fail us. Choose from the available options.")
                    self.take_turn()
                self.end_turn()
                time.sleep(1.5)
            
    def specials_prompt(self):
        print("\n--- Specials Actions---")
        for i, special in enumerate(self.specials.values()):
            print(f"{i+1}. {special['name']}\n{special['description']}")
            print()
        ability_num = input("Choose a special: ")
        print('\n\n\n')
        if ability_num in self.specials:
            self.perform_special(ability_num)
        else:
            print(f"{self.name}, choose a valid special.")
            print("ps, if you mess this up you'll be sent to the turn menu")
            ans = input('Would you like to try again, or go back to the menu? (retry/menu):')
            print('\n\n\n')
            
            if ans == 'menu':
                self.take_turn()
            else:
                self.specials_prompt()
    
    @staticmethod
    # run on opponents between turns 
    def decrement_status_turns(character):
        character.paralyzed_turns = max(0, character.paralyzed_turns - 1)
        character.invulnerable_turns = max(0, character.invulnerable_turns - 1)
        character.cooldown_turns = max(0, character.cooldown_turns - 1)
    
    # def __str__(self):
    #     stats = f"{self.name}'s Stats\nHealth Points: {self.health}/{self.max_health}\t|\tAttack Power: {self.attack_power}\t|\tAction Points: {self.action_points}\n"
    #     has_status = lambda stat: 'Yes' if stat else 'No'
    #     status = f"Invulnerable?: {has_status(self.invulnerable_turns)}\t|\tParalyzed?: {has_status(self.paralyzed_turns)}\t\t|\tIn Cooldown?: {has_status(self.cooldown_turns)}\n"
    #     return stats + status
    
    # def __repr__(self):
    #     data = lambda character: [type(character).__name__, character.name, character.health, character.max_health, character.attack_power, character.my_turn, character.cooldown_turns, character.invulnerable_turns, character.paralyzed_turns]
    #     return 'class_name: {}\ncharacter_name: {}\nhealth: {}\nmax_health: {}\nattack_power: {}\nmy_turn?: {}\ncooldown_turns: {}\ninvulnerable_turns: {}\nparalyzed_turns: {}'.format(*data(self))
