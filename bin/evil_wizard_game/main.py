from player_classes import *
from npc_classes import *
from intro import *
from time import sleep
from rich.theme import Theme
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red",
    "damage": "bold #ebcc0e"
})
# 3 extra classes added
class_arr = ['Traveler', 'Warrior', 'Mage', 'Archer', 'Paladin']

# Function to create player character based on user input
def create_character():

    print("Tell me your character class:")
    for i, char_class in enumerate(class_arr):
        if i == 0: continue # traveler is hidden
        print(f'{i}.\t{char_class}')
    
    try:
        class_choice = int(input("Enter the number of your class choice: "))
        print('\n\n\n')
    # CONDITIONAL REQUIRES ADJUSTMENT IF MORE CLASSES WERE ADDED
        if 1 <= class_choice < len(class_arr): # valid range, excluding Traveler
            class_name = class_arr[class_choice]
            chosen_class = globals()[class_name]
            name_choice = input(f"Enter your name {class_name}: ")
            print('\n\n\n')
            return chosen_class(name_choice)
        else:
            raise ValueError
    except ValueError:
        print("I'm uncertain what language that was. You must be The Traveler.\nI've heard tell your name is Jack.")
        return Traveler('Jack')
    


# Battle function with user menu for actions
def battle(good_team, bad_team):
    separator = '\n---------------------------------------------------------------------------------------\n'
    player = good_team[0]
    wizard = bad_team[0]
    while wizard.health > 0 and player.health > 0:
        player.take_turn()
        
        print(separator)
        # Evil Wizard's turn to attack and regenerate
        if wizard.health > 0:
            wizard.take_turn()
            print(separator)

        if player.health <= 0:
            print(f"{player.name} has been defeated!")
            death_of(player)
            time.sleep(2)
            prompt_restart(False)

        if wizard.health <= 0:
            print(f"")
            print(f"The wizard {wizard.name} has been defeated by {player.name}!")
            time.sleep(1)
            prompt_restart(True)
        
def death_of(who_died):
    print(f"\n\n\nYour corpse will be paraded around the kingdom, the {who_died.verba[2]} {who_died.verba[3]} which will instill inaction for the coming generations.\nThe evil wizard's reign will be unending. All hope {who_died.verba[4]}")
    if who_died.__class__ == 'Traveler': print(f"I am {who_died}'s {['wasted life', 'inflamed sense of rejection', 'broken heart', 'complete lack of surprise', 'raging bile duct', 'cold sweat', 'overwhelming sense of inadequacy'][randint(0, 6)]}.")
    print(f"\nWell, {who_died.name}... pfft, {type(who_died).__name__} indeed...")

        
def prompt_restart(win_bool):
    if win_bool:
        print('Masterful job, traveller!')
    else:
        print('*Deep Sigh* I can resurrect you.')
    change_fate = input('Would you like to try again? (y/n)')
    print('\n\n\n')
    if change_fate.lower() in ['y', 'yes']:
        print('\n\n\n\nVery Well')
        time.sleep(1)
        main()
    else:
        print('Farewell, Traveller.')
        time.sleep(2)
        quit()

# Main function to handle the flow of the game
def main():
    title_splash()
    
    # original choice names wizard
    wizard_name = intro_choice() # intro_choice ValueError will still return wizard_name
    # Evil Wizard is created
    wizard = EvilWizard(f"{wizard_name}")
    wizard.team = [wizard]
    # Character creation phase
    player = create_character()
    player.team = [player]
    #set teams
    player.opponents = wizard.team
    wizard.opponents = player.team
    
    battle(player.team, wizard.team)

if __name__ == "__main__":
    main()
    

    
# mod2_project_starter_code.py

# Displaying mod2_project_starter_code.py.