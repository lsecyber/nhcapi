import vmixapi as vmixapi
import vmixfunctions as vFunc
import ptzfunctions as ptz
import argparse
from urllib.parse import quote
from tkinter.messagebox import askyesno
from time import sleep

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


def startStream():
    """
    Starts the stream and prepares it. Prompts for conformation first.
    :return: Returns True if successful, False if not
    :rtype: bool
    """
    try:
        # open vmix if not open
        if not vmixapi.checkvMixRunning():
            if not vFunc.openvMix('C:\\QuickAccess Files\\vMix\\vMix - Sunday Mornings New.vmix'):
                print('ERROR: vmix could not be opened.')
                exit()

        # fade to slides input
        vFunc.fadeToInput(slidesInputKey)

        # fade soundboard audio down
        vFunc.fadeAudioSourceDown(soundboardAudioInputKey, duration=1000)

        # fade PC audio up
        vFunc.fadeAudioSourceUp(pcAudioInputKey, duration=1000)

        # start streaming after confirming
        yesNoAnswer = yesNoMessageBox('Are you sure that you would like to start streaming?')
        if yesNoAnswer:
            vFunc.startStreaming()

        # start external output
        vFunc.startExternal()

        # save thumbnail of service to D:\Downloads folder
        vFunc.vMixFunction(function='SnapshotInput',
                           value=quote("D:\Downloads\Thumbnail - {0:dd MMM yyyy}.jpg", safe='.'),
                           rawInputKey=sundayMorningWorshipDateInputKey)

        # set PTZ to announcements zoom
        ptz.recallPreset(PTZ_ANNOUNCEMENTS_PRESET)

        # 1000ms delay
        sleep(1)

        # send static date to preview vMix
        vFunc.previewInput(sundayMorningWorshipDateInputKey)

    except:
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
        vFunc.fadeToInput(ptzWithoutLyricsInputKey)
        vFunc.switchAudioSource(pcAudioInputKey, soundboardAudioInputKey, 1000)
        sleep(1)
        vFunc.previewInput(slidesInputKey)
    except:
        return False
    else:
        return True


def startFirstSong():
    ptz.recallPreset(PTZ_WIDE_PRESET)
    sleep(0.5)
    vFunc.fadeToInput(ptzWithLyricsInputKey)
    sleep(1)
    vFunc.previewInput(slidesInputKey)


def startGreeting():
    vFunc.selectPlaylist(greetingPlaylistName)
    vFunc.startPlaylist()
    vFunc.switchAudioSource(soundboardAudioInputKey, pcAudioInputKey, 1000)
    vFunc.showLargePreview(ptzWithLyricsInputKey)


def endGreeting():
    vFunc.hideLargePreview(ptzWithLyricsInputKey)
    vFunc.stopPlaylist()
    vFunc.fadeToInput(ptzWithLyricsInputKey)
    vFunc.switchAudioSource(pcAudioInputKey, soundboardAudioInputKey, 1000)
    sleep(1)
    vFunc.previewInput(slidesInputKey)


def startSermon():
    ptz.recallPreset(PTZ_PREACHING_PRESET)
    sleep(1.25)
    vFunc.fadeToInput(ptzWithoutLyricsInputKey)
    sleep(1)
    vFunc.previewInput(slidesInputKey)


def startCommunion():
    vFunc.fadeToInput(slidesInputKey)


def endCommunion():
    vFunc.fadeToInput(ptzWithoutLyricsInputKey)


def startLastSong():
    ptz.recallPreset(PTZ_WIDE_PRESET)
    sleep(0.5)
    vFunc.fadeToInput(ptzWithLyricsInputKey)
    sleep(1)
    vFunc.previewInput(slidesInputKey)


def endService():
    vFunc.fadeToInput(slidesInputKey)
    sleep(1.1)
    vFunc.previewInput(sundayMorningWorshipDateInputKey)
    sleep(0.5)
    vFunc.stopRecording()


def endStream():
    vFunc.fadeAudioSourceDown(soundboardAudioInputKey)
    sleep(4)
    if not yesNoMessageBox('Are you sure you would like to stop streaming?'):
        exit()
    else:
        vFunc.stopExternal()
        vFunc.stopRecording()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description="Run the specified message and options as a command.")
    p.add_argument('-s', '--step', type=str, required=True,
                   help="Step to perform. (required)")
    args = p.parse_args()
    step = args.step.strip()

    optionsArray = [
        "startStream",
        "startService",
        "startFirstSong",
        "startGreeting",
        "endGreeting",
        "startSermon",
        "startCommunion",
        "endCommunion",
        "startLastSong",
        "endService",
        "endStream"
    ]

    if not step in optionsArray:
        print('Error - invalid step "' + step + '". Options: \n' + ", ".join(optionsArray))
        exit()
    else:
        print(str(locals()[step]()))