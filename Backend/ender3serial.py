import serial
import time
import os
#import datasender

ROOT_DIR = "/home/pi/code"
TODO_DIR = "/todo"
INPROGRESS_DIR = "/inprogress"
DONE_DIR = "/done"


bedTemp = 0
nozzleTemp = 0
xpos = 0
ypos = 0
zpos = 0

#sender = datasender.datasender("192.168.0.56")

def readFromSerial(ser, forever=False):
    while True:
        output = ser.read_until('\n',1000)
        print(output[:-1])
        if len(output) == 0 and not forever:
            print("Nothing more")
            break
    return

def getMovement(_command):
    command = _command[3:]
    separated = command.split()

    for item in separated:
        if item[:1] == 'F':
            speed = item[1:]
        elif item[:1] == 'X':
            x = item[1:]
        elif item[:1] == 'Y':
            y = item[1:]
        elif item[:1] == 'Z':
            z = item[1:]

    return 'MOVEMENT', x,y,z

def getNozzleTemp(_command):
    command = _command[5:]
    separated = command.split()

    for item in separated:
        if item[:1] == 'S':
            nozzle = item[1:]

    return 'NOZZLE_TEMP', nozzle

def getBedTemp(_command):
    command = _command[5:]
    separated = command.split()

    for item in separated:
        if item[:1] == 'S':
            bed = item[1:]

    return 'BED_TEMP', bed

def getInfo(command):
    if command[:2] == 'G0' or command[:2] == 'G1':
        return getMovement(command)
    elif command[:4] == 'M104' or command[:4] == 'M109':
        return getNozzleTemp(command)
    elif command[:4] == 'M140' or command[:4] == 'M190':
        return getNozzleTemp(command)
    elif command[:3] == 'G28':
        return 'MOVEMENT', 0, 0, 0
    else:
        return 'UNSUPPORTED_COMMAND'

def unpackCommand(command): 
    global bedTemp 
    global nozzleTemp
    global xpos
    global ypos
    global zpos
    
    commandResponse = getInfo(command)
    if commandResponse[0] == "NOZZLE_TEMP":
        nozzleTemp = commandResponse[1]
    elif commandResponse[0] == "BED_TEMP":
        bedTemp = commandResponse[1]
    elif commandResponse[0] == "MOVEMENT":
        xpos = commandResponse[1]
        ypos = commandResponse[2]
        zpos = commandResponse[3]

def sendCommand(ser, command):
    ret = ser.write(b"%s\n"%command)
    unpackCommand(command)
    #sender.sendData(command)
    return ret 

def print_file(filename, serial_port):
    with serial.Serial(serial_port) as ser:
        ser.baudrate = 115200
        ser.timeout = 5
        time.sleep(20)
        readFromSerial(ser)
        
        print("Writing")
        with open(filename,"r") as f:
            lines = f.readlines()
            
            for line in lines:
                if line[:-1] == ";End of Gcode":
                    print(line)
                    break
                if line[0] == ';' or line[0] == '\n':
                    print("Skipping: %s" % (line[:-1]))
                else:
                    print("Sending: %s" % (line[:-1]))
                    sendCommand(ser, line)
                    while True:
                        output = ser.read_until('\n',1000)
                        print(output[:-1])
                        #print(output[:2])
                        if output[:2] == 'ok':
                            print("OK found")
                            break
            print("DONE")   
            
        return
        
if __name__ == "__main__":
    todos = os.listdir(ROOT_DIR + TODO_DIR)
    print(todos)
    for todo in todos:
        print("Found %s to do" % todo)
        print(ROOT_DIR + TODO_DIR + "/" + todo)
        os.rename(ROOT_DIR + TODO_DIR + "/" + todo, ROOT_DIR + INPROGRESS_DIR + "/" + todo)
        #print("I would be printing %s" % todo)
        #time.sleep(5)
        print_file(ROOT_DIR + INPROGRESS_DIR + "/" + todo, '/dev/ttyUSB0')
        os.rename(ROOT_DIR + INPROGRESS_DIR + "/" + todo, ROOT_DIR + DONE_DIR + "/" + todo)
else:
    ser = serial.Serial('/dev/ttyUSB0')
    ser.baudrate = 115200
    ser.timeout = 5
    time.sleep(5)
    readFromSerial(ser)

