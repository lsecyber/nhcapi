import sundaymornings as sm
import rtmidi
import mido

midiout = rtmidi.MidiOut()
print(mido.get_output_names())


port = mido.open_output('streamingpc 2')
with mido.open_input() as inport:
    for msg in inport:
        print(msg)

