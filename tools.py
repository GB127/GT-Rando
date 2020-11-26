def read_big(data, offset):
    low = data[offset]
    high = data[offset +1]
    return high * 16 *16 + low

def write_big(data, offset, value):
    low = value & 0xFF
    high = (value & 0xFF00) // 16 // 16
    data[offset] = low
    data[offset +1] = high
