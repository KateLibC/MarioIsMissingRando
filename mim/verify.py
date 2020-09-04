from .tools import readROM

class mimVerify(object):
    def __init__(self, romHeader, hashValue, romBytes):
        self.romHeader = romHeader
        self.hashValue = hashValue
        self.romBytes = romBytes
        self.expectedHashes = {
            'd5217f2137a4f4df63d83264a9a92bcc': {
                'Region': 'EU',
                'PRNG': {0: 0x034D, 1: 0x0356},
                },
            '2a2152976e503eaacd9815f44c262d73': {
                'Region': 'NA',
                'PRNG': {0: 0x034D, 1: 0x0356},
                },
        }
        self.romDetails = self.typeROM()

    def checkROM(self):
        return self.hashValue in self.expectedHashes.keys()

    def typeROM(self):
        return self.expectedHashes[self.hashValue]

    def prngROM(self):
        return self.typeROM()['PRNG']

    def regionROM(self):
        return self.typeROM()['Region']

    def readROM(self, address, length=2):
        return self.romBytes[address], self.romBytes[address + 1]

    def validHash(self):
        return self.hashValue in self.expectedHashes.keys()

    def prngSeedValues(self):
        p = self.prngROM()
        return self.readROM(address=p[0]), self.readROM(address=p[1])