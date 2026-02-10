from typing import Literal

from generator.chord import Chord
from generator.note import Note

Instruction = Literal["add", "no", "#", "b", "sus"]
instructions = Instruction.__args__

class Mod:

    def __init__(self, mod: dict[Instruction, int]):

        if not all(key in instructions for key in mod.keys()):
            raise ValueError(f"Invalid modifier instruction. Valid instructions: {instructions}.")

        self.mod = mod

    def apply(self, chord: "Chord") -> None:
        """
        Applies the modifiers to the given chord.

        :param chord: The chord to which the modifiers are applied.
        :return: None
        """

        for instruction, interval in self.mod.items():
            if instruction == "add":
                chord.intervals[interval] = Note(pitch=chord.scale[interval])