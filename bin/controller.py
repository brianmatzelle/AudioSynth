import numpy as np
import tkinter as tk
from tkinter import ttk
from bin import Frequency, Style, Waveform
import json

class Controller:
    def __init__(self):
        """
        Description: initializes all of the factors needed for the loops in the controller class
        and to create tkinter window
        Parameter: none
        Returns: none
        """
        # Creates tkinter window
        self.window = tk.Tk()
        # Updates the scores file
        self.programRan()
        self.window.title("Lenny's Disciples")
        self.window.iconbitmap("assets/icons/favicon.ico")
        self.createWidgets()
        self.keypressEvent(self.window)
        # Creates Frequency instance
        self.frequency_instance = Frequency.Frequency(frequency_hz=440, amplitude=1, sample_rate=44100, note_time=0.2)
        self.frequency = self.frequency_instance.getFrequency()
        self.amplitude = self.frequency_instance.getAmplitude()
        self.sample_rate = self.frequency_instance.getSamplesPerSec()
        self.note_time = self.frequency_instance.getDuration()
        self.waveform = "Sine"
        self.note_style = Style.Style()
        # dictionary for keystrokes and their respective notes
        self.keyboard_dict = {  "d" : "C", "r" : "C_SHARP", "f" : "D", "t" : "D_SHARP",
                                "g" : "E", "h" : "F", "u" : "F_SHARP", "j" : "G",
                                "i" : "G_SHARP", "k" : "A", "o" : "A_SHARP", "l" : "B", ";" : "C2"
                            }
        # dictionary for notes and their respective frequencies
        self.frequency_dict = { "C" : 261.6256, "C_SHARP" : 277.1826, "D" : 293.6648, "D_SHARP" : 311.1270,
                                "E" : 329.6276, "F" : 349.2282, "F_SHARP" : 369.9944, "G" : 391.9954,
                                "G_SHARP" : 415.3047, "A" : 440.0, "A_SHARP" : 466.1638, "B" : 493.8833,
                                "C2" : 523.2511, "C_SHARP2" : 554.3653, "D2" : 587.3295, "D_SHARP2" : 622.2540,
                                "E2" : 659.2551, "F2" : 698.4565, "F_SHARP2" : 739.9888, "G2" : 783.9909,
                                "G_SHARP2" : 830.6094, "A2" : 880.0000, "A_SHARP2" : 932.3275, "B2" : 987.7666
                            }

        # Ignores Divide by Zero error
        np.seterr(divide='ignore', invalid='ignore')
        # Print instructions
        message =  """
                        How to play:

                        | |  ||  |  | |  ||  ||  |  |   |
                        | |C#||D#|  | |F#||G#||A#|  |   |
                        | |__||__|  | |__||__||__|  |   |
                        |   |   |   |   |   |   |   |   |
                        | C | D | E | F | G | A | B | C2|
                        |___|___|___|___|___|___|___|___|

                                 |R|T| |U|I|O|
                                |D|F|G|H|J|K|L|;|
                        """
        print(message)


    def createButtons(self, parent, text_1, text_2, text_3, text_4):
        """
        Description: creates buttons used for style and waveforms
        Parameter: parent (str) determines which widget the buttons are being used for
                   text_1 (str) button 1 label
                   text_2 (str) button 2 label
                   text_3 (str) button 3 label
                   text_4 (str) button 4 label
        Returns: button_1 (string), top left button
                 button_2 (string), top right button
                 button_3 (string), bottom left button
                 button_4 (string), bottom right button
        """
        # Creates an outline for a set of 4 buttons
        button_1 = ttk.Button(parent, text=text_1, command=lambda: self.buttonPressed(text_1), compound = tk.LEFT)
        button_1.grid(row=1, column=1, ipadx=10, ipady=5, padx=5, pady=5)
        button_2 = ttk.Button(parent,text=text_2, command=lambda: self.buttonPressed(text_2), compound = tk.LEFT)
        button_2.grid(row=1, column=2, ipadx=10, ipady=5, padx=5, pady=5)
        button_3 = ttk.Button(parent, text=text_3, command=lambda: self.buttonPressed(text_3), compound = tk.LEFT)
        button_3.grid(row=2, column=1, ipadx=10, ipady=5, padx=5, pady=5)
        button_4 = ttk.Button(parent, text=text_4, command=lambda: self.buttonPressed(text_4), compound = tk.LEFT)
        button_4.grid(row=2, column=2, ipadx=10, ipady=5, padx=5, pady=5)
        return (button_1, button_2, button_3, button_4)

    def createSlider(self, parent, text):
        """
        Description: creates slider used for volume
        Parameter: parent (str) determine which widget the slider goes in
                   text (str) volume label
        Returns: none
        """
        slider = ttk.Scale(parent, length=200, from_=100, to=0, orient=tk.VERTICAL, command=lambda x: self.convertVolume(slider, text))
        slider.grid(row=1, column=1)
        slider.set(100)

    def createWidgets(self):
        """
        Description: creates the widgets for the GUI
        Parameter: none
        Returns: none
        """
        # Create room around Each section
        self.window["padx"] = 10
        self.window["pady"] = 10
        # Create Waveforms section
        waveform_frame = ttk.LabelFrame(self.window, text="Waveforms", relief=tk.RIDGE)
        waveform_frame.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=20, pady=5)
        waveform_buttons = self.createButtons(waveform_frame, "Sine", "Sawtooth", "Triangle", "Square")

        # Create Styles section
        style_frame = ttk.LabelFrame(self.window, text="Styles", relief=tk.RIDGE)
        style_frame.grid(row=2, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=20, pady=5)
        style_buttons = self.createButtons(style_frame, "Mono", "Duo", "Trio", "Quattro")


        # Create Volume section
        volume_frame = ttk.LabelFrame(self.window, text="Volume", relief=tk.RIDGE)
        volume_frame.grid(row=1, rowspan=2, column=2, sticky=tk.E + tk.W + tk.N + tk.S, padx=20, pady=5)
        self.createSlider(volume_frame, "Volume")

        # Create stats section
        self.stats_frame = ttk.LabelFrame(self.window, text="Stats", relief=tk.RIDGE)
        self.stats_frame.grid(row=3, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=20, pady=5)
        # Keypress label
        self.total_keypress_string = "Total Keypresses: " + str(self.number_of_keypresses)
        self.var_1 = tk.StringVar()
        self.var_1.set(self.total_keypress_string)
        stats_label = ttk.Label(self.stats_frame, textvariable=self.var_1)
        stats_label.grid(row=1, column=1)
        # High score label
        self.high_score_string = ""
        self.var_2 = tk.StringVar()
        self.var_2.set(self.high_score_string)
        high_score_label = ttk.Label(self.stats_frame, textvariable=self.var_2)
        high_score_label.grid(row=1, column=2)


        # Quit button in the BOTTOM right corner
        quit_button = ttk.Button(self.window, text="Quit", command=self.window.destroy)
        quit_button.grid(row=3, column=2, sticky=tk.E + tk.S, ipadx=5)

    def keypressEvent(self, focus):
        """
        Description: Highlights the clicked button, so the user receives
        feedback that the program is responding.
        Parameter: focus (tkinter object) the button that is clicked
        Returns: none
        """
        focus.bind("<Key>", self.keyPressed)

    def keyPressed(self, key):
        """
        Description: Determines that a ket is pressed
        Parameter: key (str) the key being played
        Returns: none
        """
        key_letter = key.char
        self.playKey(key_letter)
        self.updateKeyPresses()

    def buttonPressed(self, text):
        """
        Description: determines when a button is pressed
        Parameter: text (str) the label of button
        Returns: none
        """
        if text in ("Sine", "Sawtooth", "Triangle", "Square"):
            self.waveform = text
        elif text in ("Mono", "Duo", "Trio", "Quattro"):
            self.note_style.current_style = text
        else:
            pass

    def convertVolume(self, val, text):
        """
        Description: Converts the slider's value into an integer,
        so it can adjust the amplitude, which changes the volume
        Parameter: val (str) the current value of the slider,
        text (str) so the correct slider is chosen
        Returns: none
        """
        value = int(val.get())
        if text == "Volume":
            self.amplitude = value / 100

    def playKey(self, key):
        """
        Description: Plays the key depending on
        which waveform is chosen and updates the scores file
        Parameter: key (str) the key being played
        Returns: none
        """

        if key not in self.keyboard_dict.keys():
            pass
        else:
            letter = self.keyboard_dict[key]
            self.frequency = self.frequency_dict[letter]
            note = Waveform.Waveform(self.frequency, self.amplitude, self.sample_rate, self.note_time, self.note_style.current_style, letter)
            # determines which waveform is being played
            if self.waveform == "Sine":
                note.playSineWave()
            elif self.waveform == "Triangle":
                note.playTriangleWave()
            elif self.waveform == "Square":
                note.playSquareWave()
            elif self.waveform == "Sawtooth":
                note.playSawtoothWave()
            else:
                pass

    def updateKeyPresses(self):
        """
        Description: Reads the scores file and updates the number_of_keypresses value
        whenever a key is pressed
        Parameter: self
        Returns: None
        """
        with open("assets/scores.json", "r") as read_file:
            self.scores = json.load(read_file)
        self.scores["number_of_keypresses"] += 1
        self.number_of_keypresses = self.scores["number_of_keypresses"]
        self.most_keypresses = self.scores["most_keypresses"]
        if self.number_of_keypresses > self.most_keypresses:
            self.scores["most_keypresses"] = self.number_of_keypresses
            self.high_score = True
            self.displayHighscore()
        with open("assets/scores.json", "w") as write_file:
            json.dump(self.scores, write_file)
        self.total_keypress_string = "Total Keypresses: " + str(self.number_of_keypresses)
        self.var_1.set(self.total_keypress_string)

    def programRan(self):
        """
        Description: Reads the scores file and updates the times_program_ran value
        whenever the program is ran
        Parameter: self
        Returns: None
        """
        with open("assets/scores.json", "r") as read_file:
            self.scores = json.load(read_file)
        self.scores["times_program_ran"] += 1
        self.scores["number_of_keypresses"] = 0
        self.number_of_keypresses = self.scores["number_of_keypresses"]
        with open("assets/scores.json", "w") as write_file:
            json.dump(self.scores, write_file)

    def displayHighscore(self):
        """
        Description: Reads the scores file and updates the times_program_ran value
        whenever the program is ran
        Parameter: self
        Returns: None
        """
        self.high_score_string = "High Score: " + str(self.most_keypresses) + "!"
        self.var_2.set(self.high_score_string)
