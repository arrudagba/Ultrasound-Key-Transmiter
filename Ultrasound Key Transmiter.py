import math
import pyaudio
import string
import keyboard

# set the sample rate and duration
sample_rate = 44100
duration = 0.7

# define the mapping between letters and frequencies
letter_to_frequency = {}
for i, letter in enumerate(string.ascii_lowercase):
    letter_to_frequency[letter] = 1000 + (ord(letter) * 100)

# initialize PyAudio
p = pyaudio.PyAudio()
bit_depth = 8

# define a callback function to generate audio for a given letter
def callback(letter):
    # generate the tone for the letter
    # uncomment to not show the letter been pressed or the frequency been used
    # (use for debugging only)
    print('Char:' + letter + '    Frq:' + str(letter_to_frequency[letter]) + 'Hz')
    frequency = letter_to_frequency.get(letter, 0)
    if frequency == 0:
        return
    num_samples = int(sample_rate * duration)
    sine_wave = [math.sin(2 * math.pi * frequency * x / sample_rate) for x in range(num_samples)]
    sine_wave_normalized = [int((x + 1) / 2 * 255) for x in sine_wave]  # normalize and scale signal
    audio_bytes = bytes(sine_wave_normalized)

    # play tone
    stream = p.open(format=p.get_format_from_width(bit_depth // 8), channels=1, rate=sample_rate, output=True)

    stream.write(audio_bytes)
    stream.stop_stream()
    stream.close()


# listen for keyboard input and generate tones
while True:
    if keyboard.is_pressed('ctrl+c'):  # exit if Ctrl+C is pressed
        break

    for letter in string.ascii_lowercase:
        if keyboard.is_pressed(letter):
            callback(str(letter))

# clean up PyAudio resources
p.terminate()
