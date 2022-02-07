import pygame
import simpleaudio as sa
import numpy as np
import sounddevice as sd
import time

class Waveform:
    def __init__(self, frequency, amplitude, sample_rate, duration, style, letter):
        """
        Description: Creates an instance of the Waveform class, with some instance variables that were passed as parameters. Also includes dictionaries so frequency values can be assigned to notes.
        Parameter: frequency, amplitude, sample_rate, duration, style, letter
        Returns: none
        """
        pygame.sprite.Sprite.__init__(self)
        self.frequency = frequency
        self.amplitude = amplitude
        self.sample_rate = sample_rate
        self.duration = duration
        self.style = style
        self.letter = letter
        # dictionary for each note's arpeggio
        self.arpeggiation_dict = {  "C": ("C", "E", "G", "B"), "C_SHARP": ("C_SHARP", "F", "G_SHARP", "C2"),
                                    "D": ("D", "F_SHARP", "A", "C_SHARP2"), "D_SHARP": ("D_SHARP", "G", "A_SHARP", "D2"),
                                    "E": ("E", "G_SHARP", "B", "D_SHARP2"), "F": ("F", "A", "C2", "E2"),
                                    "F_SHARP": ("F_SHARP", "A_SHARP", "C_SHARP2", "F2"), "G": ("G", "B", "D2", "F_SHARP2"),
                                    "G_SHARP": ("G_SHARP", "C2", "D_SHARP2", "G2"), "A": ("A", "C_SHARP2", "E2", "G_SHARP2"),
                                    "A_SHARP": ("A_SHARP", "D2", "F2", "A2"), "B": ("B", "D_SHARP2", "F_SHARP2", "A_SHARP2"),
                                    "C2": ("C2", "E2", "G2", "B2"),
                                }
        # dictionary for each note's frequency
        self.frequency_dict = { "C" : 261.6256, "C_SHARP" : 277.1826, "D" : 293.6648, "D_SHARP" : 311.1270,
                                "E" : 329.6276, "F" : 349.2282, "F_SHARP" : 369.9944, "G" : 391.9954,
                                "G_SHARP" : 415.3047, "A" : 440.0, "A_SHARP" : 466.1638, "B" : 493.8833,
                                "C2" : 523.2511, "C_SHARP2" : 554.3653, "D2" : 587.3295, "D_SHARP2" : 622.2540,
                                "E2" : 659.2551, "F2" : 698.4565, "F_SHARP2" : 739.9888, "G2" : 783.9909,
                                "G_SHARP2" : 830.6094, "A2" : 880.0000, "A_SHARP2" : 932.3275, "B2" : 987.7666
                            }

    def generateArray(self):
        """
        Description: Math behind sound waves, it generates an array of evenly spaced numbers ranging from 0 to the
                     duration of each note. This is used to generate the waveforms used to play audio waves.
        Parameter: none
        Returns: none
        """
        self.sample_array = np.linspace(0.0, self.duration, int(self.duration * self.sample_rate), endpoint=False)

    def playSound(self):
        """
        Description: Generates a sound wave using the simpleaudio library
        Parameter: none
        Returns: none
        """
        # Ensures the highest note is in 16-bit range
        self.sound = self.waveform * (2 ** 15 - 1) / np.max(np.abs(self.waveform))
        # Converts to 16-bit data
        self.sound = self.sound.astype(np.int16)
        # Starts playback
        self.play_object = sa.play_buffer(self.sound, 1, 2, self.sample_rate)
        # Wait to finish before stopping
        self.play_object.wait_done()

    def playMono(self):
        """
        Description: Generates a mono sound wave using the sounddevice library. Uses time to determine the length of the sound.
        Parameter: none
        Returns: none
        """
        sd.play(self.waveform)
        # sleeps the program so the sound can play
        time.sleep(.2)
        # wakes the program, subsequently stopping the sound
        sd.stop()

    def playSineWave(self):
        """
        Description: Stores all info on the Sine wave preset, will be called when keys are pressed. Holds all math necessary for mono notes and arpeggios.
        Parameter: none
        Returns: none
        """
        self.generateArray()
        # uses sounddevice to play Mono notes
        if self.style == "Mono":
            self.waveform = self.amplitude * np.sin(self.frequency * self.sample_array * 2 * np.pi)
            self.playMono()
        # uses simpleaudio to play arpeggios
        elif self.style == "Duo":
            self.frequency_1, self.frequency_2 = self.getFrequencies()
            self.note_1 = self.amplitude * np.sin(self.frequency_1 * self.sample_array * 2 * np.pi)
            self.note_2 = self.amplitude * np.sin(self.frequency_2 * self.sample_array * 2 * np.pi)
            self.waveform = np.hstack((self.note_1, self.note_2))
            self.playSound()
        # triad arpeggio
        elif self.style == "Trio":
            self.frequency_1, self.frequency_2, self.frequency_3 = self.getFrequencies()
            self.note_1 = self.amplitude * np.sin(self.frequency_1 * self.sample_array * 2 * np.pi)
            self.note_2 = self.amplitude * np.sin(self.frequency_2 * self.sample_array * 2 * np.pi)
            self.note_3 = self.amplitude * np.sin(self.frequency_3 * self.sample_array * 2 * np.pi)
            self.waveform = np.hstack((self.note_1, self.note_2, self.note_3))
            self.playSound()
        # major 7th arpeggio
        elif self.style == "Quattro":
            self.frequency_1, self.frequency_2, self.frequency_3, self.frequency_4 = self.getFrequencies()
            self.note_1 = self.amplitude * np.sin(self.frequency_1 * self.sample_array * 2 * np.pi)
            self.note_2 = self.amplitude * np.sin(self.frequency_2 * self.sample_array * 2 * np.pi)
            self.note_3 = self.amplitude * np.sin(self.frequency_3 * self.sample_array * 2 * np.pi)
            self.note_4 = self.amplitude * np.sin(self.frequency_4 * self.sample_array * 2 * np.pi)
            self.waveform = np.hstack((self.note_1, self.note_2, self.note_3, self.note_4))
            self.playSound()

    def playSquareWave(self):
        """
        Description: Stores all info on the Square wave preset, will be called when keys are pressed. Holds all math necessary for mono notes and arpeggios.
        Parameter: none
        Returns: none
        """
        self.generateArray()
        # uses sounddevice to play Mono notes
        if self.style == "Mono":
            self.waveform = self.amplitude * np.sign(np.sin(self.frequency * self.sample_array * 2 * np.pi))
            self.playMono()
        # uses simpleaudio to play arpeggios
        elif self.style == "Duo":
            self.frequency_1, self.frequency_2 = self.getFrequencies()
            self.note_1 = np.sign(np.sin(self.frequency_1 * self.sample_array * 2 * np.pi))
            self.note_2 = np.sign(np.sin(self.frequency_2 * self.sample_array * 2 * np.pi))
            self.waveform = np.hstack((self.note_1, self.note_2))
            self.playSound()
        # triad arpeggio
        elif self.style == "Trio":
            self.frequency_1, self.frequency_2, self.frequency_3 = self.getFrequencies()
            self.note_1 = np.sign(np.sin(self.frequency_1 * self.sample_array * 2 * np.pi))
            self.note_2 = np.sign(np.sin(self.frequency_2 * self.sample_array * 2 * np.pi))
            self.note_3 = np.sign(np.sin(self.frequency_3 * self.sample_array * 2 * np.pi))
            self.waveform = np.hstack((self.note_1, self.note_2, self.note_3))
            self.playSound()
        # major 7th arpeggio
        elif self.style == "Quattro":
            self.frequency_1, self.frequency_2, self.frequency_3, self.frequency_4 = self.getFrequencies()
            self.note_1 = np.sign(np.sin(self.frequency_1 * self.sample_array * 2 * np.pi))
            self.note_2 = np.sign(np.sin(self.frequency_2 * self.sample_array * 2 * np.pi))
            self.note_3 = np.sign(np.sin(self.frequency_3 * self.sample_array * 2 * np.pi))
            self.note_4 = np.sign(np.sin(self.frequency_4 * self.sample_array * 2 * np.pi))
            self.waveform = np.hstack((self.note_1, self.note_2, self.note_3, self.note_4))
            self.playSound()

    def playTriangleWave(self):
        """
        Description: Stores all info on the Triangle wave preset, will be called when keys are pressed. Holds all math necessary for mono notes and arpeggios.
        Parameter: none
        Returns: none
        """
        self.generateArray()
        # uses sounddevice to play Mono notes
        if self.style == "Mono":
            self.waveform = ((2 * self.amplitude) / np.pi) * np.arcsin(np.sin(2 * np.pi * self.frequency * self.sample_array))
            self.playMono()
        # uses simpleaudio to play arpeggios
        elif self.style == "Duo":
            self.frequency_1, self.frequency_2 = self.getFrequencies()
            self.note_1 = ((2 * self.amplitude) / np.pi) * np.arcsin(np.sin(2 * np.pi * self.frequency_1 * self.sample_array))
            self.note_2 = ((2 * self.amplitude) / np.pi) * np.arcsin(np.sin(2 * np.pi * self.frequency_2 * self.sample_array))
            self.waveform = np.hstack((self.note_1, self.note_2))
            self.playSound()
        # triad arpeggio
        elif self.style == "Trio":
            self.frequency_1, self.frequency_2, self.frequency_3 = self.getFrequencies()
            self.note_1 = ((2 * self.amplitude) / np.pi) * np.arcsin(np.sin(2 * np.pi * self.frequency_1 * self.sample_array))
            self.note_2 = ((2 * self.amplitude) / np.pi) * np.arcsin(np.sin(2 * np.pi * self.frequency_2 * self.sample_array))
            self.note_3 = ((2 * self.amplitude) / np.pi) * np.arcsin(np.sin(2 * np.pi * self.frequency_3 * self.sample_array))
            self.waveform = np.hstack((self.note_1, self.note_2, self.note_3))
            self.playSound()
        # major 7th arpeggio
        elif self.style == "Quattro":
            self.frequency_1, self.frequency_2, self.frequency_3, self.frequency_4 = self.getFrequencies()
            self.note_1 = ((2 * self.amplitude) / np.pi) * np.arcsin(np.sin(2 * np.pi * self.frequency_1 * self.sample_array))
            self.note_2 = ((2 * self.amplitude) / np.pi) * np.arcsin(np.sin(2 * np.pi * self.frequency_2 * self.sample_array))
            self.note_3 = ((2 * self.amplitude) / np.pi) * np.arcsin(np.sin(2 * np.pi * self.frequency_3 * self.sample_array))
            self.note_4 = ((2 * self.amplitude) / np.pi) * np.arcsin(np.sin(2 * np.pi * self.frequency_4 * self.sample_array))
            self.waveform = np.hstack((self.note_1, self.note_2, self.note_3, self.note_4))
            self.playSound()

    def playSawtoothWave(self):
        """
        Description: Stores all info on the Sawtooth wave preset, will be called when keys are pressed. Holds all math necessary for mono notes and arpeggios.
        Parameter: none
        Returns: none
        """
        self.generateArray()
        # uses sounddevice to play Mono notes
        if self.style == "Mono":
            self.waveform = -(((2 * self.amplitude)/ np.pi) * np.arctan(1 / (np.tan(self.sample_array * np.pi * self.frequency))))
            self.playMono()
        # uses simpleaudio to play arpeggios
        elif self.style == "Duo":
            self.frequency_1, self.frequency_2 = self.getFrequencies()
            self.note_1 = -(((2 * self.amplitude)/ np.pi) * np.arctan(1 / (np.tan(self.sample_array * np.pi * self.frequency_1))))
            self.note_2 = -(((2 * self.amplitude)/ np.pi) * np.arctan(1 / (np.tan(self.sample_array * np.pi * self.frequency_2))))
            self.waveform = np.hstack((self.note_1, self.note_2))
            self.playSound()
        # triad arpeggio
        elif self.style == "Trio":
            self.frequency_1, self.frequency_2, self.frequency_3 = self.getFrequencies()
            self.note_1 = -(((2 * self.amplitude)/ np.pi) * np.arctan(1 / (np.tan(self.sample_array * np.pi * self.frequency_1))))
            self.note_2 = -(((2 * self.amplitude)/ np.pi) * np.arctan(1 / (np.tan(self.sample_array * np.pi * self.frequency_2))))
            self.note_3 = -(((2 * self.amplitude)/ np.pi) * np.arctan(1 / (np.tan(self.sample_array * np.pi * self.frequency_3))))
            self.waveform = np.hstack((self.note_1, self.note_2, self.note_3))
            self.playSound()
        # major 7th arpeggio
        elif self.style == "Quattro":
            self.frequency_1, self.frequency_2, self.frequency_3, self.frequency_4 = self.getFrequencies()
            self.note_1 = -(((2 * self.amplitude)/ np.pi) * np.arctan(1 / (np.tan(self.sample_array * np.pi * self.frequency_1))))
            self.note_2 = -(((2 * self.amplitude)/ np.pi) * np.arctan(1 / (np.tan(self.sample_array * np.pi * self.frequency_2))))
            self.note_3 = -(((2 * self.amplitude)/ np.pi) * np.arctan(1 / (np.tan(self.sample_array * np.pi * self.frequency_3))))
            self.note_4 = -(((2 * self.amplitude)/ np.pi) * np.arctan(1 / (np.tan(self.sample_array * np.pi * self.frequency_4))))
            self.waveform = np.hstack((self.note_1, self.note_2, self.note_3, self.note_4))
            self.playSound()

    def getFrequencies(self):
        """
        Description: Determines which notes are to be chosen in each arpeggio.
        Parameter: none
        Returns: none
        """
        # chooses the first two notes from the keystrokes respective dictionary
        if self.style == "Duo":
            frequency_1 = self.frequency_dict[self.arpeggiation_dict[self.letter][0]]
            frequency_2 = self.frequency_dict[self.arpeggiation_dict[self.letter][1]]
            return (frequency_1, frequency_2)
        # chooses the first three notes from the keystrokes respective dictionary
        elif self.style == "Trio":
            frequency_1 = self.frequency_dict[self.arpeggiation_dict[self.letter][0]]
            frequency_2 = self.frequency_dict[self.arpeggiation_dict[self.letter][1]]
            frequency_3 = self.frequency_dict[self.arpeggiation_dict[self.letter][2]]
            return (frequency_1, frequency_2, frequency_3)
        # chooses the first four notes from the keystrokes respective dictionary
        elif self.style == "Quattro":
            frequency_1 = self.frequency_dict[self.arpeggiation_dict[self.letter][0]]
            frequency_2 = self.frequency_dict[self.arpeggiation_dict[self.letter][1]]
            frequency_3 = self.frequency_dict[self.arpeggiation_dict[self.letter][2]]
            frequency_4 = self.frequency_dict[self.arpeggiation_dict[self.letter][3]]
            return (frequency_1, frequency_2, frequency_3, frequency_4)
