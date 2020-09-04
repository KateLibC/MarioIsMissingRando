from .tools import readROM, writeROM

import secrets

class prng(object):
    def __init__(self, romBytes, firstAddress, secondAddress):
        self.firstAddress = firstAddress
        self.secondAddress = secondAddress
        self.romBytes = romBytes
        self.firstSeed = None
        self.secondSeed = None

    def generateSeed(self):
        return secrets.choice(range(0,255)), secrets.choice(range(0,255))

    def generateSeeds(self):
        self.firstSeed = self.generateSeed()
        self.secondSeed = self.generateSeed()

    def writeSeeds(self):
        if None in [self.firstSeed, self.secondSeed]:
            self.generateSeeds()
        for address, seed in [(self.firstAddress, self.firstSeed), (self.secondAddress, self.secondSeed)]:
            i = 0
            for v in seed:
                self.romBytes = writeROM(romBytes=self.romBytes, address=address + i, value=v)
                i += 1