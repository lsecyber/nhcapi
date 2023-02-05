import sys
sys.path.append('C:\\QuickAccess Files\git\\nhcapi')

import vmixapi
import vmixfunctions as vFunc
import ptzfunctions as ptz
import argparse
import threading
from urllib.parse import quote
from tkinter.messagebox import askyesno
from time import sleep
from inspect import currentframe, getframeinfo

slidesInputKey = '4796a1f1-c6ed-4c19-ae49-075b34010ca1'
soundboardAudioInputKey = '4aedac2e-764d-4fd5-a4d7-c24150876b11'
pcAudioInputKey = '7c5cb909-67ed-4976-9bce-98cf2b7a04e8'
sundayMorningWorshipDateInputKey = '0991058a-3932-4fc9-acc5-9a15c4c5ed42'
ptzWithoutLyricsInputKey = '732fc76a-deb1-41c8-8f31-5e3f9b21be4b'
ptzWithLyricsInputKey = '4a081625-53ff-4974-852c-b32148263186'

greetingPlaylistName = 'Greeting'

PTZ_ANNOUNCEMENTS_PRESET = 4
PTZ_PREACHING_PRESET = 5
PTZ_WIDE_PRESET = 8


def yesNoMessageBox(message: str, title: str = 'Confirm - NHC vMix'):
    """
    Using tkinter, pops up a message box to confirm yes or no.

    :param message: The message to display.
    :type message: str
    :param title: The title of the message box (defaults to 'Confirm - NHC vMix')
    :type title: str
    :return: True or False based on yes or no in the message box.
    :rtype: bool
    """
    return askyesno(title=title, message=message)


def error(previousLines: int = 0):
    """
    Throws a new error that show the line number where this function was called and the line content.

    :param previousLines: (Optional, default 0) Can be used to add lines to the error before where error() is called.
    :type previousLines: int
    """
    lineNumber = currentframe().f_back.f_lineno
    with open(getframeinfo(currentframe()).filename) as file:
        x = 0
        lines = file.readlines()
        lineContent = "\n"
        for line in lines:
            x += 1
            if previousLines == 0:
                if x == lineNumber:
                    lineContent = line.lstrip()
                    break
            else:
                if (lineNumber - previousLines) <= x <= lineNumber:
                    lineContent += str(x) + "|" + line

    raise Exception("Error running line " + str(lineNumber) + ": " + lineContent)


def startStream(promptForConfirmation = True):
    """
    Starts the stream and prepares it. Prompts for confirmation first.

    :return: Returns True if successful, False if not
    :rtype: bool
    """
    try:
        # open vmix if not open
        if not vmixapi.checkvMixRunning():
            if vFunc.openvMix('C:\\QuickAccess Files\\vMix\\vMix - Sunday Mornings New.vmix') is False: error()

        # fade to slides input
        if vFunc.fadeToInput(slidesInputKey) is False: error()

        # fade soundboard audio down
        if vFunc.fadeAudioSourceDown(soundboardAudioInputKey, duration=1000) is False: error()

        # fade PC audio up
        if vFunc.fadeAudioSourceUp(pcAudioInputKey, duration=1000) is False: error()

        # start streaming after confirming
        if promptForConfirmation:
            yesNoAnswer = yesNoMessageBox('Are you sure that you would like to start streaming?')
        else:
            yesNoAnswer = False
        
        if yesNoAnswer or not promptForConfirmation:
            vFunc.startStreaming()
            print('Just started streaming.')

        # start external output
        if vFunc.startExternal() is False: error()

        # save thumbnail of service to D:\Downloads folder
        if vFunc.vMixFunction(function='SnapshotInput',
                              value=quote("D:\Downloads\Thumbnail - {0:dd MMM yyyy}.jpg", safe='.'),
                              rawInputKey=sundayMorningWorshipDateInputKey) \
                is False: error(previousLines=3)

        # runs ptz.recallPreset asynchronously
        recallPresetThread = threading.Thread(target=ptz.recallPreset, args=([PTZ_ANNOUNCEMENTS_PRESET]), kwargs={})
        recallPresetThread.start()

        # 1000ms delay
        sleep(1)

        # send static date to preview vMix
        if vFunc.previewInput(sundayMorningWorshipDateInputKey) is False: error()

        # wait for recall preset to finish
        recallPresetThread.join()

    except Exception as e:
        print(str(e))
        return False
    else:
        return True


