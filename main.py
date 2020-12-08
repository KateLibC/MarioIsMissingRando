#!/usr/bin/env python3

from romloader.cartridge import cartridge

from mim.verify import mimVerify, checkSeed
from mim.prng import prng
from mim.koopas import showKoopas
from mim.defund import displayMessage, defundSprites
from mim.credits import appendCredits
from mim.tools import inWriteROM as writeROM
from mim.tools import inLoadROM as loadROM
from mim.tools import headerROM

import sys
import argparse
import os

def loadApp():
    t = ['', 'Mario is Missing Randomizer', '', 
            '(c) 2020 Cariad Keigher <cariad@keigher.ca>', 
            'https://twitch.tv/KateLibC', '',
            'Licence is under GNU General Public License (GPL) 2.0:',
            'https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html', '',
            'All support problems should be through GitHub:',
            'https://github.com/KateLibC/MarioIsMissingRando', '']
    print('\n'.join(t))
    l = sorted([len(x) for x in t])[-1] * '='
    print(f'{l}\n')

def createArguments():
    margs = argparse.ArgumentParser()
    margs.add_argument('-i', dest='fileIn', help='Path for input ROM for patching. Must be unpatched.', required=True)
    margs.add_argument('-o', dest='fileOut', help='Output path for ROM. Any existing file will be overwritten.', required=True)
    margs.add_argument('--easy_mode', dest='easymode', 
        help='Enables a mode that flashes Koopas on an interval when they have items.', required=False,
        action='store_true', default=False)
    margs.add_argument('--seed', dest='seed', help='Use a custom seed value (format must be "00AF,AF00")', required=False)
    margs.add_argument('--undefund', dest='undefund', help='Re-enables a sprite that is removed by default. It is requested you do not use this.', 
        required=False, action='store_true', default=False)
    return margs

if __name__ == '__main__':
    loadApp()
    args = vars(createArguments().parse_args())
    c = loadROM(filename=args['fileIn'], loader=cartridge)
    c.parseHeader()
    headerROM(headers=c.romHeader, checksum=c.romHash)
    m = mimVerify(romHeader=c.romHeader, hashValue=c.romHash, romBytes=c.romBytes)
    pv = m.prngROM()
    p = prng(romBytes=c.romBytes, firstAddress=pv[0], secondAddress=pv[1])
    p.showSeed = m.prngSeedROM()
    if args['seed'] is None:
        p.generateSeeds()
        s1 = ''.join([str(hex(x)).replace('0x','') for x in p.firstSeed]).zfill(4)
        s2 = ''.join([str(hex(x)).replace('0x','') for x in p.secondSeed]).zfill(4)
        print(f'Auto-generated seed with value: {s1},{s2}\n')
    else:
        if checkSeed(seed=args['seed']):
            print(f'Setting seed to value: {args["seed"]}\n')
            p.setSeed(seed=args['seed'])
        else:
            raise Exception('Seed value is not in correct format. Expected format is something like "0F1A,98AA".')
    p.writeSeeds()
    if args['easymode']:
        print('Enabling "easy mode". Koopas will flash as you view them on the map or GPS.')
        kv = m.koopaROM()
        p.romBytes = showKoopas(romBytes=p.romBytes, startAddr=kv[0], lastAddr=kv[1])
    if args['undefund']:
        displayMessage()
    else:
        p.romBytes = defundSprites(romBytes=p.romBytes, addresses=m.defundROM())
    print('\nFinalizing everything...')
    cv = m.creditsROM()
    p.romBytes = appendCredits(romBytes=p.romBytes, startAddr=cv[0], lastAddr=cv[1])
    writeROM(filename=args['fileOut'], romBytes=p.romBytes, loader=cartridge)
    quit()