from character import *
from gc import *

# EvilWizard class (inherits from Character)
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=250, attack_power=20, action_points=12)  # Lower attack power
        self.my_turn = False
        self.invulnerable_type = self.invulnerable_type[2]
        self.set_attack_names('Shadow Strike', 'Dark Bolt')
        self.specials['1'] = {
            'type': 'ability',
            'func': self.sab_become_invincible,
            'name': 'Become Invicible',
            'print_phrase': f'clasps their hands together. A magic glowing shield encase the air around {self.name}. The invinciblity spell will last for 2 turns',
            'description': ''
        }
        self.specials['2'] = {
            'type': 'ability',
            'func': self.sab_summon_minions,
            'name': 'Summon Minions',
            'print_phrase': """releases the magic staff. It hangs in the air as bolts of dark lightning shoot from the wizard's hands, striking the ground.
                Two minions struggle from the crysalis made from dark magic and molten earth.
                Having clambored and clawed to his side, they stand ready to fight for the wizard.""",
            'description': ''
        }
        self.specials['3'] = {
            'type': 'attack',
            'func': self.sat_dark_lightning_strike,
            'name': 'Dark Lightning Strike',
            'print_phrase': 'shoots the same lightning strike at you used to conjure or disintegrate the minions. The air crackles with dark energy as the bolt strikes.',
            'description': ''
        }
        self.specials['4'] = {
            'type': 'attack',
            'func': self.sat_meteor_shower,
            'name': 'Meteor Shower',
            'print_phrase': f"raises their arms and as they crash down, with them, firely rocks plummet from the sky with your name on them. They breakup on their approach, striking {'your entire team' if len(self.opponents) > 1 else 'you'}.",
            'description': ''
        }
    
    # Adjust for paralysis and cooldown - if cooldown wizard attack doesn't include specials. Action points regen after turn complete.
    def take_turn(self):
        self.opponents = self.opponents[0].team # update opponents based on enemy team
        self.align_minions()
        if self.paralyzed_turns:
            print(f'{self.name} just stands there.')
            Character.decrement_status_turns(self)
            
        else:
            if self.action_points < 1:
                print(f"{self.name} regains 5 action points.")
                self.action_points += 5
                Character.decrement_status_turns(self)
                return
            if self.action_points >= 1:
                wizard_attacks = [self.light_attack()]
            if self.action_points >= 2:  # Only add heavy attack if there's enough action points
                wizard_attacks += [self.heavy_attack()]
            if not self.cooldown_turns:
                wizard_attacks += [str(x) for x in range(1, len(self.specials) + 1)] # add specials if not in cooldown

            # Randomly choose an attack from the list - scalable w/ added attacks
            automatic_choice = randint(0, len(wizard_attacks) - 1)
            if automatic_choice <= 1:
                self.attack(wizard_attacks[automatic_choice])
            else:
                # ability num as string from wizard_attacks
                self.perform_special(wizard_attacks[automatic_choice])
            if self.action_points >= 3 and self.health != self.max_health:
                self.regenerate()


        if len(self.team) > 1:
            for minion in self.team[1:]:
                minion.take_turn()
                
        self.end_turn()
        
        
    #override perform_special to remove prompts and to keep the same essential
    def perform_special(self, ability_num): # ap - 2, cd = 2
        self.action_points -= 2
        self.cooldown_turns = 2
        special_attack = self.specials[ability_num]
        print(f"{special_attack['name']} activated!")        
        print(f"The Evil Wizard {special_attack['print_phrase']}")
        special_attack['func']()

    
    def sab_become_invincible(self):
        self.invulnerable_turns = 3
        print(f"{self.name} laughs menacingly, a shimmering dark energy enveloping and distorting their sneering chortling form.")
        
    def sab_summon_minions(self):
        # remaining minions will be replaced, so no more than 2 minions are allowed simultaneously
        if len(self.team) > 1:
            print(f"The wizard's remaining living minions screech and howl as they are eaten by their replacements. You will not soon forget that sound.")
            for minion in self.team[1:]:  # Remove existing summoned entities
                del minion
                gc.collect()  # Force garbage collection to remove the minion from memory
        self.team = [self, SummonedEntity('Mangled Abomination', 'Electrocution', 'Ethereal Smog', health = randint(30, 40), attack_power = randint(10, 20)), SummonedEntity('Enslaved Cherufe', 'Obsidian Fist', 'Molten Spray', health = randint(30, 40), attack_power = randint(10, 20))]  # Summon two minions to fight for the wizard
        self.align_minions() # set minion.team and minion.opponents to the summoner's team and opponents
    
    
    # Heavy attack w/ effect
    def sat_dark_lightning_strike(self):
        opponent = self.opponents[-1]  # Always attack the last opponent
        if opponent.invulnerable_turns:
            print(f'Curse your skills, {opponent.name}. \"I *WILL* kill you!\" The wizard cried as the attack fizzled and did nothing.')
            return
        opponent.paralyzed_turns = randint(2, 3)  # Paralyze the last opponent for 1 or 2 turns - stats decremented at end of turn
        damage = randint(self.attack_power - 5, self.attack_power + 10)
        print(f"{opponent.name} finds themselves in excruciating pain, and unable to move. The attack so sudden, from their point of view, they then watch the attack in slow motion.")
        print(f"Over what seems like the next 20 minutes, {opponent.name} takes {damage} damage!")
    
    # Heavy attack against all opponents
    def sat_meteor_shower(self):
        for opp in self.opponents:
            damage = randint(self.attack_power - 5, self.attack_power + 10)
            if opp.invulnerable_turns:
                print(f"{opp.name} {opp.invulnerable_type} and receives no damage")
            else:
                opp.health -= damage
                print(f"{opp.name} is struck for {damage} damage!")
    
    # Evil Wizard's special ability: it can regenerate health
    def regenerate(self):
        self.action_points -= 3
        opponent = self.opponents[0] # regen always based on player
        regen_this_turn = randint(5, opponent.attack_power)
        self.health = min(self.max_health, self.health + regen_this_turn)  #[Sic] Lower regeneration amount
        print(f"{self.name} regenerates {regen_this_turn} health! Current health: {self.health}")
    
class SummonedEntity(Character):
    def __init__(self, name, attack1, attack2, health=40, attack_power=15):
        super().__init__(name, health, attack_power, action_points=1000) # Summoned entities appear to not loose stamina
        self.set_attack_names(attack1, attack2)
    
    # randomly chooses between light and heavy attacks
    def take_turn(self):
        if self.paralyzed_turns:
            print(f'{self.name} is stuck in place unable to attack.')
        else:
            opponent = self.opponents[-1] # summoned entities always attack last opponent
            if opponent.invulnerable_turns:
                print(f'{opponent.name} {opponent.invulnerable_type} and received no damage from {self.name}')
            else:
                attack_output = [self.light_attack(), self.heavy_attack()][randint(0, 1)]
                self.attack(attack_output)
        self.end_turn()
        
    