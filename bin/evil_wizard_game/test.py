

from time import sleep

from rich.console import Console
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
    "danger": "bold red"
})
console = Console(theme=custom_theme)
console.print("This is information", style="info")
console.print("[warning]The pod bay doors are locked[/warning]")
console.print("Something terrible happened!", style="danger")

from rich import print
print("[bold red]alert![/bold red] Something happened")
print("[bold italic yellow on red blink]This text is impossible to read")
print("[bold red]Bold and red[/] not bold or red")
print("[bold]Bold[italic][dim] bold and italic and dim[/dim] [/bold]italic[/italic]")
print(":red_heart-emoji:")
print(":red_heart-text:")

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

console.input("What is [i]your[/i] [bold red]name[/]? :smiley: ")

from rich.tree import Tree



tree = Tree("Rich Tree")
tree.add("foo")
tree.add("bar")
print(tree)
print(tree)
baz_tree = tree.add("baz")
baz_tree.add("[red]Red").add("[green]Green").add("[blue]Blue")
print(tree)