def startService():
    """
    Fades to ptz w/out lyrics, fades the sb audio down and the pc audio up, and sends the slides to preview.

    :return: Returns True if successful and False if fails.
    :rtype: bool
    """
    try:
        # fades to ptzWithoutLyrics input in vMix
        if vFunc.fadeToInput(ptzWithoutLyricsInputKey) is False: error()

        # fades pc audio down and soundboard audio up
        if vFunc.switchAudioSource(pcAudioInputKey, soundboardAudioInputKey, 1000) is False: error()

        sleep(1)

        # sends the slides to vMix preview
        if vFunc.previewInput(slidesInputKey) is False: error()
    except Exception as e:
        print(str(e))
        return False
    else:
        return True


def startSong():
    """
    Recalls the ptz wide preset, fades to ptz w/ lyrics, and sends the slides preview to the input.

    :return: Returns True if successful, False if failed.
    :rtype: bool
    """
    try:
        # runs ptz.recallPreset asynchronously
        recallPresetThread = threading.Thread(target=ptz.recallPreset, args=([PTZ_WIDE_PRESET]), kwargs={})
        recallPresetThread.start()

        sleep(0.5)

        # fades to the ptzWithLyrics input in vMix
        if vFunc.fadeToInput(ptzWithLyricsInputKey) is False: error()

        sleep(1)

        # sends the slides to vMix preview
        if vFunc.previewInput(slidesInputKey) is False: error()

        # wait for recall preset to finish
        recallPresetThread.join()
    except Exception as e:
        print(str(e))
        return False
    else:
        return True


def startFirstSong():
    """
    Alias for startSong()
    """
    startSong()


def startGreeting():
    """
    Selects the greeting playlist, starts that playlist, fades the soundboard audio down and the pc audio up, then shows
    a large preview of the ptz without lyrics input.

    :return: True if successful, False if not
    :rtype: bool
    """
    try:
        # select the greeting playlist
        if vFunc.selectPlaylist(greetingPlaylistName) is False: error()

        # start the playlist
        if vFunc.startPlaylist() is False: error()

        # fade soundboard down and pc up
        if vFunc.switchAudioSource(soundboardAudioInputKey, pcAudioInputKey, 1000) is False: error()

        # show a large preview of the slides input
        if vFunc.showLargePreview(slidesInputKey) is False: error()

    except Exception as e:
        print(str(e))
        return False
    else:
        return True


def endGreeting():
    """
    Hides the large preview, stops the greeting playlist, fades to the PTZ W/ Lyrics input, fades pc audio down and
    soundboard audio up, and sends the slides input to vMix preview
    :return: True if successful, False if there is an exception
    :rtype: bool
    """
    try:
        # hides the large preview of the slides input in vMix
        if vFunc.hideLargePreview(slidesInputKey) is False: error()

        # stops the greeting playlist
        if vFunc.stopPlaylist() is False: error()

        # fades to the ptz w/ lyrics input in vMix
        if vFunc.fadeToInput(ptzWithLyricsInputKey) is False: error()

        # fades the pc audio down and the soundboard audio up
        if vFunc.switchAudioSource(pcAudioInputKey, soundboardAudioInputKey, 1000) is False: error()

        sleep(1)

        # sends the slides input to vMix preview
        if vFunc.previewInput(slidesInputKey) is False: error()
    except Exception as e:
        print(str(e))
        return False
    else:
        return True


