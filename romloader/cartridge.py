from .extras import hashValue, get_two_bytes_little_endian as twoByteEndian

class cartridge(object):
    def __init__(self, romFile, romBytes=None):
        self.makeupROMMap = {
                                32: 'LoROM', 33: 'HiROM', 35: 'SA-1ROM', 48: 'LoROM/FastROM',
                                49: 'HiROM/FastROM', 50: 'ExLoROM', 53: 'ExHiROM'
                            }
        self.typeROMMap = {
                            0: 'ROM only', 1: 'ROM+RAM', 2: 'ROM+RAM+SRAM',
                            3: 'ROM+DSP', 4: 'ROM+RAM+DSP', 5: 'ROM+RAM+SRAM+DSP',
                            6: 'ROM+SRAM+DSP', 19: 'ROM+SuperFX', 20: 'ROM+RAM+SuperFX', 
                            21: 'ROM+RAM+SRAM+SuperFX', 22: 'ROM+SRAM+SuperFX', 
                            35: 'ROM+OBC1', 36: 'ROM+RAM+OBC1', 37: 'ROM+RAM+SRAM+OBC1', 
                            38: 'ROM+SRAM+OBC1', 51: 'ROM+SA-1', 52: 'ROM+RAM+SA-1', 
                            53: 'ROM+RAM+SRAM+SA-1', 54: 'ROM+SRAM+SA-1', 227:'ROM+OTHER', 
                            228:'ROM+RAM+OTHER', 229:'ROM+RAM+SRAM+OTHER', 
                            230:'ROM+SRAM+OTHER', 243: 'ROM+CUSTOM CHIP', 244: 'ROM+RAM+CUSTOM CHIP',
                            245: 'ROM+RAM+SRAM+CUSTOM CHIP', 246: 'ROM+SRAM+CUSTOM CHIP'
                          }
        self.rom_size_map = {9: '3~4MBit', 10: '5~8MBit', 11: '9~16MBit', 12: '17~32MBit', 13: '33~64MBit'}
        self.LO_ROM_HEADER = '007FC0'
        self.HI_ROM_HEADER = '00FFC0'
        if romBytes is None:
            self.romHash = hashValue(fileName=romFile)
        self.romFile = romFile
        if romBytes is None:
            self.loadROM()
        else:
            self.romBytes = romBytes
            self.readROM()

    '''
    Loads the ROM into a byte array
    '''
    def loadROM(self):
        with open(self.romFile, 'rb') as f:
            self.romBytes = bytearray(f.read())
        self.readROM()

    '''
    Gets details about the ROM by reading the array
    '''
    def readROM(self):
        self.romSize = len(self.romBytes)
        self.hasSCM = self.romSize % 1024 is not 0
        a = 0
        if self.hasSCM:
            a = 512
        s = 0
        while a < self.romSize:
            s += self.romBytes[a]
            a += 1
        self.checksumExpected = hex(s & int('FFFF', 16))

    '''
    Writes the ROM from the byte array
    '''
    def writeROM(self, fileName):
        with open(fileName, 'wb') as f:
            f.write(self.romBytes)

    '''
    Parses the header to give context to the ROM
    '''
    def parseHeader(self):
        startAddr = self.locateHeaderStart()
        self.romHeader = {'name': self.romBytes[startAddr:startAddr + 21].decode()}
        h = {
            'makeup': startAddr + 21, 'romType': startAddr + 22,
            'romSize': startAddr + 23, 'sramSize': startAddr + 24,
            'version': startAddr + 27
        }
        for k, v in h.items():
            self.romHeader[k] = self.romBytes[v]
        self.romHeader['licenceCode'] = twoByteEndian(self.romBytes[startAddr + 25], self.romBytes[startAddr + 26])
        self.romHeader['checksumCompliment'] = twoByteEndian(self.romBytes[startAddr + 28], self.romBytes[startAddr + 29])
        self.romHeader['checksum'] = twoByteEndian(self.romBytes[startAddr + 30], self.romBytes[startAddr + 31])
        self.romHeader['interupts'] = self.locateHeaderInterrupts(startAddr=startAddr)

    '''
    Locates the header in ROM and returns None if no header found
    '''
    def locateHeaderStart(self):
        def doesHeaderMatch(address):
            if self.hasSCM:
                address += 512
            cs1 = hex(self.romBytes[address + 30])[2:]
            cs1 = (2 - len(cs1)) * "0" + cs1
            cs2 = hex(self.romBytes[address + 31])[2:]
            cs2 = (2 - len(cs2)) * "0" + cs2
            checksum = cs2 + cs1
            csc1 = hex(self.romBytes[address + 28])[2:]
            csc1 = (2 - len(csc1)) * "0" + csc1
            csc2 = hex(self.romBytes[address + 29])[2:]
            csc2 = (2 - len(csc2)) * "0" + csc2
            checksumCompliment = csc2 + csc1
            return (int(checksum, 16) + int(checksumCompliment, 16) == 65535)
        for a in [int(self.LO_ROM_HEADER, 16), int(self.HI_ROM_HEADER, 16)]:
            if doesHeaderMatch(address=a):
                if self.hasSCM:
                    return a + 512
                return a
        return None

    '''
    Parses the ROM header to determine the memory values for the console interrupts
    '''
    def locateHeaderInterrupts(self, startAddr):
        def returnBytes(values):
            v1, v2 = values
            return twoByteEndian(self.romBytes[startAddr + v1], self.romBytes[startAddr + v2])
        i = {
            'native_cop_int_addr': (38, 39), 'native_brk_int_addr': (40, 41), 'native_abort_int_addr': (42, 43),
            'native_reset_int_addr': (44, 45), 'native_reset_int_addr': (46, 47),
            'cop_int_addr': (54, 55), 'abort_int_addr': (56, 57), 'nmi_int_addr': (58, 59),
            'reset_int_addr': (60, 61), 'irq_int_addr': (62, 63),
        }
        o = {}
        for k, v in i.items():
            o[k] = returnBytes(values=v)
        return o

    '''
    Returns cartridge type
    '''
    def cartridgeType(self):
        m = self.romHeader['makeup']
        if m in self.makeupROMMap.keys():
            return self.makeupROMMap[m]
        return None