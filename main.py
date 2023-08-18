from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Header, Footer, Label, Static, Button
from typing import List
from random import choice

class WinnerLabel(Static):
    """Shows the winner"""
    name = reactive("")

    def update_name(self, name: str):
        self.name = name

    def watch_name(self):
        self.update(self.name)

class FlashingArea(Static):
    """Should show the winner"""

    names = reactive([])

    def compose(self) -> ComposeResult:
        self.label = Label(f"{len(self.names)} people can win")
        yield self.label
        self.winner = WinnerLabel()
        self.winner.update_name("Who will win the most awesome of keyboards?")
        yield self.winner
        self.button = Button("Click Here", "primary")
        yield self.button

    def animate_to_colors(self, colors: List["str"]):
        duration = 0.3
        for idx, color in enumerate(colors):
            if idx < len(colors) - 1:
                self.styles.animate("background", color, duration=0.3, delay=idx * duration)
            else:
                self.styles.animate("background", color, duration=0.3, delay=idx * duration, on_complete=self.callback)



    def on_button_pressed(self):
        self.animate_to_colors(["blue", "green", "purple", "gray", "yellow"])

    def callback(self):
        self.winner.styles.color = "black"
        self.label.styles.color = "black"

        # Choose from names at random
        name = choice(self.names)
        self.winner.update_name(name)

class GiveAway(App):

    BINDINGS = [("q", "quit", "Quit the App")]
    TITLE = "Who will win?"
    SUB_TITLE = "Lets find out..."

    CSS = """
    Screen {
        align: center middle;
    }

    FlashingArea {
        background: $panel;
        border: tall yellow;
        padding: 8 30;
        width: auto;
    }

    WinnerLabel {
        margin-top: 1;
        text-align: center;
    }

    FlashingArea Button {
        text-style: bold;
        margin-top: 1;
    }

    """

    def compose(self) -> ComposeResult:
        yield Header()
        self.area = FlashingArea()
        with open("names.txt") as file:
            lines = [line.rstrip() for line in file]
        self.area.names = lines
        yield self.area
        yield Footer()



if __name__ == "__main__":

    app = GiveAway()
    app.run()

