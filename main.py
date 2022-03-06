import vmixapi
import vmixfunctions
import ptzfunctions
import time
import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the specified message and options as a command.")
    parser.add_argument('-f', '--function', type=str, required=True,help="Function to perform. (required)")
    parser.add_argument('-i', '--input-key', type=str, required=False,help="Input key to run function on (only used for vMix). (optional)")
    parser.add_argument('-d', '--duration', type=int, required=False,help="Duration of function for fades. (optional)")
    args = parser.parse_args()
    print("Function: '",args.function,"'")
    print("Duration: '",args.duration,"'")
    print("Input Key: '",args.input_key,"'")


#print(vmixapi.checkvMixRunning())

#print(vmixfunctions.openvMix())

#print(vmixapi.checkvMixRunning())

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
