import json
import struct

class abi_serializer:

  @staticmethod
  def from_dict(abi):
    abis = abi_serializer()
    abis.abi = abi
    return abis

  @staticmethod
  def from_file(file):
    with open(file) as fp:
      return abi_serializer.from_dict(json.loads(fp.read()))