from player_classes import Traveler, Warrior, Mage, Archer, Paladin
from npc_classes import EvilWizard, SummonedEntity
from intro import title_splash, intro_choice
from time import sleep
from rich.theme import Theme
from rich.console import Console

game = Theme({
    "prompt": "blink #bfc5be",
    "damage": "bold #ebcc0e",
    "traveler": "bold #8785B7",
    "warrior": "bold #FF6F61",
    "mage": "bold #6b5b93",
    "archer": "bold #88B04B",
    "paladin": "bold #F7CAC9",
    "evilwizard": "bold #BE4748",
    "summonedentity": "bold #FFFD81",
})





# 3 extra classes added
class_arr = ['Traveler', 'Warrior', 'Mage', 'Archer', 'Paladin']
console = Console(theme=game, style='#bfc5be on #2b2d31')
# Function to create player character based on user input
def create_character():
    console.clear()
    console.print("Tell me your character class:")
    class_choices = ''
    for i, char_class in enumerate(class_arr):
        if i == 0: continue # traveler is hidden
        class_choices += f'{i}.\t[{char_class.lower()}]{char_class}[/{char_class.lower()}]\n'
    console.print(class_choices)
    try:
        class_choice = int(console.input("[prompt]Enter the number of your class choice: [/prompt]"))
        console.print('\n\n\n')
    # CONDITIONAL REQUIRES ADJUSTMENT IF MORE CLASSES WERE ADDED
        if 1 <= class_choice < len(class_arr): # valid range, excluding Traveler
            class_name = class_arr[class_choice]
            chosen_class = globals()[class_name] # find class by name
            name_choice = console.input(f"[prompt]Enter your name {class_name}: [/prompt]")
            
            return chosen_class(name_choice) 
        else:
            raise ValueError
    except ValueError:
        # anything that causes a ValueError will return a mysterious traveler named Jack
        print("I'm uncertain what language that was. You must be The Traveler.\nI've heard tell your name is Jack.")
        return Traveler('Jack')
    sleep(1)
    console.clear()
    


# Battle function with user menu for actions
def battle(good_team, bad_team):
    separator = '\n---------------------------------------------------------------------------------------\n'
    player = good_team[0]
    wizard = bad_team[0]
    while wizard.health > 0 and player.health > 0:
        player.take_turn()
        sleep(1)
        
        console.print(f'{separator}')
        # Evil Wizard's turn to attack and regenerate
        if wizard.health > 0:
            wizard.take_turn()
            sleep(1)
            console.print(f'[danger]{separator}[/danger]')

        if player.health <= 0:
            print(f"{player.name} has been defeated!")
            death_of(player)
            sleep(2)
            prompt_restart(False)

        if wizard.health <= 0:
            print(f"")
            print(f"The wizard {wizard.name} has been defeated by {player.name}!")
            sleep(1)
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
    change_fate = console.input('[prompt]Would you like to try again? (y/n)[/prompt]')
    print('\n\n\n')
    if change_fate.lower() in ['y', 'yes']:
        print('\n\n\n\nVery Well')
        sleep(1)
        main()
    else:
        print('Farewell, Traveller.')
        sleep(2)
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