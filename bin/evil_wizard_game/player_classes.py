from character import *
from functools import partial
from npc_classes import  SummonedEntity

# Warrior class (inherits from Character)
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=140, attack_power=25, action_points=6) 
        self.set_attack_names('Slash', 'Mighty Swing')
        
        # ['are shielded', 'will evade', 'have a magic barrier', 'will counter-attack']
        self.invulnerable_type = self.invulnerable_type[0] # 'are shielded'
        # special funcs will start with sab or sat, [s]pecial [ab]ility or [s]pecial [at]tack respectively
        self.specials['1'] = {
            'type': 'ability',
            'func': self.sab_find_shield,
            'args': [],
            'name': 'Improvised Shield',
            'print_phrase': 'You grab the armor from the half-buried remains of two fallen heroes. With a grunt you pull them from the ground and hold them in front of you. A morbid detritus is flung in all directions',
            'description': 'Shield yourself for 2 turns'
        }
        self.specials['2'] = {
            'type': 'ability',
            'func': self.sab_gain_strength,
            'args': [],
            'name': 'Gain Strength',
            'print_phrase': 'harness your adrenaline and will your muscles stronger. The wizard senses a shift in your prowess',
            'description': 'Add 10 points to your base attack power'
        }
        self.specials['3'] = {
            'type': 'attack',
            'func': self.sat_intimidate_reality,
            'args': [],
            'name': 'Intimidate Reality',
            'print_phrase': 'cry at the heavens with a mighty roar. Your attack is mighty and unstoppable',
            'description': 'Opponent stripped of boon status (invincibility) and you hit will do double your base power in damage'
        }
        self.specials['4'] = {
            'type': 'attack',
            'func': self.sat_throw_something,
            'args': ['4'],
            'name': 'Throw Something',
            'print_phrase': "grip something you saw out of the corner of your eye. ",
            'description': "Throw something as hard as you can. It can do up do double damage. Such an unexpected and random attack disolves an enemy target's shield."
        }
        
        #With a {verba[0]}, you {ability['desc']}. The evil wizard stands there {verba[1]}, almost in awe of such awesome power
        # Your corpse will be paraded around the kingdom, the {verba[2]} {verba[3]} which will instill inaction for the coming generations.\nThe evil wizard's reign will be unending. All hope {verba[4]}
        self.verba = ['a complete lack of grace', 'in utter disbelief', 'glinting', 'volcanic glass that was a person, is imortalized. The face, melting, frames a grimace of abject terror', 'is harder than your monument to failure.']

    def sab_find_shield(self):
        self.invulnerable_turns = 2
        for opponent in self.opponents: # no target opponent - effects all opponents
            opponent.health -= randint(2, 5)
            
    def sab_gain_strength(self):
        self.attack_power += 10
        print(f"{self.name} gains 10 attack power! Current attack power: {self.attack_power}")
            
    def sat_intimidate_reality(self):
        opponent = self.target_opponent()
        opponent.invulnerable_turns = 0
        opponent.health -= 2 * self.attack_power
        
    def sat_throw_something(self, ability_num):
        power_range = (self.attack_power - 10, self.attack_power * 2)
        something = randint(*power_range)
        opponent = self.target_opponent()
        opponent.invulnerable_turns = 0
        opponent.health -= something
        # throw something random based on attack_power - your mom, if you roll a nat20
        if something in range(power_range[0], power_range[1] // 3 + 1):
            something_string = 'A rat'
        elif something in range(power_range[1] // 3, power_range[1] * 2//3 + 1):
            something_string = 'A disembodied spine'
        elif something in range(power_range[1] * 2//3, power_range[1]):
            something_string = 'A boulder'
        elif something == power_range[1]:
            something_string = 'Your mom'
        # print description reverted in super().perform_special
        self.specials[ability_num]['print_phrase'] += f"{something_string} is suddenly flung through the air, hurled at the wizard, doing {something} damage"

# Mage class (inherits from Character)
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=35, action_points=6)
        self.set_attack_names('Magic Pulse', 'White Lightning Bolt')
        # ['are shielded', 'will evade', 'have a magic barrier', 'will counter-attack']
        self.invulnerable_type = self.invulnerable_type[2]  # have a magic barrier
        
        # special funcs will start with sab or sat, [s]pecial [ab]ility or [s]pecial [at]tack respectively
        self.specials['1'] = {
            'type': 'ability',
            'func': self.sab_summon_animal_friend,
            'args': [],
            'name': 'Summon Animal Friend',
            'print_phrase': f"blow a magic whistle and, per your previous agreement, an animal friend comes to your aid. You cast a magical shield on them lasting 1 turn.",
            'description': 'An animal joins your team and will fight to the death. Shielded for first turn.\nStackable: limit of 4. If all animals summoned: randomly increase health and power, remove statuses, and make invulnerable for 1 turn.'
        }
        self.specials['2'] = {
            'type': 'ability',
            'func': self.sab_minor_heal_all_spell,
            'args': [],
            'name': 'Heal All Allies - Minor',
            'print_phrase': 'chant an incantation, and a soft glow envelops your entire team. Their wounds begin to close as the magic takes effect.',
            'description': 'Heal up to 1 wizard attack for each member of your team, including yourself.'
        }
        self.specials['3'] = {
            'type': 'attack',
            'func': self.sat_conjur_lightning_storm,
            'args': [],
            'name': 'Conjure Lightning Storm',
            'print_phrase': 'cry at the heavens with a mighty roar. Your staff pointed above the enemy team, red sprites applify your attack, wherever it lands.',
            'description': "Conjure lightning storm, to paralyze and do up to double damage to a random opponent. It's as random as it is deadly."
        }
        self.specials['4'] = {
            'type': 'attack',
            'func': self.sat_fireball,
            'args': [],
            'name': 'Fireball',
            'print_phrase': "tamp your staff and scream a spell no one hears for the eruption of flame emitted from your off-hand. It stops briefly gaining mass before hurling itself at the enemy team.",
            'description': "Cast the classic fireball spell, dealing damage to all opponents (as surely they're within a 20 foot radius of eachother).\nMay deal damage to teammate for the same reason."
        }
        
        #With a {verba[0]}, you {ability['desc']}. The evil wizard stands there {verba[1]}, almost in awe of such awesome power
        # Your corpse will be paraded around the kingdom, the {verba[2]} {verba[3]} which will instill inaction for the coming generations.\nThe evil wizard's reign will be unending. All hope {verba[4]}
        self.verba = ['a flourish', 'seething', 'ornate talisman buried in your chest.', 'The eternal prison of yours, ', 'is locked away with your slowly maddening psyche']

    
    def sab_summon_animal_friend(self):
        animal = [['Bear', 'Paw Swipe', 'Bite'], ['Wolf', 'Pounce', 'Bite'], ['Spider', 'Leg Strike', 'Venom Blast'],  ['Boar', 'Gouge', 'Tusks Charge']]
        summoned_creature = animal[randint(0, len(animal) - 1)]
        if summoned_creature[0] in [entity.name for entity in self.team]: # Check if the animal is already summoned
            for i, entity in enumerate(self.team):
                if entity.name == summoned_creature[0]:
                    prev_stats = [self.team[i].max_health, self.team[i].attack_power] # get previous stats to add to new SummonedEntity instance
                    self.team[i] = SummonedEntity(*summoned_creature, health = randint(0, 40) + prev_stats[0], attack_power = randint(0, 15) + prev_stats[1])
                    self.team[i].invulnerable_turns = 1  
                    print(f"{summoned_creature[0]} is already summoned, it has been fully healed and purified and it is now stronger.")
        else:
            self.team += [SummonedEntity(*summoned_creature, health = randint(30, 40), attack_power = randint(10, 20))]  # Add a new summoned entity to the team
            self.team[-1].invulnerable_turns = 2  # New summoned entity is invulnerable for 1 turn
            print(f'{summoned_creature[0]} arrived by your side')
        self.align_minions()
            
    def sab_minor_heal_all_spell(self):
        heal_amount = randint(5, self.opponents[0].attack_power)  # Random heal amount between 5 and 20
        for member in self.team:
            if member.health == member.max_health:
                print(f"{member.name}'s already fully healthy!")
            elif member.health + heal_amount > member.max_health:
                member.health = member.max_health  # Heal to max health
                print(f"{member.name} is fully healed now!")
            else:
                member.health += heal_amount
                print(f"{member.name} heals {heal_amount} health!")
            
    def sat_conjur_lightning_storm(self):
        rand_target = self.opponents[randint(0, len(self.opponents) - 1)]
        if rand_target.invulnerable_turns:
            print(f"{rand_target.name} {rand_target.invulnerable_type} and is uneffected")
        else:
            rand_target.paralyzed_turns = randint(1, 2)  # Paralyze a random opponent for 1 or 2 turns
            damage = randint(self.attack_power, self.attack_power * 2)
            print(f"{rand_target.name} took {damage} damage and is now paralyzed for {rand_target.paralyzed_turns} turns.")
        
    def sat_fireball(self):
        affected_opps = []
        power = randint(self.attack_power - 10, self.attack_power * 2)
        teammate_possible_index = randint(1, 5)  # Randomly choose a teammate to possibly hit - smaller teams less likely to have friendly-fire
        too_close = randint(0, 1)  # Randomly determine if the fireball hits a teammate (50% chance)
        if too_close and teammate_possible_index < len(self.team):
            teammate = self.team[teammate_possible_index]
            if teammate.invulnerable_turns:
                print(f"{teammate.name} {teammate.invulnerability_type}. Were it not for that, they would have been singed.")
            else:
                damage = randint(power // 2, power)
                teammate.health -= damage
                print(f"{teammate.name} is singed by the fireball and takes {damage} damage!")
        inv_opps = list(filter(lambda opp: opp.invulnerable_turns, self.opponents))
        if len(inv_opps) == len(self.opponents):
            print(f"They were all invulnerable. The opposing team took no damage")
        else:
            for opp in self.opponents:
                if opp not in inv_opps:
                    affected_opps += [opp]
                    opp.health -= power
            print(f"{" and ".join(map(lambda o: o.name, affected_opps))} received {power} damage from the explosion of the fireball!")


    # Add your cast spell method here

class Archer(Character):
    def __init__(self, name):
        super().__init__(name, health=120, attack_power=20, action_points=30)
        self.set_attack_names('Sonic Shot', 'Barbed Arrow')
        # ['is shielded', 'will evade', 'has a magic barrier']
        self.invulnerable_type = self.invulnerable_type[1]  # will evade
        
        # special funcs will start with sab or sat, [s]pecial [ab]ility or [s]pecial [at]tack respectively
        self.specials['1'] = {
            'type': 'ability',
            'func': self.sab_install_turret,
            'args': [],
            'name': 'Install Turret',
            'print_phrase': f"toss a device. Sprinting you step on the spring-loaded machine. A small inanimate turret pops-up points in the general direction of the enemies and begins to fire slowly.",
            'description': 'Install a small arrow turret, stackable, no limit.'
        }
        self.specials['2'] = {
            'type': 'ability',
            'func': self.sab_one_step_ahead_evasion,
            'args': [],
            'name': 'One-Step-Ahead Evation',
            'print_phrase': 'find the flow of time and the universe, and see every attack coming. Each step towards victory will be one ahead of your enemies.',
            'description': 'Your enemies will be unable to strike you for 7 turns.'
        }
        self.specials['3'] = {
            'type': 'attack',
            'func': self.sat_multi_shot,
            'args': [],
            'name': 'MultiShot',
            'print_phrase': 'grab a comical number of arrows, notched them, aimed towards the heavens. You release them and await gravity to align with your goals.',
            'description': "Shoot 17 arrows simultaneously, random damage to each enemy."
        }
        self.specials['4'] = {
            'type': 'attack',
            'func': self.sat_odeons_crit_shot,
            'args': [],
            'name': "Odeon's Crit Shot",
            'print_phrase': "Your body aligns with you mind, your bow an extention of your will, points to your goal. You can't help but aim for that stupid face.",
            'description': "60 percent of the time it works every time: causing triple damage and breaks their invulnerability spell, if any, or the attack does nothing."
        }
        
        #With a {verba[0]}, you {ability['desc']}. The evil wizard stands there {verba[1]}, almost in awe of such awesome power
        # Your corpse will be paraded around the kingdom, the {verba[2]} {verba[3]} which will instill inaction for the coming generations.\nThe evil wizard's reign will be unending. All hope {verba[4]}
        self.verba = ['lack of wasted motion', 'trying to track the blur of movement', 'paralyze spell', 'seizing your dead muscles even now, ', 'but a dream of yesteryear']

    def sab_install_turret(self):
        if len(self.team) > 1:   
            self.team += [SummonedEntity(f"turret{int(self.team[-1].name[-2:])}", 'Good Shot', 'Better Shot', health = 30, attack_power = 15)]
        else:
            self.team += [SummonedEntity('turret01', 'Good Shot', 'Better Shot', health = 30, attack_power = 15)]
        self.align_minions()
        # 85% chance of attacking successfully
        if randint(1, 20) > 3:
            self.team[-1].take_turn()
        else:
            print("The turret missed its first shot.")
        
            
    def sab_one_step_ahead_evasion(self):
        self.invulnerable_turns = 7  # Invulnerable for 7 turns
        
    def sat_multi_shot(self):
        missed_arrows = 0
        struck_arrows = 0
        no_damage_arrows = 0
        total_enemy_damage = 0
        invulnerable_opponents = filter(lambda opp: opp.invulnerable_turns, self.opponents)
        for arrow in range(17):
            enemy_index = randint(0, len(self.opponents))
            if enemy_index == len(self.opponents):
                missed_arrows += 1
            else:
                struck_arrows += 1
                # light attack damage + arrow index num
                if self.opponents[enemy_index] in invulnerable_opponents:
                    no_damage_arrows += 1
                else:
                    damage = randint(self.attack_power - 5, self.attack_power) + arrow
                    self.opponents[enemy_index].health -= damage
                    
                    total_enemy_damage += damage
        print(f"Of the 17 arrows shot, {missed_arrows} missed, and {struck_arrows} struck causing {total_enemy_damage} damage to the enemy team.")
        if no_damage_arrows: print(f"{no_damage_arrows} hit the opponents dark magic shield and did no damage.")
        
    def sat_odeons_crit_shot(self):
        opponent = self.target_opponent()
        if randint(1, 5) > 2:
            damage = self.attack_power * 3
            opponent.health -= damage
            if opponent.invulnerable_turns:
                opponent.invulnerable_turns = 0
                print(f"{opponent.name} {opponent.invulnerable_type} no more.")
                
            print(f"The scent of success burns the nostrils. {opponent.name} winces, taking {damage} damage.")
        else:
            print('You missed by a hair. A distant *thunk!* suggests the arrow embedded itself deep into something well beyond the wizard. You curse quitely.')
        
class Paladin(Character):
    def __init__(self, name):
        super().__init__(name, health=120, attack_power=30, action_points=8)
        
        self.set_attack_names("Psalm-a-dis", 'Religious Persecution')
        # ['are shielded', 'will evade', 'have a magic barrier', 'will counter-attack']
        self.invulnerable_type = self.invulnerable_type[2]  # have a magic barrier
        
        # special funcs will start with sab or sat, [s]pecial [ab]ility or [s]pecial [at]tack respectively
        self.specials['1'] = {
            'type': 'ability',
            'func': self.sab_mini_me,
            'args': [],
            'name': 'Mini-Me',
            'print_phrase': "exit your corporeal form and convince an amount of you to stay and fight by your side.",
            'description': "Keep a half-sized copy of yourself fighting you. Mini-Me, you complete me. They'll will attack right away."
        }
        self.specials['2'] = {
            'type': 'ability',
            'func': self.sab_righteous_favoritism,
            'args': [],
            'name': 'Righteous Favoritism',
            'print_phrase': 'pray, and something or someone listens. A shield of your faith galvanizes your aura. Er, for a little while.',
            'description': 'Shield yourself (and your astral projection if available) for 3 turns.'
        }
        self.specials['3'] = {
            'type': 'attack',
            'func': self.sat_holy_lancers,
            'args': [],
            'name': 'Holy Lancers',
            'print_phrase': 'call an angelic army of lancers to furious stampeed. Their silent hoove-falls in distinct juxtaposition to the clamour of their lances against the enemy.',
            'description': "Holy closers; tiny lancers. Summon a stampeed to strike each enemy at least twice."
        }
        self.specials['4'] = {
            'type': 'attack',
            'func': self.sat_holy_strike,
            'args': [],
            'name': 'Holy Strike',
            'print_phrase': "hold your sword aloft and its righteous aura sends a strike cutting towards the evil aura of the enemy.",
            'description': "Break enemy shield. Hit the enemy for sure. Do up to double damage."
        }
        
        #With a {verba[0]}, you {ability['desc']}. The evil wizard stands there {verba[1]}, almost in awe of such awesome power
        # Your corpse will be paraded around the kingdom, the {verba[2]} {verba[3]} which will instill inaction for the coming generations.\nThe evil wizard's reign will be unending. All hope {verba[4]}
        self.verba = ['prideful snear', 'disdainfully', 'face-less, armor-less, symbol-less mass of quartered body parts', 'piled into a shrine you would have never imagined', 'and faith lost forever.']

    def sab_mini_me(self):
        if len(self.team) > 1:
            del self.team[1]
            gc.collect()
        self.team += [SummonedEntity("Verne Troyer", self.attack_names['light'], self.attack_names['heavy'], health = 60, attack_power = 15)]
        self.team[1].invulnerable_type = self.invulnerable_type
        self.align_minions()
    
    def sab_righteous_favoritism(self):
        for member in self.team:
            member.invulnerable_turns = 3  # Shield for 3 turns
        
    def sat_holy_lancers(self):
        for opp in self.opponents:
            extra_hit = False
            hit = randint(self.attack_power - 5, self.attack_power + 10)
            damage = hit * 2
            # chance for 3 attacks
            if randint(1, 3) > 2:
                extra_hit = True
                damage += hit
            opp.health -= damage
            print(f"{opp.name} was hit {'thrice' if extra_hit else 'twice'}, receiving {damage} damage")
            
    def sat_holy_strike(self):
        for opp in self.opponents:
            if opp.invulnerable_turns:
                opp.invulnerable_turns = 0
                print(f"{opp.name}'s barrier shattered")
            opp.health -= self.attack_power * 2
            print(f"{opp.name} was hit twice receiving {self.attack_power * 2} damage")
    
class Traveler(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=20, action_points=20)
        
        self.all_attack_names = { 'light': ['Katana Slash'], 'heavy': ['Spinning Samurai Slice'] }
        self.set_attack_names('Katana Slash', 'Spinning Samurai Slice')
        self.invulnerable_type = 'deflected the attack with his blade'
        self.specials = {}
        self.inherit_all_specials()
        
        #With a {verba[0]}, you {ability['desc']}. The evil wizard stands there {verba[1]}, almost in awe of such awesome power
        # Your corpse will be paraded around the kingdom, the {verba[2]} {verba[3]} which will instill inaction for the coming generations.\nThe evil wizard's reign will be unending. All hope {verba[4]}
        self.verba = ['out hesitation', 'defiantly', 'people look away', 'and the children weep', 'as lost to time as the legendary Genndy Tartakovsky animation series.']
        
    def inherit_all_specials(self):
        other_classes = []
        for subclass in Character.__subclasses__():
            if subclass.__module__ != 'player_classes' or subclass.__name__ == self.__class__.__name__:
                continue
            else:
                other_classes += [subclass]
        count = 1

        for class_ in other_classes:
            instance = class_("Temp")
            self.all_attack_names['light'] += [instance.attack_names['light']]
            self.all_attack_names['heavy'] += [instance.attack_names['heavy']]
                
            for special in instance.specials.values():
                # Bind original func to this Traveler instance
                func_name = special['func'].__name__
                unbound_func = getattr(class_, func_name)
                
                bound_func = unbound_func.__get__(self, self.__class__)
                
                self.specials[str(count)] = {
                    'type': special['type'],
                    'func': bound_func,
                    'args': special['args'],
                    'name': special['name'],
                    'print_phrase': special['print_phrase'],
                    'description': special['description']
                }
                count += 1
    # override end_turn to randomize attack names -- will correctly show in menu and printed attack info
    def end_turn(self):
        self.set_attack_names(self.all_attack_names['light'][randint(0, len(self.all_attack_names['light']) - 1)], self.all_attack_names['heavy'][randint(0, len(self.all_attack_names['heavy']) - 1)])
        self.action_points += 1
        self.clear_dead()
        for character in self.team:
            self.decrement_status_turns(character)
        # no conditional due to Traveler being a player class
        self.toggle_turn()
        self.opponents[0].toggle_turn()
