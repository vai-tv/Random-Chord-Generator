from typing import Literal

from generator.chord import Chord
from generator.note import Note
from generator.scale import SCALES

Instruction = Literal["add", "no", "#", "b", "sus"]
instructions = Instruction.__args__

class Mod:

    def __init__(self, mod: dict[Instruction, int]):

        if not all(key in instructions for key in mod.keys()):
            raise ValueError(f"Invalid modifier instruction. Valid instructions: {instructions}.")

        self.mod = mod

    def __str__(self) -> str:
        s = ""
        for instruction, interval in self.mod.items():
            s += f"{instruction}{interval} "
        return s

    def apply(self, chord: "Chord") -> None:
        """
        Applies the modifiers to the given chord.

        :param chord: The chord to which the modifiers are applied.
        :return: None
        """

        if chord.type == "unknown":
            raise ValueError("Cannot apply modifiers to unknown chord type.")

        for instruction, interval in self.mod.items():
            if instruction == "add":
                # Get pitched interval
                pitch = chord.root.pitch + SCALES[chord.type][interval - 1]
                chord.intervals[interval] = Note(pitch=pitch)