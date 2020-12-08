import os

def readROM(romBytes, address, length=2):
    return romBytes[address], romBytes[address + 1]

def writeROM(romBytes, address, value):
    romBytes[address] = value
    return romBytes

def inWriteROM(filename, romBytes, loader):
    if os.path.exists(filename):
        print(f'Warning: {filename} exists and will be overwritten.')
    c = loader(romFile=None, romBytes=romBytes)
    c.writeROM(fileName=filename)
    print(f'Created new file: {filename}')

def inLoadROM(filename, loader):
    if os.path.exists(filename):
        print(f'Loading ROM: {filename}')
        return loader(romFile=filename)
    else:
        raise Exception(f'Filename not found: {filename}')

def headerROM(headers, checksum):
    i = {'Game title': 'name', 'Version': 'version'}
    o = []
    for hv, kv in i.items():
        if kv in headers.keys():
            s = f'{hv}:\t{headers[kv]}'
            o.append(s)
    o.append(f'MD5:\t\t{checksum}')
    o = '\n' + '\n'.join(o) + '\n'
    print(o)

# Code borrowed from Zoinkity
# https://www.romhacking.net/forum/index.php?topic=24436.0
'''
with open("decompressed_data.bin", 'rb') as f:
    dec = f.read()
    o = encode(dec)
    # Decode it to check the file against the original.
    print(decode(o) == dec)
    with open("output.bin", 'wb') as f:
        f.write(o)
'''

def decode(data):
    if not data[0]:
        return data
    # Be lasy and just assemble bytes.
    sz = (data[2] << 8) | data[1]
    d = iter(data[3:])
    c = 1
    out = bytearray()
    while len(out) < sz:
        if c == 1:
            # Refill.
            c = 0x10000 | next(d) | (next(d) << 8)
        if c & 1:
            p = next(d) | (next(d) << 8)
            l = (p >> 11) + 3
            p &= 0x7FF
            p += 1
            for i in range(l):
                out.append(out[-p])
        else:
            out.append(next(d))
        c >>= 1
    return bytes(out)

def _search(data, pos, sz):
    ml = min(0x22, sz - pos)
    if ml < 3:
        return 0, 0
    mp = max(0, pos - 0x800)
    hitp, hitl = 0, 3
    if mp < pos:
        hl = data[mp:pos+hitl].find(data[pos:pos+hitl])
        while hl < (pos - mp):
            while (hitl < ml) and (data[pos + hitl] == data[mp + hl + hitl]):
                hitl += 1
            mp += hl
            hitp = mp
            if hitl == ml:
                return hitp, hitl
            mp += 1
            hitl += 1
            if mp >= pos:
                break
            hl = data[mp:pos+hitl].find(data[pos:pos+hitl])
    # If length less than 4, return miss.
    if hitl < 4:
        hitl = 1
    return hitp, hitl-1

def encode(data):
    """"""
    from struct import Struct
    HW = Struct("<H")

    cap = 0x22
    sz = len(data)
    out = bytearray(b'\x01')
    out.extend(HW.pack(sz))
    c, cmds = 0, 3
    pos, flag = 0, 1
    out.append(0)
    out.append(0)
    while pos < sz:
        hitp, hitl = _search(data, pos, sz)
        if hitl < 3:
            # Push a raw if copying isn't possible.
            out.append(data[pos])
            pos += 1
        else:
            tstp, tstl = _search(data, pos+1, sz)
            if (hitl + 1) < tstl:
                out.append(data[pos])
                pos += 1
                flag <<= 1
                if flag & 0x10000:
                    HW.pack_into(out, cmds, c)
                    c, flag = 0, 1
                    cmds = len(out)
                    out.append(0)
                    out.append(0)
                hitl = tstl
                hitp = tstp
            c |= flag
            e = pos - hitp - 1
            pos += hitl
            hitl -= 3
            e |= hitl << 11
            out.extend(HW.pack(e))
        # Advance the flag and refill if required.
        flag <<= 1
        if flag & 0x10000:
            HW.pack_into(out, cmds, c)
            c, flag = 0, 1
            cmds = len(out)
            out.append(0)
            out.append(0)
    # If no cmds in final word, del it.
    if flag == 1:
        del out[-2:]
    else:
        HW.pack_into(out, cmds, c)
    return bytes(out)