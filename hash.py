import hashlib
import array
import struct

charset = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

base = 58
lut = [0] * 256
# print len(lut)  # .length()
lowbyte = '1'
prefix = "c4"
idlen = 90


m = hashlib.sha512()
m.update(u'foo')
digest = m.digest()

# for i in range(0, 64):
#   print ord(digest[i])

def bytes_to_long(bytes):
    result = 0

    for b in bytes:
        result = result * 256 + ord(b)

    return result


bigNum = bytes_to_long(digest)

# divmod(x, y)

encoded = []
for i in range(0,90):
  encoded.append(lowbyte)

encoded[0] = 'c'
encoded[1] = '4'

# print encoded

# print "bigNum: ", bigNum

for i in range(1, 89):
  if bigNum <= 0:
    break

  bigNum, bigMod = divmod(bigNum, base)
  # print "bigMod: ", bigMod
  encoded[90-i] = charset[bigMod]


print ''.join(encoded)

