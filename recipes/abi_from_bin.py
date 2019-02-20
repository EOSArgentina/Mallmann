#!/usr/bin/env python
import sys
sys.path.append("..")

from collections import OrderedDict
from mallmann import abi_serializer

if len(sys.argv) < 2:
  print("usage: abi_from_bin.py ABI_FILE")
  sys.exit(1)

abi_file = sys.argv[1]
abis = abi_serializer.from_hex(open(abi_file,"r").read())
print(abis.abi_to_json())
