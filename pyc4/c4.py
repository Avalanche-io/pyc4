import hashlib

_CHARSET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
_BASE = 58
_LUT = {}
_LOWBYTE = u'1'
_PREFIX = "c4"
_IDLEN = 90

def _init():
  for i in range(len(_LUT)):
    _LUT[i] = 0xFF # 255

  i = 0
  for c in _CHARSET:
    _LUT[c] = i
    i += 1

def _bytesToLong(data):
  result = 0
  for b in data:
    result = result * 256 + ord(b)
  return result


def _longToBytes(data):
  encoded = []
  while data > 0:
    data, mod = divmod(data, 256)
    encoded.append(chr(mod))

  return ''.join(encoded[::-1])

def parse(src):
  if not _LUT:
    _init()

  if len(src) != 90:
    return (None, "is not 90 characters long")

  if src[:2] != u'c4':
    return (None, "does not begin with 'c4'")

  bigNum = 0

  for i in range(2,90):
    try:
      b = _LUT[src[i]]
    except:
      b = 0xFF

    if b == 0xFF:
      return (None, "invalid character at " + str(i))
    bigNum *= _BASE
    bigNum += b

  id = _longToBytes(bigNum)
  pad = []
  for i in range(0,64-len(id)):
    pad.append(chr(0))
  id = ''.join(pad) + id
  return (ID(id), None)

class ID:

  def __init__(self, value):
    self.value = [0]*64
    if len(value) == 64:
      self.value = value

  def string(self):
    bigNum = _bytesToLong(self.value)
    encoded = []
    for i in range(0, 90):
      encoded.append(_LOWBYTE)

    encoded[0] = 'c'
    encoded[1] = '4'

    for i in range(1, 89):
      if bigNum <= 0:
        break

      bigNum, bigMod = divmod(bigNum, _BASE)
      encoded[90-i] = _CHARSET[bigMod]
    return ''.join(encoded)

  def bytes(self):
    return self.value

  def less(self, other):
    if not other:
      return False
    return self.value < other.value

  def __eq__(self, other):
    return self.value == other.value

  def __ne__(self, other):
    if not other:
      return False
    return self.value != other.value

class Encoder:

  def __init__(self):
    self.h = hashlib.sha512()

  def write(self, data):
    self.h.update(data)

  def reset(self):
    self.h = hashlib.sha512()

  def id(self):
    return ID(self.h.digest())

def Identify(data):
  e = Encoder()
  e.write(data)
  return e.id()
