from .tools import readROM, writeROM

'''
Just patches the credits. It's really crude the way I wrote this
but I don't really care to spend the time to figure out how the 
game reads this and spits out the text.
'''

credits = [
    [0x04, ' RANDO MADE BY ', '', '   KATELIBC   ', '  A K A CARIAD  '],
    [0x04, ' THANKS  ', '   TO   ', '', 'MACHINEGUNSALLY'],
    [0x03, '  TINA AUTH ', '', ' GREN   EON '],
    [0x08, 'REMARKS', '', ' WRITTEN ON ', 'UNCEDED LAND', ' OF THE COAST ', '  SALISH  ', '  PEOPLE   ', '           '],
    [0x07, 'MORE   REMARKS', '', '   BLACK  ', '  LIVES  ', '   MATTER    ', ' TRANS RIGHTS ', ' LAND BACK '],
    [0x03, '  YOSHI IS A  ', '', '    HORSE    '],
    [0x04, 'HORSES  LAY', '  EGGS  ', '', '  IT IS TRUE  '],
    [0x04, '   MORE THANKS   ', '', '  DAPHNE  ', ' MEOW MEOW '],
    [0x01, 'THE END']
    ]

def createCredits(credits, mode=None):
    i = []
    for credit in credits:
        v = '\xFF'.join([x for x in credit[1:]])
        if mode is not None:
            c = len(v.split())
        else:
            c = credit[0]
        credit = chr(c) + v
        i += [x for x in credit]
        i.append('\x00')
    if len(i) > 400:
        i = i[:400]
    elif len(i) < 400:
        while len(i) < 400:
            i.append('A')
    i = [ord(x) for x in i]
    return bytes(i)

def appendCredits(romBytes, startAddr, lastAddr):
    romCode = romBytes[startAddr:lastAddr]
    c = createCredits(credits=credits)
    for x in range(0, len(romCode)):
        b = c[x]
        romBytes = writeROM(romBytes=romBytes, address=startAddr + x, value=b)
    return romBytes