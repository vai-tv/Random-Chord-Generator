from generator.note import Note
import json

SCALES: dict[str, list[int]] = json.load(open("scales.json"))

class Scale:

    def __init__(self, root: Note, scale_map: list[int]):

        assert max(scale_map) < 12, "Scale intervals must be less than 12 semitones"

        self.root = root
        self.scale_map = scale_map

    def __getitem__(self, degree: int) -> int:
        """Returns the interval in semitones for the given degree of the scale."""

        index = degree - 1  # Convert to 0-based index
        octave, degree_in_octave = divmod(index, len(self.scale_map))
        return self.scale_map[degree_in_octave] + 12 * octave + self.root.pitch
    
    def __str__(self) -> str:
        return f"Scale(root={self.root}, scale_map={self.scale_map})"