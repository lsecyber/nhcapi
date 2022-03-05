import urllib3
import xmltodict
import traceback

def checkvMixRunning():
    url = "http://192.168.168.30:8088/API"
    timeout = urllib3.util.Timeout(connect=0.3,read=0.5)
    http = urllib3.PoolManager(timeout=timeout)
    try:
        response = http.request('GET', url,)
        return True
    except:
        return False

    
def getvMixAPI():  # Downloads the API information from vMix.
    url = "http://192.168.168.30:8088/API"

    http = urllib3.PoolManager()

    response = http.request('GET', url)

    try:
        data = xmltodict.parse(response.data)
    except:
        print("Failed to parse xml from response (%s)" % traceback.format_exc())

    return data['vmix']


def lookupInputKey(inputKeyToLookup):
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
        if (x > 100):
            print("x > 100")
            break

    for x in listOfKeys:
        if (inputKeyToLookup == x):
            inputKeyFound = True
            break
        else:
            inputKeyFound = False
    return inputKeyFound


def isValidInputKey(inputKeyToCheck: str):
    if (len(inputKeyToCheck) != 36):
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

        if (dash1 != "-"):
            return False
        elif (dash2 != "-"):
            return False
        elif (dash3 != "-"):
            return False
        elif (dash4 != "-"):
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
    Returns a dictionary with the left and right average of the volume meter, as well as the average meter. Value from 0 to 1.
    """
# Extracts Volume Statistics from Main.
    data = getvMixAPI()
        
    leftAudio = data['audio']['master']['@meterF1']
    rightAudio = data['audio']['master']['@meterF2']
    average = (float(leftAudio) + float(rightAudio)) * 2

    if (average <= 0.1):
        quiet = True
    else:
        quiet = False
    
    audioResult = dict([('left', leftAudio),('right', rightAudio),('average', average),('quiet',quiet)])

    return audioResult

def getInputDetails(inputNumber):  # Extracts Input Details from the vMix API.
    # Check if it is a valid input
    try:
        data = getvMixAPI()['inputs']['input'][int(inputNumber)-1]
        data['@title']
    except IndexError as e:
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
    # Check if it is a valid input
    try:
        data = getvMixAPI()['inputs']['input'][int(inputNumber)-1]
        data['@title']
    except IndexError as e:
        print(f"Input number {inputNumber} does not exist.")
        return None

    try:
        if (data['@muted'] == 'False'):
            audioInputResultMuted = False
        else:
            audioInputResultMuted = True
    
        if (data['@solo'] == 'False'):
            audioInputResultSolo = False
        else:
            audioInputResultSolo = True
    
    except KeyError as e:
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


def getStreamingDetails(logsPath: str="C:/ProgramData/vMix/streaming/"):
    streamingData

