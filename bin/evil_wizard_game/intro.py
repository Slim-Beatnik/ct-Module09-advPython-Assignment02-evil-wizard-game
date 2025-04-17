import time
from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme
from rich.align import Align
from rich.live import Live


splash_theme = Theme({
    "text": "#bfc5be",
    "bg": "#2b2d31",
    "danger": "#BE4748",
    "damage": "#ebcc0e",
    "left": "#aceeee",
    "right": "#eeacee",
    "inspect": "#eeeeac",
    "look": "#8bbf89",
    "walk": "#f033f0",
    "bag": "#f0f033",
})
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



with open("ew_logo.txt", "r", encoding="utf-8") as f:
    art = f.read()
        
art_width = len(art)
console = Console(theme=splash_theme, style='on #2b2d31')

def title_splash_animated(file_path="ew_logo.txt", delay=0.01):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    output = ""
    with Live(refresh_per_second=60) as live:
        for line in lines:
            output += line
            panel = Panel.fit(
                f"[#BE4748 on #2b2d31]{output}[/#BE4748 on #2b2d31]",
                title="EVIL WIZARD GAME",
                subtitle="Let the battle begin!",
                border_style="#ebcc0e"
            )
            live.update(Align.center(panel))
            time.sleep(delay)

def title_splash():
    console.clear()
    title_splash_animated()
    console.input("\n[blink #aceeee]Press Enter to begin your journey...[/blink #aceeee]")
    console.theme='[on blink #ebcc0e]'
    time.sleep(1)

def intro_choice():
    console.clear()
    console.print('You have traveled for days into a thick forest.\nYou stop out of sheer exhaustion and take stock\nWhat will you do next?\n')
    console.print('You can turn left, turn right, inspect surroundings, look ahead, walk ahead, or open bag.\n')
    # join map with action, wrapped in rich formatting - themes match verbs
    console.print(f'These are the commands: { ", ".join(map(lambda verb: f'[{verb}]{verb}[/{verb}]', actions)) }')
    
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