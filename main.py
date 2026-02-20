import random

from generator.mod import Mod
from generator.chord import Chord
from generator.scale import Scale, SCALES
from generator.note import Note

def random_scale() -> Scale:
    """Generates a random scale."""
    scale_name = random.choice(list(SCALES.keys()))
    return Scale(root=Note(pitch=random.randint(40, 51)), scale_map=SCALES[scale_name])

def random_chord() -> Chord:
    """Generates a random chord."""
    scale = random_scale()
    degree = random.randint(1, 7)
    modifiers = None
    if random.random() < 0.5:
        modifiers = Mod(mod={"add": random.randint(2, 7)})
    return Chord(scale=scale, degree=degree, modifiers=modifiers)

if __name__ == "__main__":
    chord = random_chord()
    print(chord)
    chord.play(duration=2.0, stagger=0.05)