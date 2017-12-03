from Crypto.PublicKey import RSA

generate = RSA.generate

MyBase = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-.'#,:;?()#!$<>'
def toMyBase(hx):
    n = 6
    hx = bin(int(hx.encode('hex'), 16))[2:]
    hx = '0'*((n-(len(hx)%n))%n) + hx
    ele = [int(hx[i:i+n], 2) for i in range(0, len(hx), n)]
    return ''.join([MyBase[i] for i in ele])

def fromMyBase(hx):
    base = 1
    value = 0
    for i in range(len(hx)):
        value += MyBase.index(hx[-i-1]) * base
        base *= len(MyBase)
    return hex(value)[2:-1].decode('hex')

def generateRSA(filename, size=1024):
    private_key = RSA.generate(size)
    public_key = private_key.publickey()
    exportRSA(filename + '-private', private_key)
    exportRSA(filename + '-public', public_key)
    return private_key, public_key

def writeKey(filename, key):
    with open(filename + ".bin", "wb") as f:
        f.write(key)

def readKey(filename):
    with open(filename + ".bin", "rb") as f:
        return f.read()

def exportRSA(filename, key):
    writeKey(filename, key.exportKey())

def importRSA(filename):
    return RSA.importKey(readKey(filename))

def importFromString(string):
    return RSA.importKey(string)

def encrypt(data, public_key):
    code = public_key.encrypt(data.encode('utf-8'), 'x')
    return toMyBase(code[0])

def decrypt(data, private_key):
    code = fromMyBase(data)
    return private_key.decrypt(code)

if __name__ == '__main__':
    #private, public = generateRSA('data/RSAKey', 1024)
    public = importRSA('data/RSAKey-public')
    private = importRSA('data/RSAKey-private')

    massage = encrypt("Hey, how are you", public)

    print massage

    print str(decrypt(massage, private))
