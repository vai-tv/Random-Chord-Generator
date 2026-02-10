"""Chords use a triad-modifier system to generate chords.

The triad is defined by a root note and a scale. The modifiers transform the triad into a proper chord."""

from generator.note import Note

class Scale:

    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "augmented": [0, 2, 4, 5, 7, 9, 10],
        "diminished": [0, 2, 3, 5, 7, 8, 9]
    }

    def __init__(self, root: Note, scale_map: list[int]):

        assert max(scale_map) < 12, "Scale intervals must be less than 12 semitones"

        self.root = root
        self.scale_map = scale_map

    def __getitem__(self, degree: int) -> int:
        """Returns the interval in semitones for the given degree of the scale."""

        index = degree - 1  # Convert to 0-based index
        octave, degree_in_octave = divmod(index, len(self.scale_map))
        return self.scale_map[degree_in_octave] + 12 * octave + self.root.pitch

class Chord:
    
    def __init__(self, scale: Scale, degree: int=1, modifiers: "Mod" = None): # type: ignore

        self.degree = degree
        self.scale = scale
        self.modifiers = modifiers

        self.intervals = {
                degree : Note(pitch=self.scale[1] + scale[degree] % 12),  # Root
            2 + degree : Note(pitch=self.scale[3] + scale[degree] % 12),  # Third
            4 + degree : Note(pitch=self.scale[5] + scale[degree] % 12)   # Fifth
        }

        if self.modifiers:
            self.modifiers.apply(self)