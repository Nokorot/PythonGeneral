from Crypto.PublicKey import RSA

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

def generate(size=1024):
    private_key = RSA.generate(size)
    public_key = private_key.publickey()
    return toMyBase( private_key.exportKey() ), toMyBase( public_key.exportKey() )

def getPublicKey(private_key):
    key = RSA.importKey( fromMyBase(private_key) )
    return toMyBase( key.getPublicKey().exportKey() )

def exportKey(filename, key):
    with open(filename + ".bin", "w") as f:
        f.write(key)

def importKey(filename):
    with open(filename + ".bin", "r") as f:
        return f.read()

def encrypt(data, public_key):
    key = RSA.importKey( fromMyBase(public_key) )
    code = key.encrypt(data.encode('utf-8'), 'x')
    return toMyBase(code[0])

def decrypt(data, private_key):
    key = RSA.importKey( fromMyBase(private_key) )
    code = fromMyBase(data)
    return key.decrypt(code)

if __name__ == '__main__':
    #private, public = generateRSA('data/RSAKey', 1024)
    public = importRSA('data/RSAKey-public')
    private = importRSA('data/RSAKey-private')

    massage = encrypt("Hey, how are you", public)

    print massage

    print str(decrypt(massage, private))
