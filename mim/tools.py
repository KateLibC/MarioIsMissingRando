def readROM(romBytes, address, length=2):
    return romBytes[address], romBytes[address + 1]

def writeROM(romBytes, address, value):
    romBytes[address] = value
    return romBytes