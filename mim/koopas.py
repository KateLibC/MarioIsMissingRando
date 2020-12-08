from .tools import readROM, writeROM

'''
Patches the power-on PRNG to get rid of unused code and 
then rearranges it so the debug code is automatically 
enabled
'''

def showKoopas(romBytes, startAddr, lastAddr):
    patchCode = [0xA9, 0x01, 0x00, 0x8D, 0x8D, 0x05]
    romCode = romBytes[startAddr:lastAddr]
    initLowCode = romCode[:6]
    initHighCode = romCode[9:15]
    newCode = initLowCode + initHighCode + bytes(patchCode)
    for x in range(0, len(newCode)):
        b = newCode[x]
        romBytes = writeROM(romBytes=romBytes, address=startAddr + x, value=b)
    return romBytes