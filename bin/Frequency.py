class Frequency:
    def __init__(self, frequency_hz, amplitude, sample_rate, note_time):
        """
        Description: initializes factors needed for creating the frequency
        Parameter: frequency_hz (int) the hertz of the frequency
                   amplitude (int) the highest value
                   sample_rate (int)
                   note_time (int) how long the notes play for
        Returns: none
        """
        self.frequency_hz = frequency_hz
        self.amplitude = amplitude
        self.sample_rate = sample_rate
        self.note_time = note_time

    def getFrequency(self):
        """
        Description: returns the value in hertz
        Parameter: none
        Returns: self.frequency_hz, the hertz of the frequency
        """
        return self.frequency_hz

    def getAmplitude(self):
        """
        Description: returns the amplitude of the frequency
        Parameter: none
        Returns: self.amplitude, the highest y value
        """
        return self.amplitude

    def getSamplesPerSec(self):
        """
        Description: returns the sample rate of the frequency
        Parameter: none
        Returns: self.sample_rate, the same rate of the frequency
        """
        return self.sample_rate

    def getDuration(self):
        """
        Description: returns duration of a note
        Parameter: none
        Returns: self.note_time, the duration of a note
        """
        return self.note_time
