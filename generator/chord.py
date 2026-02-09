from note import Note

class Scale:
    MAJOR = [0, 2, 4, 5, 7, 9, 11]
    MINOR = [0, 2, 3, 5, 7, 8, 10]
    AUGMENTED = [0, 2, 4, 5, 7, 9, 10]
    DIMINISHED = [0, 2, 3, 5, 7, 8, 9]

    def __init__(self, root: Note, scale_map: list[int]):

        assert max(scale_map) < 12, "Scale intervals must be less than 12 semitones"

        self.root = root
        self.scale_map = scale_map

    def interval(self, degree: int) -> int:
        """Returns the interval in semitones for the given degree of the scale."""

        index = degree - 1  # Convert to 0-based index
        octave, degree_in_octave = divmod(index, len(self.scale_map))
        return self.scale_map[degree_in_octave] + 12 * octave
    

s1 = Scale(Note(name="c4"), Scale.MAJOR)
print(s1.interval(1))  # Should print 0 (C4)