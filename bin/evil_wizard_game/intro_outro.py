import time

# Hidari means left, whatever, B.C. was dr strange and sherlock, Trelawney looks ahead, Jay Ungar - see wizard walk song, and Meinertzhagen had a haversack(bag).
wizard_names = ['Hidari', 'Gelina Somez of Waverly Palace', 'Strangelock', 'Trelawney The Professed', 'Jay Ungar', 'Meinertzhagen']
actions = ['left', 'right', 'inspect', 'look', 'walk', 'bag' ]
print_actions = [
    '''
        \tYou turn left and see stars. When you open your eyes a gang is standing before you.
        They take you before the wizard and say \"Here is another worthy opponent.\"
        The wizard says, \"You are welcome, young traveler.
        Now prove yourself worthy\"...
    ''',
    '''
        \tYou turn right and see a beautiful garden. A mist settles and thickens.
        A woman forms from the mist and begs your help defeating an evil wizard.
        The moment you agree you stand in a pit near a twisted thrown. Atop it, the wizard stands.
        \"No one is allowed here!\" shrieks the wizard and the battle begins.
    ''',
    '''
        \tYou inspect the surroundings. Something feels off. You reach to touch a tree and your hand finds something cold and hard.
        The illusion dispells and the wizard's laugh fills the cavern.
        \"You have fallen into my trap. Now you die!\"
    ''',
    '''
        \tYou look ahead. A wizard is stirring a boiling pot. Your gaze meets theirs, and the wizard suddenly appears beside you.
        \"You will never leave this place,\" the wizards voice makes your hackles rize with its malice.
        The battle begins. 
    ''',
    '''
        \tYou take a step forward, but there is nothing firm to step upon. You flail in a pitfall before striking the ground some distance below you.
        After a moment you stand and look for an escape. You see no route, but a small crag in the wall is lit with a faint blue light.
        An awesome cubicula stretches to a dais. A vulture perched near the throne spreads its enormous wings and flies at you.
        Feet from you it morphs into a wizard. Their gaze is pure malice. You draw your weapon. The battle begins.
    ''',
    '''
        \tAs you open your bag and your hand grazes a mysterious talisman. A huge cloud of black smoke pours from the bag.
        The smoke falls as fast as it rose and coalesces into a fowl looking figure. A wizard stands before you.
        \"Holder of my prison, you will never send me back. NOW DIE!\" The wizards boisterous cocophany of a cry rocks the forest. The battle begins.
    '''
]

def intro_choice():
    print('You have traveled for days into a thick forest.\nYou stop out of sheer exhaustion and take stock\nWhat will you do next?\n')
    print('You can turn left, turn right, inspect surroundings, look ahead, walk ahead, or open bag.\n')
    print(f'These are the commands: {", ".join(actions)}')
    
    try:
        choice = input('Choose your action: ').lower()
        if choice in actions:
            print(print_actions[actions.index(choice)])
            return wizard_names[actions.index(choice)]
        else:
            raise ValueError
    except ValueError:
        print('Invalid input. Please try again.')
        time.sleep(2)
        intro_choice()