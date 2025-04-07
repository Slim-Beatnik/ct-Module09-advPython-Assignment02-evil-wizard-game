from player_classes import *
from intro_outro import *
from time import sleep
# 3 extra classes added
class_arr = ['Traveler', 'Warrior', 'Mage', 'Archer', 'Paladin']

# Function to create player character based on user input
def create_character():

    print("Tell me your character class:")
    for i, char_class in enumerate(class_arr):
        if i == 0: continue
        print(f'{i}.\t{char_class}')
    
    try:
        class_choice = input("Enter the number of your class choice: ")
    # CONDITIONAL REQUIRES ADJUSTMENT IF MORE CLASSES WERE ADDED
        if int(class_choice) in range(1, len(class_arr)): # not len + 1 due to extra hidden class
            name = input("Enter your character's name: ")
            if class_choice == '1':
                return Warrior(name)
            elif class_choice == '2':
                return Mage(name)
            elif class_choice == '3':
                # Add Archer class here
                return Archer(name)
            elif class_choice == '4':
                # Add Paladin class here
                return Paladin(name)
            else:
                raise ValueError
    except ValueError:
        print("I'm uncertain what language that was. You must be The Traveler.\nI've heard tell your name is Jack.")
        return Traveler('Jack')
    
def specials_prompt(player):
    print("\n--- Specials Actions---")
    for i, special in enumerate(player.specials):
        print(f"{i+1}. {special['name']}\n{special['menu_desc']}")
        print()
    ability_num = input("Choose a special: ")
    if ability_num in player.specials:
        player.perform_special(ability_num)
    else:
        print(f"{player.name}, choose a valid special.")
        ans = input('Would you like to try again, or go back to the menu? (retry/menu):')
        print("ps, if you mess this up you'll be sent to the turn menu")
        if ans == 'retry':
            specials_prompt(player)
        else:
            turn_menu()


#display options based on player action points and special action cooldown
def turn_menu(player, wizard):
    while player.my_turn:
        available_options = [1, 6]
        print("\n--- Your Turn ---")
        print("1. Focus Energy")
        if player.action_points >=  1:
            available_options.append(2)
            print("2. Use Light Attack")
        elif player.action_points >=  2:
            available_options.append(3)
            print("3. Use Heavy Attack")
            if not player.cooldown:
                available_options.append(4)
                print("4. Use Specia)")
        elif player.action_points >= 3:
            available_options.append(5)
            print("5. Heal")
        print("6. View Stats")
    

    choice = input("Choose an action: ")
    #disable actions based on if they are part of the action menu
    if choice == '1':
        player.attack(player.light_attack(player.attack_name['light']), wizard)
    elif choice == '2' and choice in available_options:
        player.attack(player.heavy_attack(player.attack_name['heavy']), wizard)
    elif choice == '3' and choice in available_options:
        specials_prompt()
    elif choice == '4' and choice in available_options:
        player.heal()
        
    elif choice == '5':
        print(f'Player: ')
        player.display_stats()
        
        print('Enemy Team:')
        for opp in player.opponents:
            opp.display_stats()
        
        input('Press any key to return to the turn menu...')
        turn_menu(player, wizard) # displaying stats doesn't skip turn
    else:
        print(f"{player.name}, don't fail us. Choose from the available options.")
        turn_menu(player, wizard)
    time.sleep(2)
    player.toggle_turn()
    wizard.toggle_turn()

# Battle function with user menu for actions
def battle(player, wizard): 
    while wizard.health > 0 and player.health > 0:
        turn_menu()

        # Evil Wizard's turn to attack and regenerate
        if wizard.health > 0:
            wizard.regenerate()
            wizard.attack()

        if player.health <= 0:
            print(f"{player.name} has been defeated!")
            break

    if wizard.health <= 0:
        print(f"The wizard {wizard.name} has been defeated by {player.name}!")

# Main function to handle the flow of the game
def main():
    # original choice names wizard
    wizard_name = intro_choice()
    # Evil Wizard is created
    wizard = EvilWizard(f"{wizard_name}")
    
    # Character creation phase
    player = create_character()
    
    #set teams
    player.opponents = wizard.team
    wizard.opponents = player.team
    
    # Start the battle
    battle(player, wizard)

if __name__ == "__main__":
    main()
    

    
# mod2_project_starter_code.py

# Displaying mod2_project_starter_code.py.