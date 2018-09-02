#!/usr/bin/env python
import sys
sys.path.append("..")

from collections import OrderedDict
from mallmann import abi_serializer

if len(sys.argv) < 2:
  print "usage: abi_to_bin.py ABI_FILE"
  sys.exit(1)

abi_file = sys.argv[1]
abis = abi_serializer.from_file(abi_file)
sys.stdout.write(str(abis.abi_to_bin()).encode('hex'))
