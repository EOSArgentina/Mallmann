import io
import struct
from base58 import b58decode

def char_to_symbol(c):
  if c >= ord('a') and c <= ord('z'):
    return (c - ord('a')) + 6
  if c >= ord('1') and c <= ord('5'):
    return (c - ord('1')) + 1
  return 0

def string_to_name(s):
  name = 0
  i = 0
  while i<len(s) and i < 12:
    name |= (char_to_symbol(ord(s[i])) & 0x1f) << (64 - 5 * (i + 1))
    i += 1
  if i == 12 and i < len(s):
      name |= char_to_symbol(ord(s[12])) & 0x0F
  return name;

def string_to_symbol(precision, s):
  l = len(s)
  if l > 7: raise Exception("invalid symbol {0}".format(s))
  result = 0
  for i in xrange(l):
    if ord(s[i]) < ord('A') or ord(s[i]) > ord('Z'):
      raise Exception("invalid symbol {0}".format(s))
    else:
      result |= (int(ord(s[i])) << (8*(1+i)));
  
  result |= int(precision);
  return result;

def asset_to_uint64_pair(a):
  parts = a.split()
  if len(parts) != 2: raise Exception("invalid asset {0}".format(a))
  
  nums = parts[0].split(".")
  if len(nums) != 2: raise Exception("invalid number {0}".format(parts[0]))

  num = ''.join(nums)
  return int(num), string_to_symbol(len(nums[1]), parts[1])

class DataStream(io.BytesIO):
  
  def pack_array(self, type, values):
    self.pack_varuint32(len(values))
    for v in values:
      getattr(self, 'pack_'+type)(v)

  def pack_bool(self, v):
    self.write(b'\x00') if v else self.write(b'\x01')
  def unpack_bool(self):
    return True if self.read(1) else False

  def pack_int8(self, v):
    self.write(struct.pack("<b", v))
  def unpack_int8(self):
    return struct.unpack("<b", self.read(1))[0]

  def pack_uint8(self, v):
    self.write(struct.pack("<B", v))
  def unpack_uint8(self):
    return struct.unpack("<B", self.read(1))[0]

  def pack_int16(self, v):
    self.write(struct.pack("<h", v))
  def unpack_int16(self):
    return struct.unpack("<h", self.read(2))[0]

  def pack_uint16(self, v):
    self.write(struct.pack("<H", v))
  def unpack_uint16(self):
    return struct.unpack("<H", self.read(2))[0]

  def pack_int32(self, v):
    self.write(struct.pack("<i", v))
  def unpack_int32(self):
    return struct.unpack("<i", self.read(4))[0]

  def pack_uint32(self, v):
    self.write(struct.pack("<I", v))
  def unpack_uint32(self):
    return struct.unpack("<I", self.read(4))[0]

  def pack_int64(self, v):
    self.write(struct.pack("<q", v))
  def unpack_int64(self):
    return struct.unpack("<q", self.read(8))[0]

  def pack_uint64(self, v):
    self.write(struct.pack("<Q", v))
  def unpack_uint64(self):
    return struct.unpack("<Q", self.read(8))[0]

  def pack_int128(self, v):
    raise Exception("not implementd")
  def unpack_int128(self):
    raise Exception("not implementd")

  def pack_uint128(self, v):
    raise Exception("not implementd")
  def unpack_uint128(self):
    raise Exception("not implementd")

  def pack_varint32(self, v):
    raise Exception("not implementd")
  def unpack_varint32(self):
    raise Exception("not implementd")

  def pack_varuint32(self, v):
    val = v
    while True:
      b = val & 0x7f
      val >>= 7
      b |= ((val > 0) << 7)
      self.pack_uint8(b)
      if not val:
        break
  def unpack_varuint32():
    v = 0; b = 0; by = 0
    while True:
      b=self.read(1)[0]
      v |= (b & 0x7f) << by
      by += 7
      if b & 0x80 and by < 32:
        break
    return v

  def pack_float32(self, v):
    raise Exception("not implementd")
  def unpack_float32(self):
    raise Exception("not implementd")

  def pack_float64(self, v):
    raise Exception("not implementd")
  def unpack_float64(self):
    raise Exception("not implementd")

  def pack_float128(self, v):
    raise Exception("not implementd")
  def unpack_float128(self):
    raise Exception("not implementd")

  def pack_time_point(self, v):
    raise Exception("not implementd")
  def unpack_time_point(self):
    raise Exception("not implementd")

  def pack_time_point_sec(self, v):
    raise Exception("not implementd")
  def unpack_time_point_sec(self):
    raise Exception("not implementd")

  def pack_block_timestamp_type(self, v):
    raise Exception("not implementd")
  def unpack_block_timestamp_type(self):
    raise Exception("not implementd")

  def pack_account_name(self, v):
    self.pack_uint64(string_to_name(v))
  def unpack_account_name(self):
    raise Exception("not implementd")

  def pack_name(self, v):
    self.pack_account_name(v)
  def unpack_name(self):
    raise Exception("not implementd")

  def pack_bytes(self, v):
    self.pack_varuint32(len(v))
    self.write(v)
  def unpack_bytes(self):
    raise Exception("not implementd")

  def pack_string(self, v):
    v=str(v)
    self.pack_varuint32(len(v))
    self.write(v)
  def unpack_string(self):
    raise Exception("not implementd")

  def pack_checksum160(self, v):
    raise Exception("not implementd")
  def unpack_checksum160(self):
    raise Exception("not implementd")

  def pack_checksum256(self, v):
    raise Exception("not implementd")
  def unpack_checksum256(self):
    raise Exception("not implementd")

  def pack_checksum512(self, v):
    raise Exception("not implementd")
  def unpack_checksum512(self):
    raise Exception("not implementd")

  def pack_public_key(self, v):
    if v.startswith("EOS"):
      data = b58decode(str(v[3:]))
      if len(data) != 37: raise Exception("invalid k1 key")
      self.pack_uint8(0)
      self.write(data[:-4])
    elif v.startswith("PUB_R1_"):
      raise Exception("not implementd")
    else:
      raise Exception("invalid pubkey format")

  def unpack_public_key(self):
    raise Exception("not implementd")

  def pack_signature(self, v):
    raise Exception("not implementd")
  def unpack_signature(self):
    raise Exception("not implementd")

  def pack_symbol(self, v):
    raise Exception("not implementd")
  def unpack_symbol(self):
    raise Exception("not implementd")

  def pack_symbol_code(self, v):
    raise Exception("not implementd")
  def unpack_symbol_code(self):
    raise Exception("not implementd")

  def pack_asset(self, v):
    a, s = asset_to_uint64_pair(v)
    self.pack_uint64(a)
    self.pack_uint64(s)
  def unpack_asset(self):
    raise Exception("not implementd")

  def pack_extended_asset(self, v):
    raise Exception("not implementd")
  def unpack_extended_asset(self):
    raise Exception("not implementd")
