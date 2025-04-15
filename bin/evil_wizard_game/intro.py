import time
from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme
from rich.align import Align

# Hidari means left, obvious to those with children approaching 20 yo, B.C. was dr strange and sherlock, Trelawney looks ahead, Jay Ungar - see wizard walk song, and Meinertzhagen had a haversack(bag).
wizard_names = ['Hidari', 'Gelina Somez of Waverly Palace', 'Strangelock', 'Trelawney The Professed', 'Jay Ungar', 'Meinertzhagen']
actions = ['left', 'right', 'inspect', 'look', 'walk', 'bag' ]
print_actions = [
    '''
        \tYou turn left and see [blink damage]stars[/blink damage]. When you open your eyes a gang is standing before you.
        They take you before the wizard and say \"Here is another worthy opponent.\"
        The wizard says, \"You are welcome, young traveler.
        [danger]Now prove yourself worthy[/danger]\"[damage]...[/damage]
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

splash_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "bg": "#2b2d31",
    "danger": "bold #BE4748",
    "damage": "bold #ebcc0e"
})

with open("ew_logo.txt", "r", encoding="utf-8") as f:
    art = f.read()
        
art_width = len(art)
console = Console(theme=splash_theme, style='on #2b2d31')

def title_splash():
    
    colored_art = f"[#BE4748 on #2b2d31]{art}[/#BE4748 on #2b2d31]"
    centered_art = Align.center(Panel.fit(colored_art, subtitle="[frame bold damage]EVIL WIZARD GAME", border_style="damage"))

    console.print(centered_art)
    Align.center(input("\n[Press Enter to begin your journey...]"))

def intro_choice():
    console.print('You have traveled for days into a thick forest.\nYou stop out of sheer exhaustion and take stock\nWhat will you do next?\n')
    console.print('You can turn left, turn right, inspect surroundings, look ahead, walk ahead, or open bag.\n')
    console.print(f'These are the commands: {", ".join(actions)}')
    
    try:
        choice = input('Choose your action: ').lower()
        if choice in actions:
            console.print(print_actions[actions.index(choice)])
            return wizard_names[actions.index(choice)]
        else:
            raise ValueError
    except ValueError:
        console.print('Invalid input. Please try again.')
        time.sleep(1)
        return intro_choice()