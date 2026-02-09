import sounddevice as sd
import numpy as np

PITCHMAP = {
    "c": 0,
    "c#": 1,
    "db": 1,
    "d": 2,
    "d#": 3,
    "eb": 3,
    "e": 4,
    "f": 5,
    "f#": 6,
    "gb": 6,
    "g": 7,
    "g#": 8,
    "ab": 8,
    "a": 9,
    "a#": 10,
    "bb": 10,
    "b": 11
}

TUNE = 440  # A4 = 440 Hz

def volume_for_freq(freq, base_volume=0.4):
    # reduce volume as pitch increases
    print(f"Volume for frequency {freq} Hz: {base_volume * 100 / (freq ** 1.5)}")
    return 300 / (freq + 200)

class Note:

    def __init__(self, pitch: int | None=None, name: str | None=None, interval: int | None=None):

        if pitch is None:
            if name is None:
                raise ValueError("Either pitch or name must be provided")
            self.name = name
            self.pitch = self.name_to_pitch(name)
        elif name is None:
            self.name = self.pitch_to_name(pitch)
            self.pitch = pitch
        else:
            raise ValueError("Both pitch and name cannot be provided")
        
    def __str__(self) -> str:
        return f"Note({self.name.capitalize()} {self.pitch})"

    def name_to_pitch(self, name: str) -> int:
        if len(name) == 1:
            note = name.lower()
            octave = 1
        elif len(name) == 2:
            if name[1].isdigit():
                note = name[0].lower()
                octave = int(name[1]) + 1
            else:
                note = name.lower()
                octave = 1
        elif len(name) == 3:
            if name[2].isdigit():
                note = name[:2].lower()
                octave = int(name[2]) + 1
            else:
                raise ValueError(f"Invalid note name: {name}")
        else:
            raise ValueError(f"Invalid note name: {name}")
        if note not in PITCHMAP:
            raise ValueError(f"Invalid note name: {name}")
        return PITCHMAP[note] + 12 * octave
    
    def pitch_to_name(self, pitch: int) -> str:

        octave, note = divmod(pitch, 12)

        for key, value in PITCHMAP.items():
            if value == note:
                return key + str(octave - 1)

        raise ValueError(f"Invalid pitch: {pitch}")

    def play(self, duration: float = 1.0, sample_rate: int = 44100):
        """
        Plays the note for the given duration and sample rate.

        :param duration: The duration of the note in seconds.
        :param sample_rate: The sample rate of the audio in Hz.
        """

        frequency = TUNE * 2 ** ((self.pitch + 12 - 69) / 12) # Pitch needs to adjust one octave
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        note = volume_for_freq(frequency) * np.sin(frequency * t * 2 * np.pi)

        sd.play(note, sample_rate)
        status = sd.wait()

if __name__ == "__main__":
    print("Testing name init:")
    n1 = Note(name="c4")
    n2 = Note(name="g#")
    n3 = Note(name="g4")
    n4 = Note(name="d")
    print(n1)
    print(n2)
    print(n3)
    print(n4)

    print("\nTesting pitch init:")
    n1 = Note(pitch=60)
    print(n1)

    n1.play(1.0)

    print("\nTesting play:")
    
    scale = [0, 2, 4, 5, 7, 9, 11, 12, 11, 9, 7, 5, 4, 2, 0]  # Major scale intervals
    root_pitch = 60  # C4


    for s in scale:
        note = Note(pitch=root_pitch + s)
        print(f"Playing {note}")
        note.play(0.5)
