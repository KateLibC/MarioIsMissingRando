from .tools import readROM, writeROM

import secrets

class prng(object):
    def __init__(self, romBytes, firstAddress, secondAddress):
        self.firstAddress = firstAddress
        self.secondAddress = secondAddress
        self.romBytes = romBytes
        self.firstSeed = None
        self.secondSeed = None
        self.showSeed = None

    def generateSeed(self):
        return secrets.choice(range(0,255)), secrets.choice(range(0,255))

    def generateSeeds(self):
        self.firstSeed = self.generateSeed()
        self.secondSeed = self.generateSeed()

    def setSeed(self, seed):
        seeds = seed.split(',')
        s1 = seeds[0][:2], seeds[0][2:]
        s2 = seeds[1][:2], seeds[1][2:]
        s1 = [int(x, 16) for x in s1]
        s2 = [int(x, 16) for x in s2]
        self.firstSeed = s1
        self.secondSeed = s2

    def displaySeed(self, startAddr, lastAddr):
        v1 = ''.join([str(hex(x)).replace('0x', '') for x in self.firstSeed]).upper().zfill(4)
        v2 = ''.join([str(hex(x)).replace('0x', '') for x in self.secondSeed]).upper().zfill(4)
        seed = f'SEED VALUE {v1} {v2}'.encode('ascii')
        seed = bytes(seed)
        for x in range(0, len(seed)):
            b = seed[x]
            self.romBytes = writeROM(romBytes=self.romBytes, address=startAddr + x, value=b)

    def writeSeeds(self):
        if None in [self.firstSeed, self.secondSeed]:
            self.generateSeeds()
        for address, seed in [(self.firstAddress, self.firstSeed), (self.secondAddress, self.secondSeed)]:
            i = 0
            for v in seed:
                self.romBytes = writeROM(romBytes=self.romBytes, address=address + i, value=v)
                i += 1
        if self.showSeed is not None:
            self.displaySeed(startAddr=self.showSeed[0], lastAddr=self.showSeed[1])