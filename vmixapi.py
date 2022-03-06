import urllib3
import xmltodict
import traceback
import os
from datetime import datetime
from os import listdir
from os.path import isfile, join

def checkvMixRunning():
    """
    Checks if vMix is actively running by calling its API, and if there is no response, it determines that vMix is off.

    :return: True if vMix is running and accessible, False if not
    :rtype: bool
    """

    url = "http://192.168.168.30:8088/API"
    timeout = urllib3.util.Timeout(connect=0.3, read=0.5)
    http = urllib3.PoolManager(timeout=timeout)
    try:
        http.request('GET', url, )
        return True
    except:
        return False


def getvMixAPI():  # Downloads the API information from vMix.
    """
    Returns a dictionary with all of vMix's raw information from its API. It then converts the raw xml to a python dict.
    :return: a dictionary with all the information from vMix's API
    :rtype: dict
    """
    url = "http://192.168.168.30:8088/API"

    http = urllib3.PoolManager()

    response = http.request('GET', url)

    try:
        data = xmltodict.parse(response.data)
    except:
        print("Failed to parse xml from response (%s)" % traceback.format_exc())

    return data['vmix']


def lookupInputKey(inputKeyToLookup: str):
    """
    Checks if the input key provided is an input in vMix.

    :param inputKeyToLookup: input key to check
    :type inputKeyToLookup: str
    :return: returns True if it is in vMix, False if not
    :rtype: bool
    """
    listData = getvMixAPI()
    listData = listData['inputs']
    listOfKeys = []
    x = 0
    while True:
        try:
            listOfKeys.append(str(listData['input'][x]['@key']))
            x = x + 1
        except:
            break
        if x > 100:
            print("x > 100")
            break

    inputKeyFound = False
    for x in listOfKeys:
        if inputKeyToLookup == x:
            inputKeyFound = True
            break
        else:
            inputKeyFound = False
    return inputKeyFound


def isValidInputKey(inputKeyToCheck: str):
    """
    Checks the formatting of the provided input key to see if it is a valid vMix input key.

    :param inputKeyToCheck: input key to process
    :type inputKeyToCheck: str
    :return: returns True if it is a valid input key, False if not
    :rtype: bool
    """

    if len(inputKeyToCheck) != 36:
        return False
    else:
        dash1 = str(inputKeyToCheck[8])
        dash2 = str(inputKeyToCheck[13])
        dash3 = str(inputKeyToCheck[18])
        dash4 = str(inputKeyToCheck[23])
        pt1 = str(inputKeyToCheck[0:8])
        pt2 = str(inputKeyToCheck[9:13])
        pt3 = str(inputKeyToCheck[14:18])
        pt4 = str(inputKeyToCheck[19:23])
        pt5 = str(inputKeyToCheck[24:36])

        if dash1 != "-":
            return False
        elif dash2 != "-":
            return False
        elif dash3 != "-":
            return False
        elif dash4 != "-":
            return False
        elif not pt1.isalnum():
            return False
        elif not pt2.isalnum():
            return False
        elif not pt3.isalnum():
            return False
        elif not pt4.isalnum():
            return False
        elif not pt5.isalnum():
            return False
        else:
            return lookupInputKey(inputKeyToCheck)


def getVolumeStatistics():
    """
    Get the statistics of the master volume output of vMix.

    :returns: a dictionary with the left and right average of the volume meter and the average meter; value from 0 to 1.
    :rtype: dict
    """

    data = getvMixAPI()

    leftAudio = data['audio']['master']['@meterF1']
    rightAudio = data['audio']['master']['@meterF2']
    average = (float(leftAudio) + float(rightAudio)) * 2

    if average <= 0.1:
        quiet = True
    else:
        quiet = False

    audioResult = dict([('left', leftAudio), ('right', rightAudio), ('average', average), ('quiet', quiet)])

    return audioResult


def getInputDetails(inputNumber: int):
    """
    Gets a specific input's details from vMix's API.
    Note: this does not include audio details such as gain and meter, use getAudioInputDetails() instead.

    :param inputNumber: input number to get details for
    :type inputNumber: int
    :returns: a dictionary with the input's number, key, type, title, shortTitle, state, duration, and loop
    :rtype: dict
    """

    # Check if it is a valid input
    try:
        data = getvMixAPI()['inputs']['input'][int(inputNumber) - 1]['@title']
    except IndexError:
        print(f"Input number {inputNumber} does not exist.")
        return None

    inputResult = dict([
        ('number', int(data['@number'])),
        ('key', data['@key']),
        ('type', data['@type']),
        ('title', data['@title']),
        ('shortTitle', data['@shortTitle']),
        ('state', data['@state']),
        ('duration', float(data['@duration'])),
        ('loop', bool(data['@loop']))
    ])

    return inputResult


def getAudioInputDetails(inputNumber):
    """
        Gets a specific audio input's details from vMix's API.

        :param inputNumber: input number to get details for
        :type inputNumber: int
        :returns: a dictionary with the input's number, key, type, title, shortTitle, state, muted (bool), volume,
        ballance, solo (bool), leftMeter, rightMeter, meter, and gain.
        :rtype: dict
    """

    # Check if it is a valid input
    try:
        data = getvMixAPI()['inputs']['input'][int(inputNumber) - 1]['@title']
    except IndexError:
        print(f"Input number {inputNumber} does not exist.")
        return None

    try:
        if data['@muted'] == 'False':
            audioInputResultMuted = False
        else:
            audioInputResultMuted = True

        if data['@solo'] == 'False':
            audioInputResultSolo = False
        else:
            audioInputResultSolo = True

    except KeyError:
        print("This input is not an audio input, running getInputDetails on it.")
        return getInputDetails(inputNumber)

    audioInputResult = dict([
        ('number', int(data['@number'])),
        ('key', data['@key']),
        ('title', data['@title']),
        ('shortTitle', data['@shortTitle']),
        ('state', data['@state']),
        ('muted', audioInputResultMuted),
        ('volume', int(data['@volume'])),
        ('balance', int(data['@balance'])),
        ('solo', audioInputResultSolo),
        ('leftMeter', float(data['@meterF1'])),
        ('rightMeter', float(data['@meterF2'])),
        ('meter', float((float(data['@meterF1']) + float(data['@meterF2'])) / 2)),
        ('gain', int(round(float(data['@gainDb']))))
    ])

    return audioInputResult


def getStreamingDetails(logsPath: str = "C:/ProgramData/vMix/streaming/"):
    filelist = [f for f in listdir(logsPath) if isfile(join(logsPath, f))]
    now = datetime.now()
    today = now.strftime("%Y%m%d")
    filename_part_1 = "streaming1 " + today + "-"
    possibleFileChoices = list()
    for file in filelist:
        if file[0:20] == filename_part_1:
            possibleFileChoices.append(file)

    if len(possibleFileChoices) == 0:
        streamingLog = None
    else:
        streamingLog = possibleFileChoices[-1]
    streaming_log_absolute_path = logsPath + str(streamingLog)

    with open(streaming_log_absolute_path) as log_file:
        streamingLogLines = [line.rstrip() for line in log_file][-1]
        print(streamingLogLines)





