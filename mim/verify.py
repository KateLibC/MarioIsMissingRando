from .tools import readROM

'''
Verifies aspects of the Mario is Missing ROM. We can make easier 
patches should there be other versions, etc
'''
class mimVerify(object):
    def __init__(self, romHeader, hashValue, romBytes):
        self.romHeader = romHeader
        self.hashValue = hashValue
        self.romBytes = romBytes
        self.expectedHashes = {
            'd5217f2137a4f4df63d83264a9a92bcc': {
                'Region': 'EU',
                'PRNG': {0: 0x034D, 1: 0x0356},
                'KoopaPatch': {0: 0x034C, 1: 0x035E},
                'Credits': {0: 0x789F, 1: 0x7A2F},
                'SeedPlacement': {0: 0x53B5, 1: 0x53C9},
                'SpriteReplacement': [ {'a': 0xE1EC, 'r': None}, {'a': 0xE1F0, 'r': None}],
            },
            '2a2152976e503eaacd9815f44c262d73': {
                'Region': 'NA',
                'PRNG': {0: 0x034D, 1: 0x0356},
                'KoopaPatch': {0: 0x034C, 1: 0x035E},
                'Credits': {0: 0x789F, 1: 0x7A2F},
                'SeedPlacement': {0: 0x53B5, 1: 0x53C9},
                'SpriteReplacement': [ {'a': 0xE1EC, 'r': None}, {'a': 0xE1F0, 'r': None}],
            },
        }
        self.romDetails = self.typeROM()

    def checkROM(self):
        return self.hashValue in self.expectedHashes.keys()

    def typeROM(self):
        return self.expectedHashes[self.hashValue]

    '''
    Returns specific memory locations
    '''

    def creditsROM(self):
        return self.typeROM()['Credits']

    def defundROM(self):
        return self.typeROM()['SpriteReplacement']

    def koopaROM(self):
        return self.typeROM()['KoopaPatch']

    def prngROM(self):
        return self.typeROM()['PRNG']

    def prngSeedROM(self):
        return self.typeROM()['SeedPlacement']

    def regionROM(self):
        return self.typeROM()['Region']

    def readROM(self, address, length=2):
        return self.romBytes[address], self.romBytes[address + 1]

    def validHash(self):
        return self.hashValue in self.expectedHashes.keys()

    def prngSeedValues(self):
        p = self.prngROM()
        return self.readROM(address=p[0]), self.readROM(address=p[1])

# Really poorly written seed check
def checkSeed(seed):
    def checkValue(s):
        s = s.upper()
        # Seeds must be [0-9A-F] and cannot be '0000' in each place
        return False not in [x in 'ABCDEF0123456789' for x in s] and s != '0000'
    seed = seed.split(',')
    o = len(seed) == 2
    # If there are two values in the seed
    if o:
        o = False not in [len(x) == 4 for x in seed]
    # If the two values are the correct length
    if o:
        o = False not in [checkValue(x) for x in seed]
    return o