import urllib3
import vmixapi
import traceback
import os
import time

def openvMix(presetFile: str="C:/QuickAccess Files/vMix/vMix - Sunday Mornings.vmix"):
    doesPresetExist = os.path.exists(presetFile)
    doesvMixExist = os.path.exists("C:/Program Files (x86)/vMix/vMix64.exe")
    if(vmixapi.checkvMixRunning()):
        return True
    if doesPresetExist and doesvMixExist:
        try:
            cmdStartvMix = os.startfile(presetFile)
            cont = True
            x = 0
            time.sleep(7)
            if (vmixapi.checkvMixRunning()):
                return True
            else:
                time.sleep(10)
                if (vmixapi.checkvMixRunning()):
                    return True
                else:
                    return False
            return True
        except Exception as e:
            print("Error starting vMix: ",e)
            return False
    else:
        return False
        
def vMixFunction(function: str,duration: int=0,rawInputKey: str="",value:str="",
                 targetIPOpt: str="127.0.0.1",targetPortOpt: str="8088"):
    vMixFunctionURL = "http://" + targetIPOpt + ":" + targetPortOpt + \
                     "/api/?Function=" + function

    if (rawInputKey != ""):
        if vmixapi.isValidInputKey(rawInputKey):
            vMixFunctionURL += "&Input="
            vMixFunctionURL += rawInputKey
        else:
            print("1")
            return False

    if (value != ""):
        vMixFunctionURL += "&Value="
        vMixFunctionURL += value

    if (duration != 0):
        vMixFunctionURL += "&Duration="
        vMixFunctionURL += str(duration)

    http = urllib3.PoolManager()

    try:
        response = http.request('GET', vMixFunctionURL)
    except:
        print("2")
        return False
    
    return True


def fadeToInput(inputKey: str,targetIP: str="127.0.0.1",targetPort: str="8088"):
    return vMixFunction(function="Fade", duration=1000, rawInputKey=inputKey, targetIPOpt=targetIP, targetPortOpt=targetPort)
    

def fadeAudioSourceDown(inputKey: str,duration: int=1500,targetIP: str="127.0.0.1",targetPort: str="8088"):
    valueForFadeDown = "0," + str(duration)
    return vMixFunction(function="SetVolumeFade", value=valueForFadeDown, rawInputKey=inputKey, targetIPOpt=targetIP, targetPortOpt=targetPort)


def fadeAudioSourceUp(inputKey: str,duration: int=1500,targetIP: str="127.0.0.1",targetPort: str="8088"):
    valueForFadeDown = "100," + str(duration)
    return vMixFunction(function="SetVolumeFade", value=valueForFadeDown, rawInputKey=inputKey, targetIPOpt=targetIP, targetPortOpt=targetPort)

def switchAudioSource(inputKeyFadeOut: str,inputKeyFadeIn: str,duration: int=1500,targetIP: str="127.0.0.1",targetPort: str="8088"):
    response1 = fadeAudioSourceDown(inputKeyFadeOut,duration,targetIP,targetPort)
    response2 = fadeAudioSourceUp(inputKeyFadeIn,duration,targetIP,targetPort)
    if (response1 and response2):
        return True
    else:
        return False


def previewInput(inputKey: str,targetIP: str="127.0.0.1",targetPort: str="8088"):
    return vMixFunction(function="PreviewInput", rawInputKey=inputKey, targetIPOpt=targetIP, targetPortOpt=targetPort)


def startStreaming(targetIP: str="127.0.0.1",targetPort: str="8088"):
    return vMixFunction(function="StartStreaming", targetIPOpt=targetIP, targetPortOpt=targetPort)


def startRecording(targetIP: str="127.0.0.1",targetPort: str="8088"):
    return vMixFunction(function="StartRecording", targetIPOpt=targetIP, targetPortOpt=targetPort)


def stopStreaming(targetIP: str="127.0.0.1",targetPort: str="8088"):
    return vMixFunction(function="StopStreaming", targetIPOpt=targetIP, targetPortOpt=targetPort)


def stopRecording(targetIP: str="127.0.0.1",targetPort: str="8088"):
    return vMixFunction(function="StopRecording", targetIPOpt=targetIP, targetPortOpt=targetPort)


def startExternal(targetIP: str="127.0.0.1",targetPort: str="8088"):
    return vMixFunction(function="StartExternal", targetIPOpt=targetIP, targetPortOpt=targetPort)


def stopExternal(targetIP: str="127.0.0.1",targetPort: str="8088"):
    return vMixFunction(function="StopExternal", targetIPOpt=targetIP, targetPortOpt=targetPort)


def startPlaylist(targetIP: str="127.0.0.1",targetPort: str="8088"):
    return vMixFunction(function="StartPlaylist", targetIPOpt=targetIP, targetPortOpt=targetPort)


def stopPlaylist(targetIP: str="127.0.0.1",targetPort: str="8088"):
    return vMixFunction(function="StopPlaylist", targetIPOpt=targetIP, targetPortOpt=targetPort)