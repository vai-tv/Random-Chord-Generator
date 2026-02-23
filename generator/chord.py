"""Chords use a triad-modifier system to generate chords.

The triad is defined by a root note and a scale. The modifiers transform the triad into a proper chord."""

import json
import numpy as np

from generator.note import Note, volume_for_freq, TUNE
from generator.scale import Scale, SCALES

TRIADS: dict[str, list[int]] = json.load(open("triads.json"))
TRIAD_NAME_MAP = {tuple(sorted(intervals)) : name for name, intervals in TRIADS.items()}

class Chord:
    
    def __init__(self, scale: Scale, degree: int=1, modifiers: "Mod" = None): # type: ignore

        self.degree = degree
        self.scale = scale
        self.modifiers = modifiers

        self.root = Note(pitch=self.scale[degree])

        self.intervals = {
            1 : self.root,  # Root
            3 : Note(pitch=self.scale[2 + degree]),  # Third
            5 : Note(pitch=self.scale[4 + degree])   # Fifth
        }

        self.type = self.get_type()

        if self.modifiers:
            self.modifiers.apply(self)

    def __str__(self) -> str:
        
        s = f"{self.root.name[:-1].capitalize()}{self.type[:3]} "
        # add mods
        if self.modifiers:
            s += f"{self.modifiers}\t"

        for degree, note in self.intervals.items():
            s += f"{degree}: {note.name.capitalize()}\t"
        return s
    
    def normalise(self, limit: int=12) -> None:
        """Change octaves of all the notes to fit within {limit} semitones of the root note."""

        for degree, note in self.intervals.items():
            while note.pitch - self.root.pitch > limit:
                note.pitch -= 12
            while note.pitch - self.root.pitch < 0:
                note.pitch += 12
            note.name = note.pitch_to_name(note.pitch)

    def get_type(self) -> str:
        """Get the type of the chord based on the pitches."""

        pitches = [note.pitch for note in self.intervals.values()]
        intervals = tuple(sorted((pitch - self.root.pitch) % 12 for pitch in pitches))
        return TRIAD_NAME_MAP.get(intervals, "unknown")
    
    def play(self, duration: float=1.0, stagger: float=0.0) -> None:
        """Plays the chord for the given duration in seconds."""

        import sounddevice as sd

        frequencies = [TUNE * 2 ** ((note.pitch + 12 - 69) / 12) for note in self.intervals.values()]
        volumes = [volume_for_freq(freq) / (len(frequencies) ** 2) for freq in frequencies]

        # Generate the audio signal for each note
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio = np.zeros_like(t, dtype=np.float32)

        for i, (freq, vol) in enumerate(zip(frequencies, volumes)):
            start = i * stagger
            end = start + duration
            mask = (start <= t) & (t < end)
            audio[mask] += vol * np.sin(2 * np.pi * freq * t[mask])

        # Normalize the audio signal
        audio = (audio / np.max(np.abs(audio))) * 32767
        audio = audio.astype(np.int16)

        # Play the audio signal
        sd.play(audio, sample_rate)
        sd.wait()
