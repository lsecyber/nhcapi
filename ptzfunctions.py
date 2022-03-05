import urllib3
import traceback
import socket
import string

def sendHexCommand(hexCommand: str,targetIP: str="192.168.168.41"):
    hexcmd = hexCommand.replace(" ","")
    tcpPort = 5678
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    oldTimeout = s.gettimeout()
    s.connect((targetIP, tcpPort))
    data = bytes.fromhex(hexcmd)
    s.send(data)
    datarecv1 = s.recv(1024)
    print("Exicuting now...")
    s.settimeout(10)
    try:
        datarecv2 = s.recv(1024)
    except socket.timeout as e:
        print("Camera did not successfully exicute command. Error: ",e,'\n',
              "Data from camera: ",datarecv2, '\n',
              "responseCheck on data from camera: ", responseCheck(hexCommand))
        return False
    s.settimeout(oldTimeout)
    s.close()
    return responseCheck(datarecv1.hex())


def responseCheck(responseHex: str):
    if (len(responseHex) != 6):
        if (responseHex == "906002FF"):
            return "Syntax error - format of the hex command is incorrect."
        elif (responseHex == "906003FF"):
            return "Command buffer full - two sockets are already used, try again later."
        elif ((responseHex[0:3] == "906") and (responseHex[4:8] == "04ff")):
            return "Command canceled - a cancel command was sent in the other socket."
        elif ((responseHex[0:3] == "906") and (responseHex[4:8] == "05ff")):
            return "No socket - invalid cancle command or invalid socket number specified."
        elif ((responseHex[0:3] == "906") and (responseHex[4:8] == "41ff")):
            return "Command could not be executed due to current conditions."
    elif ((responseHex[0:3] != "904") or (responseHex[4:6] != "ff")):
        raise Exception("Invalid response from camera.")
    elif ((responseHex[0:3] != "904") or (responseHex[4:6] != "ff")):
        raise Exception("Camera returned an error in executing the command.")
    else:
        return True


def formatPresetNumber(rawPresetNumber: int,allowThreeDigits: bool=False):
    if (rawPresetNumber > 99):
        if ((allowThreeDigits) and (rawPresetNumber > 254)):
            return False
        else:
            return False
    elif ((rawPresetNumber > 89) and (rawPresetNumber < 100)):
        return False
    elif (rawPresetNumber < 10):
        try:
            presetNum = str(rawPresetNumber)
            presetNum = presetNum.zfill(2)
        except:
            return False
    else:
        try:
            presetNum = str(rawPresetNumber)
        except:
            return False
    
    return presetNum

        
def recallPreset(presetNumber: int,targetIP: str="192.168.168.41"):
    presetNum = formatPresetNumber(presetNumber)
    if (presetNum == False):
        print("Invalid preset number.")
        return False
    recallPresetCommand = "81 01 04 3F 02 "
    recallPresetCommand += presetNum
    recallPresetCommand += " FF"
    return sendHexCommand(recallPresetCommand,targetIP)


def setPreset(presetNumber: int,targetIP: str="192.168.168.41"):
    presetNum = formatPresetNumber(presetNumber)
    if (presetNum == False):
        print("Invalid preset number.")
        return False
    recallPresetCommand = "81 01 04 3F 01 "
    recallPresetCommand += presetNum
    recallPresetCommand += " FF"
    return sendHexCommand(recallPresetCommand,targetIP)

def goHome(targetIP: str="192.168.168.41"):
    return recallPreset(0,targetIP)


def autoFocus(targetIP: str="192.168.168.41"):
    hexcmd = "81 01 04 38 02 FF"
    return sendHexCommand(hexcmd,targetIP)

#print(recallPreset(5))


#sendHexCommand("81 01 04 38 02 FF")

