import base64
from time import sleep

from .tools import readROM, writeROM

'''
This removes a problematic sprite that should not exist 
in this game. This is never to be removed and no pull 
requests changing such will be accepted.

It's written in a Base64-encoded string just to prevent 
chuds from going through Github looking for such things.
'''

msg = 'SGVsbG8uCgpJZiB5b3UncmUgc2VlaW5nIHRoaXMgbWVzc2FnZSwgeW91J3ZlIG9wdGVkIHRvIApyZS1lbmFibGUgdGhlIHZpc2liaWxpdHkgb2YgcG9saWNlIHNwcml0ZXMgaW4gCnRoaXMgZ2FtZS4KClNob3VsZCB5b3UgaGF2ZSBhIHByb2JsZW0gd2l0aCB0aGlzIGJlaW5nIGEgCmRlZmF1bHQgaW4gdGhpcyB0b29sLCBpdCBpcyBsaWtlbHkgeW91J3JlIHRoZSAKdHlwZSB0aGF0IGdvZXMgb24gYWJvdXQgInBvbGl0aWNzIGhhdmluZyBubyAKcGxhY2UgaW4gdmlkZW8gZ2FtZXMiLiBJbiBhbiBpZGVhbCB3b3JsZCwgeWVzLCAKcG9saXRpY3Mgd291bGQgbm90IGJlIGluIG91ciB2aWRlbyBnYW1lcywgYnV0IAp0aGlzIHdvcmxkIGlzIG5vdCBpZGVhbCwgYW5kIGl0J3MgbGlrZWx5IHRoYXQgCnlvdXIgaWRlYWxzIGNvbWUgZnJvbSBhIHBsYWNlIG9mIHByaXZpbGVnZS4KCkRvZXMgdGhhdCBzdGF0ZW1lbnQgZ2V0IHVuZGVyIHlvdXIgc2tpbj8KClBvbGljZSBoYXZlIG11cmRlcmVkIG51bWVyb3VzIGJsYWNrIHBlcnNvbnMsIApwZXJzb25zIG9mIGNvbG91ciwgaW5kaWdlbm91cyBwZXJzb25zLCBhbmQgCnRyYW5zIHBlcnNvbnMgbm90IGJlY2F1c2UgdGhleSBkaWQgYW55dGhpbmcgCndyb25nIGJ1dCBiZWNhdXNlIG9mIHdobyB0aGV5IGFyZS4gVGhlIApwcm90ZXN0aW5nIHlvdSBzZWUgb24gdGhlIHN0cmVldHMgaXMgYW4gCmV4cHJlc3Npb24gb2YgdGhlIGZydXN0cmF0aW9uIG1hcmdpbmFsaXplZCAKcGVyc29ucyBmYWNlIGJlY2F1c2Ugb2YgYSBzeXN0ZW0gaW50ZW5kZWQgCnRvIG9wcHJlc3MgdGhlbS4KCllvdSBsaWtlbHkgZG9uJ3Qgc2VlIHRoaW5ncyB0aGF0IHdheSBiZWNhdXNlIAp0aGUgc3lzdGVtIGlzIHdvcmtpbmcgZm9yIHlvdS4gWW91IGFyZSBub3QgCmFsbG93ZWQgdG8gcGljayBhbmQgY2hvb3NlIHdoYXQgb3BwcmVzc2VkIApwZW9wbGUgY2FuIGNvbXBsYWluIGFib3V0LgoKQmxhY2sgTGl2ZXMgTWF0dGVyCkluZGlnZW5vdXMgTGl2ZXMgTWF0dGVyCgpHb2luZyBpbnRvIEdpdEh1YiBhbmQgY29tcGxhaW5pbmcgYWJvdXQgdGhpcyAKd2lsbCBub3QgZ2V0IHRoaXMgbWVzc2FnZSByZW1vdmVkLiBZb3Ugd2lsbCAKbm90IGdldCBhIGZyaWVuZGx5IHJlc3BvbnNlIGZyb20gbWUgYW5kIGl0IGlzIApsaWtlbHkgSSdsbCBtYWtlIGFuIGV4YW1wbGUgb2YgeW91IGVsc2V3aGVyZS4KClRoaXMgbWVzc2FnZSB3aWxsIHJlbWFpbiBkaXNwbGF5ZWQgZm9yIDIwCnNlY29uZHMsIGJ1dCBhcyB5b3UgaGF2ZSByZXF1ZXN0ZWQsIHRoZSAKc3ByaXRlcyB3aWxsIG5vdCBiZSBkaXNhYmxlZC4KClAuUy4gLSBJZiB5b3Ugd2FudGVkIHRoZW0gYmFjayB0byByZXNvbHZlIGEgCmJ1ZywgcGxlYXNlIGxldCBtZSBrbm93IGFuZCBJJ2xsIGZpeCB0aGUgYnVnLg=='

def displayMessage():
    m = base64.b64decode(msg)
    t = ['\n', '='*54, m.decode('utf-8'), '='*54, '\n']
    print('\n'.join(t))
    sleep(20)

def defundSprites(romBytes, addresses):
    for address in addresses:
        a = address['a']
        r = address['r']
        p = romBytes[a:a+8]
        if r is None:
            p = [0x0 for x in range(0, len(p))]
        p = bytes(p)
        for x in range(0, len(p)):
            b = p[x]
            writeROM(romBytes=romBytes, address=a + x, value=b)
    return romBytes