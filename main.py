import random

from generator.mod import Mod, instructions
from generator.chord import Chord
from generator.scale import Scale, SCALES
from generator.note import Note

progression_map = {
    1 : [2, 3, 4, 5, 6, 7],
    2 : [1, 3, 4, 5, 6, 7],
    3 : [1, 2, 4, 5, 6, 7],
    4 : [1, 5],
    5 : [1, 2],
    6 : [1, 2, 3, 4, 5, 7],
    7 : [1, 2, 3, 4, 5, 6]
}

allowed_mod_intervals = {
    "add" : [6, 9, 11, 13],
    "sus" : [2, 4, 6],
    "ext" : [7, 9, 11, 13]
}

def random_scale() -> Scale:
    """Generates a random scale."""
    scale_name = random.choice(list(SCALES.keys()))
    return Scale(root=Note(pitch=random.randint(32, 47)), name=scale_name, map=SCALES[scale_name])

def random_mod(scale, chromatic_chance: float=0.5) -> Mod:
    """Generates a random modifier for a chord."""
    mod = {}

    # If not chromatic, keep looping until the resulting interval is diatonic
    chromatic = random.random() < chromatic_chance

    while True:
        instruction = random.choice(instructions)

        allowed_intervals = allowed_mod_intervals.get(instruction, [1, 3, 5])
        interval = random.choice(allowed_intervals)

        c = Chord(scale, 1, modifiers=Mod({instruction: interval}))

        # Break the loop if the resulting chord is diatonic or if chromatic modifications are allowed
        if c.is_diatonic() or chromatic:
            mod[instruction] = interval
            break
    
    return Mod(mod) if mod else None

def progression(scale, n: int=4, mod_chance: float=0.4, chromatic_chance: float=0.5, degree_offset: int=0) -> list[Chord]:
    """Generates a progression of chords."""
    
    progression = [Chord(scale, 1 + degree_offset)]
    used_degrees = set([progression[-1].degree])

    for _ in range(n - 3): # Reserve the final two chords for a cadence
        degree = (progression[-1].degree - 1) % 7 + 1
        next_degrees = [d for d in progression_map[degree] if d not in used_degrees]
        if not next_degrees:
            next_degrees = list(progression_map[degree])
        next_degree = random.choice(next_degrees)
        used_degrees.add(next_degree)

        # Add a random modifier to the chord
        if random.random() < mod_chance and Chord(scale, next_degree).type != "unknown":
            mod = random_mod(scale, chromatic_chance=chromatic_chance)

        chord = Chord(scale, next_degree, modifiers=mod if 'mod' in locals() else None)
        progression.append(chord)

    # Add a cadence
    cadence_options = [c for c in [3, 4, 5, 7] if c != progression[-1].degree - degree_offset]
    progression.append(Chord(scale, random.choice(cadence_options) + degree_offset))

    # Add a final chord
    progression.append(Chord(scale, 1 + degree_offset))

    return progression

if __name__ == "__main__":
    scale = random_scale()
    while True:
        try:
            prog = progression(scale, 8, mod_chance=0.25, chromatic_chance=0.75, degree_offset=0)
            break
        except Exception as e:
            print(f"Error generating progression: {e}")

    print(scale, "\n")
    for chord in prog:
        print(chord)