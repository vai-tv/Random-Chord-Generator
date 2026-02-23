from typing import Literal

from generator.chord import Chord
from generator.note import Note
from generator.scale import SCALES

Instruction = Literal["add", "no", "#", "b", "sus", "ext"]
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
            raise ValueError(f"Cannot apply modifiers to unknown chord {chord}")

        for instruction, interval in self.mod.items():

            itv = chord.intervals[interval]

            if instruction == "add":
                octave, intv = divmod(interval - 1, len(SCALES[chord.type]))
                pitch = chord.root.pitch + SCALES[chord.type][intv] + 12 * octave
                chord.intervals[interval] = Note(pitch=pitch)

            elif instruction == "no":
                if interval in chord.intervals:
                    del chord.intervals[interval]

            elif instruction == "#":
                if interval in chord.intervals:
                    chord.intervals[interval] = Note(pitch=itv.pitch + 1)

            elif instruction == "b":
                if interval in chord.intervals:
                    chord.intervals[interval] = Note(pitch=itv.pitch - 1)

            elif instruction == "sus":
                # Remove 3rd and add target interval
                if 3 in chord.intervals:
                    del chord.intervals[3]
                pitch = chord.root.pitch + SCALES[chord.type][interval - 1]
                chord.intervals[interval] = Note(pitch=pitch)

            elif instruction == "ext":
                # Extend the chord by the target interval
                for degree in range(5, interval + 1, 2):
                    if degree not in chord.intervals:
                        pitch = chord.root.pitch + SCALES[chord.type][(degree - 1) % len(SCALES[chord.type])] + 12 * ((degree - 1) // len(SCALES[chord.type]))
                        chord.intervals[degree] = Note(pitch=pitch)
