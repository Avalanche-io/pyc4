import hashlib

_CHARSET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
_BASE = 58
_LUT = {}
_LOWBYTE = u'1'
_PREFIX = "c4"
_IDLEN = 90


def _init():
    for i in range(len(_LUT)):
        _LUT[i] = 0xFF  # 255

    i = 0
    for c in _CHARSET:
        _LUT[c] = i
        i += 1


def _bytes_to_long(data):
    result = 0
    for b in data:
        result = result * 256 + ord(b)
    return result


def _long_to_bytes(data):
    encoded = []
    while data > 0:
        data, mod = divmod(data, 256)
        encoded.append(chr(mod))

    return ''.join(encoded[::-1])


def parse(src):
    if not _LUT:
        _init()

    if len(src) != 90:
        return None, "is not 90 characters long"

    if src[:2] != u'c4':
        return None, "does not begin with 'c4'"

    big_num = 0

    for i in range(2, 90):
        try:
            b = _LUT[src[i]]
        except:
            b = 0xFF

        if b == 0xFF:
            return None, "invalid character at " + str(i)
        big_num *= _BASE
        big_num += b

    c_id = _long_to_bytes(big_num)
    pad = []
    for i in range(0, 64-len(c_id)):
        pad.append(chr(0))
    c_id = ''.join(pad) + c_id

    return ID(c_id), None


class ID(object):

    def __init__(self, value):
        self.value = [0]*64
        if len(value) == 64:
            self.value = value

    def string(self):
        big_num = _bytes_to_long(self.value)
        encoded = []
        for i in range(0, 90):
            encoded.append(_LOWBYTE)

        encoded[0] = 'c'
        encoded[1] = '4'

        for i in range(1, 89):
            if big_num <= 0:
                break

            big_num, big_mod = divmod(big_num, _BASE)
            encoded[90-i] = _CHARSET[big_mod]
        return ''.join(encoded)

    def __str__(self):
        return self.string()

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


class Encoder(object):

    def __init__(self):
        self.h = hashlib.sha512()

    def write(self, data):
        self.h.update(data)

    def reset(self):
        self.h = hashlib.sha512()

    def id(self):
        return ID(self.h.digest())


def identify(data):
    e = Encoder()
    e.write(data)
    return e.id()


def c4_from_file_path(file_path, byte_count=None):
    """
    Example on how to use the hashing function.
    If no byte_count is given then it will default to 65536
    :param file_path: String - Path to File to Hash
    :param byte_count: Int - Amount of bytes to process at a time
    :return: String - c4 Hash value of file
    """
    if byte_count is None:
        byte_count = 65536

    encode_c4 = Encoder()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            encode_c4.write(data)

    return encode_c4.id()


