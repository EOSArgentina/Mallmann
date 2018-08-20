def pack_bool(ds, v):
  ds.write(b'\x00') if v else ds.add(b'\x01')
def unpack_bool(ds):
  return True if ds.read(1) else False

def pack_int8(ds, v):
  ds.write(struct.pack("<b", v))
def unpack_int8(ds):
  return struct.unpack("<b", ds.read(1))[0]

def pack_uint8(ds, v):
  ds.write(struct.pack("<B", v))
def unpack_uint8(ds):
  return struct.unpack("<B", ds.read(1))[0]

def pack_int16(ds, v):
  ds.write(struct.pack("<h", v))
def unpack_int16(ds):
  return struct.unpack("<h", ds.read(2))[0]

def pack_uint16(ds, v):
  ds.write(struct.pack("<H", v))
def unpack_uint16(ds):
  return struct.unpack("<H", ds.read(2))[0]

def pack_int32(ds, v):
  ds.write(struct.pack("<i", v))
def unpack_int32(ds):
  return struct.unpack("<i", ds.read(4))[0]

def pack_uint32(ds, v):
  ds.write(struct.pack("<I", v))
def unpack_uint32(ds):
  return struct.unpack("<I", ds.read(4))[0]

def pack_int64(ds, v):
  ds.write(struct.pack("<q", v))
def unpack_int64(ds):
  return struct.unpack("<q", ds.read(8))[0]

def pack_uint64(ds, v):
  ds.write(struct.pack("<Q", v))
def unpack_uint64(ds):
  return struct.unpack("<Q", ds.read(8))[0]

def pack_int128(ds, v):
  raise Exception("not implementd")
def unpack_int128(ds):
  raise Exception("not implementd")

def pack_uint128(ds, v):
  raise Exception("not implementd")
def unpack_uint128(ds):
  raise Exception("not implementd")

def pack_varint32(ds, v):
  raise Exception("not implementd")
def unpack_varint32(ds):
  raise Exception("not implementd")

def pack_varuint32(ds, v):
  data = b''
  while v >= 0x80:
    data += bytes([(v & 0x7f) | 0x80])
    v >>= 7
  data += bytes([v])
  ds.write(data)
def unpack_varuint32(ds):
  shift = 0
  result = 0
  while True:
    b = ord(ds.read(1))
    result |= ((b & 0x7f) << shift)
    if not (b & 0x80):
      break
    shift += 7
  return result

def pack_float32(ds, v):
  raise Exception("not implementd")
def unpack_float32(ds):
  raise Exception("not implementd")

def pack_float64(ds, v):
  raise Exception("not implementd")
def unpack_float64(ds):
  raise Exception("not implementd")

def pack_float128(ds, v):
  raise Exception("not implementd")
def unpack_float128(ds):
  raise Exception("not implementd")

def pack_time_point(ds, v):
  raise Exception("not implementd")
def unpack_time_point(ds):
  raise Exception("not implementd")

def pack_time_point_sec(ds, v):
  raise Exception("not implementd")
def unpack_time_point_sec(ds):
  raise Exception("not implementd")

def pack_block_timestamp_type(ds, v):
  raise Exception("not implementd")
def unpack_block_timestamp_type(ds):
  raise Exception("not implementd")

def pack_name(ds, v):
  raise Exception("not implementd")
def unpack_name(ds):
  raise Exception("not implementd")

def pack_bytes(ds, v):
  raise Exception("not implementd")
def unpack_bytes(ds):
  raise Exception("not implementd")

def pack_string(ds, v):
  raise Exception("not implementd")
def unpack_string(ds):
  raise Exception("not implementd")

def pack_checksum160(ds, v):
  raise Exception("not implementd")
def unpack_checksum160(ds):
  raise Exception("not implementd")

def pack_checksum256(ds, v):
  raise Exception("not implementd")
def unpack_checksum256(ds):
  raise Exception("not implementd")

def pack_checksum512(ds, v):
  raise Exception("not implementd")
def unpack_checksum512(ds):
  raise Exception("not implementd")

def pack_public_key(ds, v):
  raise Exception("not implementd")
def unpack_public_key(ds):
  raise Exception("not implementd")

def pack_signature(ds, v):
  raise Exception("not implementd")
def unpack_signature(ds):
  raise Exception("not implementd")

def pack_symbol(ds, v):
  raise Exception("not implementd")
def unpack_symbol(ds):
  raise Exception("not implementd")

def pack_symbol_code(ds, v):
  raise Exception("not implementd")
def unpack_symbol_code(ds):
  raise Exception("not implementd")

def pack_asset(ds, v):
  raise Exception("not implementd")
def unpack_asset(ds):
  raise Exception("not implementd")

def pack_extended_asset(ds, v):
  raise Exception("not implementd")
def unpack_extended_asset(ds):
  raise Exception("not implementd")