def startSermon():
    """
    Recalls the PTZ preaching preset, fades to PTZ w/out lyrics, and sends slides to preview in vMix.

    :return: True if successful, False if exception
    :rtype: bool
    """
    try:
        # Recalls the PTZ preaching preset (5)
        if ptz.recallPreset(PTZ_PREACHING_PRESET) is False: error()

        sleep(0.75)

        # fades to the ptz w/out lyrics input in vMix
        if vFunc.fadeToInput(ptzWithoutLyricsInputKey) is False: error()

        sleep(1)

        # previews the slides input in vMix
        if vFunc.previewInput(slidesInputKey) is False: error()
    except Exception as e:
        print(str(e))
        return False
    else:
        return True


def startCommunion():
    """
    Fades to the slides input.
    :return: True if successful, False if there is an error
    :rtype: bool
    """
    try:
        # fades to the slides input
        if vFunc.fadeToInput(slidesInputKey) is False: error()
    except Exception as e:
        print(str(e))
        return False
    else:
        return True


def endCommunion():
    """
    Fade to the ptz w/out lyrics input.
    :return: True if successful, False if error
    :rtype: bool
    """
    try:
        if vFunc.fadeToInput(ptzWithoutLyricsInputKey) is False: error()
    except Exception as e:
        print(str(e))
        return False
    else:
        return True


def startLastSong():
    """
    Alias for startSong()
    """
    startSong()


def endService():
    """
    Fade to the slides input, send the date slide to vMix preview, and stops recording WITHOUT CONFORMATION.

    :return: True if successful, False if there is an error
    :rtype: bool
    """
    try:
        # fade to slides input in vMix
        if vFunc.fadeToInput(slidesInputKey) is False: error()

        sleep(1.1)

        # send the static (dynamic) date slide to vMix preview
        if vFunc.previewInput(sundayMorningWorshipDateInputKey) is False: error()

        sleep(0.5)

        # stop recording in vMix
        if vFunc.stopRecording() is False: error()
    except Exception as e:
        print(str(e))
        return False
    else:
        return True


def endStream(promptForConfirmation = True):
    """
    Fade soundboard audio down, delay 4 secs, then prompt to stop external output and recording.

    :return:
    :rtype:
    """
    try:
        if vFunc.fadeAudioSourceDown(soundboardAudioInputKey) is False: error()
        sleep(4)
        if promptForConfirmation:
            if not yesNoMessageBox('Are you sure you would like to stop streaming?'):
                exit()
        else:
            if vFunc.stopExternal() is False: error()
            if vFunc.stopStreaming() is False: error()
    except Exception as e:
        print(str(e))
        return False
    else:
        return True

def shutdown():
    try:
        # fade to slides input in vMix
        if vFunc.fadeToInput(slidesInputKey) is False: error()

        sleep(1.1)

        # send the static (dynamic) date slide to vMix preview
        if vFunc.previewInput(sundayMorningWorshipDateInputKey) is False: error()

        sleep(0.5)

        # stop recording in vMix
        if vFunc.stopRecording() is False: error()
    except Exception as e:
        print(str(e))
        return False
    else:
        return True


def test():
    print('HELLO WORLD FROM TEST')
    return True


def runStep(step: str):
    """
    Runs the requested step, and returns False if the step is not provided
    :param step: The step to run
    :type step: str
    :return: Returns the string of the command or False if an error
    :rtype: bool
    """
    optionsArray = [
        "startStream",
        "startService",
        "startSong",
        "startFirstSong",
        "startGreeting",
        "endGreeting",
        "startSermon",
        "startCommunion",
        "endCommunion",
        "startLastSong",
        "endService",
        "endStream",
        "test"
    ]

    if step in optionsArray:
        if 'Stream' in step:
            return str(globals()[step](False))
        else:
            return str(globals()[step]())

    else:
        print('Error - invalid step "' + step + '". Options: \n' + ", ".join(optionsArray))
        return False


if __name__ == '__main__':
    p = argparse.ArgumentParser(description="Run the specified message and options as a command.")
    p.add_argument('-s', '--step', type=str, required=True,
                   help="Step to perform. (required)")
    args = p.parse_args()
    stepToRun = args.step.strip()

    runStep(stepToRun)
