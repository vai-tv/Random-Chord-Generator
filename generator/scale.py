from generator.note import Note
import json

SCALES: dict[str, list[int]] = json.load(open("scales.json"))

class Scale:

    def __init__(self, root: Note, name: str, map: list[int]):

        assert max(map) < 12, "Scale intervals must be less than 12 semitones"

        self.root = root
        self.name = name
        self.map = map

    def __getitem__(self, degree: int) -> int:
        """Returns the interval in semitones for the given degree of the scale."""

        index = degree - 1  # Convert to 0-based index
        octave, degree_in_octave = divmod(index, len(self.map))
        return self.map[degree_in_octave] + 12 * octave + self.root.pitch
    
    def __str__(self) -> str:
        return f"{self.root.name[:-1].capitalize()} {self.name.replace('_', ' ').capitalize()} Scale"