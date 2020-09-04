from hashlib import md5

def get_two_bytes_little_endian(byte0, byte1):
    b0 = hex(byte0)[2:]
    b0 = (2 - len(b0)) * "0" + b0
    b1 = hex(byte1)[2:]
    b1 = (2 - len(b1)) * "0" + b1
    return  int(b1 + b0, 16)

def hashValue(fileName):
    with open(fileName, 'rb') as f:
        m = md5()
        while True:
            c = f.read(512)
            if not c:
                break
            m.update(c)
        return m.hexdigest()