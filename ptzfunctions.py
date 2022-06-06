import socket


def sendHexCommand(hex_command: str, target_ip: str = "192.168.168.41"):
    """
    Sends a raw hex command to the ip address provided, and receives a response. Made to be used with PTZOptics cameras.

    :param hex_command: a string with the hex command to be parsed; spaces allowed as they will be removed
    :type hex_command: str
    :param target_ip: IP address to send the command to, defaults to 192.168.168.41
    :type target_ip: str
    :return: returns True if executed successfully, returns False if failed
    :rtype: bool
    """
    hex_cmd = hex_command.replace(" ", "")
    tcpPort = 5678
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    oldTimeout = s.gettimeout()
    s.connect((target_ip, tcpPort))
    data = bytes.fromhex(hex_cmd)
    s.send(data)
    data_received_1 = s.recv(1024)
    print("Executing PTZ command now...")
    s.settimeout(10)
    data_received_2 = ""
    try:
        data_received_2 = s.recv(1024)
    except socket.timeout as e:
        print("Camera did not successfully execute command. Error: ", e, '\n',
              "Data from camera: ", data_received_2, '\n',
              "responseCheck on data from camera: ", responseCheck(hex_command))
        return False
    s.settimeout(oldTimeout)
    s.close()
    return responseCheck(data_received_1.hex())


def responseCheck(response_hex: str):
    """
    Parses the hex response from the PTZOptics camera.

    @param response_hex: hex return to process
    @type response_hex: str
    @return: returns a string with an error or True if no errors
    """
    if len(response_hex) != 6:
        if response_hex == "906002FF":
            return "Syntax error - format of the hex command is incorrect."
        elif response_hex == "906003FF":
            return "Command buffer full - two sockets are already used, try again later."
        elif (response_hex[0:3] == "906") and (response_hex[4:8] == "04ff"):
            return "Command canceled - a cancel command was sent in the other socket."
        elif (response_hex[0:3] == "906") and (response_hex[4:8] == "05ff"):
            return "No socket - invalid cancel command or invalid socket number specified."
        elif (response_hex[0:3] == "906") and (response_hex[4:8] == "41ff"):
            return "Command could not be executed due to current conditions."
    elif (response_hex[0:3] != "904") or (response_hex[4:6] != "ff"):
        raise Exception("Invalid response from camera.")
    elif (response_hex[0:3] != "904") or (response_hex[4:6] != "ff"):
        raise Exception("Camera returned an error in executing the command.")
    else:
        return True


def formatPresetNumber(raw_preset_number: int, allow_three_digits: bool = False):
    """
    Formats a preset number and ensures that it is valid for a PTZ Optics camera. Number must be between 1-89.
    If number is between 1 and 9, this function pads the number with 0s to make it two digits.

    :param raw_preset_number: preset number to process
    :type raw_preset_number: int
    :param allow_three_digits: set to True to allow three-digit numbers up to 254, defaults to False
    :type allow_three_digits: bool
    :return: Returns False if an invalid number is provided, otherwise returns the formatted number.
    """
    if raw_preset_number > 99:
        if allow_three_digits and (raw_preset_number > 254):
            return False
        else:
            return False
    elif (raw_preset_number > 89) and (raw_preset_number < 100):
        return False
    elif raw_preset_number < 10:
        try:
            presetNum = str(raw_preset_number)
            presetNum = presetNum.zfill(2)
        except:
            return False
    else:
        try:
            presetNum = str(raw_preset_number)
        except:
            return False

    return presetNum


def recallPreset(preset_number: int, target_ip: str = "192.168.168.41"):
    """
    Recalls a specific preset from the PTZOptics camera. Number must be between 1 and 89.

    :param preset_number: the preset number to recall
    :type preset_number: int
    :param target_ip: ip address of the camera, defaults to 192.168.168.41
    :type target_ip: str
    :return: returns False if successful, True if failed
    :rtype: bool
    """
    preset_num = formatPresetNumber(preset_number)
    if not preset_num:
        print("Invalid preset number.")
        return False
    recall_preset_command = "81 01 04 3F 02 "
    recall_preset_command += preset_num
    recall_preset_command += " FF"
    return sendHexCommand(recall_preset_command, target_ip)


def setPreset(preset_number: int, target_ip: str = "192.168.168.41"):
    """
    Stores to a preset the PTZ camera's current position.

    :param preset_number: preset number to set on PTZ camera, must be between 1 and 89
    :type preset_number: int
    :param target_ip: ip address of camera, default 192.168.168.41
    :type target_ip: str
    :return: true if successful, false if failed
    :rtype: bool
    """
    preset_num = formatPresetNumber(preset_number)
    if not preset_num:
        print("Invalid preset number.")
        return False
    recallPresetCommand = "81 01 04 3F 01 "
    recallPresetCommand += preset_num
    recallPresetCommand += " FF"
    return sendHexCommand(recallPresetCommand, target_ip)


def goHome(target_ip: str = "192.168.168.41"):
    """
    Returns the PTZ camera to it's "home" position. This is accomplished by calling recallPreset() to preset 0.

    :param target_ip: the IP address to send the command to
    :type target_ip: str
    :return: returns True if command execution was successful, returns False if it failed.
    :rtype: bool
    """
    return recallPreset(0, target_ip)


def autoFocus(target_ip: str = "192.168.168.41"):
    """
    Set's the PTZ camera's focus mode to autofocus, and runs the autofocus command.
    :param target_ip:
    :type target_ip:
    :return:
    :rtype:
    """
    hex_cmd = "81 01 04 38 02 FF"
    return sendHexCommand(hex_cmd, target_ip)

# print(recallPreset(5))


# sendHexCommand("81 01 04 38 02 FF")
