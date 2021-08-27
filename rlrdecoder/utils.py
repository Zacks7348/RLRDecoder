from bitstring import ConstBitStream
import math

class Size:
    BOOL = 'bool'
    BYTE = 8
    INT8_LE = 'intle:8'
    INT8_BE = 'intbe:8'
    INT32_LE = 'intle:32'
    UINT32_LE = 'uintle:32'
    INT64_LE = 'intle:64'
    UINT64_LE = 'uintle:64'
    FLOAT32_LE = 'floatle:32'

def read_str(bitstream: ConstBitStream):
    size = bitstream.read(Size.INT32_LE)
    if size < 0:
        size *= -2
        str_bytes = bitstream.read('bytes:{}'.format(size))
        # Last 2 bytes should be null characters
        return str_bytes[:-2].decode('utf-16')
    str_bytes = bitstream.read('bytes:{}'.format(size))
    # Last byte should be null character
    return str_bytes[:-1].decode('windows-1252')
