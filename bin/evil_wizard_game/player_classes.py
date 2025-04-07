from character import *
from npcs import  SummonedEntity

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
            'args': [self],
            'name': 'Improvised Shield',
            'print_phrase': 'You grab the armor from the half-buried remains of two fallen heroes. With a grunt you pull them from the ground and hold them in front of you. A morbid detritus is flung in all directions',
            'description': 'Shield yourself for 2 turns'
        }
        self.specials['2'] = {
            'type': 'ability',
            'func': self.sab_gain_strength,
            'args': [self],
            'name': 'Gain Strength',
            'print_phrase': 'harness your adrenaline and will your muscles stronger. The wizard senses a shift in your prowess',
            'description': 'Add 10 points to your base attack power'
        }
        self.specials['3'] = {
            'type': 'attack',
            'func': self.sat_intimidate_reality,
            'args': [self],
            'name': 'Intimidate Reality',
            'print_phrase': 'cry at the heavens with a mighty roar. Your attack is mighty and unstoppable',
            'description': 'Opponent stripped of boon status (invincibility) and you hit will do double your base power in damage'
        }
        self.specials['4'] = {
            'type': 'attack',
            'func': self.sat_throw_something,
            'args': [self, '4'],
            'name': 'Throw something',
            'print_phrase': "grip something you saw out of the corner of your eye. ",
            'description': 'Throw something as hard as you can. It can do up do double damage.'
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
        opponent = target_opponent()
        opponent.invulnerable_turns = 0
        opponent.health -= 2 * self.attack_power
        
    def sat_throw_something(self, ability_num):
        power_range = (self.attack_power - 10, self.attack_power * 2 + 1)
        something = randint(*power_range)
        opponent = target_opponent()
        opponent.health -= something
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
        self.set_attack_names('Magic Pulse', 'White Lightning Bolt')
        # ['are shielded', 'will evade', 'have a magic barrier', 'will counter-attack']
        self.invulnerable_type = self.invulnerable_type[2]  # have a magic barrier
        
        # special funcs will start with sab or sat, [s]pecial [ab]ility or [s]pecial [at]tack respectively
        self.specials['1'] = {
            'type': 'ability',
            'func': self.sab_summon_animal_friend,
            'args': [self],
            'name': 'Summon Animal Friend',
            'print_phrase': f"blow a magic whistle and, per your previous agreement, an animal friend comes to your aid. You cast a magical shield on them lasting 1 turn.",
            'description': 'An animal joins your team and will fight to the death. Shielded for first turn.\nStackable: limit of 4. If all animals summoned: randomly increase health and power, remove statuses, and make invulnerable for 1 turn.'
        }
        self.specials['2'] = {
            'type': 'ability',
            'func': self.sab_minor_heal_all_spell,
            'args': [self],
            'name': 'Heal All Allies - Minor',
            'print_phrase': 'chant an incantation, and a soft glow envelops your entire team. Their wounds begin to close as the magic takes effect.',
            'description': 'Heal up to 1 wizard attack for each member of your team, including yourself.'
        }
        self.specials['3'] = {
            'type': 'attack',
            'func': self.sat_conjur_lightning_storm,
            'args': [self],
            'name': 'Conjure Lightning Storm',
            'print_phrase': 'cry at the heavens with a mighty roar. Your staff pointed above the enemy team, red sprites applify your attack, wherever it lands.',
            'description': "Conjure lightning storm, to paralyze and do up to double damage to a random opponent. It's as random as it is deadly."
        }
        self.specials['4'] = {
            'type': 'attack',
            'func': self.sat_fireball,
            'args': [self, '4'],
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
                    prev_stats = [self.team[i].max_health, self.team[i].attack_power]
                    del self.team[i] # delete instance, free memory space
                    gc.collect()
                    self.team[i] = SummonedEntity(*summoned_creature, health = randint(0, 40) + prev_stats[0], attack_power = randint(0, 15) + prev_stats[1])
                    self.team[i].invulnerable_turns = 1  
                    print(f"{summoned_creature[0]} is already summoned, it has been fully healed and purified and it is now stronger.")
        else:
            self.team += [SummonedEntity(*summoned_creature), health = randint(30, 40), attack_power = randint(10, 20)]  # Add a new summoned entity to the team
            self.team[-1].invulnerable_turns = 1  # New summoned entity is invulnerable for 1 turn
            
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
        self.opponents[randint(0, len(self.opponents) - 1)].paralyzed_turns = randint(1, 2)  # Paralyze a random opponent for 1 or 2 turns
        damage = randint(self.attack_power, self.attack_power * 2)
        
    def sat_fireball(self, ability_num):
        power = randint(self.attack_power - 10, self.attack_power * 2)
        teammate_possible_index = randint(1, 5)  # Randomly choose a teammate to possibly hit
        too_close = randint(0, 1)  # Randomly determine if the fireball hits a teammate (50% chance)
        if too_close and teammate_possible_index < len(self.team):
            teammate = self.team[teammate_possible_index]
            damage = randint(power // 2, power)
            teammate.health -= damage
            print(f"{teammate.name} is singed by the fireball and takes {damage} damage!")
        for opp in self.opponents:
            opp.health -= power
        print(f"Every enemy takes {power} damage from the explosion of the fireball!")


    # Add your cast spell method here

class Archer(Character):
    def __init__(self, name):
        super().__init__(name, health=120, attack_power=20, action_points=30)
        self.set_attack_names('Sonic Shot', 'Barbed Arrow')
        # ['are shielded', 'will evade', 'have a magic barrier', 'will counter-attack']
        self.invulnerable_type = self.invulnerable_type[1]  # will evade
        
        # special funcs will start with sab or sat, [s]pecial [ab]ility or [s]pecial [at]tack respectively
        self.specials['1'] = {
            'type': 'ability',
            'func': self.sab_install_turret,
            'args': [self],
            'name': 'Install Turret',
            'print_phrase': f"toss a device. Sprinting you step on the spring-loaded machine. A small inanimate turret pops-up points in the general direction of the enemies and begins to fire slowly.",
            'description': 'Install a small arrow turret, stackable, no limit.'
        }
        self.specials['2'] = {
            'type': 'ability',
            'func': self.sab_one_step_ahead_evasion,
            'args': [self],
            'name': 'One-Step-Ahead Evation',
            'print_phrase': 'find the flow of time and the universe, and see every attack coming. Each step towards victory will be one ahead of your enemies.',
            'description': 'Your enemies will be unable to strike you for 7 turns.'
        }
        self.specials['3'] = {
            'type': 'attack',
            'func': self.sat_multi_shot,
            'args': [self],
            'name': 'MultiShot',
            'print_phrase': 'grab a comical number of arrows, notched them, aimed towards the heavens. You release them and await gravity to align with your goals.',
            'description': "Shoot 17 arrows simultaneously, random damage to each enemy."
        }
        self.specials['4'] = {
            'type': 'attack',
            'func': self.sat_odeons_crit_shot,
            'args': [self],
            'name': "Odeon's Crit Shot",
            'print_phrase': "Your body aligns with you mind, your bow an extention of your will, points to your goal. You can't help but aim for that stupid face.",
            'description': "60 percent of the time it works every time, causing triple damage or none."
        }
        
        #With a {verba[0]}, you {ability['desc']}. The evil wizard stands there {verba[1]}, almost in awe of such awesome power
        # Your corpse will be paraded around the kingdom, the {verba[2]} {verba[3]} which will instill inaction for the coming generations.\nThe evil wizard's reign will be unending. All hope {verba[4]}
        self.verba = ['lack of wasted motion', 'trying to track the blur of movement', 'paralyze spell', 'seizing your dead muscles even now, ', 'but a dream of yesteryear']

    def sab_install_turret(self):
        if len(self.team) > 1:   
            self.team += [SummonEntity(f"turret{int(self.team[-1].name[-2:])}", 'Good Shot', 'Better Shot', health = 30, attack_power = 15)]
        else:
            self.team += [SummonEntity('turret01', 'Good Shot', 'Better Shot', health = 30, attack_power = 15)]
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
        total_enemy_damage = 0
        for arrow in range(17):
            enemy_index = randint(0, len(self.opponents))
            if enemy_index == len(self.opponents):
                missed_arrows += 1
            else:
                # light attack damage + arrow index num
                self.opponents[enemy_index].health -= randint(self.attack_power - 5, self.attack_power) + arrow
        print(f"Of the 17 arrows shot, {missed_arrows} missed, and {struck_arrows} struck causing {total_enemy_damage} damage to the enemy team.")
        
    def sat_odeons_crit_shot(self):
        opponent = self.target_opponent()
        if randint(1, 5) > 2:
            damage = self.attack_power * 3
            opponent.health -= damage
            print(f"The scent of success burns the nostrils. {opponent} winces, taking {damage} damage.")
        else:
            print('You missed by a hair. A distant *twwack!* suggests the arrow embedded itself deep into something well beyond the wizard. You curse quitely.')
        
class Paladin(Character):
    def __init__(self, name):
        super().__init__(name, health=120, attack_power=30, action_points=8) 
    
class Traveler(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=20, action_points=20)