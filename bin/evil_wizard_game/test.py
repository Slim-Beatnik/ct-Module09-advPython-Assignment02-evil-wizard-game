

from time import sleep

from rich.console import Console, Group, ConsoleOptions, RenderResult
from rich.align import Align
from rich.text import Text
from rich.panel import Panel

console = Console()

with console.screen(style="bold white on red") as screen:
    for count in range(1, 0, -1):
        text = Align.center(
            Text.from_markup(f"[blink]Don't Panic![/blink]\n{count}", justify="center"),
            vertical="middle",
        )
        screen.update(Panel(text))
        sleep(1)
        
console.print("Danger, Will Robinson!", style="blink bold red underline on white")

from rich.theme import Theme
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red",
    "damage": "bold #ebcc0e"
})
console = Console(theme=custom_theme)
console.print("This is information", style="info")
console.print("[warning]The pod bay doors are locked[/warning]")
console.print("Something terrible happened!", style="danger")
console.print('You took [damage]25[/damage] points of damage!')

from rich import print
console.print("[bold red]alert![/bold red] Something happened")
console.print("[bold italic yellow on red blink]This text is impossible to read")
console.print("[bold red]Bold and red[/] not bold or red")
console.print("[bold]Bold[italic][dim] bold and italic and dim[/dim] [/bold]italic[/italic]")
console.print(":red_heart-emoji:")
console.print(":red_heart-text:")

MARKDOWN = """
# Welcome to the Evil Wizard Game

Rich can do a pretty *decent* job of rendering markdown.

1. This is a list item
2. This is another list item
"""

from rich.markdown import Markdown

console = Console()
md = Markdown(MARKDOWN)
console.print(md)

#console.input("What is [i]your[/i] [bold red]name[/]? :smiley: ")

from rich.tree import Tree



tree = Tree("Rich Tree")
tree.add("foo")
tree.add("bar")
console.print(tree)
console.print(tree)
baz_tree = tree.add("baz")
baz_tree.add("[red]Red").add("[green]Green").add("[blue]Blue")
console.print(tree)


console.print('different thing------------------------------------------------------')

from dataclasses import dataclass
from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table
from rich.padding import Padding

from rich.segment import *

@dataclass
class Student:
    id: int
    name: str
    age: int
    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield f"[b]Student:[/b] #{self.id}"
        my_table = Table("[green]Attribute[/green]", "[dark-cyan]Value[/dark-cyan]" )
        my_table.add_row("[green]name[/green]", f"[dark-cyan]{self.name}[/dark-cyan]")
        my_table.add_row("[green]age[/green]", f"[dark-cyan]{str(self.age)}[/dark-cyan]")
        yield my_table
        
stud = Student(4,'jeff', 40)
console.print(stud)
class MyObject:
    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield Segment("My", Style(color="magenta"))
        yield Segment("Object", Style(color="green"))
        yield Segment("()", Style(color="cyan"))
        
panel_group = Group(
    Panel("Hello", style="on blue"),
    Panel("World", style="on red"),
)
console.clear()
console.print(Panel(panel_group))
        
obj = MyObject()
console.print(obj)

import os
import sys

# Change CMD code page to CP437
os.system('chcp 437 > NUL')
os.system("mode con: cols=120 lines=40")

# Set Python's stdout encoding to CP437
sys.stdout.reconfigure(encoding='cp437')
from itertools import *
# Initialize rich console with NO wrapping
from math import *
fs = open('ew_logo.txt', 'r')
code = fs.readlines()
# Read ASCII art and print
f = open("ew_logo.txt", "r", encoding="cp437")
cp437_art = f.readlines()
#art_width = len(ascii_art[1])
#console = Console(height=len(ascii_art), width=600, style='#2b2d31 on #BE4748')
chars = '█  ▓▓▓▓▓▓▓▓▒░'
# art_chars = {}
# for byte in cp437_art:
#     print(line)
#     for ch in line:
#         print(bin(ch))
#         art_chars[ord(ch)] = 0
# print(ord('█'), chr(9608), '\n', art_chars)
# for ch in art_chars.keys():
#     console.print(chr(ch))
# all_char_lines = []

# for byte in cp437_art:
#     cp437_code_point = ord(bytes([byte]))
#     print(f"Byte: {byte}, CP437 Code Point: {cp437_code_point}")
ords = {}
for line in cp437_art:
    for ch in line:
        ords[ch.encode('cp437')[0]] = 0
print(ords)
# for line in cp437_art:
#     for i, char in enumerate(line):
#         if all(reduce(lambda a,c: a + c, art_chars.keys()) in line[i]):
#             all_char_lines.append(i)
#         art_chars[ord(char)] = char
        

# print('art_chars: ',art_chars)
sys.stdout.reconfigure(encoding='utf-8')
# g = open('ew_logo_utf8.txt', 'w+', encoding='utf-8')
# for line in cp437_art:
#     g.write(line)

# for line in ascii_art:
#     console.print(Padding(line, (0, (console.width - art_width // 2 - 1),0,(console.width - art_width // 2 - 1))), justify='center', end='')
# console.print()
# console.print( Markdown('# The Dark Wizard'), justify='center', style='bold', width=console.width-12)

# console.print('')
# console.print(ascii_art[0],'\n')

# sys.stdout.reconfigure(encoding='utf-8')

# console.print(Padding("██", (0,1,0,1), style="#2b2d31 on blue"), justify='center')
# print('██')

chars = '█  ▓▓▓▓▓▓▓▓▒░'
chars = list(map(lambda c: ((ord(c)%255 -6), chr(ord(c)%255 -6)), set(list(chars))))
chars = list(filter(lambda ch: ch[0] > 32, chars))
print(ord('█'), chr(9608), '\n', list(chars))
