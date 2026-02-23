import random
from unittest import case

from generator.mod import Mod
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

cadences = [3, 4, 5, 7]

def random_scale() -> Scale:
    """Generates a random scale."""
    scale_name = random.choice(list(SCALES.keys()))
    return Scale(root=Note(pitch=random.randint(40, 51)), scale_map=SCALES[scale_name])

def random_mod(scale, chromatic_chance: float=0.5) -> Mod:
    """Generates a random modifier for a chord."""
    mod = {}

    # If not chromatic, keep looping until the resulting interval is diatonic
    chromatic = random.random() < chromatic_chance

    while True:
        instruction = random.choice(["add", "no", "#", "b", "sus"])
        match instruction:
            case "add":
                interval = random.choice([6, 7, 9, 11, 13])
            case "sus":
                interval = random.choice([2, 4, 6])
            case _:
                interval = random.choice([1, 3, 5])

        c = Chord(scale, 1, modifiers=Mod({instruction: interval}))
        if c.is_diatonic() or chromatic:
            mod[instruction] = interval
            break
    
    return Mod(mod) if mod else None

def progression(scale, n: int=4) -> list[Chord]:
    """Generates a progression of chords."""
    
    progression = [Chord(scale, 1)]
    used_degrees = set([progression[-1].degree])
    for _ in range(n - 3): # Reserve the final two chords for a cadence
        degree = progression[-1].degree
        next_degrees = [d for d in progression_map[degree] if d not in used_degrees]
        if not next_degrees:
            next_degrees = list(progression_map[degree])
        next_degree = random.choice(next_degrees)
        used_degrees.add(next_degree)

        # Add a random modifier to the chord
        if random.random() < 1 and Chord(scale, next_degree).type != "unknown":  # 30% chance to add a modifier
            mod = random_mod(scale)
            print(mod)

        chord = Chord(scale, next_degree, modifiers=mod if 'mod' in locals() else None)
        progression.append(chord)

    # Add a cadence
    cadence_options = [c for c in cadences if c != progression[-1].degree]
    progression.append(Chord(scale, random.choice(cadence_options)))

    # Add a final chord
    progression.append(Chord(scale, 1))

    return progression

if __name__ == "__main__":
    scale = random_scale()
    prog = progression(scale, 8)

    print(scale, "\n")
    for chord in prog:
        print(chord)