#!/usr/bin/env python3

from romloader.cartridge import cartridge

from mim.verify import mimVerify
from mim.prng import prng

import sys

if __name__ == '__main__':
    fileIn = sys.argv[1]
    fileOut = sys.argv[2]
    print(f'Original: {fileIn}\nOutput: {fileOut}\n')
    cIn = cartridge(romFile=fileIn)
    cIn.parseHeader()
    print(f'Game title: {cIn.romHeader["name"]}\nVersion: {cIn.romHeader["version"]}\nChecksum: {cIn.checksumExpected}\n')
    m = mimVerify(romHeader=cIn.romHeader, hashValue=cIn.romHash, romBytes=cIn.romBytes)
    pv = m.prngROM()
    p = prng(romBytes=cIn.romBytes, firstAddress=pv[0], secondAddress=pv[1])
    p.generateSeeds()
    print('Seeds: {},{}'.format(''.join([str(hex(x)).replace('0x','') for x in p.firstSeed]).zfill(4), ''.join([str(hex(x)).replace('0x','') for x in p.secondSeed]).zfill(4)))
    p.writeSeeds()
    cOut = cartridge(romFile=None, romBytes=p.romBytes)
    cOut.writeROM(fileName=fileOut)
    print('\nWritten to disk.')