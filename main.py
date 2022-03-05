import vmixapi
import vmixfunctions
import ptzfunctions
import time



print(vmixapi.checkvMixRunning())

print(vmixfunctions.openvMix())

print(vmixapi.checkvMixRunning())

"""
examples:
x = input("PTZ preset to recall: ")
print(ptzfunctions.recallPreset(int(x)))


x = input("Input num for details:  ")
print("Input details: ", vmixapi.getAudioInputDetails(x))

x = input("Input num for details:  ")
print("Input details: ", vmixapi.getAudioInputDetails(x))


x = input("Input key to fade down:  ")
y = input("Input key to fade up: ")

print("Executed?  ", vmixfunctions.switchAudioSource(x,y))

print("Starting record")
print(vmixfunctions.startRecording())
input("Press enter or return to stop recording.")
print(vmixfunctions.stopRecording())

"""
